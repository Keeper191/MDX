# Manga Downloader X

## Overview

Manga Downloader is a web application that allows users to download manga from popular sites like MangaDex. The app runs in a Docker container and provides a user-friendly web interface for downloading manga directly to your preferred folder.

## Features

- **Download Manga from Multiple Sources**: Supports MangaDex and other popular manga sites.
- **User-Friendly Interface**: Simple and intuitive web interface.
- **Customizable Download Folder**: Choose where you want your manga to be saved.
- **Dockerized**: Easy to deploy and run anywhere with Docker.
- **Progress Tracker**: Real-time download progress tracking.

## Docker Images

We provide Docker images for different architectures:

- **AMD64**: `keeper191/mdx:latest`
- **ARM**: `keeper191/mdx:raspi`

## Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your machine.
- Basic understanding of running Docker containers.

## Installation

1. **Pull the Docker Image**

   For AMD64:
   ```sh
   docker pull keeper191/mdx:latest
   ```

   For ARM (Raspberry Pi):
   ```sh
   docker pull keeper191/mdx:raspi
   ```

2. **Run the Docker Container**

   For AMD64:
   ```sh
   docker run -d -p 5001:5000 -v /path/to/downloads:/downloads keeper191/mdx:latest
   ```

   For ARM (Raspberry Pi):
   ```sh
   docker run -d -p 5001:5000 -v /path/to/downloads:/downloads keeper191/mdx:raspi
   ```

   Replace `/path/to/downloads` with the path to your desired download folder.

## Usage

1. **Access the Web Interface**

   Open your browser and navigate to `http://<your-ip>:5001`.

2. **Register or Login**

   - **Register**: Create a new account by providing a username and password.
   - **Login**: Use your credentials to log in.

3. **Download Manga**

   - Enter the URL of the manga you wish to download.
   - Click the "Download" button to add the manga to the download queue.
   - Monitor the download progress in real-time.

It is open source, you can visit the github page  - https://github.com/Keeper191/MDX

---

By following these instructions, you should be able to get the Manga Downloader web app up and running with ease. Enjoy your manga downloads!
