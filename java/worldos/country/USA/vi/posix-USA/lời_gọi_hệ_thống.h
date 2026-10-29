#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Mở open
#define Đọc read
#define Ghi write
#define Đóng_tập_tin close
#define seek lseek
#define sync fsync
#define Gỡ_bỏ unlink
#define Kết_nối connect
