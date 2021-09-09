'''
Autor: Frank.Lian
Description: 
Date: 2021-05-05 10:53:00
LastEditTime: 2021-09-07 16:07:12
FilePath: /recruitment/job/views.py
Author: ic1129-x0
'''
# Create your views here.
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from job.models import Job, Resume
from job.models import Cities,JobTypes
from django.contrib.auth.mixins import LoginRequiredMixin # 一个类继承多个类
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import permission_required
import logging
Logger = logging.getLogger(__name__)

def joblist(request):
    job_list = Job.objects.order_by('job_type')
    template = loader.get_template('joblist.html')
    context = {'job_list':job_list}

    for job in job_list:
        job.city_name = Cities[job.job_city][1]
        job.job_type = JobTypes[job.job_type][1]

    #return HttpResponse(template.render(context))
    return render(request,'joblist.html',context)

def detail(request,job_id):
    try:
        job = Job.objects.get(pk=job_id)
        job.city_name = Cities[job.job_city][1]
        Logger.info('job info fetched from datebase jobid:%s' % job_id)
    except Job.DoesNotExist:
        raise Http404("Job does not exist")

    return render(request,'job.html',{'job':job})

from django.contrib.auth.models import Group, User


# 这个 URL 仅允许有 创建用户权限的用户访问
#@csrf_exempt
@permission_required('auth.user_add')
def create_hr_user(request):
    if request.method == "GET":
        return render(request, 'create_hr.html', {})
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        hr_group = Group.objects.get(name='HR')
        user = User(is_superuser=False, username=username, is_active=True, is_staff=True)
        user.set_password(password)
        user.save()
        user.groups.add(hr_group)

        messages.add_message(request, messages.INFO, 'user created %s' % username)
        return render(request, 'create_hr.html')
    return render(request, 'create_hr.html')

'''
    直接返回  HTML 内容的视图 （这段代码返回的页面有 XSS 漏洞，能够被攻击者利用）
'''
def detail_resume(request, resume_id):
    try:
        resume = Resume.objects.get(pk=resume_id)
        content = "name: %s <br>  introduction: %s <br>" % (resume.username, resume.candidate_introduction)
        return HttpResponse(content) # (html.escape(content)) 转译，建议直接用render或者继承detailview。
    except Resume.DoesNotExist:
        raise Http404("resume does not exist")

class ResumeCreateView(LoginRequiredMixin, CreateView): # 简历创建视图，类视图
    ### 从 URL 请求参数带入默认值
    def get_initial(self):
        initial = {}
        for x in self.request.GET:
            initial[x] = self.request.GET[x]
        return initial
    # 简历跟当前用户关联
    def form_valid(self, form):
        self.object = form.save(commit=False) # 验证后保存。
        self.object.applicant = self.request.user # 简历申请人，设置为当前登录用户。
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    """    简历职位页面  """
    template_name = 'resume_form.html'
    success_url = '/joblist/'
    model = Resume
    fields = ["username", "city", "phone",
        "email", "apply_position", "gender",
        "bachelor_school", "master_school", "major", "degree", "picture", "attachment",
        "candidate_introduction", "work_experience", "project_experience"]

from django.views.generic.detail import DetailView

class ResumeDetailView(DetailView):
    """   简历详情页    """
    model = Resume
    template_name = 'resume_detail.html'