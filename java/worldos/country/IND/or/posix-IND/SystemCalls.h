#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define ଖୋଲନ୍ତୁ open
#define ପଢନ୍ତୁ read
#define ଲେଖନ୍ତୁ write
#define ବନ୍ଦ_କରନ୍ତୁ close
#define seek lseek
#define sync fsync
#define ଅପସାରଣ_କରନ୍ତୁ unlink
#define ସଂଯୋଗ_କରନ୍ତୁ connect
