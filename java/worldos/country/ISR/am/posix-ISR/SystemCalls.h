#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define መክፈቻ open
#define ማንበቢያ read
#define መጻፊያ write
#define መዝጊያ close
#define seek lseek
#define sync fsync
#define ማስወገጃ unlink
#define መገናኛ connect
