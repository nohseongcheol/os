/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <stddef.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/utsname.h>
#include <sys/wait.h>
#include <unistd.h>
#include "shell_locale.h"

/* Adapted from koros4's request interpreter. Private names are localized
 * in each WorldOS edition; main and POSIX ABI names remain unchanged. */

enum { capaciteit_van_invoerregel = 512, maximaal_aantal_argumenten = 16, maximale_opdrachtnesting = 4 };
static int diepte_van_opdrachtnesting;
struct invoerstroom {
    int invoerdescriptor;
    char overdrachtsbuffer_2[256];
    size_t positie;
    size_t lengte;
};

static size_t tekstlengte_in_bytes(const char *tekst)
{
    size_t lengte = 0;
    while (tekst[lengte] != '\0')
        lengte++;
    return lengte;
}

static int teksten_gelijk(const char *links, const char *rechts)
{
    size_t positie = 0;
    while (links[positie] == rechts[positie]) {
        if (links[positie] == '\0')
            return 1;
        positie++;
    }
    return 0;
}

static void tekst_schrijven(const char *tekst)
{
    size_t lengte = tekstlengte_in_bytes(tekst);
    while (lengte > 0U) {
        ssize_t aantal_geschreven_bytes = Schrijven(STDOUT_FILENO, tekst, lengte);
        if (aantal_geschreven_bytes <= 0)
            return;
        tekst += aantal_geschreven_bytes;
        lengte -= (size_t)aantal_geschreven_bytes;
    }
}

static void geheel_getal_schrijven(int waarde)
{
    char cijfertekens[16];
    unsigned int aantal_cijfers;
    unsigned int grootte_zonder_teken;

    if (waarde < 0) {
        tekst_schrijven("-");
        grootte_zonder_teken = (unsigned int)(-(waarde + 1)) + 1U;
    } else {
        grootte_zonder_teken = (unsigned int)waarde;
    }
    aantal_cijfers = 0;
    do {
        cijfertekens[aantal_cijfers++] = (char)('0' + grootte_zonder_teken % 10U);
        grootte_zonder_teken /= 10U;
    } while (grootte_zonder_teken != 0U);
    while (aantal_cijfers > 0U) {
        aantal_cijfers--;
        (void)Schrijven(STDOUT_FILENO, &cijfertekens[aantal_cijfers], 1);
    }
}

static void fout_melden(const char *bewerking)
{
    tekst_schrijven("error: ");
    tekst_schrijven(bewerking);
    tekst_schrijven(" errno=");
    geheel_getal_schrijven(errno);
    tekst_schrijven("\n");
}

static int invoerregel_lezen(struct invoerstroom *invoer, char *invoerregel, size_t capaciteit)
{
    size_t positie = 0;
    int ongeldige_invoerregel = 0;
    char teken;
    ssize_t gelezen_bytes;
    if (capaciteit < 2U)
        return -2;
    for (;;) {
        if (invoer->positie == invoer->lengte) {
            gelezen_bytes = Lezen(invoer->invoerdescriptor, invoer->overdrachtsbuffer_2, sizeof(invoer->overdrachtsbuffer_2));
            if (gelezen_bytes < 0) {
                if (errno == EINTR)
                    continue;
                return -1;
            }
            if (gelezen_bytes == 0) {
                if (positie == 0 && !ongeldige_invoerregel)
                    return -1;
                break;
            }
            invoer->lengte = (size_t)gelezen_bytes;
            invoer->positie = 0;
        }
        teken = invoer->overdrachtsbuffer_2[invoer->positie++];
        if (teken == '\n')
            break;
        if (invoer->invoerdescriptor == STDIN_FILENO && teken == 4) {
            if (positie == 0 && !ongeldige_invoerregel)
                return -1;
            break;
        }
        if (invoer->invoerdescriptor == STDIN_FILENO && (teken == 8 || teken == 127)) {
            if (positie > 0) {
                do {
                    positie--;
                } while (positie > 0 && ((unsigned char)invoerregel[positie] & 0xc0U) == 0x80U);
            }
            continue;
        }
        if (teken == '\r')
            continue;
        if (teken == '\0') {
            ongeldige_invoerregel = 1; /* Reject binary input; do not execute its prefix. */
            continue;
        }
        if (positie + 1U < capaciteit)
            invoerregel[positie++] = teken;
        else
            ongeldige_invoerregel = 1;
    }
    invoerregel[positie] = '\0';
    return ongeldige_invoerregel ? -2 : (int)positie;
}

static int argumenten_scheiden(char *invoerregel, char **argumenten)
{
    int aantal_argumenten = 0;
    char *huidige_positie = invoerregel;
    char *uitvoerpositie = invoerregel;

    while (*huidige_positie != '\0') {
        char aanhalingsteken = '\0';
        while (*huidige_positie == ' ' || *huidige_positie == '\t')
            huidige_positie++;
        if (*huidige_positie == '\0' || *huidige_positie == '#')
            break;
        if (aantal_argumenten == maximaal_aantal_argumenten - 1)
            return -1;
        argumenten[aantal_argumenten++] = uitvoerpositie;
        while (*huidige_positie != '\0') {
            char teken = *huidige_positie++;
            if (aanhalingsteken == '\0' && (teken == ' ' || teken == '\t'))
                break;
            if (teken == '\\' && aanhalingsteken != '\'') {
                if (*huidige_positie == '\0')
                    return -1;
                *uitvoerpositie++ = *huidige_positie++;
            } else if (teken == '\'' || teken == '"') {
                if (aanhalingsteken == '\0')
                    aanhalingsteken = teken;
                else if (aanhalingsteken == teken)
                    aanhalingsteken = '\0';
                else
                    *uitvoerpositie++ = teken;
            } else {
                *uitvoerpositie++ = teken;
            }
        }
        if (aanhalingsteken != '\0')
            return -1;
        *uitvoerpositie++ = '\0';
    }
    argumenten[aantal_argumenten] = (char *)0;
    return aantal_argumenten;
}

static void hulp_tonen(void)
{
    size_t positie;
    tekst_schrijven(
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
    tekst_schrijven("Native command proposals (ASCII aliases remain available):\n");
    for (positie = 0; positie < sizeof(basisopdrachten) / sizeof(basisopdrachten[0]); positie++) {
        tekst_schrijven(lokale_opdrachtnamen[positie]);
        tekst_schrijven(" = ");
        tekst_schrijven(basisopdrachten[positie]);
        tekst_schrijven("\n");
    }
}

static int opdracht_komt_overeen(const char *tekst, const char *opdracht)
{
    size_t positie;
    if (teksten_gelijk(tekst, opdracht))
        return 1;
    for (positie = 0; positie < sizeof(basisopdrachten) / sizeof(basisopdrachten[0]); positie++)
        if (teksten_gelijk(opdracht, basisopdrachten[positie]))
            return teksten_gelijk(tekst, lokale_opdrachtnamen[positie]);
    return 0;
}

static int invoer_vertolken(int invoerdescriptor);

static int opdrachtbestand_vertolken(const char *bestandsnaam)
{
    int bestandsdescriptor_2;
    int toestand;
    if (diepte_van_opdrachtnesting >= maximale_opdrachtnesting) {
        tekst_schrijven("source: nesting limit\n");
        return 0;
    }
    bestandsdescriptor_2 = Openen(bestandsnaam, O_RDONLY);
    if (bestandsdescriptor_2 < 0) {
        fout_melden(bestandsnaam);
        return 0;
    }
    diepte_van_opdrachtnesting++;
    toestand = invoer_vertolken(bestandsdescriptor_2);
    diepte_van_opdrachtnesting--;
    (void)Sluiten(bestandsdescriptor_2);
    return toestand;
}

static void argumenten_tonen(int aantal_argumenten, char **argumenten)
{
    int positie;
    for (positie = 1; positie < aantal_argumenten; positie++) {
        if (positie != 1)
            tekst_schrijven(" ");
        tekst_schrijven(argumenten[positie]);
    }
    tekst_schrijven("\n");
}

static void werkmap_tonen(void)
{
    char pad[128];
    if (getcwd(pad, sizeof(pad)) == (char *)0) {
        fout_melden("pwd");
        return;
    }
    tekst_schrijven(pad);
    tekst_schrijven("\n");
}

static void bestandsinhoud_tonen(const char *bestandsnaam)
{
    char overdrachtsbuffer_2[128];
    int bestandsdescriptor_2 = Openen(bestandsnaam, O_RDONLY);
    ssize_t gelezen_bytes;

    if (bestandsdescriptor_2 < 0) {
        fout_melden("cat");
        return;
    }
    while ((gelezen_bytes = Lezen(bestandsdescriptor_2, overdrachtsbuffer_2, sizeof(overdrachtsbuffer_2))) > 0)
        (void)Schrijven(STDOUT_FILENO, overdrachtsbuffer_2, (size_t)gelezen_bytes);
    if (gelezen_bytes < 0)
        fout_melden("cat/read");
    (void)Sluiten(bestandsdescriptor_2);
    tekst_schrijven("\n");
}

static void bestandsinformatie_tonen(const char *bestandsnaam)
{
    struct stat toestand;
    if (stat(bestandsnaam, &toestand) < 0) {
        fout_melden("stat");
        return;
    }
    tekst_schrijven("size=");
    geheel_getal_schrijven((int)toestand.st_size);
    tekst_schrijven(S_ISDIR(toestand.st_mode) ? " type=directory\n" : " type=file\n");
}

static void procesnummers_tonen(void)
{
    tekst_schrijven("pid=");
    geheel_getal_schrijven((int)getpid());
    tekst_schrijven(" ppid=");
    geheel_getal_schrijven((int)getppid());
    tekst_schrijven("\n");
}

static void systeemidentiteit_tonen(void)
{
    struct utsname systeemidentiteit;
    if (uname(&systeemidentiteit) < 0) {
        fout_melden("uname");
        return;
    }
    tekst_schrijven(systeemidentiteit.sysname);
    tekst_schrijven(" ");
    tekst_schrijven(systeemidentiteit.release);
    tekst_schrijven(" ");
    tekst_schrijven(systeemidentiteit.machine);
    tekst_schrijven("\n");
}

static void programma_uitvoeren(int aantal_argumenten, char **argumenten)
{
    pid_t nummer_van_kindproces;
    int eindstatus_van_kindproces = 0;

    if (aantal_argumenten < 2) {
        tekst_schrijven("usage: run FILE [ARGS...]\n");
        return;
    }
    nummer_van_kindproces = fork();
    if (nummer_van_kindproces < 0) {
        fout_melden("fork");
        return;
    }
    if (nummer_van_kindproces == 0) {
        execve(argumenten[1], &argumenten[1], (char *const *)0);
        fout_melden("execve");
        _exit(127);
    }
    if (waitpid(nummer_van_kindproces, &eindstatus_van_kindproces, 0) < 0) {
        fout_melden("waitpid");
        return;
    }
    tekst_schrijven("exit-status=");
    geheel_getal_schrijven(WEXITSTATUS(eindstatus_van_kindproces));
    tekst_schrijven("\n");
}

static void terugkeer_van_datagram_testen(const char *bericht)
{
    struct sockaddr_in ontvangstadres = {0};
    struct sockaddr_in afzenderadres = {0};
    socklen_t lengte_van_afzenderadres = sizeof(afzenderadres);
    char ontvangen_gegevens[96];
    size_t berichtlengte_in_bytes = tekstlengte_in_bytes(bericht);
    int ontvangend_communicatiepunt = -1;
    int verzendend_communicatiepunt = -1;
    ssize_t aantal_ontvangen_bytes;

    if (berichtlengte_in_bytes >= sizeof(ontvangen_gegevens)) {
        tekst_schrijven("udp: message exceeds 95 bytes\n");
        return;
    }
    ontvangend_communicatiepunt = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    verzendend_communicatiepunt = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (ontvangend_communicatiepunt < 0 || verzendend_communicatiepunt < 0) {
        fout_melden("socket");
        goto communicatiepunten_sluiten;
    }
    ontvangstadres.sin_family = AF_INET;
    ontvangstadres.sin_port = htons(40404);
    ontvangstadres.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    if (bind(ontvangend_communicatiepunt, (const struct sockaddr *)&ontvangstadres, sizeof(ontvangstadres)) < 0) {
        fout_melden("bind");
        goto communicatiepunten_sluiten;
    }
    if (connect(verzendend_communicatiepunt, (const struct sockaddr *)&ontvangstadres, sizeof(ontvangstadres)) < 0) {
        fout_melden("connect");
        goto communicatiepunten_sluiten;
    }
    if (send(verzendend_communicatiepunt, bericht, berichtlengte_in_bytes, 0) != (ssize_t)berichtlengte_in_bytes) {
        fout_melden("send");
        goto communicatiepunten_sluiten;
    }
    aantal_ontvangen_bytes = recvfrom(ontvangend_communicatiepunt, ontvangen_gegevens, sizeof(ontvangen_gegevens) - 1U, 0,
                         (struct sockaddr *)&afzenderadres, &lengte_van_afzenderadres);
    if (aantal_ontvangen_bytes < 0) {
        fout_melden("recvfrom");
        goto communicatiepunten_sluiten;
    }
    ontvangen_gegevens[aantal_ontvangen_bytes] = '\0';
    tekst_schrijven("udp-received: ");
    tekst_schrijven(ontvangen_gegevens);
    tekst_schrijven("\n");

communicatiepunten_sluiten:
    if (verzendend_communicatiepunt >= 0)
        (void)Sluiten(verzendend_communicatiepunt);
    if (ontvangend_communicatiepunt >= 0)
        (void)Sluiten(ontvangend_communicatiepunt);
}

static int invoer_vertolken(int invoerdescriptor)
{
    char invoerregel[capaciteit_van_invoerregel];
    char *argumenten[maximaal_aantal_argumenten];
    struct invoerstroom invoer = {0};
    invoer.invoerdescriptor = invoerdescriptor;

    for (;;) {
        int aantal_argumenten;
        int toestand;
        if (invoerdescriptor == STDIN_FILENO)
            tekst_schrijven("worldos$ ");
        toestand = invoerregel_lezen(&invoer, invoerregel, sizeof(invoerregel));
        if (toestand == -1)
            return 0;
        if (toestand == -2) {
            tekst_schrijven("input rejected: overlong or binary line\n");
            continue;
        }
        aantal_argumenten = argumenten_scheiden(invoerregel, argumenten);
        if (aantal_argumenten < 0) {
            tekst_schrijven("syntax error: quote, escape or argument limit\n");
            continue;
        }
        if (aantal_argumenten == 0)
            continue;
        if (opdracht_komt_overeen(argumenten[0], "help"))
            hulp_tonen();
        else if (opdracht_komt_overeen(argumenten[0], "echo"))
            argumenten_tonen(aantal_argumenten, argumenten);
        else if (opdracht_komt_overeen(argumenten[0], "pwd"))
            werkmap_tonen();
        else if (opdracht_komt_overeen(argumenten[0], "cd")) {
            if (aantal_argumenten < 2)
                tekst_schrijven("usage: cd PATH\n");
            else if (chdir(argumenten[1]) < 0)
                fout_melden("cd");
        } else if (opdracht_komt_overeen(argumenten[0], "cat")) {
            if (aantal_argumenten < 2)
                tekst_schrijven("usage: cat FILE\n");
            else
                bestandsinhoud_tonen(argumenten[1]);
        } else if (opdracht_komt_overeen(argumenten[0], "stat")) {
            if (aantal_argumenten < 2)
                tekst_schrijven("usage: stat FILE\n");
            else
                bestandsinformatie_tonen(argumenten[1]);
        } else if (opdracht_komt_overeen(argumenten[0], "pid"))
            procesnummers_tonen();
        else if (opdracht_komt_overeen(argumenten[0], "uname"))
            systeemidentiteit_tonen();
        else if (opdracht_komt_overeen(argumenten[0], "run"))
            programma_uitvoeren(aantal_argumenten, argumenten);
        else if (opdracht_komt_overeen(argumenten[0], "udp"))
            terugkeer_van_datagram_testen(aantal_argumenten >= 2 ? argumenten[1] : "ping");
        else if (opdracht_komt_overeen(argumenten[0], "source")) {
            if (aantal_argumenten < 2)
                tekst_schrijven("usage: source FILE\n");
            else if (opdrachtbestand_vertolken(argumenten[1]))
                return 1;
        } else if (opdracht_komt_overeen(argumenten[0], "exit"))
            return 1;
        else
            tekst_schrijven("unknown command; type help\n");
    }
}

int main(void)
{
    tekst_schrijven("WORLDOS-SHELL:READY\n");
    (void)invoer_vertolken(STDIN_FILENO);
    tekst_schrijven("WORLDOS-SHELL:EXIT\n");
    return 0;
}
