from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="autocad-helper",
    version="1.0.0",
    author="lastnight0305",
    author_email="your.email@example.com",
    description="Ứng dụng hỗ trợ hiển thị các lệnh AutoCAD thông dụng",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lastnight0305/AutoCad-Helper",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Computer Aided Design",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Natural Language :: Vietnamese",
    ],
    python_requires=">=3.7",
    install_requires=[
        "keyboard>=0.13.5",
        "pywin32>=306",
        "winshell>=0.6",
    ],
    entry_points={
        "console_scripts": [
            "autocad-helper=main:main",
        ],
    },
)
