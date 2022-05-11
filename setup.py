from setuptools import setup

setup(
    name="auto_datafiles",
    version="0.1.0",
    py_modules=["auto_datafiles"],
    install_requires=[
        "Click",
    ],
    entry_points={
        "console_scripts": [
            "auto_datafiles = auto_datafiles:cli",
        ],
    },
)
