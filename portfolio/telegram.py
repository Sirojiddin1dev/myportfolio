import json
import logging
from urllib import error, parse, request

from django.conf import settings


logger = logging.getLogger(__name__)


def _build_contact_message_text(contact_message):
    full_name = ' '.join(
        part for part in [contact_message.first_name, contact_message.last_name] if part
    )
    language_label = dict(contact_message._meta.get_field('language_code').choices).get(
        contact_message.language_code,
        contact_message.language_code,
    )
    return (
        'Yangi ariza keldi!\n\n'
        f'Ism: {full_name or "-"}\n'
        f'Email: {contact_message.email}\n'
        f'Mavzu: {contact_message.subject}\n'
        f'Til: {language_label}\n\n'
        'Xabar:\n'
        f'{contact_message.message}'
    )


def send_contact_message_notification(contact_message):
    bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '').strip()
    chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', '').strip()
    if not bot_token or not chat_id:
        return False

    payload = parse.urlencode(
        {
            'chat_id': chat_id,
            'text': _build_contact_message_text(contact_message),
        }
    ).encode('utf-8')
    api_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

    try:
        with request.urlopen(api_url, data=payload, timeout=10) as response:
            response_data = json.loads(response.read().decode('utf-8'))
    except (error.URLError, error.HTTPError, TimeoutError, json.JSONDecodeError) as exc:
        logger.warning('Telegram notification failed for contact message %s: %s', contact_message.pk, exc)
        return False

    if not response_data.get('ok'):
        logger.warning(
            'Telegram notification was rejected for contact message %s: %s',
            contact_message.pk,
            response_data,
        )
        return False

    return True
