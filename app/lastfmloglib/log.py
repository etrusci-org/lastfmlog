# import time
import sys




class Logger:
    # errorFilename: str


    # def __init__(self, prefix: str = '| ', errorFilename: str = 'boo.log') -> None:
    #     pass


    def msg(self, message: str = '', tpl: str = '{message}{end}', end: str ='\n'):
        message = tpl.format(**{
            'message': message,
            'end': end,
        })

        sys.stdout.write(message)
        sys.stdout.flush()
