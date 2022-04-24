from re import MULTILINE
from re import findall

from setuptools import find_packages
from setuptools import setup


with open(".bumpversion.cfg") as fh:
    (version,) = findall(
        r"^current_version = (\d+\.\d+\.\d+)$", fh.read(), flags=MULTILINE
    )
with open("README.md") as fh:
    long_description = fh.read()


setup(  # https://bit.ly/3MJfVyH
    name="app",
    version=version,
    description="Dummy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Derek Wan",
    author_email="d.wan@icloud.com",
    url="https://github.com/dycw/template",
    packages=find_packages("src"),
    options={"bdist_wheel": {"universal": "1"}},
    license="MIT",
    license_files=["LICENSE"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "aerich >= 0.6.3, < 0.7",
        "aiofiles >= 0.8.0, < 0.9",
        "alembic >= 1.7.7, < 1.8",
        "asgi-lifespan >= 1.0.1, < 1.1",
        "broadcaster[redis] >= 0.2.0, < 0.3",
        "databases[sqlite] >= 0.5.5, < 0.6",
        "email-validator >= 1.1.3, < 1.2",
        "fastapi >= 0.75.2, < 0.76",
        "loguru >= 0.6.0, < 0.7",
        "httpx >= 0.22.0, < 0.23",
        "passlib[bcrypt] >= 1.7.4, < 1.8",
        "motor >= 2.5.1, < 2.6",
        "python-multipart >= 0.0.5, < 0.6",
        "pytest-asyncio >= 0.18.3, < 0.19",
        "requests >= 2.27.1, < 2.28",
        "starlette-csrf >= 1.4.3, < 1.5",
        "tortoise-orm >= 0.19.0, < 0.20",
        "uvicorn[standard] >= 0.17.6, < 0.18",
    ],
    entry_points={"console_scripts": []},
    extras_require={
        "dev": [
            # development
            "build >= 0.7.0, < 0.8",
            "bump2version >= 1.0.1, < 1.1",
            "pip-tools >= 6.6.0, < 6.7",
            "pre-commit >= 2.18.1, < 2.19",
            "pyclean >= 2.2.0, < 2.3",
            # formatters
            "black >= 22.3.0, < 22.4",
            "isort >= 5.10.1, < 5.11",
            # linters
            "flake8 >= 4.0.1, < 4.1",
            "flake8-absolute-import >= 1.0.0.1, < 1.0.1.0",
            "flake8-annotations >= 2.9.0, < 2.10",
            "flake8-bandit >= 3.0.0, < 3.1",
            "flake8-bugbear >= 22.3.23, < 22.4",
            "flake8-comprehensions >= 3.8.0, < 3.9",
            "flake8-debugger >= 4.0.0, < 4.1",
            "flake8-eradicate >= 1.2.0, < 1.3",
            "flake8-no-pep420 >= 2.2.0, < 2.3",
            "flake8-pie >= 0.15.0, < 0.16",
            "flake8-print >= 4.0.0, < 4.1",
            "flake8-simplify >= 0.19.2, < 0.20",
            "flake8-unused-arguments >= 0.0.9, < 0.1",
            # testing
            "pytest >= 7.1.2, < 7.2",
            "pytest-instafail >= 0.4.2, < 0.5",
            "pytest-xdist >= 2.5.0, < 2.6",
            # typing
            "sqlalchemy2-stubs >= 0.0.2a21, < 0.0.3",
        ]
    },
    python_requires=">= 3.9.12",
)
