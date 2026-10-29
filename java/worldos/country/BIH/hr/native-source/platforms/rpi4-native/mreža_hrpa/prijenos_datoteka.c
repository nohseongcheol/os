#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "mreža_hrpa.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int primiti_prebaciti = -1, kontrola = -1, ručno_veza = -1, podaci = -1;
static unsigned 로그인됨, korisnik_U_redu, red_promijeniti_veličinu, 줄오류, izlaz_program, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned odgovor_promijeniti_veličinu, 응답전송량, Dalje_broj_priključka;
static uint32_t Aktivnost_4d9c9a53;
static char red[256], 응답모음[2048], Datoteka_unos_naziv[64], Prijenos_naziv[64];
static unsigned char Prijenos_Stanje[16384];
static int 같은지(const char *첫째값, const char *SECOND_VALUE) { while (*첫째값 && *첫째값 == *SECOND_VALUE) { 첫째값++; SECOND_VALUE++; } return *첫째값 == *SECOND_VALUE; }
static void odgovor(const char *niz_podaci) {
    size_t artikl_COUNT = strlen(niz_podaci);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, odgovor_promijeniti_veličinu - 응답전송량); odgovor_promijeniti_veličinu -= 응답전송량; 응답전송량 = 0; }
    if (artikl_COUNT > sizeof(응답모음) - odgovor_promijeniti_veličinu) { izlaz_program = 1; return; }
    memcpy(응답모음 + odgovor_promijeniti_veličinu, niz_podaci, artikl_COUNT); odgovor_promijeniti_veličinu += artikl_COUNT;
}
static void 수치(unsigned VALUE, char *KR_podaci, unsigned *artikl_COUNT) {
    char znamenka_COUNT[10]; unsigned unos_COUNT = 0;
    do { znamenka_COUNT[unos_COUNT++] = '0' + VALUE % 10; VALUE /= 10; } while (VALUE);
    while (unos_COUNT) KR_podaci[(*artikl_COUNT)++] = znamenka_COUNT[--unos_COUNT];
}
static void Stani_Prijenos(void) {
    if (podaci >= 0) Zatvori_mreža(podaci); if (ručno_veza >= 0) Zatvori_mreža(ručno_veza);
    podaci = ručno_veza = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void prekinuti_vezu(void) {
    Stani_Prijenos(); if (kontrola >= 0) Zatvori_mreža(kontrola); kontrola = -1;
    로그인됨 = korisnik_U_redu = red_promijeniti_veličinu = 줄오류 = odgovor_promijeniti_veličinu = 응답전송량 = izlaz_program = 0;
}
int prijenos_datoteka_kontrola(int Aktivnost) {
    if (Aktivnost == 2) return primiti_prebaciti >= 0;
    if (Aktivnost == 0) { prekinuti_vezu(); if (primiti_prebaciti >= 0) Zatvori_mreža(primiti_prebaciti); primiti_prebaciti = -1; return 0; }
    if (Aktivnost != 1) return -22; if (primiti_prebaciti >= 0) return 0;
    primiti_prebaciti = 통신끝점만들기(1); if (primiti_prebaciti < 0) return primiti_prebaciti;
    int 반환값 = NET_BIND(primiti_prebaciti, 망상태읽기(0,0), 21); if (!반환값) 반환값 = NET_osluškivati(primiti_prebaciti);
    if (반환값 < 0) { Zatvori_mreža(primiti_prebaciti); primiti_prebaciti = -1; } return 반환값;
}
static int PUTANJA(const char *Ime) {
    unsigned artikl_COUNT = 0; if (*Ime == '/') Ime++;
    if (!*Ime || 같은지(Ime, ".") || 같은지(Ime, "..")) return 0;
    Datoteka_unos_naziv[artikl_COUNT++] = '/';
    while (*Ime) {
        unsigned char kodna_točka = *Ime++;
        if (artikl_COUNT >= 63 || kodna_točka < 32 || kodna_točka == 127 || kodna_točka == '/' || kodna_točka == '\\') return 0;
        Datoteka_unos_naziv[artikl_COUNT++] = kodna_točka;
    }
    Datoteka_unos_naziv[artikl_COUNT] = 0; return 1;
}
static void slati_Popis(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int artikl_COUNT = 자바파일항목길이(순번); if (artikl_COUNT <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned unos_COUNT = strlen(앞부분); memcpy(Prijenos_Stanje + 사용량, 앞부분, unos_COUNT); 사용량 += unos_COUNT;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)Prijenos_Stanje, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        unos_COUNT = strlen(뒷부분); memcpy(Prijenos_Stanje + 사용량, 뒷부분, unos_COUNT); 사용량 += unos_COUNT;
        for (int 안쪽순번 = 0; 안쪽순번 < artikl_COUNT; 안쪽순번++) Prijenos_Stanje[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        Prijenos_Stanje[사용량++] = '\r'; Prijenos_Stanje[사용량++] = '\n';
    }
}
static void Pripremi_ručno_veza(int 확장여부) {
    if (수행작업) { odgovor("450 Transfer in progress\r\n"); return; }
    Stani_Prijenos(); ručno_veza = 통신끝점만들기(1);
    if (ručno_veza >= 0) 통신주소재사용(ručno_veza);
    unsigned broj_priključka = 50000 + Dalje_broj_priključka++ % 8;
    if (ručno_veza < 0 || NET_BIND(ručno_veza, 망상태읽기(0,0), broj_priključka) || NET_osluškivati(ručno_veza)) {
        Stani_Prijenos(); odgovor("425 Cannot open passive listener\r\n"); return;
    }
    char odgovor_1262b476[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned artikl_COUNT = strlen(앞부분); memcpy(odgovor_1262b476, 앞부분, artikl_COUNT);
    if (확장여부) { 수치(broj_priključka, odgovor_1262b476, &artikl_COUNT); odgovor_1262b476[artikl_COUNT++] = '|'; }
    else {
        uint32_t adresa=망상태읽기(0,0);
        for (int indeks_položaja=24;indeks_položaja>=0;indeks_položaja-=8) { 수치((adresa>>indeks_položaja)&255,odgovor_1262b476,&artikl_COUNT);odgovor_1262b476[artikl_COUNT++]=','; }
        수치(broj_priključka / 256, odgovor_1262b476, &artikl_COUNT); odgovor_1262b476[artikl_COUNT++] = ','; 수치(broj_priključka % 256, odgovor_1262b476, &artikl_COUNT);
    }
    odgovor_1262b476[artikl_COUNT++] = ')'; odgovor_1262b476[artikl_COUNT++] = '\r'; odgovor_1262b476[artikl_COUNT++] = '\n'; odgovor_1262b476[artikl_COUNT] = 0; odgovor(odgovor_1262b476);
}
static void Naredba(void) {
    red[red_promijeniti_veličinu] = 0;
    char *부가인수 = red; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(red, "QUIT")) { Stani_Prijenos(); odgovor("221 Goodbye\r\n"); izlaz_program = 1; return; }
    if (같은지(red, "NOOP")) { odgovor("200 OK\r\n"); return; }
    if (같은지(red, "SYST")) { odgovor("215 UNIX Type: L8\r\n"); return; }
    if (같은지(red, "FEAT")) { odgovor("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(red, "USER")) { 로그인됨 = 0; korisnik_U_redu = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); odgovor(korisnik_U_redu ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(red, "PASS")) { 로그인됨 = korisnik_U_redu; odgovor(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { odgovor("530 Login first\r\n"); return; }
    if (같은지(red, "PWD")) odgovor("257 \"/\"\r\n");
    else if (같은지(red, "CWD")) odgovor(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(red, "TYPE")) odgovor(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(red, "OPTS")) odgovor(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(red, "PASV")) Pripremi_ručno_veza(0);
    else if (같은지(red, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) odgovor("522 IPv4 only\r\n"); else Pripremi_ručno_veza(1); }
    else if (같은지(red, "ABOR")) { Stani_Prijenos(); odgovor("226 Transfer aborted\r\n"); }
    else if (같은지(red, "DELE")) { odgovor(PUTANJA(부가인수) && pk_unlink(Datoteka_unos_naziv) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(red, "LIST") || 같은지(red, "NLST") || 같은지(red, "MLSD")) {
        if (수행작업) { odgovor("450 Transfer in progress\r\n"); return; }
        if (ručno_veza < 0 && podaci < 0) { odgovor("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { odgovor("550 Root listing only\r\n"); return; }
        slati_Popis(같은지(red,"MLSD") ? 2 : 같은지(red,"LIST") ? 1 : 0); 수행작업 = 2;
        odgovor("150 Opening directory listing\r\n");
    }
    else if (같은지(red, "SIZE")) {
        if (!PUTANJA(부가인수)) { odgovor("550 Invalid filename\r\n"); return; }
        int Datoteka_ustroj = pk_open(Datoteka_unos_naziv, samo_za_čitanje_VALUE, 0); if (Datoteka_ustroj < 0) { odgovor("550 File unavailable\r\n"); return; }
        int Veličina = pk_size(Datoteka_ustroj); pk_close(Datoteka_ustroj); char odgovor_1262b476[32] = "213 "; unsigned artikl_COUNT = 4;
        수치(Veličina, odgovor_1262b476, &artikl_COUNT); odgovor_1262b476[artikl_COUNT++] = '\r'; odgovor_1262b476[artikl_COUNT++] = '\n'; odgovor_1262b476[artikl_COUNT] = 0; odgovor(odgovor_1262b476);
    } else if (같은지(red, "STOR") || 같은지(red, "RETR")) {
        if (수행작업) { odgovor("450 Transfer in progress\r\n"); return; }
        if (ručno_veza < 0 && podaci < 0) { odgovor("425 Use PASV or EPSV\r\n"); return; }
        if (!PUTANJA(부가인수)) { odgovor("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(red, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(Prijenos_naziv, Datoteka_unos_naziv, strlen(Datoteka_unos_naziv) + 1);
        if (수행작업 == 2) {
            int Datoteka_ustroj = pk_open(Datoteka_unos_naziv, samo_za_čitanje_VALUE, 0);
            if (Datoteka_ustroj < 0) { 수행작업 = 0; odgovor("550 File unavailable\r\n"); return; }
            int artikl_COUNT = pk_read(Datoteka_ustroj, Prijenos_Stanje, sizeof(Prijenos_Stanje)); pk_close(Datoteka_ustroj);
            if (artikl_COUNT < 0) { 수행작업 = 0; odgovor("451 Read failed\r\n"); return; } 사용량 = artikl_COUNT;
        }
        odgovor("150 Opening binary data connection\r\n");
    } else odgovor("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (primiti_prebaciti < 0) return;
    int Dolazni_veza = NET_prihvatiti(primiti_prebaciti);
    if (Dolazni_veza >= 0) {
        if (kontrola >= 0) { NET_zapisivanje(Dolazni_veza, "421 One session at a time\r\n", 27); Zatvori_mreža(Dolazni_veza); }
        else { kontrola = Dolazni_veza; Aktivnost_4d9c9a53 = 보드밀리초(); odgovor("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (kontrola < 0) return;
    if ((uint32_t)(보드밀리초() - Aktivnost_4d9c9a53) > 60000) { prekinuti_vezu(); return; }
    if (!izlaz_program) for (unsigned proračun = 0; proračun < 256; proračun++) {
        unsigned char kodna_točka; int 반환값 = 통신읽기(kontrola, &kodna_točka, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { prekinuti_vezu(); return; } Aktivnost_4d9c9a53 = 보드밀리초();
        if (kodna_točka == '\n') { if (줄오류) odgovor("500 Command too long or invalid\r\n"); else Naredba(); red_promijeniti_veličinu = 줄오류 = 0; if (izlaz_program) break; }
        else if (kodna_točka != '\r') { if (!kodna_točka || red_promijeniti_veličinu >= sizeof(red) - 1) 줄오류 = 1; else red[red_promijeniti_veličinu++] = kodna_točka; }
    }
    if (ručno_veza >= 0 && podaci < 0) {
        int 반환값 = NET_prihvatiti(ručno_veza);
        if (반환값 >= 0) {
            if (NET_ravnopravan_član_adresa(반환값) != NET_ravnopravan_član_adresa(kontrola)) Zatvori_mreža(반환값);
            else { podaci = 반환값; Zatvori_mreža(ručno_veza); ručno_veza = -1; Aktivnost_4d9c9a53 = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && podaci >= 0) for (unsigned proračun = 0; proračun < 8; proračun++) {
        unsigned char podatkovni_blok[512]; int artikl_COUNT = 통신읽기(podaci, podatkovni_blok, sizeof(podatkovni_blok));
        if (artikl_COUNT == -11) break;
        if (artikl_COUNT < 0) { Stani_Prijenos(); odgovor("426 Data connection failed\r\n"); break; }
        Aktivnost_4d9c9a53 = 보드밀리초();
        if (artikl_COUNT == 0) {
            int REZULTAT = -1;
            if (!실패여부) {
                int Datoteka_ustroj = pk_open(Prijenos_naziv, 쓰기전용 | 없으면만들기 | skratiti_Sadržaj, 0600);
                if (Datoteka_ustroj >= 0) { REZULTAT = pk_write(Datoteka_ustroj, Prijenos_Stanje, 사용량); pk_close(Datoteka_ustroj); }
            }
            int 성공여부 = !실패여부 && REZULTAT == (int)사용량; Stani_Prijenos(); odgovor(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)artikl_COUNT > sizeof(Prijenos_Stanje) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(Prijenos_Stanje + 사용량, podatkovni_blok, artikl_COUNT); 사용량 += artikl_COUNT; }
    }
    if (수행작업 == 2 && podaci >= 0) {
        int artikl_COUNT = NET_zapisivanje(podaci, Prijenos_Stanje + 보낸수, 사용량 - 보낸수);
        if (artikl_COUNT >= 0) { 보낸수 += artikl_COUNT; Aktivnost_4d9c9a53 = 보드밀리초(); if (보낸수 == 사용량) { Stani_Prijenos(); odgovor("226 Transfer complete\r\n"); } }
        else if (artikl_COUNT != -11) { Stani_Prijenos(); odgovor("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < odgovor_promijeniti_veličinu) {
        int artikl_COUNT = NET_zapisivanje(kontrola, 응답모음 + 응답전송량, odgovor_promijeniti_veličinu - 응답전송량);
        if (artikl_COUNT > 0) 응답전송량 += artikl_COUNT; else if (artikl_COUNT != -11) { prekinuti_vezu(); return; }
    }
    if (응답전송량 == odgovor_promijeniti_veličinu) { odgovor_promijeniti_veličinu = 응답전송량 = 0; if (izlaz_program) prekinuti_vezu(); }
}
