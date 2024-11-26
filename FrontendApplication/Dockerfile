#dockerfile for FRONTEND_APPLICATION


FROM node:14 as builder
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
ARG MY_API_GATEWAY_URL
ENV API_GATEWAY=$MY_API_GATEWAY_URL
RUN npm run build
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
