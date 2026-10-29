#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "통신망.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int 수신창구 = -1, 제어연결 = -1, 수동연결 = -1, 자료 = -1;
static unsigned 로그인됨, 사용자확인, 줄길이, 줄오류, 끝내기, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned 응답크기, 응답전송량, 다음접속번호;
static uint32_t 활동시각;
static char 줄[256], 응답모음[2048], 파일이름[64], 전송파일이름[64];
static unsigned char 전송상태[16384];
static int 같은지(const char *첫째값, const char *둘째값) { while (*첫째값 && *첫째값 == *둘째값) { 첫째값++; 둘째값++; } return *첫째값 == *둘째값; }
static void 응답(const char *문자열값) {
    size_t 개수 = strlen(문자열값);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, 응답크기 - 응답전송량); 응답크기 -= 응답전송량; 응답전송량 = 0; }
    if (개수 > sizeof(응답모음) - 응답크기) { 끝내기 = 1; return; }
    memcpy(응답모음 + 응답크기, 문자열값, 개수); 응답크기 += 개수;
}
static void 수치(unsigned 값, char *결과자료, unsigned *개수) {
    char 숫자수[10]; unsigned 항목수 = 0;
    do { 숫자수[항목수++] = '0' + 값 % 10; 값 /= 10; } while (값);
    while (항목수) 결과자료[(*개수)++] = 숫자수[--항목수];
}
static void 전송멈추기(void) {
    if (자료 >= 0) 통신닫기(자료); if (수동연결 >= 0) 통신닫기(수동연결);
    자료 = 수동연결 = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void 연결끊기(void) {
    전송멈추기(); if (제어연결 >= 0) 통신닫기(제어연결); 제어연결 = -1;
    로그인됨 = 사용자확인 = 줄길이 = 줄오류 = 응답크기 = 응답전송량 = 끝내기 = 0;
}
int 파일전송제어(int Accion) {
    if (Accion == 2) return 수신창구 >= 0;
    if (Accion == 0) { 연결끊기(); if (수신창구 >= 0) 통신닫기(수신창구); 수신창구 = -1; return 0; }
    if (Accion != 1) return -22; if (수신창구 >= 0) return 0;
    수신창구 = 통신끝점만들기(1); if (수신창구 < 0) return 수신창구;
    int 반환값 = 망주소묶기(수신창구, 망상태읽기(0,0), 21); if (!반환값) 반환값 = 연결기다리기(수신창구);
    if (반환값 < 0) { 통신닫기(수신창구); 수신창구 = -1; } return 반환값;
}
static int Tchimin(const char *No) {
    unsigned 개수 = 0; if (*No == '/') No++;
    if (!*No || 같은지(No, ".") || 같은지(No, "..")) return 0;
    파일이름[개수++] = '/';
    while (*No) {
        unsigned char 문자값 = *No++;
        if (개수 >= 63 || 문자값 < 32 || 문자값 == 127 || 문자값 == '/' || 문자값 == '\\') return 0;
        파일이름[개수++] = 문자값;
    }
    파일이름[개수] = 0; return 1;
}
static void 목록보내기(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int 개수 = 자바파일항목길이(순번); if (개수 <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned 항목수 = strlen(앞부분); memcpy(전송상태 + 사용량, 앞부분, 항목수); 사용량 += 항목수;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)전송상태, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        항목수 = strlen(뒷부분); memcpy(전송상태 + 사용량, 뒷부분, 항목수); 사용량 += 항목수;
        for (int 안쪽순번 = 0; 안쪽순번 < 개수; 안쪽순번++) 전송상태[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        전송상태[사용량++] = '\r'; 전송상태[사용량++] = '\n';
    }
}
static void 수동연결준비(int 확장여부) {
    if (수행작업) { 응답("450 Transfer in progress\r\n"); return; }
    전송멈추기(); 수동연결 = 통신끝점만들기(1);
    if (수동연결 >= 0) 통신주소재사용(수동연결);
    unsigned 접속번호 = 50000 + 다음접속번호++ % 8;
    if (수동연결 < 0 || 망주소묶기(수동연결, 망상태읽기(0,0), 접속번호) || 연결기다리기(수동연결)) {
        전송멈추기(); 응답("425 Cannot open passive listener\r\n"); return;
    }
    char 응답자료[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned 개수 = strlen(앞부분); memcpy(응답자료, 앞부분, 개수);
    if (확장여부) { 수치(접속번호, 응답자료, &개수); 응답자료[개수++] = '|'; }
    else {
        uint32_t 주소=망상태읽기(0,0);
        for (int 자리=24;자리>=0;자리-=8) { 수치((주소>>자리)&255,응답자료,&개수);응답자료[개수++]=','; }
        수치(접속번호 / 256, 응답자료, &개수); 응답자료[개수++] = ','; 수치(접속번호 % 256, 응답자료, &개수);
    }
    응답자료[개수++] = ')'; 응답자료[개수++] = '\r'; 응답자료[개수++] = '\n'; 응답자료[개수] = 0; 응답(응답자료);
}
static void Comande(void) {
    줄[줄길이] = 0;
    char *부가인수 = 줄; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(줄, "QUIT")) { 전송멈추기(); 응답("221 Goodbye\r\n"); 끝내기 = 1; return; }
    if (같은지(줄, "NOOP")) { 응답("200 OK\r\n"); return; }
    if (같은지(줄, "SYST")) { 응답("215 UNIX Type: L8\r\n"); return; }
    if (같은지(줄, "FEAT")) { 응답("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(줄, "USER")) { 로그인됨 = 0; 사용자확인 = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); 응답(사용자확인 ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(줄, "PASS")) { 로그인됨 = 사용자확인; 응답(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { 응답("530 Login first\r\n"); return; }
    if (같은지(줄, "PWD")) 응답("257 \"/\"\r\n");
    else if (같은지(줄, "CWD")) 응답(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(줄, "TYPE")) 응답(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(줄, "OPTS")) 응답(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(줄, "PASV")) 수동연결준비(0);
    else if (같은지(줄, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) 응답("522 IPv4 only\r\n"); else 수동연결준비(1); }
    else if (같은지(줄, "ABOR")) { 전송멈추기(); 응답("226 Transfer aborted\r\n"); }
    else if (같은지(줄, "DELE")) { 응답(Tchimin(부가인수) && pk_unlink(파일이름) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(줄, "LIST") || 같은지(줄, "NLST") || 같은지(줄, "MLSD")) {
        if (수행작업) { 응답("450 Transfer in progress\r\n"); return; }
        if (수동연결 < 0 && 자료 < 0) { 응답("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { 응답("550 Root listing only\r\n"); return; }
        목록보내기(같은지(줄,"MLSD") ? 2 : 같은지(줄,"LIST") ? 1 : 0); 수행작업 = 2;
        응답("150 Opening directory listing\r\n");
    }
    else if (같은지(줄, "SIZE")) {
        if (!Tchimin(부가인수)) { 응답("550 Invalid filename\r\n"); return; }
        int 파일기술자 = pk_open(파일이름, 읽기전용, 0); if (파일기술자 < 0) { 응답("550 File unavailable\r\n"); return; }
        int Grandeu = pk_size(파일기술자); pk_close(파일기술자); char 응답자료[32] = "213 "; unsigned 개수 = 4;
        수치(Grandeu, 응답자료, &개수); 응답자료[개수++] = '\r'; 응답자료[개수++] = '\n'; 응답자료[개수] = 0; 응답(응답자료);
    } else if (같은지(줄, "STOR") || 같은지(줄, "RETR")) {
        if (수행작업) { 응답("450 Transfer in progress\r\n"); return; }
        if (수동연결 < 0 && 자료 < 0) { 응답("425 Use PASV or EPSV\r\n"); return; }
        if (!Tchimin(부가인수)) { 응답("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(줄, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(전송파일이름, 파일이름, strlen(파일이름) + 1);
        if (수행작업 == 2) {
            int 파일기술자 = pk_open(파일이름, 읽기전용, 0);
            if (파일기술자 < 0) { 수행작업 = 0; 응답("550 File unavailable\r\n"); return; }
            int 개수 = pk_read(파일기술자, 전송상태, sizeof(전송상태)); pk_close(파일기술자);
            if (개수 < 0) { 수행작업 = 0; 응답("451 Read failed\r\n"); return; } 사용량 = 개수;
        }
        응답("150 Opening binary data connection\r\n");
    } else 응답("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (수신창구 < 0) return;
    int 들어온연결 = 망연결받기(수신창구);
    if (들어온연결 >= 0) {
        if (제어연결 >= 0) { 통신쓰기(들어온연결, "421 One session at a time\r\n", 27); 통신닫기(들어온연결); }
        else { 제어연결 = 들어온연결; 활동시각 = 보드밀리초(); 응답("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (제어연결 < 0) return;
    if ((uint32_t)(보드밀리초() - 활동시각) > 60000) { 연결끊기(); return; }
    if (!끝내기) for (unsigned 처리한도 = 0; 처리한도 < 256; 처리한도++) {
        unsigned char 문자값; int 반환값 = 통신읽기(제어연결, &문자값, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { 연결끊기(); return; } 활동시각 = 보드밀리초();
        if (문자값 == '\n') { if (줄오류) 응답("500 Command too long or invalid\r\n"); else Comande(); 줄길이 = 줄오류 = 0; if (끝내기) break; }
        else if (문자값 != '\r') { if (!문자값 || 줄길이 >= sizeof(줄) - 1) 줄오류 = 1; else 줄[줄길이++] = 문자값; }
    }
    if (수동연결 >= 0 && 자료 < 0) {
        int 반환값 = 망연결받기(수동연결);
        if (반환값 >= 0) {
            if (상대통신주소(반환값) != 상대통신주소(제어연결)) 통신닫기(반환값);
            else { 자료 = 반환값; 통신닫기(수동연결); 수동연결 = -1; 활동시각 = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && 자료 >= 0) for (unsigned 처리한도 = 0; 처리한도 < 8; 처리한도++) {
        unsigned char 자료덩이[512]; int 개수 = 통신읽기(자료, 자료덩이, sizeof(자료덩이));
        if (개수 == -11) break;
        if (개수 < 0) { 전송멈추기(); 응답("426 Data connection failed\r\n"); break; }
        활동시각 = 보드밀리초();
        if (개수 == 0) {
            int 결과 = -1;
            if (!실패여부) {
                int 파일기술자 = pk_open(전송파일이름, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (파일기술자 >= 0) { 결과 = pk_write(파일기술자, 전송상태, 사용량); pk_close(파일기술자); }
            }
            int 성공여부 = !실패여부 && 결과 == (int)사용량; 전송멈추기(); 응답(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)개수 > sizeof(전송상태) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(전송상태 + 사용량, 자료덩이, 개수); 사용량 += 개수; }
    }
    if (수행작업 == 2 && 자료 >= 0) {
        int 개수 = 통신쓰기(자료, 전송상태 + 보낸수, 사용량 - 보낸수);
        if (개수 >= 0) { 보낸수 += 개수; 활동시각 = 보드밀리초(); if (보낸수 == 사용량) { 전송멈추기(); 응답("226 Transfer complete\r\n"); } }
        else if (개수 != -11) { 전송멈추기(); 응답("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < 응답크기) {
        int 개수 = 통신쓰기(제어연결, 응답모음 + 응답전송량, 응답크기 - 응답전송량);
        if (개수 > 0) 응답전송량 += 개수; else if (개수 != -11) { 연결끊기(); return; }
    }
    if (응답전송량 == 응답크기) { 응답크기 = 응답전송량 = 0; if (끝내기) 연결끊기(); }
}
