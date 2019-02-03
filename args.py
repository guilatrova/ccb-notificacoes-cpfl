import sys

from src.settings import DEV_RECIPIENT, RECIPIENTS


def handle_args():
    if '-me' in sys.argv:
        print('* Emails will only be sent to DEV')
        return {'to': DEV_RECIPIENT}
    else:
        return {'to': RECIPIENTS}
