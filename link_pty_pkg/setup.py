from setuptools import setup, find_packages

setup(
    name="link-pty",
    version="0.7.0",
    packages=find_packages(),
    install_requires=[
        "websockets",
        "requests",
        "psutil" 
    ],
    entry_points={
        'console_scripts': [
            'link-pty = link_pty.terminal_manager:run_terminal_manager',
        ],
    },
    author="ricepastem",
    description="A package to manage pseudo terminals via WebSocket",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/ricepastem/link_pty",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
