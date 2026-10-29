#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define തുറക്കുക open
#define വായന read
#define എഴുത്തു് write
#define അടയ്ക്കു close
#define seek lseek
#define sync fsync
#define നീക്കം_ചെയ്യുക unlink
#define കണക്ടു്_ചെയ്യുക connect
