# Use official Node image as base
FROM node:18

# Set working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the entire project
COPY . .

# Expose port for web interface
EXPOSE 3000

# Run the application
CMD ["npm", "start"]