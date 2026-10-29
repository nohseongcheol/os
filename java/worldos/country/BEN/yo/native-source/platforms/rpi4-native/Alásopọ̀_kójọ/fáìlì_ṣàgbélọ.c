#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "Alásopọ̀_kójọ.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int 수신창구 = -1, ìdarí = -1, aláfọwọ́ṣe_Ìsomọ́ = -1, détà = -1;
static unsigned 로그인됨, 사용자확인, ìlà_ìwọn, 줄오류, 끝내기, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned Fèsì_ìwọn, 응답전송량, 다음접속번호;
static uint32_t Iṣẹ́_ṣiṣe;
static char ìlà[256], 응답모음[2048], fáìlì_ìgbéwọlé_orúkọ[64], ṣàgbélọ_orúkọ[64];
static unsigned char ṣàgbélọ_ipò[16384];
static int 같은지(const char *첫째값, const char *둘째값) { while (*첫째값 && *첫째값 == *둘째값) { 첫째값++; 둘째값++; } return *첫째값 == *둘째값; }
static void Fèsì(const char *fọ́nrán_détà) {
    size_t 개수 = strlen(fọ́nrán_détà);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, Fèsì_ìwọn - 응답전송량); Fèsì_ìwọn -= 응답전송량; 응답전송량 = 0; }
    if (개수 > sizeof(응답모음) - Fèsì_ìwọn) { 끝내기 = 1; return; }
    memcpy(응답모음 + Fèsì_ìwọn, fọ́nrán_détà, 개수); Fèsì_ìwọn += 개수;
}
static void 수치(unsigned iye, char *결과자료, unsigned *개수) {
    char 숫자수[10]; unsigned 항목수 = 0;
    do { 숫자수[항목수++] = '0' + iye % 10; iye /= 10; } while (iye);
    while (항목수) 결과자료[(*개수)++] = 숫자수[--항목수];
}
static void dúró_ṣàgbélọ(void) {
    if (détà >= 0) pa_dé_Alásopọ̀(détà); if (aláfọwọ́ṣe_Ìsomọ́ >= 0) pa_dé_Alásopọ̀(aláfọwọ́ṣe_Ìsomọ́);
    détà = aláfọwọ́ṣe_Ìsomọ́ = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void ṣèpínyà(void) {
    dúró_ṣàgbélọ(); if (ìdarí >= 0) pa_dé_Alásopọ̀(ìdarí); ìdarí = -1;
    로그인됨 = 사용자확인 = ìlà_ìwọn = 줄오류 = Fèsì_ìwọn = 응답전송량 = 끝내기 = 0;
}
int fáìlì_ṣàgbélọ_ìdarí(int ìṣe) {
    if (ìṣe == 2) return 수신창구 >= 0;
    if (ìṣe == 0) { ṣèpínyà(); if (수신창구 >= 0) pa_dé_Alásopọ̀(수신창구); 수신창구 = -1; return 0; }
    if (ìṣe != 1) return -22; if (수신창구 >= 0) return 0;
    수신창구 = 통신끝점만들기(1); if (수신창구 < 0) return 수신창구;
    int 반환값 = 망주소묶기(수신창구, 망상태읽기(0,0), 21); if (!반환값) 반환값 = 연결기다리기(수신창구);
    if (반환값 < 0) { pa_dé_Alásopọ̀(수신창구); 수신창구 = -1; } return 반환값;
}
static int ọ̀nà(const char *Orúkọ) {
    unsigned 개수 = 0; if (*Orúkọ == '/') Orúkọ++;
    if (!*Orúkọ || 같은지(Orúkọ, ".") || 같은지(Orúkọ, "..")) return 0;
    fáìlì_ìgbéwọlé_orúkọ[개수++] = '/';
    while (*Orúkọ) {
        unsigned char kóòdù_ẹyọ_ọ̀rọ̀ = *Orúkọ++;
        if (개수 >= 63 || kóòdù_ẹyọ_ọ̀rọ̀ < 32 || kóòdù_ẹyọ_ọ̀rọ̀ == 127 || kóòdù_ẹyọ_ọ̀rọ̀ == '/' || kóòdù_ẹyọ_ọ̀rọ̀ == '\\') return 0;
        fáìlì_ìgbéwọlé_orúkọ[개수++] = kóòdù_ẹyọ_ọ̀rọ̀;
    }
    fáìlì_ìgbéwọlé_orúkọ[개수] = 0; return 1;
}
static void í_meèlì_Àtòkọ(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int 개수 = 자바파일항목길이(순번); if (개수 <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned 항목수 = strlen(앞부분); memcpy(ṣàgbélọ_ipò + 사용량, 앞부분, 항목수); 사용량 += 항목수;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)ṣàgbélọ_ipò, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        항목수 = strlen(뒷부분); memcpy(ṣàgbélọ_ipò + 사용량, 뒷부분, 항목수); 사용량 += 항목수;
        for (int 안쪽순번 = 0; 안쪽순번 < 개수; 안쪽순번++) ṣàgbélọ_ipò[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        ṣàgbélọ_ipò[사용량++] = '\r'; ṣàgbélọ_ipò[사용량++] = '\n';
    }
}
static void gbaradì_aláfọwọ́ṣe_Ìsomọ́(int 확장여부) {
    if (수행작업) { Fèsì("450 Transfer in progress\r\n"); return; }
    dúró_ṣàgbélọ(); aláfọwọ́ṣe_Ìsomọ́ = 통신끝점만들기(1);
    if (aláfọwọ́ṣe_Ìsomọ́ >= 0) 통신주소재사용(aláfọwọ́ṣe_Ìsomọ́);
    unsigned 접속번호 = 50000 + 다음접속번호++ % 8;
    if (aláfọwọ́ṣe_Ìsomọ́ < 0 || 망주소묶기(aláfọwọ́ṣe_Ìsomọ́, 망상태읽기(0,0), 접속번호) || 연결기다리기(aláfọwọ́ṣe_Ìsomọ́)) {
        dúró_ṣàgbélọ(); Fèsì("425 Cannot open passive listener\r\n"); return;
    }
    char 응답자료[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned 개수 = strlen(앞부분); memcpy(응답자료, 앞부분, 개수);
    if (확장여부) { 수치(접속번호, 응답자료, &개수); 응답자료[개수++] = '|'; }
    else {
        uint32_t àdírẹ́ẹ̀sì=망상태읽기(0,0);
        for (int 자리=24;자리>=0;자리-=8) { 수치((àdírẹ́ẹ̀sì>>자리)&255,응답자료,&개수);응답자료[개수++]=','; }
        수치(접속번호 / 256, 응답자료, &개수); 응답자료[개수++] = ','; 수치(접속번호 % 256, 응답자료, &개수);
    }
    응답자료[개수++] = ')'; 응답자료[개수++] = '\r'; 응답자료[개수++] = '\n'; 응답자료[개수] = 0; Fèsì(응답자료);
}
static void Àṣẹ(void) {
    ìlà[ìlà_ìwọn] = 0;
    char *부가인수 = ìlà; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(ìlà, "QUIT")) { dúró_ṣàgbélọ(); Fèsì("221 Goodbye\r\n"); 끝내기 = 1; return; }
    if (같은지(ìlà, "NOOP")) { Fèsì("200 OK\r\n"); return; }
    if (같은지(ìlà, "SYST")) { Fèsì("215 UNIX Type: L8\r\n"); return; }
    if (같은지(ìlà, "FEAT")) { Fèsì("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(ìlà, "USER")) { 로그인됨 = 0; 사용자확인 = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); Fèsì(사용자확인 ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(ìlà, "PASS")) { 로그인됨 = 사용자확인; Fèsì(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { Fèsì("530 Login first\r\n"); return; }
    if (같은지(ìlà, "PWD")) Fèsì("257 \"/\"\r\n");
    else if (같은지(ìlà, "CWD")) Fèsì(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(ìlà, "TYPE")) Fèsì(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(ìlà, "OPTS")) Fèsì(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(ìlà, "PASV")) gbaradì_aláfọwọ́ṣe_Ìsomọ́(0);
    else if (같은지(ìlà, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) Fèsì("522 IPv4 only\r\n"); else gbaradì_aláfọwọ́ṣe_Ìsomọ́(1); }
    else if (같은지(ìlà, "ABOR")) { dúró_ṣàgbélọ(); Fèsì("226 Transfer aborted\r\n"); }
    else if (같은지(ìlà, "DELE")) { Fèsì(ọ̀nà(부가인수) && pk_unlink(fáìlì_ìgbéwọlé_orúkọ) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(ìlà, "LIST") || 같은지(ìlà, "NLST") || 같은지(ìlà, "MLSD")) {
        if (수행작업) { Fèsì("450 Transfer in progress\r\n"); return; }
        if (aláfọwọ́ṣe_Ìsomọ́ < 0 && détà < 0) { Fèsì("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { Fèsì("550 Root listing only\r\n"); return; }
        í_meèlì_Àtòkọ(같은지(ìlà,"MLSD") ? 2 : 같은지(ìlà,"LIST") ? 1 : 0); 수행작업 = 2;
        Fèsì("150 Opening directory listing\r\n");
    }
    else if (같은지(ìlà, "SIZE")) {
        if (!ọ̀nà(부가인수)) { Fèsì("550 Invalid filename\r\n"); return; }
        int fáìlì_èkù = pk_open(fáìlì_ìgbéwọlé_orúkọ, kàn_kàá_iye, 0); if (fáìlì_èkù < 0) { Fèsì("550 File unavailable\r\n"); return; }
        int Ìwọ̀n = pk_size(fáìlì_èkù); pk_close(fáìlì_èkù); char 응답자료[32] = "213 "; unsigned 개수 = 4;
        수치(Ìwọ̀n, 응답자료, &개수); 응답자료[개수++] = '\r'; 응답자료[개수++] = '\n'; 응답자료[개수] = 0; Fèsì(응답자료);
    } else if (같은지(ìlà, "STOR") || 같은지(ìlà, "RETR")) {
        if (수행작업) { Fèsì("450 Transfer in progress\r\n"); return; }
        if (aláfọwọ́ṣe_Ìsomọ́ < 0 && détà < 0) { Fèsì("425 Use PASV or EPSV\r\n"); return; }
        if (!ọ̀nà(부가인수)) { Fèsì("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(ìlà, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(ṣàgbélọ_orúkọ, fáìlì_ìgbéwọlé_orúkọ, strlen(fáìlì_ìgbéwọlé_orúkọ) + 1);
        if (수행작업 == 2) {
            int fáìlì_èkù = pk_open(fáìlì_ìgbéwọlé_orúkọ, kàn_kàá_iye, 0);
            if (fáìlì_èkù < 0) { 수행작업 = 0; Fèsì("550 File unavailable\r\n"); return; }
            int 개수 = pk_read(fáìlì_èkù, ṣàgbélọ_ipò, sizeof(ṣàgbélọ_ipò)); pk_close(fáìlì_èkù);
            if (개수 < 0) { 수행작업 = 0; Fèsì("451 Read failed\r\n"); return; } 사용량 = 개수;
        }
        Fèsì("150 Opening binary data connection\r\n");
    } else Fèsì("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (수신창구 < 0) return;
    int 들어온연결 = 망연결받기(수신창구);
    if (들어온연결 >= 0) {
        if (ìdarí >= 0) { 통신쓰기(들어온연결, "421 One session at a time\r\n", 27); pa_dé_Alásopọ̀(들어온연결); }
        else { ìdarí = 들어온연결; Iṣẹ́_ṣiṣe = 보드밀리초(); Fèsì("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (ìdarí < 0) return;
    if ((uint32_t)(보드밀리초() - Iṣẹ́_ṣiṣe) > 60000) { ṣèpínyà(); return; }
    if (!끝내기) for (unsigned 처리한도 = 0; 처리한도 < 256; 처리한도++) {
        unsigned char kóòdù_ẹyọ_ọ̀rọ̀; int 반환값 = 통신읽기(ìdarí, &kóòdù_ẹyọ_ọ̀rọ̀, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { ṣèpínyà(); return; } Iṣẹ́_ṣiṣe = 보드밀리초();
        if (kóòdù_ẹyọ_ọ̀rọ̀ == '\n') { if (줄오류) Fèsì("500 Command too long or invalid\r\n"); else Àṣẹ(); ìlà_ìwọn = 줄오류 = 0; if (끝내기) break; }
        else if (kóòdù_ẹyọ_ọ̀rọ̀ != '\r') { if (!kóòdù_ẹyọ_ọ̀rọ̀ || ìlà_ìwọn >= sizeof(ìlà) - 1) 줄오류 = 1; else ìlà[ìlà_ìwọn++] = kóòdù_ẹyọ_ọ̀rọ̀; }
    }
    if (aláfọwọ́ṣe_Ìsomọ́ >= 0 && détà < 0) {
        int 반환값 = 망연결받기(aláfọwọ́ṣe_Ìsomọ́);
        if (반환값 >= 0) {
            if (상대통신주소(반환값) != 상대통신주소(ìdarí)) pa_dé_Alásopọ̀(반환값);
            else { détà = 반환값; pa_dé_Alásopọ̀(aláfọwọ́ṣe_Ìsomọ́); aláfọwọ́ṣe_Ìsomọ́ = -1; Iṣẹ́_ṣiṣe = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && détà >= 0) for (unsigned 처리한도 = 0; 처리한도 < 8; 처리한도++) {
        unsigned char détà_sèdíwọ[512]; int 개수 = 통신읽기(détà, détà_sèdíwọ, sizeof(détà_sèdíwọ));
        if (개수 == -11) break;
        if (개수 < 0) { dúró_ṣàgbélọ(); Fèsì("426 Data connection failed\r\n"); break; }
        Iṣẹ́_ṣiṣe = 보드밀리초();
        if (개수 == 0) {
            int 결과 = -1;
            if (!실패여부) {
                int fáìlì_èkù = pk_open(ṣàgbélọ_orúkọ, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (fáìlì_èkù >= 0) { 결과 = pk_write(fáìlì_èkù, ṣàgbélọ_ipò, 사용량); pk_close(fáìlì_èkù); }
            }
            int 성공여부 = !실패여부 && 결과 == (int)사용량; dúró_ṣàgbélọ(); Fèsì(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)개수 > sizeof(ṣàgbélọ_ipò) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(ṣàgbélọ_ipò + 사용량, détà_sèdíwọ, 개수); 사용량 += 개수; }
    }
    if (수행작업 == 2 && détà >= 0) {
        int 개수 = 통신쓰기(détà, ṣàgbélọ_ipò + 보낸수, 사용량 - 보낸수);
        if (개수 >= 0) { 보낸수 += 개수; Iṣẹ́_ṣiṣe = 보드밀리초(); if (보낸수 == 사용량) { dúró_ṣàgbélọ(); Fèsì("226 Transfer complete\r\n"); } }
        else if (개수 != -11) { dúró_ṣàgbélọ(); Fèsì("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < Fèsì_ìwọn) {
        int 개수 = 통신쓰기(ìdarí, 응답모음 + 응답전송량, Fèsì_ìwọn - 응답전송량);
        if (개수 > 0) 응답전송량 += 개수; else if (개수 != -11) { ṣèpínyà(); return; }
    }
    if (응답전송량 == Fèsì_ìwọn) { Fèsì_ìwọn = 응답전송량 = 0; if (끝내기) ṣèpínyà(); }
}
