#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *Zare_Daraja) { size_t Tsawo_Daraja = 0; while (Zare_Daraja[Tsawo_Daraja]) Tsawo_Daraja++; return Tsawo_Daraja; }
int strcmp(const char *kyamarar_gaba_Daraja, const char *Baya_Daraja) {
    while (*kyamarar_gaba_Daraja && *kyamarar_gaba_Daraja == *Baya_Daraja) { kyamarar_gaba_Daraja++; Baya_Daraja++; }
    return (unsigned char)*kyamarar_gaba_Daraja - (unsigned char)*Baya_Daraja;
}
int memcmp(const void *kyamarar_gaba_Daraja, const void *Baya_Daraja, size_t 바이트수) {
    const unsigned char *가 = kyamarar_gaba_Daraja, *나 = Baya_Daraja;
    for (size_t rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < 바이트수; rami_Mashigar_bayanai++) if (가[rami_Mashigar_bayanai] != 나[rami_Mashigar_bayanai]) return 가[rami_Mashigar_bayanai] - 나[rami_Mashigar_bayanai];
    return 0;
}
void *memcpy(void *Zangon_ƙarshe_Daraja, const void *원본, size_t 바이트수) {
    unsigned char *가 = Zangon_ƙarshe_Daraja; const unsigned char *나 = 원본;
    for (size_t rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < 바이트수; rami_Mashigar_bayanai++) 가[rami_Mashigar_bayanai] = 나[rami_Mashigar_bayanai];
    return Zangon_ƙarshe_Daraja;
}
void *memset(void *Zangon_ƙarshe_Daraja, int Daraja, size_t 바이트수) {
    unsigned char *Tarin_bayani = Zangon_ƙarshe_Daraja;
    for (size_t rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < 바이트수; rami_Mashigar_bayanai++) Tarin_bayani[rami_Mashigar_bayanai] = Daraja;
    return Zangon_ƙarshe_Daraja;
}
int putchar(int 문자) { unsigned char Daraja = 문자; return write(1, &Daraja, 1) == 1 ? Daraja : EOF; }
int puts(const char *Zare_Daraja) {
    size_t Tsawo_Daraja = strlen(Zare_Daraja), 위치 = 0;
    while (위치 < Tsawo_Daraja) { ssize_t 결과 = write(1, Zare_Daraja + 위치, Tsawo_Daraja - 위치); if (결과 <= 0) return EOF; 위치 += 결과; }
    return putchar('\n') == EOF ? EOF : 0;
}
