#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "Mreža_snop.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int 수신창구 = -1, kontrola = -1, ručno_veza = -1, podaci = -1;
static unsigned 로그인됨, korisnik_Uredu, redak_podesiti_veličinu, 줄오류, izađi_program, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned odgovoriti_podesiti_veličinu, 응답전송량, Dalje_broj_priključka;
static uint32_t Aktivnost;
static char Linija[256], 응답모음[2048], fajl_unos_naziv[64], prijenos_naziv[64];
static unsigned char prijenos_stanje[16384];
static int 같은지(const char *첫째값, const char *SECOND_VALUE) { while (*첫째값 && *첫째값 == *SECOND_VALUE) { 첫째값++; SECOND_VALUE++; } return *첫째값 == *SECOND_VALUE; }
static void odgovoriti(const char *string_podaci) {
    size_t stavka_COUNT = strlen(string_podaci);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, odgovoriti_podesiti_veličinu - 응답전송량); odgovoriti_podesiti_veličinu -= 응답전송량; 응답전송량 = 0; }
    if (stavka_COUNT > sizeof(응답모음) - odgovoriti_podesiti_veličinu) { izađi_program = 1; return; }
    memcpy(응답모음 + odgovoriti_podesiti_veličinu, string_podaci, stavka_COUNT); odgovoriti_podesiti_veličinu += stavka_COUNT;
}
static void 수치(unsigned VALUE, char *mjera_podaci, unsigned *stavka_COUNT) {
    char cifra_COUNT[10]; unsigned unos_COUNT = 0;
    do { cifra_COUNT[unos_COUNT++] = '0' + VALUE % 10; VALUE /= 10; } while (VALUE);
    while (unos_COUNT) mjera_podaci[(*stavka_COUNT)++] = cifra_COUNT[--unos_COUNT];
}
static void stati_prijenos(void) {
    if (podaci >= 0) zatvoriti_Mreža(podaci); if (ručno_veza >= 0) zatvoriti_Mreža(ručno_veza);
    podaci = ručno_veza = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void prekinuti_vezu(void) {
    stati_prijenos(); if (kontrola >= 0) zatvoriti_Mreža(kontrola); kontrola = -1;
    로그인됨 = korisnik_Uredu = redak_podesiti_veličinu = 줄오류 = odgovoriti_podesiti_veličinu = 응답전송량 = izađi_program = 0;
}
int fajl_prijenos_kontrola(int radnja) {
    if (radnja == 2) return 수신창구 >= 0;
    if (radnja == 0) { prekinuti_vezu(); if (수신창구 >= 0) zatvoriti_Mreža(수신창구); 수신창구 = -1; return 0; }
    if (radnja != 1) return -22; if (수신창구 >= 0) return 0;
    수신창구 = 통신끝점만들기(1); if (수신창구 < 0) return 수신창구;
    int 반환값 = 망주소묶기(수신창구, 망상태읽기(0,0), 21); if (!반환값) 반환값 = 연결기다리기(수신창구);
    if (반환값 < 0) { zatvoriti_Mreža(수신창구); 수신창구 = -1; } return 반환값;
}
static int Putanja(const char *Naziv) {
    unsigned stavka_COUNT = 0; if (*Naziv == '/') Naziv++;
    if (!*Naziv || 같은지(Naziv, ".") || 같은지(Naziv, "..")) return 0;
    fajl_unos_naziv[stavka_COUNT++] = '/';
    while (*Naziv) {
        unsigned char kôd_znaka = *Naziv++;
        if (stavka_COUNT >= 63 || kôd_znaka < 32 || kôd_znaka == 127 || kôd_znaka == '/' || kôd_znaka == '\\') return 0;
        fajl_unos_naziv[stavka_COUNT++] = kôd_znaka;
    }
    fajl_unos_naziv[stavka_COUNT] = 0; return 1;
}
static void poslati_spisak(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int stavka_COUNT = 자바파일항목길이(순번); if (stavka_COUNT <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned unos_COUNT = strlen(앞부분); memcpy(prijenos_stanje + 사용량, 앞부분, unos_COUNT); 사용량 += unos_COUNT;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)prijenos_stanje, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        unos_COUNT = strlen(뒷부분); memcpy(prijenos_stanje + 사용량, 뒷부분, unos_COUNT); 사용량 += unos_COUNT;
        for (int 안쪽순번 = 0; 안쪽순번 < stavka_COUNT; 안쪽순번++) prijenos_stanje[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        prijenos_stanje[사용량++] = '\r'; prijenos_stanje[사용량++] = '\n';
    }
}
static void Pripremiti_ručno_veza(int 확장여부) {
    if (수행작업) { odgovoriti("450 Transfer in progress\r\n"); return; }
    stati_prijenos(); ručno_veza = 통신끝점만들기(1);
    if (ručno_veza >= 0) 통신주소재사용(ručno_veza);
    unsigned broj_priključka = 50000 + Dalje_broj_priključka++ % 8;
    if (ručno_veza < 0 || 망주소묶기(ručno_veza, 망상태읽기(0,0), broj_priključka) || 연결기다리기(ručno_veza)) {
        stati_prijenos(); odgovoriti("425 Cannot open passive listener\r\n"); return;
    }
    char 응답자료[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned stavka_COUNT = strlen(앞부분); memcpy(응답자료, 앞부분, stavka_COUNT);
    if (확장여부) { 수치(broj_priključka, 응답자료, &stavka_COUNT); 응답자료[stavka_COUNT++] = '|'; }
    else {
        uint32_t adresa=망상태읽기(0,0);
        for (int položaj_INDEX=24;položaj_INDEX>=0;položaj_INDEX-=8) { 수치((adresa>>položaj_INDEX)&255,응답자료,&stavka_COUNT);응답자료[stavka_COUNT++]=','; }
        수치(broj_priključka / 256, 응답자료, &stavka_COUNT); 응답자료[stavka_COUNT++] = ','; 수치(broj_priključka % 256, 응답자료, &stavka_COUNT);
    }
    응답자료[stavka_COUNT++] = ')'; 응답자료[stavka_COUNT++] = '\r'; 응답자료[stavka_COUNT++] = '\n'; 응답자료[stavka_COUNT] = 0; odgovoriti(응답자료);
}
static void Naredba(void) {
    Linija[redak_podesiti_veličinu] = 0;
    char *부가인수 = Linija; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(Linija, "QUIT")) { stati_prijenos(); odgovoriti("221 Goodbye\r\n"); izađi_program = 1; return; }
    if (같은지(Linija, "NOOP")) { odgovoriti("200 OK\r\n"); return; }
    if (같은지(Linija, "SYST")) { odgovoriti("215 UNIX Type: L8\r\n"); return; }
    if (같은지(Linija, "FEAT")) { odgovoriti("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(Linija, "USER")) { 로그인됨 = 0; korisnik_Uredu = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); odgovoriti(korisnik_Uredu ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(Linija, "PASS")) { 로그인됨 = korisnik_Uredu; odgovoriti(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { odgovoriti("530 Login first\r\n"); return; }
    if (같은지(Linija, "PWD")) odgovoriti("257 \"/\"\r\n");
    else if (같은지(Linija, "CWD")) odgovoriti(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(Linija, "TYPE")) odgovoriti(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(Linija, "OPTS")) odgovoriti(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(Linija, "PASV")) Pripremiti_ručno_veza(0);
    else if (같은지(Linija, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) odgovoriti("522 IPv4 only\r\n"); else Pripremiti_ručno_veza(1); }
    else if (같은지(Linija, "ABOR")) { stati_prijenos(); odgovoriti("226 Transfer aborted\r\n"); }
    else if (같은지(Linija, "DELE")) { odgovoriti(Putanja(부가인수) && pk_unlink(fajl_unos_naziv) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(Linija, "LIST") || 같은지(Linija, "NLST") || 같은지(Linija, "MLSD")) {
        if (수행작업) { odgovoriti("450 Transfer in progress\r\n"); return; }
        if (ručno_veza < 0 && podaci < 0) { odgovoriti("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { odgovoriti("550 Root listing only\r\n"); return; }
        poslati_spisak(같은지(Linija,"MLSD") ? 2 : 같은지(Linija,"LIST") ? 1 : 0); 수행작업 = 2;
        odgovoriti("150 Opening directory listing\r\n");
    }
    else if (같은지(Linija, "SIZE")) {
        if (!Putanja(부가인수)) { odgovoriti("550 Invalid filename\r\n"); return; }
        int fajl_hvatište = pk_open(fajl_unos_naziv, samo_za_čitanje_VALUE, 0); if (fajl_hvatište < 0) { odgovoriti("550 File unavailable\r\n"); return; }
        int Veličina = pk_size(fajl_hvatište); pk_close(fajl_hvatište); char 응답자료[32] = "213 "; unsigned stavka_COUNT = 4;
        수치(Veličina, 응답자료, &stavka_COUNT); 응답자료[stavka_COUNT++] = '\r'; 응답자료[stavka_COUNT++] = '\n'; 응답자료[stavka_COUNT] = 0; odgovoriti(응답자료);
    } else if (같은지(Linija, "STOR") || 같은지(Linija, "RETR")) {
        if (수행작업) { odgovoriti("450 Transfer in progress\r\n"); return; }
        if (ručno_veza < 0 && podaci < 0) { odgovoriti("425 Use PASV or EPSV\r\n"); return; }
        if (!Putanja(부가인수)) { odgovoriti("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(Linija, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(prijenos_naziv, fajl_unos_naziv, strlen(fajl_unos_naziv) + 1);
        if (수행작업 == 2) {
            int fajl_hvatište = pk_open(fajl_unos_naziv, samo_za_čitanje_VALUE, 0);
            if (fajl_hvatište < 0) { 수행작업 = 0; odgovoriti("550 File unavailable\r\n"); return; }
            int stavka_COUNT = pk_read(fajl_hvatište, prijenos_stanje, sizeof(prijenos_stanje)); pk_close(fajl_hvatište);
            if (stavka_COUNT < 0) { 수행작업 = 0; odgovoriti("451 Read failed\r\n"); return; } 사용량 = stavka_COUNT;
        }
        odgovoriti("150 Opening binary data connection\r\n");
    } else odgovoriti("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (수신창구 < 0) return;
    int 들어온연결 = 망연결받기(수신창구);
    if (들어온연결 >= 0) {
        if (kontrola >= 0) { 통신쓰기(들어온연결, "421 One session at a time\r\n", 27); zatvoriti_Mreža(들어온연결); }
        else { kontrola = 들어온연결; Aktivnost = 보드밀리초(); odgovoriti("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (kontrola < 0) return;
    if ((uint32_t)(보드밀리초() - Aktivnost) > 60000) { prekinuti_vezu(); return; }
    if (!izađi_program) for (unsigned 처리한도 = 0; 처리한도 < 256; 처리한도++) {
        unsigned char kôd_znaka; int 반환값 = 통신읽기(kontrola, &kôd_znaka, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { prekinuti_vezu(); return; } Aktivnost = 보드밀리초();
        if (kôd_znaka == '\n') { if (줄오류) odgovoriti("500 Command too long or invalid\r\n"); else Naredba(); redak_podesiti_veličinu = 줄오류 = 0; if (izađi_program) break; }
        else if (kôd_znaka != '\r') { if (!kôd_znaka || redak_podesiti_veličinu >= sizeof(Linija) - 1) 줄오류 = 1; else Linija[redak_podesiti_veličinu++] = kôd_znaka; }
    }
    if (ručno_veza >= 0 && podaci < 0) {
        int 반환값 = 망연결받기(ručno_veza);
        if (반환값 >= 0) {
            if (상대통신주소(반환값) != 상대통신주소(kontrola)) zatvoriti_Mreža(반환값);
            else { podaci = 반환값; zatvoriti_Mreža(ručno_veza); ručno_veza = -1; Aktivnost = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && podaci >= 0) for (unsigned 처리한도 = 0; 처리한도 < 8; 처리한도++) {
        unsigned char podaci_blokirati[512]; int stavka_COUNT = 통신읽기(podaci, podaci_blokirati, sizeof(podaci_blokirati));
        if (stavka_COUNT == -11) break;
        if (stavka_COUNT < 0) { stati_prijenos(); odgovoriti("426 Data connection failed\r\n"); break; }
        Aktivnost = 보드밀리초();
        if (stavka_COUNT == 0) {
            int mjera = -1;
            if (!실패여부) {
                int fajl_hvatište = pk_open(prijenos_naziv, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (fajl_hvatište >= 0) { mjera = pk_write(fajl_hvatište, prijenos_stanje, 사용량); pk_close(fajl_hvatište); }
            }
            int 성공여부 = !실패여부 && mjera == (int)사용량; stati_prijenos(); odgovoriti(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)stavka_COUNT > sizeof(prijenos_stanje) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(prijenos_stanje + 사용량, podaci_blokirati, stavka_COUNT); 사용량 += stavka_COUNT; }
    }
    if (수행작업 == 2 && podaci >= 0) {
        int stavka_COUNT = 통신쓰기(podaci, prijenos_stanje + 보낸수, 사용량 - 보낸수);
        if (stavka_COUNT >= 0) { 보낸수 += stavka_COUNT; Aktivnost = 보드밀리초(); if (보낸수 == 사용량) { stati_prijenos(); odgovoriti("226 Transfer complete\r\n"); } }
        else if (stavka_COUNT != -11) { stati_prijenos(); odgovoriti("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < odgovoriti_podesiti_veličinu) {
        int stavka_COUNT = 통신쓰기(kontrola, 응답모음 + 응답전송량, odgovoriti_podesiti_veličinu - 응답전송량);
        if (stavka_COUNT > 0) 응답전송량 += stavka_COUNT; else if (stavka_COUNT != -11) { prekinuti_vezu(); return; }
    }
    if (응답전송량 == odgovoriti_podesiti_veličinu) { odgovoriti_podesiti_veličinu = 응답전송량 = 0; if (izađi_program) prekinuti_vezu(); }
}
