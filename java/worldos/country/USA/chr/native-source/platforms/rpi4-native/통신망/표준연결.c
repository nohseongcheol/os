#include "string.h"
size_t strlen(const char *ᎠᏍᏘ_ᎦᏟᏌᏅᎯ) { const char *자료위치 = ᎠᏍᏘ_ᎦᏟᏌᏅᎯ; while (*자료위치) 자료위치++; return 자료위치 - ᎠᏍᏘ_ᎦᏟᏌᏅᎯ; }
int memcmp(const void *첫째값, const void *둘째값, size_t 개수) { const unsigned char *가로좌표 = 첫째값, *세로좌표 = 둘째값; while (개수--) { if (*가로좌표 != *세로좌표) return (int)*가로좌표 - *세로좌표; 가로좌표++; 세로좌표++; } return 0; }
void *memmove(void *ᏮᎦᏛᎢ_ᎦᏟᏌᏅᎯ, const void *ᎠᏍᏘ_ᎦᏟᏌᏅᎯ, size_t 개수) { unsigned char *가로좌표 = ᏮᎦᏛᎢ_ᎦᏟᏌᏅᎯ; const unsigned char *세로좌표 = ᎠᏍᏘ_ᎦᏟᏌᏅᎯ; if (가로좌표 < 세로좌표) { for (size_t 순번 = 0; 순번 < 개수; 순번++) 가로좌표[순번] = 세로좌표[순번]; } else { while (개수) { 개수--; 가로좌표[개수] = 세로좌표[개수]; } } return ᏮᎦᏛᎢ_ᎦᏟᏌᏅᎯ; }
int strncmp(const char *첫째값, const char *둘째값, size_t 개수) { while (개수--) { unsigned char 가로좌표 = *첫째값++, 세로좌표 = *둘째값++; if (가로좌표 != 세로좌표) return (int)가로좌표-세로좌표; if (!가로좌표) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *ᎠᏍᏘ_ᎦᏟᏌᏅᎯ, char **끝위치, int ᎠᏍᏆᏚᎸ_ᎦᏯᎸᏗ_ᏧᎬᏩᎶᏗᏯ) {
    const char *시작위치 = ᎠᏍᏘ_ᎦᏟᏌᏅᎯ; unsigned long ᏧᎬᏩᎶᏗᏯ = 0; int ᎪᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ = 1, 하나라도 = 0;
    while (*ᎠᏍᏘ_ᎦᏟᏌᏅᎯ == ' ' || (*ᎠᏍᏘ_ᎦᏟᏌᏅᎯ >= 9 && *ᎠᏍᏘ_ᎦᏟᏌᏅᎯ <= 13)) ᎠᏍᏘ_ᎦᏟᏌᏅᎯ++;
    if (*ᎠᏍᏘ_ᎦᏟᏌᏅᎯ == '-' || *ᎠᏍᏘ_ᎦᏟᏌᏅᎯ == '+') { if (*ᎠᏍᏘ_ᎦᏟᏌᏅᎯ == '-') ᎪᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ = -1; ᎠᏍᏘ_ᎦᏟᏌᏅᎯ++; }
    if (ᎠᏍᏆᏚᎸ_ᎦᏯᎸᏗ_ᏧᎬᏩᎶᏗᏯ == 0) ᎠᏍᏆᏚᎸ_ᎦᏯᎸᏗ_ᏧᎬᏩᎶᏗᏯ = 10;
    while (*ᎠᏍᏘ_ᎦᏟᏌᏅᎯ >= '0' && *ᎠᏍᏘ_ᎦᏟᏌᏅᎯ <= '9' && *ᎠᏍᏘ_ᎦᏟᏌᏅᎯ - '0' < ᎠᏍᏆᏚᎸ_ᎦᏯᎸᏗ_ᏧᎬᏩᎶᏗᏯ) {
        unsigned 숫자 = *ᎠᏍᏘ_ᎦᏟᏌᏅᎯ++ - '0'; 하나라도 = 1;
        if (ᏧᎬᏩᎶᏗᏯ > (0x7ffffffffffffffful - 숫자) / (unsigned)ᎠᏍᏆᏚᎸ_ᎦᏯᎸᏗ_ᏧᎬᏩᎶᏗᏯ) ᏧᎬᏩᎶᏗᏯ = 0x7ffffffffffffffful;
        else ᏧᎬᏩᎶᏗᏯ = ᏧᎬᏩᎶᏗᏯ * ᎠᏍᏆᏚᎸ_ᎦᏯᎸᏗ_ᏧᎬᏩᎶᏗᏯ + 숫자;
    }
    if (끝위치) *끝위치 = (char *)(하나라도 ? ᎠᏍᏘ_ᎦᏟᏌᏅᎯ : 시작위치); return ᎪᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ > 0 ? (long)ᏧᎬᏩᎶᏗᏯ : -(long)ᏧᎬᏩᎶᏗᏯ;
}
int atoi(const char *ᎠᏍᏘ_ᎦᏟᏌᏅᎯ) { return (int)strtol(ᎠᏍᏘ_ᎦᏟᏌᏅᎯ, 0, 10); }
