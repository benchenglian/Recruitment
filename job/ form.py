'''
Author: Frank.Lian
Description: 
Date: 2021-09-10 17:00:53
LastEditTime: 2021-09-10 17:01:21
FilePath: /recruitment/job/ form.py
'''
from django.forms import ModelForm

from .models import Resume


class ResumeForm(ModelForm):
    class Meta:
        model = Resume

        fields = ["username", "city", "phone",
        "email", "apply_position", "born_address", "gender", "picture", "attachment",
        "bachelor_school", "master_school", "major", "degree", 
        "candidate_introduction", "work_experience", "project_experience"]