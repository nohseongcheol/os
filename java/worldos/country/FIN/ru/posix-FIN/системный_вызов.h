#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Открыть open
#define Чтение read
#define Запись write
#define Закрыть close
#define seek lseek
#define sync fsync
#define Удалить unlink
#define Подключить connect
