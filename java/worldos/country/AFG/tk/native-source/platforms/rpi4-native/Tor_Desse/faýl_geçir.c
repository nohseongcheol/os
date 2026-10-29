#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "Tor_Desse.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int 수신창구 = -1, dolandyryş = -1, el_bilen_edilýän_birikme = -1, maglumat = -1;
static unsigned 로그인됨, 사용자확인, setir_ölçegi_üýtget, 줄오류, 끝내기, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned jogap_bermek_ölçegi_üýtget, 응답전송량, 다음접속번호;
static uint32_t Işjeňlik;
static char setir[256], 응답모음[2048], faýl_girizmeklik_at[64], geçir_at[64];
static unsigned char geçir_ýagdaý[16384];
static int 같은지(const char *첫째값, const char *둘째값) { while (*첫째값 && *첫째값 == *둘째값) { 첫째값++; 둘째값++; } return *첫째값 == *둘째값; }
static void jogap_bermek(const char *setir_maglumat) {
    size_t 개수 = strlen(setir_maglumat);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, jogap_bermek_ölçegi_üýtget - 응답전송량); jogap_bermek_ölçegi_üýtget -= 응답전송량; 응답전송량 = 0; }
    if (개수 > sizeof(응답모음) - jogap_bermek_ölçegi_üýtget) { 끝내기 = 1; return; }
    memcpy(응답모음 + jogap_bermek_ölçegi_üýtget, setir_maglumat, 개수); jogap_bermek_ölçegi_üýtget += 개수;
}
static void 수치(unsigned baha, char *결과자료, unsigned *개수) {
    char 숫자수[10]; unsigned 항목수 = 0;
    do { 숫자수[항목수++] = '0' + baha % 10; baha /= 10; } while (baha);
    while (항목수) 결과자료[(*개수)++] = 숫자수[--항목수];
}
static void duruz_geçir(void) {
    if (maglumat >= 0) ýap_Tor(maglumat); if (el_bilen_edilýän_birikme >= 0) ýap_Tor(el_bilen_edilýän_birikme);
    maglumat = el_bilen_edilýän_birikme = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void birikimäni_kes(void) {
    duruz_geçir(); if (dolandyryş >= 0) ýap_Tor(dolandyryş); dolandyryş = -1;
    로그인됨 = 사용자확인 = setir_ölçegi_üýtget = 줄오류 = jogap_bermek_ölçegi_üýtget = 응답전송량 = 끝내기 = 0;
}
int faýl_geçir_dolandyryş(int iş) {
    if (iş == 2) return 수신창구 >= 0;
    if (iş == 0) { birikimäni_kes(); if (수신창구 >= 0) ýap_Tor(수신창구); 수신창구 = -1; return 0; }
    if (iş != 1) return -22; if (수신창구 >= 0) return 0;
    수신창구 = 통신끝점만들기(1); if (수신창구 < 0) return 수신창구;
    int 반환값 = 망주소묶기(수신창구, 망상태읽기(0,0), 21); if (!반환값) 반환값 = 연결기다리기(수신창구);
    if (반환값 < 0) { ýap_Tor(수신창구); 수신창구 = -1; } return 반환값;
}
static int Ýol(const char *Ad) {
    unsigned 개수 = 0; if (*Ad == '/') Ad++;
    if (!*Ad || 같은지(Ad, ".") || 같은지(Ad, "..")) return 0;
    faýl_girizmeklik_at[개수++] = '/';
    while (*Ad) {
        unsigned char nyşanyň_kody = *Ad++;
        if (개수 >= 63 || nyşanyň_kody < 32 || nyşanyň_kody == 127 || nyşanyň_kody == '/' || nyşanyň_kody == '\\') return 0;
        faýl_girizmeklik_at[개수++] = nyşanyň_kody;
    }
    faýl_girizmeklik_at[개수] = 0; return 1;
}
static void iber_Sanaw(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int 개수 = 자바파일항목길이(순번); if (개수 <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned 항목수 = strlen(앞부분); memcpy(geçir_ýagdaý + 사용량, 앞부분, 항목수); 사용량 += 항목수;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)geçir_ýagdaý, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        항목수 = strlen(뒷부분); memcpy(geçir_ýagdaý + 사용량, 뒷부분, 항목수); 사용량 += 항목수;
        for (int 안쪽순번 = 0; 안쪽순번 < 개수; 안쪽순번++) geçir_ýagdaý[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        geçir_ýagdaý[사용량++] = '\r'; geçir_ýagdaý[사용량++] = '\n';
    }
}
static void Taýýarla_el_bilen_edilýän_birikme(int 확장여부) {
    if (수행작업) { jogap_bermek("450 Transfer in progress\r\n"); return; }
    duruz_geçir(); el_bilen_edilýän_birikme = 통신끝점만들기(1);
    if (el_bilen_edilýän_birikme >= 0) 통신주소재사용(el_bilen_edilýän_birikme);
    unsigned 접속번호 = 50000 + 다음접속번호++ % 8;
    if (el_bilen_edilýän_birikme < 0 || 망주소묶기(el_bilen_edilýän_birikme, 망상태읽기(0,0), 접속번호) || 연결기다리기(el_bilen_edilýän_birikme)) {
        duruz_geçir(); jogap_bermek("425 Cannot open passive listener\r\n"); return;
    }
    char 응답자료[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned 개수 = strlen(앞부분); memcpy(응답자료, 앞부분, 개수);
    if (확장여부) { 수치(접속번호, 응답자료, &개수); 응답자료[개수++] = '|'; }
    else {
        uint32_t salgy=망상태읽기(0,0);
        for (int 자리=24;자리>=0;자리-=8) { 수치((salgy>>자리)&255,응답자료,&개수);응답자료[개수++]=','; }
        수치(접속번호 / 256, 응답자료, &개수); 응답자료[개수++] = ','; 수치(접속번호 % 256, 응답자료, &개수);
    }
    응답자료[개수++] = ')'; 응답자료[개수++] = '\r'; 응답자료[개수++] = '\n'; 응답자료[개수] = 0; jogap_bermek(응답자료);
}
static void buýruk(void) {
    setir[setir_ölçegi_üýtget] = 0;
    char *부가인수 = setir; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(setir, "QUIT")) { duruz_geçir(); jogap_bermek("221 Goodbye\r\n"); 끝내기 = 1; return; }
    if (같은지(setir, "NOOP")) { jogap_bermek("200 OK\r\n"); return; }
    if (같은지(setir, "SYST")) { jogap_bermek("215 UNIX Type: L8\r\n"); return; }
    if (같은지(setir, "FEAT")) { jogap_bermek("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(setir, "USER")) { 로그인됨 = 0; 사용자확인 = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); jogap_bermek(사용자확인 ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(setir, "PASS")) { 로그인됨 = 사용자확인; jogap_bermek(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { jogap_bermek("530 Login first\r\n"); return; }
    if (같은지(setir, "PWD")) jogap_bermek("257 \"/\"\r\n");
    else if (같은지(setir, "CWD")) jogap_bermek(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(setir, "TYPE")) jogap_bermek(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(setir, "OPTS")) jogap_bermek(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(setir, "PASV")) Taýýarla_el_bilen_edilýän_birikme(0);
    else if (같은지(setir, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) jogap_bermek("522 IPv4 only\r\n"); else Taýýarla_el_bilen_edilýän_birikme(1); }
    else if (같은지(setir, "ABOR")) { duruz_geçir(); jogap_bermek("226 Transfer aborted\r\n"); }
    else if (같은지(setir, "DELE")) { jogap_bermek(Ýol(부가인수) && pk_unlink(faýl_girizmeklik_at) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(setir, "LIST") || 같은지(setir, "NLST") || 같은지(setir, "MLSD")) {
        if (수행작업) { jogap_bermek("450 Transfer in progress\r\n"); return; }
        if (el_bilen_edilýän_birikme < 0 && maglumat < 0) { jogap_bermek("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { jogap_bermek("550 Root listing only\r\n"); return; }
        iber_Sanaw(같은지(setir,"MLSD") ? 2 : 같은지(setir,"LIST") ? 1 : 0); 수행작업 = 2;
        jogap_bermek("150 Opening directory listing\r\n");
    }
    else if (같은지(setir, "SIZE")) {
        if (!Ýol(부가인수)) { jogap_bermek("550 Invalid filename\r\n"); return; }
        int faýl_ryçag = pk_open(faýl_girizmeklik_at, diňe_okalýan_baha, 0); if (faýl_ryçag < 0) { jogap_bermek("550 File unavailable\r\n"); return; }
        int Ululyk = pk_size(faýl_ryçag); pk_close(faýl_ryçag); char 응답자료[32] = "213 "; unsigned 개수 = 4;
        수치(Ululyk, 응답자료, &개수); 응답자료[개수++] = '\r'; 응답자료[개수++] = '\n'; 응답자료[개수] = 0; jogap_bermek(응답자료);
    } else if (같은지(setir, "STOR") || 같은지(setir, "RETR")) {
        if (수행작업) { jogap_bermek("450 Transfer in progress\r\n"); return; }
        if (el_bilen_edilýän_birikme < 0 && maglumat < 0) { jogap_bermek("425 Use PASV or EPSV\r\n"); return; }
        if (!Ýol(부가인수)) { jogap_bermek("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(setir, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(geçir_at, faýl_girizmeklik_at, strlen(faýl_girizmeklik_at) + 1);
        if (수행작업 == 2) {
            int faýl_ryçag = pk_open(faýl_girizmeklik_at, diňe_okalýan_baha, 0);
            if (faýl_ryçag < 0) { 수행작업 = 0; jogap_bermek("550 File unavailable\r\n"); return; }
            int 개수 = pk_read(faýl_ryçag, geçir_ýagdaý, sizeof(geçir_ýagdaý)); pk_close(faýl_ryçag);
            if (개수 < 0) { 수행작업 = 0; jogap_bermek("451 Read failed\r\n"); return; } 사용량 = 개수;
        }
        jogap_bermek("150 Opening binary data connection\r\n");
    } else jogap_bermek("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (수신창구 < 0) return;
    int 들어온연결 = 망연결받기(수신창구);
    if (들어온연결 >= 0) {
        if (dolandyryş >= 0) { 통신쓰기(들어온연결, "421 One session at a time\r\n", 27); ýap_Tor(들어온연결); }
        else { dolandyryş = 들어온연결; Işjeňlik = 보드밀리초(); jogap_bermek("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (dolandyryş < 0) return;
    if ((uint32_t)(보드밀리초() - Işjeňlik) > 60000) { birikimäni_kes(); return; }
    if (!끝내기) for (unsigned 처리한도 = 0; 처리한도 < 256; 처리한도++) {
        unsigned char nyşanyň_kody; int 반환값 = 통신읽기(dolandyryş, &nyşanyň_kody, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { birikimäni_kes(); return; } Işjeňlik = 보드밀리초();
        if (nyşanyň_kody == '\n') { if (줄오류) jogap_bermek("500 Command too long or invalid\r\n"); else buýruk(); setir_ölçegi_üýtget = 줄오류 = 0; if (끝내기) break; }
        else if (nyşanyň_kody != '\r') { if (!nyşanyň_kody || setir_ölçegi_üýtget >= sizeof(setir) - 1) 줄오류 = 1; else setir[setir_ölçegi_üýtget++] = nyşanyň_kody; }
    }
    if (el_bilen_edilýän_birikme >= 0 && maglumat < 0) {
        int 반환값 = 망연결받기(el_bilen_edilýän_birikme);
        if (반환값 >= 0) {
            if (상대통신주소(반환값) != 상대통신주소(dolandyryş)) ýap_Tor(반환값);
            else { maglumat = 반환값; ýap_Tor(el_bilen_edilýän_birikme); el_bilen_edilýän_birikme = -1; Işjeňlik = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && maglumat >= 0) for (unsigned 처리한도 = 0; 처리한도 < 8; 처리한도++) {
        unsigned char maglumat_bökde[512]; int 개수 = 통신읽기(maglumat, maglumat_bökde, sizeof(maglumat_bökde));
        if (개수 == -11) break;
        if (개수 < 0) { duruz_geçir(); jogap_bermek("426 Data connection failed\r\n"); break; }
        Işjeňlik = 보드밀리초();
        if (개수 == 0) {
            int 결과 = -1;
            if (!실패여부) {
                int faýl_ryçag = pk_open(geçir_at, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (faýl_ryçag >= 0) { 결과 = pk_write(faýl_ryçag, geçir_ýagdaý, 사용량); pk_close(faýl_ryçag); }
            }
            int 성공여부 = !실패여부 && 결과 == (int)사용량; duruz_geçir(); jogap_bermek(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)개수 > sizeof(geçir_ýagdaý) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(geçir_ýagdaý + 사용량, maglumat_bökde, 개수); 사용량 += 개수; }
    }
    if (수행작업 == 2 && maglumat >= 0) {
        int 개수 = 통신쓰기(maglumat, geçir_ýagdaý + 보낸수, 사용량 - 보낸수);
        if (개수 >= 0) { 보낸수 += 개수; Işjeňlik = 보드밀리초(); if (보낸수 == 사용량) { duruz_geçir(); jogap_bermek("226 Transfer complete\r\n"); } }
        else if (개수 != -11) { duruz_geçir(); jogap_bermek("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < jogap_bermek_ölçegi_üýtget) {
        int 개수 = 통신쓰기(dolandyryş, 응답모음 + 응답전송량, jogap_bermek_ölçegi_üýtget - 응답전송량);
        if (개수 > 0) 응답전송량 += 개수; else if (개수 != -11) { birikimäni_kes(); return; }
    }
    if (응답전송량 == jogap_bermek_ölçegi_üýtget) { jogap_bermek_ölçegi_üýtget = 응답전송량 = 0; if (끝내기) birikimäni_kes(); }
}
