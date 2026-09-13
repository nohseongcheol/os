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

enum { inmatningsradens_kapacitet = 512, högsta_antal_argument = 16, högsta_kommandonästling = 4 };
static int kommandonästlingens_djup;
struct inmatningsström {
    int inmatningsbeskrivare;
    char överföringsbuffert_2[256];
    size_t position;
    size_t längd;
};

static size_t textlängd_i_byte(const char *text)
{
    size_t längd = 0;
    while (text[längd] != '\0')
        längd++;
    return längd;
}

static int texter_lika(const char *vänster, const char *höger)
{
    size_t position = 0;
    while (vänster[position] == höger[position]) {
        if (vänster[position] == '\0')
            return 1;
        position++;
    }
    return 0;
}

static void skriv_text(const char *text)
{
    size_t längd = textlängd_i_byte(text);
    while (längd > 0U) {
        ssize_t antal_skrivna_byte = Skriv(STDOUT_FILENO, text, längd);
        if (antal_skrivna_byte <= 0)
            return;
        text += antal_skrivna_byte;
        längd -= (size_t)antal_skrivna_byte;
    }
}

static void skriv_heltal(int värde)
{
    char siffertecken[16];
    unsigned int antal_siffror;
    unsigned int storlek_utan_tecken;

    if (värde < 0) {
        skriv_text("-");
        storlek_utan_tecken = (unsigned int)(-(värde + 1)) + 1U;
    } else {
        storlek_utan_tecken = (unsigned int)värde;
    }
    antal_siffror = 0;
    do {
        siffertecken[antal_siffror++] = (char)('0' + storlek_utan_tecken % 10U);
        storlek_utan_tecken /= 10U;
    } while (storlek_utan_tecken != 0U);
    while (antal_siffror > 0U) {
        antal_siffror--;
        (void)Skriv(STDOUT_FILENO, &siffertecken[antal_siffror], 1);
    }
}

static void rapportera_fel(const char *åtgärd)
{
    skriv_text("error: ");
    skriv_text(åtgärd);
    skriv_text(" errno=");
    skriv_heltal(errno);
    skriv_text("\n");
}

static int läs_inmatningsrad(struct inmatningsström *inmatning, char *inmatningsrad, size_t kapacitet)
{
    size_t position = 0;
    int ogiltig_inmatningsrad = 0;
    char tecken;
    ssize_t lästa_byte;
    if (kapacitet < 2U)
        return -2;
    for (;;) {
        if (inmatning->position == inmatning->längd) {
            lästa_byte = Läs(inmatning->inmatningsbeskrivare, inmatning->överföringsbuffert_2, sizeof(inmatning->överföringsbuffert_2));
            if (lästa_byte < 0) {
                if (errno == EINTR)
                    continue;
                return -1;
            }
            if (lästa_byte == 0) {
                if (position == 0 && !ogiltig_inmatningsrad)
                    return -1;
                break;
            }
            inmatning->längd = (size_t)lästa_byte;
            inmatning->position = 0;
        }
        tecken = inmatning->överföringsbuffert_2[inmatning->position++];
        if (tecken == '\n')
            break;
        if (inmatning->inmatningsbeskrivare == STDIN_FILENO && tecken == 4) {
            if (position == 0 && !ogiltig_inmatningsrad)
                return -1;
            break;
        }
        if (inmatning->inmatningsbeskrivare == STDIN_FILENO && (tecken == 8 || tecken == 127)) {
            if (position > 0) {
                do {
                    position--;
                } while (position > 0 && ((unsigned char)inmatningsrad[position] & 0xc0U) == 0x80U);
            }
            continue;
        }
        if (tecken == '\r')
            continue;
        if (tecken == '\0') {
            ogiltig_inmatningsrad = 1; /* Reject binary input; do not execute its prefix. */
            continue;
        }
        if (position + 1U < kapacitet)
            inmatningsrad[position++] = tecken;
        else
            ogiltig_inmatningsrad = 1;
    }
    inmatningsrad[position] = '\0';
    return ogiltig_inmatningsrad ? -2 : (int)position;
}

static int dela_upp_argument(char *inmatningsrad, char **argument_2)
{
    int antal_argument = 0;
    char *aktuell_position = inmatningsrad;
    char *utmatningsposition = inmatningsrad;

    while (*aktuell_position != '\0') {
        char citattecken = '\0';
        while (*aktuell_position == ' ' || *aktuell_position == '\t')
            aktuell_position++;
        if (*aktuell_position == '\0' || *aktuell_position == '#')
            break;
        if (antal_argument == högsta_antal_argument - 1)
            return -1;
        argument_2[antal_argument++] = utmatningsposition;
        while (*aktuell_position != '\0') {
            char tecken = *aktuell_position++;
            if (citattecken == '\0' && (tecken == ' ' || tecken == '\t'))
                break;
            if (tecken == '\\' && citattecken != '\'') {
                if (*aktuell_position == '\0')
                    return -1;
                *utmatningsposition++ = *aktuell_position++;
            } else if (tecken == '\'' || tecken == '"') {
                if (citattecken == '\0')
                    citattecken = tecken;
                else if (citattecken == tecken)
                    citattecken = '\0';
                else
                    *utmatningsposition++ = tecken;
            } else {
                *utmatningsposition++ = tecken;
            }
        }
        if (citattecken != '\0')
            return -1;
        *utmatningsposition++ = '\0';
    }
    argument_2[antal_argument] = (char *)0;
    return antal_argument;
}

static void visa_hjälp(void)
{
    size_t position;
    skriv_text(
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
    skriv_text("Native command proposals (ASCII aliases remain available):\n");
    for (position = 0; position < sizeof(grundkommandon) / sizeof(grundkommandon[0]); position++) {
        skriv_text(lokala_kommandonamn[position]);
        skriv_text(" = ");
        skriv_text(grundkommandon[position]);
        skriv_text("\n");
    }
}

static int kommando_stämmer(const char *text, const char *kommando)
{
    size_t position;
    if (texter_lika(text, kommando))
        return 1;
    for (position = 0; position < sizeof(grundkommandon) / sizeof(grundkommandon[0]); position++)
        if (texter_lika(kommando, grundkommandon[position]))
            return texter_lika(text, lokala_kommandonamn[position]);
    return 0;
}

static int tolka_inmatning(int inmatningsbeskrivare);

static int tolka_kommandofil(const char *filnamn)
{
    int filbeskrivare_2;
    int tillstånd;
    if (kommandonästlingens_djup >= högsta_kommandonästling) {
        skriv_text("source: nesting limit\n");
        return 0;
    }
    filbeskrivare_2 = Öppna(filnamn, O_RDONLY);
    if (filbeskrivare_2 < 0) {
        rapportera_fel(filnamn);
        return 0;
    }
    kommandonästlingens_djup++;
    tillstånd = tolka_inmatning(filbeskrivare_2);
    kommandonästlingens_djup--;
    (void)Stäng(filbeskrivare_2);
    return tillstånd;
}

static void visa_argument(int antal_argument, char **argument_2)
{
    int position;
    for (position = 1; position < antal_argument; position++) {
        if (position != 1)
            skriv_text(" ");
        skriv_text(argument_2[position]);
    }
    skriv_text("\n");
}

static void visa_arbetskatalog(void)
{
    char sökväg[128];
    if (getcwd(sökväg, sizeof(sökväg)) == (char *)0) {
        rapportera_fel("pwd");
        return;
    }
    skriv_text(sökväg);
    skriv_text("\n");
}

static void visa_filinnehåll(const char *filnamn)
{
    char överföringsbuffert_2[128];
    int filbeskrivare_2 = Öppna(filnamn, O_RDONLY);
    ssize_t lästa_byte;

    if (filbeskrivare_2 < 0) {
        rapportera_fel("cat");
        return;
    }
    while ((lästa_byte = Läs(filbeskrivare_2, överföringsbuffert_2, sizeof(överföringsbuffert_2))) > 0)
        (void)Skriv(STDOUT_FILENO, överföringsbuffert_2, (size_t)lästa_byte);
    if (lästa_byte < 0)
        rapportera_fel("cat/read");
    (void)Stäng(filbeskrivare_2);
    skriv_text("\n");
}

static void visa_filinformation(const char *filnamn)
{
    struct stat tillstånd;
    if (stat(filnamn, &tillstånd) < 0) {
        rapportera_fel("stat");
        return;
    }
    skriv_text("size=");
    skriv_heltal((int)tillstånd.st_size);
    skriv_text(S_ISDIR(tillstånd.st_mode) ? " type=directory\n" : " type=file\n");
}

static void visa_processidentifierare(void)
{
    skriv_text("pid=");
    skriv_heltal((int)getpid());
    skriv_text(" ppid=");
    skriv_heltal((int)getppid());
    skriv_text("\n");
}

static void visa_systemidentitet(void)
{
    struct utsname systemidentitet;
    if (uname(&systemidentitet) < 0) {
        rapportera_fel("uname");
        return;
    }
    skriv_text(systemidentitet.sysname);
    skriv_text(" ");
    skriv_text(systemidentitet.release);
    skriv_text(" ");
    skriv_text(systemidentitet.machine);
    skriv_text("\n");
}

static void kör_program(int antal_argument, char **argument_2)
{
    pid_t barnprocessens_identifierare;
    int barnprocessens_avslutningsstatus = 0;

    if (antal_argument < 2) {
        skriv_text("usage: run FILE [ARGS...]\n");
        return;
    }
    barnprocessens_identifierare = fork();
    if (barnprocessens_identifierare < 0) {
        rapportera_fel("fork");
        return;
    }
    if (barnprocessens_identifierare == 0) {
        execve(argument_2[1], &argument_2[1], (char *const *)0);
        rapportera_fel("execve");
        _exit(127);
    }
    if (waitpid(barnprocessens_identifierare, &barnprocessens_avslutningsstatus, 0) < 0) {
        rapportera_fel("waitpid");
        return;
    }
    skriv_text("exit-status=");
    skriv_heltal(WEXITSTATUS(barnprocessens_avslutningsstatus));
    skriv_text("\n");
}

static void prova_datagrammets_återföring(const char *meddelande)
{
    struct sockaddr_in mottagaradress = {0};
    struct sockaddr_in avsändaradress = {0};
    socklen_t avsändaradressens_längd = sizeof(avsändaradress);
    char mottagna_data[96];
    size_t meddelandets_längd_i_byte = textlängd_i_byte(meddelande);
    int mottagande_kommunikationspunkt = -1;
    int sändande_kommunikationspunkt = -1;
    ssize_t antal_mottagna_byte;

    if (meddelandets_längd_i_byte >= sizeof(mottagna_data)) {
        skriv_text("udp: message exceeds 95 bytes\n");
        return;
    }
    mottagande_kommunikationspunkt = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    sändande_kommunikationspunkt = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (mottagande_kommunikationspunkt < 0 || sändande_kommunikationspunkt < 0) {
        rapportera_fel("socket");
        goto stäng_kommunikationspunkter;
    }
    mottagaradress.sin_family = AF_INET;
    mottagaradress.sin_port = htons(40404);
    mottagaradress.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    if (bind(mottagande_kommunikationspunkt, (const struct sockaddr *)&mottagaradress, sizeof(mottagaradress)) < 0) {
        rapportera_fel("bind");
        goto stäng_kommunikationspunkter;
    }
    if (connect(sändande_kommunikationspunkt, (const struct sockaddr *)&mottagaradress, sizeof(mottagaradress)) < 0) {
        rapportera_fel("connect");
        goto stäng_kommunikationspunkter;
    }
    if (send(sändande_kommunikationspunkt, meddelande, meddelandets_längd_i_byte, 0) != (ssize_t)meddelandets_längd_i_byte) {
        rapportera_fel("send");
        goto stäng_kommunikationspunkter;
    }
    antal_mottagna_byte = recvfrom(mottagande_kommunikationspunkt, mottagna_data, sizeof(mottagna_data) - 1U, 0,
                         (struct sockaddr *)&avsändaradress, &avsändaradressens_längd);
    if (antal_mottagna_byte < 0) {
        rapportera_fel("recvfrom");
        goto stäng_kommunikationspunkter;
    }
    mottagna_data[antal_mottagna_byte] = '\0';
    skriv_text("udp-received: ");
    skriv_text(mottagna_data);
    skriv_text("\n");

stäng_kommunikationspunkter:
    if (sändande_kommunikationspunkt >= 0)
        (void)Stäng(sändande_kommunikationspunkt);
    if (mottagande_kommunikationspunkt >= 0)
        (void)Stäng(mottagande_kommunikationspunkt);
}

static int tolka_inmatning(int inmatningsbeskrivare)
{
    char inmatningsrad[inmatningsradens_kapacitet];
    char *argument_2[högsta_antal_argument];
    struct inmatningsström inmatning = {0};
    inmatning.inmatningsbeskrivare = inmatningsbeskrivare;

    for (;;) {
        int antal_argument;
        int tillstånd;
        if (inmatningsbeskrivare == STDIN_FILENO)
            skriv_text("worldos$ ");
        tillstånd = läs_inmatningsrad(&inmatning, inmatningsrad, sizeof(inmatningsrad));
        if (tillstånd == -1)
            return 0;
        if (tillstånd == -2) {
            skriv_text("input rejected: overlong or binary line\n");
            continue;
        }
        antal_argument = dela_upp_argument(inmatningsrad, argument_2);
        if (antal_argument < 0) {
            skriv_text("syntax error: quote, escape or argument limit\n");
            continue;
        }
        if (antal_argument == 0)
            continue;
        if (kommando_stämmer(argument_2[0], "help"))
            visa_hjälp();
        else if (kommando_stämmer(argument_2[0], "echo"))
            visa_argument(antal_argument, argument_2);
        else if (kommando_stämmer(argument_2[0], "pwd"))
            visa_arbetskatalog();
        else if (kommando_stämmer(argument_2[0], "cd")) {
            if (antal_argument < 2)
                skriv_text("usage: cd PATH\n");
            else if (chdir(argument_2[1]) < 0)
                rapportera_fel("cd");
        } else if (kommando_stämmer(argument_2[0], "cat")) {
            if (antal_argument < 2)
                skriv_text("usage: cat FILE\n");
            else
                visa_filinnehåll(argument_2[1]);
        } else if (kommando_stämmer(argument_2[0], "stat")) {
            if (antal_argument < 2)
                skriv_text("usage: stat FILE\n");
            else
                visa_filinformation(argument_2[1]);
        } else if (kommando_stämmer(argument_2[0], "pid"))
            visa_processidentifierare();
        else if (kommando_stämmer(argument_2[0], "uname"))
            visa_systemidentitet();
        else if (kommando_stämmer(argument_2[0], "run"))
            kör_program(antal_argument, argument_2);
        else if (kommando_stämmer(argument_2[0], "udp"))
            prova_datagrammets_återföring(antal_argument >= 2 ? argument_2[1] : "ping");
        else if (kommando_stämmer(argument_2[0], "source")) {
            if (antal_argument < 2)
                skriv_text("usage: source FILE\n");
            else if (tolka_kommandofil(argument_2[1]))
                return 1;
        } else if (kommando_stämmer(argument_2[0], "exit"))
            return 1;
        else
            skriv_text("unknown command; type help\n");
    }
}

int main(void)
{
    skriv_text("WORLDOS-SHELL:READY\n");
    (void)tolka_inmatning(STDIN_FILENO);
    skriv_text("WORLDOS-SHELL:EXIT\n");
    return 0;
}
