#! /bin/bash
log_folder="build_logs_$(date +%Y-%m-%d_%H-%M-%S)"
mkdir -p logs
mkdir -p logs/$log_folder
sudo docker build . -t "ingsw" --network=host --build-arg CACHE_DATE=$(date +%Y-%m-%d_%H-%M-%S) --build-arg GROUP_ID="group-05" --build-arg GROUP_REPO="https://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@github.com/ValentinaSona/ing-sw-2021-sona-shenouda-singh" --build-arg GROUP_DIR="ing-sw-2021-sona-shenouda-singh"  | tee logs/$log_folder/group-05_RAW.txt
sudo docker build . -t "ingsw" --network=host --build-arg CACHE_DATE=$(date +%Y-%m-%d_%H-%M-%S) --build-arg GROUP_ID="group-10" --build-arg GROUP_REPO="https://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@github.com/LucaPolattini/ing-sw-2021-polattini-ratzonel-salaris.git" --build-arg GROUP_DIR="ing-sw-2021-polattini-ratzonel-salaris"  | tee logs/$log_folder/group-10_RAW.txt
