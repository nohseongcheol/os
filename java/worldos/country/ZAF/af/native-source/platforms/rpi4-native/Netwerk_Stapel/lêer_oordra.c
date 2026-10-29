#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "Netwerk_Stapel.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int 수신창구 = -1, kontrole = -1, handmatig_verbinding = -1, data = -1;
static unsigned 로그인됨, gebruiker_OK, lyn_verstel, 줄오류, gaan_uit_program, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned antwoord_verstel, 응답전송량, 다음접속번호;
static uint32_t Aktiwiteit;
static char lyn[256], 응답모음[2048], lêer_inskrywing_naam[64], oordra_naam[64];
static unsigned char oordra_stand[16384];
static int 같은지(const char *첫째값, const char *SECOND_VALUE) { while (*첫째값 && *첫째값 == *SECOND_VALUE) { 첫째값++; SECOND_VALUE++; } return *첫째값 == *SECOND_VALUE; }
static void antwoord(const char *string_data) {
    size_t item_COUNT = strlen(string_data);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, antwoord_verstel - 응답전송량); antwoord_verstel -= 응답전송량; 응답전송량 = 0; }
    if (item_COUNT > sizeof(응답모음) - antwoord_verstel) { gaan_uit_program = 1; return; }
    memcpy(응답모음 + antwoord_verstel, string_data, item_COUNT); antwoord_verstel += item_COUNT;
}
static void 수치(unsigned VALUE, char *maatreël_data, unsigned *item_COUNT) {
    char syfer_COUNT[10]; unsigned inskrywing_COUNT = 0;
    do { syfer_COUNT[inskrywing_COUNT++] = '0' + VALUE % 10; VALUE /= 10; } while (VALUE);
    while (inskrywing_COUNT) maatreël_data[(*item_COUNT)++] = syfer_COUNT[--inskrywing_COUNT];
}
static void Stop_oordra(void) {
    if (data >= 0) sluit_Netwerk(data); if (handmatig_verbinding >= 0) sluit_Netwerk(handmatig_verbinding);
    data = handmatig_verbinding = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void ontkoppel(void) {
    Stop_oordra(); if (kontrole >= 0) sluit_Netwerk(kontrole); kontrole = -1;
    로그인됨 = gebruiker_OK = lyn_verstel = 줄오류 = antwoord_verstel = 응답전송량 = gaan_uit_program = 0;
}
int lêer_oordra_kontrole(int Aksie) {
    if (Aksie == 2) return 수신창구 >= 0;
    if (Aksie == 0) { ontkoppel(); if (수신창구 >= 0) sluit_Netwerk(수신창구); 수신창구 = -1; return 0; }
    if (Aksie != 1) return -22; if (수신창구 >= 0) return 0;
    수신창구 = 통신끝점만들기(1); if (수신창구 < 0) return 수신창구;
    int 반환값 = 망주소묶기(수신창구, 망상태읽기(0,0), 21); if (!반환값) 반환값 = 연결기다리기(수신창구);
    if (반환값 < 0) { sluit_Netwerk(수신창구); 수신창구 = -1; } return 반환값;
}
static int Pad(const char *Naam) {
    unsigned item_COUNT = 0; if (*Naam == '/') Naam++;
    if (!*Naam || 같은지(Naam, ".") || 같은지(Naam, "..")) return 0;
    lêer_inskrywing_naam[item_COUNT++] = '/';
    while (*Naam) {
        unsigned char karakterkode = *Naam++;
        if (item_COUNT >= 63 || karakterkode < 32 || karakterkode == 127 || karakterkode == '/' || karakterkode == '\\') return 0;
        lêer_inskrywing_naam[item_COUNT++] = karakterkode;
    }
    lêer_inskrywing_naam[item_COUNT] = 0; return 1;
}
static void e_pos_Lys(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int item_COUNT = 자바파일항목길이(순번); if (item_COUNT <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned inskrywing_COUNT = strlen(앞부분); memcpy(oordra_stand + 사용량, 앞부분, inskrywing_COUNT); 사용량 += inskrywing_COUNT;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)oordra_stand, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        inskrywing_COUNT = strlen(뒷부분); memcpy(oordra_stand + 사용량, 뒷부분, inskrywing_COUNT); 사용량 += inskrywing_COUNT;
        for (int 안쪽순번 = 0; 안쪽순번 < item_COUNT; 안쪽순번++) oordra_stand[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        oordra_stand[사용량++] = '\r'; oordra_stand[사용량++] = '\n';
    }
}
static void Maak_gereed_handmatig_verbinding(int 확장여부) {
    if (수행작업) { antwoord("450 Transfer in progress\r\n"); return; }
    Stop_oordra(); handmatig_verbinding = 통신끝점만들기(1);
    if (handmatig_verbinding >= 0) 통신주소재사용(handmatig_verbinding);
    unsigned 접속번호 = 50000 + 다음접속번호++ % 8;
    if (handmatig_verbinding < 0 || 망주소묶기(handmatig_verbinding, 망상태읽기(0,0), 접속번호) || 연결기다리기(handmatig_verbinding)) {
        Stop_oordra(); antwoord("425 Cannot open passive listener\r\n"); return;
    }
    char 응답자료[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned item_COUNT = strlen(앞부분); memcpy(응답자료, 앞부분, item_COUNT);
    if (확장여부) { 수치(접속번호, 응답자료, &item_COUNT); 응답자료[item_COUNT++] = '|'; }
    else {
        uint32_t adres=망상태읽기(0,0);
        for (int plaas_INDEX=24;plaas_INDEX>=0;plaas_INDEX-=8) { 수치((adres>>plaas_INDEX)&255,응답자료,&item_COUNT);응답자료[item_COUNT++]=','; }
        수치(접속번호 / 256, 응답자료, &item_COUNT); 응답자료[item_COUNT++] = ','; 수치(접속번호 % 256, 응답자료, &item_COUNT);
    }
    응답자료[item_COUNT++] = ')'; 응답자료[item_COUNT++] = '\r'; 응답자료[item_COUNT++] = '\n'; 응답자료[item_COUNT] = 0; antwoord(응답자료);
}
static void Opdrag(void) {
    lyn[lyn_verstel] = 0;
    char *부가인수 = lyn; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(lyn, "QUIT")) { Stop_oordra(); antwoord("221 Goodbye\r\n"); gaan_uit_program = 1; return; }
    if (같은지(lyn, "NOOP")) { antwoord("200 OK\r\n"); return; }
    if (같은지(lyn, "SYST")) { antwoord("215 UNIX Type: L8\r\n"); return; }
    if (같은지(lyn, "FEAT")) { antwoord("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(lyn, "USER")) { 로그인됨 = 0; gebruiker_OK = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); antwoord(gebruiker_OK ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(lyn, "PASS")) { 로그인됨 = gebruiker_OK; antwoord(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { antwoord("530 Login first\r\n"); return; }
    if (같은지(lyn, "PWD")) antwoord("257 \"/\"\r\n");
    else if (같은지(lyn, "CWD")) antwoord(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(lyn, "TYPE")) antwoord(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(lyn, "OPTS")) antwoord(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(lyn, "PASV")) Maak_gereed_handmatig_verbinding(0);
    else if (같은지(lyn, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) antwoord("522 IPv4 only\r\n"); else Maak_gereed_handmatig_verbinding(1); }
    else if (같은지(lyn, "ABOR")) { Stop_oordra(); antwoord("226 Transfer aborted\r\n"); }
    else if (같은지(lyn, "DELE")) { antwoord(Pad(부가인수) && pk_unlink(lêer_inskrywing_naam) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(lyn, "LIST") || 같은지(lyn, "NLST") || 같은지(lyn, "MLSD")) {
        if (수행작업) { antwoord("450 Transfer in progress\r\n"); return; }
        if (handmatig_verbinding < 0 && data < 0) { antwoord("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { antwoord("550 Root listing only\r\n"); return; }
        e_pos_Lys(같은지(lyn,"MLSD") ? 2 : 같은지(lyn,"LIST") ? 1 : 0); 수행작업 = 2;
        antwoord("150 Opening directory listing\r\n");
    }
    else if (같은지(lyn, "SIZE")) {
        if (!Pad(부가인수)) { antwoord("550 Invalid filename\r\n"); return; }
        int lêer_handvatsel = pk_open(lêer_inskrywing_naam, leesalleen_VALUE, 0); if (lêer_handvatsel < 0) { antwoord("550 File unavailable\r\n"); return; }
        int Grootte = pk_size(lêer_handvatsel); pk_close(lêer_handvatsel); char 응답자료[32] = "213 "; unsigned item_COUNT = 4;
        수치(Grootte, 응답자료, &item_COUNT); 응답자료[item_COUNT++] = '\r'; 응답자료[item_COUNT++] = '\n'; 응답자료[item_COUNT] = 0; antwoord(응답자료);
    } else if (같은지(lyn, "STOR") || 같은지(lyn, "RETR")) {
        if (수행작업) { antwoord("450 Transfer in progress\r\n"); return; }
        if (handmatig_verbinding < 0 && data < 0) { antwoord("425 Use PASV or EPSV\r\n"); return; }
        if (!Pad(부가인수)) { antwoord("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(lyn, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(oordra_naam, lêer_inskrywing_naam, strlen(lêer_inskrywing_naam) + 1);
        if (수행작업 == 2) {
            int lêer_handvatsel = pk_open(lêer_inskrywing_naam, leesalleen_VALUE, 0);
            if (lêer_handvatsel < 0) { 수행작업 = 0; antwoord("550 File unavailable\r\n"); return; }
            int item_COUNT = pk_read(lêer_handvatsel, oordra_stand, sizeof(oordra_stand)); pk_close(lêer_handvatsel);
            if (item_COUNT < 0) { 수행작업 = 0; antwoord("451 Read failed\r\n"); return; } 사용량 = item_COUNT;
        }
        antwoord("150 Opening binary data connection\r\n");
    } else antwoord("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (수신창구 < 0) return;
    int Inkomend_verbinding = 망연결받기(수신창구);
    if (Inkomend_verbinding >= 0) {
        if (kontrole >= 0) { 통신쓰기(Inkomend_verbinding, "421 One session at a time\r\n", 27); sluit_Netwerk(Inkomend_verbinding); }
        else { kontrole = Inkomend_verbinding; Aktiwiteit = 보드밀리초(); antwoord("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (kontrole < 0) return;
    if ((uint32_t)(보드밀리초() - Aktiwiteit) > 60000) { ontkoppel(); return; }
    if (!gaan_uit_program) for (unsigned 처리한도 = 0; 처리한도 < 256; 처리한도++) {
        unsigned char karakterkode; int 반환값 = 통신읽기(kontrole, &karakterkode, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { ontkoppel(); return; } Aktiwiteit = 보드밀리초();
        if (karakterkode == '\n') { if (줄오류) antwoord("500 Command too long or invalid\r\n"); else Opdrag(); lyn_verstel = 줄오류 = 0; if (gaan_uit_program) break; }
        else if (karakterkode != '\r') { if (!karakterkode || lyn_verstel >= sizeof(lyn) - 1) 줄오류 = 1; else lyn[lyn_verstel++] = karakterkode; }
    }
    if (handmatig_verbinding >= 0 && data < 0) {
        int 반환값 = 망연결받기(handmatig_verbinding);
        if (반환값 >= 0) {
            if (상대통신주소(반환값) != 상대통신주소(kontrole)) sluit_Netwerk(반환값);
            else { data = 반환값; sluit_Netwerk(handmatig_verbinding); handmatig_verbinding = -1; Aktiwiteit = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && data >= 0) for (unsigned 처리한도 = 0; 처리한도 < 8; 처리한도++) {
        unsigned char data_blokkeer[512]; int item_COUNT = 통신읽기(data, data_blokkeer, sizeof(data_blokkeer));
        if (item_COUNT == -11) break;
        if (item_COUNT < 0) { Stop_oordra(); antwoord("426 Data connection failed\r\n"); break; }
        Aktiwiteit = 보드밀리초();
        if (item_COUNT == 0) {
            int maatreël = -1;
            if (!실패여부) {
                int lêer_handvatsel = pk_open(oordra_naam, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (lêer_handvatsel >= 0) { maatreël = pk_write(lêer_handvatsel, oordra_stand, 사용량); pk_close(lêer_handvatsel); }
            }
            int 성공여부 = !실패여부 && maatreël == (int)사용량; Stop_oordra(); antwoord(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)item_COUNT > sizeof(oordra_stand) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(oordra_stand + 사용량, data_blokkeer, item_COUNT); 사용량 += item_COUNT; }
    }
    if (수행작업 == 2 && data >= 0) {
        int item_COUNT = 통신쓰기(data, oordra_stand + 보낸수, 사용량 - 보낸수);
        if (item_COUNT >= 0) { 보낸수 += item_COUNT; Aktiwiteit = 보드밀리초(); if (보낸수 == 사용량) { Stop_oordra(); antwoord("226 Transfer complete\r\n"); } }
        else if (item_COUNT != -11) { Stop_oordra(); antwoord("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < antwoord_verstel) {
        int item_COUNT = 통신쓰기(kontrole, 응답모음 + 응답전송량, antwoord_verstel - 응답전송량);
        if (item_COUNT > 0) 응답전송량 += item_COUNT; else if (item_COUNT != -11) { ontkoppel(); return; }
    }
    if (응답전송량 == antwoord_verstel) { antwoord_verstel = 응답전송량 = 0; if (gaan_uit_program) ontkoppel(); }
}
