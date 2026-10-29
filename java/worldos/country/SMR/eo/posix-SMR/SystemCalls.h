#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define Malfermu open
#define Lego read
#define Skribo write
#define Fermu close
#define seek lseek
#define sync fsync
#define Forigi unlink
#define Konekti connect
