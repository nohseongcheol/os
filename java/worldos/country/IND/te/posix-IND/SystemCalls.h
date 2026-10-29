#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define తెరువు open
#define చదువు read
#define వ్రాయుము write
#define మూసివేయి close
#define seek lseek
#define sync fsync
#define తీసివేయు unlink
#define కనెక్టుచేయి connect
