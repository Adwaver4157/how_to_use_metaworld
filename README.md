# Install MetaWorld using Docker
First pull docker image for metaworld
```bash
docker pull adwaver4157/r3m:latest
```

Then run docker container
```bash
docker run -it --rm --name takanami_r3m \
               --gpus all --shm-size=16gb \
               --mount type=bind,source="$(pwd)",target=/root/workspace \
               -p 5900:5900 -p 6006:6006 -p 8088:8888 \
               adwaver4157/r3m:latest
```
And install metaworld
```bash
bash install.sh
```

Finally run vnc and metaworld env
```bash
vnc
python simple_env.py
```

