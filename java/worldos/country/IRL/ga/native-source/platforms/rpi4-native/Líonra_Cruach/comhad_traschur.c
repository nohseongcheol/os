#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "Líonra_Cruach.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int 수신창구 = -1, rialú = -1, láimhe_nasc = -1, sonraí = -1;
static unsigned 로그인됨, úsáideoir_OK, líne_socraigh_méid, 줄오류, scoir_clár_55b3a1cd, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned freagair_socraigh_méid, 응답전송량, Ar_aghaidh_uimhir_phoirt;
static uint32_t Gníomhaíocht;
static char Líne[256], 응답모음[2048], comhad_iontráil_ainm[64], traschur_ainm[64];
static unsigned char traschur_staid[16384];
static int 같은지(const char *첫째값, const char *SECOND_VALUE) { while (*첫째값 && *첫째값 == *SECOND_VALUE) { 첫째값++; SECOND_VALUE++; } return *첫째값 == *SECOND_VALUE; }
static void freagair(const char *teaghrán_sonraí) {
    size_t mír_COUNT = strlen(teaghrán_sonraí);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, freagair_socraigh_méid - 응답전송량); freagair_socraigh_méid -= 응답전송량; 응답전송량 = 0; }
    if (mír_COUNT > sizeof(응답모음) - freagair_socraigh_méid) { scoir_clár_55b3a1cd = 1; return; }
    memcpy(응답모음 + freagair_socraigh_méid, teaghrán_sonraí, mír_COUNT); freagair_socraigh_méid += mír_COUNT;
}
static void 수치(unsigned VALUE, char *tomhas_sonraí, unsigned *mír_COUNT) {
    char digit_COUNT[10]; unsigned iontráil_COUNT = 0;
    do { digit_COUNT[iontráil_COUNT++] = '0' + VALUE % 10; VALUE /= 10; } while (VALUE);
    while (iontráil_COUNT) tomhas_sonraí[(*mír_COUNT)++] = digit_COUNT[--iontráil_COUNT];
}
static void stop_traschur(void) {
    if (sonraí >= 0) dún_Líonra(sonraí); if (láimhe_nasc >= 0) dún_Líonra(láimhe_nasc);
    sonraí = láimhe_nasc = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void dínasc(void) {
    stop_traschur(); if (rialú >= 0) dún_Líonra(rialú); rialú = -1;
    로그인됨 = úsáideoir_OK = líne_socraigh_méid = 줄오류 = freagair_socraigh_méid = 응답전송량 = scoir_clár_55b3a1cd = 0;
}
int comhad_traschur_rialú(int Gníomh) {
    if (Gníomh == 2) return 수신창구 >= 0;
    if (Gníomh == 0) { dínasc(); if (수신창구 >= 0) dún_Líonra(수신창구); 수신창구 = -1; return 0; }
    if (Gníomh != 1) return -22; if (수신창구 >= 0) return 0;
    수신창구 = 통신끝점만들기(1); if (수신창구 < 0) return 수신창구;
    int 반환값 = 망주소묶기(수신창구, 망상태읽기(0,0), 21); if (!반환값) 반환값 = 연결기다리기(수신창구);
    if (반환값 < 0) { dún_Líonra(수신창구); 수신창구 = -1; } return 반환값;
}
static int CONAIR(const char *Ainm) {
    unsigned mír_COUNT = 0; if (*Ainm == '/') Ainm++;
    if (!*Ainm || 같은지(Ainm, ".") || 같은지(Ainm, "..")) return 0;
    comhad_iontráil_ainm[mír_COUNT++] = '/';
    while (*Ainm) {
        unsigned char pointe_cóid = *Ainm++;
        if (mír_COUNT >= 63 || pointe_cóid < 32 || pointe_cóid == 127 || pointe_cóid == '/' || pointe_cóid == '\\') return 0;
        comhad_iontráil_ainm[mír_COUNT++] = pointe_cóid;
    }
    comhad_iontráil_ainm[mír_COUNT] = 0; return 1;
}
static void seol_Liosta(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int mír_COUNT = 자바파일항목길이(순번); if (mír_COUNT <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned iontráil_COUNT = strlen(앞부분); memcpy(traschur_staid + 사용량, 앞부분, iontráil_COUNT); 사용량 += iontráil_COUNT;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)traschur_staid, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        iontráil_COUNT = strlen(뒷부분); memcpy(traschur_staid + 사용량, 뒷부분, iontráil_COUNT); 사용량 += iontráil_COUNT;
        for (int 안쪽순번 = 0; 안쪽순번 < mír_COUNT; 안쪽순번++) traschur_staid[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        traschur_staid[사용량++] = '\r'; traschur_staid[사용량++] = '\n';
    }
}
static void Ullmhaigh_láimhe_nasc(int 확장여부) {
    if (수행작업) { freagair("450 Transfer in progress\r\n"); return; }
    stop_traschur(); láimhe_nasc = 통신끝점만들기(1);
    if (láimhe_nasc >= 0) 통신주소재사용(láimhe_nasc);
    unsigned uimhir_phoirt = 50000 + Ar_aghaidh_uimhir_phoirt++ % 8;
    if (láimhe_nasc < 0 || 망주소묶기(láimhe_nasc, 망상태읽기(0,0), uimhir_phoirt) || 연결기다리기(láimhe_nasc)) {
        stop_traschur(); freagair("425 Cannot open passive listener\r\n"); return;
    }
    char 응답자료[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned mír_COUNT = strlen(앞부분); memcpy(응답자료, 앞부분, mír_COUNT);
    if (확장여부) { 수치(uimhir_phoirt, 응답자료, &mír_COUNT); 응답자료[mír_COUNT++] = '|'; }
    else {
        uint32_t ADDRESS=망상태읽기(0,0);
        for (int suíomh_INDEX=24;suíomh_INDEX>=0;suíomh_INDEX-=8) { 수치((ADDRESS>>suíomh_INDEX)&255,응답자료,&mír_COUNT);응답자료[mír_COUNT++]=','; }
        수치(uimhir_phoirt / 256, 응답자료, &mír_COUNT); 응답자료[mír_COUNT++] = ','; 수치(uimhir_phoirt % 256, 응답자료, &mír_COUNT);
    }
    응답자료[mír_COUNT++] = ')'; 응답자료[mír_COUNT++] = '\r'; 응답자료[mír_COUNT++] = '\n'; 응답자료[mír_COUNT] = 0; freagair(응답자료);
}
static void Ordú(void) {
    Líne[líne_socraigh_méid] = 0;
    char *부가인수 = Líne; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(Líne, "QUIT")) { stop_traschur(); freagair("221 Goodbye\r\n"); scoir_clár_55b3a1cd = 1; return; }
    if (같은지(Líne, "NOOP")) { freagair("200 OK\r\n"); return; }
    if (같은지(Líne, "SYST")) { freagair("215 UNIX Type: L8\r\n"); return; }
    if (같은지(Líne, "FEAT")) { freagair("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(Líne, "USER")) { 로그인됨 = 0; úsáideoir_OK = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); freagair(úsáideoir_OK ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(Líne, "PASS")) { 로그인됨 = úsáideoir_OK; freagair(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { freagair("530 Login first\r\n"); return; }
    if (같은지(Líne, "PWD")) freagair("257 \"/\"\r\n");
    else if (같은지(Líne, "CWD")) freagair(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(Líne, "TYPE")) freagair(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(Líne, "OPTS")) freagair(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(Líne, "PASV")) Ullmhaigh_láimhe_nasc(0);
    else if (같은지(Líne, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) freagair("522 IPv4 only\r\n"); else Ullmhaigh_láimhe_nasc(1); }
    else if (같은지(Líne, "ABOR")) { stop_traschur(); freagair("226 Transfer aborted\r\n"); }
    else if (같은지(Líne, "DELE")) { freagair(CONAIR(부가인수) && pk_unlink(comhad_iontráil_ainm) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(Líne, "LIST") || 같은지(Líne, "NLST") || 같은지(Líne, "MLSD")) {
        if (수행작업) { freagair("450 Transfer in progress\r\n"); return; }
        if (láimhe_nasc < 0 && sonraí < 0) { freagair("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { freagair("550 Root listing only\r\n"); return; }
        seol_Liosta(같은지(Líne,"MLSD") ? 2 : 같은지(Líne,"LIST") ? 1 : 0); 수행작업 = 2;
        freagair("150 Opening directory listing\r\n");
    }
    else if (같은지(Líne, "SIZE")) {
        if (!CONAIR(부가인수)) { freagair("550 Invalid filename\r\n"); return; }
        int comhad_hanla = pk_open(comhad_iontráil_ainm, inléite_amháin_VALUE, 0); if (comhad_hanla < 0) { freagair("550 File unavailable\r\n"); return; }
        int Méid = pk_size(comhad_hanla); pk_close(comhad_hanla); char 응답자료[32] = "213 "; unsigned mír_COUNT = 4;
        수치(Méid, 응답자료, &mír_COUNT); 응답자료[mír_COUNT++] = '\r'; 응답자료[mír_COUNT++] = '\n'; 응답자료[mír_COUNT] = 0; freagair(응답자료);
    } else if (같은지(Líne, "STOR") || 같은지(Líne, "RETR")) {
        if (수행작업) { freagair("450 Transfer in progress\r\n"); return; }
        if (láimhe_nasc < 0 && sonraí < 0) { freagair("425 Use PASV or EPSV\r\n"); return; }
        if (!CONAIR(부가인수)) { freagair("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(Líne, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(traschur_ainm, comhad_iontráil_ainm, strlen(comhad_iontráil_ainm) + 1);
        if (수행작업 == 2) {
            int comhad_hanla = pk_open(comhad_iontráil_ainm, inléite_amháin_VALUE, 0);
            if (comhad_hanla < 0) { 수행작업 = 0; freagair("550 File unavailable\r\n"); return; }
            int mír_COUNT = pk_read(comhad_hanla, traschur_staid, sizeof(traschur_staid)); pk_close(comhad_hanla);
            if (mír_COUNT < 0) { 수행작업 = 0; freagair("451 Read failed\r\n"); return; } 사용량 = mír_COUNT;
        }
        freagair("150 Opening binary data connection\r\n");
    } else freagair("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (수신창구 < 0) return;
    int 들어온연결 = 망연결받기(수신창구);
    if (들어온연결 >= 0) {
        if (rialú >= 0) { 통신쓰기(들어온연결, "421 One session at a time\r\n", 27); dún_Líonra(들어온연결); }
        else { rialú = 들어온연결; Gníomhaíocht = 보드밀리초(); freagair("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (rialú < 0) return;
    if ((uint32_t)(보드밀리초() - Gníomhaíocht) > 60000) { dínasc(); return; }
    if (!scoir_clár_55b3a1cd) for (unsigned 처리한도 = 0; 처리한도 < 256; 처리한도++) {
        unsigned char pointe_cóid; int 반환값 = 통신읽기(rialú, &pointe_cóid, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { dínasc(); return; } Gníomhaíocht = 보드밀리초();
        if (pointe_cóid == '\n') { if (줄오류) freagair("500 Command too long or invalid\r\n"); else Ordú(); líne_socraigh_méid = 줄오류 = 0; if (scoir_clár_55b3a1cd) break; }
        else if (pointe_cóid != '\r') { if (!pointe_cóid || líne_socraigh_méid >= sizeof(Líne) - 1) 줄오류 = 1; else Líne[líne_socraigh_méid++] = pointe_cóid; }
    }
    if (láimhe_nasc >= 0 && sonraí < 0) {
        int 반환값 = 망연결받기(láimhe_nasc);
        if (반환값 >= 0) {
            if (상대통신주소(반환값) != 상대통신주소(rialú)) dún_Líonra(반환값);
            else { sonraí = 반환값; dún_Líonra(láimhe_nasc); láimhe_nasc = -1; Gníomhaíocht = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && sonraí >= 0) for (unsigned 처리한도 = 0; 처리한도 < 8; 처리한도++) {
        unsigned char sonraí_bac[512]; int mír_COUNT = 통신읽기(sonraí, sonraí_bac, sizeof(sonraí_bac));
        if (mír_COUNT == -11) break;
        if (mír_COUNT < 0) { stop_traschur(); freagair("426 Data connection failed\r\n"); break; }
        Gníomhaíocht = 보드밀리초();
        if (mír_COUNT == 0) {
            int tomhas = -1;
            if (!실패여부) {
                int comhad_hanla = pk_open(traschur_ainm, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (comhad_hanla >= 0) { tomhas = pk_write(comhad_hanla, traschur_staid, 사용량); pk_close(comhad_hanla); }
            }
            int 성공여부 = !실패여부 && tomhas == (int)사용량; stop_traschur(); freagair(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)mír_COUNT > sizeof(traschur_staid) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(traschur_staid + 사용량, sonraí_bac, mír_COUNT); 사용량 += mír_COUNT; }
    }
    if (수행작업 == 2 && sonraí >= 0) {
        int mír_COUNT = 통신쓰기(sonraí, traschur_staid + 보낸수, 사용량 - 보낸수);
        if (mír_COUNT >= 0) { 보낸수 += mír_COUNT; Gníomhaíocht = 보드밀리초(); if (보낸수 == 사용량) { stop_traschur(); freagair("226 Transfer complete\r\n"); } }
        else if (mír_COUNT != -11) { stop_traschur(); freagair("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < freagair_socraigh_méid) {
        int mír_COUNT = 통신쓰기(rialú, 응답모음 + 응답전송량, freagair_socraigh_méid - 응답전송량);
        if (mír_COUNT > 0) 응답전송량 += mír_COUNT; else if (mír_COUNT != -11) { dínasc(); return; }
    }
    if (응답전송량 == freagair_socraigh_méid) { freagair_socraigh_méid = 응답전송량 = 0; if (scoir_clár_55b3a1cd) dínasc(); }
}
