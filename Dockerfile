# Pull base image
FROM ubuntu:18.04

# RUN apt-get update && apt-get install -y software-properties-common

RUN apt update && apt install -y curl

# Install Java 11 and Maven
RUN apt update 
# RUN apt -y install default-jre
# RUN apt -y install default-jdk

RUN curl -O https://download.java.net/java/GA/jdk15.0.2/0d1cfde4252546c6931946de8db48ee2/7/GPL/openjdk-15.0.2_linux-x64_bin.tar.gz
RUN tar -xvf openjdk-15.0.2_linux-x64_bin.tar.gz
RUN mv jdk-15.0.2 /opt/
ENV JAVA_HOME=/opt/jdk-15.0.2
ENV PATH="${PATH}:${JAVA_HOME}/bin"
CMD echo java -version
CMD echo ${PATH}

# RUN echo oracle-java14-installer shared/accepted-oracle-license-v1-2 select true | sudo /usr/bin/debconf-set-selections
# RUN add-apt-repository ppa:linuxuprising/java
# RUN apt update
# RUN apt -y install oracle-java14-installer

RUN apt -y install maven

# Install default pom dependencies with Maven
RUN mkdir default_pom
COPY default_pom.xml default_pom/pom.xml
WORKDIR default_pom
RUN mvn install
WORKDIR ..

# Install git
RUN apt -y install git

# Pass current time to force rebuild from this point
ARG CACHE_DATE=use_cache_if_no_date_passed


# ===================== #
# ======= group ======= #
# ===================== #
ARG GROUP_ID
ARG GROUP_REPO
ARG GROUP_DIR

# Clone repo
RUN git clone ${GROUP_REPO}

# Enter directory
WORKDIR ${GROUP_DIR}

RUN rm -rf *.idea
RUN rm -rf *.iml

# Execute tests
RUN mvn clean test sonar:sonar -Dsonar.projectKey=${GROUP_ID} -Dsonar.host.url=http://localhost:9000 -Dsonar.login=admin -Dsonar.password=admin ; exit 0

# Delete files
WORKDIR ..
RUN rm -rf ${GROUP_DIR}
