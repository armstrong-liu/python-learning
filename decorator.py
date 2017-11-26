#!/usr/bin/env python
# coding=utf-8
import pdb


class Armstrong(object):
    def __init__(self, func):
        print('Class initialize')
        self.func = func

    def __call__(self):
        print('The name is %s' % self.func())


def log(func):
    def wrapper(*args, **kw):
        print('pring logs')
        func(*args, **kw)
    return wrapper


@Armstrong
def get_content():
    print('Hello World')


if __name__ == '__main__':
    func = get_content
    func()
    pdb.set_trace()
