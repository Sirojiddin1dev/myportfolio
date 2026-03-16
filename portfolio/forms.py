from django import forms

from .models import ContactMessage
from .translation_utils import get_ui_text, normalize_language_code


class ContactMessageForm(forms.ModelForm):
    def __init__(self, *args, language_code='en', **kwargs):
        super().__init__(*args, **kwargs)
        language_code = normalize_language_code(language_code)
        field_config = {
            'first_name': {
                'label': get_ui_text('first_name', language_code),
                'autocomplete': 'given-name',
            },
            'last_name': {
                'label': get_ui_text('last_name', language_code),
                'autocomplete': 'family-name',
            },
            'email': {
                'label': get_ui_text('email', language_code),
                'autocomplete': 'email',
            },
            'subject': {
                'label': get_ui_text('subject', language_code),
                'autocomplete': 'off',
            },
            'message': {
                'label': get_ui_text('message_placeholder', language_code),
                'autocomplete': 'off',
            },
        }

        for field_name, config in field_config.items():
            field = self.fields[field_name]
            field.label = config['label']
            field.widget.attrs.update(
                {
                    'placeholder': config['label'],
                    'aria-label': config['label'],
                    'autocomplete': config['autocomplete'],
                }
            )

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
                    'inputmode': 'email',
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
