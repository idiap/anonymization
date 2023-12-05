from os.path import join

from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]


setup(
    name="anonymization",
    version="0.1.0",
    description="Project Description",
    packages=find_packages(),
    install_requires=requirements,
    test_suite="tests",
    include_package_data=True,
    zip_safe=False,
    scripts=[
        join("scripts", "gen_config"),
        join("scripts", "anonymize"),
        join("scripts", "configure"),
    ],
)
