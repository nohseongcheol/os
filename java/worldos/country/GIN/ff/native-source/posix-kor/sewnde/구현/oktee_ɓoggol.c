#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *ɓoggol_njaru) { size_t njuuteendi_njaru = 0; while (ɓoggol_njaru[njuuteendi_njaru]) njuuteendi_njaru++; return njuuteendi_njaru; }
int strcmp(const char *앞, const char *Caggal_njaru) {
    while (*앞 && *앞 == *Caggal_njaru) { 앞++; Caggal_njaru++; }
    return (unsigned char)*앞 - (unsigned char)*Caggal_njaru;
}
int memcmp(const void *앞, const void *Caggal_njaru, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = Caggal_njaru;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) if (가[칸] != 나[칸]) return 가[칸] - 나[칸];
    return 0;
}
void *memcpy(void *tiindaare_njaru, const void *원본, size_t 바이트수) {
    unsigned char *가 = tiindaare_njaru; const unsigned char *나 = 원본;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) 가[칸] = 나[칸];
    return tiindaare_njaru;
}
void *memset(void *tiindaare_njaru, int njaru, size_t 바이트수) {
    unsigned char *keɓe = tiindaare_njaru;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) keɓe[칸] = njaru;
    return tiindaare_njaru;
}
int putchar(int 문자) { unsigned char njaru = 문자; return write(1, &njaru, 1) == 1 ? njaru : EOF; }
int puts(const char *ɓoggol_njaru) {
    size_t njuuteendi_njaru = strlen(ɓoggol_njaru), 위치 = 0;
    while (위치 < njuuteendi_njaru) { ssize_t 결과 = write(1, ɓoggol_njaru + 위치, njuuteendi_njaru - 위치); if (결과 <= 0) return EOF; 위치 += 결과; }
    return putchar('\n') == EOF ? EOF : 0;
}
