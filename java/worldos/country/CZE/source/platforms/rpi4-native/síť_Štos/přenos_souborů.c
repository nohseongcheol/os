#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "síť_Štos.h"
#include "string.h"
#include "Soubor_ABI.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int dostat_port = -1, řízení = -1, ruční_kontakt = -1, data = -1;
static unsigned 로그인됨, uživatel_OK, čára_změnit_velikost, 줄오류, ukončit_program, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned odezva_změnit_velikost, 응답전송량, Další_číslo_portu;
static uint32_t Aktivita;
static char vstupní_řádek[256], 응답모음[2048], Soubor_položka_název[64], přenos_název[64];
static unsigned char přenos_Stav[16384];
static int 같은지(const char *첫째값, const char *SEKUNDA_HODNOTA) { while (*첫째값 && *첫째값 == *SEKUNDA_HODNOTA) { 첫째값++; SEKUNDA_HODNOTA++; } return *첫째값 == *SEKUNDA_HODNOTA; }
static void odezva(const char *řetězec_data) {
    size_t zboží_POČET = strlen(řetězec_data);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, odezva_změnit_velikost - 응답전송량); odezva_změnit_velikost -= 응답전송량; 응답전송량 = 0; }
    if (zboží_POČET > sizeof(응답모음) - odezva_změnit_velikost) { ukončit_program = 1; return; }
    memcpy(응답모음 + odezva_změnit_velikost, řetězec_data, zboží_POČET); odezva_změnit_velikost += zboží_POČET;
}
static void 수치(unsigned HODNOTA, char *KV_data, unsigned *zboží_POČET) {
    char číslice_POČET[10]; unsigned položka_POČET = 0;
    do { číslice_POČET[položka_POČET++] = '0' + HODNOTA % 10; HODNOTA /= 10; } while (HODNOTA);
    while (položka_POČET) KV_data[(*zboží_POČET)++] = číslice_POČET[--položka_POČET];
}
static void Stop_přenos(void) {
    if (data >= 0) Zavřít_síť(data); if (ruční_kontakt >= 0) Zavřít_síť(ruční_kontakt);
    data = ruční_kontakt = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void odpojit(void) {
    Stop_přenos(); if (řízení >= 0) Zavřít_síť(řízení); řízení = -1;
    로그인됨 = uživatel_OK = čára_změnit_velikost = 줄오류 = odezva_změnit_velikost = 응답전송량 = ukončit_program = 0;
}
int přenos_souborů_řízení(int Akce) {
    if (Akce == 2) return dostat_port >= 0;
    if (Akce == 0) { odpojit(); if (dostat_port >= 0) Zavřít_síť(dostat_port); dostat_port = -1; return 0; }
    if (Akce != 1) return -22; if (dostat_port >= 0) return 0;
    dostat_port = Create_soket_účastník(1); if (dostat_port < 0) return dostat_port;
    int 반환값 = čistý_vázat(dostat_port, 망상태읽기(0,0), 21); if (!반환값) 반환값 = čistý_naslouchat(dostat_port);
    if (반환값 < 0) { Zavřít_síť(dostat_port); dostat_port = -1; } return 반환값;
}
static int cesta_2(const char *Název) {
    unsigned zboží_POČET = 0; if (*Název == '/') Název++;
    if (!*Název || 같은지(Název, ".") || 같은지(Název, "..")) return 0;
    Soubor_položka_název[zboží_POČET++] = '/';
    while (*Název) {
        unsigned char bod_kódu = *Název++;
        if (zboží_POČET >= 63 || bod_kódu < 32 || bod_kódu == 127 || bod_kódu == '/' || bod_kódu == '\\') return 0;
        Soubor_položka_název[zboží_POČET++] = bod_kódu;
    }
    Soubor_položka_název[zboží_POČET] = 0; return 1;
}
static void poslat_Seznam(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int zboží_POČET = 자바파일항목길이(순번); if (zboží_POČET <= 0) continue;
        const char *řádkování_část = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned položka_POČET = strlen(řádkování_část); memcpy(přenos_Stav + 사용량, řádkování_část, položka_POČET); 사용량 += položka_POČET;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)přenos_Stav, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        položka_POČET = strlen(뒷부분); memcpy(přenos_Stav + 사용량, 뒷부분, položka_POČET); 사용량 += položka_POČET;
        for (int 안쪽순번 = 0; 안쪽순번 < zboží_POČET; 안쪽순번++) přenos_Stav[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        přenos_Stav[사용량++] = '\r'; přenos_Stav[사용량++] = '\n';
    }
}
static void Připravit_ruční_kontakt(int 확장여부) {
    if (수행작업) { odezva("450 Transfer in progress\r\n"); return; }
    Stop_přenos(); ruční_kontakt = Create_soket_účastník(1);
    if (ruční_kontakt >= 0) 통신주소재사용(ruční_kontakt);
    unsigned číslo_portu = 50000 + Další_číslo_portu++ % 8;
    if (ruční_kontakt < 0 || čistý_vázat(ruční_kontakt, 망상태읽기(0,0), číslo_portu) || čistý_naslouchat(ruční_kontakt)) {
        Stop_přenos(); odezva("425 Cannot open passive listener\r\n"); return;
    }
    char odpověď[96]; const char *řádkování_část = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned zboží_POČET = strlen(řádkování_část); memcpy(odpověď, řádkování_část, zboží_POČET);
    if (확장여부) { 수치(číslo_portu, odpověď, &zboží_POČET); odpověď[zboží_POČET++] = '|'; }
    else {
        uint32_t Adresa=망상태읽기(0,0);
        for (int poziční_index=24;poziční_index>=0;poziční_index-=8) { 수치((Adresa>>poziční_index)&255,odpověď,&zboží_POČET);odpověď[zboží_POČET++]=','; }
        수치(číslo_portu / 256, odpověď, &zboží_POČET); odpověď[zboží_POČET++] = ','; 수치(číslo_portu % 256, odpověď, &zboží_POČET);
    }
    odpověď[zboží_POČET++] = ')'; odpověď[zboží_POČET++] = '\r'; odpověď[zboží_POČET++] = '\n'; odpověď[zboží_POČET] = 0; odezva(odpověď);
}
static void příkaz(void) {
    vstupní_řádek[čára_změnit_velikost] = 0;
    char *부가인수 = vstupní_řádek; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(vstupní_řádek, "QUIT")) { Stop_přenos(); odezva("221 Goodbye\r\n"); ukončit_program = 1; return; }
    if (같은지(vstupní_řádek, "NOOP")) { odezva("200 OK\r\n"); return; }
    if (같은지(vstupní_řádek, "SYST")) { odezva("215 UNIX Type: L8\r\n"); return; }
    if (같은지(vstupní_řádek, "FEAT")) { odezva("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(vstupní_řádek, "USER")) { 로그인됨 = 0; uživatel_OK = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); odezva(uživatel_OK ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(vstupní_řádek, "PASS")) { 로그인됨 = uživatel_OK; odezva(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { odezva("530 Login first\r\n"); return; }
    if (같은지(vstupní_řádek, "PWD")) odezva("257 \"/\"\r\n");
    else if (같은지(vstupní_řádek, "CWD")) odezva(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(vstupní_řádek, "TYPE")) odezva(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(vstupní_řádek, "OPTS")) odezva(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(vstupní_řádek, "PASV")) Připravit_ruční_kontakt(0);
    else if (같은지(vstupní_řádek, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) odezva("522 IPv4 only\r\n"); else Připravit_ruční_kontakt(1); }
    else if (같은지(vstupní_řádek, "ABOR")) { Stop_přenos(); odezva("226 Transfer aborted\r\n"); }
    else if (같은지(vstupní_řádek, "DELE")) { odezva(cesta_2(부가인수) && pk_unlink(Soubor_položka_název) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(vstupní_řádek, "LIST") || 같은지(vstupní_řádek, "NLST") || 같은지(vstupní_řádek, "MLSD")) {
        if (수행작업) { odezva("450 Transfer in progress\r\n"); return; }
        if (ruční_kontakt < 0 && data < 0) { odezva("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { odezva("550 Root listing only\r\n"); return; }
        poslat_Seznam(같은지(vstupní_řádek,"MLSD") ? 2 : 같은지(vstupní_řádek,"LIST") ? 1 : 0); 수행작업 = 2;
        odezva("150 Opening directory listing\r\n");
    }
    else if (같은지(vstupní_řádek, "SIZE")) {
        if (!cesta_2(부가인수)) { odezva("550 Invalid filename\r\n"); return; }
        int popisovač_souboru = pk_open(Soubor_položka_název, jen_pro_čtení_HODNOTA, 0); if (popisovač_souboru < 0) { odezva("550 File unavailable\r\n"); return; }
        int Velikost = pk_size(popisovač_souboru); pk_close(popisovač_souboru); char odpověď[32] = "213 "; unsigned zboží_POČET = 4;
        수치(Velikost, odpověď, &zboží_POČET); odpověď[zboží_POČET++] = '\r'; odpověď[zboží_POČET++] = '\n'; odpověď[zboží_POČET] = 0; odezva(odpověď);
    } else if (같은지(vstupní_řádek, "STOR") || 같은지(vstupní_řádek, "RETR")) {
        if (수행작업) { odezva("450 Transfer in progress\r\n"); return; }
        if (ruční_kontakt < 0 && data < 0) { odezva("425 Use PASV or EPSV\r\n"); return; }
        if (!cesta_2(부가인수)) { odezva("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(vstupní_řádek, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(přenos_název, Soubor_položka_název, strlen(Soubor_položka_název) + 1);
        if (수행작업 == 2) {
            int popisovač_souboru = pk_open(Soubor_položka_název, jen_pro_čtení_HODNOTA, 0);
            if (popisovač_souboru < 0) { 수행작업 = 0; odezva("550 File unavailable\r\n"); return; }
            int zboží_POČET = pk_read(popisovač_souboru, přenos_Stav, sizeof(přenos_Stav)); pk_close(popisovač_souboru);
            if (zboží_POČET < 0) { 수행작업 = 0; odezva("451 Read failed\r\n"); return; } 사용량 = zboží_POČET;
        }
        odezva("150 Opening binary data connection\r\n");
    } else odezva("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (dostat_port < 0) return;
    int Příchozí_kontakt = čistý_přijmout(dostat_port);
    if (Příchozí_kontakt >= 0) {
        if (řízení >= 0) { čistý_zápis(Příchozí_kontakt, "421 One session at a time\r\n", 27); Zavřít_síť(Příchozí_kontakt); }
        else { řízení = Příchozí_kontakt; Aktivita = 보드밀리초(); odezva("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (řízení < 0) return;
    if ((uint32_t)(보드밀리초() - Aktivita) > 60000) { odpojit(); return; }
    if (!ukončit_program) for (unsigned rozpočet = 0; rozpočet < 256; rozpočet++) {
        unsigned char bod_kódu; int 반환값 = 통신읽기(řízení, &bod_kódu, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { odpojit(); return; } Aktivita = 보드밀리초();
        if (bod_kódu == '\n') { if (줄오류) odezva("500 Command too long or invalid\r\n"); else příkaz(); čára_změnit_velikost = 줄오류 = 0; if (ukončit_program) break; }
        else if (bod_kódu != '\r') { if (!bod_kódu || čára_změnit_velikost >= sizeof(vstupní_řádek) - 1) 줄오류 = 1; else vstupní_řádek[čára_změnit_velikost++] = bod_kódu; }
    }
    if (ruční_kontakt >= 0 && data < 0) {
        int 반환값 = čistý_přijmout(ruční_kontakt);
        if (반환값 >= 0) {
            if (čistý_partner_ODKAZ(반환값) != čistý_partner_ODKAZ(řízení)) Zavřít_síť(반환값);
            else { data = 반환값; Zavřít_síť(ruční_kontakt); ruční_kontakt = -1; Aktivita = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && data >= 0) for (unsigned rozpočet = 0; rozpočet < 8; rozpočet++) {
        unsigned char datový_blok[512]; int zboží_POČET = 통신읽기(data, datový_blok, sizeof(datový_blok));
        if (zboží_POČET == -11) break;
        if (zboží_POČET < 0) { Stop_přenos(); odezva("426 Data connection failed\r\n"); break; }
        Aktivita = 보드밀리초();
        if (zboží_POČET == 0) {
            int VÝSLEDEK = -1;
            if (!실패여부) {
                int popisovač_souboru = pk_open(přenos_název, 쓰기전용 | 없으면만들기 | stříhat_Obsah, 0600);
                if (popisovač_souboru >= 0) { VÝSLEDEK = pk_write(popisovač_souboru, přenos_Stav, 사용량); pk_close(popisovač_souboru); }
            }
            int 성공여부 = !실패여부 && VÝSLEDEK == (int)사용량; Stop_přenos(); odezva(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)zboží_POČET > sizeof(přenos_Stav) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(přenos_Stav + 사용량, datový_blok, zboží_POČET); 사용량 += zboží_POČET; }
    }
    if (수행작업 == 2 && data >= 0) {
        int zboží_POČET = čistý_zápis(data, přenos_Stav + 보낸수, 사용량 - 보낸수);
        if (zboží_POČET >= 0) { 보낸수 += zboží_POČET; Aktivita = 보드밀리초(); if (보낸수 == 사용량) { Stop_přenos(); odezva("226 Transfer complete\r\n"); } }
        else if (zboží_POČET != -11) { Stop_přenos(); odezva("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < odezva_změnit_velikost) {
        int zboží_POČET = čistý_zápis(řízení, 응답모음 + 응답전송량, odezva_změnit_velikost - 응답전송량);
        if (zboží_POČET > 0) 응답전송량 += zboží_POČET; else if (zboží_POČET != -11) { odpojit(); return; }
    }
    if (응답전송량 == odezva_změnit_velikost) { odezva_změnit_velikost = 응답전송량 = 0; if (ukončit_program) odpojit(); }
}
