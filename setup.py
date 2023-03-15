"""Setup script."""
from setuptools import setup

setup(
    name="spot_utils",
    version="0.1.0",
    packages=[],
    install_requires=[],
    include_package_data=True,
    extras_require={
        "develop": [
            "black",
            "docformatter",
            "isort",
            "mypy",
            "pylint>=2.14.5",
            "pytest-pylint>=0.18.0",
        ]
    },
)
