#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "netværk_Stak.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int modtage_port = -1, kontrol = -1, manuel_forbindelse = -1, data = -1;
static unsigned 로그인됨, bruger_OK, linje_tilpasse_størrelse, 줄오류, afslut_app, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned svar_tilpasse_størrelse, 응답전송량, Næste_portnummer;
static uint32_t Aktivitet;
static char Linje[256], 응답모음[2048], fil_post_navn[64], overføre_navn[64];
static unsigned char overføre_status[16384];
static int 같은지(const char *첫째값, const char *SEKUND_VÆRDI) { while (*첫째값 && *첫째값 == *SEKUND_VÆRDI) { 첫째값++; SEKUND_VÆRDI++; } return *첫째값 == *SEKUND_VÆRDI; }
static void svar(const char *streng_data) {
    size_t vare_TÆL = strlen(streng_data);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, svar_tilpasse_størrelse - 응답전송량); svar_tilpasse_størrelse -= 응답전송량; 응답전송량 = 0; }
    if (vare_TÆL > sizeof(응답모음) - svar_tilpasse_størrelse) { afslut_app = 1; return; }
    memcpy(응답모음 + svar_tilpasse_størrelse, streng_data, vare_TÆL); svar_tilpasse_størrelse += vare_TÆL;
}
static void 수치(unsigned VÆRDI, char *KR_data, unsigned *vare_TÆL) {
    char ciffer_TÆL[10]; unsigned post_TÆL_8f7753a1 = 0;
    do { ciffer_TÆL[post_TÆL_8f7753a1++] = '0' + VÆRDI % 10; VÆRDI /= 10; } while (VÆRDI);
    while (post_TÆL_8f7753a1) KR_data[(*vare_TÆL)++] = ciffer_TÆL[--post_TÆL_8f7753a1];
}
static void Stop_overføre(void) {
    if (data >= 0) Luk_netværk(data); if (manuel_forbindelse >= 0) Luk_netværk(manuel_forbindelse);
    data = manuel_forbindelse = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void afbryde_forbindelsen(void) {
    Stop_overføre(); if (kontrol >= 0) Luk_netværk(kontrol); kontrol = -1;
    로그인됨 = bruger_OK = linje_tilpasse_størrelse = 줄오류 = svar_tilpasse_størrelse = 응답전송량 = afslut_app = 0;
}
int filoverførsel_kontrol(int Handling) {
    if (Handling == 2) return modtage_port >= 0;
    if (Handling == 0) { afbryde_forbindelsen(); if (modtage_port >= 0) Luk_netværk(modtage_port); modtage_port = -1; return 0; }
    if (Handling != 1) return -22; if (modtage_port >= 0) return 0;
    modtage_port = åbne_socket_slutpunkt(1); if (modtage_port < 0) return modtage_port;
    int 반환값 = NET_BIND(modtage_port, 망상태읽기(0,0), 21); if (!반환값) 반환값 = NET_lytte(modtage_port);
    if (반환값 < 0) { Luk_netværk(modtage_port); modtage_port = -1; } return 반환값;
}
static int Sti(const char *Navn) {
    unsigned vare_TÆL = 0; if (*Navn == '/') Navn++;
    if (!*Navn || 같은지(Navn, ".") || 같은지(Navn, "..")) return 0;
    fil_post_navn[vare_TÆL++] = '/';
    while (*Navn) {
        unsigned char tegnkode = *Navn++;
        if (vare_TÆL >= 63 || tegnkode < 32 || tegnkode == 127 || tegnkode == '/' || tegnkode == '\\') return 0;
        fil_post_navn[vare_TÆL++] = tegnkode;
    }
    fil_post_navn[vare_TÆL] = 0; return 1;
}
static void maile_Liste(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int vare_TÆL = 자바파일항목길이(순번); if (vare_TÆL <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned post_TÆL_8f7753a1 = strlen(앞부분); memcpy(overføre_status + 사용량, 앞부분, post_TÆL_8f7753a1); 사용량 += post_TÆL_8f7753a1;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)overføre_status, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        post_TÆL_8f7753a1 = strlen(뒷부분); memcpy(overføre_status + 사용량, 뒷부분, post_TÆL_8f7753a1); 사용량 += post_TÆL_8f7753a1;
        for (int 안쪽순번 = 0; 안쪽순번 < vare_TÆL; 안쪽순번++) overføre_status[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        overføre_status[사용량++] = '\r'; overføre_status[사용량++] = '\n';
    }
}
static void Tilrettelæg_manuel_forbindelse(int 확장여부) {
    if (수행작업) { svar("450 Transfer in progress\r\n"); return; }
    Stop_overføre(); manuel_forbindelse = åbne_socket_slutpunkt(1);
    if (manuel_forbindelse >= 0) 통신주소재사용(manuel_forbindelse);
    unsigned portnummer = 50000 + Næste_portnummer++ % 8;
    if (manuel_forbindelse < 0 || NET_BIND(manuel_forbindelse, 망상태읽기(0,0), portnummer) || NET_lytte(manuel_forbindelse)) {
        Stop_overføre(); svar("425 Cannot open passive listener\r\n"); return;
    }
    char svar_1262b476[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned vare_TÆL = strlen(앞부분); memcpy(svar_1262b476, 앞부분, vare_TÆL);
    if (확장여부) { 수치(portnummer, svar_1262b476, &vare_TÆL); svar_1262b476[vare_TÆL++] = '|'; }
    else {
        uint32_t mail=망상태읽기(0,0);
        for (int positionsindeks=24;positionsindeks>=0;positionsindeks-=8) { 수치((mail>>positionsindeks)&255,svar_1262b476,&vare_TÆL);svar_1262b476[vare_TÆL++]=','; }
        수치(portnummer / 256, svar_1262b476, &vare_TÆL); svar_1262b476[vare_TÆL++] = ','; 수치(portnummer % 256, svar_1262b476, &vare_TÆL);
    }
    svar_1262b476[vare_TÆL++] = ')'; svar_1262b476[vare_TÆL++] = '\r'; svar_1262b476[vare_TÆL++] = '\n'; svar_1262b476[vare_TÆL] = 0; svar(svar_1262b476);
}
static void Kommando(void) {
    Linje[linje_tilpasse_størrelse] = 0;
    char *부가인수 = Linje; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(Linje, "QUIT")) { Stop_overføre(); svar("221 Goodbye\r\n"); afslut_app = 1; return; }
    if (같은지(Linje, "NOOP")) { svar("200 OK\r\n"); return; }
    if (같은지(Linje, "SYST")) { svar("215 UNIX Type: L8\r\n"); return; }
    if (같은지(Linje, "FEAT")) { svar("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(Linje, "USER")) { 로그인됨 = 0; bruger_OK = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); svar(bruger_OK ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(Linje, "PASS")) { 로그인됨 = bruger_OK; svar(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { svar("530 Login first\r\n"); return; }
    if (같은지(Linje, "PWD")) svar("257 \"/\"\r\n");
    else if (같은지(Linje, "CWD")) svar(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(Linje, "TYPE")) svar(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(Linje, "OPTS")) svar(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(Linje, "PASV")) Tilrettelæg_manuel_forbindelse(0);
    else if (같은지(Linje, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) svar("522 IPv4 only\r\n"); else Tilrettelæg_manuel_forbindelse(1); }
    else if (같은지(Linje, "ABOR")) { Stop_overføre(); svar("226 Transfer aborted\r\n"); }
    else if (같은지(Linje, "DELE")) { svar(Sti(부가인수) && pk_unlink(fil_post_navn) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(Linje, "LIST") || 같은지(Linje, "NLST") || 같은지(Linje, "MLSD")) {
        if (수행작업) { svar("450 Transfer in progress\r\n"); return; }
        if (manuel_forbindelse < 0 && data < 0) { svar("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { svar("550 Root listing only\r\n"); return; }
        maile_Liste(같은지(Linje,"MLSD") ? 2 : 같은지(Linje,"LIST") ? 1 : 0); 수행작업 = 2;
        svar("150 Opening directory listing\r\n");
    }
    else if (같은지(Linje, "SIZE")) {
        if (!Sti(부가인수)) { svar("550 Invalid filename\r\n"); return; }
        int fil_handle = pk_open(fil_post_navn, skrivebeskyttet_VÆRDI, 0); if (fil_handle < 0) { svar("550 File unavailable\r\n"); return; }
        int Størrelse = pk_size(fil_handle); pk_close(fil_handle); char svar_1262b476[32] = "213 "; unsigned vare_TÆL = 4;
        수치(Størrelse, svar_1262b476, &vare_TÆL); svar_1262b476[vare_TÆL++] = '\r'; svar_1262b476[vare_TÆL++] = '\n'; svar_1262b476[vare_TÆL] = 0; svar(svar_1262b476);
    } else if (같은지(Linje, "STOR") || 같은지(Linje, "RETR")) {
        if (수행작업) { svar("450 Transfer in progress\r\n"); return; }
        if (manuel_forbindelse < 0 && data < 0) { svar("425 Use PASV or EPSV\r\n"); return; }
        if (!Sti(부가인수)) { svar("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(Linje, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(overføre_navn, fil_post_navn, strlen(fil_post_navn) + 1);
        if (수행작업 == 2) {
            int fil_handle = pk_open(fil_post_navn, skrivebeskyttet_VÆRDI, 0);
            if (fil_handle < 0) { 수행작업 = 0; svar("550 File unavailable\r\n"); return; }
            int vare_TÆL = pk_read(fil_handle, overføre_status, sizeof(overføre_status)); pk_close(fil_handle);
            if (vare_TÆL < 0) { 수행작업 = 0; svar("451 Read failed\r\n"); return; } 사용량 = vare_TÆL;
        }
        svar("150 Opening binary data connection\r\n");
    } else svar("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (modtage_port < 0) return;
    int Indgående_forbindelse = NET_acceptere(modtage_port);
    if (Indgående_forbindelse >= 0) {
        if (kontrol >= 0) { NET_skrive(Indgående_forbindelse, "421 One session at a time\r\n", 27); Luk_netværk(Indgående_forbindelse); }
        else { kontrol = Indgående_forbindelse; Aktivitet = 보드밀리초(); svar("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (kontrol < 0) return;
    if ((uint32_t)(보드밀리초() - Aktivitet) > 60000) { afbryde_forbindelsen(); return; }
    if (!afslut_app) for (unsigned budget = 0; budget < 256; budget++) {
        unsigned char tegnkode; int 반환값 = 통신읽기(kontrol, &tegnkode, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { afbryde_forbindelsen(); return; } Aktivitet = 보드밀리초();
        if (tegnkode == '\n') { if (줄오류) svar("500 Command too long or invalid\r\n"); else Kommando(); linje_tilpasse_størrelse = 줄오류 = 0; if (afslut_app) break; }
        else if (tegnkode != '\r') { if (!tegnkode || linje_tilpasse_størrelse >= sizeof(Linje) - 1) 줄오류 = 1; else Linje[linje_tilpasse_størrelse++] = tegnkode; }
    }
    if (manuel_forbindelse >= 0 && data < 0) {
        int 반환값 = NET_acceptere(manuel_forbindelse);
        if (반환값 >= 0) {
            if (NET_peer_mail(반환값) != NET_peer_mail(kontrol)) Luk_netværk(반환값);
            else { data = 반환값; Luk_netværk(manuel_forbindelse); manuel_forbindelse = -1; Aktivitet = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && data >= 0) for (unsigned budget = 0; budget < 8; budget++) {
        unsigned char datablok[512]; int vare_TÆL = 통신읽기(data, datablok, sizeof(datablok));
        if (vare_TÆL == -11) break;
        if (vare_TÆL < 0) { Stop_overføre(); svar("426 Data connection failed\r\n"); break; }
        Aktivitet = 보드밀리초();
        if (vare_TÆL == 0) {
            int KR = -1;
            if (!실패여부) {
                int fil_handle = pk_open(overføre_navn, 쓰기전용 | 없으면만들기 | afkorte_Indhold, 0600);
                if (fil_handle >= 0) { KR = pk_write(fil_handle, overføre_status, 사용량); pk_close(fil_handle); }
            }
            int 성공여부 = !실패여부 && KR == (int)사용량; Stop_overføre(); svar(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)vare_TÆL > sizeof(overføre_status) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(overføre_status + 사용량, datablok, vare_TÆL); 사용량 += vare_TÆL; }
    }
    if (수행작업 == 2 && data >= 0) {
        int vare_TÆL = NET_skrive(data, overføre_status + 보낸수, 사용량 - 보낸수);
        if (vare_TÆL >= 0) { 보낸수 += vare_TÆL; Aktivitet = 보드밀리초(); if (보낸수 == 사용량) { Stop_overføre(); svar("226 Transfer complete\r\n"); } }
        else if (vare_TÆL != -11) { Stop_overføre(); svar("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < svar_tilpasse_størrelse) {
        int vare_TÆL = NET_skrive(kontrol, 응답모음 + 응답전송량, svar_tilpasse_størrelse - 응답전송량);
        if (vare_TÆL > 0) 응답전송량 += vare_TÆL; else if (vare_TÆL != -11) { afbryde_forbindelsen(); return; }
    }
    if (응답전송량 == svar_tilpasse_størrelse) { svar_tilpasse_størrelse = 응답전송량 = 0; if (afslut_app) afbryde_forbindelsen(); }
}
