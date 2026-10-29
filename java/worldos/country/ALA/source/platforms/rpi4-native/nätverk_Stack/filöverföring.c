#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "nätverk_Stack.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int få_port = -1, kontroll = -1, manuell_kontakt = -1, data = -1;
static unsigned 로그인됨, användare_OK, rad_storlek, 줄오류, avsluta_app, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned svara_storlek, 응답전송량, Nästa_portnummer;
static uint32_t Aktivitet;
static char inmatningsrad[256], 응답모음[2048], fil_post_namn[64], Överför_namn[64];
static unsigned char Överför_status[16384];
static int 같은지(const char *첫째값, const char *SEKUND_värde) { while (*첫째값 && *첫째값 == *SEKUND_värde) { 첫째값++; SEKUND_värde++; } return *첫째값 == *SEKUND_värde; }
static void svara(const char *sträng_data) {
    size_t objekt_ANTAL = strlen(sträng_data);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, svara_storlek - 응답전송량); svara_storlek -= 응답전송량; 응답전송량 = 0; }
    if (objekt_ANTAL > sizeof(응답모음) - svara_storlek) { avsluta_app = 1; return; }
    memcpy(응답모음 + svara_storlek, sträng_data, objekt_ANTAL); svara_storlek += objekt_ANTAL;
}
static void 수치(unsigned värde, char *KR_data, unsigned *objekt_ANTAL) {
    char siffra_ANTAL[10]; unsigned post_ANTAL = 0;
    do { siffra_ANTAL[post_ANTAL++] = '0' + värde % 10; värde /= 10; } while (värde);
    while (post_ANTAL) KR_data[(*objekt_ANTAL)++] = siffra_ANTAL[--post_ANTAL];
}
static void Stopp_Överför(void) {
    if (data >= 0) Stäng_nätverk(data); if (manuell_kontakt >= 0) Stäng_nätverk(manuell_kontakt);
    data = manuell_kontakt = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void koppla_från(void) {
    Stopp_Överför(); if (kontroll >= 0) Stäng_nätverk(kontroll); kontroll = -1;
    로그인됨 = användare_OK = rad_storlek = 줄오류 = svara_storlek = 응답전송량 = avsluta_app = 0;
}
int filöverföring_kontroll(int Åtgärd) {
    if (Åtgärd == 2) return få_port >= 0;
    if (Åtgärd == 0) { koppla_från(); if (få_port >= 0) Stäng_nätverk(få_port); få_port = -1; return 0; }
    if (Åtgärd != 1) return -22; if (få_port >= 0) return 0;
    få_port = Skapa_socket_deltagare(1); if (få_port < 0) return få_port;
    int 반환값 = NET_BIND(få_port, läsa_nätverk_status(0,0), 21); if (!반환값) 반환값 = NET_lyssna(få_port);
    if (반환값 < 0) { Stäng_nätverk(få_port); få_port = -1; } return 반환값;
}
static int sökväg_2(const char *Namn) {
    unsigned objekt_ANTAL = 0; if (*Namn == '/') Namn++;
    if (!*Namn || 같은지(Namn, ".") || 같은지(Namn, "..")) return 0;
    fil_post_namn[objekt_ANTAL++] = '/';
    while (*Namn) {
        unsigned char kodpunkt = *Namn++;
        if (objekt_ANTAL >= 63 || kodpunkt < 32 || kodpunkt == 127 || kodpunkt == '/' || kodpunkt == '\\') return 0;
        fil_post_namn[objekt_ANTAL++] = kodpunkt;
    }
    fil_post_namn[objekt_ANTAL] = 0; return 1;
}
static void skicka_ange(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int objekt_ANTAL = 자바파일항목길이(순번); if (objekt_ANTAL <= 0) continue;
        const char *avstånd_del = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned post_ANTAL = strlen(avstånd_del); memcpy(Överför_status + 사용량, avstånd_del, post_ANTAL); 사용량 += post_ANTAL;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)Överför_status, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        post_ANTAL = strlen(뒷부분); memcpy(Överför_status + 사용량, 뒷부분, post_ANTAL); 사용량 += post_ANTAL;
        for (int 안쪽순번 = 0; 안쪽순번 < objekt_ANTAL; 안쪽순번++) Överför_status[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        Överför_status[사용량++] = '\r'; Överför_status[사용량++] = '\n';
    }
}
static void Förbereda_manuell_kontakt(int 확장여부) {
    if (수행작업) { svara("450 Transfer in progress\r\n"); return; }
    Stopp_Överför(); manuell_kontakt = Skapa_socket_deltagare(1);
    if (manuell_kontakt >= 0) 통신주소재사용(manuell_kontakt);
    unsigned portnummer = 50000 + Nästa_portnummer++ % 8;
    if (manuell_kontakt < 0 || NET_BIND(manuell_kontakt, läsa_nätverk_status(0,0), portnummer) || NET_lyssna(manuell_kontakt)) {
        Stopp_Överför(); svara("425 Cannot open passive listener\r\n"); return;
    }
    char svar[96]; const char *avstånd_del = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned objekt_ANTAL = strlen(avstånd_del); memcpy(svar, avstånd_del, objekt_ANTAL);
    if (확장여부) { 수치(portnummer, svar, &objekt_ANTAL); svar[objekt_ANTAL++] = '|'; }
    else {
        uint32_t Adress=läsa_nätverk_status(0,0);
        for (int positionsindex=24;positionsindex>=0;positionsindex-=8) { 수치((Adress>>positionsindex)&255,svar,&objekt_ANTAL);svar[objekt_ANTAL++]=','; }
        수치(portnummer / 256, svar, &objekt_ANTAL); svar[objekt_ANTAL++] = ','; 수치(portnummer % 256, svar, &objekt_ANTAL);
    }
    svar[objekt_ANTAL++] = ')'; svar[objekt_ANTAL++] = '\r'; svar[objekt_ANTAL++] = '\n'; svar[objekt_ANTAL] = 0; svara(svar);
}
static void kommando(void) {
    inmatningsrad[rad_storlek] = 0;
    char *부가인수 = inmatningsrad; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(inmatningsrad, "QUIT")) { Stopp_Överför(); svara("221 Goodbye\r\n"); avsluta_app = 1; return; }
    if (같은지(inmatningsrad, "NOOP")) { svara("200 OK\r\n"); return; }
    if (같은지(inmatningsrad, "SYST")) { svara("215 UNIX Type: L8\r\n"); return; }
    if (같은지(inmatningsrad, "FEAT")) { svara("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(inmatningsrad, "USER")) { 로그인됨 = 0; användare_OK = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); svara(användare_OK ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(inmatningsrad, "PASS")) { 로그인됨 = användare_OK; svara(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { svara("530 Login first\r\n"); return; }
    if (같은지(inmatningsrad, "PWD")) svara("257 \"/\"\r\n");
    else if (같은지(inmatningsrad, "CWD")) svara(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(inmatningsrad, "TYPE")) svara(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(inmatningsrad, "OPTS")) svara(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(inmatningsrad, "PASV")) Förbereda_manuell_kontakt(0);
    else if (같은지(inmatningsrad, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) svara("522 IPv4 only\r\n"); else Förbereda_manuell_kontakt(1); }
    else if (같은지(inmatningsrad, "ABOR")) { Stopp_Överför(); svara("226 Transfer aborted\r\n"); }
    else if (같은지(inmatningsrad, "DELE")) { svara(sökväg_2(부가인수) && pk_unlink(fil_post_namn) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(inmatningsrad, "LIST") || 같은지(inmatningsrad, "NLST") || 같은지(inmatningsrad, "MLSD")) {
        if (수행작업) { svara("450 Transfer in progress\r\n"); return; }
        if (manuell_kontakt < 0 && data < 0) { svara("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { svara("550 Root listing only\r\n"); return; }
        skicka_ange(같은지(inmatningsrad,"MLSD") ? 2 : 같은지(inmatningsrad,"LIST") ? 1 : 0); 수행작업 = 2;
        svara("150 Opening directory listing\r\n");
    }
    else if (같은지(inmatningsrad, "SIZE")) {
        if (!sökväg_2(부가인수)) { svara("550 Invalid filename\r\n"); return; }
        int filreferens = pk_open(fil_post_namn, skrivskyddad_värde, 0); if (filreferens < 0) { svara("550 File unavailable\r\n"); return; }
        int Storlek = pk_size(filreferens); pk_close(filreferens); char svar[32] = "213 "; unsigned objekt_ANTAL = 4;
        수치(Storlek, svar, &objekt_ANTAL); svar[objekt_ANTAL++] = '\r'; svar[objekt_ANTAL++] = '\n'; svar[objekt_ANTAL] = 0; svara(svar);
    } else if (같은지(inmatningsrad, "STOR") || 같은지(inmatningsrad, "RETR")) {
        if (수행작업) { svara("450 Transfer in progress\r\n"); return; }
        if (manuell_kontakt < 0 && data < 0) { svara("425 Use PASV or EPSV\r\n"); return; }
        if (!sökväg_2(부가인수)) { svara("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(inmatningsrad, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(Överför_namn, fil_post_namn, strlen(fil_post_namn) + 1);
        if (수행작업 == 2) {
            int filreferens = pk_open(fil_post_namn, skrivskyddad_värde, 0);
            if (filreferens < 0) { 수행작업 = 0; svara("550 File unavailable\r\n"); return; }
            int objekt_ANTAL = pk_read(filreferens, Överför_status, sizeof(Överför_status)); pk_close(filreferens);
            if (objekt_ANTAL < 0) { 수행작업 = 0; svara("451 Read failed\r\n"); return; } 사용량 = objekt_ANTAL;
        }
        svara("150 Opening binary data connection\r\n");
    } else svara("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (få_port < 0) return;
    int Inkommande_kontakt = NET_acceptera(få_port);
    if (Inkommande_kontakt >= 0) {
        if (kontroll >= 0) { NET_skriva(Inkommande_kontakt, "421 One session at a time\r\n", 27); Stäng_nätverk(Inkommande_kontakt); }
        else { kontroll = Inkommande_kontakt; Aktivitet = 보드밀리초(); svara("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (kontroll < 0) return;
    if ((uint32_t)(보드밀리초() - Aktivitet) > 60000) { koppla_från(); return; }
    if (!avsluta_app) for (unsigned budget = 0; budget < 256; budget++) {
        unsigned char kodpunkt; int 반환값 = NET_läsa(kontroll, &kodpunkt, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { koppla_från(); return; } Aktivitet = 보드밀리초();
        if (kodpunkt == '\n') { if (줄오류) svara("500 Command too long or invalid\r\n"); else kommando(); rad_storlek = 줄오류 = 0; if (avsluta_app) break; }
        else if (kodpunkt != '\r') { if (!kodpunkt || rad_storlek >= sizeof(inmatningsrad) - 1) 줄오류 = 1; else inmatningsrad[rad_storlek++] = kodpunkt; }
    }
    if (manuell_kontakt >= 0 && data < 0) {
        int 반환값 = NET_acceptera(manuell_kontakt);
        if (반환값 >= 0) {
            if (NET_peer_ADRESS(반환값) != NET_peer_ADRESS(kontroll)) Stäng_nätverk(반환값);
            else { data = 반환값; Stäng_nätverk(manuell_kontakt); manuell_kontakt = -1; Aktivitet = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && data >= 0) for (unsigned budget = 0; budget < 8; budget++) {
        unsigned char datablock[512]; int objekt_ANTAL = NET_läsa(data, datablock, sizeof(datablock));
        if (objekt_ANTAL == -11) break;
        if (objekt_ANTAL < 0) { Stopp_Överför(); svara("426 Data connection failed\r\n"); break; }
        Aktivitet = 보드밀리초();
        if (objekt_ANTAL == 0) {
            int RESULTAT = -1;
            if (!실패여부) {
                int filreferens = pk_open(Överför_namn, 쓰기전용 | 없으면만들기 | trimma_Innehåll, 0600);
                if (filreferens >= 0) { RESULTAT = pk_write(filreferens, Överför_status, 사용량); pk_close(filreferens); }
            }
            int 성공여부 = !실패여부 && RESULTAT == (int)사용량; Stopp_Överför(); svara(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)objekt_ANTAL > sizeof(Överför_status) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(Överför_status + 사용량, datablock, objekt_ANTAL); 사용량 += objekt_ANTAL; }
    }
    if (수행작업 == 2 && data >= 0) {
        int objekt_ANTAL = NET_skriva(data, Överför_status + 보낸수, 사용량 - 보낸수);
        if (objekt_ANTAL >= 0) { 보낸수 += objekt_ANTAL; Aktivitet = 보드밀리초(); if (보낸수 == 사용량) { Stopp_Överför(); svara("226 Transfer complete\r\n"); } }
        else if (objekt_ANTAL != -11) { Stopp_Överför(); svara("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < svara_storlek) {
        int objekt_ANTAL = NET_skriva(kontroll, 응답모음 + 응답전송량, svara_storlek - 응답전송량);
        if (objekt_ANTAL > 0) 응답전송량 += objekt_ANTAL; else if (objekt_ANTAL != -11) { koppla_från(); return; }
    }
    if (응답전송량 == svara_storlek) { svara_storlek = 응답전송량 = 0; if (avsluta_app) koppla_från(); }
}
