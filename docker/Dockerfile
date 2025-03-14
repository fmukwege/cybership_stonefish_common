ARG ROS_DISTRO=humble
ARG UID=1000
ARG GID=1000

FROM ros:$ROS_DISTRO

ARG ROS_DISTRO
ARG UID
ARG GID

ENV ROS_DISTRO=${ROS_DISTRO}
ENV DEBIAN_FRONTEND=noninteractive
ENV DEBIAN_FRONTEND=teletype

RUN apt-get update && apt-get install -y sudo

RUN uid=${UID} && \
    if getent passwd $uid > /dev/null; then \
        username=$(getent passwd $uid | cut -d: -f1); \
        userdel -r $username; \
    fi

RUN groupadd --gid "${GID}" ros_user \
    && useradd --uid "${UID}" --gid "${GID}" -m ros_user \
    && usermod -aG sudo ros_user \
    && echo "ros_user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y git

RUN git clone https://github.com/patrykcieslak/stonefish

RUN apt-get install -y \
    libsdl2-dev \
    libglm-dev \
    libfreetype6-dev \
    ros-$ROS_DISTRO-pcl-conversions \
    ros-$ROS_DISTRO-image-transport \
    tmux \
    python3-pip
    
RUN cd stonefish && \
    mkdir -p build && \
    cd build && cmake .. && \
    make -j4 && make install 

RUN mkdir -p stonefish_ws/src && \
    cd stonefish_ws/src && git clone https://github.com/patrykcieslak/stonefish_ros2.git

RUN /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash && \
    cd /stonefish_ws && \
    export MAKEFLAGS='-j1 -l1' && colcon build"

ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

COPY . ros2_ws/src

RUN chown -R ros_user:ros_user /ros2_ws

RUN /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash && \
    source stonefish_ws/install/setup.bash && \
    cd /ros2_ws && \
    colcon build --packages-select cybership_simulation_common"

ENTRYPOINT ["/bin/bash", "-c", "source /opt/ros/${ROS_DISTRO}/setup.bash &&\
             source stonefish_ws/install/setup.bash &&\
             source ros2_ws/install/setup.bash &&\
             ros2 launch cybership_simulation_common simulation_nogpu.launch.py"]
         

