#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "Netwọọkụ_ikpo.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int 수신창구 = -1, njizi = -1, nke_eji_aka_mèe_njikọ = -1, datà = -1;
static unsigned 로그인됨, 사용자확인, ahịrī_ụha, 줄오류, 끝내기, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned nzaghachi_ụha, 응답전송량, 다음접속번호;
static uint32_t Mmèmmè;
static char ahịrī[256], 응답모음[2048], ọbọakwụkwọ_ndebà_akara_ahà[64], dògharịa_akara_ahà[64];
static unsigned char dògharịa_ọnọdụ[16384];
static int 같은지(const char *첫째값, const char *둘째값) { while (*첫째값 && *첫째값 == *둘째값) { 첫째값++; 둘째값++; } return *첫째값 == *둘째값; }
static void nzaghachi(const char *ùsòròokwū_datà) {
    size_t 개수 = strlen(ùsòròokwū_datà);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, nzaghachi_ụha - 응답전송량); nzaghachi_ụha -= 응답전송량; 응답전송량 = 0; }
    if (개수 > sizeof(응답모음) - nzaghachi_ụha) { 끝내기 = 1; return; }
    memcpy(응답모음 + nzaghachi_ụha, ùsòròokwū_datà, 개수); nzaghachi_ụha += 개수;
}
static void 수치(unsigned valuu, char *결과자료, unsigned *개수) {
    char 숫자수[10]; unsigned 항목수 = 0;
    do { 숫자수[항목수++] = '0' + valuu % 10; valuu /= 10; } while (valuu);
    while (항목수) 결과자료[(*개수)++] = 숫자수[--항목수];
}
static void kwụsị_dògharịa(void) {
    if (datà >= 0) mmechi_Netwọọkụ(datà); if (nke_eji_aka_mèe_njikọ >= 0) mmechi_Netwọọkụ(nke_eji_aka_mèe_njikọ);
    datà = nke_eji_aka_mèe_njikọ = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void wepụ_njikọ(void) {
    kwụsị_dògharịa(); if (njizi >= 0) mmechi_Netwọọkụ(njizi); njizi = -1;
    로그인됨 = 사용자확인 = ahịrī_ụha = 줄오류 = nzaghachi_ụha = 응답전송량 = 끝내기 = 0;
}
int ọbọakwụkwọ_dògharịa_njizi(int mmèm) {
    if (mmèm == 2) return 수신창구 >= 0;
    if (mmèm == 0) { wepụ_njikọ(); if (수신창구 >= 0) mmechi_Netwọọkụ(수신창구); 수신창구 = -1; return 0; }
    if (mmèm != 1) return -22; if (수신창구 >= 0) return 0;
    수신창구 = 통신끝점만들기(1); if (수신창구 < 0) return 수신창구;
    int 반환값 = 망주소묶기(수신창구, 망상태읽기(0,0), 21); if (!반환값) 반환값 = 연결기다리기(수신창구);
    if (반환값 < 0) { mmechi_Netwọọkụ(수신창구); 수신창구 = -1; } return 반환값;
}
static int ụzọ_ozi(const char *Aha) {
    unsigned 개수 = 0; if (*Aha == '/') Aha++;
    if (!*Aha || 같은지(Aha, ".") || 같은지(Aha, "..")) return 0;
    ọbọakwụkwọ_ndebà_akara_ahà[개수++] = '/';
    while (*Aha) {
        unsigned char koòdù_nkeakàrà = *Aha++;
        if (개수 >= 63 || koòdù_nkeakàrà < 32 || koòdù_nkeakàrà == 127 || koòdù_nkeakàrà == '/' || koòdù_nkeakàrà == '\\') return 0;
        ọbọakwụkwọ_ndebà_akara_ahà[개수++] = koòdù_nkeakàrà;
    }
    ọbọakwụkwọ_ndebà_akara_ahà[개수] = 0; return 1;
}
static void zìga_ndepụta(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int 개수 = 자바파일항목길이(순번); if (개수 <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned 항목수 = strlen(앞부분); memcpy(dògharịa_ọnọdụ + 사용량, 앞부분, 항목수); 사용량 += 항목수;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)dògharịa_ọnọdụ, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        항목수 = strlen(뒷부분); memcpy(dògharịa_ọnọdụ + 사용량, 뒷부분, 항목수); 사용량 += 항목수;
        for (int 안쪽순번 = 0; 안쪽순번 < 개수; 안쪽순번++) dògharịa_ọnọdụ[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        dògharịa_ọnọdụ[사용량++] = '\r'; dògharịa_ọnọdụ[사용량++] = '\n';
    }
}
static void Kwado_nke_eji_aka_mèe_njikọ(int 확장여부) {
    if (수행작업) { nzaghachi("450 Transfer in progress\r\n"); return; }
    kwụsị_dògharịa(); nke_eji_aka_mèe_njikọ = 통신끝점만들기(1);
    if (nke_eji_aka_mèe_njikọ >= 0) 통신주소재사용(nke_eji_aka_mèe_njikọ);
    unsigned 접속번호 = 50000 + 다음접속번호++ % 8;
    if (nke_eji_aka_mèe_njikọ < 0 || 망주소묶기(nke_eji_aka_mèe_njikọ, 망상태읽기(0,0), 접속번호) || 연결기다리기(nke_eji_aka_mèe_njikọ)) {
        kwụsị_dògharịa(); nzaghachi("425 Cannot open passive listener\r\n"); return;
    }
    char 응답자료[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned 개수 = strlen(앞부분); memcpy(응답자료, 앞부분, 개수);
    if (확장여부) { 수치(접속번호, 응답자료, &개수); 응답자료[개수++] = '|'; }
    else {
        uint32_t àdreèsì=망상태읽기(0,0);
        for (int 자리=24;자리>=0;자리-=8) { 수치((àdreèsì>>자리)&255,응답자료,&개수);응답자료[개수++]=','; }
        수치(접속번호 / 256, 응답자료, &개수); 응답자료[개수++] = ','; 수치(접속번호 % 256, 응답자료, &개수);
    }
    응답자료[개수++] = ')'; 응답자료[개수++] = '\r'; 응답자료[개수++] = '\n'; 응답자료[개수] = 0; nzaghachi(응답자료);
}
static void Ntiiwu(void) {
    ahịrī[ahịrī_ụha] = 0;
    char *부가인수 = ahịrī; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(ahịrī, "QUIT")) { kwụsị_dògharịa(); nzaghachi("221 Goodbye\r\n"); 끝내기 = 1; return; }
    if (같은지(ahịrī, "NOOP")) { nzaghachi("200 OK\r\n"); return; }
    if (같은지(ahịrī, "SYST")) { nzaghachi("215 UNIX Type: L8\r\n"); return; }
    if (같은지(ahịrī, "FEAT")) { nzaghachi("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(ahịrī, "USER")) { 로그인됨 = 0; 사용자확인 = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); nzaghachi(사용자확인 ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(ahịrī, "PASS")) { 로그인됨 = 사용자확인; nzaghachi(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { nzaghachi("530 Login first\r\n"); return; }
    if (같은지(ahịrī, "PWD")) nzaghachi("257 \"/\"\r\n");
    else if (같은지(ahịrī, "CWD")) nzaghachi(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(ahịrī, "TYPE")) nzaghachi(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(ahịrī, "OPTS")) nzaghachi(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(ahịrī, "PASV")) Kwado_nke_eji_aka_mèe_njikọ(0);
    else if (같은지(ahịrī, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) nzaghachi("522 IPv4 only\r\n"); else Kwado_nke_eji_aka_mèe_njikọ(1); }
    else if (같은지(ahịrī, "ABOR")) { kwụsị_dògharịa(); nzaghachi("226 Transfer aborted\r\n"); }
    else if (같은지(ahịrī, "DELE")) { nzaghachi(ụzọ_ozi(부가인수) && pk_unlink(ọbọakwụkwọ_ndebà_akara_ahà) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(ahịrī, "LIST") || 같은지(ahịrī, "NLST") || 같은지(ahịrī, "MLSD")) {
        if (수행작업) { nzaghachi("450 Transfer in progress\r\n"); return; }
        if (nke_eji_aka_mèe_njikọ < 0 && datà < 0) { nzaghachi("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { nzaghachi("550 Root listing only\r\n"); return; }
        zìga_ndepụta(같은지(ahịrī,"MLSD") ? 2 : 같은지(ahịrī,"LIST") ? 1 : 0); 수행작업 = 2;
        nzaghachi("150 Opening directory listing\r\n");
    }
    else if (같은지(ahịrī, "SIZE")) {
        if (!ụzọ_ozi(부가인수)) { nzaghachi("550 Invalid filename\r\n"); return; }
        int ọbọakwụkwọ_ebenjìaka = pk_open(ọbọakwụkwọ_ndebà_akara_ahà, ọgụgụ_naanị_valuu, 0); if (ọbọakwụkwọ_ebenjìaka < 0) { nzaghachi("550 File unavailable\r\n"); return; }
        int Ụhara = pk_size(ọbọakwụkwọ_ebenjìaka); pk_close(ọbọakwụkwọ_ebenjìaka); char 응답자료[32] = "213 "; unsigned 개수 = 4;
        수치(Ụhara, 응답자료, &개수); 응답자료[개수++] = '\r'; 응답자료[개수++] = '\n'; 응답자료[개수] = 0; nzaghachi(응답자료);
    } else if (같은지(ahịrī, "STOR") || 같은지(ahịrī, "RETR")) {
        if (수행작업) { nzaghachi("450 Transfer in progress\r\n"); return; }
        if (nke_eji_aka_mèe_njikọ < 0 && datà < 0) { nzaghachi("425 Use PASV or EPSV\r\n"); return; }
        if (!ụzọ_ozi(부가인수)) { nzaghachi("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(ahịrī, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(dògharịa_akara_ahà, ọbọakwụkwọ_ndebà_akara_ahà, strlen(ọbọakwụkwọ_ndebà_akara_ahà) + 1);
        if (수행작업 == 2) {
            int ọbọakwụkwọ_ebenjìaka = pk_open(ọbọakwụkwọ_ndebà_akara_ahà, ọgụgụ_naanị_valuu, 0);
            if (ọbọakwụkwọ_ebenjìaka < 0) { 수행작업 = 0; nzaghachi("550 File unavailable\r\n"); return; }
            int 개수 = pk_read(ọbọakwụkwọ_ebenjìaka, dògharịa_ọnọdụ, sizeof(dògharịa_ọnọdụ)); pk_close(ọbọakwụkwọ_ebenjìaka);
            if (개수 < 0) { 수행작업 = 0; nzaghachi("451 Read failed\r\n"); return; } 사용량 = 개수;
        }
        nzaghachi("150 Opening binary data connection\r\n");
    } else nzaghachi("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (수신창구 < 0) return;
    int 들어온연결 = 망연결받기(수신창구);
    if (들어온연결 >= 0) {
        if (njizi >= 0) { 통신쓰기(들어온연결, "421 One session at a time\r\n", 27); mmechi_Netwọọkụ(들어온연결); }
        else { njizi = 들어온연결; Mmèmmè = 보드밀리초(); nzaghachi("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (njizi < 0) return;
    if ((uint32_t)(보드밀리초() - Mmèmmè) > 60000) { wepụ_njikọ(); return; }
    if (!끝내기) for (unsigned 처리한도 = 0; 처리한도 < 256; 처리한도++) {
        unsigned char koòdù_nkeakàrà; int 반환값 = 통신읽기(njizi, &koòdù_nkeakàrà, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { wepụ_njikọ(); return; } Mmèmmè = 보드밀리초();
        if (koòdù_nkeakàrà == '\n') { if (줄오류) nzaghachi("500 Command too long or invalid\r\n"); else Ntiiwu(); ahịrī_ụha = 줄오류 = 0; if (끝내기) break; }
        else if (koòdù_nkeakàrà != '\r') { if (!koòdù_nkeakàrà || ahịrī_ụha >= sizeof(ahịrī) - 1) 줄오류 = 1; else ahịrī[ahịrī_ụha++] = koòdù_nkeakàrà; }
    }
    if (nke_eji_aka_mèe_njikọ >= 0 && datà < 0) {
        int 반환값 = 망연결받기(nke_eji_aka_mèe_njikọ);
        if (반환값 >= 0) {
            if (상대통신주소(반환값) != 상대통신주소(njizi)) mmechi_Netwọọkụ(반환값);
            else { datà = 반환값; mmechi_Netwọọkụ(nke_eji_aka_mèe_njikọ); nke_eji_aka_mèe_njikọ = -1; Mmèmmè = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && datà >= 0) for (unsigned 처리한도 = 0; 처리한도 < 8; 처리한도++) {
        unsigned char datà_gbochie[512]; int 개수 = 통신읽기(datà, datà_gbochie, sizeof(datà_gbochie));
        if (개수 == -11) break;
        if (개수 < 0) { kwụsị_dògharịa(); nzaghachi("426 Data connection failed\r\n"); break; }
        Mmèmmè = 보드밀리초();
        if (개수 == 0) {
            int 결과 = -1;
            if (!실패여부) {
                int ọbọakwụkwọ_ebenjìaka = pk_open(dògharịa_akara_ahà, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (ọbọakwụkwọ_ebenjìaka >= 0) { 결과 = pk_write(ọbọakwụkwọ_ebenjìaka, dògharịa_ọnọdụ, 사용량); pk_close(ọbọakwụkwọ_ebenjìaka); }
            }
            int 성공여부 = !실패여부 && 결과 == (int)사용량; kwụsị_dògharịa(); nzaghachi(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)개수 > sizeof(dògharịa_ọnọdụ) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(dògharịa_ọnọdụ + 사용량, datà_gbochie, 개수); 사용량 += 개수; }
    }
    if (수행작업 == 2 && datà >= 0) {
        int 개수 = 통신쓰기(datà, dògharịa_ọnọdụ + 보낸수, 사용량 - 보낸수);
        if (개수 >= 0) { 보낸수 += 개수; Mmèmmè = 보드밀리초(); if (보낸수 == 사용량) { kwụsị_dògharịa(); nzaghachi("226 Transfer complete\r\n"); } }
        else if (개수 != -11) { kwụsị_dògharịa(); nzaghachi("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < nzaghachi_ụha) {
        int 개수 = 통신쓰기(njizi, 응답모음 + 응답전송량, nzaghachi_ụha - 응답전송량);
        if (개수 > 0) 응답전송량 += 개수; else if (개수 != -11) { wepụ_njikọ(); return; }
    }
    if (응답전송량 == nzaghachi_ụha) { nzaghachi_ụha = 응답전송량 = 0; if (끝내기) wepụ_njikọ(); }
}
