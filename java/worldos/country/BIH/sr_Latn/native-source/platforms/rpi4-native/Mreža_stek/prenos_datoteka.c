#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "Mreža_stek.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int primiti_port = -1, kontrola = -1, ručno_veza = -1, podaci = -1;
static unsigned 로그인됨, korisnik_U_redu, red_promeniti_veličinu, 줄오류, Napusti_program, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned odgovor_promeniti_veličinu, 응답전송량, Dalje_broj_porta;
static uint32_t Aktivnost;
static char red[256], 응답모음[2048], Datoteka_stavka_ime[64], prenos_ime[64];
static unsigned char prenos_Status[16384];
static int 같은지(const char *첫째값, const char *SECOND_VALUE) { while (*첫째값 && *첫째값 == *SECOND_VALUE) { 첫째값++; SECOND_VALUE++; } return *첫째값 == *SECOND_VALUE; }
static void odgovor(const char *niska_podaci) {
    size_t stavka_COUNT = strlen(niska_podaci);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, odgovor_promeniti_veličinu - 응답전송량); odgovor_promeniti_veličinu -= 응답전송량; 응답전송량 = 0; }
    if (stavka_COUNT > sizeof(응답모음) - odgovor_promeniti_veličinu) { Napusti_program = 1; return; }
    memcpy(응답모음 + odgovor_promeniti_veličinu, niska_podaci, stavka_COUNT); odgovor_promeniti_veličinu += stavka_COUNT;
}
static void 수치(unsigned VALUE, char *KR_podaci, unsigned *stavka_COUNT) {
    char cifra_COUNT[10]; unsigned stavka_COUNT_8f7753a1 = 0;
    do { cifra_COUNT[stavka_COUNT_8f7753a1++] = '0' + VALUE % 10; VALUE /= 10; } while (VALUE);
    while (stavka_COUNT_8f7753a1) KR_podaci[(*stavka_COUNT)++] = cifra_COUNT[--stavka_COUNT_8f7753a1];
}
static void Stani_prenos(void) {
    if (podaci >= 0) Zatvori_Mreža(podaci); if (ručno_veza >= 0) Zatvori_Mreža(ručno_veza);
    podaci = ručno_veza = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void prekinuti_vezu(void) {
    Stani_prenos(); if (kontrola >= 0) Zatvori_Mreža(kontrola); kontrola = -1;
    로그인됨 = korisnik_U_redu = red_promeniti_veličinu = 줄오류 = odgovor_promeniti_veličinu = 응답전송량 = Napusti_program = 0;
}
int prenos_datoteka_kontrola(int radnja) {
    if (radnja == 2) return primiti_port >= 0;
    if (radnja == 0) { prekinuti_vezu(); if (primiti_port >= 0) Zatvori_Mreža(primiti_port); primiti_port = -1; return 0; }
    if (radnja != 1) return -22; if (primiti_port >= 0) return 0;
    primiti_port = 통신끝점만들기(1); if (primiti_port < 0) return primiti_port;
    int 반환값 = NET_povezati(primiti_port, 망상태읽기(0,0), 21); if (!반환값) 반환값 = NET_slušati(primiti_port);
    if (반환값 < 0) { Zatvori_Mreža(primiti_port); primiti_port = -1; } return 반환값;
}
static int putanja(const char *ime) {
    unsigned stavka_COUNT = 0; if (*ime == '/') ime++;
    if (!*ime || 같은지(ime, ".") || 같은지(ime, "..")) return 0;
    Datoteka_stavka_ime[stavka_COUNT++] = '/';
    while (*ime) {
        unsigned char kôd_znaka = *ime++;
        if (stavka_COUNT >= 63 || kôd_znaka < 32 || kôd_znaka == 127 || kôd_znaka == '/' || kôd_znaka == '\\') return 0;
        Datoteka_stavka_ime[stavka_COUNT++] = kôd_znaka;
    }
    Datoteka_stavka_ime[stavka_COUNT] = 0; return 1;
}
static void poslati_Lista(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int stavka_COUNT = 자바파일항목길이(순번); if (stavka_COUNT <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned stavka_COUNT_8f7753a1 = strlen(앞부분); memcpy(prenos_Status + 사용량, 앞부분, stavka_COUNT_8f7753a1); 사용량 += stavka_COUNT_8f7753a1;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)prenos_Status, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        stavka_COUNT_8f7753a1 = strlen(뒷부분); memcpy(prenos_Status + 사용량, 뒷부분, stavka_COUNT_8f7753a1); 사용량 += stavka_COUNT_8f7753a1;
        for (int 안쪽순번 = 0; 안쪽순번 < stavka_COUNT; 안쪽순번++) prenos_Status[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        prenos_Status[사용량++] = '\r'; prenos_Status[사용량++] = '\n';
    }
}
static void Pripremi_ručno_veza(int 확장여부) {
    if (수행작업) { odgovor("450 Transfer in progress\r\n"); return; }
    Stani_prenos(); ručno_veza = 통신끝점만들기(1);
    if (ručno_veza >= 0) 통신주소재사용(ručno_veza);
    unsigned broj_porta = 50000 + Dalje_broj_porta++ % 8;
    if (ručno_veza < 0 || NET_povezati(ručno_veza, 망상태읽기(0,0), broj_porta) || NET_slušati(ručno_veza)) {
        Stani_prenos(); odgovor("425 Cannot open passive listener\r\n"); return;
    }
    char odgovor_1262b476[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned stavka_COUNT = strlen(앞부분); memcpy(odgovor_1262b476, 앞부분, stavka_COUNT);
    if (확장여부) { 수치(broj_porta, odgovor_1262b476, &stavka_COUNT); odgovor_1262b476[stavka_COUNT++] = '|'; }
    else {
        uint32_t adresa=망상태읽기(0,0);
        for (int indeks_pozicije=24;indeks_pozicije>=0;indeks_pozicije-=8) { 수치((adresa>>indeks_pozicije)&255,odgovor_1262b476,&stavka_COUNT);odgovor_1262b476[stavka_COUNT++]=','; }
        수치(broj_porta / 256, odgovor_1262b476, &stavka_COUNT); odgovor_1262b476[stavka_COUNT++] = ','; 수치(broj_porta % 256, odgovor_1262b476, &stavka_COUNT);
    }
    odgovor_1262b476[stavka_COUNT++] = ')'; odgovor_1262b476[stavka_COUNT++] = '\r'; odgovor_1262b476[stavka_COUNT++] = '\n'; odgovor_1262b476[stavka_COUNT] = 0; odgovor(odgovor_1262b476);
}
static void komanda(void) {
    red[red_promeniti_veličinu] = 0;
    char *부가인수 = red; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(red, "QUIT")) { Stani_prenos(); odgovor("221 Goodbye\r\n"); Napusti_program = 1; return; }
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
    else if (같은지(red, "ABOR")) { Stani_prenos(); odgovor("226 Transfer aborted\r\n"); }
    else if (같은지(red, "DELE")) { odgovor(putanja(부가인수) && pk_unlink(Datoteka_stavka_ime) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(red, "LIST") || 같은지(red, "NLST") || 같은지(red, "MLSD")) {
        if (수행작업) { odgovor("450 Transfer in progress\r\n"); return; }
        if (ručno_veza < 0 && podaci < 0) { odgovor("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { odgovor("550 Root listing only\r\n"); return; }
        poslati_Lista(같은지(red,"MLSD") ? 2 : 같은지(red,"LIST") ? 1 : 0); 수행작업 = 2;
        odgovor("150 Opening directory listing\r\n");
    }
    else if (같은지(red, "SIZE")) {
        if (!putanja(부가인수)) { odgovor("550 Invalid filename\r\n"); return; }
        int Datoteka_pokazivač = pk_open(Datoteka_stavka_ime, samo_za_čitanje_VALUE, 0); if (Datoteka_pokazivač < 0) { odgovor("550 File unavailable\r\n"); return; }
        int promeniti_veličinu = pk_size(Datoteka_pokazivač); pk_close(Datoteka_pokazivač); char odgovor_1262b476[32] = "213 "; unsigned stavka_COUNT = 4;
        수치(promeniti_veličinu, odgovor_1262b476, &stavka_COUNT); odgovor_1262b476[stavka_COUNT++] = '\r'; odgovor_1262b476[stavka_COUNT++] = '\n'; odgovor_1262b476[stavka_COUNT] = 0; odgovor(odgovor_1262b476);
    } else if (같은지(red, "STOR") || 같은지(red, "RETR")) {
        if (수행작업) { odgovor("450 Transfer in progress\r\n"); return; }
        if (ručno_veza < 0 && podaci < 0) { odgovor("425 Use PASV or EPSV\r\n"); return; }
        if (!putanja(부가인수)) { odgovor("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(red, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(prenos_ime, Datoteka_stavka_ime, strlen(Datoteka_stavka_ime) + 1);
        if (수행작업 == 2) {
            int Datoteka_pokazivač = pk_open(Datoteka_stavka_ime, samo_za_čitanje_VALUE, 0);
            if (Datoteka_pokazivač < 0) { 수행작업 = 0; odgovor("550 File unavailable\r\n"); return; }
            int stavka_COUNT = pk_read(Datoteka_pokazivač, prenos_Status, sizeof(prenos_Status)); pk_close(Datoteka_pokazivač);
            if (stavka_COUNT < 0) { 수행작업 = 0; odgovor("451 Read failed\r\n"); return; } 사용량 = stavka_COUNT;
        }
        odgovor("150 Opening binary data connection\r\n");
    } else odgovor("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (primiti_port < 0) return;
    int dolazni_veza = NET_prihvatiti(primiti_port);
    if (dolazni_veza >= 0) {
        if (kontrola >= 0) { 통신쓰기(dolazni_veza, "421 One session at a time\r\n", 27); Zatvori_Mreža(dolazni_veza); }
        else { kontrola = dolazni_veza; Aktivnost = 보드밀리초(); odgovor("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (kontrola < 0) return;
    if ((uint32_t)(보드밀리초() - Aktivnost) > 60000) { prekinuti_vezu(); return; }
    if (!Napusti_program) for (unsigned budžet = 0; budžet < 256; budžet++) {
        unsigned char kôd_znaka; int 반환값 = 통신읽기(kontrola, &kôd_znaka, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { prekinuti_vezu(); return; } Aktivnost = 보드밀리초();
        if (kôd_znaka == '\n') { if (줄오류) odgovor("500 Command too long or invalid\r\n"); else komanda(); red_promeniti_veličinu = 줄오류 = 0; if (Napusti_program) break; }
        else if (kôd_znaka != '\r') { if (!kôd_znaka || red_promeniti_veličinu >= sizeof(red) - 1) 줄오류 = 1; else red[red_promeniti_veličinu++] = kôd_znaka; }
    }
    if (ručno_veza >= 0 && podaci < 0) {
        int 반환값 = NET_prihvatiti(ručno_veza);
        if (반환값 >= 0) {
            if (NET_ravnopravni_uređaj_adresa(반환값) != NET_ravnopravni_uređaj_adresa(kontrola)) Zatvori_Mreža(반환값);
            else { podaci = 반환값; Zatvori_Mreža(ručno_veza); ručno_veza = -1; Aktivnost = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && podaci >= 0) for (unsigned budžet = 0; budžet < 8; budžet++) {
        unsigned char blok_podataka[512]; int stavka_COUNT = 통신읽기(podaci, blok_podataka, sizeof(blok_podataka));
        if (stavka_COUNT == -11) break;
        if (stavka_COUNT < 0) { Stani_prenos(); odgovor("426 Data connection failed\r\n"); break; }
        Aktivnost = 보드밀리초();
        if (stavka_COUNT == 0) {
            int KR = -1;
            if (!실패여부) {
                int Datoteka_pokazivač = pk_open(prenos_ime, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (Datoteka_pokazivač >= 0) { KR = pk_write(Datoteka_pokazivač, prenos_Status, 사용량); pk_close(Datoteka_pokazivač); }
            }
            int 성공여부 = !실패여부 && KR == (int)사용량; Stani_prenos(); odgovor(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)stavka_COUNT > sizeof(prenos_Status) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(prenos_Status + 사용량, blok_podataka, stavka_COUNT); 사용량 += stavka_COUNT; }
    }
    if (수행작업 == 2 && podaci >= 0) {
        int stavka_COUNT = 통신쓰기(podaci, prenos_Status + 보낸수, 사용량 - 보낸수);
        if (stavka_COUNT >= 0) { 보낸수 += stavka_COUNT; Aktivnost = 보드밀리초(); if (보낸수 == 사용량) { Stani_prenos(); odgovor("226 Transfer complete\r\n"); } }
        else if (stavka_COUNT != -11) { Stani_prenos(); odgovor("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < odgovor_promeniti_veličinu) {
        int stavka_COUNT = 통신쓰기(kontrola, 응답모음 + 응답전송량, odgovor_promeniti_veličinu - 응답전송량);
        if (stavka_COUNT > 0) 응답전송량 += stavka_COUNT; else if (stavka_COUNT != -11) { prekinuti_vezu(); return; }
    }
    if (응답전송량 == odgovor_promeniti_veličinu) { odgovor_promeniti_veličinu = 응답전송량 = 0; if (Napusti_program) prekinuti_vezu(); }
}
