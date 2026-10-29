#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "Netweke_kgoboko.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int 수신창구 = -1, taolo = -1, menyuale_kgokaganya = -1, data = -1;
static unsigned 로그인됨, 사용자확인, mothaladi_bogolo, 줄오류, 끝내기, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned fetola_bogolo, 응답전송량, 다음접속번호;
static uint32_t Modiro;
static char mothaladi[256], 응답모음[2048], faele_go_tsenya_tshedimošo_leina[64], fetišetša_leina[64];
static unsigned char fetišetša_boemo[16384];
static int 같은지(const char *첫째값, const char *둘째값) { while (*첫째값 && *첫째값 == *둘째값) { 첫째값++; 둘째값++; } return *첫째값 == *둘째값; }
static void fetola(const char *molokoloko_data) {
    size_t 개수 = strlen(molokoloko_data);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, fetola_bogolo - 응답전송량); fetola_bogolo -= 응답전송량; 응답전송량 = 0; }
    if (개수 > sizeof(응답모음) - fetola_bogolo) { 끝내기 = 1; return; }
    memcpy(응답모음 + fetola_bogolo, molokoloko_data, 개수); fetola_bogolo += 개수;
}
static void 수치(unsigned boleng, char *결과자료, unsigned *개수) {
    char 숫자수[10]; unsigned 항목수 = 0;
    do { 숫자수[항목수++] = '0' + boleng % 10; boleng /= 10; } while (boleng);
    while (항목수) 결과자료[(*개수)++] = 숫자수[--항목수];
}
static void Ema_fetišetša(void) {
    if (data >= 0) tswalela_Netweke(data); if (menyuale_kgokaganya >= 0) tswalela_Netweke(menyuale_kgokaganya);
    data = menyuale_kgokaganya = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void aroganya(void) {
    Ema_fetišetša(); if (taolo >= 0) tswalela_Netweke(taolo); taolo = -1;
    로그인됨 = 사용자확인 = mothaladi_bogolo = 줄오류 = fetola_bogolo = 응답전송량 = 끝내기 = 0;
}
int faele_fetišetša_taolo(int Mogato) {
    if (Mogato == 2) return 수신창구 >= 0;
    if (Mogato == 0) { aroganya(); if (수신창구 >= 0) tswalela_Netweke(수신창구); 수신창구 = -1; return 0; }
    if (Mogato != 1) return -22; if (수신창구 >= 0) return 0;
    수신창구 = 통신끝점만들기(1); if (수신창구 < 0) return 수신창구;
    int 반환값 = 망주소묶기(수신창구, 망상태읽기(0,0), 21); if (!반환값) 반환값 = 연결기다리기(수신창구);
    if (반환값 < 0) { tswalela_Netweke(수신창구); 수신창구 = -1; } return 반환값;
}
static int Tsejana(const char *Leina) {
    unsigned 개수 = 0; if (*Leina == '/') Leina++;
    if (!*Leina || 같은지(Leina, ".") || 같은지(Leina, "..")) return 0;
    faele_go_tsenya_tshedimošo_leina[개수++] = '/';
    while (*Leina) {
        unsigned char khouto_ya_tlhaka = *Leina++;
        if (개수 >= 63 || khouto_ya_tlhaka < 32 || khouto_ya_tlhaka == 127 || khouto_ya_tlhaka == '/' || khouto_ya_tlhaka == '\\') return 0;
        faele_go_tsenya_tshedimošo_leina[개수++] = khouto_ya_tlhaka;
    }
    faele_go_tsenya_tshedimošo_leina[개수] = 0; return 1;
}
static void Romela_Lenaneo(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int 개수 = 자바파일항목길이(순번); if (개수 <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned 항목수 = strlen(앞부분); memcpy(fetišetša_boemo + 사용량, 앞부분, 항목수); 사용량 += 항목수;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)fetišetša_boemo, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        항목수 = strlen(뒷부분); memcpy(fetišetša_boemo + 사용량, 뒷부분, 항목수); 사용량 += 항목수;
        for (int 안쪽순번 = 0; 안쪽순번 < 개수; 안쪽순번++) fetišetša_boemo[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        fetišetša_boemo[사용량++] = '\r'; fetišetša_boemo[사용량++] = '\n';
    }
}
static void Lokišetša_menyuale_kgokaganya(int 확장여부) {
    if (수행작업) { fetola("450 Transfer in progress\r\n"); return; }
    Ema_fetišetša(); menyuale_kgokaganya = 통신끝점만들기(1);
    if (menyuale_kgokaganya >= 0) 통신주소재사용(menyuale_kgokaganya);
    unsigned 접속번호 = 50000 + 다음접속번호++ % 8;
    if (menyuale_kgokaganya < 0 || 망주소묶기(menyuale_kgokaganya, 망상태읽기(0,0), 접속번호) || 연결기다리기(menyuale_kgokaganya)) {
        Ema_fetišetša(); fetola("425 Cannot open passive listener\r\n"); return;
    }
    char 응답자료[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned 개수 = strlen(앞부분); memcpy(응답자료, 앞부분, 개수);
    if (확장여부) { 수치(접속번호, 응답자료, &개수); 응답자료[개수++] = '|'; }
    else {
        uint32_t atrese=망상태읽기(0,0);
        for (int 자리=24;자리>=0;자리-=8) { 수치((atrese>>자리)&255,응답자료,&개수);응답자료[개수++]=','; }
        수치(접속번호 / 256, 응답자료, &개수); 응답자료[개수++] = ','; 수치(접속번호 % 256, 응답자료, &개수);
    }
    응답자료[개수++] = ')'; 응답자료[개수++] = '\r'; 응답자료[개수++] = '\n'; 응답자료[개수] = 0; fetola(응답자료);
}
static void Taelo(void) {
    mothaladi[mothaladi_bogolo] = 0;
    char *부가인수 = mothaladi; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(mothaladi, "QUIT")) { Ema_fetišetša(); fetola("221 Goodbye\r\n"); 끝내기 = 1; return; }
    if (같은지(mothaladi, "NOOP")) { fetola("200 OK\r\n"); return; }
    if (같은지(mothaladi, "SYST")) { fetola("215 UNIX Type: L8\r\n"); return; }
    if (같은지(mothaladi, "FEAT")) { fetola("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(mothaladi, "USER")) { 로그인됨 = 0; 사용자확인 = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); fetola(사용자확인 ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(mothaladi, "PASS")) { 로그인됨 = 사용자확인; fetola(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { fetola("530 Login first\r\n"); return; }
    if (같은지(mothaladi, "PWD")) fetola("257 \"/\"\r\n");
    else if (같은지(mothaladi, "CWD")) fetola(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(mothaladi, "TYPE")) fetola(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(mothaladi, "OPTS")) fetola(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(mothaladi, "PASV")) Lokišetša_menyuale_kgokaganya(0);
    else if (같은지(mothaladi, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) fetola("522 IPv4 only\r\n"); else Lokišetša_menyuale_kgokaganya(1); }
    else if (같은지(mothaladi, "ABOR")) { Ema_fetišetša(); fetola("226 Transfer aborted\r\n"); }
    else if (같은지(mothaladi, "DELE")) { fetola(Tsejana(부가인수) && pk_unlink(faele_go_tsenya_tshedimošo_leina) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(mothaladi, "LIST") || 같은지(mothaladi, "NLST") || 같은지(mothaladi, "MLSD")) {
        if (수행작업) { fetola("450 Transfer in progress\r\n"); return; }
        if (menyuale_kgokaganya < 0 && data < 0) { fetola("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { fetola("550 Root listing only\r\n"); return; }
        Romela_Lenaneo(같은지(mothaladi,"MLSD") ? 2 : 같은지(mothaladi,"LIST") ? 1 : 0); 수행작업 = 2;
        fetola("150 Opening directory listing\r\n");
    }
    else if (같은지(mothaladi, "SIZE")) {
        if (!Tsejana(부가인수)) { fetola("550 Invalid filename\r\n"); return; }
        int faele_tshwaro = pk_open(faele_go_tsenya_tshedimošo_leina, balwago_fela_boleng, 0); if (faele_tshwaro < 0) { fetola("550 File unavailable\r\n"); return; }
        int Bogolo = pk_size(faele_tshwaro); pk_close(faele_tshwaro); char 응답자료[32] = "213 "; unsigned 개수 = 4;
        수치(Bogolo, 응답자료, &개수); 응답자료[개수++] = '\r'; 응답자료[개수++] = '\n'; 응답자료[개수] = 0; fetola(응답자료);
    } else if (같은지(mothaladi, "STOR") || 같은지(mothaladi, "RETR")) {
        if (수행작업) { fetola("450 Transfer in progress\r\n"); return; }
        if (menyuale_kgokaganya < 0 && data < 0) { fetola("425 Use PASV or EPSV\r\n"); return; }
        if (!Tsejana(부가인수)) { fetola("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(mothaladi, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(fetišetša_leina, faele_go_tsenya_tshedimošo_leina, strlen(faele_go_tsenya_tshedimošo_leina) + 1);
        if (수행작업 == 2) {
            int faele_tshwaro = pk_open(faele_go_tsenya_tshedimošo_leina, balwago_fela_boleng, 0);
            if (faele_tshwaro < 0) { 수행작업 = 0; fetola("550 File unavailable\r\n"); return; }
            int 개수 = pk_read(faele_tshwaro, fetišetša_boemo, sizeof(fetišetša_boemo)); pk_close(faele_tshwaro);
            if (개수 < 0) { 수행작업 = 0; fetola("451 Read failed\r\n"); return; } 사용량 = 개수;
        }
        fetola("150 Opening binary data connection\r\n");
    } else fetola("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (수신창구 < 0) return;
    int 들어온연결 = 망연결받기(수신창구);
    if (들어온연결 >= 0) {
        if (taolo >= 0) { 통신쓰기(들어온연결, "421 One session at a time\r\n", 27); tswalela_Netweke(들어온연결); }
        else { taolo = 들어온연결; Modiro = 보드밀리초(); fetola("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (taolo < 0) return;
    if ((uint32_t)(보드밀리초() - Modiro) > 60000) { aroganya(); return; }
    if (!끝내기) for (unsigned 처리한도 = 0; 처리한도 < 256; 처리한도++) {
        unsigned char khouto_ya_tlhaka; int 반환값 = 통신읽기(taolo, &khouto_ya_tlhaka, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { aroganya(); return; } Modiro = 보드밀리초();
        if (khouto_ya_tlhaka == '\n') { if (줄오류) fetola("500 Command too long or invalid\r\n"); else Taelo(); mothaladi_bogolo = 줄오류 = 0; if (끝내기) break; }
        else if (khouto_ya_tlhaka != '\r') { if (!khouto_ya_tlhaka || mothaladi_bogolo >= sizeof(mothaladi) - 1) 줄오류 = 1; else mothaladi[mothaladi_bogolo++] = khouto_ya_tlhaka; }
    }
    if (menyuale_kgokaganya >= 0 && data < 0) {
        int 반환값 = 망연결받기(menyuale_kgokaganya);
        if (반환값 >= 0) {
            if (상대통신주소(반환값) != 상대통신주소(taolo)) tswalela_Netweke(반환값);
            else { data = 반환값; tswalela_Netweke(menyuale_kgokaganya); menyuale_kgokaganya = -1; Modiro = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && data >= 0) for (unsigned 처리한도 = 0; 처리한도 < 8; 처리한도++) {
        unsigned char data_thibela[512]; int 개수 = 통신읽기(data, data_thibela, sizeof(data_thibela));
        if (개수 == -11) break;
        if (개수 < 0) { Ema_fetišetša(); fetola("426 Data connection failed\r\n"); break; }
        Modiro = 보드밀리초();
        if (개수 == 0) {
            int 결과 = -1;
            if (!실패여부) {
                int faele_tshwaro = pk_open(fetišetša_leina, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (faele_tshwaro >= 0) { 결과 = pk_write(faele_tshwaro, fetišetša_boemo, 사용량); pk_close(faele_tshwaro); }
            }
            int 성공여부 = !실패여부 && 결과 == (int)사용량; Ema_fetišetša(); fetola(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)개수 > sizeof(fetišetša_boemo) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(fetišetša_boemo + 사용량, data_thibela, 개수); 사용량 += 개수; }
    }
    if (수행작업 == 2 && data >= 0) {
        int 개수 = 통신쓰기(data, fetišetša_boemo + 보낸수, 사용량 - 보낸수);
        if (개수 >= 0) { 보낸수 += 개수; Modiro = 보드밀리초(); if (보낸수 == 사용량) { Ema_fetišetša(); fetola("226 Transfer complete\r\n"); } }
        else if (개수 != -11) { Ema_fetišetša(); fetola("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < fetola_bogolo) {
        int 개수 = 통신쓰기(taolo, 응답모음 + 응답전송량, fetola_bogolo - 응답전송량);
        if (개수 > 0) 응답전송량 += 개수; else if (개수 != -11) { aroganya(); return; }
    }
    if (응답전송량 == fetola_bogolo) { fetola_bogolo = 응답전송량 = 0; if (끝내기) aroganya(); }
}
