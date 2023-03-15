"""Setup script."""
from setuptools import setup

setup(
    name="spot-utils",
    version="0.1.0",
    packages=[],  # TODO #find_packages(include=["predicators", "predicators.*"]),
    install_requires=[],
    include_package_data=True,
    extras_require={
        "develop": [
            "black",
            "docformatter",
            "isort",
            "mypy@git+https://github.com/python/mypy.git@9bd651758e8ea2494"
            + "837814092af70f8d9e6f7a1",
            "docformatter",
        ]
    },
)
