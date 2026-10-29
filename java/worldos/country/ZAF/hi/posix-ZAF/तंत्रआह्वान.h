#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define खोलें open
#define पढ़ें read
#define लिखें write
#define बंदकरें close
#define स्थानबदलें lseek
#define समक्रमण fsync
#define हटाएँ unlink
#define जोड़ना connect
