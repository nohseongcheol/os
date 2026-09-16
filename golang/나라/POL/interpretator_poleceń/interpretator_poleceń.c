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

enum { pojemność_wiersza_wejścia = 512, maksymalna_liczba_argumentów = 16, maksymalne_zagnieżdżenie_plików_poleceń = 4 };
static int głębokość_zagnieżdżenia_plików_poleceń;
struct strumień_wejściowy {
    int deskryptor_wejścia;
    char bufor_przesyłania_2[256];
    size_t pozycja;
    size_t długość;
};

static size_t długość_tekstu_w_bajtach(const char *tekst)
{
    size_t długość = 0;
    while (tekst[długość] != '\0')
        długość++;
    return długość;
}

static int teksty_równe(const char *lewy, const char *prawy)
{
    size_t pozycja = 0;
    while (lewy[pozycja] == prawy[pozycja]) {
        if (lewy[pozycja] == '\0')
            return 1;
        pozycja++;
    }
    return 0;
}

static void wypisz_tekst(const char *tekst)
{
    size_t długość = długość_tekstu_w_bajtach(tekst);
    while (długość > 0U) {
        ssize_t liczba_zapisanych_bajtów = Zapis(STDOUT_FILENO, tekst, długość);
        if (liczba_zapisanych_bajtów <= 0)
            return;
        tekst += liczba_zapisanych_bajtów;
        długość -= (size_t)liczba_zapisanych_bajtów;
    }
}

static void wypisz_liczbę_całkowitą(int wartość)
{
    char znaki_cyfr[16];
    unsigned int liczba_cyfr;
    unsigned int wartość_bez_znaku;

    if (wartość < 0) {
        wypisz_tekst("-");
        wartość_bez_znaku = (unsigned int)(-(wartość + 1)) + 1U;
    } else {
        wartość_bez_znaku = (unsigned int)wartość;
    }
    liczba_cyfr = 0;
    do {
        znaki_cyfr[liczba_cyfr++] = (char)('0' + wartość_bez_znaku % 10U);
        wartość_bez_znaku /= 10U;
    } while (wartość_bez_znaku != 0U);
    while (liczba_cyfr > 0U) {
        liczba_cyfr--;
        (void)Zapis(STDOUT_FILENO, &znaki_cyfr[liczba_cyfr], 1);
    }
}

static void zgłoś_błąd(const char *operacja)
{
    wypisz_tekst("error: ");
    wypisz_tekst(operacja);
    wypisz_tekst(" errno=");
    wypisz_liczbę_całkowitą(errno);
    wypisz_tekst("\n");
}

static int odczytaj_wiersz_wejścia(struct strumień_wejściowy *wejście, char *wiersz_wejścia, size_t pojemność)
{
    size_t pozycja = 0;
    int nieprawidłowy_wiersz_wejścia = 0;
    char znak;
    ssize_t odczytane_bajty;
    if (pojemność < 2U)
        return -2;
    for (;;) {
        if (wejście->pozycja == wejście->długość) {
            odczytane_bajty = Odczyt(wejście->deskryptor_wejścia, wejście->bufor_przesyłania_2, sizeof(wejście->bufor_przesyłania_2));
            if (odczytane_bajty < 0) {
                if (errno == EINTR)
                    continue;
                return -1;
            }
            if (odczytane_bajty == 0) {
                if (pozycja == 0 && !nieprawidłowy_wiersz_wejścia)
                    return -1;
                break;
            }
            wejście->długość = (size_t)odczytane_bajty;
            wejście->pozycja = 0;
        }
        znak = wejście->bufor_przesyłania_2[wejście->pozycja++];
        if (znak == '\n')
            break;
        if (wejście->deskryptor_wejścia == STDIN_FILENO && znak == 4) {
            if (pozycja == 0 && !nieprawidłowy_wiersz_wejścia)
                return -1;
            break;
        }
        if (wejście->deskryptor_wejścia == STDIN_FILENO && (znak == 8 || znak == 127)) {
            if (pozycja > 0) {
                do {
                    pozycja--;
                } while (pozycja > 0 && ((unsigned char)wiersz_wejścia[pozycja] & 0xc0U) == 0x80U);
            }
            continue;
        }
        if (znak == '\r')
            continue;
        if (znak == '\0') {
            nieprawidłowy_wiersz_wejścia = 1; /* Reject binary input; do not execute its prefix. */
            continue;
        }
        if (pozycja + 1U < pojemność)
            wiersz_wejścia[pozycja++] = znak;
        else
            nieprawidłowy_wiersz_wejścia = 1;
    }
    wiersz_wejścia[pozycja] = '\0';
    return nieprawidłowy_wiersz_wejścia ? -2 : (int)pozycja;
}

static int rozdziel_argumenty(char *wiersz_wejścia, char **argumenty)
{
    int liczba_argumentów = 0;
    char *bieżąca_pozycja = wiersz_wejścia;
    char *pozycja_wyjścia = wiersz_wejścia;

    while (*bieżąca_pozycja != '\0') {
        char cudzysłów = '\0';
        while (*bieżąca_pozycja == ' ' || *bieżąca_pozycja == '\t')
            bieżąca_pozycja++;
        if (*bieżąca_pozycja == '\0' || *bieżąca_pozycja == '#')
            break;
        if (liczba_argumentów == maksymalna_liczba_argumentów - 1)
            return -1;
        argumenty[liczba_argumentów++] = pozycja_wyjścia;
        while (*bieżąca_pozycja != '\0') {
            char znak = *bieżąca_pozycja++;
            if (cudzysłów == '\0' && (znak == ' ' || znak == '\t'))
                break;
            if (znak == '\\' && cudzysłów != '\'') {
                if (*bieżąca_pozycja == '\0')
                    return -1;
                *pozycja_wyjścia++ = *bieżąca_pozycja++;
            } else if (znak == '\'' || znak == '"') {
                if (cudzysłów == '\0')
                    cudzysłów = znak;
                else if (cudzysłów == znak)
                    cudzysłów = '\0';
                else
                    *pozycja_wyjścia++ = znak;
            } else {
                *pozycja_wyjścia++ = znak;
            }
        }
        if (cudzysłów != '\0')
            return -1;
        *pozycja_wyjścia++ = '\0';
    }
    argumenty[liczba_argumentów] = (char *)0;
    return liczba_argumentów;
}

static void pokaż_pomoc(void)
{
    size_t pozycja;
    wypisz_tekst(
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
    wypisz_tekst("Native command proposals (ASCII aliases remain available):\n");
    for (pozycja = 0; pozycja < sizeof(polecenia_podstawowe) / sizeof(polecenia_podstawowe[0]); pozycja++) {
        wypisz_tekst(lokalne_nazwy_poleceń[pozycja]);
        wypisz_tekst(" = ");
        wypisz_tekst(polecenia_podstawowe[pozycja]);
        wypisz_tekst("\n");
    }
}

static int polecenie_pasuje(const char *tekst, const char *polecenie)
{
    size_t pozycja;
    if (teksty_równe(tekst, polecenie))
        return 1;
    for (pozycja = 0; pozycja < sizeof(polecenia_podstawowe) / sizeof(polecenia_podstawowe[0]); pozycja++)
        if (teksty_równe(polecenie, polecenia_podstawowe[pozycja]))
            return teksty_równe(tekst, lokalne_nazwy_poleceń[pozycja]);
    return 0;
}

static int interpretuj_wejście(int deskryptor_wejścia);

static int interpretuj_plik_poleceń(const char *nazwa_pliku)
{
    int deskryptor_pliku_2;
    int stan;
    if (głębokość_zagnieżdżenia_plików_poleceń >= maksymalne_zagnieżdżenie_plików_poleceń) {
        wypisz_tekst("source: nesting limit\n");
        return 0;
    }
    deskryptor_pliku_2 = Otwórz(nazwa_pliku, O_RDONLY);
    if (deskryptor_pliku_2 < 0) {
        zgłoś_błąd(nazwa_pliku);
        return 0;
    }
    głębokość_zagnieżdżenia_plików_poleceń++;
    stan = interpretuj_wejście(deskryptor_pliku_2);
    głębokość_zagnieżdżenia_plików_poleceń--;
    (void)Zamknij(deskryptor_pliku_2);
    return stan;
}

static void wypisz_argumenty(int liczba_argumentów, char **argumenty)
{
    int pozycja;
    for (pozycja = 1; pozycja < liczba_argumentów; pozycja++) {
        if (pozycja != 1)
            wypisz_tekst(" ");
        wypisz_tekst(argumenty[pozycja]);
    }
    wypisz_tekst("\n");
}

static void pokaż_katalog_roboczy(void)
{
    char ścieżka[128];
    if (getcwd(ścieżka, sizeof(ścieżka)) == (char *)0) {
        zgłoś_błąd("pwd");
        return;
    }
    wypisz_tekst(ścieżka);
    wypisz_tekst("\n");
}

static void pokaż_zawartość_pliku(const char *nazwa_pliku)
{
    char bufor_przesyłania_2[128];
    int deskryptor_pliku_2 = Otwórz(nazwa_pliku, O_RDONLY);
    ssize_t odczytane_bajty;

    if (deskryptor_pliku_2 < 0) {
        zgłoś_błąd("cat");
        return;
    }
    while ((odczytane_bajty = Odczyt(deskryptor_pliku_2, bufor_przesyłania_2, sizeof(bufor_przesyłania_2))) > 0)
        (void)Zapis(STDOUT_FILENO, bufor_przesyłania_2, (size_t)odczytane_bajty);
    if (odczytane_bajty < 0)
        zgłoś_błąd("cat/read");
    (void)Zamknij(deskryptor_pliku_2);
    wypisz_tekst("\n");
}

static void pokaż_informacje_o_pliku(const char *nazwa_pliku)
{
    struct stat stan;
    if (stat(nazwa_pliku, &stan) < 0) {
        zgłoś_błąd("stat");
        return;
    }
    wypisz_tekst("size=");
    wypisz_liczbę_całkowitą((int)stan.st_size);
    wypisz_tekst(S_ISDIR(stan.st_mode) ? " type=directory\n" : " type=file\n");
}

static void pokaż_identyfikatory_procesów(void)
{
    wypisz_tekst("pid=");
    wypisz_liczbę_całkowitą((int)getpid());
    wypisz_tekst(" ppid=");
    wypisz_liczbę_całkowitą((int)getppid());
    wypisz_tekst("\n");
}

static void pokaż_tożsamość_systemu(void)
{
    struct utsname tożsamość_systemu;
    if (uname(&tożsamość_systemu) < 0) {
        zgłoś_błąd("uname");
        return;
    }
    wypisz_tekst(tożsamość_systemu.sysname);
    wypisz_tekst(" ");
    wypisz_tekst(tożsamość_systemu.release);
    wypisz_tekst(" ");
    wypisz_tekst(tożsamość_systemu.machine);
    wypisz_tekst("\n");
}

static void uruchom_program(int liczba_argumentów, char **argumenty)
{
    pid_t identyfikator_procesu_potomnego;
    int stan_zakończenia_procesu_potomnego = 0;

    if (liczba_argumentów < 2) {
        wypisz_tekst("usage: run FILE [ARGS...]\n");
        return;
    }
    identyfikator_procesu_potomnego = fork();
    if (identyfikator_procesu_potomnego < 0) {
        zgłoś_błąd("fork");
        return;
    }
    if (identyfikator_procesu_potomnego == 0) {
        execve(argumenty[1], &argumenty[1], (char *const *)0);
        zgłoś_błąd("execve");
        _exit(127);
    }
    if (waitpid(identyfikator_procesu_potomnego, &stan_zakończenia_procesu_potomnego, 0) < 0) {
        zgłoś_błąd("waitpid");
        return;
    }
    wypisz_tekst("exit-status=");
    wypisz_liczbę_całkowitą(WEXITSTATUS(stan_zakończenia_procesu_potomnego));
    wypisz_tekst("\n");
}

static void sprawdź_powrót_datagramu(const char *wiadomość)
{
    struct sockaddr_in adres_odbiorcy = {0};
    struct sockaddr_in adres_nadawcy = {0};
    socklen_t długość_adresu_nadawcy = sizeof(adres_nadawcy);
    char odebrane_dane[96];
    size_t długość_wiadomości_w_bajtach = długość_tekstu_w_bajtach(wiadomość);
    int punkt_odbiorczy = -1;
    int punkt_nadawczy = -1;
    ssize_t liczba_odebranych_bajtów;

    if (długość_wiadomości_w_bajtach >= sizeof(odebrane_dane)) {
        wypisz_tekst("udp: message exceeds 95 bytes\n");
        return;
    }
    punkt_odbiorczy = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    punkt_nadawczy = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (punkt_odbiorczy < 0 || punkt_nadawczy < 0) {
        zgłoś_błąd("socket");
        goto zamknij_punkty_komunikacji;
    }
    adres_odbiorcy.sin_family = AF_INET;
    adres_odbiorcy.sin_port = htons(40404);
    adres_odbiorcy.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    if (bind(punkt_odbiorczy, (const struct sockaddr *)&adres_odbiorcy, sizeof(adres_odbiorcy)) < 0) {
        zgłoś_błąd("bind");
        goto zamknij_punkty_komunikacji;
    }
    if (connect(punkt_nadawczy, (const struct sockaddr *)&adres_odbiorcy, sizeof(adres_odbiorcy)) < 0) {
        zgłoś_błąd("connect");
        goto zamknij_punkty_komunikacji;
    }
    if (send(punkt_nadawczy, wiadomość, długość_wiadomości_w_bajtach, 0) != (ssize_t)długość_wiadomości_w_bajtach) {
        zgłoś_błąd("send");
        goto zamknij_punkty_komunikacji;
    }
    liczba_odebranych_bajtów = recvfrom(punkt_odbiorczy, odebrane_dane, sizeof(odebrane_dane) - 1U, 0,
                         (struct sockaddr *)&adres_nadawcy, &długość_adresu_nadawcy);
    if (liczba_odebranych_bajtów < 0) {
        zgłoś_błąd("recvfrom");
        goto zamknij_punkty_komunikacji;
    }
    odebrane_dane[liczba_odebranych_bajtów] = '\0';
    wypisz_tekst("udp-received: ");
    wypisz_tekst(odebrane_dane);
    wypisz_tekst("\n");

zamknij_punkty_komunikacji:
    if (punkt_nadawczy >= 0)
        (void)Zamknij(punkt_nadawczy);
    if (punkt_odbiorczy >= 0)
        (void)Zamknij(punkt_odbiorczy);
}

static int interpretuj_wejście(int deskryptor_wejścia)
{
    char wiersz_wejścia[pojemność_wiersza_wejścia];
    char *argumenty[maksymalna_liczba_argumentów];
    struct strumień_wejściowy wejście = {0};
    wejście.deskryptor_wejścia = deskryptor_wejścia;

    for (;;) {
        int liczba_argumentów;
        int stan;
        if (deskryptor_wejścia == STDIN_FILENO)
            wypisz_tekst("worldos$ ");
        stan = odczytaj_wiersz_wejścia(&wejście, wiersz_wejścia, sizeof(wiersz_wejścia));
        if (stan == -1)
            return 0;
        if (stan == -2) {
            wypisz_tekst("input rejected: overlong or binary line\n");
            continue;
        }
        liczba_argumentów = rozdziel_argumenty(wiersz_wejścia, argumenty);
        if (liczba_argumentów < 0) {
            wypisz_tekst("syntax error: quote, escape or argument limit\n");
            continue;
        }
        if (liczba_argumentów == 0)
            continue;
        if (polecenie_pasuje(argumenty[0], "help"))
            pokaż_pomoc();
        else if (polecenie_pasuje(argumenty[0], "echo"))
            wypisz_argumenty(liczba_argumentów, argumenty);
        else if (polecenie_pasuje(argumenty[0], "pwd"))
            pokaż_katalog_roboczy();
        else if (polecenie_pasuje(argumenty[0], "cd")) {
            if (liczba_argumentów < 2)
                wypisz_tekst("usage: cd PATH\n");
            else if (chdir(argumenty[1]) < 0)
                zgłoś_błąd("cd");
        } else if (polecenie_pasuje(argumenty[0], "cat")) {
            if (liczba_argumentów < 2)
                wypisz_tekst("usage: cat FILE\n");
            else
                pokaż_zawartość_pliku(argumenty[1]);
        } else if (polecenie_pasuje(argumenty[0], "stat")) {
            if (liczba_argumentów < 2)
                wypisz_tekst("usage: stat FILE\n");
            else
                pokaż_informacje_o_pliku(argumenty[1]);
        } else if (polecenie_pasuje(argumenty[0], "pid"))
            pokaż_identyfikatory_procesów();
        else if (polecenie_pasuje(argumenty[0], "uname"))
            pokaż_tożsamość_systemu();
        else if (polecenie_pasuje(argumenty[0], "run"))
            uruchom_program(liczba_argumentów, argumenty);
        else if (polecenie_pasuje(argumenty[0], "udp"))
            sprawdź_powrót_datagramu(liczba_argumentów >= 2 ? argumenty[1] : "ping");
        else if (polecenie_pasuje(argumenty[0], "source")) {
            if (liczba_argumentów < 2)
                wypisz_tekst("usage: source FILE\n");
            else if (interpretuj_plik_poleceń(argumenty[1]))
                return 1;
        } else if (polecenie_pasuje(argumenty[0], "exit"))
            return 1;
        else
            wypisz_tekst("unknown command; type help\n");
    }
}

int main(void)
{
    wypisz_tekst("WORLDOS-SHELL:READY\n");
    (void)interpretuj_wejście(STDIN_FILENO);
    wypisz_tekst("WORLDOS-SHELL:EXIT\n");
    return 0;
}
