#!/usr/bin/env python

# setuptools doesn't support type hints for now:
# https://github.com/pypa/setuptools/issues/2345
# so we ignoring mypy checks on this package
from setuptools import find_packages, setup  # type: ignore

with open("README.md") as f:
    long_description = f.read()


setup(
    name="cachetory",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="Caching library with support for multiple cache backends",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Pavel Perestoronin",
    author_email="pavel.perestoronin@kpn.com",
    url="https://github.com/kpn/cachetory",
    packages=find_packages(exclude=["tests*"]),
    tests_require=["tox"],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP",
    ],
)