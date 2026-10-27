# Talent360 x Eddekhar landing page + booking API, for Railway (or any Docker host).
# Builds the static pages with Python, then serves them and the API from one Node process.
FROM node:20-slim
RUN apt-get update && apt-get install -y --no-install-recommends python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY backend/package.json backend/package-lock.json backend/
RUN npm --prefix backend ci --omit=dev
COPY . .
RUN python3 build.py
ENV NODE_ENV=production
EXPOSE 8080
CMD ["node", "backend/server.js"]
