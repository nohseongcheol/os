/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <Netzadressumwandlung/Bytereihenfolge.h>
#include <errno.h>
#include <fcntl.h>
#include <Netzverbund/Adresse.h>
#include <Grunddefinitionen.h>
#include <System/socket.h>
#include <System/stat.h>
#include <System/Systemkennung.h>
#include <System/Kindwartung.h>
#include <unistd.h>
#include "shell_locale.h"

/* Adapted from koros4's request interpreter. Private names are localized
 * in each WorldOS edition; main and POSIX ABI names remain unchanged. */

enum { Eingabezeilenkapazität = 512, maximale_Argumentanzahl = 16, maximale_Skriptverschachtelung = 4 };
static int Skriptverschachtelungstiefe;
struct Eingabestrom {
    int Eingabedeskriptor;
    char Übertragungspuffer_2[256];
    size_t Position;
    size_t Länge;
};

static size_t Textlänge_in_Bytes(const char *Text)
{
    size_t Länge = 0;
    while (Text[Länge] != '\0')
        Länge++;
    return Länge;
}

static int Texte_gleich(const char *links, const char *rechts)
{
    size_t Position = 0;
    while (links[Position] == rechts[Position]) {
        if (links[Position] == '\0')
            return 1;
        Position++;
    }
    return 0;
}

static void Text_schreiben(const char *Text)
{
    size_t Länge = Textlänge_in_Bytes(Text);
    while (Länge > 0U) {
        ssize_t geschriebene_Byteanzahl = schreiben(STDOUT_FILENO, Text, Länge);
        if (geschriebene_Byteanzahl <= 0)
            return;
        Text += geschriebene_Byteanzahl;
        Länge -= (size_t)geschriebene_Byteanzahl;
    }
}

static void Ganzzahl_schreiben(int Wert)
{
    char Ziffernzeichen[16];
    unsigned int Ziffernanzahl;
    unsigned int vorzeichenloser_Betrag;

    if (Wert < 0) {
        Text_schreiben("-");
        vorzeichenloser_Betrag = (unsigned int)(-(Wert + 1)) + 1U;
    } else {
        vorzeichenloser_Betrag = (unsigned int)Wert;
    }
    Ziffernanzahl = 0;
    do {
        Ziffernzeichen[Ziffernanzahl++] = (char)('0' + vorzeichenloser_Betrag % 10U);
        vorzeichenloser_Betrag /= 10U;
    } while (vorzeichenloser_Betrag != 0U);
    while (Ziffernanzahl > 0U) {
        Ziffernanzahl--;
        (void)schreiben(STDOUT_FILENO, &Ziffernzeichen[Ziffernanzahl], 1);
    }
}

static void Fehler_melden(const char *Operation)
{
    Text_schreiben("error: ");
    Text_schreiben(Operation);
    Text_schreiben(" errno=");
    Ganzzahl_schreiben(errno);
    Text_schreiben("\n");
}

static int Eingabezeile_lesen(struct Eingabestrom *Eingabe, char *Eingabezeile, size_t Kapazität)
{
    size_t Position = 0;
    int ungültige_Eingabezeile = 0;
    char Zeichen;
    ssize_t gelesene_Bytes;
    if (Kapazität < 2U)
        return -2;
    for (;;) {
        if (Eingabe->Position == Eingabe->Länge) {
            gelesene_Bytes = lesen(Eingabe->Eingabedeskriptor, Eingabe->Übertragungspuffer_2, sizeof(Eingabe->Übertragungspuffer_2));
            if (gelesene_Bytes < 0) {
                if (errno == EINTR)
                    continue;
                return -1;
            }
            if (gelesene_Bytes == 0) {
                if (Position == 0 && !ungültige_Eingabezeile)
                    return -1;
                break;
            }
            Eingabe->Länge = (size_t)gelesene_Bytes;
            Eingabe->Position = 0;
        }
        Zeichen = Eingabe->Übertragungspuffer_2[Eingabe->Position++];
        if (Zeichen == '\n')
            break;
        if (Eingabe->Eingabedeskriptor == STDIN_FILENO && Zeichen == 4) {
            if (Position == 0 && !ungültige_Eingabezeile)
                return -1;
            break;
        }
        if (Eingabe->Eingabedeskriptor == STDIN_FILENO && (Zeichen == 8 || Zeichen == 127)) {
            if (Position > 0) {
                do {
                    Position--;
                } while (Position > 0 && ((unsigned char)Eingabezeile[Position] & 0xc0U) == 0x80U);
            }
            continue;
        }
        if (Zeichen == '\r')
            continue;
        if (Zeichen == '\0') {
            ungültige_Eingabezeile = 1; /* Reject binary input; do not execute its prefix. */
            continue;
        }
        if (Position + 1U < Kapazität)
            Eingabezeile[Position++] = Zeichen;
        else
            ungültige_Eingabezeile = 1;
    }
    Eingabezeile[Position] = '\0';
    return ungültige_Eingabezeile ? -2 : (int)Position;
}

static int Argumente_trennen(char *Eingabezeile, char **Argumente)
{
    int Argumentanzahl = 0;
    char *aktuelle_Position = Eingabezeile;
    char *Ausgabeposition = Eingabezeile;

    while (*aktuelle_Position != '\0') {
        char Anführungszeichen = '\0';
        while (*aktuelle_Position == ' ' || *aktuelle_Position == '\t')
            aktuelle_Position++;
        if (*aktuelle_Position == '\0' || *aktuelle_Position == '#')
            break;
        if (Argumentanzahl == maximale_Argumentanzahl - 1)
            return -1;
        Argumente[Argumentanzahl++] = Ausgabeposition;
        while (*aktuelle_Position != '\0') {
            char Zeichen = *aktuelle_Position++;
            if (Anführungszeichen == '\0' && (Zeichen == ' ' || Zeichen == '\t'))
                break;
            if (Zeichen == '\\' && Anführungszeichen != '\'') {
                if (*aktuelle_Position == '\0')
                    return -1;
                *Ausgabeposition++ = *aktuelle_Position++;
            } else if (Zeichen == '\'' || Zeichen == '"') {
                if (Anführungszeichen == '\0')
                    Anführungszeichen = Zeichen;
                else if (Anführungszeichen == Zeichen)
                    Anführungszeichen = '\0';
                else
                    *Ausgabeposition++ = Zeichen;
            } else {
                *Ausgabeposition++ = Zeichen;
            }
        }
        if (Anführungszeichen != '\0')
            return -1;
        *Ausgabeposition++ = '\0';
    }
    Argumente[Argumentanzahl] = (char *)0;
    return Argumentanzahl;
}

static void Hilfe_anzeigen(void)
{
    size_t Position;
    Text_schreiben(
        "WorldOS command interpreter commands:\n"
        "  help                 show this help\n"
        "  echo TEXT            print text\n"
        "  pwd                  show current directory\n"
        "  cd PATH              change directory\n"
        "  cat FILE             print a FAT file\n"
        "  stat FILE            show file size\n"
        "  pid                  show process identifiers\n"
        "  uname                show operating-system identity\n"
        "  run FILE [ARGS...]   execute a user ELF program\n"
        "  udp [TEXT]           call POSIX UDP and loop back TEXT\n"
        "  source FILE          interpret a UTF-8 command file\n"
        "  exit                 leave the shell\n");
    Text_schreiben("Native command proposals (ASCII aliases remain available):\n");
    for (Position = 0; Position < sizeof(Grundbefehle) / sizeof(Grundbefehle[0]); Position++) {
        Text_schreiben(lokale_Befehlsnamen[Position]);
        Text_schreiben(" = ");
        Text_schreiben(Grundbefehle[Position]);
        Text_schreiben("\n");
    }
}

static int Befehl_stimmt_überein(const char *Text, const char *Befehl)
{
    size_t Position;
    if (Texte_gleich(Text, Befehl))
        return 1;
    for (Position = 0; Position < sizeof(Grundbefehle) / sizeof(Grundbefehle[0]); Position++)
        if (Texte_gleich(Befehl, Grundbefehle[Position]))
            return Texte_gleich(Text, lokale_Befehlsnamen[Position]);
    return 0;
}

static int Eingabe_auswerten(int Eingabedeskriptor);

static int Befehlsdatei_auswerten(const char *Dateiname)
{
    int Dateideskriptor_2;
    int Status;
    if (Skriptverschachtelungstiefe >= maximale_Skriptverschachtelung) {
        Text_schreiben("source: nesting limit\n");
        return 0;
    }
    Dateideskriptor_2 = öffnen(Dateiname, O_RDONLY);
    if (Dateideskriptor_2 < 0) {
        Fehler_melden(Dateiname);
        return 0;
    }
    Skriptverschachtelungstiefe++;
    Status = Eingabe_auswerten(Dateideskriptor_2);
    Skriptverschachtelungstiefe--;
    (void)schließen(Dateideskriptor_2);
    return Status;
}

static void Argumente_ausgeben(int Argumentanzahl, char **Argumente)
{
    int Position;
    for (Position = 1; Position < Argumentanzahl; Position++) {
        if (Position != 1)
            Text_schreiben(" ");
        Text_schreiben(Argumente[Position]);
    }
    Text_schreiben("\n");
}

static void Arbeitsverzeichnis_anzeigen(void)
{
    char Pfad[128];
    if (Arbeitsverzeichnispfad_ermitteln(Pfad, sizeof(Pfad)) == (char *)0) {
        Fehler_melden("pwd");
        return;
    }
    Text_schreiben(Pfad);
    Text_schreiben("\n");
}

static void Dateiinhalt_anzeigen(const char *Dateiname)
{
    char Übertragungspuffer_2[128];
    int Dateideskriptor_2 = öffnen(Dateiname, O_RDONLY);
    ssize_t gelesene_Bytes;

    if (Dateideskriptor_2 < 0) {
        Fehler_melden("cat");
        return;
    }
    while ((gelesene_Bytes = lesen(Dateideskriptor_2, Übertragungspuffer_2, sizeof(Übertragungspuffer_2))) > 0)
        (void)schreiben(STDOUT_FILENO, Übertragungspuffer_2, (size_t)gelesene_Bytes);
    if (gelesene_Bytes < 0)
        Fehler_melden("cat/read");
    (void)schließen(Dateideskriptor_2);
    Text_schreiben("\n");
}

static void Dateiinformationen_anzeigen(const char *Dateiname)
{
    struct Dateizustand Status;
    if (Dateizustand(Dateiname, &Status) < 0) {
        Fehler_melden("stat");
        return;
    }
    Text_schreiben("size=");
    Ganzzahl_schreiben((int)Status.st_size);
    Text_schreiben(S_ISDIR(Status.st_mode) ? " type=directory\n" : " type=file\n");
}

static void Prozesskennungen_anzeigen(void)
{
    Text_schreiben("pid=");
    Ganzzahl_schreiben((int)Prozesskennung_ermitteln());
    Text_schreiben(" ppid=");
    Ganzzahl_schreiben((int)Elternprozesskennung_ermitteln());
    Text_schreiben("\n");
}

static void Systemkennung_anzeigen(void)
{
    struct utsname Systemidentität;
    if (Systeminformationen_ermitteln(&Systemidentität) < 0) {
        Fehler_melden("uname");
        return;
    }
    Text_schreiben(Systemidentität.sysname);
    Text_schreiben(" ");
    Text_schreiben(Systemidentität.release);
    Text_schreiben(" ");
    Text_schreiben(Systemidentität.machine);
    Text_schreiben("\n");
}

static void Programm_ausführen(int Argumentanzahl, char **Argumente)
{
    pid_t Kindprozesskennung;
    int Beendigungsstatus_des_Kindprozesses = 0;

    if (Argumentanzahl < 2) {
        Text_schreiben("usage: run FILE [ARGS...]\n");
        return;
    }
    Kindprozesskennung = Prozess_verzweigen();
    if (Kindprozesskennung < 0) {
        Fehler_melden("fork");
        return;
    }
    if (Kindprozesskennung == 0) {
        Programmbild_ersetzen(Argumente[1], &Argumente[1], (char *const *)0);
        Fehler_melden("execve");
        sofort_beenden(127);
    }
    if (bestimmtes_Kind_abwarten(Kindprozesskennung, &Beendigungsstatus_des_Kindprozesses, 0) < 0) {
        Fehler_melden("waitpid");
        return;
    }
    Text_schreiben("exit-status=");
    Ganzzahl_schreiben(WEXITSTATUS(Beendigungsstatus_des_Kindprozesses));
    Text_schreiben("\n");
}

static void Datagrammrücklauf_prüfen(const char *Nachricht)
{
    struct Netzverbundendpunktadresse Empfängeradresse = {0};
    struct Netzverbundendpunktadresse Absenderadresse = {0};
    Adresslängentyp Absenderadresslänge = sizeof(Absenderadresse);
    char empfangene_Daten[96];
    size_t Nachrichtenlänge_in_Bytes = Textlänge_in_Bytes(Nachricht);
    int Empfangssockel = -1;
    int Sendesockel = -1;
    ssize_t empfangene_Byteanzahl;

    if (Nachrichtenlänge_in_Bytes >= sizeof(empfangene_Daten)) {
        Text_schreiben("udp: message exceeds 95 bytes\n");
        return;
    }
    Empfangssockel = Kommunikationsendpunkt_anlegen(Netzverbundadressfamilienkennung, Datagrammendpunkt, Benutzerdatagrammprotokoll);
    Sendesockel = Kommunikationsendpunkt_anlegen(Netzverbundadressfamilienkennung, Datagrammendpunkt, Benutzerdatagrammprotokoll);
    if (Empfangssockel < 0 || Sendesockel < 0) {
        Fehler_melden("socket");
        goto Sockel_schließen;
    }
    Empfängeradresse.Netzverbundadressfamilie = Netzverbundadressfamilienkennung;
    Empfängeradresse.Kommunikationsportnummer = _16_Bit_in_Netzreihenfolge(40404);
    Empfängeradresse.Netzverbundadressinhalt.Adresswert = _32_Bit_in_Netzreihenfolge(Rückschleifenadresse);
    if (lokale_Adresse_zuordnen(Empfangssockel, (const struct Kommunikationsendpunktadresse *)&Empfängeradresse, sizeof(Empfängeradresse)) < 0) {
        Fehler_melden("bind");
        goto Sockel_schließen;
    }
    if (Gegenstelle_verbinden(Sendesockel, (const struct Kommunikationsendpunktadresse *)&Empfängeradresse, sizeof(Empfängeradresse)) < 0) {
        Fehler_melden("connect");
        goto Sockel_schließen;
    }
    if (senden(Sendesockel, Nachricht, Nachrichtenlänge_in_Bytes, 0) != (ssize_t)Nachrichtenlänge_in_Bytes) {
        Fehler_melden("send");
        goto Sockel_schließen;
    }
    empfangene_Byteanzahl = mit_Absenderadresse_empfangen(Empfangssockel, empfangene_Daten, sizeof(empfangene_Daten) - 1U, 0,
                         (struct Kommunikationsendpunktadresse *)&Absenderadresse, &Absenderadresslänge);
    if (empfangene_Byteanzahl < 0) {
        Fehler_melden("recvfrom");
        goto Sockel_schließen;
    }
    empfangene_Daten[empfangene_Byteanzahl] = '\0';
    Text_schreiben("udp-received: ");
    Text_schreiben(empfangene_Daten);
    Text_schreiben("\n");

Sockel_schließen:
    if (Sendesockel >= 0)
        (void)schließen(Sendesockel);
    if (Empfangssockel >= 0)
        (void)schließen(Empfangssockel);
}

static int Eingabe_auswerten(int Eingabedeskriptor)
{
    char Eingabezeile[Eingabezeilenkapazität];
    char *Argumente[maximale_Argumentanzahl];
    struct Eingabestrom Eingabe = {0};
    Eingabe.Eingabedeskriptor = Eingabedeskriptor;

    for (;;) {
        int Argumentanzahl;
        int Status;
        if (Eingabedeskriptor == STDIN_FILENO)
            Text_schreiben("worldos$ ");
        Status = Eingabezeile_lesen(&Eingabe, Eingabezeile, sizeof(Eingabezeile));
        if (Status == -1)
            return 0;
        if (Status == -2) {
            Text_schreiben("input rejected: overlong or binary line\n");
            continue;
        }
        Argumentanzahl = Argumente_trennen(Eingabezeile, Argumente);
        if (Argumentanzahl < 0) {
            Text_schreiben("syntax error: quote, escape or argument limit\n");
            continue;
        }
        if (Argumentanzahl == 0)
            continue;
        if (Befehl_stimmt_überein(Argumente[0], "help"))
            Hilfe_anzeigen();
        else if (Befehl_stimmt_überein(Argumente[0], "echo"))
            Argumente_ausgeben(Argumentanzahl, Argumente);
        else if (Befehl_stimmt_überein(Argumente[0], "pwd"))
            Arbeitsverzeichnis_anzeigen();
        else if (Befehl_stimmt_überein(Argumente[0], "cd")) {
            if (Argumentanzahl < 2)
                Text_schreiben("usage: cd PATH\n");
            else if (Arbeitsverzeichnis_wechseln(Argumente[1]) < 0)
                Fehler_melden("cd");
        } else if (Befehl_stimmt_überein(Argumente[0], "cat")) {
            if (Argumentanzahl < 2)
                Text_schreiben("usage: cat FILE\n");
            else
                Dateiinhalt_anzeigen(Argumente[1]);
        } else if (Befehl_stimmt_überein(Argumente[0], "stat")) {
            if (Argumentanzahl < 2)
                Text_schreiben("usage: stat FILE\n");
            else
                Dateiinformationen_anzeigen(Argumente[1]);
        } else if (Befehl_stimmt_überein(Argumente[0], "pid"))
            Prozesskennungen_anzeigen();
        else if (Befehl_stimmt_überein(Argumente[0], "uname"))
            Systemkennung_anzeigen();
        else if (Befehl_stimmt_überein(Argumente[0], "run"))
            Programm_ausführen(Argumentanzahl, Argumente);
        else if (Befehl_stimmt_überein(Argumente[0], "udp"))
            Datagrammrücklauf_prüfen(Argumentanzahl >= 2 ? Argumente[1] : "ping");
        else if (Befehl_stimmt_überein(Argumente[0], "source")) {
            if (Argumentanzahl < 2)
                Text_schreiben("usage: source FILE\n");
            else if (Befehlsdatei_auswerten(Argumente[1]))
                return 1;
        } else if (Befehl_stimmt_überein(Argumente[0], "exit"))
            return 1;
        else
            Text_schreiben("unknown command; type help\n");
    }
}

int main(void)
{
    Text_schreiben("WORLDOS-SHELL:READY\n");
    (void)Eingabe_auswerten(STDIN_FILENO);
    Text_schreiben("WORLDOS-SHELL:EXIT\n");
    return 0;
}
