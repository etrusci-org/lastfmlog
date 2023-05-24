import argparse




class CLIParser:
    ''' Simple argparse wrapper for the lazy.
        Relevant docs: https://docs.python.org/3/library/argparse.html

        Example Conf
        conf = {
            'info': {
                'prog': 'app.py',
                'description': 'This does something.',
                'epilog': 'Copyright or whatever',
            },
            'args': [
                {
                    'arg': 'action',
                    'metavar': 'ACTION',
                    'type': str,
                    'choices': ['update'],
                    'help': 'Do something.',
                },
                {
                    'arg': '--updatefromstart',
                    'action': 'store_true',
                    'help': 'Fetch tracks from the beginning of time.',
                },
                {
                    'arg': ['-d', '--datadir'],
                    'metavar': 'PATH',
                    'type': str,
                    'required': False,
                    'default': '/tmp/foo',
                    'help': 'Override default data directory path.',
                },
            ],
        }
    '''
    conf: dict
    parser: argparse.ArgumentParser
    args: dict


    def __init__(self, conf) -> None:
        self.conf = conf
        self.parser = argparse.ArgumentParser()
        self.parser.prog = self.conf['info']['prog']
        self.parser.description = self.conf['info']['description']
        self.parser.epilog = self.conf['info']['epilog']
        for arg_conf in self.conf['args']:
            if isinstance(arg_conf['arg'], str):
                arg = arg_conf['arg']
                del arg_conf['arg']
                self.parser.add_argument(arg, **arg_conf)
            elif isinstance(arg_conf['arg'], list):
                arg_long, arg_short = arg_conf['arg']
                del arg_conf['arg']
                self.parser.add_argument(arg_long, arg_short, **arg_conf)
            else:
                print('Invalid argument conf:', arg_conf['arg'])


    def parseArgs(self) -> dict:
        if self.parser:
            self.args = self.parser.parse_args()
        return vars(self.args)


    def printHelp(self) -> None:
        self.parser.print_help()
