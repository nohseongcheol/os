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

enum { kapasiti_baris_masukan = 512, bilangan_argumen_maksimum = 16, kedalaman_fail_perintah_maksimum = 4 };
static int kedalaman_fail_perintah;
struct aliran_masukan {
    int pemerihal_masukan;
    char penimbal_pemindahan[256];
    size_t kedudukan;
    size_t panjang;
};

static size_t panjang_teks_dalam_bait(const char *teks)
{
    size_t panjang = 0;
    while (teks[panjang] != '\0')
        panjang++;
    return panjang;
}

static int teks_sama(const char *kiri, const char *kanan)
{
    size_t kedudukan = 0;
    while (kiri[kedudukan] == kanan[kedudukan]) {
        if (kiri[kedudukan] == '\0')
            return 1;
        kedudukan++;
    }
    return 0;
}

static void tulis_teks(const char *teks)
{
    size_t panjang = panjang_teks_dalam_bait(teks);
    while (panjang > 0U) {
        ssize_t bilangan_bait_ditulis = Tulis(STDOUT_FILENO, teks, panjang);
        if (bilangan_bait_ditulis <= 0)
            return;
        teks += bilangan_bait_ditulis;
        panjang -= (size_t)bilangan_bait_ditulis;
    }
}

static void tulis_nombor_bulat(int nilai)
{
    char aksara_digit[16];
    unsigned int bilangan_digit;
    unsigned int magnitud_tanpa_tanda;

    if (nilai < 0) {
        tulis_teks("-");
        magnitud_tanpa_tanda = (unsigned int)(-(nilai + 1)) + 1U;
    } else {
        magnitud_tanpa_tanda = (unsigned int)nilai;
    }
    bilangan_digit = 0;
    do {
        aksara_digit[bilangan_digit++] = (char)('0' + magnitud_tanpa_tanda % 10U);
        magnitud_tanpa_tanda /= 10U;
    } while (magnitud_tanpa_tanda != 0U);
    while (bilangan_digit > 0U) {
        bilangan_digit--;
        (void)Tulis(STDOUT_FILENO, &aksara_digit[bilangan_digit], 1);
    }
}

static void laporkan_ralat(const char *operasi)
{
    tulis_teks("error: ");
    tulis_teks(operasi);
    tulis_teks(" errno=");
    tulis_nombor_bulat(errno);
    tulis_teks("\n");
}

static int baca_baris_masukan(struct aliran_masukan *masukan, char *baris_masukan, size_t kapasiti)
{
    size_t kedudukan = 0;
    int baris_masukan_tidak_sah = 0;
    char aksara;
    ssize_t bait_dibaca;
    if (kapasiti < 2U)
        return -2;
    for (;;) {
        if (masukan->kedudukan == masukan->panjang) {
            bait_dibaca = Baca(masukan->pemerihal_masukan, masukan->penimbal_pemindahan, sizeof(masukan->penimbal_pemindahan));
            if (bait_dibaca < 0) {
                if (errno == EINTR)
                    continue;
                return -1;
            }
            if (bait_dibaca == 0) {
                if (kedudukan == 0 && !baris_masukan_tidak_sah)
                    return -1;
                break;
            }
            masukan->panjang = (size_t)bait_dibaca;
            masukan->kedudukan = 0;
        }
        aksara = masukan->penimbal_pemindahan[masukan->kedudukan++];
        if (aksara == '\n')
            break;
        if (masukan->pemerihal_masukan == STDIN_FILENO && aksara == 4) {
            if (kedudukan == 0 && !baris_masukan_tidak_sah)
                return -1;
            break;
        }
        if (masukan->pemerihal_masukan == STDIN_FILENO && (aksara == 8 || aksara == 127)) {
            if (kedudukan > 0) {
                do {
                    kedudukan--;
                } while (kedudukan > 0 && ((unsigned char)baris_masukan[kedudukan] & 0xc0U) == 0x80U);
            }
            continue;
        }
        if (aksara == '\r')
            continue;
        if (aksara == '\0') {
            baris_masukan_tidak_sah = 1; /* Reject binary input; do not execute its prefix. */
            continue;
        }
        if (kedudukan + 1U < kapasiti)
            baris_masukan[kedudukan++] = aksara;
        else
            baris_masukan_tidak_sah = 1;
    }
    baris_masukan[kedudukan] = '\0';
    return baris_masukan_tidak_sah ? -2 : (int)kedudukan;
}

static int pisahkan_argumen(char *baris_masukan, char **argumen)
{
    int bilangan_argumen = 0;
    char *kedudukan_semasa = baris_masukan;
    char *kedudukan_keluaran = baris_masukan;

    while (*kedudukan_semasa != '\0') {
        char tanda_petik = '\0';
        while (*kedudukan_semasa == ' ' || *kedudukan_semasa == '\t')
            kedudukan_semasa++;
        if (*kedudukan_semasa == '\0' || *kedudukan_semasa == '#')
            break;
        if (bilangan_argumen == bilangan_argumen_maksimum - 1)
            return -1;
        argumen[bilangan_argumen++] = kedudukan_keluaran;
        while (*kedudukan_semasa != '\0') {
            char aksara = *kedudukan_semasa++;
            if (tanda_petik == '\0' && (aksara == ' ' || aksara == '\t'))
                break;
            if (aksara == '\\' && tanda_petik != '\'') {
                if (*kedudukan_semasa == '\0')
                    return -1;
                *kedudukan_keluaran++ = *kedudukan_semasa++;
            } else if (aksara == '\'' || aksara == '"') {
                if (tanda_petik == '\0')
                    tanda_petik = aksara;
                else if (tanda_petik == aksara)
                    tanda_petik = '\0';
                else
                    *kedudukan_keluaran++ = aksara;
            } else {
                *kedudukan_keluaran++ = aksara;
            }
        }
        if (tanda_petik != '\0')
            return -1;
        *kedudukan_keluaran++ = '\0';
    }
    argumen[bilangan_argumen] = (char *)0;
    return bilangan_argumen;
}

static void paparkan_bantuan(void)
{
    size_t kedudukan;
    tulis_teks(
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
    tulis_teks("Native command proposals (ASCII aliases remain available):\n");
    for (kedudukan = 0; kedudukan < sizeof(perintah_rujukan) / sizeof(perintah_rujukan[0]); kedudukan++) {
        tulis_teks(nama_perintah_tempatan[kedudukan]);
        tulis_teks(" = ");
        tulis_teks(perintah_rujukan[kedudukan]);
        tulis_teks("\n");
    }
}

static int perintah_sepadan(const char *teks, const char *perintah)
{
    size_t kedudukan;
    if (teks_sama(teks, perintah))
        return 1;
    for (kedudukan = 0; kedudukan < sizeof(perintah_rujukan) / sizeof(perintah_rujukan[0]); kedudukan++)
        if (teks_sama(perintah, perintah_rujukan[kedudukan]))
            return teks_sama(teks, nama_perintah_tempatan[kedudukan]);
    return 0;
}

static int tafsirkan_masukan(int pemerihal_masukan);

static int tafsirkan_fail_perintah(const char *nama_fail)
{
    int pemerihal_fail;
    int keadaan;
    if (kedalaman_fail_perintah >= kedalaman_fail_perintah_maksimum) {
        tulis_teks("source: nesting limit\n");
        return 0;
    }
    pemerihal_fail = Buka(nama_fail, O_RDONLY);
    if (pemerihal_fail < 0) {
        laporkan_ralat(nama_fail);
        return 0;
    }
    kedalaman_fail_perintah++;
    keadaan = tafsirkan_masukan(pemerihal_fail);
    kedalaman_fail_perintah--;
    (void)Tutup(pemerihal_fail);
    return keadaan;
}

static void paparkan_argumen(int bilangan_argumen, char **argumen)
{
    int kedudukan;
    for (kedudukan = 1; kedudukan < bilangan_argumen; kedudukan++) {
        if (kedudukan != 1)
            tulis_teks(" ");
        tulis_teks(argumen[kedudukan]);
    }
    tulis_teks("\n");
}

static void paparkan_direktori_semasa(void)
{
    char laluan[128];
    if (getcwd(laluan, sizeof(laluan)) == (char *)0) {
        laporkan_ralat("pwd");
        return;
    }
    tulis_teks(laluan);
    tulis_teks("\n");
}

static void paparkan_kandungan_fail(const char *nama_fail)
{
    char penimbal_pemindahan[128];
    int pemerihal_fail = Buka(nama_fail, O_RDONLY);
    ssize_t bait_dibaca;

    if (pemerihal_fail < 0) {
        laporkan_ralat("cat");
        return;
    }
    while ((bait_dibaca = Baca(pemerihal_fail, penimbal_pemindahan, sizeof(penimbal_pemindahan))) > 0)
        (void)Tulis(STDOUT_FILENO, penimbal_pemindahan, (size_t)bait_dibaca);
    if (bait_dibaca < 0)
        laporkan_ralat("cat/read");
    (void)Tutup(pemerihal_fail);
    tulis_teks("\n");
}

static void paparkan_maklumat_fail(const char *nama_fail)
{
    struct stat keadaan;
    if (stat(nama_fail, &keadaan) < 0) {
        laporkan_ralat("stat");
        return;
    }
    tulis_teks("size=");
    tulis_nombor_bulat((int)keadaan.st_size);
    tulis_teks(S_ISDIR(keadaan.st_mode) ? " type=directory\n" : " type=file\n");
}

static void paparkan_pengenal_proses(void)
{
    tulis_teks("pid=");
    tulis_nombor_bulat((int)getpid());
    tulis_teks(" ppid=");
    tulis_nombor_bulat((int)getppid());
    tulis_teks("\n");
}

static void paparkan_identiti_sistem(void)
{
    struct utsname identiti_sistem;
    if (uname(&identiti_sistem) < 0) {
        laporkan_ralat("uname");
        return;
    }
    tulis_teks(identiti_sistem.sysname);
    tulis_teks(" ");
    tulis_teks(identiti_sistem.release);
    tulis_teks(" ");
    tulis_teks(identiti_sistem.machine);
    tulis_teks("\n");
}

static void jalankan_atur_cara(int bilangan_argumen, char **argumen)
{
    pid_t pengenal_proses_anak;
    int keadaan_penamatan_proses_anak = 0;

    if (bilangan_argumen < 2) {
        tulis_teks("usage: run FILE [ARGS...]\n");
        return;
    }
    pengenal_proses_anak = fork();
    if (pengenal_proses_anak < 0) {
        laporkan_ralat("fork");
        return;
    }
    if (pengenal_proses_anak == 0) {
        execve(argumen[1], &argumen[1], (char *const *)0);
        laporkan_ralat("execve");
        _exit(127);
    }
    if (waitpid(pengenal_proses_anak, &keadaan_penamatan_proses_anak, 0) < 0) {
        laporkan_ralat("waitpid");
        return;
    }
    tulis_teks("exit-status=");
    tulis_nombor_bulat(WEXITSTATUS(keadaan_penamatan_proses_anak));
    tulis_teks("\n");
}

static void uji_pengembalian_datagram(const char *mesej)
{
    struct sockaddr_in alamat_penerima = {0};
    struct sockaddr_in alamat_penghantar = {0};
    socklen_t panjang_alamat_penghantar = sizeof(alamat_penghantar);
    char data_diterima[96];
    size_t panjang_mesej_dalam_bait = panjang_teks_dalam_bait(mesej);
    int hujung_komunikasi_penerima = -1;
    int hujung_komunikasi_penghantar = -1;
    ssize_t bilangan_bait_diterima;

    if (panjang_mesej_dalam_bait >= sizeof(data_diterima)) {
        tulis_teks("udp: message exceeds 95 bytes\n");
        return;
    }
    hujung_komunikasi_penerima = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    hujung_komunikasi_penghantar = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (hujung_komunikasi_penerima < 0 || hujung_komunikasi_penghantar < 0) {
        laporkan_ralat("socket");
        goto tutup_hujung_komunikasi;
    }
    alamat_penerima.sin_family = AF_INET;
    alamat_penerima.sin_port = htons(40404);
    alamat_penerima.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    if (bind(hujung_komunikasi_penerima, (const struct sockaddr *)&alamat_penerima, sizeof(alamat_penerima)) < 0) {
        laporkan_ralat("bind");
        goto tutup_hujung_komunikasi;
    }
    if (connect(hujung_komunikasi_penghantar, (const struct sockaddr *)&alamat_penerima, sizeof(alamat_penerima)) < 0) {
        laporkan_ralat("connect");
        goto tutup_hujung_komunikasi;
    }
    if (send(hujung_komunikasi_penghantar, mesej, panjang_mesej_dalam_bait, 0) != (ssize_t)panjang_mesej_dalam_bait) {
        laporkan_ralat("send");
        goto tutup_hujung_komunikasi;
    }
    bilangan_bait_diterima = recvfrom(hujung_komunikasi_penerima, data_diterima, sizeof(data_diterima) - 1U, 0,
                         (struct sockaddr *)&alamat_penghantar, &panjang_alamat_penghantar);
    if (bilangan_bait_diterima < 0) {
        laporkan_ralat("recvfrom");
        goto tutup_hujung_komunikasi;
    }
    data_diterima[bilangan_bait_diterima] = '\0';
    tulis_teks("udp-received: ");
    tulis_teks(data_diterima);
    tulis_teks("\n");

tutup_hujung_komunikasi:
    if (hujung_komunikasi_penghantar >= 0)
        (void)Tutup(hujung_komunikasi_penghantar);
    if (hujung_komunikasi_penerima >= 0)
        (void)Tutup(hujung_komunikasi_penerima);
}

static int tafsirkan_masukan(int pemerihal_masukan)
{
    char baris_masukan[kapasiti_baris_masukan];
    char *argumen[bilangan_argumen_maksimum];
    struct aliran_masukan masukan = {0};
    masukan.pemerihal_masukan = pemerihal_masukan;

    for (;;) {
        int bilangan_argumen;
        int keadaan;
        if (pemerihal_masukan == STDIN_FILENO)
            tulis_teks("worldos$ ");
        keadaan = baca_baris_masukan(&masukan, baris_masukan, sizeof(baris_masukan));
        if (keadaan == -1)
            return 0;
        if (keadaan == -2) {
            tulis_teks("input rejected: overlong or binary line\n");
            continue;
        }
        bilangan_argumen = pisahkan_argumen(baris_masukan, argumen);
        if (bilangan_argumen < 0) {
            tulis_teks("syntax error: quote, escape or argument limit\n");
            continue;
        }
        if (bilangan_argumen == 0)
            continue;
        if (perintah_sepadan(argumen[0], "help"))
            paparkan_bantuan();
        else if (perintah_sepadan(argumen[0], "echo"))
            paparkan_argumen(bilangan_argumen, argumen);
        else if (perintah_sepadan(argumen[0], "pwd"))
            paparkan_direktori_semasa();
        else if (perintah_sepadan(argumen[0], "cd")) {
            if (bilangan_argumen < 2)
                tulis_teks("usage: cd PATH\n");
            else if (chdir(argumen[1]) < 0)
                laporkan_ralat("cd");
        } else if (perintah_sepadan(argumen[0], "cat")) {
            if (bilangan_argumen < 2)
                tulis_teks("usage: cat FILE\n");
            else
                paparkan_kandungan_fail(argumen[1]);
        } else if (perintah_sepadan(argumen[0], "stat")) {
            if (bilangan_argumen < 2)
                tulis_teks("usage: stat FILE\n");
            else
                paparkan_maklumat_fail(argumen[1]);
        } else if (perintah_sepadan(argumen[0], "pid"))
            paparkan_pengenal_proses();
        else if (perintah_sepadan(argumen[0], "uname"))
            paparkan_identiti_sistem();
        else if (perintah_sepadan(argumen[0], "run"))
            jalankan_atur_cara(bilangan_argumen, argumen);
        else if (perintah_sepadan(argumen[0], "udp"))
            uji_pengembalian_datagram(bilangan_argumen >= 2 ? argumen[1] : "ping");
        else if (perintah_sepadan(argumen[0], "source")) {
            if (bilangan_argumen < 2)
                tulis_teks("usage: source FILE\n");
            else if (tafsirkan_fail_perintah(argumen[1]))
                return 1;
        } else if (perintah_sepadan(argumen[0], "exit"))
            return 1;
        else
            tulis_teks("unknown command; type help\n");
    }
}

int main(void)
{
    tulis_teks("WORLDOS-SHELL:READY\n");
    (void)tafsirkan_masukan(STDIN_FILENO);
    tulis_teks("WORLDOS-SHELL:EXIT\n");
    return 0;
}
