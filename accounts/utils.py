# Helper functions


def detect_user(user):
    url_to_redirect = None
    if user.role == 1:
        url_to_redirect = 'vendor-dashboard'
    elif user.role == 2:
        url_to_redirect = 'customer-dashboard'
    elif user.role == None and user.is_superadmin:
        url_to_redirect = '/admin'
    return url_to_redirect
