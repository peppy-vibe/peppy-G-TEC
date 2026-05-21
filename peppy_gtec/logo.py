
LINE_TYPE_01 = '''══════════════════════════════════════════════'''

LINE_TYPE_02 = '''______________________________________________'''

LINE_TYPE_03 = '''||||||||||||||||||||||||||||||||||||||||||||||'''

LOGO = r'''                                        v1.1.0
    ██████╗      ████████╗███████╗ ██████╗
   ██╔════╝      ╚══██╔══╝██╔════╝██╔════╝
   ██║  ███╗█████╗  ██║   █████╗  ██║
   ██║   ██║╚════╝  ██║   ██╔══╝  ██║
   ╚██████╔╝        ██║   ███████╗╚██████╗
    ╚═════╝         ╚═╝   ╚══════╝ ╚═════╝
             Unleash Green Energy'''


SHOTCUTS = ''' [CTRL+ALT+E] \033[32mEnforce\033[0m  [CTRL+ALT+R] \033[31mRelease\033[0m
 [CTRL+ALT+C] \033[33mCancel\033[0m   [  CTRL+C  ] Quit'''


def print_logo():
    """Print the logo and optionally the instructions."""
    logo = [
        LINE_TYPE_01,
        LOGO,
        LINE_TYPE_01,
    ]
    print('\n'.join(logo))

def print_instructions():
    """Print the instructions."""
    instructions = [
        SHOTCUTS,
        LINE_TYPE_01,
    ]
    print('\n'.join(instructions))

if __name__ == '__main__':
    print_logo()
    print_instructions()