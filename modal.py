# Author: Harrison Muncaster
# Purpose: Library to be used to easily build Modal Views for Slack Applications
# PY Version: Python 3.9

def view(**kwargs: str) -> dict:
    """Return dict that represents the TYPE of view. ie. modal vs home view."""
    schema = {
        'type': kwargs['type'],
        'title': plain_text_object(kwargs['text'])
    }
    return schema


def submit(text: str) -> dict:
    """Return dict that represents the SUBMIT button."""
    schema = {
        'submit': plain_text_object(text)
    }
    return schema


def close(text: str) -> dict:
    """Return dict that represents the CLOSE button."""
    schema = {
        'close': plain_text_object(text)
    }
    return schema


def header(text: str) -> dict:
    """Return dict that represents a HEADER."""
    schema = {
        'type': 'header',
        'text': plain_text_object(text)
    }
    return schema


def divider() -> dict:
    """Return dict that represents a DIVIDER."""
    schema = {
        'type': 'divider'
    }
    return schema


def plain_text_object(text: str) -> dict:
    """Return dict that represents a PLAIN_TEXT text section."""
    schema = {
        'type': 'plain_text',
        'text': text,
        'emoji': True
    }
    return schema


def mrkdwn_object(text: str) -> dict:
    """Return dict that represents a MRKDWN text section."""
    schema = {
        'type': 'mrkdwn',
        'text': text
    }
    return schema


def confirm(**kwargs: str) -> dict:
    """Return dict of CONFIRM section to be appended to an INPUT or ACTION block."""
    schema = {
        'title': {
            'type': 'plain_text',
            'text': kwargs['confirm_title']
        },
        'text': {
            'type': 'mrkdwn',
            'text': kwargs['confirm_text']
        },
        'confirm': {
            'type': 'plain_text',
            'text': kwargs['confirm_approve_text']
        },
        'deny': {
            'type': 'plain_text',
            'text': kwargs['confirm_deny_text']
        }
    }
    return schema


def blocks(blocks_list: list) -> dict:
    """Return dict that represents the entire BLOCKS section."""
    schema = {
        'blocks': blocks_list
    }
    return schema


def section(**kwargs: [str, list]) -> dict:
    """Return dict that represents a SECTION block."""
    schema = {
        'type': 'section',
        'text': mrkdwn_object(kwargs['section_text'])
    }
    if kwargs.get('type'):
        if kwargs['type'] == 'button':
            schema = {**schema, **{'accessory': button(**kwargs)}}

        elif kwargs['type'] == 'image':
            schema = {**schema, **{'accessory': image(**kwargs)}}

        elif kwargs['type'] == 'datepicker':
            schema = {**schema, **{'accessory': datepicker(**kwargs)}}

        elif kwargs['type'] == 'timepicker':
            schema = {**schema, **{'accessory': timepicker(**kwargs)}}

        elif kwargs['type'] == 'static_select' or kwargs['type'] == 'multi_static_select':
            schema = {**schema, **{'accessory': static_select(**kwargs)}}

        elif kwargs['type'] == 'users_select' or kwargs['type'] == 'multi_users_select':
            schema = {**schema, **{'accessory': users_select(**kwargs)}}

        elif kwargs['type'] == 'checkboxes':
            schema = {**schema, **{'accessory': checkboxes(**kwargs)}}

        elif kwargs['type'] == 'radio_buttons':
            schema = {**schema, **{'accessory': radio_buttons(**kwargs)}}

        elif kwargs['type'] == 'overflow':
            schema = {**schema, **{'accessory': overflow(**kwargs)}}

        elif kwargs['type'] == 'fields':
            schema = {'type': 'section', 'fields': [mrkdwn_object(item) for item in kwargs['fields_list']]}

    return schema


def actions(items: list) -> dict:
    """Return dict that represents an ACTION block."""
    schema = {
        'type': 'actions',
        'elements': items
    }
    return schema


def input_type(**kwargs: str) -> dict:
    """Return dict that represents an INPUT block."""
    schema = {
        'type': 'input'
    }
    if kwargs['type'] == 'plain_text_input':
        schema = {**schema, **{'element': plain_text_input(**kwargs)}}

    elif kwargs['type'] == 'datepicker':
        schema = {**schema, **{'element': datepicker(**kwargs)}}

    elif kwargs['type'] == 'timepicker':
        schema = {**schema, **{'element': timepicker(**kwargs)}}

    elif kwargs['type'] == 'static_select' or kwargs['type'] == 'multi_static_select':
        schema = {**schema, **{'element': static_select(**kwargs)}}

    elif kwargs['type'] == 'conversations_select' or kwargs['type'] == 'multi_conversations_select':
        schema = {**schema, **{'element': conversations_select(**kwargs)}}

    elif kwargs['type'] == 'channels_select' or kwargs['type'] == 'multi_channels_select':
        schema = {**schema, **{'element': channels_select(**kwargs)}}

    elif kwargs['type'] == 'users_select' or kwargs['type'] == 'multi_users_select':
        schema = {**schema, **{'element': users_select(**kwargs)}}

    elif kwargs['type'] == 'checkboxes':
        schema = {**schema, **{'element': checkboxes(**kwargs)}}

    elif kwargs['type'] == 'radio_buttons':
        schema = {**schema, **{'element': radio_buttons(**kwargs)}}

    if kwargs.get('optional'):
        schema = {**schema, **{'optional': kwargs['optional']}}

    schema = {**schema, **{'label': plain_text_object(kwargs['label'])}}
    return schema


def option_items(items: [str, list]) -> list:
    """Return list that represents items belonging OPTIONS key in ACCESSORY block."""
    if isinstance(items[0], str):
        options = [{'text': plain_text_object(item), 'value': item} for item in items]
    else:
        options = [{'text': mrkdwn_object(item['text']),
                    'description': mrkdwn_object(item['description']),
                    'value': item['value']} for item in items]
    return options


def button(**kwargs: [str, dict]) -> dict:
    """Return dict that represents a BUTTON action
    to be appended to an ACTIONS or SECTIONS block."""
    schema = {
        'type': 'button',
        'text': plain_text_object(kwargs['text']),
        'value': kwargs['value'],
        'action_id': kwargs['action_id']
    }
    if kwargs.get('url'):
        schema = {**schema, 'url': kwargs['url']}

    if (kwargs.get('confirm_title')
        and kwargs.get('confirm_text')
        and kwargs.get('confirm_approve_text')
            and kwargs.get('confirm_deny_text')):
        schema = {**schema, **{'confirm': confirm(**kwargs)}}

    return schema


def plain_text_input(**kwargs: str) -> dict:
    """Return dict that represents a PLAIN_TEXT_INPUT action
    to be appended to an ACTIONS, SECTION, or INPUT block."""
    schema = {
        'type': 'plain_text_input',
        'action_id': kwargs['action_id']
    }
    if kwargs.get('placeholder'):
        schema = {**schema, **{'placeholder': plain_text_object(kwargs['placeholder'])}}

    if kwargs.get('multiline'):
        schema = {**schema, **{'multiline': kwargs['multiline']}}

    return schema


def static_select(**kwargs: [str, list]) -> dict:
    """Return dict that represents a STATIC_SELECT or MULTI_STATIC_SELECT action
    to be appended to an ACTIONS, SECTION, or INPUT block."""
    schema = {
        'type': kwargs['type'],
        'options': option_items(kwargs['options']),
        'action_id': kwargs['action_id']
    }
    if kwargs.get('placeholder'):
        schema = {**schema, **{'placeholder': plain_text_object(kwargs['placeholder'])}}

    return schema


def conversations_select(**kwargs: str) -> dict:
    """Return dict that represents a CONVERSATIONS_SELECT or MULTI_CONVERSATIONS_SELECT
    action to be appended to an ACTIONS, SECTION, or INPUT block."""
    schema = {
        'type': kwargs['type'],
        'action_id': kwargs['action_id']
    }
    if kwargs.get('placeholder'):
        schema = {**schema, **{'placeholder': plain_text_object(kwargs['placeholder'])}}

    if kwargs.get('initial_convo'):
        schema = {**schema, **{'initial_user': kwargs['initial_convo']}}

    return schema


def users_select(**kwargs: str) -> dict:
    """Return dict that represents a USERS_SELECT or MULTI_USERS_SELECT action
    to be appended to an ACTIONS, SECTION, or INPUT block."""
    schema = {
        'type': kwargs['type'],
        'action_id': kwargs['action_id']
    }
    if kwargs.get('placeholder'):
        schema = {**schema, **{'placeholder': plain_text_object(kwargs['placeholder'])}}

    if kwargs.get('initial_user'):
        schema = {**schema, **{'initial_user': kwargs['initial_user']}}

    return schema


def channels_select(**kwargs: str) -> dict:
    """Return dict that represents a CHANNELS_SELECT or MULTI_CHANNELS_SELECT action
    to be appended to an ACTIONS, SECTION, or INPUT block."""
    schema = {
        'type': kwargs['type'],
        'action_id': kwargs['action_id']
    }
    if kwargs.get('placeholder'):
        schema = {**schema, **{'placeholder': plain_text_object(kwargs['placeholder'])}}

    if kwargs.get('initial_channel'):
        schema = {**schema, **{'initial_channel': kwargs['initial_channel']}}

    return schema


def datepicker(**kwargs: str) -> dict:
    """Return dict that represents a DATEPICKER action
    to be appended to an ACTIONS, SECTION, or INPUT block."""
    schema = {
        'type': 'datepicker',
        'action_id': kwargs['action_id']
    }
    if kwargs.get('placeholder'):
        schema = {**schema, **{'placeholder': plain_text_object(kwargs['placeholder'])}}

    if kwargs.get('initial_date'):
        schema = {**schema, **{'initial_date': kwargs['initial_date']}}

    return schema


def timepicker(**kwargs: str) -> dict:
    """Return dict that represents a TIMEPICKER action
    to be appended to an ACTIONS, SECTION, or INPUT block."""
    schema = {
        'type': 'timepicker',
        'action_id': kwargs['action_id']
    }
    if kwargs.get('placeholder'):
        schema = {**schema, **{'placeholder': plain_text_object(kwargs['placeholder'])}}

    if kwargs.get('initial_time'):
        schema = {**schema, **{'initial_time': kwargs['initial_time']}}

    return schema


def checkboxes(**kwargs: [str, list]) -> dict:
    """Return dict that represents a CHECKBOXES action
    to be appended to an ACTIONS, SECTION, or INPUT block."""
    schema = {
        'type': 'checkboxes',
        'options': option_items(kwargs['options']),
        'action_id': kwargs['action_id']
    }
    return schema


def radio_buttons(**kwargs: [str, list]) -> dict:
    """Return dict that represents a RADIO BUTTONS action
    to be appended to an ACTIONS, SECTION, or INPUT block."""
    schema = {
        'type': 'radio_buttons',
        'options': option_items(kwargs['options']),
        'action_id': kwargs['action_id']
    }
    return schema


def overflow(**kwargs: [str, list]) -> dict:
    """Return dict that represents an OVERFLOW action
    to be appended to an ACTIONS, SECTION, or INPUT block."""
    schema = {
        'type': 'overflow',
        'options': option_items(kwargs['options']),
        'action_id': kwargs['action_id']
    }
    return schema


def image(**kwargs: str) -> dict:
    """Return dict that represents an IMAGE item to be
    appended to a SECTION block."""
    schema = {
        'type': 'image',
        'image_url': kwargs['image_url'],
        'alt_text': kwargs['alt_text']
    }
    if kwargs.get('title'):
        schema = {**schema, **{'title': plain_text_object(kwargs['title'])}}

    return schema
