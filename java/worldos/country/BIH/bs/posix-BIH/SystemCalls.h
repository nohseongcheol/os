#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Otvori open
#define Čitaj read
#define Piši write
#define Zatvori close
#define seek lseek
#define sync fsync
#define Ukloni unlink
#define Spoji_se connect
