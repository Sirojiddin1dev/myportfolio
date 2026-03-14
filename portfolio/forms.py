from django import forms

from .models import ContactMessage
from .translation_utils import get_ui_text, normalize_language_code


class ContactMessageForm(forms.ModelForm):
    def __init__(self, *args, language_code='en', **kwargs):
        super().__init__(*args, **kwargs)
        language_code = normalize_language_code(language_code)
        self.fields['first_name'].widget.attrs['placeholder'] = get_ui_text('first_name', language_code)
        self.fields['last_name'].widget.attrs['placeholder'] = get_ui_text('last_name', language_code)
        self.fields['email'].widget.attrs['placeholder'] = get_ui_text('email', language_code)
        self.fields['subject'].widget.attrs['placeholder'] = get_ui_text('subject', language_code)
        self.fields['message'].widget.attrs['placeholder'] = get_ui_text('message_placeholder', language_code)

    class Meta:
        model = ContactMessage
        fields = ['first_name', 'last_name', 'email', 'subject', 'message']
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control transition-all placeholder-[#fff] focus:outline-0 focus:shadow-none focus:border-b-[#fe3e57] focus:bg-transparent base-font text-[#FFF] text-[14px] pr-[12px] py-[6px] bg-transparent w-full h-[50px] border-[0px] border-b-[1px] border-[#464646]',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control transition-all placeholder-[#fff] focus:outline-0 focus:shadow-none focus:border-b-[#fe3e57] focus:bg-transparent base-font text-[#FFF] text-[14px] pr-[12px] py-[6px] bg-transparent w-full h-[50px] border-[0px] border-b-[1px] border-[#464646]',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control transition-all placeholder-[#fff] focus:outline-0 focus:shadow-none focus:border-b-[#fe3e57] focus:bg-transparent base-font text-[#FFF] text-[14px] pr-[12px] py-[6px] bg-transparent w-full h-[50px] border-[0px] border-b-[1px] border-[#464646]',
                }
            ),
            'subject': forms.TextInput(
                attrs={
                    'class': 'form-control transition-all placeholder-[#fff] focus:outline-0 focus:shadow-none focus:border-b-[#fe3e57] focus:bg-transparent base-font text-[#FFF] text-[14px] pr-[12px] py-[6px] bg-transparent w-full h-[50px] border-[0px] border-b-[1px] border-[#464646]',
                }
            ),
            'message': forms.Textarea(
                attrs={
                    'class': 'form-control transition-all placeholder-[#fff] focus:outline-0 focus:shadow-none focus:border-b-[#fe3e57] focus:bg-transparent base-font text-[#FFF] text-[14px] pr-[12px] py-[6px] bg-transparent w-full h-[175px] sm:h-[90px] border-[0px] border-b-[1px] border-[#464646]',
                    'rows': 5,
                }
            ),
        }
