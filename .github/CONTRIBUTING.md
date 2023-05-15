# Contributing Guide

To contribute, please follow these steps:

1. Fork the project name repository on GitHub.
1. Create a new branch for your feature or bug fix.
1. Setup development environment.

    ```shell
    # install pipx
    python3 -m pip install --user pipx
    python3 -m pipx ensurepath

    # install poetry
    pipx install poetry

    # install project dependencies
    poetry install

    # do test build
    poetry build
    ```

1. Make your changes
1. Lint and validate your code

    ```shell
    poetry run pre-commit run --all-files
    ```

1. Commit your changes.
1. Make sure the `README.md` and any other relevant documentation are kept up-to-date.
1. Push to your forked repository.
1. Create a new pull request from your fork to this project.
1. Please ensure that your pull request includes a detailed description of your changes.
