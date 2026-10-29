#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Öppna open
#define Läs read
#define Skriv write
#define Stäng close
#define seek lseek
#define sync fsync
#define Ta_bort unlink
#define Anslut connect
