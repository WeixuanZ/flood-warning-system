from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(name='floodsystem',
      version='1.0',
      author="Weixuan Zhang, Ghifari Pradana",
      description='CUED Part IA flood warning system exercise',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/WeixuanZ/flood-warning-system",
      packages=['floodsystem'],
      classifiers=["License :: OSI Approved :: MIT License"]
      )
