# --- Node base ---
FROM node:lts-alpine AS base
# copy source code into working directory
WORKDIR /usr/local/src/app
COPY ./package.json ./webpack.config.js ./webpack.config.prod.js ./.babelrc ./
COPY ./src/ ./src/

# --- Node dependencies ---
# Install react, react-scripts
FROM base AS dependencies
# build react-application
RUN npm install webpack@4.46.0
RUN npm install file-loader@6.2.0
RUN npm install minio
RUN npm install react-cookie

# --- npm build ---
FROM dependencies AS builder
# COPY production modules
# COPY --from=dependencies ./node_modules ./
RUN npm run-script build

# change image to nginx
FROM nginx:1.17.7 AS deployer

# copy react-application into nginxs working directory
RUN rm -r /usr/share/nginx/html
COPY --from=builder /usr/local/src/app/dist /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./public/favicon.ico /usr/share/nginx/html
COPY ./public/static/images/ /usr/share/nginx/html/images/

# expose port used by nginx
EXPOSE 8082