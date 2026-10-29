#ifndef systemnahNetzwerkKopf
#define systemnahNetzwerkKopf
#include <stdint.h>
#include <stddef.h>
void netzwerkVorbereiten(void);
void netzwerkUntersuchen(void);
int netzbuchseEndpunktErstellen(int typKategorie);
int netzZuordnen(int dateiKennwert, uint32_t adresse, unsigned portNummer);
int netzLauschen(int dateiKennwert);
void wiederverwendenNetzbuchseAdresse(int dateiKennwert);
int netzVerbinden(int dateiKennwert, uint32_t adresse, unsigned portNummer);
int netzAnnehmen(int dateiKennwert);
int netzLesen(int dateiKennwert, void *Daten, unsigned elementeintragAnzahl);
int netzSchreiben(int dateiKennwert, const void *Daten, unsigned elementeintragAnzahl);
int datagrammSenden(int dateiKennwert, const void *Daten, unsigned elementeintragAnzahl, uint32_t adresse, unsigned portNummer);
int datagrammEmpfangen(int dateiKennwert, void *Daten, unsigned elementeintragAnzahl);
unsigned netzwerkPortNummer(int dateiKennwert);
unsigned gegenstellePortNummer(int dateiKennwert);
uint32_t netzGegenstelleAdresse(int dateiKennwert);
void netzwerkSchließen(int dateiKennwert);
int dateiÜbertragungSteuerung(int aktion);
void dateiÜbertragungUntersuchen(void);
uint32_t netzwerkZustandLesen(unsigned eintragWert, unsigned Nummer);
int netzwerkKonfigurieren(unsigned aktion, uint32_t adresse, uint32_t maskeWert, uint32_t netzübergangWert);
int rückmeldungPrüfungStarten(uint32_t adresse, unsigned reihenfolgeWert);
int rückmeldungPrüfungLesen(unsigned eintragWert);
#endif
