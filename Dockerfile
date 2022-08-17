FROM stablebaselines/stable-baselines3:latest

SHELL ["/bin/bash", "-c"]

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
    libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
RUN curl https://pyenv.run | bash && \
    echo '' >> /root/.bash_profile && \
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> /root/.bash_profile && \
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> /root/.bash_profile && \
    echo 'eval "$(pyenv init --path)"' >> /root/.bash_profile && \
    echo 'eval "$(pyenv virtualenv-init -)"' >> /root/.bash_profile
RUN source /root/.bash_profile && \
    pyenv install 3.8.11 && \
    pyenv global 3.8.11 && \
    pip install -U pip


RUN apt-get update && apt-get install -y \
    xvfb x11vnc python-opengl icewm
RUN echo 'alias vnc="export DISPLAY=:0; Xvfb :0 -screen 0 1400x900x24 & x11vnc -display :0 -forever -noxdamage > /dev/null 2>&1 & icewm-session &"' >> /root/.bashrc

# DL libraries and jupyter ----------------
RUN source /root/.bash_profile && \
    pip install setuptools jupyterlab && \
    pip install tensorflow && \
    echo 'alias jl="jupyter lab --ip 0.0.0.0 --port 8888 --NotebookApp.token='' --allow-root &"' >> /root/.bashrc && \
    echo 'alias tb="tensorboard --host 0.0.0.0 --port 6006 --logdir runs &"' >> /root/.bashrc

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
    curl \
    git \
    libgl1-mesa-dev \
    libgl1-mesa-glx \
    libglew-dev \
    libosmesa6-dev \
    software-properties-common \
    net-tools \
    unzip \
    vim \
    virtualenv \
    wget \
    xpra \
    xserver-xorg-dev

RUN curl -o /usr/local/bin/patchelf https://s3-us-west-2.amazonaws.com/openai-sci-artifacts/manual-builds/patchelf_0.9_amd64.elf \
    && chmod +x /usr/local/bin/patchelf

RUN mkdir -p /root/.mujoco \
    && wget https://mujoco.org/download/mujoco210-linux-x86_64.tar.gz -O mujoco.tar.gz \
    && tar -xf mujoco.tar.gz -C /root/.mujoco \
    && rm mujoco.tar.gz

ENV LD_LIBRARY_PATH /root/.mujoco/mujoco210/bin:${LD_LIBRARY_PATH}
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib64:${LD_LIBRARY_PATH}

RUN git clone https://github.com/openai/mujoco-py.git -b v2.1.2.14 --depth 1 && \
    cd mujoco-py && \
    source /root/.bash_profile && \
    pip install -r requirements.txt && \
    sed -i -e 's/= LinuxCPU/= LinuxGPU/g' mujoco_py/builder.py && \
    pip install -e . 

RUN echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/root/.mujoco/mujoco210/bin' >> /root/.bashrc && \
    echo 'test -r ~/.bashrc && . ~/.bashrc' >> /root/.bash_profile

# utils ----------------
RUN apt-get update && apt-get install -y \
    vim

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN cd / && \
    git clone https://github.com/suraj-nair-1/metaworld.git && \
    cd metaworld && \
    source /root/.bash_profile && \
    sed -i -e 's/mujoco-py<2.1,>=2.0/mujoco-py/' setup.py && \
    pip install -e .

WORKDIR /root/workspace

RUN source ~/.bash_profile
CMD ["/bin/bash", "-c", "source ~/.bash_profile && bash"]