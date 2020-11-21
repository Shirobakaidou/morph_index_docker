FROM mundialis/grass-py3-pdal
#FROM continuumio/miniconda3
#CMD grass --config

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

RUN apt-get update --fix-missing && \
    apt-get install -y wget bzip2 ca-certificates curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda clean -tipsy && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

ENV TINI_VERSION v0.16.1
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini

ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "/bin/bash" ]
#CMD grass --config

##--------------------------------------------------------##
##--------------------------------------------------------##


# Set Working Directory to /app
WORKDIR /app

# Create the environment
COPY environment.yml .
RUN conda env create -f environment.yml

# Make RUN commands use the new env; "basinIndex" is the name of the conda env
SHELL ["conda", "run", "-n", "basinIndex", "/bin/bash", "-c"]

# Make sure the env is activated
#RUN echo "Make sure numpy is installed:"
#RUN python -c "import numpy"

# The code ro run when container is started
COPY myscript.py ./script/
#COPY input/. ./input/
ENTRYPOINT ["conda", "run", "-n", "basinIndex", "python", "./script/myscript.py"]

