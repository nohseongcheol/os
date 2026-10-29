#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "hálózat_Sor.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int fogad_port = -1, vezérlő = -1, kézi_ismerős = -1, adat = -1;
static unsigned 로그인됨, felhasználó_OK, sor_méretez, 줄오류, kilépés_app, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned válasz_méretez, 응답전송량, Tovább_portszám;
static uint32_t Tevékenység;
static char Vonal[256], 응답모음[2048], Fájl_bejegyzés_név[64], átvisz_név[64];
static unsigned char átvisz_Állapot[16384];
static int 같은지(const char *첫째값, const char *MPERC_ÉRTÉK) { while (*첫째값 && *첫째값 == *MPERC_ÉRTÉK) { 첫째값++; MPERC_ÉRTÉK++; } return *첫째값 == *MPERC_ÉRTÉK; }
static void válasz(const char *sztring_adat) {
    size_t cikk_DARAB = strlen(sztring_adat);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, válasz_méretez - 응답전송량); válasz_méretez -= 응답전송량; 응답전송량 = 0; }
    if (cikk_DARAB > sizeof(응답모음) - válasz_méretez) { kilépés_app = 1; return; }
    memcpy(응답모음 + válasz_méretez, sztring_adat, cikk_DARAB); válasz_méretez += cikk_DARAB;
}
static void 수치(unsigned ÉRTÉK, char *KR_adat, unsigned *cikk_DARAB) {
    char számjegy_DARAB[10]; unsigned bejegyzés_DARAB = 0;
    do { számjegy_DARAB[bejegyzés_DARAB++] = '0' + ÉRTÉK % 10; ÉRTÉK /= 10; } while (ÉRTÉK);
    while (bejegyzés_DARAB) KR_adat[(*cikk_DARAB)++] = számjegy_DARAB[--bejegyzés_DARAB];
}
static void Állj_átvisz(void) {
    if (adat >= 0) bezár_hálózat(adat); if (kézi_ismerős >= 0) bezár_hálózat(kézi_ismerős);
    adat = kézi_ismerős = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void megszakít(void) {
    Állj_átvisz(); if (vezérlő >= 0) bezár_hálózat(vezérlő); vezérlő = -1;
    로그인됨 = felhasználó_OK = sor_méretez = 줄오류 = válasz_méretez = 응답전송량 = kilépés_app = 0;
}
int fájlátvitel_vezérlő(int Művelet) {
    if (Művelet == 2) return fogad_port >= 0;
    if (Művelet == 0) { megszakít(); if (fogad_port >= 0) bezár_hálózat(fogad_port); fogad_port = -1; return 0; }
    if (Művelet != 1) return -22; if (fogad_port >= 0) return 0;
    fogad_port = készít_szoftvercsatorna_végpont(1); if (fogad_port < 0) return fogad_port;
    int 반환값 = NET_BIND(fogad_port, 망상태읽기(0,0), 21); if (!반환값) 반환값 = NET_figyelés(fogad_port);
    if (반환값 < 0) { bezár_hálózat(fogad_port); fogad_port = -1; } return 반환값;
}
static int ÚTVONAL(const char *Név) {
    unsigned cikk_DARAB = 0; if (*Név == '/') Név++;
    if (!*Név || 같은지(Név, ".") || 같은지(Név, "..")) return 0;
    Fájl_bejegyzés_név[cikk_DARAB++] = '/';
    while (*Név) {
        unsigned char kódpont = *Név++;
        if (cikk_DARAB >= 63 || kódpont < 32 || kódpont == 127 || kódpont == '/' || kódpont == '\\') return 0;
        Fájl_bejegyzés_név[cikk_DARAB++] = kódpont;
    }
    Fájl_bejegyzés_név[cikk_DARAB] = 0; return 1;
}
static void küld_Lista(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int cikk_DARAB = 자바파일항목길이(순번); if (cikk_DARAB <= 0) continue;
        const char *sorköz_rész = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned bejegyzés_DARAB = strlen(sorköz_rész); memcpy(átvisz_Állapot + 사용량, sorköz_rész, bejegyzés_DARAB); 사용량 += bejegyzés_DARAB;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)átvisz_Állapot, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        bejegyzés_DARAB = strlen(뒷부분); memcpy(átvisz_Állapot + 사용량, 뒷부분, bejegyzés_DARAB); 사용량 += bejegyzés_DARAB;
        for (int 안쪽순번 = 0; 안쪽순번 < cikk_DARAB; 안쪽순번++) átvisz_Állapot[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        átvisz_Állapot[사용량++] = '\r'; átvisz_Állapot[사용량++] = '\n';
    }
}
static void Előkészítés_kézi_ismerős(int 확장여부) {
    if (수행작업) { válasz("450 Transfer in progress\r\n"); return; }
    Állj_átvisz(); kézi_ismerős = készít_szoftvercsatorna_végpont(1);
    if (kézi_ismerős >= 0) 통신주소재사용(kézi_ismerős);
    unsigned portszám = 50000 + Tovább_portszám++ % 8;
    if (kézi_ismerős < 0 || NET_BIND(kézi_ismerős, 망상태읽기(0,0), portszám) || NET_figyelés(kézi_ismerős)) {
        Állj_átvisz(); válasz("425 Cannot open passive listener\r\n"); return;
    }
    char válasz_1262b476[96]; const char *sorköz_rész = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned cikk_DARAB = strlen(sorköz_rész); memcpy(válasz_1262b476, sorköz_rész, cikk_DARAB);
    if (확장여부) { 수치(portszám, válasz_1262b476, &cikk_DARAB); válasz_1262b476[cikk_DARAB++] = '|'; }
    else {
        uint32_t CÍM=망상태읽기(0,0);
        for (int helyzetindex=24;helyzetindex>=0;helyzetindex-=8) { 수치((CÍM>>helyzetindex)&255,válasz_1262b476,&cikk_DARAB);válasz_1262b476[cikk_DARAB++]=','; }
        수치(portszám / 256, válasz_1262b476, &cikk_DARAB); válasz_1262b476[cikk_DARAB++] = ','; 수치(portszám % 256, válasz_1262b476, &cikk_DARAB);
    }
    válasz_1262b476[cikk_DARAB++] = ')'; válasz_1262b476[cikk_DARAB++] = '\r'; válasz_1262b476[cikk_DARAB++] = '\n'; válasz_1262b476[cikk_DARAB] = 0; válasz(válasz_1262b476);
}
static void Parancs(void) {
    Vonal[sor_méretez] = 0;
    char *부가인수 = Vonal; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(Vonal, "QUIT")) { Állj_átvisz(); válasz("221 Goodbye\r\n"); kilépés_app = 1; return; }
    if (같은지(Vonal, "NOOP")) { válasz("200 OK\r\n"); return; }
    if (같은지(Vonal, "SYST")) { válasz("215 UNIX Type: L8\r\n"); return; }
    if (같은지(Vonal, "FEAT")) { válasz("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(Vonal, "USER")) { 로그인됨 = 0; felhasználó_OK = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); válasz(felhasználó_OK ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(Vonal, "PASS")) { 로그인됨 = felhasználó_OK; válasz(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { válasz("530 Login first\r\n"); return; }
    if (같은지(Vonal, "PWD")) válasz("257 \"/\"\r\n");
    else if (같은지(Vonal, "CWD")) válasz(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(Vonal, "TYPE")) válasz(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(Vonal, "OPTS")) válasz(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(Vonal, "PASV")) Előkészítés_kézi_ismerős(0);
    else if (같은지(Vonal, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) válasz("522 IPv4 only\r\n"); else Előkészítés_kézi_ismerős(1); }
    else if (같은지(Vonal, "ABOR")) { Állj_átvisz(); válasz("226 Transfer aborted\r\n"); }
    else if (같은지(Vonal, "DELE")) { válasz(ÚTVONAL(부가인수) && pk_unlink(Fájl_bejegyzés_név) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(Vonal, "LIST") || 같은지(Vonal, "NLST") || 같은지(Vonal, "MLSD")) {
        if (수행작업) { válasz("450 Transfer in progress\r\n"); return; }
        if (kézi_ismerős < 0 && adat < 0) { válasz("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { válasz("550 Root listing only\r\n"); return; }
        küld_Lista(같은지(Vonal,"MLSD") ? 2 : 같은지(Vonal,"LIST") ? 1 : 0); 수행작업 = 2;
        válasz("150 Opening directory listing\r\n");
    }
    else if (같은지(Vonal, "SIZE")) {
        if (!ÚTVONAL(부가인수)) { válasz("550 Invalid filename\r\n"); return; }
        int fájlleíró = pk_open(Fájl_bejegyzés_név, írásvédett_ÉRTÉK, 0); if (fájlleíró < 0) { válasz("550 File unavailable\r\n"); return; }
        int Méret = pk_size(fájlleíró); pk_close(fájlleíró); char válasz_1262b476[32] = "213 "; unsigned cikk_DARAB = 4;
        수치(Méret, válasz_1262b476, &cikk_DARAB); válasz_1262b476[cikk_DARAB++] = '\r'; válasz_1262b476[cikk_DARAB++] = '\n'; válasz_1262b476[cikk_DARAB] = 0; válasz(válasz_1262b476);
    } else if (같은지(Vonal, "STOR") || 같은지(Vonal, "RETR")) {
        if (수행작업) { válasz("450 Transfer in progress\r\n"); return; }
        if (kézi_ismerős < 0 && adat < 0) { válasz("425 Use PASV or EPSV\r\n"); return; }
        if (!ÚTVONAL(부가인수)) { válasz("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(Vonal, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(átvisz_név, Fájl_bejegyzés_név, strlen(Fájl_bejegyzés_név) + 1);
        if (수행작업 == 2) {
            int fájlleíró = pk_open(Fájl_bejegyzés_név, írásvédett_ÉRTÉK, 0);
            if (fájlleíró < 0) { 수행작업 = 0; válasz("550 File unavailable\r\n"); return; }
            int cikk_DARAB = pk_read(fájlleíró, átvisz_Állapot, sizeof(átvisz_Állapot)); pk_close(fájlleíró);
            if (cikk_DARAB < 0) { 수행작업 = 0; válasz("451 Read failed\r\n"); return; } 사용량 = cikk_DARAB;
        }
        válasz("150 Opening binary data connection\r\n");
    } else válasz("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (fogad_port < 0) return;
    int Bejövő_ismerős = NET_elfogad(fogad_port);
    if (Bejövő_ismerős >= 0) {
        if (vezérlő >= 0) { NET_ír(Bejövő_ismerős, "421 One session at a time\r\n", 27); bezár_hálózat(Bejövő_ismerős); }
        else { vezérlő = Bejövő_ismerős; Tevékenység = 보드밀리초(); válasz("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (vezérlő < 0) return;
    if ((uint32_t)(보드밀리초() - Tevékenység) > 60000) { megszakít(); return; }
    if (!kilépés_app) for (unsigned költségkeret = 0; költségkeret < 256; költségkeret++) {
        unsigned char kódpont; int 반환값 = 통신읽기(vezérlő, &kódpont, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { megszakít(); return; } Tevékenység = 보드밀리초();
        if (kódpont == '\n') { if (줄오류) válasz("500 Command too long or invalid\r\n"); else Parancs(); sor_méretez = 줄오류 = 0; if (kilépés_app) break; }
        else if (kódpont != '\r') { if (!kódpont || sor_méretez >= sizeof(Vonal) - 1) 줄오류 = 1; else Vonal[sor_méretez++] = kódpont; }
    }
    if (kézi_ismerős >= 0 && adat < 0) {
        int 반환값 = NET_elfogad(kézi_ismerős);
        if (반환값 >= 0) {
            if (NET_társ_CÍM(반환값) != NET_társ_CÍM(vezérlő)) bezár_hálózat(반환값);
            else { adat = 반환값; bezár_hálózat(kézi_ismerős); kézi_ismerős = -1; Tevékenység = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && adat >= 0) for (unsigned költségkeret = 0; költségkeret < 8; költségkeret++) {
        unsigned char adatblokk[512]; int cikk_DARAB = 통신읽기(adat, adatblokk, sizeof(adatblokk));
        if (cikk_DARAB == -11) break;
        if (cikk_DARAB < 0) { Állj_átvisz(); válasz("426 Data connection failed\r\n"); break; }
        Tevékenység = 보드밀리초();
        if (cikk_DARAB == 0) {
            int KR = -1;
            if (!실패여부) {
                int fájlleíró = pk_open(átvisz_név, 쓰기전용 | 없으면만들기 | vág_Tartalom, 0600);
                if (fájlleíró >= 0) { KR = pk_write(fájlleíró, átvisz_Állapot, 사용량); pk_close(fájlleíró); }
            }
            int 성공여부 = !실패여부 && KR == (int)사용량; Állj_átvisz(); válasz(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)cikk_DARAB > sizeof(átvisz_Állapot) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(átvisz_Állapot + 사용량, adatblokk, cikk_DARAB); 사용량 += cikk_DARAB; }
    }
    if (수행작업 == 2 && adat >= 0) {
        int cikk_DARAB = NET_ír(adat, átvisz_Állapot + 보낸수, 사용량 - 보낸수);
        if (cikk_DARAB >= 0) { 보낸수 += cikk_DARAB; Tevékenység = 보드밀리초(); if (보낸수 == 사용량) { Állj_átvisz(); válasz("226 Transfer complete\r\n"); } }
        else if (cikk_DARAB != -11) { Állj_átvisz(); válasz("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < válasz_méretez) {
        int cikk_DARAB = NET_ír(vezérlő, 응답모음 + 응답전송량, válasz_méretez - 응답전송량);
        if (cikk_DARAB > 0) 응답전송량 += cikk_DARAB; else if (cikk_DARAB != -11) { megszakít(); return; }
    }
    if (응답전송량 == válasz_méretez) { válasz_méretez = 응답전송량 = 0; if (kilépés_app) megszakít(); }
}
