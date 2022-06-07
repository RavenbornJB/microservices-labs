#!/bin/bash

consul agent -dev & &> /dev/null

consul kv put hz_map "distributed-map"
consul kv put hz_queue "bounded-queue"
consul kv put connect_timeout 5
consul kv put hz_address "127.0.0.1"
consul kv put logging_nodes "http://localhost:8091 http://localhost:8092 http://localhost:8093"
consul kv put messages_nodes "http://localhost:9001 http://localhost:9002"
