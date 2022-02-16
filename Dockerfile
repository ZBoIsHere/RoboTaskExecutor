FROM ros:noetic
SHELL ["/bin/bash", "-c"]
#COPY ./proxy/bashrcproxy /root/
#RUN cat /root/bashrcproxy >> /root/.bashrc
#COPY ./proxy/apt.conf /etc/apt
#RUN sed '1i\nameserver 127.0.0.53' /etc/resolv.conf
#RUN source /root/.bashrc
#RUN cp -a /etc/apt/sources.list /etc/apt/sources.list.bk
#RUN sudo sed -i "s@http://.*ports.ubuntu.com@http://mirrors.tools.huawei.com@g" /etc/apt/sources.list
#RUN sudo sed -i "s@http://.*security.ubuntu.com@http://mirrors.tools.huawei.com@g" /etc/apt/sources.list
#RUN sudo sh -c '. /etc/lsb-release && echo "deb http://mirrors.ustc.edu.cn/ros/ubuntu/ lsb_release -cs main" > /etc/apt/sources.list.d/ros1-latest.list'
RUN apt-get update && apt-get install -y ros-noetic-move-base ros-noetic-navigation
#RUN apt-get install -y vim

COPY ./*.py /root/
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN source /opt/ros/noetic/setup.bash
ENV PYTHONPATH /opt/ros/noetic/lib/python3/dist-packages
ENTRYPOINT ["python3", "-u", "/root/executor.py"]
