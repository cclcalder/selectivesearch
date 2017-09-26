FROM jjanzic/docker-python3-opencv

RUN pip install numpy \
    && pip install scipy \
    && pip install scikit-image \
    && pip install scikit-learn \
    && pip install selectivesearch
ADD setup.py /code/
WORKDIR /usr/src/selectivesearch