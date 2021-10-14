##!/usr/bin/env sh
#
#WKHTML2PDF_VERSION='0.12.4'
#
#sudo apt-get install -y openssl build-essential xorg libssl-dev
#wget "https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/${WKHTML2PDF_VERSION}/wkhtmltox-${WKHTML2PDF_VERSION}_linux-generic-amd64.tar.xz"
#tar -xJf "wkhtmltox-${WKHTML2PDF_VERSION}_linux-generic-amd64.tar.xz"
#cd wkhtmltox
#sudo chown root:root bin/wkhtmltopdf
#sudo cp -r ./* /usr/


main(){
    install_ubuntu
    update_packages
    install_packages
    install_opencv
    install_pillow
    install_dependencies
    # should_start
}

update_packages(){
    echo "Updating Packages..."
    apt update
    apt upgrade -y
    clear
}

install_packages(){
    echo "Installing missing Packages..."
    apt install -y \
        python \
        wget \
        git \
        ffmpeg \
        mediainfo \
        neofetch \
        jq \
        libatlas-base-dev \
        libavcodec-dev \
        libavdevice-dev \
        libavfilter-dev \
        libavformat-dev \
        libavutil-dev \
        libboost-python-dev \
        libcurl4-openssl-dev \
        libffi-dev \
        libgconf-2-4 \
        libgtk-3-dev \
        libjpeg-dev \
        libjpeg62-turbo-dev \
        libopus-dev \
        libopus0 \
        libpq-dev \
        libreadline-dev \
        libswresample-dev \
        libswscale-dev \
        libssl-dev \
        libwebp-dev \
        libx11-dev \
        libxi6 \
        libxml2-dev \
        libxslt1-dev \
        libyaml-dev \
        megatools \
        openssh-client \
        openssh-server \
        openssl \
        p7zip-full \
        pdftk \
        procps \
        unzip \
        wkhtmltopdf \
        zip
    clear
    echo "Remove Unused packages..."
    apt autoremove --purge
    clear
}