FROM node:20-alpine
WORKDIR /app

# Copy package configuration files
COPY frontend/package*.json ./

# Install packages
RUN npm install

# Copy frontend source files
COPY frontend/ ./

# 1. Accept the build argument
ARG NEXT_PUBLIC_API_URL
# 2. Make it available as an environment variable during the build
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

# 3. Build the Next.js production bundle!
RUN npm run build

EXPOSE 3000

# 4. Start the production server (no more 'npm run dev')
CMD ["npm", "start"]
