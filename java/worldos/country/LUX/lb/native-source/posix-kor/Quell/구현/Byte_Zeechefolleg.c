#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *Zeechefolleg_VALUE) { size_t Längt_VALUE = 0; while (Zeechefolleg_VALUE[Längt_VALUE]) Längt_VALUE++; return Längt_VALUE; }
int strcmp(const char *앞, const char *Zeréck_VALUE) {
    while (*앞 && *앞 == *Zeréck_VALUE) { 앞++; Zeréck_VALUE++; }
    return (unsigned char)*앞 - (unsigned char)*Zeréck_VALUE;
}
int memcmp(const void *앞, const void *Zeréck_VALUE, size_t Byte_COUNT) {
    const unsigned char *가 = 앞, *나 = Zeréck_VALUE;
    for (size_t Slot_Agab = 0; Slot_Agab < Byte_COUNT; Slot_Agab++) if (가[Slot_Agab] != 나[Slot_Agab]) return 가[Slot_Agab] - 나[Slot_Agab];
    return 0;
}
void *memcpy(void *Zil_VALUE, const void *원본, size_t Byte_COUNT) {
    unsigned char *가 = Zil_VALUE; const unsigned char *나 = 원본;
    for (size_t Slot_Agab = 0; Slot_Agab < Byte_COUNT; Slot_Agab++) 가[Slot_Agab] = 나[Slot_Agab];
    return Zil_VALUE;
}
void *memset(void *Zil_VALUE, int VALUE, size_t Byte_COUNT) {
    unsigned char *Daten = Zil_VALUE;
    for (size_t Slot_Agab = 0; Slot_Agab < Byte_COUNT; Slot_Agab++) Daten[Slot_Agab] = VALUE;
    return Zil_VALUE;
}
int putchar(int 문자) { unsigned char VALUE = 문자; return write(1, &VALUE, 1) == 1 ? VALUE : EOF; }
int puts(const char *Zeechefolleg_VALUE) {
    size_t Längt_VALUE = strlen(Zeechefolleg_VALUE), positionéieren = 0;
    while (positionéieren < Längt_VALUE) { ssize_t Mooss = write(1, Zeechefolleg_VALUE + positionéieren, Längt_VALUE - positionéieren); if (Mooss <= 0) return EOF; positionéieren += Mooss; }
    return putchar('\n') == EOF ? EOF : 0;
}
