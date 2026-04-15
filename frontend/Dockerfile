# Base image with Node 22 (LTS)
FROM node:22-alpine

# Set the working directory inside the container
WORKDIR /frontend

# Copy package files first (for layer caching)
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Expose the Vite dev server port
EXPOSE 5173

# Run Vite dev server
CMD ["npm", "run", "dev"]
