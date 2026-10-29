#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define öffnen open
#define lesen read
#define schreiben write
#define schließen close
#define positionieren lseek
#define abgleichen fsync
#define entfernen unlink
#define verbinden connect
