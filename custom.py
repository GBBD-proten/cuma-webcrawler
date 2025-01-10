


def view_custom(view):
    return view.replace('조회', '').replace(' ', '')


def get_number_custom(text):
    return ''.join(filter(str.isdigit, str(text)))
