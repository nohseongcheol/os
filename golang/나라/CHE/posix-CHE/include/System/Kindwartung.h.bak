#ifndef _include_System_Kindwartung
#define _include_System_Kindwartung

#include <System/Datentypen.h>

#define WNOHANG 1
#define WEXITSTATUS(Status) (((Status) >> 8) & 0xff)
#define WIFEXITED(Status) (((Status) & 0x7f) == 0)

#ifdef __cplusplus
extern "C" {
#endif
pid_t Kind_abwarten(int *Status);
pid_t bestimmtes_Kind_abwarten(pid_t pid, int *Status, int options);
#ifdef __cplusplus
}
#endif

#endif
