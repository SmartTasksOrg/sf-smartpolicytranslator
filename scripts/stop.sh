#!/usr/bin/env bash
cd "$(dirname "$0")/.."
[ -f .spt.pid ] && kill "$(cat .spt.pid)" 2>/dev/null && rm -f .spt.pid && echo "service stopped" || echo "no service pid found"
