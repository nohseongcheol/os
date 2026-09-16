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

enum { syöterivin_kapasiteetti = 512, argumenttien_enimmäismäärä = 16, komentotiedostojen_enimmäissisäkkäisyys = 4 };
static int komentotiedostojen_sisäkkäisyyssyvyys;
struct syötevirta {
    int syötekuvaaja;
    char siirtopuskuri_2[256];
    size_t paikka;
    size_t pituus;
};

static size_t tekstin_pituus_tavuina(const char *teksti)
{
    size_t pituus = 0;
    while (teksti[pituus] != '\0')
        pituus++;
    return pituus;
}

static int tekstit_samat(const char *vasen, const char *oikea)
{
    size_t paikka = 0;
    while (vasen[paikka] == oikea[paikka]) {
        if (vasen[paikka] == '\0')
            return 1;
        paikka++;
    }
    return 0;
}

static void kirjoita_teksti(const char *teksti)
{
    size_t pituus = tekstin_pituus_tavuina(teksti);
    while (pituus > 0U) {
        ssize_t kirjoitettujen_tavujen_määrä = Kirjoitus(STDOUT_FILENO, teksti, pituus);
        if (kirjoitettujen_tavujen_määrä <= 0)
            return;
        teksti += kirjoitettujen_tavujen_määrä;
        pituus -= (size_t)kirjoitettujen_tavujen_määrä;
    }
}

static void kirjoita_kokonaisluku(int arvo)
{
    char numeromerkit[16];
    unsigned int numeroiden_määrä;
    unsigned int etumerkitön_suuruus;

    if (arvo < 0) {
        kirjoita_teksti("-");
        etumerkitön_suuruus = (unsigned int)(-(arvo + 1)) + 1U;
    } else {
        etumerkitön_suuruus = (unsigned int)arvo;
    }
    numeroiden_määrä = 0;
    do {
        numeromerkit[numeroiden_määrä++] = (char)('0' + etumerkitön_suuruus % 10U);
        etumerkitön_suuruus /= 10U;
    } while (etumerkitön_suuruus != 0U);
    while (numeroiden_määrä > 0U) {
        numeroiden_määrä--;
        (void)Kirjoitus(STDOUT_FILENO, &numeromerkit[numeroiden_määrä], 1);
    }
}

static void ilmoita_virhe(const char *toiminto)
{
    kirjoita_teksti("error: ");
    kirjoita_teksti(toiminto);
    kirjoita_teksti(" errno=");
    kirjoita_kokonaisluku(errno);
    kirjoita_teksti("\n");
}

static int lue_syöterivi(struct syötevirta *syöte, char *syöterivi, size_t kapasiteetti)
{
    size_t paikka = 0;
    int virheellinen_syöterivi = 0;
    char merkki;
    ssize_t luetut_tavut;
    if (kapasiteetti < 2U)
        return -2;
    for (;;) {
        if (syöte->paikka == syöte->pituus) {
            luetut_tavut = Luku(syöte->syötekuvaaja, syöte->siirtopuskuri_2, sizeof(syöte->siirtopuskuri_2));
            if (luetut_tavut < 0) {
                if (errno == EINTR)
                    continue;
                return -1;
            }
            if (luetut_tavut == 0) {
                if (paikka == 0 && !virheellinen_syöterivi)
                    return -1;
                break;
            }
            syöte->pituus = (size_t)luetut_tavut;
            syöte->paikka = 0;
        }
        merkki = syöte->siirtopuskuri_2[syöte->paikka++];
        if (merkki == '\n')
            break;
        if (syöte->syötekuvaaja == STDIN_FILENO && merkki == 4) {
            if (paikka == 0 && !virheellinen_syöterivi)
                return -1;
            break;
        }
        if (syöte->syötekuvaaja == STDIN_FILENO && (merkki == 8 || merkki == 127)) {
            if (paikka > 0) {
                do {
                    paikka--;
                } while (paikka > 0 && ((unsigned char)syöterivi[paikka] & 0xc0U) == 0x80U);
            }
            continue;
        }
        if (merkki == '\r')
            continue;
        if (merkki == '\0') {
            virheellinen_syöterivi = 1; /* Reject binary input; do not execute its prefix. */
            continue;
        }
        if (paikka + 1U < kapasiteetti)
            syöterivi[paikka++] = merkki;
        else
            virheellinen_syöterivi = 1;
    }
    syöterivi[paikka] = '\0';
    return virheellinen_syöterivi ? -2 : (int)paikka;
}

static int erota_argumentit(char *syöterivi, char **argumentit)
{
    int argumenttien_määrä = 0;
    char *nykyinen_paikka = syöterivi;
    char *tulostuspaikka = syöterivi;

    while (*nykyinen_paikka != '\0') {
        char lainausmerkki = '\0';
        while (*nykyinen_paikka == ' ' || *nykyinen_paikka == '\t')
            nykyinen_paikka++;
        if (*nykyinen_paikka == '\0' || *nykyinen_paikka == '#')
            break;
        if (argumenttien_määrä == argumenttien_enimmäismäärä - 1)
            return -1;
        argumentit[argumenttien_määrä++] = tulostuspaikka;
        while (*nykyinen_paikka != '\0') {
            char merkki = *nykyinen_paikka++;
            if (lainausmerkki == '\0' && (merkki == ' ' || merkki == '\t'))
                break;
            if (merkki == '\\' && lainausmerkki != '\'') {
                if (*nykyinen_paikka == '\0')
                    return -1;
                *tulostuspaikka++ = *nykyinen_paikka++;
            } else if (merkki == '\'' || merkki == '"') {
                if (lainausmerkki == '\0')
                    lainausmerkki = merkki;
                else if (lainausmerkki == merkki)
                    lainausmerkki = '\0';
                else
                    *tulostuspaikka++ = merkki;
            } else {
                *tulostuspaikka++ = merkki;
            }
        }
        if (lainausmerkki != '\0')
            return -1;
        *tulostuspaikka++ = '\0';
    }
    argumentit[argumenttien_määrä] = (char *)0;
    return argumenttien_määrä;
}

static void näytä_ohje(void)
{
    size_t paikka;
    kirjoita_teksti(
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
    kirjoita_teksti("Native command proposals (ASCII aliases remain available):\n");
    for (paikka = 0; paikka < sizeof(peruskomennot) / sizeof(peruskomennot[0]); paikka++) {
        kirjoita_teksti(paikalliset_komentonimet[paikka]);
        kirjoita_teksti(" = ");
        kirjoita_teksti(peruskomennot[paikka]);
        kirjoita_teksti("\n");
    }
}

static int komento_täsmää(const char *teksti, const char *komento)
{
    size_t paikka;
    if (tekstit_samat(teksti, komento))
        return 1;
    for (paikka = 0; paikka < sizeof(peruskomennot) / sizeof(peruskomennot[0]); paikka++)
        if (tekstit_samat(komento, peruskomennot[paikka]))
            return tekstit_samat(teksti, paikalliset_komentonimet[paikka]);
    return 0;
}

static int tulkitse_syöte(int syötekuvaaja);

static int tulkitse_komentotiedosto(const char *tiedoston_nimi)
{
    int tiedostokuvaaja_2;
    int tila;
    if (komentotiedostojen_sisäkkäisyyssyvyys >= komentotiedostojen_enimmäissisäkkäisyys) {
        kirjoita_teksti("source: nesting limit\n");
        return 0;
    }
    tiedostokuvaaja_2 = Avaa(tiedoston_nimi, O_RDONLY);
    if (tiedostokuvaaja_2 < 0) {
        ilmoita_virhe(tiedoston_nimi);
        return 0;
    }
    komentotiedostojen_sisäkkäisyyssyvyys++;
    tila = tulkitse_syöte(tiedostokuvaaja_2);
    komentotiedostojen_sisäkkäisyyssyvyys--;
    (void)Sulje(tiedostokuvaaja_2);
    return tila;
}

static void näytä_argumentit(int argumenttien_määrä, char **argumentit)
{
    int paikka;
    for (paikka = 1; paikka < argumenttien_määrä; paikka++) {
        if (paikka != 1)
            kirjoita_teksti(" ");
        kirjoita_teksti(argumentit[paikka]);
    }
    kirjoita_teksti("\n");
}

static void näytä_työhakemisto(void)
{
    char polku[128];
    if (getcwd(polku, sizeof(polku)) == (char *)0) {
        ilmoita_virhe("pwd");
        return;
    }
    kirjoita_teksti(polku);
    kirjoita_teksti("\n");
}

static void näytä_tiedoston_sisältö(const char *tiedoston_nimi)
{
    char siirtopuskuri_2[128];
    int tiedostokuvaaja_2 = Avaa(tiedoston_nimi, O_RDONLY);
    ssize_t luetut_tavut;

    if (tiedostokuvaaja_2 < 0) {
        ilmoita_virhe("cat");
        return;
    }
    while ((luetut_tavut = Luku(tiedostokuvaaja_2, siirtopuskuri_2, sizeof(siirtopuskuri_2))) > 0)
        (void)Kirjoitus(STDOUT_FILENO, siirtopuskuri_2, (size_t)luetut_tavut);
    if (luetut_tavut < 0)
        ilmoita_virhe("cat/read");
    (void)Sulje(tiedostokuvaaja_2);
    kirjoita_teksti("\n");
}

static void näytä_tiedoston_tiedot(const char *tiedoston_nimi)
{
    struct stat tila;
    if (stat(tiedoston_nimi, &tila) < 0) {
        ilmoita_virhe("stat");
        return;
    }
    kirjoita_teksti("size=");
    kirjoita_kokonaisluku((int)tila.st_size);
    kirjoita_teksti(S_ISDIR(tila.st_mode) ? " type=directory\n" : " type=file\n");
}

static void näytä_prosessitunnukset(void)
{
    kirjoita_teksti("pid=");
    kirjoita_kokonaisluku((int)getpid());
    kirjoita_teksti(" ppid=");
    kirjoita_kokonaisluku((int)getppid());
    kirjoita_teksti("\n");
}

static void näytä_järjestelmätiedot(void)
{
    struct utsname järjestelmätiedot;
    if (uname(&järjestelmätiedot) < 0) {
        ilmoita_virhe("uname");
        return;
    }
    kirjoita_teksti(järjestelmätiedot.sysname);
    kirjoita_teksti(" ");
    kirjoita_teksti(järjestelmätiedot.release);
    kirjoita_teksti(" ");
    kirjoita_teksti(järjestelmätiedot.machine);
    kirjoita_teksti("\n");
}

static void suorita_ohjelma(int argumenttien_määrä, char **argumentit)
{
    pid_t lapsiprosessin_tunnus;
    int lapsiprosessin_päättymistila = 0;

    if (argumenttien_määrä < 2) {
        kirjoita_teksti("usage: run FILE [ARGS...]\n");
        return;
    }
    lapsiprosessin_tunnus = fork();
    if (lapsiprosessin_tunnus < 0) {
        ilmoita_virhe("fork");
        return;
    }
    if (lapsiprosessin_tunnus == 0) {
        execve(argumentit[1], &argumentit[1], (char *const *)0);
        ilmoita_virhe("execve");
        _exit(127);
    }
    if (waitpid(lapsiprosessin_tunnus, &lapsiprosessin_päättymistila, 0) < 0) {
        ilmoita_virhe("waitpid");
        return;
    }
    kirjoita_teksti("exit-status=");
    kirjoita_kokonaisluku(WEXITSTATUS(lapsiprosessin_päättymistila));
    kirjoita_teksti("\n");
}

static void testaa_tietosähkeen_palautus(const char *viesti)
{
    struct sockaddr_in vastaanottajan_osoite = {0};
    struct sockaddr_in lähettäjän_osoite = {0};
    socklen_t lähettäjän_osoitteen_pituus = sizeof(lähettäjän_osoite);
    char vastaanotetut_tiedot[96];
    size_t viestin_pituus_tavuina = tekstin_pituus_tavuina(viesti);
    int vastaanottava_yhteyspiste = -1;
    int lähettävä_yhteyspiste = -1;
    ssize_t vastaanotettujen_tavujen_määrä;

    if (viestin_pituus_tavuina >= sizeof(vastaanotetut_tiedot)) {
        kirjoita_teksti("udp: message exceeds 95 bytes\n");
        return;
    }
    vastaanottava_yhteyspiste = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    lähettävä_yhteyspiste = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (vastaanottava_yhteyspiste < 0 || lähettävä_yhteyspiste < 0) {
        ilmoita_virhe("socket");
        goto sulje_yhteyspisteet;
    }
    vastaanottajan_osoite.sin_family = AF_INET;
    vastaanottajan_osoite.sin_port = htons(40404);
    vastaanottajan_osoite.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    if (bind(vastaanottava_yhteyspiste, (const struct sockaddr *)&vastaanottajan_osoite, sizeof(vastaanottajan_osoite)) < 0) {
        ilmoita_virhe("bind");
        goto sulje_yhteyspisteet;
    }
    if (connect(lähettävä_yhteyspiste, (const struct sockaddr *)&vastaanottajan_osoite, sizeof(vastaanottajan_osoite)) < 0) {
        ilmoita_virhe("connect");
        goto sulje_yhteyspisteet;
    }
    if (send(lähettävä_yhteyspiste, viesti, viestin_pituus_tavuina, 0) != (ssize_t)viestin_pituus_tavuina) {
        ilmoita_virhe("send");
        goto sulje_yhteyspisteet;
    }
    vastaanotettujen_tavujen_määrä = recvfrom(vastaanottava_yhteyspiste, vastaanotetut_tiedot, sizeof(vastaanotetut_tiedot) - 1U, 0,
                         (struct sockaddr *)&lähettäjän_osoite, &lähettäjän_osoitteen_pituus);
    if (vastaanotettujen_tavujen_määrä < 0) {
        ilmoita_virhe("recvfrom");
        goto sulje_yhteyspisteet;
    }
    vastaanotetut_tiedot[vastaanotettujen_tavujen_määrä] = '\0';
    kirjoita_teksti("udp-received: ");
    kirjoita_teksti(vastaanotetut_tiedot);
    kirjoita_teksti("\n");

sulje_yhteyspisteet:
    if (lähettävä_yhteyspiste >= 0)
        (void)Sulje(lähettävä_yhteyspiste);
    if (vastaanottava_yhteyspiste >= 0)
        (void)Sulje(vastaanottava_yhteyspiste);
}

static int tulkitse_syöte(int syötekuvaaja)
{
    char syöterivi[syöterivin_kapasiteetti];
    char *argumentit[argumenttien_enimmäismäärä];
    struct syötevirta syöte = {0};
    syöte.syötekuvaaja = syötekuvaaja;

    for (;;) {
        int argumenttien_määrä;
        int tila;
        if (syötekuvaaja == STDIN_FILENO)
            kirjoita_teksti("worldos$ ");
        tila = lue_syöterivi(&syöte, syöterivi, sizeof(syöterivi));
        if (tila == -1)
            return 0;
        if (tila == -2) {
            kirjoita_teksti("input rejected: overlong or binary line\n");
            continue;
        }
        argumenttien_määrä = erota_argumentit(syöterivi, argumentit);
        if (argumenttien_määrä < 0) {
            kirjoita_teksti("syntax error: quote, escape or argument limit\n");
            continue;
        }
        if (argumenttien_määrä == 0)
            continue;
        if (komento_täsmää(argumentit[0], "help"))
            näytä_ohje();
        else if (komento_täsmää(argumentit[0], "echo"))
            näytä_argumentit(argumenttien_määrä, argumentit);
        else if (komento_täsmää(argumentit[0], "pwd"))
            näytä_työhakemisto();
        else if (komento_täsmää(argumentit[0], "cd")) {
            if (argumenttien_määrä < 2)
                kirjoita_teksti("usage: cd PATH\n");
            else if (chdir(argumentit[1]) < 0)
                ilmoita_virhe("cd");
        } else if (komento_täsmää(argumentit[0], "cat")) {
            if (argumenttien_määrä < 2)
                kirjoita_teksti("usage: cat FILE\n");
            else
                näytä_tiedoston_sisältö(argumentit[1]);
        } else if (komento_täsmää(argumentit[0], "stat")) {
            if (argumenttien_määrä < 2)
                kirjoita_teksti("usage: stat FILE\n");
            else
                näytä_tiedoston_tiedot(argumentit[1]);
        } else if (komento_täsmää(argumentit[0], "pid"))
            näytä_prosessitunnukset();
        else if (komento_täsmää(argumentit[0], "uname"))
            näytä_järjestelmätiedot();
        else if (komento_täsmää(argumentit[0], "run"))
            suorita_ohjelma(argumenttien_määrä, argumentit);
        else if (komento_täsmää(argumentit[0], "udp"))
            testaa_tietosähkeen_palautus(argumenttien_määrä >= 2 ? argumentit[1] : "ping");
        else if (komento_täsmää(argumentit[0], "source")) {
            if (argumenttien_määrä < 2)
                kirjoita_teksti("usage: source FILE\n");
            else if (tulkitse_komentotiedosto(argumentit[1]))
                return 1;
        } else if (komento_täsmää(argumentit[0], "exit"))
            return 1;
        else
            kirjoita_teksti("unknown command; type help\n");
    }
}

int main(void)
{
    kirjoita_teksti("WORLDOS-SHELL:READY\n");
    (void)tulkitse_syöte(STDIN_FILENO);
    kirjoita_teksti("WORLDOS-SHELL:EXIT\n");
    return 0;
}
