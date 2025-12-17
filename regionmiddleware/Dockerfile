FROM node:18-alpine

WORKDIR /usr/src/app

# Copiamos manifests para aprovechar cache
COPY package*.json ./

# Instala dependencias (reproducible con lock)
RUN npm ci --omit=dev

# Copiamos el resto del código
COPY . .

EXPOSE 8080
CMD ["npm", "start"]
