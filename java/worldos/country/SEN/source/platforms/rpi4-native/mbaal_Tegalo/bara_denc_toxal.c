#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "mbaal_Tegalo.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int 수신창구 = -1, Saytu_doxinu_ordinateur = -1, téere_leeral_jokkalóo = -1, mbir = -1;
static unsigned 로그인됨, 사용자확인, buum_tolluwaay, 줄오류, 끝내기, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned tontu_tolluwaay, 응답전송량, 다음접속번호;
static uint32_t Jëf;
static char buum[256], 응답모음[2048], bara_denc_dugal_xabaar_tur[64], toxal_tur[64];
static unsigned char toxal_nekkin[16384];
static int 같은지(const char *첫째값, const char *둘째값) { while (*첫째값 && *첫째값 == *둘째값) { 첫째값++; 둘째값++; } return *첫째값 == *둘째값; }
static void tontu(const char *araf_yu_bennoo_mbir) {
    size_t 개수 = strlen(araf_yu_bennoo_mbir);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, tontu_tolluwaay - 응답전송량); tontu_tolluwaay -= 응답전송량; 응답전송량 = 0; }
    if (개수 > sizeof(응답모음) - tontu_tolluwaay) { 끝내기 = 1; return; }
    memcpy(응답모음 + tontu_tolluwaay, araf_yu_bennoo_mbir, 개수); tontu_tolluwaay += 개수;
}
static void 수치(unsigned xëyma, char *결과자료, unsigned *개수) {
    char 숫자수[10]; unsigned 항목수 = 0;
    do { 숫자수[항목수++] = '0' + xëyma % 10; xëyma /= 10; } while (xëyma);
    while (항목수) 결과자료[(*개수)++] = 숫자수[--항목수];
}
static void tees_toxal(void) {
    if (mbir >= 0) Tej_mbaal(mbir); if (téere_leeral_jokkalóo >= 0) Tej_mbaal(téere_leeral_jokkalóo);
    mbir = téere_leeral_jokkalóo = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void dakkal_jokkoo(void) {
    tees_toxal(); if (Saytu_doxinu_ordinateur >= 0) Tej_mbaal(Saytu_doxinu_ordinateur); Saytu_doxinu_ordinateur = -1;
    로그인됨 = 사용자확인 = buum_tolluwaay = 줄오류 = tontu_tolluwaay = 응답전송량 = 끝내기 = 0;
}
int bara_denc_toxal_Saytu_doxinu_ordinateur(int jëf) {
    if (jëf == 2) return 수신창구 >= 0;
    if (jëf == 0) { dakkal_jokkoo(); if (수신창구 >= 0) Tej_mbaal(수신창구); 수신창구 = -1; return 0; }
    if (jëf != 1) return -22; if (수신창구 >= 0) return 0;
    수신창구 = 통신끝점만들기(1); if (수신창구 < 0) return 수신창구;
    int 반환값 = 망주소묶기(수신창구, 망상태읽기(0,0), 21); if (!반환값) 반환값 = 연결기다리기(수신창구);
    if (반환값 < 0) { Tej_mbaal(수신창구); 수신창구 = -1; } return 반환값;
}
static int Yoonu_jëmale(const char *tur_253d1510) {
    unsigned 개수 = 0; if (*tur_253d1510 == '/') tur_253d1510++;
    if (!*tur_253d1510 || 같은지(tur_253d1510, ".") || 같은지(tur_253d1510, "..")) return 0;
    bara_denc_dugal_xabaar_tur[개수++] = '/';
    while (*tur_253d1510) {
        unsigned char kotu_araf = *tur_253d1510++;
        if (개수 >= 63 || kotu_araf < 32 || kotu_araf == 127 || kotu_araf == '/' || kotu_araf == '\\') return 0;
        bara_denc_dugal_xabaar_tur[개수++] = kotu_araf;
    }
    bara_denc_dugal_xabaar_tur[개수] = 0; return 1;
}
static void Yónnee_lim(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int 개수 = 자바파일항목길이(순번); if (개수 <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned 항목수 = strlen(앞부분); memcpy(toxal_nekkin + 사용량, 앞부분, 항목수); 사용량 += 항목수;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)toxal_nekkin, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        항목수 = strlen(뒷부분); memcpy(toxal_nekkin + 사용량, 뒷부분, 항목수); 사용량 += 항목수;
        for (int 안쪽순번 = 0; 안쪽순번 < 개수; 안쪽순번++) toxal_nekkin[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        toxal_nekkin[사용량++] = '\r'; toxal_nekkin[사용량++] = '\n';
    }
}
static void jël_matuwaay_téere_leeral_jokkalóo(int 확장여부) {
    if (수행작업) { tontu("450 Transfer in progress\r\n"); return; }
    tees_toxal(); téere_leeral_jokkalóo = 통신끝점만들기(1);
    if (téere_leeral_jokkalóo >= 0) 통신주소재사용(téere_leeral_jokkalóo);
    unsigned 접속번호 = 50000 + 다음접속번호++ % 8;
    if (téere_leeral_jokkalóo < 0 || 망주소묶기(téere_leeral_jokkalóo, 망상태읽기(0,0), 접속번호) || 연결기다리기(téere_leeral_jokkalóo)) {
        tees_toxal(); tontu("425 Cannot open passive listener\r\n"); return;
    }
    char 응답자료[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned 개수 = strlen(앞부분); memcpy(응답자료, 앞부분, 개수);
    if (확장여부) { 수치(접속번호, 응답자료, &개수); 응답자료[개수++] = '|'; }
    else {
        uint32_t dëkkuwaay=망상태읽기(0,0);
        for (int 자리=24;자리>=0;자리-=8) { 수치((dëkkuwaay>>자리)&255,응답자료,&개수);응답자료[개수++]=','; }
        수치(접속번호 / 256, 응답자료, &개수); 응답자료[개수++] = ','; 수치(접속번호 % 256, 응답자료, &개수);
    }
    응답자료[개수++] = ')'; 응답자료[개수++] = '\r'; 응답자료[개수++] = '\n'; 응답자료[개수] = 0; tontu(응답자료);
}
static void ndigel(void) {
    buum[buum_tolluwaay] = 0;
    char *부가인수 = buum; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(buum, "QUIT")) { tees_toxal(); tontu("221 Goodbye\r\n"); 끝내기 = 1; return; }
    if (같은지(buum, "NOOP")) { tontu("200 OK\r\n"); return; }
    if (같은지(buum, "SYST")) { tontu("215 UNIX Type: L8\r\n"); return; }
    if (같은지(buum, "FEAT")) { tontu("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(buum, "USER")) { 로그인됨 = 0; 사용자확인 = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); tontu(사용자확인 ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(buum, "PASS")) { 로그인됨 = 사용자확인; tontu(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { tontu("530 Login first\r\n"); return; }
    if (같은지(buum, "PWD")) tontu("257 \"/\"\r\n");
    else if (같은지(buum, "CWD")) tontu(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(buum, "TYPE")) tontu(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(buum, "OPTS")) tontu(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(buum, "PASV")) jël_matuwaay_téere_leeral_jokkalóo(0);
    else if (같은지(buum, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) tontu("522 IPv4 only\r\n"); else jël_matuwaay_téere_leeral_jokkalóo(1); }
    else if (같은지(buum, "ABOR")) { tees_toxal(); tontu("226 Transfer aborted\r\n"); }
    else if (같은지(buum, "DELE")) { tontu(Yoonu_jëmale(부가인수) && pk_unlink(bara_denc_dugal_xabaar_tur) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(buum, "LIST") || 같은지(buum, "NLST") || 같은지(buum, "MLSD")) {
        if (수행작업) { tontu("450 Transfer in progress\r\n"); return; }
        if (téere_leeral_jokkalóo < 0 && mbir < 0) { tontu("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { tontu("550 Root listing only\r\n"); return; }
        Yónnee_lim(같은지(buum,"MLSD") ? 2 : 같은지(buum,"LIST") ? 1 : 0); 수행작업 = 2;
        tontu("150 Opening directory listing\r\n");
    }
    else if (같은지(buum, "SIZE")) {
        if (!Yoonu_jëmale(부가인수)) { tontu("550 Invalid filename\r\n"); return; }
        int bara_denc_yombal = pk_open(bara_denc_dugal_xabaar_tur, ngir_jaŋarek_la_xëyma, 0); if (bara_denc_yombal < 0) { tontu("550 File unavailable\r\n"); return; }
        int tolluwaay = pk_size(bara_denc_yombal); pk_close(bara_denc_yombal); char 응답자료[32] = "213 "; unsigned 개수 = 4;
        수치(tolluwaay, 응답자료, &개수); 응답자료[개수++] = '\r'; 응답자료[개수++] = '\n'; 응답자료[개수] = 0; tontu(응답자료);
    } else if (같은지(buum, "STOR") || 같은지(buum, "RETR")) {
        if (수행작업) { tontu("450 Transfer in progress\r\n"); return; }
        if (téere_leeral_jokkalóo < 0 && mbir < 0) { tontu("425 Use PASV or EPSV\r\n"); return; }
        if (!Yoonu_jëmale(부가인수)) { tontu("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(buum, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(toxal_tur, bara_denc_dugal_xabaar_tur, strlen(bara_denc_dugal_xabaar_tur) + 1);
        if (수행작업 == 2) {
            int bara_denc_yombal = pk_open(bara_denc_dugal_xabaar_tur, ngir_jaŋarek_la_xëyma, 0);
            if (bara_denc_yombal < 0) { 수행작업 = 0; tontu("550 File unavailable\r\n"); return; }
            int 개수 = pk_read(bara_denc_yombal, toxal_nekkin, sizeof(toxal_nekkin)); pk_close(bara_denc_yombal);
            if (개수 < 0) { 수행작업 = 0; tontu("451 Read failed\r\n"); return; } 사용량 = 개수;
        }
        tontu("150 Opening binary data connection\r\n");
    } else tontu("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (수신창구 < 0) return;
    int 들어온연결 = 망연결받기(수신창구);
    if (들어온연결 >= 0) {
        if (Saytu_doxinu_ordinateur >= 0) { 통신쓰기(들어온연결, "421 One session at a time\r\n", 27); Tej_mbaal(들어온연결); }
        else { Saytu_doxinu_ordinateur = 들어온연결; Jëf = 보드밀리초(); tontu("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (Saytu_doxinu_ordinateur < 0) return;
    if ((uint32_t)(보드밀리초() - Jëf) > 60000) { dakkal_jokkoo(); return; }
    if (!끝내기) for (unsigned 처리한도 = 0; 처리한도 < 256; 처리한도++) {
        unsigned char kotu_araf; int 반환값 = 통신읽기(Saytu_doxinu_ordinateur, &kotu_araf, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { dakkal_jokkoo(); return; } Jëf = 보드밀리초();
        if (kotu_araf == '\n') { if (줄오류) tontu("500 Command too long or invalid\r\n"); else ndigel(); buum_tolluwaay = 줄오류 = 0; if (끝내기) break; }
        else if (kotu_araf != '\r') { if (!kotu_araf || buum_tolluwaay >= sizeof(buum) - 1) 줄오류 = 1; else buum[buum_tolluwaay++] = kotu_araf; }
    }
    if (téere_leeral_jokkalóo >= 0 && mbir < 0) {
        int 반환값 = 망연결받기(téere_leeral_jokkalóo);
        if (반환값 >= 0) {
            if (상대통신주소(반환값) != 상대통신주소(Saytu_doxinu_ordinateur)) Tej_mbaal(반환값);
            else { mbir = 반환값; Tej_mbaal(téere_leeral_jokkalóo); téere_leeral_jokkalóo = -1; Jëf = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && mbir >= 0) for (unsigned 처리한도 = 0; 처리한도 < 8; 처리한도++) {
        unsigned char mbir_gatandu[512]; int 개수 = 통신읽기(mbir, mbir_gatandu, sizeof(mbir_gatandu));
        if (개수 == -11) break;
        if (개수 < 0) { tees_toxal(); tontu("426 Data connection failed\r\n"); break; }
        Jëf = 보드밀리초();
        if (개수 == 0) {
            int 결과 = -1;
            if (!실패여부) {
                int bara_denc_yombal = pk_open(toxal_tur, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (bara_denc_yombal >= 0) { 결과 = pk_write(bara_denc_yombal, toxal_nekkin, 사용량); pk_close(bara_denc_yombal); }
            }
            int 성공여부 = !실패여부 && 결과 == (int)사용량; tees_toxal(); tontu(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)개수 > sizeof(toxal_nekkin) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(toxal_nekkin + 사용량, mbir_gatandu, 개수); 사용량 += 개수; }
    }
    if (수행작업 == 2 && mbir >= 0) {
        int 개수 = 통신쓰기(mbir, toxal_nekkin + 보낸수, 사용량 - 보낸수);
        if (개수 >= 0) { 보낸수 += 개수; Jëf = 보드밀리초(); if (보낸수 == 사용량) { tees_toxal(); tontu("226 Transfer complete\r\n"); } }
        else if (개수 != -11) { tees_toxal(); tontu("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < tontu_tolluwaay) {
        int 개수 = 통신쓰기(Saytu_doxinu_ordinateur, 응답모음 + 응답전송량, tontu_tolluwaay - 응답전송량);
        if (개수 > 0) 응답전송량 += 개수; else if (개수 != -11) { dakkal_jokkoo(); return; }
    }
    if (응답전송량 == tontu_tolluwaay) { tontu_tolluwaay = 응답전송량 = 0; if (끝내기) dakkal_jokkoo(); }
}
