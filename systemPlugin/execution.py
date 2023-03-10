

# Copyright: IDG TECHtalk on YouTube
def checkArg(args: list, trigger: tuple):
    """Deprecate: use 'argparse' instead"""
    for idx, arg in enumerate(args):
        if arg in trigger:
            return args[idx + 1]