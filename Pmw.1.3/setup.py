#!/usr/bin/env python
# setup.py 
from distutils.core import setup 


setup(name="Pmw",
      version='1.3',
      description = 'Python Mega Widgets',
      author="Telstra Corporation Limited, Australia",
      author_email="",
      url='http://pmw.sourceforge.net/',
      package_dir = { "Pmw":""},
      packages=['Pmw', 'Pmw.Pmw_1_3',
		'Pmw.Pmw_1_3.bin',
		'Pmw.Pmw_1_3.contrib',
		'Pmw.Pmw_1_3.demos', 
		'Pmw.Pmw_1_3.doc', 
		'Pmw.Pmw_1_3.lib', 
		'Pmw.Pmw_1_3.tests',],
      package_data={'Pmw': ['Pmw_1_3/lib/Pmw.def',]},
      license='BSD',
      long_description='''Pmw is a toolkit for building high-level compound widgets, or megawidgets, 
	constructed using other widgets as component parts. It promotes consistent look and feel within
	 and between graphical applications, is highly configurable to your needs and is easy to use.''',
      classifiers = [
          'Development Status :: Alpha',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: BSD',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: GUI',
          ],
     )
