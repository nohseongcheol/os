#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Адкрыць open
#define Чытанне read
#define Запіс write
#define Закрыць close
#define seek lseek
#define sync fsync
#define Выдаліць unlink
#define Злучыцца connect
