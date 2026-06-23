FROM node:20-alpine

WORKDIR /app

# Copy dependency files
COPY package*.json ./

# Install dependencies (including devDependencies so vite is available)
RUN npm ci

# Copy the rest of the source code
COPY . .

# Accept build-time environment variable argument
ARG VITE_API_URL
ENV VITE_API_URL=${VITE_API_URL:-/api}

# Build the application
RUN npm run build

# Expose Vite preview port
EXPOSE 5173

# Serve the static files using Vite preview
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "5173"]
