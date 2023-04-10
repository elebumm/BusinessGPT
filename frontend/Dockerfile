# Use the official Node.js runtime as a parent image
FROM node:16

# Set the working directory to /app
WORKDIR /app

# Copy the package.json and package-lock.json files to the container
COPY package*.json ./

# Install the dependencies
RUN yarn install
COPY . /app

# Expose the port that the application will run on
EXPOSE 3000

# Start the application
RUN yarn build
