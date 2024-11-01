# Read the contents of your README file
from pathlib import Path

from setuptools import find_namespace_packages, find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


def parse_requirements(filename):
    with open(filename, "r") as file:
        return file.read().splitlines()


docs_packages = ["mkdocs==1.3.0", "mkdocstrings==0.18.1"]

style_packages = ["black==22.3.0", "flake8==3.9.2", "isort==5.10.1"]

test_packages = ["pytest==7.1.2", "pytest-cov==2.10.1", "great-expectations==0.15.15"]

static_analysis_packages = ["radon==6.0.1"]

setup(
    name="walle",
    version="0.1.0",  # Update this as needed
    description="Walle",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tom chang",
    author_email="thomas.w.wchang@gmail.com",
    url="https://github.com/thomaschangsf/walle",  # Replace with your project's URL
    packages=find_namespace_packages(),  # Automatically find packages in the project; find_packages() vs find_namespace_packages()
    install_requires=parse_requirements("requirements.txt"),
    extras_requires={
        "dev": static_analysis_packages + docs_packages + style_packages + test_packages,
        "style": style_packages,
        "docs": docs_packages,
        "test": test_packages,
    },
    classifiers=[
        "Development Status :: 3 - Alpha",  # Change as appropriate
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",  # Update to your license
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",  # Adjust to the required Python version
    # entry_points={
    #    'console_scripts': [
    #        'moemtos=moemtos.cli:main',  # Adjust to your command-line script entry point
    #    ],
    # },
    include_package_data=True,  # Include non-Python files specified in MANIFEST.in
    zip_safe=False,
)
