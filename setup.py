import sys
import codecs

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

from envProtect import envprotect


class PyTest(TestCommand):
    """
    Running `$ python setup.py test' simply installs minimal requirements
    and runs the tests with no fancy stuff like parallel execution.
    """
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [
            '--doctest-modules', '--verbose',
            './envprotect', './tests'
        ]
        self.test_suite = True

    def run_tests(self):
        import pytest
        sys.exit(pytest.main(self.test_args))


tests_require = [
    'pytest',
    'mock',
]


install_requires = [
    'Pygments>=2.5.2',
    'requests-toolbelt>=0.9.1',
]


def long_description():
    with codecs.open('README.rst', encoding='utf8') as f:
        return f.read()


setup(
    name='envprotect',
    version=envprotect.__version__,
    description=envprotect.__doc__.strip(),
    long_description=long_description(),
    url='https://www.passeriform.com/proj/envprotect',
    download_url=f'https://github.com/Passeriform/envProtect/archive/{envprotect.__version__}.tar.gz',
    author=envprotect.__author__,
    author_email='passeriform.ub@gmail.com',
    license=envprotect.__licence__,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'envprotect = envprotect.__main__:main',
            'envscan = envprotect.__main__:scan',
            'envdump = envprotect.__main__:extract',
        ],
    },
    python_requires='>=3.6',
    extras_require=extras_require,
    install_requires=install_requires,
    tests_require=tests_require,
    cmdclass={'test': PyTest},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Version Control',
        'Topic :: Terminals',
        'Topic :: Utilities'
    ],
    project_urls={
        'Source': 'https://github.com/Passeriform/envProtect',
    },
)
