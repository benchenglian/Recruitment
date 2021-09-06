
from django.contrib import admin,messages
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from interview.models import Candidate
from interview import candidate_fieldset as cf
from interview import dingtalk
from datetime import datetime
from django.db.models import Q
import logging
import csv

from job.models import Resume

logger = logging.getLogger(__name__)

exportable_fields = ('username','city','phone','bachelor_school','master_school','degree','first_result',
                     'first_interviewer_user','second_result','second_interviewer_user','hr_result','hr_score','hr_remark','hr_interviewer_user'
                     )

# 通知一面面试官
def notify_interviewer(modeladmin, request, queryset):
    candidates = ""
    interviewers = ""
    for obj in queryset:
        candidates = obj.username + ";" + candidates
        interviewers = obj.first_interviewer_user.username + ";" + interviewers
    dingtalk.send("候选人 %s 进入面试环境，亲爱的面试官，请准备面试： %s" % (candidates,interviewers))
    messages.add_message(request, messages.INFO, '已成功发送面试通知' )
notify_interviewer.short_description = '通知一面面试官'

# Register your models here.
def  export_model_as_csv (modeladmin,request,queryset): #request用户发起的请求，queryset页面选择的结果集。
    response =  HttpResponse(content_type='text/csv')
    field_list = exportable_fields
    response['Content-Disposition'] = 'attachment; filename=recruitment-candidates-list-%s.csv' % (
        datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
                                       )
    # 写入表头
    writer = csv.writer(response)
    writer.writerow(
        [ queryset.model._meta.get_field(f).verbose_name.title() for f in field_list ] # 页面当中的字段=导出文件的表头
    )
    for obj in queryset:
        # 单行的记录（各个字段的值），写入到CSV文件
        csv_line_values = []
        for field in field_list:
            field_object =queryset.model._meta.get_field(field)
            field_value = field_object.value_from_object(obj)
            csv_line_values.append(field_value)
        writer.writerow(csv_line_values)
    logger.info('%s 导出 %s 条数据' % (request.user,len(queryset)))
    logger.error('%s 导出 %s 条数据' % (request.user,len(queryset)))
    return response

export_model_as_csv.short_description ='导出为CSV文件'
export_model_as_csv.allowed_permissions = ('export',)





# 候选人管理类
class CandidateAdmin(admin.ModelAdmin):
    exclude = ('creator','created_date','modified_date')

    actions = (export_model_as_csv, notify_interviewer,)

    def has_export_permission(self,request):
        opts = self.opts
        return request.user.has_perm('%s.%s' %(opts.app_label,"export"))

    list_display = (
        'username','city','bachelor_school','get_resume','first_score','first_result','first_interviewer_user',
        'second_result','second_interviewer_user','hr_score','hr_result','last_editor'
    )

    # 设置只读
    #readonly_fields = ('first_interviewer_user','second_interviewer_user')

    # 列表设置编辑
    default_list_editable = ('first_interviewer_user','second_interviewer_user',)

    def get_list_editable(self,request):
        group_names = self.get_group_names(request.user)

        if request.user.is_superuser or 'HR' in group_names:
            return self.default_list_editable
        return ()

    # 覆盖此方法
    def get_changelist_instance(self, request):
        self.list_editable = self.get_list_editable(request)
        return super(CandidateAdmin,self).get_changelist_instance(request)

    def get_group_names(self,user):
        group_names = []
        for g in user.groups.all():
            group_names.append(g.name)
        return group_names

    # 对于非管理员，非HR，获取自己是一面面试官或者二面面试官的勾选人集合：s
    def get_queryset(self, request):# 列表页展示默认调用此方法。
        qs = super(CandidateAdmin,self).get_queryset(request)
        group_names = self.get_group_names(request.user)
        if request.user.is_superuser or 'hr' in group_names:
            return qs
        return Candidate.objects.filter(Q(first_interviewer_user = request.user) | Q(second_interviewer_user = request.user)
        )

    def get_resume(self, obj):
        if not obj.phone: # 电话号码为空返回空。
            return ""
        resumes = Resume.objects.filter(phone=obj.phone)
        if resumes and len(resumes) > 0: # 找到简历返回链接地址。
            return mark_safe(u'<a href="/resume/%s" target="_blank">%s</a' % (resumes[0].id, "查看简历")) #通过新页面打开 target="_blank"
        return ""

    get_resume.short_description = '查看简历'
    get_resume.allow_tags = True


    # 面试官不可修改面试官
    def get_readonly_fields(self, request, obj=None):
        group_names = self.get_group_names(request.user)

        if 'interviewer' in group_names:
            logger.info("interviewer is in user's group for %s" % request.user.username)
            return ('first_interviewer_user','second_interviewer_user')
        return ()

    # 筛选条件
    list_filter = ('city','first_result','second_result','hr_result','first_interviewer_user','second_interviewer_user','hr_interviewer_user')

    # 查询字段
    search_fields = ('username','phone','email','bachelor_school')

    # 排序
    ordering = ('hr_result','second_result','first_result')

    # 一面面试官仅填写一面反馈，二面面试官可以填写二面反馈
    def get_fieldsets(self, request, obj = Candidate):
        group_names = self.get_group_names(request.user)
        # obj = cf
        if 'interviewer' in group_names and obj.first_interviewer_user == request.user:
            return cf.default_fieldsets_first
        if 'interviewer' in group_names and obj.second_interviewer_user == request.user:
            return cf.default_fieldsets_second
        return cf.default_fieldsets

    def save_model(self, request, obj, form, change):
        obj.last_editor = request.user.username
        if not obj.creator:
            obj.creator = request.user.username
        obj.modified_date = datetime.now()
        obj.save()

admin.site.register(Candidate,CandidateAdmin) # 注册进来