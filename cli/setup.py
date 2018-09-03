from setuptools import setup

setup(
    name='beeweb',
    version='0.1',
    py_modules=['beeweb', 'tfs_pull', 'tfs_list', 'tfs_integration', 'test_suite'],
    install_requires=[
        'click==6.7',
        'beautifulsoup4==4.6.1',
        'dohq-tfs==1.0.81',
    ],
    entry_points='''
        [console_scripts]
        beeweb=beeweb:main
    ''',
)
