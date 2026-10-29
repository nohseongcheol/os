#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *igicenteruro_agaciro) { size_t uburebure_agaciro = 0; while (igicenteruro_agaciro[uburebure_agaciro]) uburebure_agaciro++; return uburebure_agaciro; }
int strcmp(const char *앞, const char *Ikibanza_agaciro) {
    while (*앞 && *앞 == *Ikibanza_agaciro) { 앞++; Ikibanza_agaciro++; }
    return (unsigned char)*앞 - (unsigned char)*Ikibanza_agaciro;
}
int memcmp(const void *앞, const void *Ikibanza_agaciro, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = Ikibanza_agaciro;
    for (size_t umwanya_icyinjizwa = 0; umwanya_icyinjizwa < 바이트수; umwanya_icyinjizwa++) if (가[umwanya_icyinjizwa] != 나[umwanya_icyinjizwa]) return 가[umwanya_icyinjizwa] - 나[umwanya_icyinjizwa];
    return 0;
}
void *memcpy(void *aho_ijya_agaciro, const void *원본, size_t 바이트수) {
    unsigned char *가 = aho_ijya_agaciro; const unsigned char *나 = 원본;
    for (size_t umwanya_icyinjizwa = 0; umwanya_icyinjizwa < 바이트수; umwanya_icyinjizwa++) 가[umwanya_icyinjizwa] = 나[umwanya_icyinjizwa];
    return aho_ijya_agaciro;
}
void *memset(void *aho_ijya_agaciro, int agaciro, size_t 바이트수) {
    unsigned char *amakurushingiro = aho_ijya_agaciro;
    for (size_t umwanya_icyinjizwa = 0; umwanya_icyinjizwa < 바이트수; umwanya_icyinjizwa++) amakurushingiro[umwanya_icyinjizwa] = agaciro;
    return aho_ijya_agaciro;
}
int putchar(int 문자) { unsigned char agaciro = 문자; return write(1, &agaciro, 1) == 1 ? agaciro : EOF; }
int puts(const char *igicenteruro_agaciro) {
    size_t uburebure_agaciro = strlen(igicenteruro_agaciro), 위치 = 0;
    while (위치 < uburebure_agaciro) { ssize_t 결과 = write(1, igicenteruro_agaciro + 위치, uburebure_agaciro - 위치); if (결과 <= 0) return EOF; 위치 += 결과; }
    return putchar('\n') == EOF ? EOF : 0;
}
