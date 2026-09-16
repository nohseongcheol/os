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

enum { capacità_della_riga_di_ingresso = 512, numero_massimo_di_argomenti = 16, annidamento_massimo_dei_comandi = 4 };
static int profondità_di_annidamento_dei_comandi;
struct flusso_di_ingresso {
    int descrittore_di_ingresso;
    char memoria_intermedia_di_trasferimento_2[256];
    size_t posizione;
    size_t lunghezza;
};

static size_t lunghezza_del_testo_in_ottetti(const char *testo)
{
    size_t lunghezza = 0;
    while (testo[lunghezza] != '\0')
        lunghezza++;
    return lunghezza;
}

static int testi_uguali(const char *sinistra, const char *destra)
{
    size_t posizione = 0;
    while (sinistra[posizione] == destra[posizione]) {
        if (sinistra[posizione] == '\0')
            return 1;
        posizione++;
    }
    return 0;
}

static void scrivi_testo(const char *testo)
{
    size_t lunghezza = lunghezza_del_testo_in_ottetti(testo);
    while (lunghezza > 0U) {
        ssize_t numero_di_ottetti_scritti = Scrittura(STDOUT_FILENO, testo, lunghezza);
        if (numero_di_ottetti_scritti <= 0)
            return;
        testo += numero_di_ottetti_scritti;
        lunghezza -= (size_t)numero_di_ottetti_scritti;
    }
}

static void scrivi_intero(int valore)
{
    char caratteri_delle_cifre[16];
    unsigned int numero_di_cifre;
    unsigned int grandezza_senza_segno;

    if (valore < 0) {
        scrivi_testo("-");
        grandezza_senza_segno = (unsigned int)(-(valore + 1)) + 1U;
    } else {
        grandezza_senza_segno = (unsigned int)valore;
    }
    numero_di_cifre = 0;
    do {
        caratteri_delle_cifre[numero_di_cifre++] = (char)('0' + grandezza_senza_segno % 10U);
        grandezza_senza_segno /= 10U;
    } while (grandezza_senza_segno != 0U);
    while (numero_di_cifre > 0U) {
        numero_di_cifre--;
        (void)Scrittura(STDOUT_FILENO, &caratteri_delle_cifre[numero_di_cifre], 1);
    }
}

static void segnala_errore(const char *operazione)
{
    scrivi_testo("error: ");
    scrivi_testo(operazione);
    scrivi_testo(" errno=");
    scrivi_intero(errno);
    scrivi_testo("\n");
}

static int leggi_riga_di_ingresso(struct flusso_di_ingresso *ingresso, char *riga_di_ingresso, size_t capacità)
{
    size_t posizione = 0;
    int riga_di_ingresso_non_valida = 0;
    char carattere;
    ssize_t ottetti_letti;
    if (capacità < 2U)
        return -2;
    for (;;) {
        if (ingresso->posizione == ingresso->lunghezza) {
            ottetti_letti = Lettura(ingresso->descrittore_di_ingresso, ingresso->memoria_intermedia_di_trasferimento_2, sizeof(ingresso->memoria_intermedia_di_trasferimento_2));
            if (ottetti_letti < 0) {
                if (errno == EINTR)
                    continue;
                return -1;
            }
            if (ottetti_letti == 0) {
                if (posizione == 0 && !riga_di_ingresso_non_valida)
                    return -1;
                break;
            }
            ingresso->lunghezza = (size_t)ottetti_letti;
            ingresso->posizione = 0;
        }
        carattere = ingresso->memoria_intermedia_di_trasferimento_2[ingresso->posizione++];
        if (carattere == '\n')
            break;
        if (ingresso->descrittore_di_ingresso == STDIN_FILENO && carattere == 4) {
            if (posizione == 0 && !riga_di_ingresso_non_valida)
                return -1;
            break;
        }
        if (ingresso->descrittore_di_ingresso == STDIN_FILENO && (carattere == 8 || carattere == 127)) {
            if (posizione > 0) {
                do {
                    posizione--;
                } while (posizione > 0 && ((unsigned char)riga_di_ingresso[posizione] & 0xc0U) == 0x80U);
            }
            continue;
        }
        if (carattere == '\r')
            continue;
        if (carattere == '\0') {
            riga_di_ingresso_non_valida = 1; /* Reject binary input; do not execute its prefix. */
            continue;
        }
        if (posizione + 1U < capacità)
            riga_di_ingresso[posizione++] = carattere;
        else
            riga_di_ingresso_non_valida = 1;
    }
    riga_di_ingresso[posizione] = '\0';
    return riga_di_ingresso_non_valida ? -2 : (int)posizione;
}

static int separa_argomenti(char *riga_di_ingresso, char **argomenti)
{
    int numero_di_argomenti = 0;
    char *posizione_corrente = riga_di_ingresso;
    char *posizione_di_uscita = riga_di_ingresso;

    while (*posizione_corrente != '\0') {
        char virgolette = '\0';
        while (*posizione_corrente == ' ' || *posizione_corrente == '\t')
            posizione_corrente++;
        if (*posizione_corrente == '\0' || *posizione_corrente == '#')
            break;
        if (numero_di_argomenti == numero_massimo_di_argomenti - 1)
            return -1;
        argomenti[numero_di_argomenti++] = posizione_di_uscita;
        while (*posizione_corrente != '\0') {
            char carattere = *posizione_corrente++;
            if (virgolette == '\0' && (carattere == ' ' || carattere == '\t'))
                break;
            if (carattere == '\\' && virgolette != '\'') {
                if (*posizione_corrente == '\0')
                    return -1;
                *posizione_di_uscita++ = *posizione_corrente++;
            } else if (carattere == '\'' || carattere == '"') {
                if (virgolette == '\0')
                    virgolette = carattere;
                else if (virgolette == carattere)
                    virgolette = '\0';
                else
                    *posizione_di_uscita++ = carattere;
            } else {
                *posizione_di_uscita++ = carattere;
            }
        }
        if (virgolette != '\0')
            return -1;
        *posizione_di_uscita++ = '\0';
    }
    argomenti[numero_di_argomenti] = (char *)0;
    return numero_di_argomenti;
}

static void mostra_aiuto(void)
{
    size_t posizione;
    scrivi_testo(
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
    scrivi_testo("Native command proposals (ASCII aliases remain available):\n");
    for (posizione = 0; posizione < sizeof(comandi_di_riferimento) / sizeof(comandi_di_riferimento[0]); posizione++) {
        scrivi_testo(nomi_locali_dei_comandi[posizione]);
        scrivi_testo(" = ");
        scrivi_testo(comandi_di_riferimento[posizione]);
        scrivi_testo("\n");
    }
}

static int comando_corrispondente(const char *testo, const char *comando)
{
    size_t posizione;
    if (testi_uguali(testo, comando))
        return 1;
    for (posizione = 0; posizione < sizeof(comandi_di_riferimento) / sizeof(comandi_di_riferimento[0]); posizione++)
        if (testi_uguali(comando, comandi_di_riferimento[posizione]))
            return testi_uguali(testo, nomi_locali_dei_comandi[posizione]);
    return 0;
}

static int interpreta_ingresso(int descrittore_di_ingresso);

static int interpreta_file_di_comandi(const char *nome_del_file)
{
    int descrittore_del_file_2;
    int stato;
    if (profondità_di_annidamento_dei_comandi >= annidamento_massimo_dei_comandi) {
        scrivi_testo("source: nesting limit\n");
        return 0;
    }
    descrittore_del_file_2 = Apri(nome_del_file, O_RDONLY);
    if (descrittore_del_file_2 < 0) {
        segnala_errore(nome_del_file);
        return 0;
    }
    profondità_di_annidamento_dei_comandi++;
    stato = interpreta_ingresso(descrittore_del_file_2);
    profondità_di_annidamento_dei_comandi--;
    (void)Chiudi(descrittore_del_file_2);
    return stato;
}

static void mostra_argomenti(int numero_di_argomenti, char **argomenti)
{
    int posizione;
    for (posizione = 1; posizione < numero_di_argomenti; posizione++) {
        if (posizione != 1)
            scrivi_testo(" ");
        scrivi_testo(argomenti[posizione]);
    }
    scrivi_testo("\n");
}

static void mostra_cartella_corrente(void)
{
    char percorso[128];
    if (getcwd(percorso, sizeof(percorso)) == (char *)0) {
        segnala_errore("pwd");
        return;
    }
    scrivi_testo(percorso);
    scrivi_testo("\n");
}

static void mostra_contenuto_del_file(const char *nome_del_file)
{
    char memoria_intermedia_di_trasferimento_2[128];
    int descrittore_del_file_2 = Apri(nome_del_file, O_RDONLY);
    ssize_t ottetti_letti;

    if (descrittore_del_file_2 < 0) {
        segnala_errore("cat");
        return;
    }
    while ((ottetti_letti = Lettura(descrittore_del_file_2, memoria_intermedia_di_trasferimento_2, sizeof(memoria_intermedia_di_trasferimento_2))) > 0)
        (void)Scrittura(STDOUT_FILENO, memoria_intermedia_di_trasferimento_2, (size_t)ottetti_letti);
    if (ottetti_letti < 0)
        segnala_errore("cat/read");
    (void)Chiudi(descrittore_del_file_2);
    scrivi_testo("\n");
}

static void mostra_informazioni_del_file(const char *nome_del_file)
{
    struct stat stato;
    if (stat(nome_del_file, &stato) < 0) {
        segnala_errore("stat");
        return;
    }
    scrivi_testo("size=");
    scrivi_intero((int)stato.st_size);
    scrivi_testo(S_ISDIR(stato.st_mode) ? " type=directory\n" : " type=file\n");
}

static void mostra_identificatori_dei_processi(void)
{
    scrivi_testo("pid=");
    scrivi_intero((int)getpid());
    scrivi_testo(" ppid=");
    scrivi_intero((int)getppid());
    scrivi_testo("\n");
}

static void mostra_identità_del_sistema(void)
{
    struct utsname identità_del_sistema;
    if (uname(&identità_del_sistema) < 0) {
        segnala_errore("uname");
        return;
    }
    scrivi_testo(identità_del_sistema.sysname);
    scrivi_testo(" ");
    scrivi_testo(identità_del_sistema.release);
    scrivi_testo(" ");
    scrivi_testo(identità_del_sistema.machine);
    scrivi_testo("\n");
}

static void esegui_programma(int numero_di_argomenti, char **argomenti)
{
    pid_t identificatore_del_processo_figlio;
    int stato_di_terminazione_del_figlio = 0;

    if (numero_di_argomenti < 2) {
        scrivi_testo("usage: run FILE [ARGS...]\n");
        return;
    }
    identificatore_del_processo_figlio = fork();
    if (identificatore_del_processo_figlio < 0) {
        segnala_errore("fork");
        return;
    }
    if (identificatore_del_processo_figlio == 0) {
        execve(argomenti[1], &argomenti[1], (char *const *)0);
        segnala_errore("execve");
        _exit(127);
    }
    if (waitpid(identificatore_del_processo_figlio, &stato_di_terminazione_del_figlio, 0) < 0) {
        segnala_errore("waitpid");
        return;
    }
    scrivi_testo("exit-status=");
    scrivi_intero(WEXITSTATUS(stato_di_terminazione_del_figlio));
    scrivi_testo("\n");
}

static void verifica_ritorno_del_datagramma(const char *messaggio)
{
    struct sockaddr_in indirizzo_ricevente = {0};
    struct sockaddr_in indirizzo_del_mittente = {0};
    socklen_t lunghezza_dell_indirizzo_del_mittente = sizeof(indirizzo_del_mittente);
    char dati_ricevuti[96];
    size_t lunghezza_del_messaggio_in_ottetti = lunghezza_del_testo_in_ottetti(messaggio);
    int estremità_ricevente = -1;
    int estremità_trasmittente = -1;
    ssize_t numero_di_ottetti_ricevuti;

    if (lunghezza_del_messaggio_in_ottetti >= sizeof(dati_ricevuti)) {
        scrivi_testo("udp: message exceeds 95 bytes\n");
        return;
    }
    estremità_ricevente = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    estremità_trasmittente = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (estremità_ricevente < 0 || estremità_trasmittente < 0) {
        segnala_errore("socket");
        goto chiudi_estremità_di_comunicazione;
    }
    indirizzo_ricevente.sin_family = AF_INET;
    indirizzo_ricevente.sin_port = htons(40404);
    indirizzo_ricevente.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    if (bind(estremità_ricevente, (const struct sockaddr *)&indirizzo_ricevente, sizeof(indirizzo_ricevente)) < 0) {
        segnala_errore("bind");
        goto chiudi_estremità_di_comunicazione;
    }
    if (connect(estremità_trasmittente, (const struct sockaddr *)&indirizzo_ricevente, sizeof(indirizzo_ricevente)) < 0) {
        segnala_errore("connect");
        goto chiudi_estremità_di_comunicazione;
    }
    if (send(estremità_trasmittente, messaggio, lunghezza_del_messaggio_in_ottetti, 0) != (ssize_t)lunghezza_del_messaggio_in_ottetti) {
        segnala_errore("send");
        goto chiudi_estremità_di_comunicazione;
    }
    numero_di_ottetti_ricevuti = recvfrom(estremità_ricevente, dati_ricevuti, sizeof(dati_ricevuti) - 1U, 0,
                         (struct sockaddr *)&indirizzo_del_mittente, &lunghezza_dell_indirizzo_del_mittente);
    if (numero_di_ottetti_ricevuti < 0) {
        segnala_errore("recvfrom");
        goto chiudi_estremità_di_comunicazione;
    }
    dati_ricevuti[numero_di_ottetti_ricevuti] = '\0';
    scrivi_testo("udp-received: ");
    scrivi_testo(dati_ricevuti);
    scrivi_testo("\n");

chiudi_estremità_di_comunicazione:
    if (estremità_trasmittente >= 0)
        (void)Chiudi(estremità_trasmittente);
    if (estremità_ricevente >= 0)
        (void)Chiudi(estremità_ricevente);
}

static int interpreta_ingresso(int descrittore_di_ingresso)
{
    char riga_di_ingresso[capacità_della_riga_di_ingresso];
    char *argomenti[numero_massimo_di_argomenti];
    struct flusso_di_ingresso ingresso = {0};
    ingresso.descrittore_di_ingresso = descrittore_di_ingresso;

    for (;;) {
        int numero_di_argomenti;
        int stato;
        if (descrittore_di_ingresso == STDIN_FILENO)
            scrivi_testo("worldos$ ");
        stato = leggi_riga_di_ingresso(&ingresso, riga_di_ingresso, sizeof(riga_di_ingresso));
        if (stato == -1)
            return 0;
        if (stato == -2) {
            scrivi_testo("input rejected: overlong or binary line\n");
            continue;
        }
        numero_di_argomenti = separa_argomenti(riga_di_ingresso, argomenti);
        if (numero_di_argomenti < 0) {
            scrivi_testo("syntax error: quote, escape or argument limit\n");
            continue;
        }
        if (numero_di_argomenti == 0)
            continue;
        if (comando_corrispondente(argomenti[0], "help"))
            mostra_aiuto();
        else if (comando_corrispondente(argomenti[0], "echo"))
            mostra_argomenti(numero_di_argomenti, argomenti);
        else if (comando_corrispondente(argomenti[0], "pwd"))
            mostra_cartella_corrente();
        else if (comando_corrispondente(argomenti[0], "cd")) {
            if (numero_di_argomenti < 2)
                scrivi_testo("usage: cd PATH\n");
            else if (chdir(argomenti[1]) < 0)
                segnala_errore("cd");
        } else if (comando_corrispondente(argomenti[0], "cat")) {
            if (numero_di_argomenti < 2)
                scrivi_testo("usage: cat FILE\n");
            else
                mostra_contenuto_del_file(argomenti[1]);
        } else if (comando_corrispondente(argomenti[0], "stat")) {
            if (numero_di_argomenti < 2)
                scrivi_testo("usage: stat FILE\n");
            else
                mostra_informazioni_del_file(argomenti[1]);
        } else if (comando_corrispondente(argomenti[0], "pid"))
            mostra_identificatori_dei_processi();
        else if (comando_corrispondente(argomenti[0], "uname"))
            mostra_identità_del_sistema();
        else if (comando_corrispondente(argomenti[0], "run"))
            esegui_programma(numero_di_argomenti, argomenti);
        else if (comando_corrispondente(argomenti[0], "udp"))
            verifica_ritorno_del_datagramma(numero_di_argomenti >= 2 ? argomenti[1] : "ping");
        else if (comando_corrispondente(argomenti[0], "source")) {
            if (numero_di_argomenti < 2)
                scrivi_testo("usage: source FILE\n");
            else if (interpreta_file_di_comandi(argomenti[1]))
                return 1;
        } else if (comando_corrispondente(argomenti[0], "exit"))
            return 1;
        else
            scrivi_testo("unknown command; type help\n");
    }
}

int main(void)
{
    scrivi_testo("WORLDOS-SHELL:READY\n");
    (void)interpreta_ingresso(STDIN_FILENO);
    scrivi_testo("WORLDOS-SHELL:EXIT\n");
    return 0;
}
