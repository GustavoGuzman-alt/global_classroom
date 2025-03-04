from setuptools import setup, find_packages

setup(
    name="GlobalClassroom",
    version="0.1.0",
    description="A tool to translate educational videos and documents into multiple languages.",
    author="Gustavo Guzman",
    author_email="gustavo.guzman88@gmail.com.com",
    url="https://github.com/GustavoGuzman-alt/GlobalClassroom",  # Update with your repo URL
    packages=find_packages(),
    install_requires=[
        "whisper>=1.2.0",
        "deep-translator>=1.7.0",
        "pysrt>=1.1.2",
        "python-docx>=0.8.11",
        "PySide6>=6.2.0",
        "torch"
    ],
    entry_points={
        "console_scripts": [
            "global_classroom=main:run_app"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
