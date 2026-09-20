FROM rust:1.89-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends python3.13 python3-pip nodejs npm zstd make git && rm -rf /var/lib/apt/lists/*
RUN npm install -g pnpm@10.5.0
WORKDIR /workspace
COPY . /workspace/neon_dynasty
RUN python3 -m pip install --break-system-packages -r /workspace/neon_dynasty/requirements-math.txt
