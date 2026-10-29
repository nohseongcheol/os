#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "lìonra_stac.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int 수신창구 = -1, smachd = -1, de_làimh_ceangal = -1, dàta = -1;
static unsigned 로그인됨, cleachdaiche_Ceart_ma_thà, loidhne_atharraich_am_meud, 줄오류, fàg_an_seo_ap, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned freagair_atharraich_am_meud, 응답전송량, 다음접속번호;
static uint32_t gnìomhachd;
static char loidhne[256], 응답모음[2048], faidhle_cur_a_steach_ainm[64], tar_chur_ainm[64];
static unsigned char tar_chur_cor[16384];
static int 같은지(const char *첫째값, const char *SECOND_VALUE) { while (*첫째값 && *첫째값 == *SECOND_VALUE) { 첫째값++; SECOND_VALUE++; } return *첫째값 == *SECOND_VALUE; }
static void freagair(const char *sreang_dàta) {
    size_t nì_COUNT = strlen(sreang_dàta);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, freagair_atharraich_am_meud - 응답전송량); freagair_atharraich_am_meud -= 응답전송량; 응답전송량 = 0; }
    if (nì_COUNT > sizeof(응답모음) - freagair_atharraich_am_meud) { fàg_an_seo_ap = 1; return; }
    memcpy(응답모음 + freagair_atharraich_am_meud, sreang_dàta, nì_COUNT); freagair_atharraich_am_meud += nì_COUNT;
}
static void 수치(unsigned VALUE, char *tomhas_dàta, unsigned *nì_COUNT) {
    char figear_COUNT[10]; unsigned cur_a_steach_COUNT = 0;
    do { figear_COUNT[cur_a_steach_COUNT++] = '0' + VALUE % 10; VALUE /= 10; } while (VALUE);
    while (cur_a_steach_COUNT) tomhas_dàta[(*nì_COUNT)++] = figear_COUNT[--cur_a_steach_COUNT];
}
static void Stad_tar_chur(void) {
    if (dàta >= 0) dùin_lìonra(dàta); if (de_làimh_ceangal >= 0) dùin_lìonra(de_làimh_ceangal);
    dàta = de_làimh_ceangal = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void dì_cheangail(void) {
    Stad_tar_chur(); if (smachd >= 0) dùin_lìonra(smachd); smachd = -1;
    로그인됨 = cleachdaiche_Ceart_ma_thà = loidhne_atharraich_am_meud = 줄오류 = freagair_atharraich_am_meud = 응답전송량 = fàg_an_seo_ap = 0;
}
int faidhle_tar_chur_smachd(int Gnìomh) {
    if (Gnìomh == 2) return 수신창구 >= 0;
    if (Gnìomh == 0) { dì_cheangail(); if (수신창구 >= 0) dùin_lìonra(수신창구); 수신창구 = -1; return 0; }
    if (Gnìomh != 1) return -22; if (수신창구 >= 0) return 0;
    수신창구 = 통신끝점만들기(1); if (수신창구 < 0) return 수신창구;
    int 반환값 = 망주소묶기(수신창구, 망상태읽기(0,0), 21); if (!반환값) 반환값 = 연결기다리기(수신창구);
    if (반환값 < 0) { dùin_lìonra(수신창구); 수신창구 = -1; } return 반환값;
}
static int Slighe(const char *Ainm) {
    unsigned nì_COUNT = 0; if (*Ainm == '/') Ainm++;
    if (!*Ainm || 같은지(Ainm, ".") || 같은지(Ainm, "..")) return 0;
    faidhle_cur_a_steach_ainm[nì_COUNT++] = '/';
    while (*Ainm) {
        unsigned char còd_a_charactair = *Ainm++;
        if (nì_COUNT >= 63 || còd_a_charactair < 32 || còd_a_charactair == 127 || còd_a_charactair == '/' || còd_a_charactair == '\\') return 0;
        faidhle_cur_a_steach_ainm[nì_COUNT++] = còd_a_charactair;
    }
    faidhle_cur_a_steach_ainm[nì_COUNT] = 0; return 1;
}
static void cuir_Liosta(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int nì_COUNT = 자바파일항목길이(순번); if (nì_COUNT <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned cur_a_steach_COUNT = strlen(앞부분); memcpy(tar_chur_cor + 사용량, 앞부분, cur_a_steach_COUNT); 사용량 += cur_a_steach_COUNT;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)tar_chur_cor, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        cur_a_steach_COUNT = strlen(뒷부분); memcpy(tar_chur_cor + 사용량, 뒷부분, cur_a_steach_COUNT); 사용량 += cur_a_steach_COUNT;
        for (int 안쪽순번 = 0; 안쪽순번 < nì_COUNT; 안쪽순번++) tar_chur_cor[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        tar_chur_cor[사용량++] = '\r'; tar_chur_cor[사용량++] = '\n';
    }
}
static void Ullaich_de_làimh_ceangal(int 확장여부) {
    if (수행작업) { freagair("450 Transfer in progress\r\n"); return; }
    Stad_tar_chur(); de_làimh_ceangal = 통신끝점만들기(1);
    if (de_làimh_ceangal >= 0) 통신주소재사용(de_làimh_ceangal);
    unsigned 접속번호 = 50000 + 다음접속번호++ % 8;
    if (de_làimh_ceangal < 0 || 망주소묶기(de_làimh_ceangal, 망상태읽기(0,0), 접속번호) || 연결기다리기(de_làimh_ceangal)) {
        Stad_tar_chur(); freagair("425 Cannot open passive listener\r\n"); return;
    }
    char 응답자료[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned nì_COUNT = strlen(앞부분); memcpy(응답자료, 앞부분, nì_COUNT);
    if (확장여부) { 수치(접속번호, 응답자료, &nì_COUNT); 응답자료[nì_COUNT++] = '|'; }
    else {
        uint32_t ADDRESS=망상태읽기(0,0);
        for (int suidhich_INDEX=24;suidhich_INDEX>=0;suidhich_INDEX-=8) { 수치((ADDRESS>>suidhich_INDEX)&255,응답자료,&nì_COUNT);응답자료[nì_COUNT++]=','; }
        수치(접속번호 / 256, 응답자료, &nì_COUNT); 응답자료[nì_COUNT++] = ','; 수치(접속번호 % 256, 응답자료, &nì_COUNT);
    }
    응답자료[nì_COUNT++] = ')'; 응답자료[nì_COUNT++] = '\r'; 응답자료[nì_COUNT++] = '\n'; 응답자료[nì_COUNT] = 0; freagair(응답자료);
}
static void àithne(void) {
    loidhne[loidhne_atharraich_am_meud] = 0;
    char *부가인수 = loidhne; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(loidhne, "QUIT")) { Stad_tar_chur(); freagair("221 Goodbye\r\n"); fàg_an_seo_ap = 1; return; }
    if (같은지(loidhne, "NOOP")) { freagair("200 OK\r\n"); return; }
    if (같은지(loidhne, "SYST")) { freagair("215 UNIX Type: L8\r\n"); return; }
    if (같은지(loidhne, "FEAT")) { freagair("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(loidhne, "USER")) { 로그인됨 = 0; cleachdaiche_Ceart_ma_thà = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); freagair(cleachdaiche_Ceart_ma_thà ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(loidhne, "PASS")) { 로그인됨 = cleachdaiche_Ceart_ma_thà; freagair(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { freagair("530 Login first\r\n"); return; }
    if (같은지(loidhne, "PWD")) freagair("257 \"/\"\r\n");
    else if (같은지(loidhne, "CWD")) freagair(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(loidhne, "TYPE")) freagair(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(loidhne, "OPTS")) freagair(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(loidhne, "PASV")) Ullaich_de_làimh_ceangal(0);
    else if (같은지(loidhne, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) freagair("522 IPv4 only\r\n"); else Ullaich_de_làimh_ceangal(1); }
    else if (같은지(loidhne, "ABOR")) { Stad_tar_chur(); freagair("226 Transfer aborted\r\n"); }
    else if (같은지(loidhne, "DELE")) { freagair(Slighe(부가인수) && pk_unlink(faidhle_cur_a_steach_ainm) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(loidhne, "LIST") || 같은지(loidhne, "NLST") || 같은지(loidhne, "MLSD")) {
        if (수행작업) { freagair("450 Transfer in progress\r\n"); return; }
        if (de_làimh_ceangal < 0 && dàta < 0) { freagair("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { freagair("550 Root listing only\r\n"); return; }
        cuir_Liosta(같은지(loidhne,"MLSD") ? 2 : 같은지(loidhne,"LIST") ? 1 : 0); 수행작업 = 2;
        freagair("150 Opening directory listing\r\n");
    }
    else if (같은지(loidhne, "SIZE")) {
        if (!Slighe(부가인수)) { freagair("550 Invalid filename\r\n"); return; }
        int faidhle_làmhrachan = pk_open(faidhle_cur_a_steach_ainm, ri_leughadh_a_mhàin_VALUE, 0); if (faidhle_làmhrachan < 0) { freagair("550 File unavailable\r\n"); return; }
        int atharraich_am_meud = pk_size(faidhle_làmhrachan); pk_close(faidhle_làmhrachan); char 응답자료[32] = "213 "; unsigned nì_COUNT = 4;
        수치(atharraich_am_meud, 응답자료, &nì_COUNT); 응답자료[nì_COUNT++] = '\r'; 응답자료[nì_COUNT++] = '\n'; 응답자료[nì_COUNT] = 0; freagair(응답자료);
    } else if (같은지(loidhne, "STOR") || 같은지(loidhne, "RETR")) {
        if (수행작업) { freagair("450 Transfer in progress\r\n"); return; }
        if (de_làimh_ceangal < 0 && dàta < 0) { freagair("425 Use PASV or EPSV\r\n"); return; }
        if (!Slighe(부가인수)) { freagair("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(loidhne, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(tar_chur_ainm, faidhle_cur_a_steach_ainm, strlen(faidhle_cur_a_steach_ainm) + 1);
        if (수행작업 == 2) {
            int faidhle_làmhrachan = pk_open(faidhle_cur_a_steach_ainm, ri_leughadh_a_mhàin_VALUE, 0);
            if (faidhle_làmhrachan < 0) { 수행작업 = 0; freagair("550 File unavailable\r\n"); return; }
            int nì_COUNT = pk_read(faidhle_làmhrachan, tar_chur_cor, sizeof(tar_chur_cor)); pk_close(faidhle_làmhrachan);
            if (nì_COUNT < 0) { 수행작업 = 0; freagair("451 Read failed\r\n"); return; } 사용량 = nì_COUNT;
        }
        freagair("150 Opening binary data connection\r\n");
    } else freagair("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (수신창구 < 0) return;
    int 들어온연결 = 망연결받기(수신창구);
    if (들어온연결 >= 0) {
        if (smachd >= 0) { 통신쓰기(들어온연결, "421 One session at a time\r\n", 27); dùin_lìonra(들어온연결); }
        else { smachd = 들어온연결; gnìomhachd = 보드밀리초(); freagair("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (smachd < 0) return;
    if ((uint32_t)(보드밀리초() - gnìomhachd) > 60000) { dì_cheangail(); return; }
    if (!fàg_an_seo_ap) for (unsigned 처리한도 = 0; 처리한도 < 256; 처리한도++) {
        unsigned char còd_a_charactair; int 반환값 = 통신읽기(smachd, &còd_a_charactair, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { dì_cheangail(); return; } gnìomhachd = 보드밀리초();
        if (còd_a_charactair == '\n') { if (줄오류) freagair("500 Command too long or invalid\r\n"); else àithne(); loidhne_atharraich_am_meud = 줄오류 = 0; if (fàg_an_seo_ap) break; }
        else if (còd_a_charactair != '\r') { if (!còd_a_charactair || loidhne_atharraich_am_meud >= sizeof(loidhne) - 1) 줄오류 = 1; else loidhne[loidhne_atharraich_am_meud++] = còd_a_charactair; }
    }
    if (de_làimh_ceangal >= 0 && dàta < 0) {
        int 반환값 = 망연결받기(de_làimh_ceangal);
        if (반환값 >= 0) {
            if (상대통신주소(반환값) != 상대통신주소(smachd)) dùin_lìonra(반환값);
            else { dàta = 반환값; dùin_lìonra(de_làimh_ceangal); de_làimh_ceangal = -1; gnìomhachd = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && dàta >= 0) for (unsigned 처리한도 = 0; 처리한도 < 8; 처리한도++) {
        unsigned char dàta_bac[512]; int nì_COUNT = 통신읽기(dàta, dàta_bac, sizeof(dàta_bac));
        if (nì_COUNT == -11) break;
        if (nì_COUNT < 0) { Stad_tar_chur(); freagair("426 Data connection failed\r\n"); break; }
        gnìomhachd = 보드밀리초();
        if (nì_COUNT == 0) {
            int tomhas = -1;
            if (!실패여부) {
                int faidhle_làmhrachan = pk_open(tar_chur_ainm, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (faidhle_làmhrachan >= 0) { tomhas = pk_write(faidhle_làmhrachan, tar_chur_cor, 사용량); pk_close(faidhle_làmhrachan); }
            }
            int 성공여부 = !실패여부 && tomhas == (int)사용량; Stad_tar_chur(); freagair(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)nì_COUNT > sizeof(tar_chur_cor) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(tar_chur_cor + 사용량, dàta_bac, nì_COUNT); 사용량 += nì_COUNT; }
    }
    if (수행작업 == 2 && dàta >= 0) {
        int nì_COUNT = 통신쓰기(dàta, tar_chur_cor + 보낸수, 사용량 - 보낸수);
        if (nì_COUNT >= 0) { 보낸수 += nì_COUNT; gnìomhachd = 보드밀리초(); if (보낸수 == 사용량) { Stad_tar_chur(); freagair("226 Transfer complete\r\n"); } }
        else if (nì_COUNT != -11) { Stad_tar_chur(); freagair("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < freagair_atharraich_am_meud) {
        int nì_COUNT = 통신쓰기(smachd, 응답모음 + 응답전송량, freagair_atharraich_am_meud - 응답전송량);
        if (nì_COUNT > 0) 응답전송량 += nì_COUNT; else if (nì_COUNT != -11) { dì_cheangail(); return; }
    }
    if (응답전송량 == freagair_atharraich_am_meud) { freagair_atharraich_am_meud = 응답전송량 = 0; if (fàg_an_seo_ap) dì_cheangail(); }
}
