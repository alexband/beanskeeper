from setuptools import setup, Extension

setup(
        name = 'fnv1a',
        version = '1.1',
        ext_modules = [
            Extension('fnv1a', ['fnv1a.c']),
            ],
        tests_require = ['nose'],
        test_suite = 'nose.collector',
        )
