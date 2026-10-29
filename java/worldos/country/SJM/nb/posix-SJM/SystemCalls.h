#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Åpne open
#define Les read
#define Skriv write
#define Lukk close
#define seek lseek
#define sync fsync
#define Fjern unlink
#define Koble_til connect
