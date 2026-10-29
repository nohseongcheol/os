#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define เปิด open
#define อ่าน read
#define เขียน write
#define ปิด close
#define seek lseek
#define sync fsync
#define ลบ unlink
#define เชื่อมต่อ connect
