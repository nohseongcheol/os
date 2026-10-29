#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "nettverk_stakk.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int motta_port = -1, kontroll = -1, manuell_kontakt = -1, data = -1;
static unsigned 로그인됨, bruker_OK, linje_skalere, 줄오류, avslutt_app, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned svar_skalere, 응답전송량, Neste_portnummer;
static uint32_t Aktivitet;
static char Linje[256], 응답모음[2048], Fil_oppføring_navn[64], overføre_navn[64];
static unsigned char overføre_status[16384];
static int 같은지(const char *첫째값, const char *SEKUND_VERDI) { while (*첫째값 && *첫째값 == *SEKUND_VERDI) { 첫째값++; SEKUND_VERDI++; } return *첫째값 == *SEKUND_VERDI; }
static void svar(const char *streng_data) {
    size_t vare_ANTALL = strlen(streng_data);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, svar_skalere - 응답전송량); svar_skalere -= 응답전송량; 응답전송량 = 0; }
    if (vare_ANTALL > sizeof(응답모음) - svar_skalere) { avslutt_app = 1; return; }
    memcpy(응답모음 + svar_skalere, streng_data, vare_ANTALL); svar_skalere += vare_ANTALL;
}
static void 수치(unsigned VERDI, char *KR_data, unsigned *vare_ANTALL) {
    char siffer_ANTALL[10]; unsigned oppføring_ANTALL = 0;
    do { siffer_ANTALL[oppføring_ANTALL++] = '0' + VERDI % 10; VERDI /= 10; } while (VERDI);
    while (oppføring_ANTALL) KR_data[(*vare_ANTALL)++] = siffer_ANTALL[--oppføring_ANTALL];
}
static void Stopp_overføre(void) {
    if (data >= 0) Lukk_nettverk(data); if (manuell_kontakt >= 0) Lukk_nettverk(manuell_kontakt);
    data = manuell_kontakt = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void legg_på(void) {
    Stopp_overføre(); if (kontroll >= 0) Lukk_nettverk(kontroll); kontroll = -1;
    로그인됨 = bruker_OK = linje_skalere = 줄오류 = svar_skalere = 응답전송량 = avslutt_app = 0;
}
int filoverføring_kontroll(int Handling) {
    if (Handling == 2) return motta_port >= 0;
    if (Handling == 0) { legg_på(); if (motta_port >= 0) Lukk_nettverk(motta_port); motta_port = -1; return 0; }
    if (Handling != 1) return -22; if (motta_port >= 0) return 0;
    motta_port = åpne_socket_deltaker(1); if (motta_port < 0) return motta_port;
    int 반환값 = netto_BIND(motta_port, 망상태읽기(0,0), 21); if (!반환값) 반환값 = 연결기다리기(motta_port);
    if (반환값 < 0) { Lukk_nettverk(motta_port); motta_port = -1; } return 반환값;
}
static int Sti(const char *Navn) {
    unsigned vare_ANTALL = 0; if (*Navn == '/') Navn++;
    if (!*Navn || 같은지(Navn, ".") || 같은지(Navn, "..")) return 0;
    Fil_oppføring_navn[vare_ANTALL++] = '/';
    while (*Navn) {
        unsigned char tegnkode = *Navn++;
        if (vare_ANTALL >= 63 || tegnkode < 32 || tegnkode == 127 || tegnkode == '/' || tegnkode == '\\') return 0;
        Fil_oppføring_navn[vare_ANTALL++] = tegnkode;
    }
    Fil_oppføring_navn[vare_ANTALL] = 0; return 1;
}
static void sende_Liste(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int vare_ANTALL = 자바파일항목길이(순번); if (vare_ANTALL <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned oppføring_ANTALL = strlen(앞부분); memcpy(overføre_status + 사용량, 앞부분, oppføring_ANTALL); 사용량 += oppføring_ANTALL;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)overføre_status, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        oppføring_ANTALL = strlen(뒷부분); memcpy(overføre_status + 사용량, 뒷부분, oppføring_ANTALL); 사용량 += oppføring_ANTALL;
        for (int 안쪽순번 = 0; 안쪽순번 < vare_ANTALL; 안쪽순번++) overføre_status[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        overføre_status[사용량++] = '\r'; overføre_status[사용량++] = '\n';
    }
}
static void Forbered_manuell_kontakt(int 확장여부) {
    if (수행작업) { svar("450 Transfer in progress\r\n"); return; }
    Stopp_overføre(); manuell_kontakt = åpne_socket_deltaker(1);
    if (manuell_kontakt >= 0) 통신주소재사용(manuell_kontakt);
    unsigned portnummer = 50000 + Neste_portnummer++ % 8;
    if (manuell_kontakt < 0 || netto_BIND(manuell_kontakt, 망상태읽기(0,0), portnummer) || 연결기다리기(manuell_kontakt)) {
        Stopp_overføre(); svar("425 Cannot open passive listener\r\n"); return;
    }
    char svar_1262b476[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned vare_ANTALL = strlen(앞부분); memcpy(svar_1262b476, 앞부분, vare_ANTALL);
    if (확장여부) { 수치(portnummer, svar_1262b476, &vare_ANTALL); svar_1262b476[vare_ANTALL++] = '|'; }
    else {
        uint32_t e_post=망상태읽기(0,0);
        for (int posisjonsindeks=24;posisjonsindeks>=0;posisjonsindeks-=8) { 수치((e_post>>posisjonsindeks)&255,svar_1262b476,&vare_ANTALL);svar_1262b476[vare_ANTALL++]=','; }
        수치(portnummer / 256, svar_1262b476, &vare_ANTALL); svar_1262b476[vare_ANTALL++] = ','; 수치(portnummer % 256, svar_1262b476, &vare_ANTALL);
    }
    svar_1262b476[vare_ANTALL++] = ')'; svar_1262b476[vare_ANTALL++] = '\r'; svar_1262b476[vare_ANTALL++] = '\n'; svar_1262b476[vare_ANTALL] = 0; svar(svar_1262b476);
}
static void Kommando(void) {
    Linje[linje_skalere] = 0;
    char *부가인수 = Linje; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(Linje, "QUIT")) { Stopp_overføre(); svar("221 Goodbye\r\n"); avslutt_app = 1; return; }
    if (같은지(Linje, "NOOP")) { svar("200 OK\r\n"); return; }
    if (같은지(Linje, "SYST")) { svar("215 UNIX Type: L8\r\n"); return; }
    if (같은지(Linje, "FEAT")) { svar("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(Linje, "USER")) { 로그인됨 = 0; bruker_OK = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); svar(bruker_OK ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(Linje, "PASS")) { 로그인됨 = bruker_OK; svar(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { svar("530 Login first\r\n"); return; }
    if (같은지(Linje, "PWD")) svar("257 \"/\"\r\n");
    else if (같은지(Linje, "CWD")) svar(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(Linje, "TYPE")) svar(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(Linje, "OPTS")) svar(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(Linje, "PASV")) Forbered_manuell_kontakt(0);
    else if (같은지(Linje, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) svar("522 IPv4 only\r\n"); else Forbered_manuell_kontakt(1); }
    else if (같은지(Linje, "ABOR")) { Stopp_overføre(); svar("226 Transfer aborted\r\n"); }
    else if (같은지(Linje, "DELE")) { svar(Sti(부가인수) && pk_unlink(Fil_oppføring_navn) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(Linje, "LIST") || 같은지(Linje, "NLST") || 같은지(Linje, "MLSD")) {
        if (수행작업) { svar("450 Transfer in progress\r\n"); return; }
        if (manuell_kontakt < 0 && data < 0) { svar("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { svar("550 Root listing only\r\n"); return; }
        sende_Liste(같은지(Linje,"MLSD") ? 2 : 같은지(Linje,"LIST") ? 1 : 0); 수행작업 = 2;
        svar("150 Opening directory listing\r\n");
    }
    else if (같은지(Linje, "SIZE")) {
        if (!Sti(부가인수)) { svar("550 Invalid filename\r\n"); return; }
        int Fil_håndtak = pk_open(Fil_oppføring_navn, skrivebeskyttet_VERDI, 0); if (Fil_håndtak < 0) { svar("550 File unavailable\r\n"); return; }
        int Størrelse = pk_size(Fil_håndtak); pk_close(Fil_håndtak); char svar_1262b476[32] = "213 "; unsigned vare_ANTALL = 4;
        수치(Størrelse, svar_1262b476, &vare_ANTALL); svar_1262b476[vare_ANTALL++] = '\r'; svar_1262b476[vare_ANTALL++] = '\n'; svar_1262b476[vare_ANTALL] = 0; svar(svar_1262b476);
    } else if (같은지(Linje, "STOR") || 같은지(Linje, "RETR")) {
        if (수행작업) { svar("450 Transfer in progress\r\n"); return; }
        if (manuell_kontakt < 0 && data < 0) { svar("425 Use PASV or EPSV\r\n"); return; }
        if (!Sti(부가인수)) { svar("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(Linje, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(overføre_navn, Fil_oppføring_navn, strlen(Fil_oppføring_navn) + 1);
        if (수행작업 == 2) {
            int Fil_håndtak = pk_open(Fil_oppføring_navn, skrivebeskyttet_VERDI, 0);
            if (Fil_håndtak < 0) { 수행작업 = 0; svar("550 File unavailable\r\n"); return; }
            int vare_ANTALL = pk_read(Fil_håndtak, overføre_status, sizeof(overføre_status)); pk_close(Fil_håndtak);
            if (vare_ANTALL < 0) { 수행작업 = 0; svar("451 Read failed\r\n"); return; } 사용량 = vare_ANTALL;
        }
        svar("150 Opening binary data connection\r\n");
    } else svar("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (motta_port < 0) return;
    int Innkommende_kontakt = netto_godta(motta_port);
    if (Innkommende_kontakt >= 0) {
        if (kontroll >= 0) { netto_skrive(Innkommende_kontakt, "421 One session at a time\r\n", 27); Lukk_nettverk(Innkommende_kontakt); }
        else { kontroll = Innkommende_kontakt; Aktivitet = 보드밀리초(); svar("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (kontroll < 0) return;
    if ((uint32_t)(보드밀리초() - Aktivitet) > 60000) { legg_på(); return; }
    if (!avslutt_app) for (unsigned budsjett = 0; budsjett < 256; budsjett++) {
        unsigned char tegnkode; int 반환값 = 통신읽기(kontroll, &tegnkode, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { legg_på(); return; } Aktivitet = 보드밀리초();
        if (tegnkode == '\n') { if (줄오류) svar("500 Command too long or invalid\r\n"); else Kommando(); linje_skalere = 줄오류 = 0; if (avslutt_app) break; }
        else if (tegnkode != '\r') { if (!tegnkode || linje_skalere >= sizeof(Linje) - 1) 줄오류 = 1; else Linje[linje_skalere++] = tegnkode; }
    }
    if (manuell_kontakt >= 0 && data < 0) {
        int 반환값 = netto_godta(manuell_kontakt);
        if (반환값 >= 0) {
            if (netto_node_e_post(반환값) != netto_node_e_post(kontroll)) Lukk_nettverk(반환값);
            else { data = 반환값; Lukk_nettverk(manuell_kontakt); manuell_kontakt = -1; Aktivitet = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && data >= 0) for (unsigned budsjett = 0; budsjett < 8; budsjett++) {
        unsigned char data_blokk[512]; int vare_ANTALL = 통신읽기(data, data_blokk, sizeof(data_blokk));
        if (vare_ANTALL == -11) break;
        if (vare_ANTALL < 0) { Stopp_overføre(); svar("426 Data connection failed\r\n"); break; }
        Aktivitet = 보드밀리초();
        if (vare_ANTALL == 0) {
            int KR = -1;
            if (!실패여부) {
                int Fil_håndtak = pk_open(overføre_navn, 쓰기전용 | 없으면만들기 | avkorte_Innhold, 0600);
                if (Fil_håndtak >= 0) { KR = pk_write(Fil_håndtak, overføre_status, 사용량); pk_close(Fil_håndtak); }
            }
            int 성공여부 = !실패여부 && KR == (int)사용량; Stopp_overføre(); svar(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)vare_ANTALL > sizeof(overføre_status) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(overføre_status + 사용량, data_blokk, vare_ANTALL); 사용량 += vare_ANTALL; }
    }
    if (수행작업 == 2 && data >= 0) {
        int vare_ANTALL = netto_skrive(data, overføre_status + 보낸수, 사용량 - 보낸수);
        if (vare_ANTALL >= 0) { 보낸수 += vare_ANTALL; Aktivitet = 보드밀리초(); if (보낸수 == 사용량) { Stopp_overføre(); svar("226 Transfer complete\r\n"); } }
        else if (vare_ANTALL != -11) { Stopp_overføre(); svar("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < svar_skalere) {
        int vare_ANTALL = netto_skrive(kontroll, 응답모음 + 응답전송량, svar_skalere - 응답전송량);
        if (vare_ANTALL > 0) 응답전송량 += vare_ANTALL; else if (vare_ANTALL != -11) { legg_på(); return; }
    }
    if (응답전송량 == svar_skalere) { svar_skalere = 응답전송량 = 0; if (avslutt_app) legg_på(); }
}
