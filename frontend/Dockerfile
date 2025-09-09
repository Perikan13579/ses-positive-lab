FROM node:22-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]


# --- 開発環境用 ---
# FROM node:22-alpine
# WORKDIR /app
# COPY package*.json ./
# RUN npm install
# COPY . .
# EXPOSE 3000
# CMD ["npm", "start"]