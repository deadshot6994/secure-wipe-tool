from setuptools import setup, find_packages # type: ignore

setup(
    name="secure-wipe-tool",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "tk",
        "reportlab",
        "pycryptodome"
    ],
    entry_points={
        "console_scripts": [
            "secure-wipe=app.main:main"
        ]
    },
)
