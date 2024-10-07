from setuptools import find_packages, setup

setup(
    name="hackathon-prompt-optimizer",
    version="1.0.0",
    description="Hackathon LLM Prompt Optimization",
    include_package_data=True,
    packages=find_packages(exclude=["tests"]),
    entry_points={
        "console_scripts": [
            "prompt-opt = src.app.orchestration:cli",
        ]
    },
)
