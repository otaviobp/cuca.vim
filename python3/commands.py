from collections.abc import Mapping
import errno
import inspect


class CLICommander:
    def __init__(self, binary_name, cmds):
        self.commands = {
            "bash-completion": self.bash_completion,
            "help": self.help,
        }
        self.commands.update(cmds)
        self.binary_name = binary_name

    def __call(self, func, params):
        sig = inspect.signature(func)

        if "args" in sig.parameters:
            return func(args=params)

        if len(params) != len(sig.parameters):
            print("{}: Invalid number of parameters".format(self.binary_name))
            return errno.EINVAL

        return func(*params)

    def run(self, args):
        i = 0
        commands = self.commands
        for i in range(len(args)):
            cmd = args[i]
            if cmd not in commands:
                break

            if callable(commands[cmd]):
                return self.__call(commands[cmd], args[i + 1 :])

            if isinstance(commands[cmd], Mapping):
                commands = commands[cmd]
                args = args[i:]
            else:
                return errno.EINVAL

        if "" in commands:
            return self.__call(commands[""], args[i + 1 :])

        print(
            '{}: "{}" is not a valid {} command'.format(
                self.binary_name, " ".join(args), self.binary_name
            )
        )
        return errno.EPERM

    def bash_completion(self, args=None):
        if not args:
            args = []

        args = args[1:-1]
        cmd = self.commands
        while type(cmd) is dict and args:
            if not args[0] in cmd:
                return
            cmd = cmd[args[0]]
            args = args[1:]

        if type(cmd) is not dict:
            return
        print(" ".join(cmd.keys() - ["bash-completion"]))

    def help(self, args):
        print("HELP")
