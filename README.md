# PhotoShare

PhotoShare is a REST API application built with FastAPI for managing photo sharing with comprehensive features.

## Features

- **Authentication**: JWT with roles (User, Moderator, Admin).
- **Photo Management**: Upload, delete, edit, and tag photos.
- **Comments**: Users can comment on photos, with admin/moderator controls.
- **User Profiles**: View and edit profiles, admin can ban users.
- **Additional**: Rate photos, image transformations, QR code generation.

## Installation

1. Clone the repository and navigate to the project directory.
2. Create and activate a virtual environment.
3. Install dependencies from `requirements.txt`.

## Usage

Run the app with `uvicorn PhooShare.app.main:app --reload`.

## Testing

Run tests with `pytest --cov=.` aiming for 90%+ coverage.

## Deployment

Deploy on cloud services like Koyeb or Fly.io.
