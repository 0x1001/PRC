from distutils.core import setup

setup(
    name='PRC',
    version='0.9.3',
    author='Damian Nowok',
    author_email='damian.nowok@gmail.com',
    packages=['prc', 'prc.test', 'prc.comm'],
    scripts=['bin/example_prcclient.py','bin/example_prcserver.py'],
    url='http://pypi.python.org/pypi/prc/',
    license='LICENSE.txt',
    description='Python Remote Console',
    long_description=open('README.txt').read(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
)