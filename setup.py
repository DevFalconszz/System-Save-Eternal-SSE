from setuptools import setup, find_packages

setup(
    name="system-save-eternal",
    version="2.0.0",
    packages=find_packages(include=["src", "src.*"]),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "sse=src.main:main",
            "sse-cli=src.main:cli_main",
        ],
    },
)
