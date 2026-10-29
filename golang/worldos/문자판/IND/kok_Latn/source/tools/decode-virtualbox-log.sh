#!/bin/sh
set -eu

log_file=${1:-build/virtualbox-current.log}
kernel_file=${2:-build/kernel.bin}

if [ ! -r "$log_file" ]; then
	echo "log not found: $log_file" >&2
	exit 1
fi

exception_lines=$(tr -d '\000\r' < "$log_file" |
	sed -n '/EXCEPTION vec=/p; /HALTED AFTER EXCEPTION/p')

if [ -n "$exception_lines" ]; then
	printf '%s\n' "$exception_lines"
else
	echo "No exception records found. Recent guest output:"
	tail -c 2048 "$log_file" | tr -d '\000\r'
	echo
fi

if [ ! -f "$kernel_file" ]; then
	echo "kernel symbols not found: $kernel_file" >&2
	exit 1
fi

addresses=$(printf '%s\n' "$exception_lines" |
	sed -n 's/.* eip=\([[:xdigit:]]\{8\}\).*/0x\1/p' | sort -u)
if [ -n "$addresses" ]; then
	echo
	echo "Resolved exception instruction addresses:"
	for address in $addresses; do
		printf '%s: ' "$address"
		addr2line -f -C -e "$kernel_file" "$address" | tr '\n' ' '
		echo
	done
fi
