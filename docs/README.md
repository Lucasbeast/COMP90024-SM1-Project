# Project Directory

This directory contains essential configuration files and a group report. Below is a brief description of each file and their purposes:

## Files

- **elastic.env**
  - This file contains environment variables required for running Python scripts that interact with Elasticsearch.
  - Ensure this file is in the same directory as the scripts that need these environment variables.

- **ES_USERNAME**
  - Contains the Elasticsearch username.
  - **Important:** Ensure that the `ES_USERNAME` environment variable is set before executing any scripts that require it.
  - Use the following command to secure this file:
    ```bash
    chmod 600 ES_USERNAME
    ```

- **ES_PASSWORD**
  - Contains the Elasticsearch password.
  - **Important:** Ensure that the `ES_PASSWORD` environment variable is set before executing any scripts that require it.
  - Use the following command to secure this file:
    ```bash
    chmod 600 ES_PASSWORD
    ```

- **README.md**
  - This file provides an overview of the directory and its contents.

- **report-Group43.pdf**
  - A PDF document containing the report for Group 43.
  - Last modified on 22/05/2024.

## Setup Instructions

1. Ensure the `elastic.env` file is in the same directory as the scripts that need these environment variables.
2. Set the `ES_USERNAME` and `ES_PASSWORD` environment variables before executing any related scripts.
3. Secure the `ES_USERNAME` and `ES_PASSWORD` files using `chmod 600` to ensure they are not accessible by unauthorized users.
4. Refer to the `report-Group43.pdf` for the detailed group report.