from setuptools import setup

setup(
    name='olympics_engine',
    version='0.1.0',
    description='A multi-agent benchmark',
    url='https://github.com/jidiai/olympics_engine',
    author='Yan Song',
    author_email='yan.song@ia.ac.cn',
    license='MIT',
    packages=['olympics_engine'],
    install_requires=['pygame==2.0.2',
                      'numpy',
                      'gym'
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)