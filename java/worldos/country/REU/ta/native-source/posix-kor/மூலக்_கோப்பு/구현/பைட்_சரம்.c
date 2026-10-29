#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *சரம்_மதிப்பு) { size_t நீளம்_மதிப்பு = 0; while (சரம்_மதிப்பு[நீளம்_மதிப்பு]) நீளம்_மதிப்பு++; return நீளம்_மதிப்பு; }
int strcmp(const char *முன்_மதிப்பு, const char *பின்_மதிப்பு) {
    while (*முன்_மதிப்பு && *முன்_மதிப்பு == *பின்_மதிப்பு) { முன்_மதிப்பு++; பின்_மதிப்பு++; }
    return (unsigned char)*முன்_மதிப்பு - (unsigned char)*பின்_மதிப்பு;
}
int memcmp(const void *முன்_மதிப்பு, const void *பின்_மதிப்பு, size_t 바이트수) {
    const unsigned char *가 = முன்_மதிப்பு, *나 = பின்_மதிப்பு;
    for (size_t ஸ்லாட்_உள்ளீடு = 0; ஸ்லாட்_உள்ளீடு < 바이트수; ஸ்லாட்_உள்ளீடு++) if (가[ஸ்லாட்_உள்ளீடு] != 나[ஸ்லாட்_உள்ளீடு]) return 가[ஸ்லாட்_உள்ளீடு] - 나[ஸ்லாட்_உள்ளீடு];
    return 0;
}
void *memcpy(void *இலக்கு_மதிப்பு, const void *원본, size_t 바이트수) {
    unsigned char *가 = இலக்கு_மதிப்பு; const unsigned char *나 = 원본;
    for (size_t ஸ்லாட்_உள்ளீடு = 0; ஸ்லாட்_உள்ளீடு < 바이트수; ஸ்லாட்_உள்ளீடு++) 가[ஸ்லாட்_உள்ளீடு] = 나[ஸ்லாட்_உள்ளீடு];
    return இலக்கு_மதிப்பு;
}
void *memset(void *இலக்கு_மதிப்பு, int மதிப்பு, size_t 바이트수) {
    unsigned char *தரவு = இலக்கு_மதிப்பு;
    for (size_t ஸ்லாட்_உள்ளீடு = 0; ஸ்லாட்_உள்ளீடு < 바이트수; ஸ்லாட்_உள்ளீடு++) தரவு[ஸ்லாட்_உள்ளீடு] = மதிப்பு;
    return இலக்கு_மதிப்பு;
}
int putchar(int 문자) { unsigned char மதிப்பு = 문자; return write(1, &மதிப்பு, 1) == 1 ? மதிப்பு : EOF; }
int puts(const char *சரம்_மதிப்பு) {
    size_t நீளம்_மதிப்பு = strlen(சரம்_மதிப்பு), இடம் = 0;
    while (இடம் < நீளம்_மதிப்பு) { ssize_t அளவிடக்கூடியது = write(1, சரம்_மதிப்பு + இடம், நீளம்_மதிப்பு - இடம்); if (அளவிடக்கூடியது <= 0) return EOF; இடம் += அளவிடக்கூடியது; }
    return putchar('\n') == EOF ? EOF : 0;
}
