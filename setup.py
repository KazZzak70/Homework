from setuptools import setup, find_packages

with open("requirements.txt") as req:
    all_req = req.read().split("\n")
all_req = [req.split() for req in all_req]
long_description = " "

setup(
    name="rss_reader",
    version="1.4",
    author="Maksim Kazak",
    author_email="kazak.ya.maxim@gmail.com",
    long_description=long_description,
    packages=find_packages(),
    python_requires=">=3.8, <4",
    install_requires=all_req,
    entry_points={
        'console_scripts': ['rss_reader=rss_reader.rss_reader:rss_reader']
    }
)


