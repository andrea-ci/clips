# Clips

A simple parser for building graceful command-line interfaces, with chained commands and colorful usage messages. Clips uses [getopt](https://docs.python.org/3/library/getopt.html) for parsing command arguments and options (scanning mode is GNU-flavoured).

Colors are implemented through ANSI codes and they are not expected to work on Windows. More generally, please note that Clips is not tested for Windows environment.

# Quick start

Install with *pip*:

`pip install clips`

# Usage example

A console with a chained command:

```
from clips import ArgParser

# init console
console = ArgParser(
    'myconsole',                # prog. name
    description=description,    # prog. description
    banner=banner               # usage banner
)

# add a console-level argument
console.add_argument('-v', '--version', help='Show version')

# add a console command
cmd = console.add_command('command', help='A command')

# add a subcommand
subcmd = cmd.add_command('subcommand', help='A subcommand')

# add an argument to subcommand
subcmd.add_argument('arg', help='Argument for this subcommand')
```

Parsing method returns a dictionary of user context,

```
# parse arguments
args = console.parse_args(['command', 'subcommand', 'this'])
print(args)
```

so that output is:

```
{
    '-h': False,
    '--help': False,
    '-v': False,
    '--version': False,
    'command': True,
    'subcommand': True,
    'arg': 'this'
}
```

Argument can have default values:

```
console.add_argument('-o', '--opt', valued=True, default=10)
```

To display usage help:

```
# console-level usage
print(console.usage_help())

# command-level usage
print(console.usage_help(['command']))
print(console.usage_help(['command', 'subcommand']))

```

To disable internal management of help option:

```
# init console
console = ArgParser(
    'myconsole',                # prog. name
    add_help=False              # no help hook
)
```

Use colors for title and text:

```
# init console
console = ArgParser(
    'myconsole',                # prog. name
    title_fg='orange',          # title foreground color
    title_bg='green',           # title background color
    text_fg='green',            # text foreground color
    text_bg='orange'            # text background color
    )
```

Group commands by sections (this affects only usage help):

```
# create section with commands
console.add_section('First section')
cmd1 = console.add_command('cmd1')
cmd2 = console.add_command('cmd2')

# another section
console.add_section('Second section')
cmd3 = console.add_command('cmd3')
cmd4 = console.add_command('cmd4')
```

Available colors for titles and text parts:
- foreground: *black*, *red*, *green*, *orange*, *blue*, *cyan*, *lightgrey*, *darkgrey*, *lightred*, *lightgreen*, *yellow*, *lightblue*, *pink*, *lightcyan*
- background: *black*, *red*, *green*, *orange*, *blue*, *purple*, *cyan*, *lightgrey*
