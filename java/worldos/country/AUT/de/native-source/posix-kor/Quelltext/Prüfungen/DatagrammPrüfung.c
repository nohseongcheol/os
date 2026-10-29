#include <DateiABI.h>
#include <NetzwerkABI.h>
#include <string.h>
#include <stdio.h>

#define überprüfen(bedingung) do { if (!(bedingung)) { puts("POSIX UDP CHECK FAILED: " #bedingung); return 1; } } while (0)
int main(int argumenteAnzahl, char **argumentListe) {
    überprüfen(argumenteAnzahl == 2);
    int portNummer = 0;
    for (int platzEintrag = 0; argumentListe[1][platzEintrag]; platzEintrag++) {
        überprüfen(argumentListe[1][platzEintrag] >= '0' && argumentListe[1][platzEintrag] <= '9');
        portNummer = portNummer * 10 + argumentListe[1][platzEintrag] - '0';
        überprüfen(portNummer <= 65535);
    }
    int endpunktWert = endpunktErstellen(AF_INET, SOCK_DGRAM, 0);
    überprüfen(endpunktWert == 3);
    struct sockaddr_in lokalGültigkeitsbereich = {0}, gegenstelleWert = {0}, empfangenWertAdresse = {0};
    lokalGültigkeitsbereich.sin_family = AF_INET;
    socklen_t Länge = sizeof lokalGültigkeitsbereich;
    überprüfen(netzbuchseAdresseLesen(endpunktWert, (struct sockaddr *)&lokalGültigkeitsbereich, &Länge) == 0 && lokalGültigkeitsbereich.sin_port == 0);
    überprüfen(adresseZuordnen(endpunktWert, (struct sockaddr *)&lokalGültigkeitsbereich, sizeof lokalGültigkeitsbereich) == 0);
    überprüfen(netzbuchseAdresseLesen(endpunktWert, (struct sockaddr *)&lokalGültigkeitsbereich, &Länge) == 0 && ntohs(lokalGültigkeitsbereich.sin_port) >= 49152);
    überprüfen(adresseZuordnen(endpunktWert, (struct sockaddr *)&lokalGültigkeitsbereich, sizeof lokalGültigkeitsbereich) == -1 && errno == EINVAL);
    int zweiterOrdnungszahl = socket(AF_INET, SOCK_DGRAM, 0);
    überprüfen(bind(zweiterOrdnungszahl, (struct sockaddr *)&lokalGültigkeitsbereich, sizeof lokalGültigkeitsbereich) == -1 && errno == EADDRINUSE);
    überprüfen(close(zweiterOrdnungszahl) == 0);
    zweiterOrdnungszahl = dup(endpunktWert);
    überprüfen(close(endpunktWert) == 0); endpunktWert = zweiterOrdnungszahl;
    gegenstelleWert.sin_family = AF_INET; gegenstelleWert.sin_port = netzwerkKurz(portNummer);
    überprüfen(netzwerkAdresseAnalysieren(AF_INET, "10.0.2.2", &gegenstelleWert.sin_addr) == 1);
    struct timeval wertWarten = {0, 200000};
    überprüfen(netzwerkEinstellungenÄndern(endpunktWert, SOL_SOCKET, SO_RCVTIMEO, &wertWarten, sizeof wertWarten) == 0);
    char Daten[32];
    überprüfen(datagrammDatenEmpfangen(endpunktWert, Daten, sizeof Daten, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    überprüfen(datagrammDatenSenden(endpunktWert, "posix-udp", 9, 0, (struct sockaddr *)&gegenstelleWert, sizeof gegenstelleWert) == 9);
    Länge = sizeof empfangenWertAdresse;
    überprüfen(recvfrom(endpunktWert, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    überprüfen(datagrammDatenEmpfangen(endpunktWert, Daten, sizeof Daten, 0, (struct sockaddr *)&empfangenWertAdresse, &Länge) == 9);
    überprüfen(memcmp(Daten, "posix-udp", 9) == 0 && Länge == 16);
    überprüfen(empfangenWertAdresse.sin_port == gegenstelleWert.sin_port && empfangenWertAdresse.sin_addr.s_addr == gegenstelleWert.sin_addr.s_addr);
    überprüfen(sendto(endpunktWert, "truncate", 8, 0, (struct sockaddr *)&gegenstelleWert, sizeof gegenstelleWert) == 8);
    überprüfen(recvfrom(endpunktWert, Daten, 3, 0, NULL, NULL) == 3 && memcmp(Daten, "tru", 3) == 0);
    überprüfen(recvfrom(endpunktWert, Daten, sizeof Daten, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    überprüfen(sendto(endpunktWert, NULL, 0, 0, (struct sockaddr *)&gegenstelleWert, sizeof gegenstelleWert) == 0);
    überprüfen(recvfrom(endpunktWert, NULL, 0, 0, NULL, NULL) == 0);
    überprüfen(recvfrom(endpunktWert, Daten, sizeof Daten, 0, NULL, NULL) == -1 && errno == EAGAIN);
    überprüfen(close(endpunktWert) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
