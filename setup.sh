#!/bin/bash
# これはyahoojapanさんのNGTをGRPCで利用するためのセットアップに関するファイルです
# 実行して出来たファイル内に書いてあるLicenseに従って利用してください

cd /app
curl -O https://raw.githubusercontent.com/yahoojapan/ngtd/master/proto/ngtd.proto
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ngtd.proto
