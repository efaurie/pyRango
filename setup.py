from setuptools import setup, find_packages


def main():
    with open('requirements.txt') as dependencies:
        required = dependencies.read().splitlines()

    setup(
        name="pyRango",
        version='0.0.1',
        author="Eric Faurie",
        packages=find_packages(where='.', exclude='examples'),
        install_requires=required
    )


if __name__ == "__main__":
    main()
