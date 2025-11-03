FROM node:22-alpine as builder

WORKDIR /app

# package.json と package-lock.json をコピーして依存関係をインストール
COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build


# ランナー (ビルドされた静的ファイルを Nginx で配信)
FROM nginx:alpine

# Nginxのデフォルト設定ファイルを削除
RUN rm /etc/nginx/conf.d/default.conf

# 独自の Nginx 設定ファイルを作成・配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# ビルダーステージからビルド結果を Nginx の静的ファイルディレクトリにコピー
COPY --from=builder /app/build /usr/share/nginx/html

# Nginxのデフォルトポートを公開
EXPOSE 80

# コンテナ起動時に Nginx をフォアグラウンドで実行
CMD ["nginx", "-g", "daemon off;"]