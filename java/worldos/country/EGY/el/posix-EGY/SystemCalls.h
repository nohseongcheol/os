#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Άνοιγμα open
#define Ανάγνωση read
#define Εγγραφή write
#define Κλείσιμο close
#define seek lseek
#define sync fsync
#define Αφαίρεση unlink
#define Σύνδεση connect
