FROM debian:bookworm-slim

RUN apt-get update && \
    apt-get install -y hping3 iproute2 && \
    rm -rf /var/lib/apt/lists/*

CMD ["bash"]