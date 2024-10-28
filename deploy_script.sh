#!/usr/bin/env bash
# deploy_script.sh
# by colin on iamIPaddr
# revision on iamIPaddr
##################################
##脚本功能：
# 部署**运维API接口服务
#
##脚本说明：
#+ 用docker启动ck-ops API 接口服务

REGISTRY='harbor.betack.com'
IMG_TAG='v1'
CONTAINER_NAME='ck_ops'

# 删除旧有的部署
docker container rm -f $(docker container ls -q -f "name=${CONTAINER_NAME}")
# 新启动服务
#+ 把 ck-ops API 服务器启动需要的 .env 挂载到容器中
docker run --name ${CONTAINER_NAME} -itd --restart=unless-stopped \
    --mount type=bind,src='/opt/import_data/ck_ops/.env',dst='/opt/betack/.env' \
    -p iamIPaddr:iamIPaddr ${REGISTRY}/devops-tools/ck_ops:${IMG_TAG}
# 检查容器运行情况
sleep 10
docker container ls -q -f "name=${CONTAINER_NAME}"
docker container logs ${CONTAINER_NAME}

