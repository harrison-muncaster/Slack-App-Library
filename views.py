import modal


def blocks_schema(blocks_list):
    schema = {
        **modal.view('modal', 'My Test App'),
        **modal.blocks(blocks_list)
    }
    return schema


def first_view():
    blocks_list = [
        modal.actions([modal.button(text='My Button', value='my_button', action_id='button_1')])
    ]

    schema = {**blocks_schema(blocks_list), **modal.submit('Submit')}
    return schema


def second_view():
    blocks_list = [
        modal.plain_text_object('first'),
        modal.plain_text_object('second')
    ]

    schema = {**blocks_schema(blocks_list), **modal.submit('Submit'), **modal.close('Quit')}
    return schema


print(first_view())