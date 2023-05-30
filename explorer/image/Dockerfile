# this docker file create your own ubuntu

FROM ubuntu

# Update the package lists
RUN apt-get update

# Install network utilities
RUN apt-get install -y \
                iputils-ping \
                wget \
                dnsutils \
                net-tools \
                curl \
                git \
                nano \
                unzip \
                zip \
                python3 \
                python3-pip

# Set the hostname to 'ddd'
RUN echo 'nnt' > /etc/hostname

# Create a new user
RUN useradd -m nnt

# Set password for nnt user
RUN echo 'nnt:dtd' | chpasswd

# Set the default working directory
WORKDIR /home/nnt

# Set the new user as the default user
USER nnt

CMD ["/bin/bash"]
