#!/bin/bash
{
mkdir -p ~/.ssh
cat > ~/.ssh/config <<EOF
Host github.com
    StrictHostKeyChecking no
EOF

export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
cd /data
} &> /dev/null
cp .pypirc ~/.pypirc | true
# use "ant test -Dtest=<testname>" to single test
ant $*
