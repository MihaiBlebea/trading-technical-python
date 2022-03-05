FROM python:3.9

# set the id and gid of the user from host
# TODO: remove hardcode and set by command or pass from terminal
ARG UNAME=mihai
ARG UID=1000
ARG GID=1000

# create a new group with the gid predefined
RUN groupadd -g $GID -o $UNAME

# add a new user with the known id and add it to the group already created
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME

RUN apt-get update

WORKDIR /app

RUN python -m venv env

COPY requirements.txt .

RUN ./env/bin/pip3 install --upgrade pip

RUN ./env/bin/pip3 install -r requirements.txt

VOLUME [ "/app/data" ]

COPY . .

# give the user the ownership off all the files in the working dir
RUN chown -R $UNAME:$UNAME /app

# assume the role of the user in the docker container
USER $UNAME

CMD ["./execute.sh", "src/stream"]
