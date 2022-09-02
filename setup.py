from setuptools import find_packages
from distutils.core import setup


def description():
  with open("README.md", "r") as f:
    return f.read()


def requirements():
  with open("requirements.txt", "r") as f:
    return f.read().split("\n")


setup(name="KamTube",
      version = "0.0.2-beta",
      author="Kamuri Amorim",
      author_email='luiz.k.amorim@gmail.com',
      url="https://github.com/kamuridesu/KamTube",
      download_url = "https://github.com/kamuridesu/KamTube/archive/refs/heads/main.zip",
      long_description=description(),
      long_description_content_type="text/markdown",
      license="MIT",
      packages=find_packages("."),
      install_requires=["aiohttp==3.8.1", "beautifulsoup4==4.8.2"],
      entry_points={
        'console_scripts':[
            'kamtube=KamTube.cli:main'
        ]
      }
)