# import time
import sys




class Logger:
    def msg(self, message: str = '', tpl: str = '{message}{end}', end: str ='\n'):
        message = tpl.format(**{
            'message': message,
            'end': end,
        })

        sys.stdout.write(message)
        sys.stdout.flush()
