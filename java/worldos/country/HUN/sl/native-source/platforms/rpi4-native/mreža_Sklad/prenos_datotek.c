#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "mreža_Sklad.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int sprejeti_sprejemati_prejeti_prejemati_vrata = -1, nadzor = -1, ročno_povezava = -1, podatki = -1;
static unsigned 로그인됨, uporabnik_V_redu, linija_spremeniti_velikost, 줄오류, izhod_aplikacija, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned odgovor_spremeniti_velikost, 응답전송량, Naprej_številka_vrat;
static uint32_t Dejavnost;
static char Črtni[256], 응답모음[2048], Datoteka_vnos_ime[64], Prenos_ime[64];
static unsigned char Prenos_stanje[16384];
static int 같은지(const char *첫째값, const char *SECOND_VALUE) { while (*첫째값 && *첫째값 == *SECOND_VALUE) { 첫째값++; SECOND_VALUE++; } return *첫째값 == *SECOND_VALUE; }
static void odgovor(const char *niz_podatki) {
    size_t element_COUNT = strlen(niz_podatki);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, odgovor_spremeniti_velikost - 응답전송량); odgovor_spremeniti_velikost -= 응답전송량; 응답전송량 = 0; }
    if (element_COUNT > sizeof(응답모음) - odgovor_spremeniti_velikost) { izhod_aplikacija = 1; return; }
    memcpy(응답모음 + odgovor_spremeniti_velikost, niz_podatki, element_COUNT); odgovor_spremeniti_velikost += element_COUNT;
}
static void 수치(unsigned VALUE, char *KR_podatki, unsigned *element_COUNT) {
    char številka_COUNT[10]; unsigned vnos_COUNT = 0;
    do { številka_COUNT[vnos_COUNT++] = '0' + VALUE % 10; VALUE /= 10; } while (VALUE);
    while (vnos_COUNT) KR_podatki[(*element_COUNT)++] = številka_COUNT[--vnos_COUNT];
}
static void Stop_Prenos(void) {
    if (podatki >= 0) Zapri_mreža(podatki); if (ročno_povezava >= 0) Zapri_mreža(ročno_povezava);
    podatki = ročno_povezava = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void prekiniti_povezavo(void) {
    Stop_Prenos(); if (nadzor >= 0) Zapri_mreža(nadzor); nadzor = -1;
    로그인됨 = uporabnik_V_redu = linija_spremeniti_velikost = 줄오류 = odgovor_spremeniti_velikost = 응답전송량 = izhod_aplikacija = 0;
}
int prenos_datotek_nadzor(int Dejanje) {
    if (Dejanje == 2) return sprejeti_sprejemati_prejeti_prejemati_vrata >= 0;
    if (Dejanje == 0) { prekiniti_povezavo(); if (sprejeti_sprejemati_prejeti_prejemati_vrata >= 0) Zapri_mreža(sprejeti_sprejemati_prejeti_prejemati_vrata); sprejeti_sprejemati_prejeti_prejemati_vrata = -1; return 0; }
    if (Dejanje != 1) return -22; if (sprejeti_sprejemati_prejeti_prejemati_vrata >= 0) return 0;
    sprejeti_sprejemati_prejeti_prejemati_vrata = Ustvari_vtičnica_končna_točka(1); if (sprejeti_sprejemati_prejeti_prejemati_vrata < 0) return sprejeti_sprejemati_prejeti_prejemati_vrata;
    int 반환값 = NET_BIND(sprejeti_sprejemati_prejeti_prejemati_vrata, 망상태읽기(0,0), 21); if (!반환값) 반환값 = NET_poslušati(sprejeti_sprejemati_prejeti_prejemati_vrata);
    if (반환값 < 0) { Zapri_mreža(sprejeti_sprejemati_prejeti_prejemati_vrata); sprejeti_sprejemati_prejeti_prejemati_vrata = -1; } return 반환값;
}
static int POT(const char *Ime) {
    unsigned element_COUNT = 0; if (*Ime == '/') Ime++;
    if (!*Ime || 같은지(Ime, ".") || 같은지(Ime, "..")) return 0;
    Datoteka_vnos_ime[element_COUNT++] = '/';
    while (*Ime) {
        unsigned char koda_znaka = *Ime++;
        if (element_COUNT >= 63 || koda_znaka < 32 || koda_znaka == 127 || koda_znaka == '/' || koda_znaka == '\\') return 0;
        Datoteka_vnos_ime[element_COUNT++] = koda_znaka;
    }
    Datoteka_vnos_ime[element_COUNT] = 0; return 1;
}
static void poslati_Seznam(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int element_COUNT = 자바파일항목길이(순번); if (element_COUNT <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned vnos_COUNT = strlen(앞부분); memcpy(Prenos_stanje + 사용량, 앞부분, vnos_COUNT); 사용량 += vnos_COUNT;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)Prenos_stanje, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        vnos_COUNT = strlen(뒷부분); memcpy(Prenos_stanje + 사용량, 뒷부분, vnos_COUNT); 사용량 += vnos_COUNT;
        for (int 안쪽순번 = 0; 안쪽순번 < element_COUNT; 안쪽순번++) Prenos_stanje[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        Prenos_stanje[사용량++] = '\r'; Prenos_stanje[사용량++] = '\n';
    }
}
static void Pripravi_ročno_povezava(int 확장여부) {
    if (수행작업) { odgovor("450 Transfer in progress\r\n"); return; }
    Stop_Prenos(); ročno_povezava = Ustvari_vtičnica_končna_točka(1);
    if (ročno_povezava >= 0) 통신주소재사용(ročno_povezava);
    unsigned številka_vrat = 50000 + Naprej_številka_vrat++ % 8;
    if (ročno_povezava < 0 || NET_BIND(ročno_povezava, 망상태읽기(0,0), številka_vrat) || NET_poslušati(ročno_povezava)) {
        Stop_Prenos(); odgovor("425 Cannot open passive listener\r\n"); return;
    }
    char odziv[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned element_COUNT = strlen(앞부분); memcpy(odziv, 앞부분, element_COUNT);
    if (확장여부) { 수치(številka_vrat, odziv, &element_COUNT); odziv[element_COUNT++] = '|'; }
    else {
        uint32_t naslov=망상태읽기(0,0);
        for (int kazalec_mesta=24;kazalec_mesta>=0;kazalec_mesta-=8) { 수치((naslov>>kazalec_mesta)&255,odziv,&element_COUNT);odziv[element_COUNT++]=','; }
        수치(številka_vrat / 256, odziv, &element_COUNT); odziv[element_COUNT++] = ','; 수치(številka_vrat % 256, odziv, &element_COUNT);
    }
    odziv[element_COUNT++] = ')'; odziv[element_COUNT++] = '\r'; odziv[element_COUNT++] = '\n'; odziv[element_COUNT] = 0; odgovor(odziv);
}
static void Ukaz(void) {
    Črtni[linija_spremeniti_velikost] = 0;
    char *부가인수 = Črtni; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(Črtni, "QUIT")) { Stop_Prenos(); odgovor("221 Goodbye\r\n"); izhod_aplikacija = 1; return; }
    if (같은지(Črtni, "NOOP")) { odgovor("200 OK\r\n"); return; }
    if (같은지(Črtni, "SYST")) { odgovor("215 UNIX Type: L8\r\n"); return; }
    if (같은지(Črtni, "FEAT")) { odgovor("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(Črtni, "USER")) { 로그인됨 = 0; uporabnik_V_redu = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); odgovor(uporabnik_V_redu ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(Črtni, "PASS")) { 로그인됨 = uporabnik_V_redu; odgovor(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { odgovor("530 Login first\r\n"); return; }
    if (같은지(Črtni, "PWD")) odgovor("257 \"/\"\r\n");
    else if (같은지(Črtni, "CWD")) odgovor(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(Črtni, "TYPE")) odgovor(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(Črtni, "OPTS")) odgovor(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(Črtni, "PASV")) Pripravi_ročno_povezava(0);
    else if (같은지(Črtni, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) odgovor("522 IPv4 only\r\n"); else Pripravi_ročno_povezava(1); }
    else if (같은지(Črtni, "ABOR")) { Stop_Prenos(); odgovor("226 Transfer aborted\r\n"); }
    else if (같은지(Črtni, "DELE")) { odgovor(POT(부가인수) && pk_unlink(Datoteka_vnos_ime) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(Črtni, "LIST") || 같은지(Črtni, "NLST") || 같은지(Črtni, "MLSD")) {
        if (수행작업) { odgovor("450 Transfer in progress\r\n"); return; }
        if (ročno_povezava < 0 && podatki < 0) { odgovor("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { odgovor("550 Root listing only\r\n"); return; }
        poslati_Seznam(같은지(Črtni,"MLSD") ? 2 : 같은지(Črtni,"LIST") ? 1 : 0); 수행작업 = 2;
        odgovor("150 Opening directory listing\r\n");
    }
    else if (같은지(Črtni, "SIZE")) {
        if (!POT(부가인수)) { odgovor("550 Invalid filename\r\n"); return; }
        int Datoteka_ročica = pk_open(Datoteka_vnos_ime, samo_za_branje_VALUE, 0); if (Datoteka_ročica < 0) { odgovor("550 File unavailable\r\n"); return; }
        int Velikost = pk_size(Datoteka_ročica); pk_close(Datoteka_ročica); char odziv[32] = "213 "; unsigned element_COUNT = 4;
        수치(Velikost, odziv, &element_COUNT); odziv[element_COUNT++] = '\r'; odziv[element_COUNT++] = '\n'; odziv[element_COUNT] = 0; odgovor(odziv);
    } else if (같은지(Črtni, "STOR") || 같은지(Črtni, "RETR")) {
        if (수행작업) { odgovor("450 Transfer in progress\r\n"); return; }
        if (ročno_povezava < 0 && podatki < 0) { odgovor("425 Use PASV or EPSV\r\n"); return; }
        if (!POT(부가인수)) { odgovor("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(Črtni, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(Prenos_ime, Datoteka_vnos_ime, strlen(Datoteka_vnos_ime) + 1);
        if (수행작업 == 2) {
            int Datoteka_ročica = pk_open(Datoteka_vnos_ime, samo_za_branje_VALUE, 0);
            if (Datoteka_ročica < 0) { 수행작업 = 0; odgovor("550 File unavailable\r\n"); return; }
            int element_COUNT = pk_read(Datoteka_ročica, Prenos_stanje, sizeof(Prenos_stanje)); pk_close(Datoteka_ročica);
            if (element_COUNT < 0) { 수행작업 = 0; odgovor("451 Read failed\r\n"); return; } 사용량 = element_COUNT;
        }
        odgovor("150 Opening binary data connection\r\n");
    } else odgovor("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (sprejeti_sprejemati_prejeti_prejemati_vrata < 0) return;
    int Dohoden_povezava = NET_sprejeti(sprejeti_sprejemati_prejeti_prejemati_vrata);
    if (Dohoden_povezava >= 0) {
        if (nadzor >= 0) { NET_pisati(Dohoden_povezava, "421 One session at a time\r\n", 27); Zapri_mreža(Dohoden_povezava); }
        else { nadzor = Dohoden_povezava; Dejavnost = 보드밀리초(); odgovor("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (nadzor < 0) return;
    if ((uint32_t)(보드밀리초() - Dejavnost) > 60000) { prekiniti_povezavo(); return; }
    if (!izhod_aplikacija) for (unsigned proračun = 0; proračun < 256; proračun++) {
        unsigned char koda_znaka; int 반환값 = 통신읽기(nadzor, &koda_znaka, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { prekiniti_povezavo(); return; } Dejavnost = 보드밀리초();
        if (koda_znaka == '\n') { if (줄오류) odgovor("500 Command too long or invalid\r\n"); else Ukaz(); linija_spremeniti_velikost = 줄오류 = 0; if (izhod_aplikacija) break; }
        else if (koda_znaka != '\r') { if (!koda_znaka || linija_spremeniti_velikost >= sizeof(Črtni) - 1) 줄오류 = 1; else Črtni[linija_spremeniti_velikost++] = koda_znaka; }
    }
    if (ročno_povezava >= 0 && podatki < 0) {
        int 반환값 = NET_sprejeti(ročno_povezava);
        if (반환값 >= 0) {
            if (NET_enakovreden_naslov(반환값) != NET_enakovreden_naslov(nadzor)) Zapri_mreža(반환값);
            else { podatki = 반환값; Zapri_mreža(ročno_povezava); ročno_povezava = -1; Dejavnost = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && podatki >= 0) for (unsigned proračun = 0; proračun < 8; proračun++) {
        unsigned char blok_podatkov[512]; int element_COUNT = 통신읽기(podatki, blok_podatkov, sizeof(blok_podatkov));
        if (element_COUNT == -11) break;
        if (element_COUNT < 0) { Stop_Prenos(); odgovor("426 Data connection failed\r\n"); break; }
        Dejavnost = 보드밀리초();
        if (element_COUNT == 0) {
            int REZULTAT = -1;
            if (!실패여부) {
                int Datoteka_ročica = pk_open(Prenos_ime, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (Datoteka_ročica >= 0) { REZULTAT = pk_write(Datoteka_ročica, Prenos_stanje, 사용량); pk_close(Datoteka_ročica); }
            }
            int 성공여부 = !실패여부 && REZULTAT == (int)사용량; Stop_Prenos(); odgovor(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)element_COUNT > sizeof(Prenos_stanje) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(Prenos_stanje + 사용량, blok_podatkov, element_COUNT); 사용량 += element_COUNT; }
    }
    if (수행작업 == 2 && podatki >= 0) {
        int element_COUNT = NET_pisati(podatki, Prenos_stanje + 보낸수, 사용량 - 보낸수);
        if (element_COUNT >= 0) { 보낸수 += element_COUNT; Dejavnost = 보드밀리초(); if (보낸수 == 사용량) { Stop_Prenos(); odgovor("226 Transfer complete\r\n"); } }
        else if (element_COUNT != -11) { Stop_Prenos(); odgovor("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < odgovor_spremeniti_velikost) {
        int element_COUNT = NET_pisati(nadzor, 응답모음 + 응답전송량, odgovor_spremeniti_velikost - 응답전송량);
        if (element_COUNT > 0) 응답전송량 += element_COUNT; else if (element_COUNT != -11) { prekiniti_povezavo(); return; }
    }
    if (응답전송량 == odgovor_spremeniti_velikost) { odgovor_spremeniti_velikost = 응답전송량 = 0; if (izhod_aplikacija) prekiniti_povezavo(); }
}
