#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define 開く open
#define 読む read
#define 書く write
#define 閉じる close
#define 位置を移す lseek
#define 記録を同期する fsync
#define 削除する unlink
#define 接続する connect
