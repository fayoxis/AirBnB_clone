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


def validate_file(file_path, file_type):
    """
    it will Start to validation of files
    """
    headers = {'Content-Type': "{}; charset=utf-8".format(file_type)}
    # Open files in binary mode:
    # https://requests.readthedocs.io/en/master/user/advanced/
    data = open(file_path, "rb").read()
    url = "https://validator.w3.org/nu/?out=json"
    response = requests.post(url, headers=headers, data=data)

    if not response.status_code < 400:
        raise ConnectionError("Unable to connect to API endpoint.")

    result = []
    messages = response.json().get('messages', [])
    for message in messages:
        # Capture files that have incomplete or broken HTML
        if message['type'] == 'error' or message['type'] == 'info':
            result.append("'{}' => {}".format(file_path, message['message']))
        else:
            result.append("[{}:{}] {}".format(
                file_path, message['lastLine'], message['message']))
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
