#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "Inethiwekhi_fumba.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int 수신창구 = -1, isilawuli = -1, ozenzela_ngokwakho_uqhagamshelo = -1, iingcombolo = -1;
static unsigned 로그인됨, 사용자확인, umgca_isayizi, 줄오류, 끝내기, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned phendula_isayizi, 응답전송량, 다음접속번호;
static uint32_t Umsebenzi;
static char umgca[256], 응답모음[2048], ifayile_ufako_nkcukacha_igama[64], gqithisela_igama[64];
static unsigned char gqithisela_imo[16384];
static int 같은지(const char *첫째값, const char *둘째값) { while (*첫째값 && *첫째값 == *둘째값) { 첫째값++; 둘째값++; } return *첫째값 == *둘째값; }
static void phendula(const char *uluhlu_lweekharektha_iingcombolo) {
    size_t 개수 = strlen(uluhlu_lweekharektha_iingcombolo);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, phendula_isayizi - 응답전송량); phendula_isayizi -= 응답전송량; 응답전송량 = 0; }
    if (개수 > sizeof(응답모음) - phendula_isayizi) { 끝내기 = 1; return; }
    memcpy(응답모음 + phendula_isayizi, uluhlu_lweekharektha_iingcombolo, 개수); phendula_isayizi += 개수;
}
static void 수치(unsigned ixabiso, char *결과자료, unsigned *개수) {
    char 숫자수[10]; unsigned 항목수 = 0;
    do { 숫자수[항목수++] = '0' + ixabiso % 10; ixabiso /= 10; } while (ixabiso);
    while (항목수) 결과자료[(*개수)++] = 숫자수[--항목수];
}
static void misa_gqithisela(void) {
    if (iingcombolo >= 0) vala_Inethiwekhi(iingcombolo); if (ozenzela_ngokwakho_uqhagamshelo >= 0) vala_Inethiwekhi(ozenzela_ngokwakho_uqhagamshelo);
    iingcombolo = ozenzela_ngokwakho_uqhagamshelo = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void qhawula_uqhagamshelwano(void) {
    misa_gqithisela(); if (isilawuli >= 0) vala_Inethiwekhi(isilawuli); isilawuli = -1;
    로그인됨 = 사용자확인 = umgca_isayizi = 줄오류 = phendula_isayizi = 응답전송량 = 끝내기 = 0;
}
int ifayile_gqithisela_isilawuli(int Intshukumo) {
    if (Intshukumo == 2) return 수신창구 >= 0;
    if (Intshukumo == 0) { qhawula_uqhagamshelwano(); if (수신창구 >= 0) vala_Inethiwekhi(수신창구); 수신창구 = -1; return 0; }
    if (Intshukumo != 1) return -22; if (수신창구 >= 0) return 0;
    수신창구 = 통신끝점만들기(1); if (수신창구 < 0) return 수신창구;
    int 반환값 = 망주소묶기(수신창구, 망상태읽기(0,0), 21); if (!반환값) 반환값 = 연결기다리기(수신창구);
    if (반환값 < 0) { vala_Inethiwekhi(수신창구); 수신창구 = -1; } return 반환값;
}
static int INDLELA(const char *Igama) {
    unsigned 개수 = 0; if (*Igama == '/') Igama++;
    if (!*Igama || 같은지(Igama, ".") || 같은지(Igama, "..")) return 0;
    ifayile_ufako_nkcukacha_igama[개수++] = '/';
    while (*Igama) {
        unsigned char ikhowudi_yekharakhtha = *Igama++;
        if (개수 >= 63 || ikhowudi_yekharakhtha < 32 || ikhowudi_yekharakhtha == 127 || ikhowudi_yekharakhtha == '/' || ikhowudi_yekharakhtha == '\\') return 0;
        ifayile_ufako_nkcukacha_igama[개수++] = ikhowudi_yekharakhtha;
    }
    ifayile_ufako_nkcukacha_igama[개수] = 0; return 1;
}
static void thumela_uludwe(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int 개수 = 자바파일항목길이(순번); if (개수 <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned 항목수 = strlen(앞부분); memcpy(gqithisela_imo + 사용량, 앞부분, 항목수); 사용량 += 항목수;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)gqithisela_imo, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        항목수 = strlen(뒷부분); memcpy(gqithisela_imo + 사용량, 뒷부분, 항목수); 사용량 += 항목수;
        for (int 안쪽순번 = 0; 안쪽순번 < 개수; 안쪽순번++) gqithisela_imo[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        gqithisela_imo[사용량++] = '\r'; gqithisela_imo[사용량++] = '\n';
    }
}
static void lungisa_ozenzela_ngokwakho_uqhagamshelo(int 확장여부) {
    if (수행작업) { phendula("450 Transfer in progress\r\n"); return; }
    misa_gqithisela(); ozenzela_ngokwakho_uqhagamshelo = 통신끝점만들기(1);
    if (ozenzela_ngokwakho_uqhagamshelo >= 0) 통신주소재사용(ozenzela_ngokwakho_uqhagamshelo);
    unsigned 접속번호 = 50000 + 다음접속번호++ % 8;
    if (ozenzela_ngokwakho_uqhagamshelo < 0 || 망주소묶기(ozenzela_ngokwakho_uqhagamshelo, 망상태읽기(0,0), 접속번호) || 연결기다리기(ozenzela_ngokwakho_uqhagamshelo)) {
        misa_gqithisela(); phendula("425 Cannot open passive listener\r\n"); return;
    }
    char 응답자료[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned 개수 = strlen(앞부분); memcpy(응답자료, 앞부분, 개수);
    if (확장여부) { 수치(접속번호, 응답자료, &개수); 응답자료[개수++] = '|'; }
    else {
        uint32_t idilesi=망상태읽기(0,0);
        for (int 자리=24;자리>=0;자리-=8) { 수치((idilesi>>자리)&255,응답자료,&개수);응답자료[개수++]=','; }
        수치(접속번호 / 256, 응답자료, &개수); 응답자료[개수++] = ','; 수치(접속번호 % 256, 응답자료, &개수);
    }
    응답자료[개수++] = ')'; 응답자료[개수++] = '\r'; 응답자료[개수++] = '\n'; 응답자료[개수] = 0; phendula(응답자료);
}
static void Umyalelo(void) {
    umgca[umgca_isayizi] = 0;
    char *부가인수 = umgca; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(umgca, "QUIT")) { misa_gqithisela(); phendula("221 Goodbye\r\n"); 끝내기 = 1; return; }
    if (같은지(umgca, "NOOP")) { phendula("200 OK\r\n"); return; }
    if (같은지(umgca, "SYST")) { phendula("215 UNIX Type: L8\r\n"); return; }
    if (같은지(umgca, "FEAT")) { phendula("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(umgca, "USER")) { 로그인됨 = 0; 사용자확인 = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); phendula(사용자확인 ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(umgca, "PASS")) { 로그인됨 = 사용자확인; phendula(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { phendula("530 Login first\r\n"); return; }
    if (같은지(umgca, "PWD")) phendula("257 \"/\"\r\n");
    else if (같은지(umgca, "CWD")) phendula(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(umgca, "TYPE")) phendula(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(umgca, "OPTS")) phendula(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(umgca, "PASV")) lungisa_ozenzela_ngokwakho_uqhagamshelo(0);
    else if (같은지(umgca, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) phendula("522 IPv4 only\r\n"); else lungisa_ozenzela_ngokwakho_uqhagamshelo(1); }
    else if (같은지(umgca, "ABOR")) { misa_gqithisela(); phendula("226 Transfer aborted\r\n"); }
    else if (같은지(umgca, "DELE")) { phendula(INDLELA(부가인수) && pk_unlink(ifayile_ufako_nkcukacha_igama) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(umgca, "LIST") || 같은지(umgca, "NLST") || 같은지(umgca, "MLSD")) {
        if (수행작업) { phendula("450 Transfer in progress\r\n"); return; }
        if (ozenzela_ngokwakho_uqhagamshelo < 0 && iingcombolo < 0) { phendula("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { phendula("550 Root listing only\r\n"); return; }
        thumela_uludwe(같은지(umgca,"MLSD") ? 2 : 같은지(umgca,"LIST") ? 1 : 0); 수행작업 = 2;
        phendula("150 Opening directory listing\r\n");
    }
    else if (같은지(umgca, "SIZE")) {
        if (!INDLELA(부가인수)) { phendula("550 Invalid filename\r\n"); return; }
        int ifayile_isibambi = pk_open(ifayile_ufako_nkcukacha_igama, efundwayo_kuphela_ixabiso, 0); if (ifayile_isibambi < 0) { phendula("550 File unavailable\r\n"); return; }
        int Ubukhulu = pk_size(ifayile_isibambi); pk_close(ifayile_isibambi); char 응답자료[32] = "213 "; unsigned 개수 = 4;
        수치(Ubukhulu, 응답자료, &개수); 응답자료[개수++] = '\r'; 응답자료[개수++] = '\n'; 응답자료[개수] = 0; phendula(응답자료);
    } else if (같은지(umgca, "STOR") || 같은지(umgca, "RETR")) {
        if (수행작업) { phendula("450 Transfer in progress\r\n"); return; }
        if (ozenzela_ngokwakho_uqhagamshelo < 0 && iingcombolo < 0) { phendula("425 Use PASV or EPSV\r\n"); return; }
        if (!INDLELA(부가인수)) { phendula("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(umgca, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(gqithisela_igama, ifayile_ufako_nkcukacha_igama, strlen(ifayile_ufako_nkcukacha_igama) + 1);
        if (수행작업 == 2) {
            int ifayile_isibambi = pk_open(ifayile_ufako_nkcukacha_igama, efundwayo_kuphela_ixabiso, 0);
            if (ifayile_isibambi < 0) { 수행작업 = 0; phendula("550 File unavailable\r\n"); return; }
            int 개수 = pk_read(ifayile_isibambi, gqithisela_imo, sizeof(gqithisela_imo)); pk_close(ifayile_isibambi);
            if (개수 < 0) { 수행작업 = 0; phendula("451 Read failed\r\n"); return; } 사용량 = 개수;
        }
        phendula("150 Opening binary data connection\r\n");
    } else phendula("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (수신창구 < 0) return;
    int 들어온연결 = 망연결받기(수신창구);
    if (들어온연결 >= 0) {
        if (isilawuli >= 0) { 통신쓰기(들어온연결, "421 One session at a time\r\n", 27); vala_Inethiwekhi(들어온연결); }
        else { isilawuli = 들어온연결; Umsebenzi = 보드밀리초(); phendula("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (isilawuli < 0) return;
    if ((uint32_t)(보드밀리초() - Umsebenzi) > 60000) { qhawula_uqhagamshelwano(); return; }
    if (!끝내기) for (unsigned 처리한도 = 0; 처리한도 < 256; 처리한도++) {
        unsigned char ikhowudi_yekharakhtha; int 반환값 = 통신읽기(isilawuli, &ikhowudi_yekharakhtha, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { qhawula_uqhagamshelwano(); return; } Umsebenzi = 보드밀리초();
        if (ikhowudi_yekharakhtha == '\n') { if (줄오류) phendula("500 Command too long or invalid\r\n"); else Umyalelo(); umgca_isayizi = 줄오류 = 0; if (끝내기) break; }
        else if (ikhowudi_yekharakhtha != '\r') { if (!ikhowudi_yekharakhtha || umgca_isayizi >= sizeof(umgca) - 1) 줄오류 = 1; else umgca[umgca_isayizi++] = ikhowudi_yekharakhtha; }
    }
    if (ozenzela_ngokwakho_uqhagamshelo >= 0 && iingcombolo < 0) {
        int 반환값 = 망연결받기(ozenzela_ngokwakho_uqhagamshelo);
        if (반환값 >= 0) {
            if (상대통신주소(반환값) != 상대통신주소(isilawuli)) vala_Inethiwekhi(반환값);
            else { iingcombolo = 반환값; vala_Inethiwekhi(ozenzela_ngokwakho_uqhagamshelo); ozenzela_ngokwakho_uqhagamshelo = -1; Umsebenzi = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && iingcombolo >= 0) for (unsigned 처리한도 = 0; 처리한도 < 8; 처리한도++) {
        unsigned char iingcombolo_thintela[512]; int 개수 = 통신읽기(iingcombolo, iingcombolo_thintela, sizeof(iingcombolo_thintela));
        if (개수 == -11) break;
        if (개수 < 0) { misa_gqithisela(); phendula("426 Data connection failed\r\n"); break; }
        Umsebenzi = 보드밀리초();
        if (개수 == 0) {
            int 결과 = -1;
            if (!실패여부) {
                int ifayile_isibambi = pk_open(gqithisela_igama, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (ifayile_isibambi >= 0) { 결과 = pk_write(ifayile_isibambi, gqithisela_imo, 사용량); pk_close(ifayile_isibambi); }
            }
            int 성공여부 = !실패여부 && 결과 == (int)사용량; misa_gqithisela(); phendula(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)개수 > sizeof(gqithisela_imo) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(gqithisela_imo + 사용량, iingcombolo_thintela, 개수); 사용량 += 개수; }
    }
    if (수행작업 == 2 && iingcombolo >= 0) {
        int 개수 = 통신쓰기(iingcombolo, gqithisela_imo + 보낸수, 사용량 - 보낸수);
        if (개수 >= 0) { 보낸수 += 개수; Umsebenzi = 보드밀리초(); if (보낸수 == 사용량) { misa_gqithisela(); phendula("226 Transfer complete\r\n"); } }
        else if (개수 != -11) { misa_gqithisela(); phendula("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < phendula_isayizi) {
        int 개수 = 통신쓰기(isilawuli, 응답모음 + 응답전송량, phendula_isayizi - 응답전송량);
        if (개수 > 0) 응답전송량 += 개수; else if (개수 != -11) { qhawula_uqhagamshelwano(); return; }
    }
    if (응답전송량 == phendula_isayizi) { phendula_isayizi = 응답전송량 = 0; if (끝내기) qhawula_uqhagamshelwano(); }
}
