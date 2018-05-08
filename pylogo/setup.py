try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    import warnings
    warnings.filterwarnings("ignore", "Unknown distribution option")
    import sys
    # patch distutils if it can't cope with the "classifiers" keyword
    if sys.version < '2.2.3':
        from distutils.dist import DistributionMetadata
        DistributionMetadata.classifiers = None
        DistributionMetadata.download_url = None

__version__ = '0.5'

setup(name="PyLogo",
      version=__version__,
      description="Logo interpreter",
      long_description="""\
An interpreter for the Logo educational programming language.

This version of Logo is a faithful representation of the language,
written in a way that makes it compatible with Python code.
Primitives are written in Python, and Python can call Logo code
similar to how it calls Python code.

There is a `Subversion repository
<http://svn.colorstudy.com/PyLogo/trunk#egg=PyLogo-dev>`_.
""",
      classifiers=[
        "Development Status :: 3 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Logo",
        "Programming Language :: Python",
        "Topic :: Education",
        "Topic :: Software Development :: Interpreters",
        ],
      author="Ian Bicking",
      author_email="ianb@colorstudy.com",
      url="http://pylogo.org",
      license="MIT",
      packages=["pylogo"],
      entry_points="""
      [console_scripts]
      pylogo = pylogo.script:main
      """,
      )

# Send announce to:
#   python-announce@python.org
#   python-list@python.org
#   edu-sig@python.org
#   LogoForum@yahoogroups.com
#   Freshmeat
#   PyPI
