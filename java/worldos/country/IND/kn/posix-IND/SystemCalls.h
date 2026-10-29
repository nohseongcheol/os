#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define ತೆರೆ open
#define ಓದು read
#define ಬರೆ write
#define ಮುಚ್ಚು close
#define seek lseek
#define sync fsync
#define ತೆಗೆದು_ಹಾಕು unlink
#define ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು connect
