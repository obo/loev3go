#!/usr/bin/python

import os, sys
import optparse

try:
    here = __file__
except NameError:
    here = sys.argv[0]

parser = optparse.OptionParser(usage='%prog [OPTIONS]')
parser.add_option(
    '-c', '--console',
    help="Run the interpreter in the console (not the GUI)",
    action="store_true",
    dest="console")
parser.add_option(
    '-q', '--quit',
    help="Quit after loading and running files",
    action="store_true",
    dest="quit_after")
parser.add_option(
    '--doctest',
    help="Doctest the given (text) files",
    action="store_true",
    dest="doctest")

from pylogo import Logo

def main():
    doit(sys.argv[1:])

def doit(args):
    options, filenames = parser.parse_args(args)
    if options.doctest:
        from pylogo.logodoctest import testfile
        import doctest
        for fn in filenames:
            print '-- Testing %s %s' % (fn, '-'*(40-len(fn)))
            testfile(fn, optionflags=doctest.ELLIPSIS,
                     verbose_summary=True,
                     interp=Logo)
    else:
        for filename in filenames:
            Logo.import_logo(filename)
        if options.quit_after:
            return
        if options.console:
            Logo.input_loop(sys.stdin, sys.stdout)
        else:
            from pylogo import ide
            ide.main()
