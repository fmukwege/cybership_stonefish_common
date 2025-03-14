ARG ROS_DISTRO=humble
ARG UID=1000
ARG GID=1000

FROM andeshog/stonefish-ros2:$ROS_DISTRO

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

COPY . ros2_ws/src

RUN chown -R ros_user:ros_user /ros2_ws

RUN /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash && \
    source /stonefish_ws/install/setup.bash && \
    cd /ros2_ws && \
    colcon build --packages-select cybership_simulation_common"

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN ls -R /ros2_ws
ENTRYPOINT ["/entrypoint.sh"]

CMD ["bash"]
         

