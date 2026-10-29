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

enum { kapacita_vstupního_řádku = 512, maximální_počet_argumentů = 16, maximální_vnoření_příkazových_souborů = 4 };
static int hloubka_vnoření_příkazových_souborů;
struct vstupní_proud {
    int vstupní_deskriptor;
    char vyrovnávací_paměť_přenosu_2[256];
    size_t pozice;
    size_t délka;
};

static size_t délka_textu_v_bajtech(const char *text)
{
    size_t délka = 0;
    while (text[délka] != '\0')
        délka++;
    return délka;
}

static int texty_stejné(const char *levý, const char *pravý)
{
    size_t pozice = 0;
    while (levý[pozice] == pravý[pozice]) {
        if (levý[pozice] == '\0')
            return 1;
        pozice++;
    }
    return 0;
}

static void vypsat_text(const char *text)
{
    size_t délka = délka_textu_v_bajtech(text);
    while (délka > 0U) {
        ssize_t počet_zapsaných_bajtů = Zápis(STDOUT_FILENO, text, délka);
        if (počet_zapsaných_bajtů <= 0)
            return;
        text += počet_zapsaných_bajtů;
        délka -= (size_t)počet_zapsaných_bajtů;
    }
}

static void vypsat_celé_číslo(int hodnota)
{
    char znaky_číslic[16];
    unsigned int počet_číslic;
    unsigned int velikost_bez_znaménka;

    if (hodnota < 0) {
        vypsat_text("-");
        velikost_bez_znaménka = (unsigned int)(-(hodnota + 1)) + 1U;
    } else {
        velikost_bez_znaménka = (unsigned int)hodnota;
    }
    počet_číslic = 0;
    do {
        znaky_číslic[počet_číslic++] = (char)('0' + velikost_bez_znaménka % 10U);
        velikost_bez_znaménka /= 10U;
    } while (velikost_bez_znaménka != 0U);
    while (počet_číslic > 0U) {
        počet_číslic--;
        (void)Zápis(STDOUT_FILENO, &znaky_číslic[počet_číslic], 1);
    }
}

static void ohlásit_chybu(const char *operace)
{
    vypsat_text("error: ");
    vypsat_text(operace);
    vypsat_text(" errno=");
    vypsat_celé_číslo(errno);
    vypsat_text("\n");
}

static int číst_vstupní_řádek(struct vstupní_proud *vstup, char *vstupní_řádek, size_t kapacita)
{
    size_t pozice = 0;
    int neplatný_vstupní_řádek = 0;
    char znak;
    ssize_t přečtené_bajty;
    if (kapacita < 2U)
        return -2;
    for (;;) {
        if (vstup->pozice == vstup->délka) {
            přečtené_bajty = Čtení(vstup->vstupní_deskriptor, vstup->vyrovnávací_paměť_přenosu_2, sizeof(vstup->vyrovnávací_paměť_přenosu_2));
            if (přečtené_bajty < 0) {
                if (errno == EINTR)
                    continue;
                return -1;
            }
            if (přečtené_bajty == 0) {
                if (pozice == 0 && !neplatný_vstupní_řádek)
                    return -1;
                break;
            }
            vstup->délka = (size_t)přečtené_bajty;
            vstup->pozice = 0;
        }
        znak = vstup->vyrovnávací_paměť_přenosu_2[vstup->pozice++];
        if (znak == '\n')
            break;
        if (vstup->vstupní_deskriptor == STDIN_FILENO && znak == 4) {
            if (pozice == 0 && !neplatný_vstupní_řádek)
                return -1;
            break;
        }
        if (vstup->vstupní_deskriptor == STDIN_FILENO && (znak == 8 || znak == 127)) {
            if (pozice > 0) {
                do {
                    pozice--;
                } while (pozice > 0 && ((unsigned char)vstupní_řádek[pozice] & 0xc0U) == 0x80U);
            }
            continue;
        }
        if (znak == '\r')
            continue;
        if (znak == '\0') {
            neplatný_vstupní_řádek = 1; /* Reject binary input; do not execute its prefix. */
            continue;
        }
        if (pozice + 1U < kapacita)
            vstupní_řádek[pozice++] = znak;
        else
            neplatný_vstupní_řádek = 1;
    }
    vstupní_řádek[pozice] = '\0';
    return neplatný_vstupní_řádek ? -2 : (int)pozice;
}

static int rozdělit_argumenty(char *vstupní_řádek, char **argumenty)
{
    int počet_argumentů = 0;
    char *aktuální_pozice = vstupní_řádek;
    char *výstupní_pozice = vstupní_řádek;

    while (*aktuální_pozice != '\0') {
        char uvozovka = '\0';
        while (*aktuální_pozice == ' ' || *aktuální_pozice == '\t')
            aktuální_pozice++;
        if (*aktuální_pozice == '\0' || *aktuální_pozice == '#')
            break;
        if (počet_argumentů == maximální_počet_argumentů - 1)
            return -1;
        argumenty[počet_argumentů++] = výstupní_pozice;
        while (*aktuální_pozice != '\0') {
            char znak = *aktuální_pozice++;
            if (uvozovka == '\0' && (znak == ' ' || znak == '\t'))
                break;
            if (znak == '\\' && uvozovka != '\'') {
                if (*aktuální_pozice == '\0')
                    return -1;
                *výstupní_pozice++ = *aktuální_pozice++;
            } else if (znak == '\'' || znak == '"') {
                if (uvozovka == '\0')
                    uvozovka = znak;
                else if (uvozovka == znak)
                    uvozovka = '\0';
                else
                    *výstupní_pozice++ = znak;
            } else {
                *výstupní_pozice++ = znak;
            }
        }
        if (uvozovka != '\0')
            return -1;
        *výstupní_pozice++ = '\0';
    }
    argumenty[počet_argumentů] = (char *)0;
    return počet_argumentů;
}

static void zobrazit_nápovědu(void)
{
    size_t pozice;
    vypsat_text(
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
    vypsat_text("Native command proposals (ASCII aliases remain available):\n");
    for (pozice = 0; pozice < sizeof(základní_příkazy) / sizeof(základní_příkazy[0]); pozice++) {
        vypsat_text(místní_názvy_příkazů[pozice]);
        vypsat_text(" = ");
        vypsat_text(základní_příkazy[pozice]);
        vypsat_text("\n");
    }
}

static int příkaz_odpovídá(const char *text, const char *příkaz)
{
    size_t pozice;
    if (texty_stejné(text, příkaz))
        return 1;
    for (pozice = 0; pozice < sizeof(základní_příkazy) / sizeof(základní_příkazy[0]); pozice++)
        if (texty_stejné(příkaz, základní_příkazy[pozice]))
            return texty_stejné(text, místní_názvy_příkazů[pozice]);
    return 0;
}

static int interpretovat_vstup(int vstupní_deskriptor);

static int interpretovat_příkazový_soubor(const char *název_souboru)
{
    int deskriptor_souboru_2;
    int stav;
    if (hloubka_vnoření_příkazových_souborů >= maximální_vnoření_příkazových_souborů) {
        vypsat_text("source: nesting limit\n");
        return 0;
    }
    deskriptor_souboru_2 = Otevřít(název_souboru, O_RDONLY);
    if (deskriptor_souboru_2 < 0) {
        ohlásit_chybu(název_souboru);
        return 0;
    }
    hloubka_vnoření_příkazových_souborů++;
    stav = interpretovat_vstup(deskriptor_souboru_2);
    hloubka_vnoření_příkazových_souborů--;
    (void)Zavřít(deskriptor_souboru_2);
    return stav;
}

static void vypsat_argumenty(int počet_argumentů, char **argumenty)
{
    int pozice;
    for (pozice = 1; pozice < počet_argumentů; pozice++) {
        if (pozice != 1)
            vypsat_text(" ");
        vypsat_text(argumenty[pozice]);
    }
    vypsat_text("\n");
}

static void zobrazit_pracovní_adresář(void)
{
    char cesta[128];
    if (getcwd(cesta, sizeof(cesta)) == (char *)0) {
        ohlásit_chybu("pwd");
        return;
    }
    vypsat_text(cesta);
    vypsat_text("\n");
}

static void zobrazit_obsah_souboru(const char *název_souboru)
{
    char vyrovnávací_paměť_přenosu_2[128];
    int deskriptor_souboru_2 = Otevřít(název_souboru, O_RDONLY);
    ssize_t přečtené_bajty;

    if (deskriptor_souboru_2 < 0) {
        ohlásit_chybu("cat");
        return;
    }
    while ((přečtené_bajty = Čtení(deskriptor_souboru_2, vyrovnávací_paměť_přenosu_2, sizeof(vyrovnávací_paměť_přenosu_2))) > 0)
        (void)Zápis(STDOUT_FILENO, vyrovnávací_paměť_přenosu_2, (size_t)přečtené_bajty);
    if (přečtené_bajty < 0)
        ohlásit_chybu("cat/read");
    (void)Zavřít(deskriptor_souboru_2);
    vypsat_text("\n");
}

static void zobrazit_informace_o_souboru(const char *název_souboru)
{
    struct stat stav;
    if (stat(název_souboru, &stav) < 0) {
        ohlásit_chybu("stat");
        return;
    }
    vypsat_text("size=");
    vypsat_celé_číslo((int)stav.st_size);
    vypsat_text(S_ISDIR(stav.st_mode) ? " type=directory\n" : " type=file\n");
}

static void zobrazit_identifikátory_procesů(void)
{
    vypsat_text("pid=");
    vypsat_celé_číslo((int)getpid());
    vypsat_text(" ppid=");
    vypsat_celé_číslo((int)getppid());
    vypsat_text("\n");
}

static void zobrazit_identitu_systému(void)
{
    struct utsname identita_systému;
    if (uname(&identita_systému) < 0) {
        ohlásit_chybu("uname");
        return;
    }
    vypsat_text(identita_systému.sysname);
    vypsat_text(" ");
    vypsat_text(identita_systému.release);
    vypsat_text(" ");
    vypsat_text(identita_systému.machine);
    vypsat_text("\n");
}

static void spustit_program(int počet_argumentů, char **argumenty)
{
    pid_t identifikátor_potomka;
    int stav_ukončení_potomka = 0;

    if (počet_argumentů < 2) {
        vypsat_text("usage: run FILE [ARGS...]\n");
        return;
    }
    identifikátor_potomka = fork();
    if (identifikátor_potomka < 0) {
        ohlásit_chybu("fork");
        return;
    }
    if (identifikátor_potomka == 0) {
        execve(argumenty[1], &argumenty[1], (char *const *)0);
        ohlásit_chybu("execve");
        _exit(127);
    }
    if (waitpid(identifikátor_potomka, &stav_ukončení_potomka, 0) < 0) {
        ohlásit_chybu("waitpid");
        return;
    }
    vypsat_text("exit-status=");
    vypsat_celé_číslo(WEXITSTATUS(stav_ukončení_potomka));
    vypsat_text("\n");
}

static void ověřit_návrat_datagramu(const char *zpráva)
{
    struct sockaddr_in adresa_příjemce = {0};
    struct sockaddr_in adresa_odesílatele = {0};
    socklen_t délka_adresy_odesílatele = sizeof(adresa_odesílatele);
    char přijatá_data[96];
    size_t délka_zprávy_v_bajtech = délka_textu_v_bajtech(zpráva);
    int přijímací_koncový_bod = -1;
    int odesílací_koncový_bod = -1;
    ssize_t počet_přijatých_bajtů;

    if (délka_zprávy_v_bajtech >= sizeof(přijatá_data)) {
        vypsat_text("udp: message exceeds 95 bytes\n");
        return;
    }
    přijímací_koncový_bod = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    odesílací_koncový_bod = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (přijímací_koncový_bod < 0 || odesílací_koncový_bod < 0) {
        ohlásit_chybu("socket");
        goto zavřít_komunikační_body;
    }
    adresa_příjemce.sin_family = AF_INET;
    adresa_příjemce.sin_port = htons(40404);
    adresa_příjemce.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    if (bind(přijímací_koncový_bod, (const struct sockaddr *)&adresa_příjemce, sizeof(adresa_příjemce)) < 0) {
        ohlásit_chybu("bind");
        goto zavřít_komunikační_body;
    }
    if (connect(odesílací_koncový_bod, (const struct sockaddr *)&adresa_příjemce, sizeof(adresa_příjemce)) < 0) {
        ohlásit_chybu("connect");
        goto zavřít_komunikační_body;
    }
    if (send(odesílací_koncový_bod, zpráva, délka_zprávy_v_bajtech, 0) != (ssize_t)délka_zprávy_v_bajtech) {
        ohlásit_chybu("send");
        goto zavřít_komunikační_body;
    }
    počet_přijatých_bajtů = recvfrom(přijímací_koncový_bod, přijatá_data, sizeof(přijatá_data) - 1U, 0,
                         (struct sockaddr *)&adresa_odesílatele, &délka_adresy_odesílatele);
    if (počet_přijatých_bajtů < 0) {
        ohlásit_chybu("recvfrom");
        goto zavřít_komunikační_body;
    }
    přijatá_data[počet_přijatých_bajtů] = '\0';
    vypsat_text("udp-received: ");
    vypsat_text(přijatá_data);
    vypsat_text("\n");

zavřít_komunikační_body:
    if (odesílací_koncový_bod >= 0)
        (void)Zavřít(odesílací_koncový_bod);
    if (přijímací_koncový_bod >= 0)
        (void)Zavřít(přijímací_koncový_bod);
}

static int interpretovat_vstup(int vstupní_deskriptor)
{
    char vstupní_řádek[kapacita_vstupního_řádku];
    char *argumenty[maximální_počet_argumentů];
    struct vstupní_proud vstup = {0};
    vstup.vstupní_deskriptor = vstupní_deskriptor;

    for (;;) {
        int počet_argumentů;
        int stav;
        if (vstupní_deskriptor == STDIN_FILENO)
            vypsat_text("worldos$ ");
        stav = číst_vstupní_řádek(&vstup, vstupní_řádek, sizeof(vstupní_řádek));
        if (stav == -1)
            return 0;
        if (stav == -2) {
            vypsat_text("input rejected: overlong or binary line\n");
            continue;
        }
        počet_argumentů = rozdělit_argumenty(vstupní_řádek, argumenty);
        if (počet_argumentů < 0) {
            vypsat_text("syntax error: quote, escape or argument limit\n");
            continue;
        }
        if (počet_argumentů == 0)
            continue;
        if (příkaz_odpovídá(argumenty[0], "help"))
            zobrazit_nápovědu();
        else if (příkaz_odpovídá(argumenty[0], "echo"))
            vypsat_argumenty(počet_argumentů, argumenty);
        else if (příkaz_odpovídá(argumenty[0], "pwd"))
            zobrazit_pracovní_adresář();
        else if (příkaz_odpovídá(argumenty[0], "cd")) {
            if (počet_argumentů < 2)
                vypsat_text("usage: cd PATH\n");
            else if (chdir(argumenty[1]) < 0)
                ohlásit_chybu("cd");
        } else if (příkaz_odpovídá(argumenty[0], "cat")) {
            if (počet_argumentů < 2)
                vypsat_text("usage: cat FILE\n");
            else
                zobrazit_obsah_souboru(argumenty[1]);
        } else if (příkaz_odpovídá(argumenty[0], "stat")) {
            if (počet_argumentů < 2)
                vypsat_text("usage: stat FILE\n");
            else
                zobrazit_informace_o_souboru(argumenty[1]);
        } else if (příkaz_odpovídá(argumenty[0], "pid"))
            zobrazit_identifikátory_procesů();
        else if (příkaz_odpovídá(argumenty[0], "uname"))
            zobrazit_identitu_systému();
        else if (příkaz_odpovídá(argumenty[0], "run"))
            spustit_program(počet_argumentů, argumenty);
        else if (příkaz_odpovídá(argumenty[0], "udp"))
            ověřit_návrat_datagramu(počet_argumentů >= 2 ? argumenty[1] : "ping");
        else if (příkaz_odpovídá(argumenty[0], "source")) {
            if (počet_argumentů < 2)
                vypsat_text("usage: source FILE\n");
            else if (interpretovat_příkazový_soubor(argumenty[1]))
                return 1;
        } else if (příkaz_odpovídá(argumenty[0], "exit"))
            return 1;
        else
            vypsat_text("unknown command; type help\n");
    }
}

int main(void)
{
    vypsat_text("WORLDOS-SHELL:READY\n");
    (void)interpretovat_vstup(STDIN_FILENO);
    vypsat_text("WORLDOS-SHELL:EXIT\n");
    return 0;
}
