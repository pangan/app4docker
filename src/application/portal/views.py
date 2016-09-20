from portal import portal


@portal.route('/')
def index():
    return 'This is index!'
