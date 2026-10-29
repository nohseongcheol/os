#pragma once
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <pthread.h>
#define ਖੋਲ੍ਹੋ open
#define ਪੜ੍ਹਨ read
#define ਲਿਖਣ write
#define ਬੰਦ_ਕਰੋ close
#define seek lseek
#define sync fsync
#define ਹਟਾਓ unlink
#define ਕੁਨੈਕਸ਼ਨ_ਕਰੋ connect
