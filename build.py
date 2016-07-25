#!/usr/bin/python

"""
build:
        build current project in ~/builds/project_name/branch-suffix directory.
        If suffix not spend - folder don't have "-suffix" part.

Usage:
    build [(-c CMAKE_FLAGS)] [(--suffix DESINATION_SUFFIX)] [(-k KPAPNISO_FLAGS)]
    build (-h | --help)
    build (-v | --version)


Options:
    [(-c CMAKE_FLAGS)|(--cmake CMAKE_FLAGS)]    Spend given CMAKE_FLAGS to cmake build process
    [(--suffix DESINATION_SUFFIX)]                          Append '-DESINATION_SUFFIX' to build dir name after branch
    -h, --help                                              Show this help text
    -v, --version                                           Show version
"""

import os
import docopt
from subprocess import call, check_output
from docopt import docopt

build_dir='/home/intey/builds'

def prepend_D(args):
    return map(lambda a: '-DCMAKE_%s' % a, args)


def prepend_KND(args):
    return map(lambda a: '-DKPAPNISO_%s' % a, args)


def execute_build(build_dir, project_dir, branch_name, cmake_flags=None, kn_flags=None):
    maybeflags=[]
    if cmake_flags is not None:
        maybeflags.extend(prepend_D(cmake_flags.split(',')))
    if kn_flags is not None:
        maybeflags.extend(prepend_KND(kn_flags.split(',')))

    project_name = os.path.basename(project_dir)

    destination = os.path.join(build_dir, project_name, branch_name)
    if not os.path.exists(destination):
        os.makedirs(destination)
    try:

        os.chdir(destination)

        print('call cmake ', " ".join(maybeflags), 'in', destination, 'on', project_dir)
        cmake_command = ['cmake', project_dir]
        cmake_command.extend(maybeflags)
        call(cmake_command)
        call(['make'])
    finally:
        os.chdir(project_dir)

if __name__ == "__main__":
    arguments = docopt(__doc__, version='0.1')

    cmake_flags = arguments['CMAKE_FLAGS']

    kn_flags = arguments['KPAPNISO_FLAGS']

    suffix = arguments['DESINATION_SUFFIX'] or ''

    curr_dir = os.path.dirname(os.path.realpath(__file__))
    print(curr_dir)
    ref = check_output(['%s/gitbranch' % curr_dir,  os.curdir]).decode('utf-8')
    ref = ref.rstrip() # remove '\n'
    branch_name = "_".join(ref.split('/')[-2:]) # replace / with _

    if suffix != '':
        branch_name = branch_name + '-' + suffix

    project_dir = os.path.abspath(os.curdir)

    execute_build(build_dir, project_dir, branch_name, cmake_flags, kn_flags)
