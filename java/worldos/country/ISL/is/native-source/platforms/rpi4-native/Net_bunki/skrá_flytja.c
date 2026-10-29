#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "Net_bunki.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int 수신창구 = -1, stýring = -1, handvirkt_tenging = -1, gögn = -1;
static unsigned 로그인됨, notandi_Í_lagi, lína_breyta_stærð, 줄오류, hætta_forrit, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned svara_breyta_stærð, 응답전송량, Áfram_tengisnúmer;
static uint32_t Virkni;
static char Lína[256], 응답모음[2048], skrá_færsla_heiti[64], flytja_heiti[64];
static unsigned char flytja_staða[16384];
static int 같은지(const char *첫째값, const char *SECOND_VALUE) { while (*첫째값 && *첫째값 == *SECOND_VALUE) { 첫째값++; SECOND_VALUE++; } return *첫째값 == *SECOND_VALUE; }
static void svara(const char *strengur_gögn) {
    size_t vara_COUNT = strlen(strengur_gögn);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, svara_breyta_stærð - 응답전송량); svara_breyta_stærð -= 응답전송량; 응답전송량 = 0; }
    if (vara_COUNT > sizeof(응답모음) - svara_breyta_stærð) { hætta_forrit = 1; return; }
    memcpy(응답모음 + svara_breyta_stærð, strengur_gögn, vara_COUNT); svara_breyta_stærð += vara_COUNT;
}
static void 수치(unsigned VALUE, char *mæld_stærð_gögn, unsigned *vara_COUNT) {
    char tölustafur_COUNT[10]; unsigned færsla_COUNT = 0;
    do { tölustafur_COUNT[færsla_COUNT++] = '0' + VALUE % 10; VALUE /= 10; } while (VALUE);
    while (færsla_COUNT) mæld_stærð_gögn[(*vara_COUNT)++] = tölustafur_COUNT[--færsla_COUNT];
}
static void Stopp_flytja(void) {
    if (gögn >= 0) loka_Net(gögn); if (handvirkt_tenging >= 0) loka_Net(handvirkt_tenging);
    gögn = handvirkt_tenging = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void aftengja(void) {
    Stopp_flytja(); if (stýring >= 0) loka_Net(stýring); stýring = -1;
    로그인됨 = notandi_Í_lagi = lína_breyta_stærð = 줄오류 = svara_breyta_stærð = 응답전송량 = hætta_forrit = 0;
}
int skrá_flytja_stýring(int Aðgerð) {
    if (Aðgerð == 2) return 수신창구 >= 0;
    if (Aðgerð == 0) { aftengja(); if (수신창구 >= 0) loka_Net(수신창구); 수신창구 = -1; return 0; }
    if (Aðgerð != 1) return -22; if (수신창구 >= 0) return 0;
    수신창구 = 통신끝점만들기(1); if (수신창구 < 0) return 수신창구;
    int 반환값 = nettó_BIND(수신창구, 망상태읽기(0,0), 21); if (!반환값) 반환값 = nettó_hlusta(수신창구);
    if (반환값 < 0) { loka_Net(수신창구); 수신창구 = -1; } return 반환값;
}
static int SLÓÐ(const char *Heiti) {
    unsigned vara_COUNT = 0; if (*Heiti == '/') Heiti++;
    if (!*Heiti || 같은지(Heiti, ".") || 같은지(Heiti, "..")) return 0;
    skrá_færsla_heiti[vara_COUNT++] = '/';
    while (*Heiti) {
        unsigned char stafkóði = *Heiti++;
        if (vara_COUNT >= 63 || stafkóði < 32 || stafkóði == 127 || stafkóði == '/' || stafkóði == '\\') return 0;
        skrá_færsla_heiti[vara_COUNT++] = stafkóði;
    }
    skrá_færsla_heiti[vara_COUNT] = 0; return 1;
}
static void senda_Listi(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int vara_COUNT = 자바파일항목길이(순번); if (vara_COUNT <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned færsla_COUNT = strlen(앞부분); memcpy(flytja_staða + 사용량, 앞부분, færsla_COUNT); 사용량 += færsla_COUNT;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)flytja_staða, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        færsla_COUNT = strlen(뒷부분); memcpy(flytja_staða + 사용량, 뒷부분, færsla_COUNT); 사용량 += færsla_COUNT;
        for (int 안쪽순번 = 0; 안쪽순번 < vara_COUNT; 안쪽순번++) flytja_staða[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        flytja_staða[사용량++] = '\r'; flytja_staða[사용량++] = '\n';
    }
}
static void Undirbúa_handvirkt_tenging(int 확장여부) {
    if (수행작업) { svara("450 Transfer in progress\r\n"); return; }
    Stopp_flytja(); handvirkt_tenging = 통신끝점만들기(1);
    if (handvirkt_tenging >= 0) 통신주소재사용(handvirkt_tenging);
    unsigned tengisnúmer = 50000 + Áfram_tengisnúmer++ % 8;
    if (handvirkt_tenging < 0 || nettó_BIND(handvirkt_tenging, 망상태읽기(0,0), tengisnúmer) || nettó_hlusta(handvirkt_tenging)) {
        Stopp_flytja(); svara("425 Cannot open passive listener\r\n"); return;
    }
    char 응답자료[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned vara_COUNT = strlen(앞부분); memcpy(응답자료, 앞부분, vara_COUNT);
    if (확장여부) { 수치(tengisnúmer, 응답자료, &vara_COUNT); 응답자료[vara_COUNT++] = '|'; }
    else {
        uint32_t slóð=망상태읽기(0,0);
        for (int staða_INDEX=24;staða_INDEX>=0;staða_INDEX-=8) { 수치((slóð>>staða_INDEX)&255,응답자료,&vara_COUNT);응답자료[vara_COUNT++]=','; }
        수치(tengisnúmer / 256, 응답자료, &vara_COUNT); 응답자료[vara_COUNT++] = ','; 수치(tengisnúmer % 256, 응답자료, &vara_COUNT);
    }
    응답자료[vara_COUNT++] = ')'; 응답자료[vara_COUNT++] = '\r'; 응답자료[vara_COUNT++] = '\n'; 응답자료[vara_COUNT] = 0; svara(응답자료);
}
static void Skipun(void) {
    Lína[lína_breyta_stærð] = 0;
    char *부가인수 = Lína; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(Lína, "QUIT")) { Stopp_flytja(); svara("221 Goodbye\r\n"); hætta_forrit = 1; return; }
    if (같은지(Lína, "NOOP")) { svara("200 OK\r\n"); return; }
    if (같은지(Lína, "SYST")) { svara("215 UNIX Type: L8\r\n"); return; }
    if (같은지(Lína, "FEAT")) { svara("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(Lína, "USER")) { 로그인됨 = 0; notandi_Í_lagi = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); svara(notandi_Í_lagi ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(Lína, "PASS")) { 로그인됨 = notandi_Í_lagi; svara(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { svara("530 Login first\r\n"); return; }
    if (같은지(Lína, "PWD")) svara("257 \"/\"\r\n");
    else if (같은지(Lína, "CWD")) svara(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(Lína, "TYPE")) svara(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(Lína, "OPTS")) svara(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(Lína, "PASV")) Undirbúa_handvirkt_tenging(0);
    else if (같은지(Lína, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) svara("522 IPv4 only\r\n"); else Undirbúa_handvirkt_tenging(1); }
    else if (같은지(Lína, "ABOR")) { Stopp_flytja(); svara("226 Transfer aborted\r\n"); }
    else if (같은지(Lína, "DELE")) { svara(SLÓÐ(부가인수) && pk_unlink(skrá_færsla_heiti) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(Lína, "LIST") || 같은지(Lína, "NLST") || 같은지(Lína, "MLSD")) {
        if (수행작업) { svara("450 Transfer in progress\r\n"); return; }
        if (handvirkt_tenging < 0 && gögn < 0) { svara("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { svara("550 Root listing only\r\n"); return; }
        senda_Listi(같은지(Lína,"MLSD") ? 2 : 같은지(Lína,"LIST") ? 1 : 0); 수행작업 = 2;
        svara("150 Opening directory listing\r\n");
    }
    else if (같은지(Lína, "SIZE")) {
        if (!SLÓÐ(부가인수)) { svara("550 Invalid filename\r\n"); return; }
        int skrá_hald = pk_open(skrá_færsla_heiti, skrifvarið_VALUE, 0); if (skrá_hald < 0) { svara("550 File unavailable\r\n"); return; }
        int Stærð = pk_size(skrá_hald); pk_close(skrá_hald); char 응답자료[32] = "213 "; unsigned vara_COUNT = 4;
        수치(Stærð, 응답자료, &vara_COUNT); 응답자료[vara_COUNT++] = '\r'; 응답자료[vara_COUNT++] = '\n'; 응답자료[vara_COUNT] = 0; svara(응답자료);
    } else if (같은지(Lína, "STOR") || 같은지(Lína, "RETR")) {
        if (수행작업) { svara("450 Transfer in progress\r\n"); return; }
        if (handvirkt_tenging < 0 && gögn < 0) { svara("425 Use PASV or EPSV\r\n"); return; }
        if (!SLÓÐ(부가인수)) { svara("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(Lína, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(flytja_heiti, skrá_færsla_heiti, strlen(skrá_færsla_heiti) + 1);
        if (수행작업 == 2) {
            int skrá_hald = pk_open(skrá_færsla_heiti, skrifvarið_VALUE, 0);
            if (skrá_hald < 0) { 수행작업 = 0; svara("550 File unavailable\r\n"); return; }
            int vara_COUNT = pk_read(skrá_hald, flytja_staða, sizeof(flytja_staða)); pk_close(skrá_hald);
            if (vara_COUNT < 0) { 수행작업 = 0; svara("451 Read failed\r\n"); return; } 사용량 = vara_COUNT;
        }
        svara("150 Opening binary data connection\r\n");
    } else svara("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (수신창구 < 0) return;
    int Innhringing_tenging = nettó_samþykkja(수신창구);
    if (Innhringing_tenging >= 0) {
        if (stýring >= 0) { nettó_skrifa(Innhringing_tenging, "421 One session at a time\r\n", 27); loka_Net(Innhringing_tenging); }
        else { stýring = Innhringing_tenging; Virkni = 보드밀리초(); svara("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (stýring < 0) return;
    if ((uint32_t)(보드밀리초() - Virkni) > 60000) { aftengja(); return; }
    if (!hætta_forrit) for (unsigned fjárhagsáætlun = 0; fjárhagsáætlun < 256; fjárhagsáætlun++) {
        unsigned char stafkóði; int 반환값 = 통신읽기(stýring, &stafkóði, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { aftengja(); return; } Virkni = 보드밀리초();
        if (stafkóði == '\n') { if (줄오류) svara("500 Command too long or invalid\r\n"); else Skipun(); lína_breyta_stærð = 줄오류 = 0; if (hætta_forrit) break; }
        else if (stafkóði != '\r') { if (!stafkóði || lína_breyta_stærð >= sizeof(Lína) - 1) 줄오류 = 1; else Lína[lína_breyta_stærð++] = stafkóði; }
    }
    if (handvirkt_tenging >= 0 && gögn < 0) {
        int 반환값 = nettó_samþykkja(handvirkt_tenging);
        if (반환값 >= 0) {
            if (nettó_jafningi_slóð(반환값) != nettó_jafningi_slóð(stýring)) loka_Net(반환값);
            else { gögn = 반환값; loka_Net(handvirkt_tenging); handvirkt_tenging = -1; Virkni = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && gögn >= 0) for (unsigned fjárhagsáætlun = 0; fjárhagsáætlun < 8; fjárhagsáætlun++) {
        unsigned char gögn_útiloka[512]; int vara_COUNT = 통신읽기(gögn, gögn_útiloka, sizeof(gögn_útiloka));
        if (vara_COUNT == -11) break;
        if (vara_COUNT < 0) { Stopp_flytja(); svara("426 Data connection failed\r\n"); break; }
        Virkni = 보드밀리초();
        if (vara_COUNT == 0) {
            int NIÐURSTAÐA = -1;
            if (!실패여부) {
                int skrá_hald = pk_open(flytja_heiti, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (skrá_hald >= 0) { NIÐURSTAÐA = pk_write(skrá_hald, flytja_staða, 사용량); pk_close(skrá_hald); }
            }
            int 성공여부 = !실패여부 && NIÐURSTAÐA == (int)사용량; Stopp_flytja(); svara(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)vara_COUNT > sizeof(flytja_staða) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(flytja_staða + 사용량, gögn_útiloka, vara_COUNT); 사용량 += vara_COUNT; }
    }
    if (수행작업 == 2 && gögn >= 0) {
        int vara_COUNT = nettó_skrifa(gögn, flytja_staða + 보낸수, 사용량 - 보낸수);
        if (vara_COUNT >= 0) { 보낸수 += vara_COUNT; Virkni = 보드밀리초(); if (보낸수 == 사용량) { Stopp_flytja(); svara("226 Transfer complete\r\n"); } }
        else if (vara_COUNT != -11) { Stopp_flytja(); svara("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < svara_breyta_stærð) {
        int vara_COUNT = nettó_skrifa(stýring, 응답모음 + 응답전송량, svara_breyta_stærð - 응답전송량);
        if (vara_COUNT > 0) 응답전송량 += vara_COUNT; else if (vara_COUNT != -11) { aftengja(); return; }
    }
    if (응답전송량 == svara_breyta_stærð) { svara_breyta_stærð = 응답전송량 = 0; if (hætta_forrit) aftengja(); }
}
