#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "Rhwydwaith_pentwr.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int 수신창구 = -1, rheoli = -1, llaw_cyswllt = -1, data = -1;
static unsigned 로그인됨, defnyddiwr_Iawn, llinell_newid_maint, 줄오류, gadael_Rhaglen_55b3a1cd, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned ateb_newid_maint, 응답전송량, Nesaf_rhif_porth;
static uint32_t Gweithgarwch;
static char llinell[256], 응답모음[2048], ffeil_cofnod_enw[64], trosglwyddo_enw[64];
static unsigned char trosglwyddo_cyflwr[16384];
static int 같은지(const char *첫째값, const char *SECOND_VALUE) { while (*첫째값 && *첫째값 == *SECOND_VALUE) { 첫째값++; SECOND_VALUE++; } return *첫째값 == *SECOND_VALUE; }
static void ateb(const char *testun_data) {
    size_t eitem_COUNT = strlen(testun_data);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, ateb_newid_maint - 응답전송량); ateb_newid_maint -= 응답전송량; 응답전송량 = 0; }
    if (eitem_COUNT > sizeof(응답모음) - ateb_newid_maint) { gadael_Rhaglen_55b3a1cd = 1; return; }
    memcpy(응답모음 + ateb_newid_maint, testun_data, eitem_COUNT); ateb_newid_maint += eitem_COUNT;
}
static void 수치(unsigned VALUE, char *mesur_data, unsigned *eitem_COUNT) {
    char digid_COUNT[10]; unsigned cofnod_COUNT = 0;
    do { digid_COUNT[cofnod_COUNT++] = '0' + VALUE % 10; VALUE /= 10; } while (VALUE);
    while (cofnod_COUNT) mesur_data[(*eitem_COUNT)++] = digid_COUNT[--cofnod_COUNT];
}
static void Stop_trosglwyddo(void) {
    if (data >= 0) cau_Rhwydwaith(data); if (llaw_cyswllt >= 0) cau_Rhwydwaith(llaw_cyswllt);
    data = llaw_cyswllt = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void datgysylltu(void) {
    Stop_trosglwyddo(); if (rheoli >= 0) cau_Rhwydwaith(rheoli); rheoli = -1;
    로그인됨 = defnyddiwr_Iawn = llinell_newid_maint = 줄오류 = ateb_newid_maint = 응답전송량 = gadael_Rhaglen_55b3a1cd = 0;
}
int ffeil_trosglwyddo_rheoli(int Gweithrediad) {
    if (Gweithrediad == 2) return 수신창구 >= 0;
    if (Gweithrediad == 0) { datgysylltu(); if (수신창구 >= 0) cau_Rhwydwaith(수신창구); 수신창구 = -1; return 0; }
    if (Gweithrediad != 1) return -22; if (수신창구 >= 0) return 0;
    수신창구 = 통신끝점만들기(1); if (수신창구 < 0) return 수신창구;
    int 반환값 = 망주소묶기(수신창구, 망상태읽기(0,0), 21); if (!반환값) 반환값 = 연결기다리기(수신창구);
    if (반환값 < 0) { cau_Rhwydwaith(수신창구); 수신창구 = -1; } return 반환값;
}
static int LLWYBR(const char *Enw) {
    unsigned eitem_COUNT = 0; if (*Enw == '/') Enw++;
    if (!*Enw || 같은지(Enw, ".") || 같은지(Enw, "..")) return 0;
    ffeil_cofnod_enw[eitem_COUNT++] = '/';
    while (*Enw) {
        unsigned char cod_nod = *Enw++;
        if (eitem_COUNT >= 63 || cod_nod < 32 || cod_nod == 127 || cod_nod == '/' || cod_nod == '\\') return 0;
        ffeil_cofnod_enw[eitem_COUNT++] = cod_nod;
    }
    ffeil_cofnod_enw[eitem_COUNT] = 0; return 1;
}
static void anfon_Rhestr(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int eitem_COUNT = 자바파일항목길이(순번); if (eitem_COUNT <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned cofnod_COUNT = strlen(앞부분); memcpy(trosglwyddo_cyflwr + 사용량, 앞부분, cofnod_COUNT); 사용량 += cofnod_COUNT;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)trosglwyddo_cyflwr, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        cofnod_COUNT = strlen(뒷부분); memcpy(trosglwyddo_cyflwr + 사용량, 뒷부분, cofnod_COUNT); 사용량 += cofnod_COUNT;
        for (int 안쪽순번 = 0; 안쪽순번 < eitem_COUNT; 안쪽순번++) trosglwyddo_cyflwr[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        trosglwyddo_cyflwr[사용량++] = '\r'; trosglwyddo_cyflwr[사용량++] = '\n';
    }
}
static void Paratoi_llaw_cyswllt(int 확장여부) {
    if (수행작업) { ateb("450 Transfer in progress\r\n"); return; }
    Stop_trosglwyddo(); llaw_cyswllt = 통신끝점만들기(1);
    if (llaw_cyswllt >= 0) 통신주소재사용(llaw_cyswllt);
    unsigned rhif_porth = 50000 + Nesaf_rhif_porth++ % 8;
    if (llaw_cyswllt < 0 || 망주소묶기(llaw_cyswllt, 망상태읽기(0,0), rhif_porth) || 연결기다리기(llaw_cyswllt)) {
        Stop_trosglwyddo(); ateb("425 Cannot open passive listener\r\n"); return;
    }
    char 응답자료[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned eitem_COUNT = strlen(앞부분); memcpy(응답자료, 앞부분, eitem_COUNT);
    if (확장여부) { 수치(rhif_porth, 응답자료, &eitem_COUNT); 응답자료[eitem_COUNT++] = '|'; }
    else {
        uint32_t ADDRESS=망상태읽기(0,0);
        for (int safle_INDEX=24;safle_INDEX>=0;safle_INDEX-=8) { 수치((ADDRESS>>safle_INDEX)&255,응답자료,&eitem_COUNT);응답자료[eitem_COUNT++]=','; }
        수치(rhif_porth / 256, 응답자료, &eitem_COUNT); 응답자료[eitem_COUNT++] = ','; 수치(rhif_porth % 256, 응답자료, &eitem_COUNT);
    }
    응답자료[eitem_COUNT++] = ')'; 응답자료[eitem_COUNT++] = '\r'; 응답자료[eitem_COUNT++] = '\n'; 응답자료[eitem_COUNT] = 0; ateb(응답자료);
}
static void Gorchymyn(void) {
    llinell[llinell_newid_maint] = 0;
    char *부가인수 = llinell; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(llinell, "QUIT")) { Stop_trosglwyddo(); ateb("221 Goodbye\r\n"); gadael_Rhaglen_55b3a1cd = 1; return; }
    if (같은지(llinell, "NOOP")) { ateb("200 OK\r\n"); return; }
    if (같은지(llinell, "SYST")) { ateb("215 UNIX Type: L8\r\n"); return; }
    if (같은지(llinell, "FEAT")) { ateb("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(llinell, "USER")) { 로그인됨 = 0; defnyddiwr_Iawn = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); ateb(defnyddiwr_Iawn ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(llinell, "PASS")) { 로그인됨 = defnyddiwr_Iawn; ateb(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { ateb("530 Login first\r\n"); return; }
    if (같은지(llinell, "PWD")) ateb("257 \"/\"\r\n");
    else if (같은지(llinell, "CWD")) ateb(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(llinell, "TYPE")) ateb(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(llinell, "OPTS")) ateb(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(llinell, "PASV")) Paratoi_llaw_cyswllt(0);
    else if (같은지(llinell, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) ateb("522 IPv4 only\r\n"); else Paratoi_llaw_cyswllt(1); }
    else if (같은지(llinell, "ABOR")) { Stop_trosglwyddo(); ateb("226 Transfer aborted\r\n"); }
    else if (같은지(llinell, "DELE")) { ateb(LLWYBR(부가인수) && pk_unlink(ffeil_cofnod_enw) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(llinell, "LIST") || 같은지(llinell, "NLST") || 같은지(llinell, "MLSD")) {
        if (수행작업) { ateb("450 Transfer in progress\r\n"); return; }
        if (llaw_cyswllt < 0 && data < 0) { ateb("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { ateb("550 Root listing only\r\n"); return; }
        anfon_Rhestr(같은지(llinell,"MLSD") ? 2 : 같은지(llinell,"LIST") ? 1 : 0); 수행작업 = 2;
        ateb("150 Opening directory listing\r\n");
    }
    else if (같은지(llinell, "SIZE")) {
        if (!LLWYBR(부가인수)) { ateb("550 Invalid filename\r\n"); return; }
        int ffeil_dolen = pk_open(ffeil_cofnod_enw, darllen_yn_unig_VALUE, 0); if (ffeil_dolen < 0) { ateb("550 File unavailable\r\n"); return; }
        int Maint = pk_size(ffeil_dolen); pk_close(ffeil_dolen); char 응답자료[32] = "213 "; unsigned eitem_COUNT = 4;
        수치(Maint, 응답자료, &eitem_COUNT); 응답자료[eitem_COUNT++] = '\r'; 응답자료[eitem_COUNT++] = '\n'; 응답자료[eitem_COUNT] = 0; ateb(응답자료);
    } else if (같은지(llinell, "STOR") || 같은지(llinell, "RETR")) {
        if (수행작업) { ateb("450 Transfer in progress\r\n"); return; }
        if (llaw_cyswllt < 0 && data < 0) { ateb("425 Use PASV or EPSV\r\n"); return; }
        if (!LLWYBR(부가인수)) { ateb("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(llinell, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(trosglwyddo_enw, ffeil_cofnod_enw, strlen(ffeil_cofnod_enw) + 1);
        if (수행작업 == 2) {
            int ffeil_dolen = pk_open(ffeil_cofnod_enw, darllen_yn_unig_VALUE, 0);
            if (ffeil_dolen < 0) { 수행작업 = 0; ateb("550 File unavailable\r\n"); return; }
            int eitem_COUNT = pk_read(ffeil_dolen, trosglwyddo_cyflwr, sizeof(trosglwyddo_cyflwr)); pk_close(ffeil_dolen);
            if (eitem_COUNT < 0) { 수행작업 = 0; ateb("451 Read failed\r\n"); return; } 사용량 = eitem_COUNT;
        }
        ateb("150 Opening binary data connection\r\n");
    } else ateb("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (수신창구 < 0) return;
    int 들어온연결 = 망연결받기(수신창구);
    if (들어온연결 >= 0) {
        if (rheoli >= 0) { 통신쓰기(들어온연결, "421 One session at a time\r\n", 27); cau_Rhwydwaith(들어온연결); }
        else { rheoli = 들어온연결; Gweithgarwch = 보드밀리초(); ateb("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (rheoli < 0) return;
    if ((uint32_t)(보드밀리초() - Gweithgarwch) > 60000) { datgysylltu(); return; }
    if (!gadael_Rhaglen_55b3a1cd) for (unsigned 처리한도 = 0; 처리한도 < 256; 처리한도++) {
        unsigned char cod_nod; int 반환값 = 통신읽기(rheoli, &cod_nod, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { datgysylltu(); return; } Gweithgarwch = 보드밀리초();
        if (cod_nod == '\n') { if (줄오류) ateb("500 Command too long or invalid\r\n"); else Gorchymyn(); llinell_newid_maint = 줄오류 = 0; if (gadael_Rhaglen_55b3a1cd) break; }
        else if (cod_nod != '\r') { if (!cod_nod || llinell_newid_maint >= sizeof(llinell) - 1) 줄오류 = 1; else llinell[llinell_newid_maint++] = cod_nod; }
    }
    if (llaw_cyswllt >= 0 && data < 0) {
        int 반환값 = 망연결받기(llaw_cyswllt);
        if (반환값 >= 0) {
            if (상대통신주소(반환값) != 상대통신주소(rheoli)) cau_Rhwydwaith(반환값);
            else { data = 반환값; cau_Rhwydwaith(llaw_cyswllt); llaw_cyswllt = -1; Gweithgarwch = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && data >= 0) for (unsigned 처리한도 = 0; 처리한도 < 8; 처리한도++) {
        unsigned char data_rhwystro[512]; int eitem_COUNT = 통신읽기(data, data_rhwystro, sizeof(data_rhwystro));
        if (eitem_COUNT == -11) break;
        if (eitem_COUNT < 0) { Stop_trosglwyddo(); ateb("426 Data connection failed\r\n"); break; }
        Gweithgarwch = 보드밀리초();
        if (eitem_COUNT == 0) {
            int mesur = -1;
            if (!실패여부) {
                int ffeil_dolen = pk_open(trosglwyddo_enw, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (ffeil_dolen >= 0) { mesur = pk_write(ffeil_dolen, trosglwyddo_cyflwr, 사용량); pk_close(ffeil_dolen); }
            }
            int 성공여부 = !실패여부 && mesur == (int)사용량; Stop_trosglwyddo(); ateb(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)eitem_COUNT > sizeof(trosglwyddo_cyflwr) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(trosglwyddo_cyflwr + 사용량, data_rhwystro, eitem_COUNT); 사용량 += eitem_COUNT; }
    }
    if (수행작업 == 2 && data >= 0) {
        int eitem_COUNT = 통신쓰기(data, trosglwyddo_cyflwr + 보낸수, 사용량 - 보낸수);
        if (eitem_COUNT >= 0) { 보낸수 += eitem_COUNT; Gweithgarwch = 보드밀리초(); if (보낸수 == 사용량) { Stop_trosglwyddo(); ateb("226 Transfer complete\r\n"); } }
        else if (eitem_COUNT != -11) { Stop_trosglwyddo(); ateb("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < ateb_newid_maint) {
        int eitem_COUNT = 통신쓰기(rheoli, 응답모음 + 응답전송량, ateb_newid_maint - 응답전송량);
        if (eitem_COUNT > 0) 응답전송량 += eitem_COUNT; else if (eitem_COUNT != -11) { datgysylltu(); return; }
    }
    if (응답전송량 == ateb_newid_maint) { ateb_newid_maint = 응답전송량 = 0; if (gadael_Rhaglen_55b3a1cd) datgysylltu(); }
}
