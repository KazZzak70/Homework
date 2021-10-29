from setuptools import setup, find_packages

with open("requirements.txt") as req:
    all_req = req.read().split("\n")
all_req = [req.split() for req in all_req]
with open("README.md") as ld_file:
    long_description = ld_file.read()

setup(
    name="rss_reader",
    version="1.4",
    author="Maksim Kazak",
    author_email="kazak.ya.maxim@gmail.com",
    description="Pure Python command-line RSS reader",
    long_description=long_description,
    include_package_data=True,
    packages=find_packages(),
    package_data={
        "pdf_output": ["fonts/*.ttf"]
    },
    python_requires=">=3.8, <4",
    install_requires=all_req,
    entry_points={
        'console_scripts': ['rss_reader=rss_reader.rss_reader:rss_reader']
    }
)


