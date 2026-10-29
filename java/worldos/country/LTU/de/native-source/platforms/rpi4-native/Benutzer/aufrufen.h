#ifndef systemnahBenutzerAufrufVorgangKopf
#define systemnahBenutzerAufrufVorgangKopf
#include <stdint.h>
#include <stddef.h>
// JKOROS ABI v1: x8=aufrufen Nummer, x0..x5=argumente, x0=ergebnis/negativWert fehler. Linux ABI 아님.
static inline intptr_t benutzerAufrufen(uintptr_t Nummer, uintptr_t ersterOperand, uintptr_t zweiterOperand, uintptr_t dritterOperand,
                                uintptr_t vierterOperand, uintptr_t fünfterOperand, uintptr_t sechsterOperand) {
    register uintptr_t nullwertRegister __asm__("x0") = ersterOperand;
    register uintptr_t einsRegister __asm__("x1") = zweiterOperand;
    register uintptr_t zweiRegister __asm__("x2") = dritterOperand;
    register uintptr_t dreiRegister __asm__("x3") = vierterOperand;
    register uintptr_t vierRegister __asm__("x4") = fünfterOperand;
    register uintptr_t fünfRegister __asm__("x5") = sechsterOperand;
    register uintptr_t achtRegister __asm__("x8") = Nummer;
    __asm__ volatile("svc #0" : "+r"(nullwertRegister) : "r"(einsRegister), "r"(zweiRegister), "r"(dreiRegister), "r"(vierRegister), "r"(fünfRegister), "r"(achtRegister) : "memory", "cc");
    return (intptr_t)nullwertRegister;
}
static inline intptr_t bildschirmRechteck(unsigned waagerechteKoordinateKoordinate, unsigned senkrechteKoordinateKoordinate, unsigned angefordertBreiteWert, unsigned angefordertHöheWert, unsigned rGBFarbe) {
    return benutzerAufrufen(13, waagerechteKoordinateKoordinate, senkrechteKoordinateKoordinate, rGBFarbe, angefordertBreiteWert, angefordertHöheWert, 0);
}
static inline intptr_t benutzerSpeicherEnde(uintptr_t endung) { return benutzerAufrufen(8, endung, 0, 0, 0, 0, 0); }
static inline intptr_t bildschirmBreiteLesen(void) { return benutzerAufrufen(22, 0, 0, 0, 0, 0, 0); }
static inline intptr_t bildschirmHöheLesen(void) { return benutzerAufrufen(22, 1, 0, 0, 0, 0, 0); }
static inline intptr_t fürBildschirmTasteWarten(void) {
    intptr_t ergebnis = benutzerAufrufen(16, 0, 0, 0, 0, 0, 0);
    if (ergebnis < 0) return ergebnis;
    do { ergebnis = benutzerAufrufen(16, 1, 0, 0, 0, 0, 0); } while (ergebnis == -11);
    benutzerAufrufen(16, 2, 0, 0, 0, 0, 0);
    return ergebnis;
}
static inline intptr_t benutzerArgumentAnzahl(void) { return benutzerAufrufen(15, UINTPTR_MAX, 0, 0, 0, 0, 0); }
static inline intptr_t benutzerArgument(unsigned Nummer, char *inhaltswertWert, size_t größe) {
    return benutzerAufrufen(15, Nummer, (uintptr_t)inhaltswertWert, größe, 0, 0, 0);
}
#endif
