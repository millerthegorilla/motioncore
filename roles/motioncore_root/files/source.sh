#!/bin/bash
ip -f inet addr show tun0 | sed -En -e 's/.*inet ([0-9.]+).*/\1/p'
