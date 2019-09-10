from setuptools import setup, Extension

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='px4tuning',
    version='0.1.1',
    description='Auto tuning for PX4',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['px4tuning'],
    author='Diego Eckhard',
    author_email='diego@eckhard.com.br',
    url="https://github.com/diegoeck/px4tuning",
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['px4att=px4tuning.px4att:main'],
    },
    zip_safe=False
)
