# -*- coding: utf-8 -*-
from pathlib import Path
from setuptools import find_packages, setup


README = (Path(__file__).parent / "README.md").read_text()

REQUIRES = ["pluggy>=1.0,<1.1", "robotframework>=4.0,<5.0"]
EXTRAS_REQUIRE = {"test": ["pytest>=5.2.2,<6.3.0" "black==21.12b0"]}


def get_version():
    global_vars = {}
    exec(Path("src/rf_network/version.py").read_text(), global_vars)
    return global_vars["__version__"]


setup(
    name="rf-network",
    keywords=["rf-network", "robotframework", "network", "testing"],
    license="MIT license",
    version=get_version(),
    author="Tafsir Thiam",
    author_email="ttafsir@gmail.com",
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description=(
        "A pluggable multi-vendor network connection library for RobotFramework"
    ),
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ttafsir/rf-network",
    packages=find_packages("src", exclude=("tests",)),
    package_dir={"": "src"},
    install_requires=REQUIRES,
    include_package_data=True,
    extras_require=EXTRAS_REQUIRE,
    tests_require=["rf-network[test]"],
)
