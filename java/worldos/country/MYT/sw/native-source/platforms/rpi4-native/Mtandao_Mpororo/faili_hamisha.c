#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "Mtandao_Mpororo.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int 수신창구 = -1, udhibiti = -1, a_mikono_muunganisho = -1, data = -1;
static unsigned 로그인됨, mtumiaji_Sawa, laini_panga_ukubwa, 줄오류, 끝내기, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned jibu_panga_ukubwa, 응답전송량, 다음접속번호;
static uint32_t Shughuli;
static char laini[256], 응답모음[2048], faili_ingizo_jina[64], hamisha_jina[64];
static unsigned char hamisha_hali[16384];
static int 같은지(const char *첫째값, const char *둘째값) { while (*첫째값 && *첫째값 == *둘째값) { 첫째값++; 둘째값++; } return *첫째값 == *둘째값; }
static void jibu(const char *tungo_data) {
    size_t 개수 = strlen(tungo_data);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, jibu_panga_ukubwa - 응답전송량); jibu_panga_ukubwa -= 응답전송량; 응답전송량 = 0; }
    if (개수 > sizeof(응답모음) - jibu_panga_ukubwa) { 끝내기 = 1; return; }
    memcpy(응답모음 + jibu_panga_ukubwa, tungo_data, 개수); jibu_panga_ukubwa += 개수;
}
static void 수치(unsigned thamani, char *결과자료, unsigned *개수) {
    char 숫자수[10]; unsigned 항목수 = 0;
    do { 숫자수[항목수++] = '0' + thamani % 10; thamani /= 10; } while (thamani);
    while (항목수) 결과자료[(*개수)++] = 숫자수[--항목수];
}
static void Simama_hamisha(void) {
    if (data >= 0) funga_Mtandao(data); if (a_mikono_muunganisho >= 0) funga_Mtandao(a_mikono_muunganisho);
    data = a_mikono_muunganisho = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void tenganisha(void) {
    Simama_hamisha(); if (udhibiti >= 0) funga_Mtandao(udhibiti); udhibiti = -1;
    로그인됨 = mtumiaji_Sawa = laini_panga_ukubwa = 줄오류 = jibu_panga_ukubwa = 응답전송량 = 끝내기 = 0;
}
int faili_hamisha_udhibiti(int Kitendo) {
    if (Kitendo == 2) return 수신창구 >= 0;
    if (Kitendo == 0) { tenganisha(); if (수신창구 >= 0) funga_Mtandao(수신창구); 수신창구 = -1; return 0; }
    if (Kitendo != 1) return -22; if (수신창구 >= 0) return 0;
    수신창구 = 통신끝점만들기(1); if (수신창구 < 0) return 수신창구;
    int 반환값 = 망주소묶기(수신창구, 망상태읽기(0,0), 21); if (!반환값) 반환값 = 연결기다리기(수신창구);
    if (반환값 < 0) { funga_Mtandao(수신창구); 수신창구 = -1; } return 반환값;
}
static int njia(const char *Jina) {
    unsigned 개수 = 0; if (*Jina == '/') Jina++;
    if (!*Jina || 같은지(Jina, ".") || 같은지(Jina, "..")) return 0;
    faili_ingizo_jina[개수++] = '/';
    while (*Jina) {
        unsigned char msimbo_wa_kibambo = *Jina++;
        if (개수 >= 63 || msimbo_wa_kibambo < 32 || msimbo_wa_kibambo == 127 || msimbo_wa_kibambo == '/' || msimbo_wa_kibambo == '\\') return 0;
        faili_ingizo_jina[개수++] = msimbo_wa_kibambo;
    }
    faili_ingizo_jina[개수] = 0; return 1;
}
static void tuma_Orodha(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int 개수 = 자바파일항목길이(순번); if (개수 <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned 항목수 = strlen(앞부분); memcpy(hamisha_hali + 사용량, 앞부분, 항목수); 사용량 += 항목수;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)hamisha_hali, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        항목수 = strlen(뒷부분); memcpy(hamisha_hali + 사용량, 뒷부분, 항목수); 사용량 += 항목수;
        for (int 안쪽순번 = 0; 안쪽순번 < 개수; 안쪽순번++) hamisha_hali[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        hamisha_hali[사용량++] = '\r'; hamisha_hali[사용량++] = '\n';
    }
}
static void Andaa_a_mikono_muunganisho(int 확장여부) {
    if (수행작업) { jibu("450 Transfer in progress\r\n"); return; }
    Simama_hamisha(); a_mikono_muunganisho = 통신끝점만들기(1);
    if (a_mikono_muunganisho >= 0) 통신주소재사용(a_mikono_muunganisho);
    unsigned namba_ya_kituo = 50000 + 다음접속번호++ % 8;
    if (a_mikono_muunganisho < 0 || 망주소묶기(a_mikono_muunganisho, 망상태읽기(0,0), namba_ya_kituo) || 연결기다리기(a_mikono_muunganisho)) {
        Simama_hamisha(); jibu("425 Cannot open passive listener\r\n"); return;
    }
    char 응답자료[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned 개수 = strlen(앞부분); memcpy(응답자료, 앞부분, 개수);
    if (확장여부) { 수치(namba_ya_kituo, 응답자료, &개수); 응답자료[개수++] = '|'; }
    else {
        uint32_t anwani=망상태읽기(0,0);
        for (int 자리=24;자리>=0;자리-=8) { 수치((anwani>>자리)&255,응답자료,&개수);응답자료[개수++]=','; }
        수치(namba_ya_kituo / 256, 응답자료, &개수); 응답자료[개수++] = ','; 수치(namba_ya_kituo % 256, 응답자료, &개수);
    }
    응답자료[개수++] = ')'; 응답자료[개수++] = '\r'; 응답자료[개수++] = '\n'; 응답자료[개수] = 0; jibu(응답자료);
}
static void amri(void) {
    laini[laini_panga_ukubwa] = 0;
    char *부가인수 = laini; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(laini, "QUIT")) { Simama_hamisha(); jibu("221 Goodbye\r\n"); 끝내기 = 1; return; }
    if (같은지(laini, "NOOP")) { jibu("200 OK\r\n"); return; }
    if (같은지(laini, "SYST")) { jibu("215 UNIX Type: L8\r\n"); return; }
    if (같은지(laini, "FEAT")) { jibu("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(laini, "USER")) { 로그인됨 = 0; mtumiaji_Sawa = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); jibu(mtumiaji_Sawa ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(laini, "PASS")) { 로그인됨 = mtumiaji_Sawa; jibu(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { jibu("530 Login first\r\n"); return; }
    if (같은지(laini, "PWD")) jibu("257 \"/\"\r\n");
    else if (같은지(laini, "CWD")) jibu(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(laini, "TYPE")) jibu(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(laini, "OPTS")) jibu(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(laini, "PASV")) Andaa_a_mikono_muunganisho(0);
    else if (같은지(laini, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) jibu("522 IPv4 only\r\n"); else Andaa_a_mikono_muunganisho(1); }
    else if (같은지(laini, "ABOR")) { Simama_hamisha(); jibu("226 Transfer aborted\r\n"); }
    else if (같은지(laini, "DELE")) { jibu(njia(부가인수) && pk_unlink(faili_ingizo_jina) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(laini, "LIST") || 같은지(laini, "NLST") || 같은지(laini, "MLSD")) {
        if (수행작업) { jibu("450 Transfer in progress\r\n"); return; }
        if (a_mikono_muunganisho < 0 && data < 0) { jibu("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { jibu("550 Root listing only\r\n"); return; }
        tuma_Orodha(같은지(laini,"MLSD") ? 2 : 같은지(laini,"LIST") ? 1 : 0); 수행작업 = 2;
        jibu("150 Opening directory listing\r\n");
    }
    else if (같은지(laini, "SIZE")) {
        if (!njia(부가인수)) { jibu("550 Invalid filename\r\n"); return; }
        int faili_kishiko = pk_open(faili_ingizo_jina, soma_tu_thamani, 0); if (faili_kishiko < 0) { jibu("550 File unavailable\r\n"); return; }
        int panga_ukubwa = pk_size(faili_kishiko); pk_close(faili_kishiko); char 응답자료[32] = "213 "; unsigned 개수 = 4;
        수치(panga_ukubwa, 응답자료, &개수); 응답자료[개수++] = '\r'; 응답자료[개수++] = '\n'; 응답자료[개수] = 0; jibu(응답자료);
    } else if (같은지(laini, "STOR") || 같은지(laini, "RETR")) {
        if (수행작업) { jibu("450 Transfer in progress\r\n"); return; }
        if (a_mikono_muunganisho < 0 && data < 0) { jibu("425 Use PASV or EPSV\r\n"); return; }
        if (!njia(부가인수)) { jibu("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(laini, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(hamisha_jina, faili_ingizo_jina, strlen(faili_ingizo_jina) + 1);
        if (수행작업 == 2) {
            int faili_kishiko = pk_open(faili_ingizo_jina, soma_tu_thamani, 0);
            if (faili_kishiko < 0) { 수행작업 = 0; jibu("550 File unavailable\r\n"); return; }
            int 개수 = pk_read(faili_kishiko, hamisha_hali, sizeof(hamisha_hali)); pk_close(faili_kishiko);
            if (개수 < 0) { 수행작업 = 0; jibu("451 Read failed\r\n"); return; } 사용량 = 개수;
        }
        jibu("150 Opening binary data connection\r\n");
    } else jibu("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (수신창구 < 0) return;
    int Inayoingia_muunganisho = 망연결받기(수신창구);
    if (Inayoingia_muunganisho >= 0) {
        if (udhibiti >= 0) { 통신쓰기(Inayoingia_muunganisho, "421 One session at a time\r\n", 27); funga_Mtandao(Inayoingia_muunganisho); }
        else { udhibiti = Inayoingia_muunganisho; Shughuli = 보드밀리초(); jibu("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (udhibiti < 0) return;
    if ((uint32_t)(보드밀리초() - Shughuli) > 60000) { tenganisha(); return; }
    if (!끝내기) for (unsigned 처리한도 = 0; 처리한도 < 256; 처리한도++) {
        unsigned char msimbo_wa_kibambo; int 반환값 = 통신읽기(udhibiti, &msimbo_wa_kibambo, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { tenganisha(); return; } Shughuli = 보드밀리초();
        if (msimbo_wa_kibambo == '\n') { if (줄오류) jibu("500 Command too long or invalid\r\n"); else amri(); laini_panga_ukubwa = 줄오류 = 0; if (끝내기) break; }
        else if (msimbo_wa_kibambo != '\r') { if (!msimbo_wa_kibambo || laini_panga_ukubwa >= sizeof(laini) - 1) 줄오류 = 1; else laini[laini_panga_ukubwa++] = msimbo_wa_kibambo; }
    }
    if (a_mikono_muunganisho >= 0 && data < 0) {
        int 반환값 = 망연결받기(a_mikono_muunganisho);
        if (반환값 >= 0) {
            if (상대통신주소(반환값) != 상대통신주소(udhibiti)) funga_Mtandao(반환값);
            else { data = 반환값; funga_Mtandao(a_mikono_muunganisho); a_mikono_muunganisho = -1; Shughuli = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && data >= 0) for (unsigned 처리한도 = 0; 처리한도 < 8; 처리한도++) {
        unsigned char data_zuia[512]; int 개수 = 통신읽기(data, data_zuia, sizeof(data_zuia));
        if (개수 == -11) break;
        if (개수 < 0) { Simama_hamisha(); jibu("426 Data connection failed\r\n"); break; }
        Shughuli = 보드밀리초();
        if (개수 == 0) {
            int 결과 = -1;
            if (!실패여부) {
                int faili_kishiko = pk_open(hamisha_jina, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (faili_kishiko >= 0) { 결과 = pk_write(faili_kishiko, hamisha_hali, 사용량); pk_close(faili_kishiko); }
            }
            int 성공여부 = !실패여부 && 결과 == (int)사용량; Simama_hamisha(); jibu(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)개수 > sizeof(hamisha_hali) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(hamisha_hali + 사용량, data_zuia, 개수); 사용량 += 개수; }
    }
    if (수행작업 == 2 && data >= 0) {
        int 개수 = 통신쓰기(data, hamisha_hali + 보낸수, 사용량 - 보낸수);
        if (개수 >= 0) { 보낸수 += 개수; Shughuli = 보드밀리초(); if (보낸수 == 사용량) { Simama_hamisha(); jibu("226 Transfer complete\r\n"); } }
        else if (개수 != -11) { Simama_hamisha(); jibu("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < jibu_panga_ukubwa) {
        int 개수 = 통신쓰기(udhibiti, 응답모음 + 응답전송량, jibu_panga_ukubwa - 응답전송량);
        if (개수 > 0) 응답전송량 += 개수; else if (개수 != -11) { tenganisha(); return; }
    }
    if (응답전송량 == jibu_panga_ukubwa) { jibu_panga_ukubwa = 응답전송량 = 0; if (끝내기) tenganisha(); }
}
