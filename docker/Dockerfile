FROM ros:humble

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y git

RUN git clone https://github.com/patrykcieslak/stonefish

RUN apt-get install -y \
    libsdl2-dev \
    libglm-dev \
    libfreetype6-dev \
    ros-humble-pcl-conversions \
    ros-humble-image-transport \
    tmux \
    python3-pip
    
RUN cd stonefish && \
    mkdir -p build && \
    cd build && cmake .. && \
    make -j4 && make install 

RUN mkdir -p stonefish_ws/src && \
    cd stonefish_ws/src && git clone https://github.com/patrykcieslak/stonefish_ros2.git

RUN /bin/bash -c "source /opt/ros/humble/setup.bash && \
    cd /stonefish_ws && \
    export MAKEFLAGS='-j1 -l1' && colcon build"

ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

COPY . ros2_ws/src

RUN /bin/bash -c "source /opt/ros/humble/setup.bash && \
    source stonefish_ws/install/setup.bash && \
    cd /ros2_ws && \
    colcon build --packages-select cybership_simulation_common"

ENTRYPOINT ["/bin/bash", "-c", "source /opt/ros/humble/setup.bash &&\
             source stonefish_ws/install/setup.bash &&\
             source ros2_ws/install/setup.bash &&\
             ros2 launch cybership_simulation_common simulation_nogpu.launch.py"]
         

