import subprocess
import re
import os

def get_args():
    """
    Builds and returns needed arguments for subprocess other than stdin, stdout and stderr
    """

    args = {    
        'shell': True,
        'encoding': 'UTF-8'
    }

    if hasattr(subprocess, 'STARTUPINFO'):
        # Windows specific arguments
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        encoding = get_codepage()

        args.update({    
            'startupinfo': si,
            'env': os.environ,
            'encoding': encoding
        })

    return args

def get_codepage():
    """
    Returns active code page for Windows
    """

    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    cp = subprocess.check_output(
        "chcp 65001",
        stdin = subprocess.PIPE,
        stderr = subprocess.PIPE,
        startupinfo = si,
        shell = True,
        env = os.environ,
        timeout = 5
    )
    match = re.search(rb"(\d+)\s*$", cp)
    if match is None:
        raise ValueError("Could not determine active Windows code page")

    return "cp" + match.group(1).decode("ascii")
