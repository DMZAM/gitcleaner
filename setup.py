from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gitcleaner",
    version="1.0.0",
    author="DMZAM",
    author_email="dmzam@example.com",
    description="Аналог BFG Repo-Cleaner на Python для очистки Git репозиториев",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DMZAM/gitcleaner",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=[
        "click>=8.0.0",
        "tqdm>=4.60.0",
        "colorama>=0.4.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "black>=21.0.0",
            "flake8>=3.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "gitcleaner=gitcleaner.cli:main",
        ],
    },
    keywords="git, cleanup, bfg, repository, clean, remove, delete, files",
    project_urls={
        "Bug Reports": "https://github.com/DMZAM/gitcleaner/issues",
        "Source": "https://github.com/DMZAM/gitcleaner",
        "Documentation": "https://github.com/DMZAM/gitcleaner#readme",
    },
)