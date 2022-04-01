FROM node:16.14

# set working directory
WORKDIR /app

COPY package.json /app/
COPY package-lock.json /app/
RUN npm install
#RUN npm install -g @vue/cli @vue/cli-init cross-env

CMD ["npm", "run", "serve"]
#CMD /bin/bash
