FROM node:20-alpine
WORKDIR /app
# Copy package configuration files
COPY frontend/package*.json ./
# Install packages
RUN npm install
# Copy frontend source files
COPY frontend/ ./
EXPOSE 3000
# Run Next.js dev server listening on all host interfaces
CMD ["npm", "run", "dev", "--", "-H", "0.0.0.0"]