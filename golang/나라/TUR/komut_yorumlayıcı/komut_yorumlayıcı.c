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

enum { girdi_satırı_kapasitesi = 512, en_fazla_bağımsız_değişken_sayısı = 16, en_fazla_komut_dosyası_iç_içeliği = 4 };
static int komut_dosyası_iç_içelik_derinliği;
struct girdi_akışı {
    int girdi_tanımlayıcısı;
    char aktarım_ara_belleği_2[256];
    size_t konum;
    size_t uzunluk;
};

static size_t metnin_bayt_uzunluğu(const char *metin)
{
    size_t uzunluk = 0;
    while (metin[uzunluk] != '\0')
        uzunluk++;
    return uzunluk;
}

static int metinler_eşit(const char *sol, const char *sağ)
{
    size_t konum = 0;
    while (sol[konum] == sağ[konum]) {
        if (sol[konum] == '\0')
            return 1;
        konum++;
    }
    return 0;
}

static void metin_yaz(const char *metin)
{
    size_t uzunluk = metnin_bayt_uzunluğu(metin);
    while (uzunluk > 0U) {
        ssize_t yazılan_bayt_sayısı = Yazma(STDOUT_FILENO, metin, uzunluk);
        if (yazılan_bayt_sayısı <= 0)
            return;
        metin += yazılan_bayt_sayısı;
        uzunluk -= (size_t)yazılan_bayt_sayısı;
    }
}

static void tam_sayı_yaz(int değer)
{
    char rakam_karakterleri[16];
    unsigned int rakam_sayısı;
    unsigned int işaretsiz_büyüklük;

    if (değer < 0) {
        metin_yaz("-");
        işaretsiz_büyüklük = (unsigned int)(-(değer + 1)) + 1U;
    } else {
        işaretsiz_büyüklük = (unsigned int)değer;
    }
    rakam_sayısı = 0;
    do {
        rakam_karakterleri[rakam_sayısı++] = (char)('0' + işaretsiz_büyüklük % 10U);
        işaretsiz_büyüklük /= 10U;
    } while (işaretsiz_büyüklük != 0U);
    while (rakam_sayısı > 0U) {
        rakam_sayısı--;
        (void)Yazma(STDOUT_FILENO, &rakam_karakterleri[rakam_sayısı], 1);
    }
}

static void hata_bildir(const char *işlem)
{
    metin_yaz("error: ");
    metin_yaz(işlem);
    metin_yaz(" errno=");
    tam_sayı_yaz(errno);
    metin_yaz("\n");
}

static int girdi_satırını_oku(struct girdi_akışı *girdi, char *girdi_satırı, size_t kapasite)
{
    size_t konum = 0;
    int geçersiz_girdi_satırı = 0;
    char karakter;
    ssize_t okunan_baytlar;
    if (kapasite < 2U)
        return -2;
    for (;;) {
        if (girdi->konum == girdi->uzunluk) {
            okunan_baytlar = Okuma(girdi->girdi_tanımlayıcısı, girdi->aktarım_ara_belleği_2, sizeof(girdi->aktarım_ara_belleği_2));
            if (okunan_baytlar < 0) {
                if (errno == EINTR)
                    continue;
                return -1;
            }
            if (okunan_baytlar == 0) {
                if (konum == 0 && !geçersiz_girdi_satırı)
                    return -1;
                break;
            }
            girdi->uzunluk = (size_t)okunan_baytlar;
            girdi->konum = 0;
        }
        karakter = girdi->aktarım_ara_belleği_2[girdi->konum++];
        if (karakter == '\n')
            break;
        if (girdi->girdi_tanımlayıcısı == STDIN_FILENO && karakter == 4) {
            if (konum == 0 && !geçersiz_girdi_satırı)
                return -1;
            break;
        }
        if (girdi->girdi_tanımlayıcısı == STDIN_FILENO && (karakter == 8 || karakter == 127)) {
            if (konum > 0) {
                do {
                    konum--;
                } while (konum > 0 && ((unsigned char)girdi_satırı[konum] & 0xc0U) == 0x80U);
            }
            continue;
        }
        if (karakter == '\r')
            continue;
        if (karakter == '\0') {
            geçersiz_girdi_satırı = 1; /* Reject binary input; do not execute its prefix. */
            continue;
        }
        if (konum + 1U < kapasite)
            girdi_satırı[konum++] = karakter;
        else
            geçersiz_girdi_satırı = 1;
    }
    girdi_satırı[konum] = '\0';
    return geçersiz_girdi_satırı ? -2 : (int)konum;
}

static int bağımsız_değişkenleri_ayır(char *girdi_satırı, char **bağımsız_değişkenler)
{
    int bağımsız_değişken_sayısı = 0;
    char *geçerli_konum = girdi_satırı;
    char *çıktı_konumu = girdi_satırı;

    while (*geçerli_konum != '\0') {
        char tırnak = '\0';
        while (*geçerli_konum == ' ' || *geçerli_konum == '\t')
            geçerli_konum++;
        if (*geçerli_konum == '\0' || *geçerli_konum == '#')
            break;
        if (bağımsız_değişken_sayısı == en_fazla_bağımsız_değişken_sayısı - 1)
            return -1;
        bağımsız_değişkenler[bağımsız_değişken_sayısı++] = çıktı_konumu;
        while (*geçerli_konum != '\0') {
            char karakter = *geçerli_konum++;
            if (tırnak == '\0' && (karakter == ' ' || karakter == '\t'))
                break;
            if (karakter == '\\' && tırnak != '\'') {
                if (*geçerli_konum == '\0')
                    return -1;
                *çıktı_konumu++ = *geçerli_konum++;
            } else if (karakter == '\'' || karakter == '"') {
                if (tırnak == '\0')
                    tırnak = karakter;
                else if (tırnak == karakter)
                    tırnak = '\0';
                else
                    *çıktı_konumu++ = karakter;
            } else {
                *çıktı_konumu++ = karakter;
            }
        }
        if (tırnak != '\0')
            return -1;
        *çıktı_konumu++ = '\0';
    }
    bağımsız_değişkenler[bağımsız_değişken_sayısı] = (char *)0;
    return bağımsız_değişken_sayısı;
}

static void yardım_göster(void)
{
    size_t konum;
    metin_yaz(
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
    metin_yaz("Native command proposals (ASCII aliases remain available):\n");
    for (konum = 0; konum < sizeof(temel_komutlar) / sizeof(temel_komutlar[0]); konum++) {
        metin_yaz(yerel_komut_adları[konum]);
        metin_yaz(" = ");
        metin_yaz(temel_komutlar[konum]);
        metin_yaz("\n");
    }
}

static int komut_eşleşiyor(const char *metin, const char *komut)
{
    size_t konum;
    if (metinler_eşit(metin, komut))
        return 1;
    for (konum = 0; konum < sizeof(temel_komutlar) / sizeof(temel_komutlar[0]); konum++)
        if (metinler_eşit(komut, temel_komutlar[konum]))
            return metinler_eşit(metin, yerel_komut_adları[konum]);
    return 0;
}

static int girdiyi_yorumla(int girdi_tanımlayıcısı);

static int komut_dosyasını_yorumla(const char *dosya_adı)
{
    int dosya_tanımlayıcısı_2;
    int durum;
    if (komut_dosyası_iç_içelik_derinliği >= en_fazla_komut_dosyası_iç_içeliği) {
        metin_yaz("source: nesting limit\n");
        return 0;
    }
    dosya_tanımlayıcısı_2 = Aç(dosya_adı, O_RDONLY);
    if (dosya_tanımlayıcısı_2 < 0) {
        hata_bildir(dosya_adı);
        return 0;
    }
    komut_dosyası_iç_içelik_derinliği++;
    durum = girdiyi_yorumla(dosya_tanımlayıcısı_2);
    komut_dosyası_iç_içelik_derinliği--;
    (void)Kapat(dosya_tanımlayıcısı_2);
    return durum;
}

static void bağımsız_değişkenleri_göster(int bağımsız_değişken_sayısı, char **bağımsız_değişkenler)
{
    int konum;
    for (konum = 1; konum < bağımsız_değişken_sayısı; konum++) {
        if (konum != 1)
            metin_yaz(" ");
        metin_yaz(bağımsız_değişkenler[konum]);
    }
    metin_yaz("\n");
}

static void çalışma_dizinini_göster(void)
{
    char yol[128];
    if (getcwd(yol, sizeof(yol)) == (char *)0) {
        hata_bildir("pwd");
        return;
    }
    metin_yaz(yol);
    metin_yaz("\n");
}

static void dosya_içeriğini_göster(const char *dosya_adı)
{
    char aktarım_ara_belleği_2[128];
    int dosya_tanımlayıcısı_2 = Aç(dosya_adı, O_RDONLY);
    ssize_t okunan_baytlar;

    if (dosya_tanımlayıcısı_2 < 0) {
        hata_bildir("cat");
        return;
    }
    while ((okunan_baytlar = Okuma(dosya_tanımlayıcısı_2, aktarım_ara_belleği_2, sizeof(aktarım_ara_belleği_2))) > 0)
        (void)Yazma(STDOUT_FILENO, aktarım_ara_belleği_2, (size_t)okunan_baytlar);
    if (okunan_baytlar < 0)
        hata_bildir("cat/read");
    (void)Kapat(dosya_tanımlayıcısı_2);
    metin_yaz("\n");
}

static void dosya_bilgilerini_göster(const char *dosya_adı)
{
    struct stat durum;
    if (stat(dosya_adı, &durum) < 0) {
        hata_bildir("stat");
        return;
    }
    metin_yaz("size=");
    tam_sayı_yaz((int)durum.st_size);
    metin_yaz(S_ISDIR(durum.st_mode) ? " type=directory\n" : " type=file\n");
}

static void süreç_kimliklerini_göster(void)
{
    metin_yaz("pid=");
    tam_sayı_yaz((int)getpid());
    metin_yaz(" ppid=");
    tam_sayı_yaz((int)getppid());
    metin_yaz("\n");
}

static void sistem_kimliğini_göster(void)
{
    struct utsname sistem_kimliği;
    if (uname(&sistem_kimliği) < 0) {
        hata_bildir("uname");
        return;
    }
    metin_yaz(sistem_kimliği.sysname);
    metin_yaz(" ");
    metin_yaz(sistem_kimliği.release);
    metin_yaz(" ");
    metin_yaz(sistem_kimliği.machine);
    metin_yaz("\n");
}

static void programı_çalıştır(int bağımsız_değişken_sayısı, char **bağımsız_değişkenler)
{
    pid_t çocuk_süreç_kimliği;
    int çocuk_sürecin_sonlanma_durumu = 0;

    if (bağımsız_değişken_sayısı < 2) {
        metin_yaz("usage: run FILE [ARGS...]\n");
        return;
    }
    çocuk_süreç_kimliği = fork();
    if (çocuk_süreç_kimliği < 0) {
        hata_bildir("fork");
        return;
    }
    if (çocuk_süreç_kimliği == 0) {
        execve(bağımsız_değişkenler[1], &bağımsız_değişkenler[1], (char *const *)0);
        hata_bildir("execve");
        _exit(127);
    }
    if (waitpid(çocuk_süreç_kimliği, &çocuk_sürecin_sonlanma_durumu, 0) < 0) {
        hata_bildir("waitpid");
        return;
    }
    metin_yaz("exit-status=");
    tam_sayı_yaz(WEXITSTATUS(çocuk_sürecin_sonlanma_durumu));
    metin_yaz("\n");
}

static void veri_birimi_geri_dönüşünü_sına(const char *ileti)
{
    struct sockaddr_in alıcı_adresi = {0};
    struct sockaddr_in gönderen_adresi = {0};
    socklen_t gönderen_adresinin_uzunluğu = sizeof(gönderen_adresi);
    char alınan_veri[96];
    size_t iletinin_bayt_uzunluğu = metnin_bayt_uzunluğu(ileti);
    int alıcı_iletişim_ucu = -1;
    int gönderici_iletişim_ucu = -1;
    ssize_t alınan_bayt_sayısı;

    if (iletinin_bayt_uzunluğu >= sizeof(alınan_veri)) {
        metin_yaz("udp: message exceeds 95 bytes\n");
        return;
    }
    alıcı_iletişim_ucu = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    gönderici_iletişim_ucu = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (alıcı_iletişim_ucu < 0 || gönderici_iletişim_ucu < 0) {
        hata_bildir("socket");
        goto iletişim_uçlarını_kapat;
    }
    alıcı_adresi.sin_family = AF_INET;
    alıcı_adresi.sin_port = htons(40404);
    alıcı_adresi.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    if (bind(alıcı_iletişim_ucu, (const struct sockaddr *)&alıcı_adresi, sizeof(alıcı_adresi)) < 0) {
        hata_bildir("bind");
        goto iletişim_uçlarını_kapat;
    }
    if (connect(gönderici_iletişim_ucu, (const struct sockaddr *)&alıcı_adresi, sizeof(alıcı_adresi)) < 0) {
        hata_bildir("connect");
        goto iletişim_uçlarını_kapat;
    }
    if (send(gönderici_iletişim_ucu, ileti, iletinin_bayt_uzunluğu, 0) != (ssize_t)iletinin_bayt_uzunluğu) {
        hata_bildir("send");
        goto iletişim_uçlarını_kapat;
    }
    alınan_bayt_sayısı = recvfrom(alıcı_iletişim_ucu, alınan_veri, sizeof(alınan_veri) - 1U, 0,
                         (struct sockaddr *)&gönderen_adresi, &gönderen_adresinin_uzunluğu);
    if (alınan_bayt_sayısı < 0) {
        hata_bildir("recvfrom");
        goto iletişim_uçlarını_kapat;
    }
    alınan_veri[alınan_bayt_sayısı] = '\0';
    metin_yaz("udp-received: ");
    metin_yaz(alınan_veri);
    metin_yaz("\n");

iletişim_uçlarını_kapat:
    if (gönderici_iletişim_ucu >= 0)
        (void)Kapat(gönderici_iletişim_ucu);
    if (alıcı_iletişim_ucu >= 0)
        (void)Kapat(alıcı_iletişim_ucu);
}

static int girdiyi_yorumla(int girdi_tanımlayıcısı)
{
    char girdi_satırı[girdi_satırı_kapasitesi];
    char *bağımsız_değişkenler[en_fazla_bağımsız_değişken_sayısı];
    struct girdi_akışı girdi = {0};
    girdi.girdi_tanımlayıcısı = girdi_tanımlayıcısı;

    for (;;) {
        int bağımsız_değişken_sayısı;
        int durum;
        if (girdi_tanımlayıcısı == STDIN_FILENO)
            metin_yaz("worldos$ ");
        durum = girdi_satırını_oku(&girdi, girdi_satırı, sizeof(girdi_satırı));
        if (durum == -1)
            return 0;
        if (durum == -2) {
            metin_yaz("input rejected: overlong or binary line\n");
            continue;
        }
        bağımsız_değişken_sayısı = bağımsız_değişkenleri_ayır(girdi_satırı, bağımsız_değişkenler);
        if (bağımsız_değişken_sayısı < 0) {
            metin_yaz("syntax error: quote, escape or argument limit\n");
            continue;
        }
        if (bağımsız_değişken_sayısı == 0)
            continue;
        if (komut_eşleşiyor(bağımsız_değişkenler[0], "help"))
            yardım_göster();
        else if (komut_eşleşiyor(bağımsız_değişkenler[0], "echo"))
            bağımsız_değişkenleri_göster(bağımsız_değişken_sayısı, bağımsız_değişkenler);
        else if (komut_eşleşiyor(bağımsız_değişkenler[0], "pwd"))
            çalışma_dizinini_göster();
        else if (komut_eşleşiyor(bağımsız_değişkenler[0], "cd")) {
            if (bağımsız_değişken_sayısı < 2)
                metin_yaz("usage: cd PATH\n");
            else if (chdir(bağımsız_değişkenler[1]) < 0)
                hata_bildir("cd");
        } else if (komut_eşleşiyor(bağımsız_değişkenler[0], "cat")) {
            if (bağımsız_değişken_sayısı < 2)
                metin_yaz("usage: cat FILE\n");
            else
                dosya_içeriğini_göster(bağımsız_değişkenler[1]);
        } else if (komut_eşleşiyor(bağımsız_değişkenler[0], "stat")) {
            if (bağımsız_değişken_sayısı < 2)
                metin_yaz("usage: stat FILE\n");
            else
                dosya_bilgilerini_göster(bağımsız_değişkenler[1]);
        } else if (komut_eşleşiyor(bağımsız_değişkenler[0], "pid"))
            süreç_kimliklerini_göster();
        else if (komut_eşleşiyor(bağımsız_değişkenler[0], "uname"))
            sistem_kimliğini_göster();
        else if (komut_eşleşiyor(bağımsız_değişkenler[0], "run"))
            programı_çalıştır(bağımsız_değişken_sayısı, bağımsız_değişkenler);
        else if (komut_eşleşiyor(bağımsız_değişkenler[0], "udp"))
            veri_birimi_geri_dönüşünü_sına(bağımsız_değişken_sayısı >= 2 ? bağımsız_değişkenler[1] : "ping");
        else if (komut_eşleşiyor(bağımsız_değişkenler[0], "source")) {
            if (bağımsız_değişken_sayısı < 2)
                metin_yaz("usage: source FILE\n");
            else if (komut_dosyasını_yorumla(bağımsız_değişkenler[1]))
                return 1;
        } else if (komut_eşleşiyor(bağımsız_değişkenler[0], "exit"))
            return 1;
        else
            metin_yaz("unknown command; type help\n");
    }
}

int main(void)
{
    metin_yaz("WORLDOS-SHELL:READY\n");
    (void)girdiyi_yorumla(STDIN_FILENO);
    metin_yaz("WORLDOS-SHELL:EXIT\n");
    return 0;
}
