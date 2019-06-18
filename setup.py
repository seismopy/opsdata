# !/usr/bin/env python

from distutils.core import setup


requirements = open("requirements.txt").read()

setup(
    name="opsdata_template",
    packages=[],
    version="0.1.2",
    description="an obsplus dataset template",
    author="Derrick Chambers",
    license="BSD",
    author_email="djachambeador@gmail.com",
    requirements=requirements,
    url="https://github.com/seismopy/opsdata",
    keywords=["cookiecutter", "template", "package"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development",
    ],
)
