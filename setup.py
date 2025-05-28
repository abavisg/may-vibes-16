from setuptools import setup, find_packages

setup(
    name="debate_day",
    version="1.0.0",
    description="Debate Day 2.0 - AI debate platform",
    author="AI Vibes Team",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.103.1",
        "pydantic>=2.0.0",
        "uvicorn>=0.23.2",
        "python-dotenv>=1.0.0",
    ],
    python_requires=">=3.9",
) 