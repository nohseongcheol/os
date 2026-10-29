#include "string.h"
size_t strlen(const char *ষ্ট্ৰিং_ডাটা) { const char *ডাটা_স্থান_সলনি_কৰক = ষ্ট্ৰিং_ডাটা; while (*ডাটা_স্থান_সলনি_কৰক) ডাটা_স্থান_সলনি_কৰক++; return ডাটা_স্থান_সলনি_কৰক - ষ্ট্ৰিং_ডাটা; }
int memcmp(const void *첫째값, const void *둘째값, size_t 개수) { const unsigned char *x_ক_ৰ্ডিনেট = 첫째값, *세로좌표 = 둘째값; while (개수--) { if (*x_ক_ৰ্ডিনেট != *세로좌표) return (int)*x_ক_ৰ্ডিনেট - *세로좌표; x_ক_ৰ্ডিনেট++; 세로좌표++; } return 0; }
void *memmove(void *গন্তব্য_স্থান_ডাটা, const void *ষ্ট্ৰিং_ডাটা, size_t 개수) { unsigned char *x_ক_ৰ্ডিনেট = গন্তব্য_স্থান_ডাটা; const unsigned char *세로좌표 = ষ্ট্ৰিং_ডাটা; if (x_ক_ৰ্ডিনেট < 세로좌표) { for (size_t 순번 = 0; 순번 < 개수; 순번++) x_ক_ৰ্ডিনেট[순번] = 세로좌표[순번]; } else { while (개수) { 개수--; x_ক_ৰ্ডিনেট[개수] = 세로좌표[개수]; } } return গন্তব্য_স্থান_ডাটা; }
int strncmp(const char *첫째값, const char *둘째값, size_t 개수) { while (개수--) { unsigned char x_ক_ৰ্ডিনেট = *첫째값++, 세로좌표 = *둘째값++; if (x_ক_ৰ্ডিনেট != 세로좌표) return (int)x_ক_ৰ্ডিনেট-세로좌표; if (!x_ক_ৰ্ডিনেট) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *ষ্ট্ৰিং_ডাটা, char **অন্ত_কৰক_অফছেট, int পটভূমি_মান) {
    const char *আৰম্ভ_অফছেট = ষ্ট্ৰিং_ডাটা; unsigned long মান = 0; int এনকোডিং_মান = 1, 하나라도 = 0;
    while (*ষ্ট্ৰিং_ডাটা == ' ' || (*ষ্ট্ৰিং_ডাটা >= 9 && *ষ্ট্ৰিং_ডাটা <= 13)) ষ্ট্ৰিং_ডাটা++;
    if (*ষ্ট্ৰিং_ডাটা == '-' || *ষ্ট্ৰিং_ডাটা == '+') { if (*ষ্ট্ৰিং_ডাটা == '-') এনকোডিং_মান = -1; ষ্ট্ৰিং_ডাটা++; }
    if (পটভূমি_মান == 0) পটভূমি_মান = 10;
    while (*ষ্ট্ৰিং_ডাটা >= '0' && *ষ্ট্ৰিং_ডাটা <= '9' && *ষ্ট্ৰিং_ডাটা - '0' < পটভূমি_মান) {
        unsigned অংক_মান = *ষ্ট্ৰিং_ডাটা++ - '0'; 하나라도 = 1;
        if (মান > (0x7ffffffffffffffful - অংক_মান) / (unsigned)পটভূমি_মান) মান = 0x7ffffffffffffffful;
        else মান = মান * পটভূমি_মান + অংক_মান;
    }
    if (অন্ত_কৰক_অফছেট) *অন্ত_কৰক_অফছেট = (char *)(하나라도 ? ষ্ট্ৰিং_ডাটা : আৰম্ভ_অফছেট); return এনকোডিং_মান > 0 ? (long)মান : -(long)মান;
}
int atoi(const char *ষ্ট্ৰিং_ডাটা) { return (int)strtol(ষ্ট্ৰিং_ডাটা, 0, 10); }
