#dockerfile for API_GATEWAY


FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --silent
COPY . .
EXPOSE 3000
ENV PORT=3000
CMD ["node", "index.js"]
