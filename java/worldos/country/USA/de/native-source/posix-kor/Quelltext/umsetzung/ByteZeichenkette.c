#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *Zeichenkette) { size_t Länge = 0; while (Zeichenkette[Länge]) Länge++; return Länge; }
int strcmp(const char *vorderseiteWert, const char *rückseiteWert) {
    while (*vorderseiteWert && *vorderseiteWert == *rückseiteWert) { vorderseiteWert++; rückseiteWert++; }
    return (unsigned char)*vorderseiteWert - (unsigned char)*rückseiteWert;
}
int memcmp(const void *vorderseiteWert, const void *rückseiteWert, size_t byteAnzahl) {
    const unsigned char *ersterOperand = vorderseiteWert, *zweiterOperand = rückseiteWert;
    for (size_t platzEintrag = 0; platzEintrag < byteAnzahl; platzEintrag++) if (ersterOperand[platzEintrag] != zweiterOperand[platzEintrag]) return ersterOperand[platzEintrag] - zweiterOperand[platzEintrag];
    return 0;
}
void *memcpy(void *zielWert, const void *ursprünglich, size_t byteAnzahl) {
    unsigned char *ersterOperand = zielWert; const unsigned char *zweiterOperand = ursprünglich;
    for (size_t platzEintrag = 0; platzEintrag < byteAnzahl; platzEintrag++) ersterOperand[platzEintrag] = zweiterOperand[platzEintrag];
    return zielWert;
}
void *memset(void *zielWert, int Wert, size_t byteAnzahl) {
    unsigned char *Daten = zielWert;
    for (size_t platzEintrag = 0; platzEintrag < byteAnzahl; platzEintrag++) Daten[platzEintrag] = Wert;
    return zielWert;
}
int putchar(int Zeichen) { unsigned char Wert = Zeichen; return write(1, &Wert, 1) == 1 ? Wert : EOF; }
int puts(const char *Zeichenkette) {
    size_t Länge = strlen(Zeichenkette), position = 0;
    while (position < Länge) { ssize_t ergebnis = write(1, Zeichenkette + position, Länge - position); if (ergebnis <= 0) return EOF; position += ergebnis; }
    return putchar('\n') == EOF ? EOF : 0;
}
