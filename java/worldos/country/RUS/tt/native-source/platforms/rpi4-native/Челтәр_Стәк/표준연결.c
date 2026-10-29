#include "string.h"
size_t strlen(const char *юл_мәгълүмат) { const char *мәгълүмат_урнаштыру = юл_мәгълүмат; while (*мәгълүмат_урнаштыру) мәгълүмат_урнаштыру++; return мәгълүмат_урнаштыру - юл_мәгълүмат; }
int memcmp(const void *첫째값, const void *SECOND_VALUE, size_t элемент_COUNT) { const unsigned char *X_координатасы = 첫째값, *세로좌표 = SECOND_VALUE; while (элемент_COUNT--) { if (*X_координатасы != *세로좌표) return (int)*X_координатасы - *세로좌표; X_координатасы++; 세로좌표++; } return 0; }
void *memmove(void *күчерү_урыны_мәгълүмат, const void *юл_мәгълүмат, size_t элемент_COUNT) { unsigned char *X_координатасы = күчерү_урыны_мәгълүмат; const unsigned char *세로좌표 = юл_мәгълүмат; if (X_координатасы < 세로좌표) { for (size_t 순번 = 0; 순번 < элемент_COUNT; 순번++) X_координатасы[순번] = 세로좌표[순번]; } else { while (элемент_COUNT) { элемент_COUNT--; X_координатасы[элемент_COUNT] = 세로좌표[элемент_COUNT]; } } return күчерү_урыны_мәгълүмат; }
int strncmp(const char *첫째값, const char *SECOND_VALUE, size_t элемент_COUNT) { while (элемент_COUNT--) { unsigned char X_координатасы = *첫째값++, 세로좌표 = *SECOND_VALUE++; if (X_координатасы != 세로좌표) return (int)X_координатасы-세로좌표; if (!X_координатасы) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *юл_мәгълүмат, char **тәмамлау_OFFSET, int Фон_VALUE) {
    const char *Start_OFFSET = юл_мәгълүмат; unsigned long VALUE = 0; int кодлау_VALUE = 1, 하나라도 = 0;
    while (*юл_мәгълүмат == ' ' || (*юл_мәгълүмат >= 9 && *юл_мәгълүмат <= 13)) юл_мәгълүмат++;
    if (*юл_мәгълүмат == '-' || *юл_мәгълүмат == '+') { if (*юл_мәгълүмат == '-') кодлау_VALUE = -1; юл_мәгълүмат++; }
    if (Фон_VALUE == 0) Фон_VALUE = 10;
    while (*юл_мәгълүмат >= '0' && *юл_мәгълүмат <= '9' && *юл_мәгълүмат - '0' < Фон_VALUE) {
        unsigned сан_VALUE = *юл_мәгълүмат++ - '0'; 하나라도 = 1;
        if (VALUE > (0x7ffffffffffffffful - сан_VALUE) / (unsigned)Фон_VALUE) VALUE = 0x7ffffffffffffffful;
        else VALUE = VALUE * Фон_VALUE + сан_VALUE;
    }
    if (тәмамлау_OFFSET) *тәмамлау_OFFSET = (char *)(하나라도 ? юл_мәгълүмат : Start_OFFSET); return кодлау_VALUE > 0 ? (long)VALUE : -(long)VALUE;
}
int atoi(const char *юл_мәгълүмат) { return (int)strtol(юл_мәгълүмат, 0, 10); }
