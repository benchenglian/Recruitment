from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from interview.models import DEGREE_TYPE

# Create your models here.
JobTypes = [
    (0,"技术类"),
    (1,"产品类"),
    (2,"运营类"),
    (3,"设计类")
]
Cities = [
    (0,"北京"),
    (1,"上海"),
    (2,"深圳")
]

class Job(models.Model):
    # Translators: 职位实体的翻译
    job_type = models.SmallIntegerField(blank=False,choices=JobTypes,verbose_name=_('职位类别'))
    job_name = models.CharField(max_length=250,blank=False,verbose_name=_('职位名称'))
    job_city = models.SmallIntegerField(choices=Cities,blank=False,verbose_name=_('工作地点'))
    job_responsibility = models.TextField(max_length=1024,verbose_name=_('职位职责'))
    job_requirement = models.TextField(max_length=1024,blank=False,verbose_name=_('职位要求'))
    creator = models.ForeignKey(User,verbose_name=_('创建人'),null=True,on_delete=models.SET_NULL)
    created_date = models.DateTimeField(verbose_name=_('创建日期'),default=datetime.now)
    modifled_date = models.DateTimeField(verbose_name=_('修改日期'),default=datetime.now)

    # blank 设置为 True 时，字段可以为空；设置为 False 时，字段是必须填写的默认为 False
    # choices 用于页面上的选择框标签，需要先提供一个二维的二元元组，第一个元素表示存在数据库内真实的值，第二个表示页面上显示的具体内容
    # verbose_name 该字段显示名称
    # max_length这个属性的值限制字符个数的长度
    # null 设置为 True 时，数据库的字段允许为NULL，而且表单中的空值将会被存储为NULL；设置为 False 时，数据库的字段不允许为NULL；默认为 False
    # default 默认值
    '''
    on_delete:
    on_delete=None, # 删除关联表中的数据时,当前表与其关联的field的行为
    on_delete=models.CASCADE, # 删除关联数据,与之关联也删除
    on_delete=models.DO_NOTHING, # 删除关联数据,什么也不做
    on_delete=models.PROTECT, # 删除关联数据,引发错误ProtectedError
    on_delete=models.SET_NULL, # 删除关联数据,与之关联的值设置为null（前提FK字段需要设置为可空,一对一同理）
    on_delete=models.SET_DEFAULT, # 删除关联数据,与之关联的值设置为默认值（前提FK字段需要设置默认值,一对一同理）
    on_delete=models.SET, # 删除关联数据
    a. 与之关联的值设置为指定值,设置：models.SET(值)
    b. 与之关联的值设置为可执行对象的返回值,设置：models.SET(可执行对象)
    '''
    '''
    models.SmallIntegerField   ---数字   数据库中的字段有：tinyint、smallint、int、bigint.   类似 IntegerField， 不过只允许某个取值范围内的整数。(依赖数据库)
    models.CharField   ---字符串字段  单行输入，用于较短的字符串，如要保存大量文本, 使用 TextField。必须 max_length 参数，django会根据这个参数在数据库层和校验层限制该字段所允许的最大字符数。
    models.TextField   ---字符串=longtext ，一个容量很大的文本字段， admin 管理界面用 <textarea>多行编辑框表示该字段数据。
    models.ForeignKey 用户与栏目是“一对多”关系，所以用ForeignKey,一个用户可以设置多个栏目,此处的user字段对应实际表中的user_id,来自于User表中主键
    models.DateTimeField  ---日期类型 datetime   同DateField的参数
    https://blog.csdn.net/weixin_42575020/article/details/81561074
    '''
    class Meta:
        verbose_name = _('职位')
        verbose_name_plural = _('职位列表')

    def __str__(self):
        return self.job_name


class Resume(models.Model):
    # Translators: 简历实体的翻译
    username = models.CharField(max_length=135, verbose_name=_('姓名'))
    applicant = models.ForeignKey(User, verbose_name=_("申请人"), null=True, on_delete=models.SET_NULL)
    city = models.CharField(max_length=135, verbose_name=_('城市'))
    phone = models.CharField(max_length=135, verbose_name=_('手机号码'))
    email = models.EmailField(max_length=135, blank=True, verbose_name=_('邮箱'))
    apply_position = models.CharField(max_length=135, blank=True, verbose_name=_('应聘职位'))
    born_address = models.CharField(max_length=135, blank=True, verbose_name=_('生源地'))
    gender = models.CharField(max_length=135, blank=True, verbose_name=_('性别'))
    picture = models.ImageField(upload_to='images/', blank=True, verbose_name=_('个人照片'))
    attachment = models.FileField(upload_to='file/', blank=True, verbose_name=_('简历附件'))

    # 学校与学历信息
    bachelor_school = models.CharField(max_length=135, blank=True, verbose_name=_('本科学校'))
    master_school = models.CharField(max_length=135, blank=True, verbose_name=_('研究生学校'))
    doctor_school = models.CharField(max_length=135, blank=True, verbose_name=_('博士生学校'))
    major = models.CharField(max_length=135, blank=True, verbose_name=_('专业'))
    degree = models.CharField(max_length=135, choices=DEGREE_TYPE, blank=True, verbose_name=_('学历'))
    created_date = models.DateTimeField(verbose_name=_("创建日期"), default=datetime.now)
    modified_date = models.DateTimeField(verbose_name=_("修改日期"), auto_now=True)

    # 候选人自我介绍，工作经历，项目经历
    candidate_introduction = models.TextField(max_length=1024, blank=True, verbose_name=_('自我介绍'))
    work_experience = models.TextField(max_length=1024, blank=True, verbose_name=_('工作经历'))
    project_experience = models.TextField(max_length=1024, blank=True, verbose_name=_('项目经历'))

    class Meta:
        verbose_name = _('简历')
        verbose_name_plural = _('简历列表')

    def __str__(self):
        return self.username