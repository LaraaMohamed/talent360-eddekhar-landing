# Talent360 x Eddekhar landing page + booking API, for Railway (or any Docker host).
# Stage 1 builds the static pages with Python 3.12 (template.py needs 3.12 f-string rules).
FROM python:3.12-slim AS site
WORKDIR /src
COPY . .
RUN python3 build.py

# Stage 2 serves the pages and the API from one Node process.
FROM node:20-slim
WORKDIR /app
COPY backend/package.json backend/package-lock.json backend/
RUN npm --prefix backend ci --omit=dev
COPY . .
COPY --from=site /src/dist ./dist
ENV NODE_ENV=production
EXPOSE 8080
CMD ["node", "backend/server.js"]
