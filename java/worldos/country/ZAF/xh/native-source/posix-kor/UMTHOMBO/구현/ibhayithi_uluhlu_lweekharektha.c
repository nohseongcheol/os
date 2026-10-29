#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *uluhlu_lweekharektha_ixabiso) { size_t ubude_ixabiso = 0; while (uluhlu_lweekharektha_ixabiso[ubude_ixabiso]) ubude_ixabiso++; return ubude_ixabiso; }
int strcmp(const char *앞, const char *Emva_ixabiso) {
    while (*앞 && *앞 == *Emva_ixabiso) { 앞++; Emva_ixabiso++; }
    return (unsigned char)*앞 - (unsigned char)*Emva_ixabiso;
}
int memcmp(const void *앞, const void *Emva_ixabiso, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = Emva_ixabiso;
    for (size_t isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < 바이트수; isithuba_ufako_nkcukacha++) if (가[isithuba_ufako_nkcukacha] != 나[isithuba_ufako_nkcukacha]) return 가[isithuba_ufako_nkcukacha] - 나[isithuba_ufako_nkcukacha];
    return 0;
}
void *memcpy(void *indawo_ekuyiwa_kuyo_ixabiso, const void *원본, size_t 바이트수) {
    unsigned char *가 = indawo_ekuyiwa_kuyo_ixabiso; const unsigned char *나 = 원본;
    for (size_t isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < 바이트수; isithuba_ufako_nkcukacha++) 가[isithuba_ufako_nkcukacha] = 나[isithuba_ufako_nkcukacha];
    return indawo_ekuyiwa_kuyo_ixabiso;
}
void *memset(void *indawo_ekuyiwa_kuyo_ixabiso, int ixabiso, size_t 바이트수) {
    unsigned char *iingcombolo = indawo_ekuyiwa_kuyo_ixabiso;
    for (size_t isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < 바이트수; isithuba_ufako_nkcukacha++) iingcombolo[isithuba_ufako_nkcukacha] = ixabiso;
    return indawo_ekuyiwa_kuyo_ixabiso;
}
int putchar(int 문자) { unsigned char ixabiso = 문자; return write(1, &ixabiso, 1) == 1 ? ixabiso : EOF; }
int puts(const char *uluhlu_lweekharektha_ixabiso) {
    size_t ubude_ixabiso = strlen(uluhlu_lweekharektha_ixabiso), 위치 = 0;
    while (위치 < ubude_ixabiso) { ssize_t 결과 = write(1, uluhlu_lweekharektha_ixabiso + 위치, ubude_ixabiso - 위치); if (결과 <= 0) return EOF; 위치 += 결과; }
    return putchar('\n') == EOF ? EOF : 0;
}
