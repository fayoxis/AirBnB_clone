#!/usr/bin/python3
"""
W3C validator for best School

For HTML and CSS files.

Based on 2 APIs:

- https://validator.w3.org/nu/
- http://jigsaw.w3.org/css-validator/validator


Usage:

Simple file:

```
./w3c_validator.py index.html
```

Multiple files:

"""
import sys
import requests


def __print_stdout(msg):
    """this will Print a message in STDOUT
    """
    sys.stdout.write(msg)


def __print_stderr(msg):
    """this will Print a message in STDERR
    """
    sys.stderr.write(msg)


import requests

def analyse_html(file_path):
    """Analyze HTML file"""
    headers = {'Content-Type': "text/html; charset=utf-8"}
    data = open(file_path, "rb").read()
    url = "https://validator.w3.org/nu/?out=json"
    response = requests.post(url, headers=headers, data=data)
    result = []
    messages = response.json().get('messages', [])
    for message in messages:
        result.append("[{}:{}] {}".format(file_path, message['lastLine'], message['message']))
    return result


def analyse_css(file_path):
    """Analyze CSS file"""
    data = {'output': "json"}
    files = {'file': (file_path, open(file_path, 'rb'), 'text/css')}
    url = "http://jigsaw.w3.org/css-validator/validator"
    response = requests.post(url, data=data, files=files)
    result = []
    errors = response.json().get('cssvalidation', {}).get('errors', [])
    for error in errors:
        result.append("[{}:{}] {}".format(file_path, error['line'], error['message']))
    return result

def __analyse(file_path):
    nb_errors = 0
    try:
        result = None
        if file_path.endswith('.css'):
            result = __analyse_css(file_path)
        else:
            result = __analyse_html(file_path)

        if len(result) > 0:
            for msg in result:
                __print_stderr("{}\n".format(msg))
                nb_errors += 1
        else:
            __print_stdout("{}: OK\n".format(file_path))

    except Exception as e:
        __print_stderr("[{}] {}\n".format(e.__class__.__name__, e))
    return nb_errors


def __files_loop():
    nb_errors = 0
    for file_path in sys.argv[1:]:
        nb_errors += __analyse(file_path)

    return nb_errors


if __name__ == "__main__":
    """ this appears like the Main
    """
    if len(sys.argv) < 2:
        __print_stderr("usage: w3c_validator.py file1 file2 ...\n")
        exit(1)
    sys.exit(__files_loop())
