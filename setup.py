from setuptools import setup, Extension

setup(
    name='px4tuning',
    version='0.1',
    description='Auto tuning for PX4',
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
