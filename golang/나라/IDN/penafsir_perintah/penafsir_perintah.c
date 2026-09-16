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

enum { kapasitas_baris_masukan = 512, jumlah_argumen_maksimum = 16, kedalaman_berkas_perintah_maksimum = 4 };
static int kedalaman_berkas_perintah;
struct aliran_masukan {
    int deskriptor_masukan;
    char penyangga_transfer_2[256];
    size_t posisi;
    size_t panjang;
};

static size_t panjang_teks_dalam_byte(const char *teks)
{
    size_t panjang = 0;
    while (teks[panjang] != '\0')
        panjang++;
    return panjang;
}

static int teks_sama(const char *kiri, const char *kanan)
{
    size_t posisi = 0;
    while (kiri[posisi] == kanan[posisi]) {
        if (kiri[posisi] == '\0')
            return 1;
        posisi++;
    }
    return 0;
}

static void tulis_teks(const char *teks)
{
    size_t panjang = panjang_teks_dalam_byte(teks);
    while (panjang > 0U) {
        ssize_t jumlah_byte_ditulis = Tulis(STDOUT_FILENO, teks, panjang);
        if (jumlah_byte_ditulis <= 0)
            return;
        teks += jumlah_byte_ditulis;
        panjang -= (size_t)jumlah_byte_ditulis;
    }
}

static void tulis_bilangan_bulat(int nilai)
{
    char karakter_digit[16];
    unsigned int jumlah_digit;
    unsigned int besar_tanpa_tanda;

    if (nilai < 0) {
        tulis_teks("-");
        besar_tanpa_tanda = (unsigned int)(-(nilai + 1)) + 1U;
    } else {
        besar_tanpa_tanda = (unsigned int)nilai;
    }
    jumlah_digit = 0;
    do {
        karakter_digit[jumlah_digit++] = (char)('0' + besar_tanpa_tanda % 10U);
        besar_tanpa_tanda /= 10U;
    } while (besar_tanpa_tanda != 0U);
    while (jumlah_digit > 0U) {
        jumlah_digit--;
        (void)Tulis(STDOUT_FILENO, &karakter_digit[jumlah_digit], 1);
    }
}

static void laporkan_galat(const char *operasi)
{
    tulis_teks("error: ");
    tulis_teks(operasi);
    tulis_teks(" errno=");
    tulis_bilangan_bulat(errno);
    tulis_teks("\n");
}

static int baca_baris_masukan(struct aliran_masukan *masukan, char *baris_masukan, size_t kapasitas)
{
    size_t posisi = 0;
    int baris_masukan_tidak_sah = 0;
    char karakter;
    ssize_t byte_terbaca;
    if (kapasitas < 2U)
        return -2;
    for (;;) {
        if (masukan->posisi == masukan->panjang) {
            byte_terbaca = Baca(masukan->deskriptor_masukan, masukan->penyangga_transfer_2, sizeof(masukan->penyangga_transfer_2));
            if (byte_terbaca < 0) {
                if (errno == EINTR)
                    continue;
                return -1;
            }
            if (byte_terbaca == 0) {
                if (posisi == 0 && !baris_masukan_tidak_sah)
                    return -1;
                break;
            }
            masukan->panjang = (size_t)byte_terbaca;
            masukan->posisi = 0;
        }
        karakter = masukan->penyangga_transfer_2[masukan->posisi++];
        if (karakter == '\n')
            break;
        if (masukan->deskriptor_masukan == STDIN_FILENO && karakter == 4) {
            if (posisi == 0 && !baris_masukan_tidak_sah)
                return -1;
            break;
        }
        if (masukan->deskriptor_masukan == STDIN_FILENO && (karakter == 8 || karakter == 127)) {
            if (posisi > 0) {
                do {
                    posisi--;
                } while (posisi > 0 && ((unsigned char)baris_masukan[posisi] & 0xc0U) == 0x80U);
            }
            continue;
        }
        if (karakter == '\r')
            continue;
        if (karakter == '\0') {
            baris_masukan_tidak_sah = 1; /* Reject binary input; do not execute its prefix. */
            continue;
        }
        if (posisi + 1U < kapasitas)
            baris_masukan[posisi++] = karakter;
        else
            baris_masukan_tidak_sah = 1;
    }
    baris_masukan[posisi] = '\0';
    return baris_masukan_tidak_sah ? -2 : (int)posisi;
}

static int pisahkan_argumen(char *baris_masukan, char **argumen)
{
    int jumlah_argumen = 0;
    char *posisi_saat_ini = baris_masukan;
    char *posisi_keluaran = baris_masukan;

    while (*posisi_saat_ini != '\0') {
        char tanda_kutip = '\0';
        while (*posisi_saat_ini == ' ' || *posisi_saat_ini == '\t')
            posisi_saat_ini++;
        if (*posisi_saat_ini == '\0' || *posisi_saat_ini == '#')
            break;
        if (jumlah_argumen == jumlah_argumen_maksimum - 1)
            return -1;
        argumen[jumlah_argumen++] = posisi_keluaran;
        while (*posisi_saat_ini != '\0') {
            char karakter = *posisi_saat_ini++;
            if (tanda_kutip == '\0' && (karakter == ' ' || karakter == '\t'))
                break;
            if (karakter == '\\' && tanda_kutip != '\'') {
                if (*posisi_saat_ini == '\0')
                    return -1;
                *posisi_keluaran++ = *posisi_saat_ini++;
            } else if (karakter == '\'' || karakter == '"') {
                if (tanda_kutip == '\0')
                    tanda_kutip = karakter;
                else if (tanda_kutip == karakter)
                    tanda_kutip = '\0';
                else
                    *posisi_keluaran++ = karakter;
            } else {
                *posisi_keluaran++ = karakter;
            }
        }
        if (tanda_kutip != '\0')
            return -1;
        *posisi_keluaran++ = '\0';
    }
    argumen[jumlah_argumen] = (char *)0;
    return jumlah_argumen;
}

static void tampilkan_bantuan(void)
{
    size_t posisi;
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
    for (posisi = 0; posisi < sizeof(perintah_acuan) / sizeof(perintah_acuan[0]); posisi++) {
        tulis_teks(nama_perintah_setempat[posisi]);
        tulis_teks(" = ");
        tulis_teks(perintah_acuan[posisi]);
        tulis_teks("\n");
    }
}

static int perintah_cocok(const char *teks, const char *perintah)
{
    size_t posisi;
    if (teks_sama(teks, perintah))
        return 1;
    for (posisi = 0; posisi < sizeof(perintah_acuan) / sizeof(perintah_acuan[0]); posisi++)
        if (teks_sama(perintah, perintah_acuan[posisi]))
            return teks_sama(teks, nama_perintah_setempat[posisi]);
    return 0;
}

static int tafsirkan_masukan(int deskriptor_masukan);

static int tafsirkan_berkas_perintah(const char *nama_berkas)
{
    int deskriptor_berkas_2;
    int status;
    if (kedalaman_berkas_perintah >= kedalaman_berkas_perintah_maksimum) {
        tulis_teks("source: nesting limit\n");
        return 0;
    }
    deskriptor_berkas_2 = Buka(nama_berkas, O_RDONLY);
    if (deskriptor_berkas_2 < 0) {
        laporkan_galat(nama_berkas);
        return 0;
    }
    kedalaman_berkas_perintah++;
    status = tafsirkan_masukan(deskriptor_berkas_2);
    kedalaman_berkas_perintah--;
    (void)Tutup(deskriptor_berkas_2);
    return status;
}

static void tampilkan_argumen(int jumlah_argumen, char **argumen)
{
    int posisi;
    for (posisi = 1; posisi < jumlah_argumen; posisi++) {
        if (posisi != 1)
            tulis_teks(" ");
        tulis_teks(argumen[posisi]);
    }
    tulis_teks("\n");
}

static void tampilkan_direktori_kerja(void)
{
    char jalur[128];
    if (getcwd(jalur, sizeof(jalur)) == (char *)0) {
        laporkan_galat("pwd");
        return;
    }
    tulis_teks(jalur);
    tulis_teks("\n");
}

static void tampilkan_isi_berkas(const char *nama_berkas)
{
    char penyangga_transfer_2[128];
    int deskriptor_berkas_2 = Buka(nama_berkas, O_RDONLY);
    ssize_t byte_terbaca;

    if (deskriptor_berkas_2 < 0) {
        laporkan_galat("cat");
        return;
    }
    while ((byte_terbaca = Baca(deskriptor_berkas_2, penyangga_transfer_2, sizeof(penyangga_transfer_2))) > 0)
        (void)Tulis(STDOUT_FILENO, penyangga_transfer_2, (size_t)byte_terbaca);
    if (byte_terbaca < 0)
        laporkan_galat("cat/read");
    (void)Tutup(deskriptor_berkas_2);
    tulis_teks("\n");
}

static void tampilkan_informasi_berkas(const char *nama_berkas)
{
    struct stat status;
    if (stat(nama_berkas, &status) < 0) {
        laporkan_galat("stat");
        return;
    }
    tulis_teks("size=");
    tulis_bilangan_bulat((int)status.st_size);
    tulis_teks(S_ISDIR(status.st_mode) ? " type=directory\n" : " type=file\n");
}

static void tampilkan_pengenal_proses(void)
{
    tulis_teks("pid=");
    tulis_bilangan_bulat((int)getpid());
    tulis_teks(" ppid=");
    tulis_bilangan_bulat((int)getppid());
    tulis_teks("\n");
}

static void tampilkan_identitas_sistem(void)
{
    struct utsname identitas_sistem;
    if (uname(&identitas_sistem) < 0) {
        laporkan_galat("uname");
        return;
    }
    tulis_teks(identitas_sistem.sysname);
    tulis_teks(" ");
    tulis_teks(identitas_sistem.release);
    tulis_teks(" ");
    tulis_teks(identitas_sistem.machine);
    tulis_teks("\n");
}

static void jalankan_program(int jumlah_argumen, char **argumen)
{
    pid_t pengenal_proses_anak;
    int status_penghentian_proses_anak = 0;

    if (jumlah_argumen < 2) {
        tulis_teks("usage: run FILE [ARGS...]\n");
        return;
    }
    pengenal_proses_anak = fork();
    if (pengenal_proses_anak < 0) {
        laporkan_galat("fork");
        return;
    }
    if (pengenal_proses_anak == 0) {
        execve(argumen[1], &argumen[1], (char *const *)0);
        laporkan_galat("execve");
        _exit(127);
    }
    if (waitpid(pengenal_proses_anak, &status_penghentian_proses_anak, 0) < 0) {
        laporkan_galat("waitpid");
        return;
    }
    tulis_teks("exit-status=");
    tulis_bilangan_bulat(WEXITSTATUS(status_penghentian_proses_anak));
    tulis_teks("\n");
}

static void uji_pengembalian_datagram(const char *pesan)
{
    struct sockaddr_in alamat_penerima = {0};
    struct sockaddr_in alamat_pengirim = {0};
    socklen_t panjang_alamat_pengirim = sizeof(alamat_pengirim);
    char data_diterima[96];
    size_t panjang_pesan_dalam_byte = panjang_teks_dalam_byte(pesan);
    int ujung_komunikasi_penerima = -1;
    int ujung_komunikasi_pengirim = -1;
    ssize_t jumlah_byte_diterima;

    if (panjang_pesan_dalam_byte >= sizeof(data_diterima)) {
        tulis_teks("udp: message exceeds 95 bytes\n");
        return;
    }
    ujung_komunikasi_penerima = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    ujung_komunikasi_pengirim = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (ujung_komunikasi_penerima < 0 || ujung_komunikasi_pengirim < 0) {
        laporkan_galat("socket");
        goto tutup_ujung_komunikasi;
    }
    alamat_penerima.sin_family = AF_INET;
    alamat_penerima.sin_port = htons(40404);
    alamat_penerima.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    if (bind(ujung_komunikasi_penerima, (const struct sockaddr *)&alamat_penerima, sizeof(alamat_penerima)) < 0) {
        laporkan_galat("bind");
        goto tutup_ujung_komunikasi;
    }
    if (connect(ujung_komunikasi_pengirim, (const struct sockaddr *)&alamat_penerima, sizeof(alamat_penerima)) < 0) {
        laporkan_galat("connect");
        goto tutup_ujung_komunikasi;
    }
    if (send(ujung_komunikasi_pengirim, pesan, panjang_pesan_dalam_byte, 0) != (ssize_t)panjang_pesan_dalam_byte) {
        laporkan_galat("send");
        goto tutup_ujung_komunikasi;
    }
    jumlah_byte_diterima = recvfrom(ujung_komunikasi_penerima, data_diterima, sizeof(data_diterima) - 1U, 0,
                         (struct sockaddr *)&alamat_pengirim, &panjang_alamat_pengirim);
    if (jumlah_byte_diterima < 0) {
        laporkan_galat("recvfrom");
        goto tutup_ujung_komunikasi;
    }
    data_diterima[jumlah_byte_diterima] = '\0';
    tulis_teks("udp-received: ");
    tulis_teks(data_diterima);
    tulis_teks("\n");

tutup_ujung_komunikasi:
    if (ujung_komunikasi_pengirim >= 0)
        (void)Tutup(ujung_komunikasi_pengirim);
    if (ujung_komunikasi_penerima >= 0)
        (void)Tutup(ujung_komunikasi_penerima);
}

static int tafsirkan_masukan(int deskriptor_masukan)
{
    char baris_masukan[kapasitas_baris_masukan];
    char *argumen[jumlah_argumen_maksimum];
    struct aliran_masukan masukan = {0};
    masukan.deskriptor_masukan = deskriptor_masukan;

    for (;;) {
        int jumlah_argumen;
        int status;
        if (deskriptor_masukan == STDIN_FILENO)
            tulis_teks("worldos$ ");
        status = baca_baris_masukan(&masukan, baris_masukan, sizeof(baris_masukan));
        if (status == -1)
            return 0;
        if (status == -2) {
            tulis_teks("input rejected: overlong or binary line\n");
            continue;
        }
        jumlah_argumen = pisahkan_argumen(baris_masukan, argumen);
        if (jumlah_argumen < 0) {
            tulis_teks("syntax error: quote, escape or argument limit\n");
            continue;
        }
        if (jumlah_argumen == 0)
            continue;
        if (perintah_cocok(argumen[0], "help"))
            tampilkan_bantuan();
        else if (perintah_cocok(argumen[0], "echo"))
            tampilkan_argumen(jumlah_argumen, argumen);
        else if (perintah_cocok(argumen[0], "pwd"))
            tampilkan_direktori_kerja();
        else if (perintah_cocok(argumen[0], "cd")) {
            if (jumlah_argumen < 2)
                tulis_teks("usage: cd PATH\n");
            else if (chdir(argumen[1]) < 0)
                laporkan_galat("cd");
        } else if (perintah_cocok(argumen[0], "cat")) {
            if (jumlah_argumen < 2)
                tulis_teks("usage: cat FILE\n");
            else
                tampilkan_isi_berkas(argumen[1]);
        } else if (perintah_cocok(argumen[0], "stat")) {
            if (jumlah_argumen < 2)
                tulis_teks("usage: stat FILE\n");
            else
                tampilkan_informasi_berkas(argumen[1]);
        } else if (perintah_cocok(argumen[0], "pid"))
            tampilkan_pengenal_proses();
        else if (perintah_cocok(argumen[0], "uname"))
            tampilkan_identitas_sistem();
        else if (perintah_cocok(argumen[0], "run"))
            jalankan_program(jumlah_argumen, argumen);
        else if (perintah_cocok(argumen[0], "udp"))
            uji_pengembalian_datagram(jumlah_argumen >= 2 ? argumen[1] : "ping");
        else if (perintah_cocok(argumen[0], "source")) {
            if (jumlah_argumen < 2)
                tulis_teks("usage: source FILE\n");
            else if (tafsirkan_berkas_perintah(argumen[1]))
                return 1;
        } else if (perintah_cocok(argumen[0], "exit"))
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
