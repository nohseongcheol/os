#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define ouvrir open
#define lire read
#define écrire write
#define fermer close
#define positionner lseek
#define synchroniser fsync
#define supprimer unlink
#define connecter connect
