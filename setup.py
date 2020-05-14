#!/usr/bin/env python3

"""The setup script."""

import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent

with open(here / "yaqd_arduino_gpio" / "VERSION") as version_file:
    version = version_file.read().strip()


with open("README.md") as readme_file:
    readme = readme_file.read()


requirements = ["yaqd-core"]

extra_requirements = {"dev": ["black", "pre-commit"]}
extra_files = {"yaqd_arduino_gpio": ["VERSION"]}

setup(
    author="Brandon Mehlenbacher",
    author_email="bmehlenbacher4@gmail.com",
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
    ],
    description="yaq daemon for controlling arduinos input/output interface",
    entry_points={
        "console_scripts": [
            "yaqd-arduino-gpio=yaqd_arduino_gpio._arduino_gpio:ArduinoGpio.main",
        ],
    },
    install_requires=requirements,
    extras_require=extra_requirements,
    license="GNU Lesser General Public License v3 (LGPL)",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    package_data=extra_files,
    keywords="yaqd_arduino_gpio",
    name="yaqd_arduino_gpio",
    packages=find_packages(include=["yaqd_arduino_gpio", "yaqd_arduino_gpio.*"]),
    url="https://gitlab.com/bmehlenbacher/yaqd_arduino_gpio",
    version=version,
    zip_safe=False,
)
