import argparse




class CLIParser:
    ''' Simple argparse wrapper for the lazy.
        Relevant docs: https://docs.python.org/3/library/argparse.html

        Example conf:
        [
            {
                'arg': ('--bot-dir', '-b'),
                'metavar': 'PATH',
                'type': str,
                'required': True,
                'help': 'Path to bot directory.'
            },
            {
                'arg': ('--mode', '-m'),
                'metavar': 'MODE',
                'type': str,
                'default': None,
                'required': True,
                'choices': ['admin', 'bot', 'log'],
                'help': 'Which module to load.'
            },
            ...,
        ]
    '''
    conf: dict
    parser: argparse.ArgumentParser
    args: dict


    def __init__(self, conf):
        self.conf = conf
        self.parser = argparse.ArgumentParser()

        for arg_conf in self.conf:
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
