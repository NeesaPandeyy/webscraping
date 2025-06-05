# from django import forms

# from .models import NewsPost


# class NewsPostForm(forms.ModelForm):
#     class Meta:
#         model = NewsPost
#         fields = ["title", "description", "category", "tags", "status"]

from ckeditor.widgets import CKEditorWidget
from django import forms

from .models import NewsPost


class NewsPostAdminForm(forms.ModelForm):
    class Meta:
        model = NewsPost
        fields = "__all__"
        widgets = {
            "description": CKEditorWidget(config_name="default"),
        }
