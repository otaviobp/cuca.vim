from collections.abc import Mapping
import errno
import inspect


def foo(flags):
    return flags


class CLICommander:
    def __init__(self, binary_name, cmds):
        self.commands = {
            "bash-completion": self.bash_completion,
            "help": self.help,
        }
        self.commands.update(cmds)
        self.binary_name = binary_name

    def __call(self, func, params, flags):
        sig = inspect.signature(func)
        kwargs = {}
        for a in sig.parameters:
            if a not in ["args", "flags"]:
                if len(params) == 0:
                    print("{}: Invalid number of parameters".format(self.binary_name))
                    return errno.EINVAL
                kwargs[a] = params.pop(0)

        if "args" in sig.parameters:
            kwargs["args"] = params
        else:
            if len(params) > 0:
                print("{}: Invalid number of parameters".format(self.binary_name))
                return errno.EINVAL

        if "flags" in sig.parameters:
            kwargs["flags"] = flags

        return func(**kwargs)

    def __remove_flags(self, args):
        new_args = []
        flags = {}
        for i in args:
            if i.startswith("-"):
                values = i.split("=", 2)
                if len(values) < 2:
                    values.append("")
                flags[values[0]] = values[1]
            else:
                new_args.append(i)

        return new_args, flags

    def run(self, args, parse_flags=foo):
        args, flags = self.__remove_flags(args)
        flags = parse_flags(flags)

        i = 0
        commands = self.commands
        for i in range(len(args)):
            cmd = args[i]
            if cmd not in commands:
                break

            if callable(commands[cmd]):
                return self.__call(commands[cmd], args[i + 1 :], flags)

            if isinstance(commands[cmd], Mapping):
                commands = commands[cmd]
                args = args[i:]
            else:
                return errno.EINVAL

        if "" in commands:
            return self.__call(commands[""], args[i + 1 :], flags)

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
        while isinstance(cmd, Mapping) and args:
            if not args[0] in cmd:
                return
            cmd = cmd[args[0]]
            args = args[1:]

        if not isinstance(cmd, Mapping):
            return
        print(" ".join(cmd.keys() - ["bash-completion"]))

    def help(self, args):
        print("HELP")
