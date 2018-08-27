from setuptools import setup, Extension

setup(
    name='px4tuning',
    version='0.1',
    description='Auto tuning for PX4',
    packages=['px4tuning'],
    author='Diego Eckhard',
    author_email='diego@eckhard.com.br`',
    license='MIT',
    entry_points={
        'console_scripts': ['px4att=px4tuning.px4att:main'],
    },
    zip_safe=False
)
