from setuptools import find_packages, setup  # type: ignore
from version import __version__

setup(
    name="pythoned",
    version=__version__,
    packages=find_packages(),
    url="http://github.com/ebonnal/pythoned",
    license="Apache 2.",
    author="ebonnal",
    author_email="bonnal.enzo.dev@gmail.com",
    description="PYTHON EDitor: edit lines via Python expressions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "pythoned=pythoned.__main__:main",
        ],
    },
)
