#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "Hanyar_sadarwa_tara.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int 수신창구 = -1, masarrafa = -1, Aikin_hannu_haɗi = -1, Tarin_bayani = -1;
static unsigned 로그인됨, Mai_anfani_da_kwamfuta_TO, Layi_girma, 줄오류, 끝내기, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned mayar_da_martani_girma, 응답전송량, 다음접속번호;
static uint32_t Aiki_4d9c9a53;
static char Layi[256], 응답모음[2048], Fayil_Mashigar_bayanai_Suna[64], Gusar_da_Suna[64];
static unsigned char Gusar_da_Matsayi[16384];
static int 같은지(const char *첫째값, const char *둘째값) { while (*첫째값 && *첫째값 == *둘째값) { 첫째값++; 둘째값++; } return *첫째값 == *둘째값; }
static void mayar_da_martani(const char *Zare_Tarin_bayani) {
    size_t 개수 = strlen(Zare_Tarin_bayani);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, mayar_da_martani_girma - 응답전송량); mayar_da_martani_girma -= 응답전송량; 응답전송량 = 0; }
    if (개수 > sizeof(응답모음) - mayar_da_martani_girma) { 끝내기 = 1; return; }
    memcpy(응답모음 + mayar_da_martani_girma, Zare_Tarin_bayani, 개수); mayar_da_martani_girma += 개수;
}
static void 수치(unsigned Daraja, char *결과자료, unsigned *개수) {
    char 숫자수[10]; unsigned 항목수 = 0;
    do { 숫자수[항목수++] = '0' + Daraja % 10; Daraja /= 10; } while (Daraja);
    while (항목수) 결과자료[(*개수)++] = 숫자수[--항목수];
}
static void Tsaya_Gusar_da(void) {
    if (Tarin_bayani >= 0) Rufe_Hanyar_sadarwa(Tarin_bayani); if (Aikin_hannu_haɗi >= 0) Rufe_Hanyar_sadarwa(Aikin_hannu_haɗi);
    Tarin_bayani = Aikin_hannu_haɗi = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void cire_haɗi(void) {
    Tsaya_Gusar_da(); if (masarrafa >= 0) Rufe_Hanyar_sadarwa(masarrafa); masarrafa = -1;
    로그인됨 = Mai_anfani_da_kwamfuta_TO = Layi_girma = 줄오류 = mayar_da_martani_girma = 응답전송량 = 끝내기 = 0;
}
int Fayil_Gusar_da_masarrafa(int Aiki) {
    if (Aiki == 2) return 수신창구 >= 0;
    if (Aiki == 0) { cire_haɗi(); if (수신창구 >= 0) Rufe_Hanyar_sadarwa(수신창구); 수신창구 = -1; return 0; }
    if (Aiki != 1) return -22; if (수신창구 >= 0) return 0;
    수신창구 = 통신끝점만들기(1); if (수신창구 < 0) return 수신창구;
    int 반환값 = 망주소묶기(수신창구, 망상태읽기(0,0), 21); if (!반환값) 반환값 = 연결기다리기(수신창구);
    if (반환값 < 0) { Rufe_Hanyar_sadarwa(수신창구); 수신창구 = -1; } return 반환값;
}
static int Hanyar_shiga(const char *Suna) {
    unsigned 개수 = 0; if (*Suna == '/') Suna++;
    if (!*Suna || 같은지(Suna, ".") || 같은지(Suna, "..")) return 0;
    Fayil_Mashigar_bayanai_Suna[개수++] = '/';
    while (*Suna) {
        unsigned char Lambar_sirrin_harafi = *Suna++;
        if (개수 >= 63 || Lambar_sirrin_harafi < 32 || Lambar_sirrin_harafi == 127 || Lambar_sirrin_harafi == '/' || Lambar_sirrin_harafi == '\\') return 0;
        Fayil_Mashigar_bayanai_Suna[개수++] = Lambar_sirrin_harafi;
    }
    Fayil_Mashigar_bayanai_Suna[개수] = 0; return 1;
}
static void Aika_Jeri(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int 개수 = 자바파일항목길이(순번); if (개수 <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned 항목수 = strlen(앞부분); memcpy(Gusar_da_Matsayi + 사용량, 앞부분, 항목수); 사용량 += 항목수;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)Gusar_da_Matsayi, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        항목수 = strlen(뒷부분); memcpy(Gusar_da_Matsayi + 사용량, 뒷부분, 항목수); 사용량 += 항목수;
        for (int 안쪽순번 = 0; 안쪽순번 < 개수; 안쪽순번++) Gusar_da_Matsayi[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        Gusar_da_Matsayi[사용량++] = '\r'; Gusar_da_Matsayi[사용량++] = '\n';
    }
}
static void Shirya_Aikin_hannu_haɗi(int 확장여부) {
    if (수행작업) { mayar_da_martani("450 Transfer in progress\r\n"); return; }
    Tsaya_Gusar_da(); Aikin_hannu_haɗi = 통신끝점만들기(1);
    if (Aikin_hannu_haɗi >= 0) 통신주소재사용(Aikin_hannu_haɗi);
    unsigned lambar_kafa = 50000 + 다음접속번호++ % 8;
    if (Aikin_hannu_haɗi < 0 || 망주소묶기(Aikin_hannu_haɗi, 망상태읽기(0,0), lambar_kafa) || 연결기다리기(Aikin_hannu_haɗi)) {
        Tsaya_Gusar_da(); mayar_da_martani("425 Cannot open passive listener\r\n"); return;
    }
    char 응답자료[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned 개수 = strlen(앞부분); memcpy(응답자료, 앞부분, 개수);
    if (확장여부) { 수치(lambar_kafa, 응답자료, &개수); 응답자료[개수++] = '|'; }
    else {
        uint32_t imel=망상태읽기(0,0);
        for (int 자리=24;자리>=0;자리-=8) { 수치((imel>>자리)&255,응답자료,&개수);응답자료[개수++]=','; }
        수치(lambar_kafa / 256, 응답자료, &개수); 응답자료[개수++] = ','; 수치(lambar_kafa % 256, 응답자료, &개수);
    }
    응답자료[개수++] = ')'; 응답자료[개수++] = '\r'; 응답자료[개수++] = '\n'; 응답자료[개수] = 0; mayar_da_martani(응답자료);
}
static void Umarni(void) {
    Layi[Layi_girma] = 0;
    char *부가인수 = Layi; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(Layi, "QUIT")) { Tsaya_Gusar_da(); mayar_da_martani("221 Goodbye\r\n"); 끝내기 = 1; return; }
    if (같은지(Layi, "NOOP")) { mayar_da_martani("200 OK\r\n"); return; }
    if (같은지(Layi, "SYST")) { mayar_da_martani("215 UNIX Type: L8\r\n"); return; }
    if (같은지(Layi, "FEAT")) { mayar_da_martani("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(Layi, "USER")) { 로그인됨 = 0; Mai_anfani_da_kwamfuta_TO = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); mayar_da_martani(Mai_anfani_da_kwamfuta_TO ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(Layi, "PASS")) { 로그인됨 = Mai_anfani_da_kwamfuta_TO; mayar_da_martani(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { mayar_da_martani("530 Login first\r\n"); return; }
    if (같은지(Layi, "PWD")) mayar_da_martani("257 \"/\"\r\n");
    else if (같은지(Layi, "CWD")) mayar_da_martani(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(Layi, "TYPE")) mayar_da_martani(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(Layi, "OPTS")) mayar_da_martani(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(Layi, "PASV")) Shirya_Aikin_hannu_haɗi(0);
    else if (같은지(Layi, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) mayar_da_martani("522 IPv4 only\r\n"); else Shirya_Aikin_hannu_haɗi(1); }
    else if (같은지(Layi, "ABOR")) { Tsaya_Gusar_da(); mayar_da_martani("226 Transfer aborted\r\n"); }
    else if (같은지(Layi, "DELE")) { mayar_da_martani(Hanyar_shiga(부가인수) && pk_unlink(Fayil_Mashigar_bayanai_Suna) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(Layi, "LIST") || 같은지(Layi, "NLST") || 같은지(Layi, "MLSD")) {
        if (수행작업) { mayar_da_martani("450 Transfer in progress\r\n"); return; }
        if (Aikin_hannu_haɗi < 0 && Tarin_bayani < 0) { mayar_da_martani("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { mayar_da_martani("550 Root listing only\r\n"); return; }
        Aika_Jeri(같은지(Layi,"MLSD") ? 2 : 같은지(Layi,"LIST") ? 1 : 0); 수행작업 = 2;
        mayar_da_martani("150 Opening directory listing\r\n");
    }
    else if (같은지(Layi, "SIZE")) {
        if (!Hanyar_shiga(부가인수)) { mayar_da_martani("550 Invalid filename\r\n"); return; }
        int Fayil_Mariki = pk_open(Fayil_Mashigar_bayanai_Suna, karanta_kawai_Daraja, 0); if (Fayil_Mariki < 0) { mayar_da_martani("550 File unavailable\r\n"); return; }
        int Girma = pk_size(Fayil_Mariki); pk_close(Fayil_Mariki); char 응답자료[32] = "213 "; unsigned 개수 = 4;
        수치(Girma, 응답자료, &개수); 응답자료[개수++] = '\r'; 응답자료[개수++] = '\n'; 응답자료[개수] = 0; mayar_da_martani(응답자료);
    } else if (같은지(Layi, "STOR") || 같은지(Layi, "RETR")) {
        if (수행작업) { mayar_da_martani("450 Transfer in progress\r\n"); return; }
        if (Aikin_hannu_haɗi < 0 && Tarin_bayani < 0) { mayar_da_martani("425 Use PASV or EPSV\r\n"); return; }
        if (!Hanyar_shiga(부가인수)) { mayar_da_martani("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(Layi, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(Gusar_da_Suna, Fayil_Mashigar_bayanai_Suna, strlen(Fayil_Mashigar_bayanai_Suna) + 1);
        if (수행작업 == 2) {
            int Fayil_Mariki = pk_open(Fayil_Mashigar_bayanai_Suna, karanta_kawai_Daraja, 0);
            if (Fayil_Mariki < 0) { 수행작업 = 0; mayar_da_martani("550 File unavailable\r\n"); return; }
            int 개수 = pk_read(Fayil_Mariki, Gusar_da_Matsayi, sizeof(Gusar_da_Matsayi)); pk_close(Fayil_Mariki);
            if (개수 < 0) { 수행작업 = 0; mayar_da_martani("451 Read failed\r\n"); return; } 사용량 = 개수;
        }
        mayar_da_martani("150 Opening binary data connection\r\n");
    } else mayar_da_martani("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (수신창구 < 0) return;
    int Mai_shigowa_haɗi = 망연결받기(수신창구);
    if (Mai_shigowa_haɗi >= 0) {
        if (masarrafa >= 0) { 통신쓰기(Mai_shigowa_haɗi, "421 One session at a time\r\n", 27); Rufe_Hanyar_sadarwa(Mai_shigowa_haɗi); }
        else { masarrafa = Mai_shigowa_haɗi; Aiki_4d9c9a53 = 보드밀리초(); mayar_da_martani("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (masarrafa < 0) return;
    if ((uint32_t)(보드밀리초() - Aiki_4d9c9a53) > 60000) { cire_haɗi(); return; }
    if (!끝내기) for (unsigned 처리한도 = 0; 처리한도 < 256; 처리한도++) {
        unsigned char Lambar_sirrin_harafi; int 반환값 = 통신읽기(masarrafa, &Lambar_sirrin_harafi, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { cire_haɗi(); return; } Aiki_4d9c9a53 = 보드밀리초();
        if (Lambar_sirrin_harafi == '\n') { if (줄오류) mayar_da_martani("500 Command too long or invalid\r\n"); else Umarni(); Layi_girma = 줄오류 = 0; if (끝내기) break; }
        else if (Lambar_sirrin_harafi != '\r') { if (!Lambar_sirrin_harafi || Layi_girma >= sizeof(Layi) - 1) 줄오류 = 1; else Layi[Layi_girma++] = Lambar_sirrin_harafi; }
    }
    if (Aikin_hannu_haɗi >= 0 && Tarin_bayani < 0) {
        int 반환값 = 망연결받기(Aikin_hannu_haɗi);
        if (반환값 >= 0) {
            if (상대통신주소(반환값) != 상대통신주소(masarrafa)) Rufe_Hanyar_sadarwa(반환값);
            else { Tarin_bayani = 반환값; Rufe_Hanyar_sadarwa(Aikin_hannu_haɗi); Aikin_hannu_haɗi = -1; Aiki_4d9c9a53 = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && Tarin_bayani >= 0) for (unsigned 처리한도 = 0; 처리한도 < 8; 처리한도++) {
        unsigned char Tarin_bayani_bulo[512]; int 개수 = 통신읽기(Tarin_bayani, Tarin_bayani_bulo, sizeof(Tarin_bayani_bulo));
        if (개수 == -11) break;
        if (개수 < 0) { Tsaya_Gusar_da(); mayar_da_martani("426 Data connection failed\r\n"); break; }
        Aiki_4d9c9a53 = 보드밀리초();
        if (개수 == 0) {
            int 결과 = -1;
            if (!실패여부) {
                int Fayil_Mariki = pk_open(Gusar_da_Suna, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (Fayil_Mariki >= 0) { 결과 = pk_write(Fayil_Mariki, Gusar_da_Matsayi, 사용량); pk_close(Fayil_Mariki); }
            }
            int 성공여부 = !실패여부 && 결과 == (int)사용량; Tsaya_Gusar_da(); mayar_da_martani(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)개수 > sizeof(Gusar_da_Matsayi) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(Gusar_da_Matsayi + 사용량, Tarin_bayani_bulo, 개수); 사용량 += 개수; }
    }
    if (수행작업 == 2 && Tarin_bayani >= 0) {
        int 개수 = 통신쓰기(Tarin_bayani, Gusar_da_Matsayi + 보낸수, 사용량 - 보낸수);
        if (개수 >= 0) { 보낸수 += 개수; Aiki_4d9c9a53 = 보드밀리초(); if (보낸수 == 사용량) { Tsaya_Gusar_da(); mayar_da_martani("226 Transfer complete\r\n"); } }
        else if (개수 != -11) { Tsaya_Gusar_da(); mayar_da_martani("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < mayar_da_martani_girma) {
        int 개수 = 통신쓰기(masarrafa, 응답모음 + 응답전송량, mayar_da_martani_girma - 응답전송량);
        if (개수 > 0) 응답전송량 += 개수; else if (개수 != -11) { cire_haɗi(); return; }
    }
    if (응답전송량 == mayar_da_martani_girma) { mayar_da_martani_girma = 응답전송량 = 0; if (끝내기) cire_haɗi(); }
}
