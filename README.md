# DataLayer Fetcher API

This project provides an API for fetching data layer information from a given URL.

## Installation

1. Clone this repository.
2. Install the required dependencies with `pip install -r requirements.txt`.

## Usage

Start the server with the command `python main.py`.

The API has two endpoints:

- `GET /`: Returns a welcome message.
- `POST /url`: Fetches the data layer from the provided URL.

To fetch the data layer from a URL, send a POST request to `/url` with the following JSON body:

```json
{
    "target_url": "https://example.com"
}