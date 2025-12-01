from setuptools import setup, find_packages

setup(
    name="intelligence-platform",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.36.0",
        "pandas>=2.2.0",
        "openai>=1.12.0",
        "numpy>=1.26.4",
        "python-dotenv>=1.0.0",
    ],
    python_requires=">=3.11",
)