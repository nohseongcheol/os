#include <Netzadressumwandlung/Bytereihenfolge.h>
#include <errno.h>
#include <System/socket.h>
#include <unistd.h>

static unsigned int length_of(const char *s)
{
    unsigned int n = 0;
    while (s[n] != 0) n++;
    return n;
}

static void say(const char *s) { (void)schreiben(STDOUT_FILENO, s, length_of(s)); }

static void report(const char *Systemidentität, int pass)
{
    say(pass ? "NTEST:PASS:" : "NTEST:FAIL:");
    say(Systemidentität);
    say("\n");
}

int main(void)
{
    struct Netzverbundendpunktadresse server_address = {0};
    struct Netzverbundendpunktadresse source = {0};
    Adresslängentyp source_length = sizeof(source);
    char Übertragungspuffer_2[8] = {0};
    int server = Kommunikationsendpunkt_anlegen(Netzverbundadressfamilienkennung, Datagrammendpunkt, Benutzerdatagrammprotokoll);
    int client = Kommunikationsendpunkt_anlegen(Netzverbundadressfamilienkennung, Datagrammendpunkt, 0);

    report("socket-server", server >= 3);
    report("socket-client", client >= 3 && client != server);
    server_address.Netzverbundadressfamilie = Netzverbundadressfamilienkennung;
    server_address.Kommunikationsportnummer = _16_Bit_in_Netzreihenfolge(32345);
    server_address.Netzverbundadressinhalt.Adresswert = _32_Bit_in_Netzreihenfolge(Rückschleifenadresse);
    report("bind", lokale_Adresse_zuordnen(server, (const struct Kommunikationsendpunktadresse *)&server_address,
                        sizeof(server_address)) == 0);
    report("connect", Gegenstelle_verbinden(client, (const struct Kommunikationsendpunktadresse *)&server_address,
                              sizeof(server_address)) == 0);
    report("send", senden(client, "ping", 4, 0) == 4);
    report("recvfrom", mit_Absenderadresse_empfangen(server, Übertragungspuffer_2, sizeof(Übertragungspuffer_2), 0,
                                (struct Kommunikationsendpunktadresse *)&source, &source_length) == 4 &&
                       Übertragungspuffer_2[0] == 'p' && Übertragungspuffer_2[3] == 'g' && source_length == 16);
    errno = 0;
    report("empty-eagain", empfangen(server, Übertragungspuffer_2, sizeof(Übertragungspuffer_2), 0) == -1 && errno == EAGAIN);
    report("getsockname", lokale_Endpunktadresse_ermitteln(server, (struct Kommunikationsendpunktadresse *)&source,
                                      &source_length) == 0 && source.Kommunikationsportnummer == _16_Bit_in_Netzreihenfolge(32345));
    errno = 0;
    report("udp-listen-not-supported", Verbindungsannahme_vorbereiten(server, 1) == -1 && errno == EOPNOTSUPP);
    report("close-client", schließen(client) == 0);
    report("close-server", schließen(server) == 0);
    say("NTEST:DONE\n");
    return 0;
}
