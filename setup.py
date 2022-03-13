from setuptools import setup
import pathlib
import shutil
import sys
import os


here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

if sys.argv[-1] == 'update':
    if os.path.isdir('dist'):
        shutil.rmtree('dist')
    if os.path.isdir('module_Thw.egg-info'):
        shutil.rmtree('module_Thw.egg-info')
    os.system('python -m build')
    os.system('twine upload dist/*')
    sys.exit()


setup(
    name='module-Thw',
    version='0.0.1',
    description='some module',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Thachj-Thw/module',
    author='Thw',
    author_email='',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Natural Language :: Vietnamese'
    ],
    keywords='module',
    packages=['module'],
    install_requires=['pywin32'],
    python_requires='>=3.6',
    include_package_data=True,
    project_urls={
        'Source': 'https://github.com/Thachj-Thw/module',
    },
)
