#!/usr/bin/python3

"""
build:
    build current project in ~/builds/project_name/branch-suffix directory.
    If suffix not spend - folder don't have "-suffix" part.

Usage:
    build [(-c CMAKE_FLAGS)...] [(--suffix DESINATION_SUFFIX)]
        [(-k KPAPNISO_FLAGS)...] [(-j PROCS)]
    build dst [(-b| --bin)]
    build config
    build (-h | --help)
    build (-v | --version)

Commands:
    dst                                             Get destination folder path
    config                                          Configure build toolset.
        This changes .build.cfg file in project main dir

Options:
    [(-b | --bin)]                                  Append 'bin' to destination
    [(-c CMAKE_FLAGS)|(--cmake CMAKE_FLAGS)]        Spend given CMAKE_FLAGS to
        cmake build process. This flags will be prepend with 'CMAKE_'
    [(-k CMAKE_FLAGS)|(--kpapniso KPAPNISO_FLAGS)]  Spend given KPAPNISO_FLAGS
        to cmake build process. This flags will be prepended with 'KPAPNISO_'
    [(--suffix DESINATION_SUFFIX)]                  Append '-DESINATION_SUFFIX'
        to build dir name after branch
    [-j PROCS]                                      make -j PROCS
    -h, --help                                      Show this help text
    -v, --version                                   Show version
"""

import sys
import os
import docopt
from subprocess import call
from docopt import docopt
import re
from configparser import ConfigParser


def git_branch():
    line = open('.git/HEAD').readline()
    col = re.search('heads/', line).end()
    return line[col::].strip().replace('/', '_')


def gen_destination(build_dir, project_dir, branch_name):
    project_name = os.path.basename(project_dir)
    destination = os.path.join(build_dir, project_name, branch_name)
    if not os.path.exists(destination):
        os.makedirs(destination)
    return destination


def prepend(group, args):
    return map(lambda arg: '-D%s_%s' % (group, arg), args)


def execute_build(destination, project_dir, cmake_flags=None, project_flags=None,
                  makeJ=None):
    group = None
    try:
        group = parser.get('COMMON','project_group')
    except:
        print("for project keys, set 'project_group' in ~/.build.cfg")
        print("group flags was not be executed")

    maybeflags=[]
    if cmake_flags is not None:
        # flags = parser.get('COMMON','cmake_flags')
        maybeflags.extend(prepend("CMAKE", cmake_flags))
    if group is not None:
        maybeflags.extend(prepend(group, project_flags))
        try:
            flags = parser.get('COMMON', 'project_flags').split()
        except:
            pass  # skip unexist flags
        maybeflags.extend(prepend(group, flags))
    try:
        os.chdir(destination)
        cmake_command = ['cmake', project_dir]
        cmake_command.extend(maybeflags)
        print('call cmake:', ' '.join(cmake_command),
              'in', os.getcwd(),
              'on', project_dir)
        print('=============================================================')

        call(cmake_command)
        if makeJ:
            call(['make', '-j', makeJ])
        else:
            call(['make'])

    finally:
        os.chdir(project_dir)


if __name__ == "__main__":
    arguments = docopt(__doc__, version='0.1')
    cmake_flags = arguments['CMAKE_FLAGS']
    kn_flags = arguments['KPAPNISO_FLAGS']
    suffix = arguments['DESINATION_SUFFIX'] or ''
    makeJ = arguments['PROCS']

    parser = ConfigParser()

    home = os.environ['HOME']

    config_path = os.path.join(home, '.build.cfg')
    parser.read(config_path)

    build_dir = os.path.join(home, 'builds')

    project_dir = os.getcwd()
    branch = git_branch()
    if suffix != '':
        branch = branch + '-' + suffix
    destination = gen_destination(build_dir, project_dir, branch)

    if arguments['dst']:
        if arguments['-b']:
            print(destination+'/bin')
        else:
            print(destination)
        sys.exit(0)

    if arguments['config']:
        call([parser.get('COMMON', 'editor'), config_path])
        sys.exit(0)

    else:
        execute_build(destination, project_dir, cmake_flags, kn_flags, makeJ)
