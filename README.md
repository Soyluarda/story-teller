# Story Generator

This project is an application that analyzes user activities retrieved from Strava and generates storylines using an AI-based language model for each activity.

## Installation and Usage

### Installation

1. Clone the project: `git clone https://github.com/username/repository.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Create a file which is named `.env` and copy the content of `example.env` to it.

### Usage

1. Run the project: `docker-compose up --build`
2. Go to `http://localhost:8000/api/v1/docs` in your browser.
3. Use endpoints to retrieve Strava events and create stories.

## Strava Integration

This application accesses user activities using Strava's OAuth 2.0 protocol. You'll need to add your Strava API key to the `.env` file for user authorization.

