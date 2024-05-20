from flask import request


def main():
    year = int(request.args.get('year'))
    month = int(request.args.get('month'))
    return f'the year is :{year}- and month is {month}'
