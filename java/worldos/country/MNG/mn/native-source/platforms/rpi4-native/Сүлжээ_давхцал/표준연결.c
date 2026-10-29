#include "string.h"
size_t strlen(const char *мөр_өгөгдөл) { const char *자료위치 = мөр_өгөгдөл; while (*자료위치) 자료위치++; return 자료위치 - мөр_өгөгдөл; }
int memcmp(const void *첫째값, const void *둘째값, size_t 개수) { const unsigned char *х_координат = 첫째값, *세로좌표 = 둘째값; while (개수--) { if (*х_координат != *세로좌표) return (int)*х_координат - *세로좌표; х_координат++; 세로좌표++; } return 0; }
void *memmove(void *товлосон_газар_өгөгдөл, const void *мөр_өгөгдөл, size_t 개수) { unsigned char *х_координат = товлосон_газар_өгөгдөл; const unsigned char *세로좌표 = мөр_өгөгдөл; if (х_координат < 세로좌표) { for (size_t 순번 = 0; 순번 < 개수; 순번++) х_координат[순번] = 세로좌표[순번]; } else { while (개수) { 개수--; х_координат[개수] = 세로좌표[개수]; } } return товлосон_газар_өгөгдөл; }
int strncmp(const char *첫째값, const char *둘째값, size_t 개수) { while (개수--) { unsigned char х_координат = *첫째값++, 세로좌표 = *둘째값++; if (х_координат != 세로좌표) return (int)х_координат-세로좌표; if (!х_координат) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *мөр_өгөгдөл, char **дуусгах_Оффсет, int Дэвсгэр_утга) {
    const char *Эхлэл_Оффсет = мөр_өгөгдөл; unsigned long утга = 0; int кодчлол_утга = 1, 하나라도 = 0;
    while (*мөр_өгөгдөл == ' ' || (*мөр_өгөгдөл >= 9 && *мөр_өгөгдөл <= 13)) мөр_өгөгдөл++;
    if (*мөр_өгөгдөл == '-' || *мөр_өгөгдөл == '+') { if (*мөр_өгөгдөл == '-') кодчлол_утга = -1; мөр_өгөгдөл++; }
    if (Дэвсгэр_утга == 0) Дэвсгэр_утга = 10;
    while (*мөр_өгөгдөл >= '0' && *мөр_өгөгдөл <= '9' && *мөр_өгөгдөл - '0' < Дэвсгэр_утга) {
        unsigned тоо_утга = *мөр_өгөгдөл++ - '0'; 하나라도 = 1;
        if (утга > (0x7ffffffffffffffful - тоо_утга) / (unsigned)Дэвсгэр_утга) утга = 0x7ffffffffffffffful;
        else утга = утга * Дэвсгэр_утга + тоо_утга;
    }
    if (дуусгах_Оффсет) *дуусгах_Оффсет = (char *)(하나라도 ? мөр_өгөгдөл : Эхлэл_Оффсет); return кодчлол_утга > 0 ? (long)утга : -(long)утга;
}
int atoi(const char *мөр_өгөгдөл) { return (int)strtol(мөр_өгөгдөл, 0, 10); }
