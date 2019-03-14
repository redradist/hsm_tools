import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fsm_tools",
    version="0.0.1",
    author="Denis Kotov (redradist, RedRadist, redra, RedRa)",
    author_email="redradist@gmail.com",
    description="FSMTools is a package for creating different kinds of FSM (Finite State Machine), "
                "HSM (Hierarchical State Machine)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={'fsm_tools': 'src/fsm_tools'},
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)