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
RUN echo 'attacker' > /etc/hostname

# Create a new user
RUN useradd -m attacker

# Set password for attacker user
RUN echo 'attacker:attacker' | chpasswd

# Set the default working directory
WORKDIR /home/attacker

# Set the new user as the default user
USER attacker

CMD ["/bin/bash"]
