#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "iNethiwekhi_Isitaki.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int 수신창구 = -1, isilawuli = -1, isilandelwa_uxhumano = -1, imininingwane = -1;
static unsigned 로그인됨, 사용자확인, umugqa_linganisa, 줄오류, 끝내기, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned phendula_linganisa, 응답전송량, 다음접속번호;
static uint32_t isenzo;
static char umugqa[256], 응답모음[2048], ifayela_okufakwayo_igama[64], dlulisa_igama[64];
static unsigned char dlulisa_isimo[16384];
static int 같은지(const char *첫째값, const char *둘째값) { while (*첫째값 && *첫째값 == *둘째값) { 첫째값++; 둘째값++; } return *첫째값 == *둘째값; }
static void phendula(const char *uchunge_imininingwane) {
    size_t 개수 = strlen(uchunge_imininingwane);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, phendula_linganisa - 응답전송량); phendula_linganisa -= 응답전송량; 응답전송량 = 0; }
    if (개수 > sizeof(응답모음) - phendula_linganisa) { 끝내기 = 1; return; }
    memcpy(응답모음 + phendula_linganisa, uchunge_imininingwane, 개수); phendula_linganisa += 개수;
}
static void 수치(unsigned inani, char *결과자료, unsigned *개수) {
    char 숫자수[10]; unsigned 항목수 = 0;
    do { 숫자수[항목수++] = '0' + inani % 10; inani /= 10; } while (inani);
    while (항목수) 결과자료[(*개수)++] = 숫자수[--항목수];
}
static void ima_dlulisa(void) {
    if (imininingwane >= 0) vala_iNethiwekhi(imininingwane); if (isilandelwa_uxhumano >= 0) vala_iNethiwekhi(isilandelwa_uxhumano);
    imininingwane = isilandelwa_uxhumano = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void nqamula(void) {
    ima_dlulisa(); if (isilawuli >= 0) vala_iNethiwekhi(isilawuli); isilawuli = -1;
    로그인됨 = 사용자확인 = umugqa_linganisa = 줄오류 = phendula_linganisa = 응답전송량 = 끝내기 = 0;
}
int ifayela_dlulisa_isilawuli(int Isenzo) {
    if (Isenzo == 2) return 수신창구 >= 0;
    if (Isenzo == 0) { nqamula(); if (수신창구 >= 0) vala_iNethiwekhi(수신창구); 수신창구 = -1; return 0; }
    if (Isenzo != 1) return -22; if (수신창구 >= 0) return 0;
    수신창구 = 통신끝점만들기(1); if (수신창구 < 0) return 수신창구;
    int 반환값 = 망주소묶기(수신창구, 망상태읽기(0,0), 21); if (!반환값) 반환값 = 연결기다리기(수신창구);
    if (반환값 < 0) { vala_iNethiwekhi(수신창구); 수신창구 = -1; } return 반환값;
}
static int Indlela_2(const char *Igama) {
    unsigned 개수 = 0; if (*Igama == '/') Igama++;
    if (!*Igama || 같은지(Igama, ".") || 같은지(Igama, "..")) return 0;
    ifayela_okufakwayo_igama[개수++] = '/';
    while (*Igama) {
        unsigned char ikhodi_yohlamvu = *Igama++;
        if (개수 >= 63 || ikhodi_yohlamvu < 32 || ikhodi_yohlamvu == 127 || ikhodi_yohlamvu == '/' || ikhodi_yohlamvu == '\\') return 0;
        ifayela_okufakwayo_igama[개수++] = ikhodi_yohlamvu;
    }
    ifayela_okufakwayo_igama[개수] = 0; return 1;
}
static void Thumela_Uhlu(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int 개수 = 자바파일항목길이(순번); if (개수 <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned 항목수 = strlen(앞부분); memcpy(dlulisa_isimo + 사용량, 앞부분, 항목수); 사용량 += 항목수;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)dlulisa_isimo, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        항목수 = strlen(뒷부분); memcpy(dlulisa_isimo + 사용량, 뒷부분, 항목수); 사용량 += 항목수;
        for (int 안쪽순번 = 0; 안쪽순번 < 개수; 안쪽순번++) dlulisa_isimo[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        dlulisa_isimo[사용량++] = '\r'; dlulisa_isimo[사용량++] = '\n';
    }
}
static void Hlela_isilandelwa_uxhumano(int 확장여부) {
    if (수행작업) { phendula("450 Transfer in progress\r\n"); return; }
    ima_dlulisa(); isilandelwa_uxhumano = 통신끝점만들기(1);
    if (isilandelwa_uxhumano >= 0) 통신주소재사용(isilandelwa_uxhumano);
    unsigned 접속번호 = 50000 + 다음접속번호++ % 8;
    if (isilandelwa_uxhumano < 0 || 망주소묶기(isilandelwa_uxhumano, 망상태읽기(0,0), 접속번호) || 연결기다리기(isilandelwa_uxhumano)) {
        ima_dlulisa(); phendula("425 Cannot open passive listener\r\n"); return;
    }
    char 응답자료[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned 개수 = strlen(앞부분); memcpy(응답자료, 앞부분, 개수);
    if (확장여부) { 수치(접속번호, 응답자료, &개수); 응답자료[개수++] = '|'; }
    else {
        uint32_t ikheli=망상태읽기(0,0);
        for (int 자리=24;자리>=0;자리-=8) { 수치((ikheli>>자리)&255,응답자료,&개수);응답자료[개수++]=','; }
        수치(접속번호 / 256, 응답자료, &개수); 응답자료[개수++] = ','; 수치(접속번호 % 256, 응답자료, &개수);
    }
    응답자료[개수++] = ')'; 응답자료[개수++] = '\r'; 응답자료[개수++] = '\n'; 응답자료[개수] = 0; phendula(응답자료);
}
static void Umlayelo(void) {
    umugqa[umugqa_linganisa] = 0;
    char *부가인수 = umugqa; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(umugqa, "QUIT")) { ima_dlulisa(); phendula("221 Goodbye\r\n"); 끝내기 = 1; return; }
    if (같은지(umugqa, "NOOP")) { phendula("200 OK\r\n"); return; }
    if (같은지(umugqa, "SYST")) { phendula("215 UNIX Type: L8\r\n"); return; }
    if (같은지(umugqa, "FEAT")) { phendula("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(umugqa, "USER")) { 로그인됨 = 0; 사용자확인 = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); phendula(사용자확인 ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(umugqa, "PASS")) { 로그인됨 = 사용자확인; phendula(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { phendula("530 Login first\r\n"); return; }
    if (같은지(umugqa, "PWD")) phendula("257 \"/\"\r\n");
    else if (같은지(umugqa, "CWD")) phendula(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(umugqa, "TYPE")) phendula(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(umugqa, "OPTS")) phendula(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(umugqa, "PASV")) Hlela_isilandelwa_uxhumano(0);
    else if (같은지(umugqa, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) phendula("522 IPv4 only\r\n"); else Hlela_isilandelwa_uxhumano(1); }
    else if (같은지(umugqa, "ABOR")) { ima_dlulisa(); phendula("226 Transfer aborted\r\n"); }
    else if (같은지(umugqa, "DELE")) { phendula(Indlela_2(부가인수) && pk_unlink(ifayela_okufakwayo_igama) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(umugqa, "LIST") || 같은지(umugqa, "NLST") || 같은지(umugqa, "MLSD")) {
        if (수행작업) { phendula("450 Transfer in progress\r\n"); return; }
        if (isilandelwa_uxhumano < 0 && imininingwane < 0) { phendula("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { phendula("550 Root listing only\r\n"); return; }
        Thumela_Uhlu(같은지(umugqa,"MLSD") ? 2 : 같은지(umugqa,"LIST") ? 1 : 0); 수행작업 = 2;
        phendula("150 Opening directory listing\r\n");
    }
    else if (같은지(umugqa, "SIZE")) {
        if (!Indlela_2(부가인수)) { phendula("550 Invalid filename\r\n"); return; }
        int ifayela_isibambo = pk_open(ifayela_okufakwayo_igama, fundwayo_kuphela_inani, 0); if (ifayela_isibambo < 0) { phendula("550 File unavailable\r\n"); return; }
        int Ubungako = pk_size(ifayela_isibambo); pk_close(ifayela_isibambo); char 응답자료[32] = "213 "; unsigned 개수 = 4;
        수치(Ubungako, 응답자료, &개수); 응답자료[개수++] = '\r'; 응답자료[개수++] = '\n'; 응답자료[개수] = 0; phendula(응답자료);
    } else if (같은지(umugqa, "STOR") || 같은지(umugqa, "RETR")) {
        if (수행작업) { phendula("450 Transfer in progress\r\n"); return; }
        if (isilandelwa_uxhumano < 0 && imininingwane < 0) { phendula("425 Use PASV or EPSV\r\n"); return; }
        if (!Indlela_2(부가인수)) { phendula("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(umugqa, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(dlulisa_igama, ifayela_okufakwayo_igama, strlen(ifayela_okufakwayo_igama) + 1);
        if (수행작업 == 2) {
            int ifayela_isibambo = pk_open(ifayela_okufakwayo_igama, fundwayo_kuphela_inani, 0);
            if (ifayela_isibambo < 0) { 수행작업 = 0; phendula("550 File unavailable\r\n"); return; }
            int 개수 = pk_read(ifayela_isibambo, dlulisa_isimo, sizeof(dlulisa_isimo)); pk_close(ifayela_isibambo);
            if (개수 < 0) { 수행작업 = 0; phendula("451 Read failed\r\n"); return; } 사용량 = 개수;
        }
        phendula("150 Opening binary data connection\r\n");
    } else phendula("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (수신창구 < 0) return;
    int 들어온연결 = 망연결받기(수신창구);
    if (들어온연결 >= 0) {
        if (isilawuli >= 0) { 통신쓰기(들어온연결, "421 One session at a time\r\n", 27); vala_iNethiwekhi(들어온연결); }
        else { isilawuli = 들어온연결; isenzo = 보드밀리초(); phendula("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (isilawuli < 0) return;
    if ((uint32_t)(보드밀리초() - isenzo) > 60000) { nqamula(); return; }
    if (!끝내기) for (unsigned 처리한도 = 0; 처리한도 < 256; 처리한도++) {
        unsigned char ikhodi_yohlamvu; int 반환값 = 통신읽기(isilawuli, &ikhodi_yohlamvu, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { nqamula(); return; } isenzo = 보드밀리초();
        if (ikhodi_yohlamvu == '\n') { if (줄오류) phendula("500 Command too long or invalid\r\n"); else Umlayelo(); umugqa_linganisa = 줄오류 = 0; if (끝내기) break; }
        else if (ikhodi_yohlamvu != '\r') { if (!ikhodi_yohlamvu || umugqa_linganisa >= sizeof(umugqa) - 1) 줄오류 = 1; else umugqa[umugqa_linganisa++] = ikhodi_yohlamvu; }
    }
    if (isilandelwa_uxhumano >= 0 && imininingwane < 0) {
        int 반환값 = 망연결받기(isilandelwa_uxhumano);
        if (반환값 >= 0) {
            if (상대통신주소(반환값) != 상대통신주소(isilawuli)) vala_iNethiwekhi(반환값);
            else { imininingwane = 반환값; vala_iNethiwekhi(isilandelwa_uxhumano); isilandelwa_uxhumano = -1; isenzo = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && imininingwane >= 0) for (unsigned 처리한도 = 0; 처리한도 < 8; 처리한도++) {
        unsigned char imininingwane_vimbela[512]; int 개수 = 통신읽기(imininingwane, imininingwane_vimbela, sizeof(imininingwane_vimbela));
        if (개수 == -11) break;
        if (개수 < 0) { ima_dlulisa(); phendula("426 Data connection failed\r\n"); break; }
        isenzo = 보드밀리초();
        if (개수 == 0) {
            int 결과 = -1;
            if (!실패여부) {
                int ifayela_isibambo = pk_open(dlulisa_igama, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (ifayela_isibambo >= 0) { 결과 = pk_write(ifayela_isibambo, dlulisa_isimo, 사용량); pk_close(ifayela_isibambo); }
            }
            int 성공여부 = !실패여부 && 결과 == (int)사용량; ima_dlulisa(); phendula(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)개수 > sizeof(dlulisa_isimo) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(dlulisa_isimo + 사용량, imininingwane_vimbela, 개수); 사용량 += 개수; }
    }
    if (수행작업 == 2 && imininingwane >= 0) {
        int 개수 = 통신쓰기(imininingwane, dlulisa_isimo + 보낸수, 사용량 - 보낸수);
        if (개수 >= 0) { 보낸수 += 개수; isenzo = 보드밀리초(); if (보낸수 == 사용량) { ima_dlulisa(); phendula("226 Transfer complete\r\n"); } }
        else if (개수 != -11) { ima_dlulisa(); phendula("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < phendula_linganisa) {
        int 개수 = 통신쓰기(isilawuli, 응답모음 + 응답전송량, phendula_linganisa - 응답전송량);
        if (개수 > 0) 응답전송량 += 개수; else if (개수 != -11) { nqamula(); return; }
    }
    if (응답전송량 == phendula_linganisa) { phendula_linganisa = 응답전송량 = 0; if (끝내기) nqamula(); }
}
