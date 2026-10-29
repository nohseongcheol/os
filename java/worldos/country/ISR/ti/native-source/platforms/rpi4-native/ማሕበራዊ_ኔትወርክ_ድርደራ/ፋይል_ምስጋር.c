#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "ማሕበራዊ_ኔትወርክ_ድርደራ.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int 수신창구 = -1, ቁጽጽር = -1, ብኢድ_ርክብ = -1, ሓበሬታ = -1;
static unsigned 로그인됨, 사용자확인, መስመር_መጠን, 줄오류, 끝내기, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned መልስ_መጠን, 응답전송량, 다음접속번호;
static uint32_t ተግባር;
static char መስመር[256], 응답모음[2048], ፋይል_ምእታው_ሽም[64], ምስጋር_ሽም[64];
static unsigned char ምስጋር_ደረጃ[16384];
static int 같은지(const char *첫째값, const char *둘째값) { while (*첫째값 && *첫째값 == *둘째값) { 첫째값++; 둘째값++; } return *첫째값 == *둘째값; }
static void መልስ(const char *ሕብረ_ቁምፊ_ሓበሬታ) {
    size_t 개수 = strlen(ሕብረ_ቁምፊ_ሓበሬታ);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, መልስ_መጠን - 응답전송량); መልስ_መጠን -= 응답전송량; 응답전송량 = 0; }
    if (개수 > sizeof(응답모음) - መልስ_መጠን) { 끝내기 = 1; return; }
    memcpy(응답모음 + መልስ_መጠን, ሕብረ_ቁምፊ_ሓበሬታ, 개수); መልስ_መጠን += 개수;
}
static void 수치(unsigned ዋጋ, char *결과자료, unsigned *개수) {
    char 숫자수[10]; unsigned 항목수 = 0;
    do { 숫자수[항목수++] = '0' + ዋጋ % 10; ዋጋ /= 10; } while (ዋጋ);
    while (항목수) 결과자료[(*개수)++] = 숫자수[--항목수];
}
static void ኣቑም_ምስጋር(void) {
    if (ሓበሬታ >= 0) ዕጸው_ማሕበራዊ_ኔትወርክ(ሓበሬታ); if (ብኢድ_ርክብ >= 0) ዕጸው_ማሕበራዊ_ኔትወርክ(ብኢድ_ርክብ);
    ሓበሬታ = ብኢድ_ርክብ = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void ብተኽ(void) {
    ኣቑም_ምስጋር(); if (ቁጽጽር >= 0) ዕጸው_ማሕበራዊ_ኔትወርክ(ቁጽጽር); ቁጽጽር = -1;
    로그인됨 = 사용자확인 = መስመር_መጠን = 줄오류 = መልስ_መጠን = 응답전송량 = 끝내기 = 0;
}
int ፋይል_ምስጋር_ቁጽጽር(int ስጉምቲ) {
    if (ስጉምቲ == 2) return 수신창구 >= 0;
    if (ስጉምቲ == 0) { ብተኽ(); if (수신창구 >= 0) ዕጸው_ማሕበራዊ_ኔትወርክ(수신창구); 수신창구 = -1; return 0; }
    if (ስጉምቲ != 1) return -22; if (수신창구 >= 0) return 0;
    수신창구 = 통신끝점만들기(1); if (수신창구 < 0) return 수신창구;
    int 반환값 = 망주소묶기(수신창구, 망상태읽기(0,0), 21); if (!반환값) 반환값 = 연결기다리기(수신창구);
    if (반환값 < 0) { ዕጸው_ማሕበራዊ_ኔትወርክ(수신창구); 수신창구 = -1; } return 반환값;
}
static int መገዲ(const char *ሽም) {
    unsigned 개수 = 0; if (*ሽም == '/') ሽም++;
    if (!*ሽም || 같은지(ሽም, ".") || 같은지(ሽም, "..")) return 0;
    ፋይል_ምእታው_ሽም[개수++] = '/';
    while (*ሽም) {
        unsigned char ኮድ_ፊደል = *ሽም++;
        if (개수 >= 63 || ኮድ_ፊደል < 32 || ኮድ_ፊደል == 127 || ኮድ_ፊደል == '/' || ኮድ_ፊደል == '\\') return 0;
        ፋይል_ምእታው_ሽም[개수++] = ኮድ_ፊደል;
    }
    ፋይል_ምእታው_ሽም[개수] = 0; return 1;
}
static void ለኣኽ_ዝርዝር(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int 개수 = 자바파일항목길이(순번); if (개수 <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned 항목수 = strlen(앞부분); memcpy(ምስጋር_ደረጃ + 사용량, 앞부분, 항목수); 사용량 += 항목수;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)ምስጋር_ደረጃ, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        항목수 = strlen(뒷부분); memcpy(ምስጋር_ደረጃ + 사용량, 뒷부분, 항목수); 사용량 += 항목수;
        for (int 안쪽순번 = 0; 안쪽순번 < 개수; 안쪽순번++) ምስጋር_ደረጃ[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        ምስጋር_ደረጃ[사용량++] = '\r'; ምስጋር_ደረጃ[사용량++] = '\n';
    }
}
static void ኣዳልው_ብኢድ_ርክብ(int 확장여부) {
    if (수행작업) { መልስ("450 Transfer in progress\r\n"); return; }
    ኣቑም_ምስጋር(); ብኢድ_ርክብ = 통신끝점만들기(1);
    if (ብኢድ_ርክብ >= 0) 통신주소재사용(ብኢድ_ርክብ);
    unsigned 접속번호 = 50000 + 다음접속번호++ % 8;
    if (ብኢድ_ርክብ < 0 || 망주소묶기(ብኢድ_ርክብ, 망상태읽기(0,0), 접속번호) || 연결기다리기(ብኢድ_ርክብ)) {
        ኣቑም_ምስጋር(); መልስ("425 Cannot open passive listener\r\n"); return;
    }
    char 응답자료[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned 개수 = strlen(앞부분); memcpy(응답자료, 앞부분, 개수);
    if (확장여부) { 수치(접속번호, 응답자료, &개수); 응답자료[개수++] = '|'; }
    else {
        uint32_t ኣድራሻ=망상태읽기(0,0);
        for (int 자리=24;자리>=0;자리-=8) { 수치((ኣድራሻ>>자리)&255,응답자료,&개수);응답자료[개수++]=','; }
        수치(접속번호 / 256, 응답자료, &개수); 응답자료[개수++] = ','; 수치(접속번호 % 256, 응답자료, &개수);
    }
    응답자료[개수++] = ')'; 응답자료[개수++] = '\r'; 응답자료[개수++] = '\n'; 응답자료[개수] = 0; መልስ(응답자료);
}
static void ትእዛዝ(void) {
    መስመር[መስመር_መጠን] = 0;
    char *부가인수 = መስመር; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(መስመር, "QUIT")) { ኣቑም_ምስጋር(); መልስ("221 Goodbye\r\n"); 끝내기 = 1; return; }
    if (같은지(መስመር, "NOOP")) { መልስ("200 OK\r\n"); return; }
    if (같은지(መስመር, "SYST")) { መልስ("215 UNIX Type: L8\r\n"); return; }
    if (같은지(መስመር, "FEAT")) { መልስ("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(መስመር, "USER")) { 로그인됨 = 0; 사용자확인 = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); መልስ(사용자확인 ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(መስመር, "PASS")) { 로그인됨 = 사용자확인; መልስ(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { መልስ("530 Login first\r\n"); return; }
    if (같은지(መስመር, "PWD")) መልስ("257 \"/\"\r\n");
    else if (같은지(መስመር, "CWD")) መልስ(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(መስመር, "TYPE")) መልስ(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(መስመር, "OPTS")) መልስ(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(መስመር, "PASV")) ኣዳልው_ብኢድ_ርክብ(0);
    else if (같은지(መስመር, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) መልስ("522 IPv4 only\r\n"); else ኣዳልው_ብኢድ_ርክብ(1); }
    else if (같은지(መስመር, "ABOR")) { ኣቑም_ምስጋር(); መልስ("226 Transfer aborted\r\n"); }
    else if (같은지(መስመር, "DELE")) { መልስ(መገዲ(부가인수) && pk_unlink(ፋይል_ምእታው_ሽም) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(መስመር, "LIST") || 같은지(መስመር, "NLST") || 같은지(መስመር, "MLSD")) {
        if (수행작업) { መልስ("450 Transfer in progress\r\n"); return; }
        if (ብኢድ_ርክብ < 0 && ሓበሬታ < 0) { መልስ("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { መልስ("550 Root listing only\r\n"); return; }
        ለኣኽ_ዝርዝር(같은지(መስመር,"MLSD") ? 2 : 같은지(መስመር,"LIST") ? 1 : 0); 수행작업 = 2;
        መልስ("150 Opening directory listing\r\n");
    }
    else if (같은지(መስመር, "SIZE")) {
        if (!መገዲ(부가인수)) { መልስ("550 Invalid filename\r\n"); return; }
        int ፋይል_መትሓዚ = pk_open(ፋይል_ምእታው_ሽም, ንምንባብ_ጥራይ_ዋጋ, 0); if (ፋይል_መትሓዚ < 0) { መልስ("550 File unavailable\r\n"); return; }
        int መጠን = pk_size(ፋይል_መትሓዚ); pk_close(ፋይል_መትሓዚ); char 응답자료[32] = "213 "; unsigned 개수 = 4;
        수치(መጠን, 응답자료, &개수); 응답자료[개수++] = '\r'; 응답자료[개수++] = '\n'; 응답자료[개수] = 0; መልስ(응답자료);
    } else if (같은지(መስመር, "STOR") || 같은지(መስመር, "RETR")) {
        if (수행작업) { መልስ("450 Transfer in progress\r\n"); return; }
        if (ብኢድ_ርክብ < 0 && ሓበሬታ < 0) { መልስ("425 Use PASV or EPSV\r\n"); return; }
        if (!መገዲ(부가인수)) { መልስ("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(መስመር, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(ምስጋር_ሽም, ፋይል_ምእታው_ሽም, strlen(ፋይል_ምእታው_ሽም) + 1);
        if (수행작업 == 2) {
            int ፋይል_መትሓዚ = pk_open(ፋይል_ምእታው_ሽም, ንምንባብ_ጥራይ_ዋጋ, 0);
            if (ፋይል_መትሓዚ < 0) { 수행작업 = 0; መልስ("550 File unavailable\r\n"); return; }
            int 개수 = pk_read(ፋይል_መትሓዚ, ምስጋር_ደረጃ, sizeof(ምስጋር_ደረጃ)); pk_close(ፋይል_መትሓዚ);
            if (개수 < 0) { 수행작업 = 0; መልስ("451 Read failed\r\n"); return; } 사용량 = 개수;
        }
        መልስ("150 Opening binary data connection\r\n");
    } else መልስ("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (수신창구 < 0) return;
    int 들어온연결 = 망연결받기(수신창구);
    if (들어온연결 >= 0) {
        if (ቁጽጽር >= 0) { 통신쓰기(들어온연결, "421 One session at a time\r\n", 27); ዕጸው_ማሕበራዊ_ኔትወርክ(들어온연결); }
        else { ቁጽጽር = 들어온연결; ተግባር = 보드밀리초(); መልስ("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (ቁጽጽር < 0) return;
    if ((uint32_t)(보드밀리초() - ተግባር) > 60000) { ብተኽ(); return; }
    if (!끝내기) for (unsigned 처리한도 = 0; 처리한도 < 256; 처리한도++) {
        unsigned char ኮድ_ፊደል; int 반환값 = 통신읽기(ቁጽጽር, &ኮድ_ፊደል, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { ብተኽ(); return; } ተግባር = 보드밀리초();
        if (ኮድ_ፊደል == '\n') { if (줄오류) መልስ("500 Command too long or invalid\r\n"); else ትእዛዝ(); መስመር_መጠን = 줄오류 = 0; if (끝내기) break; }
        else if (ኮድ_ፊደል != '\r') { if (!ኮድ_ፊደል || መስመር_መጠን >= sizeof(መስመር) - 1) 줄오류 = 1; else መስመር[መስመር_መጠን++] = ኮድ_ፊደል; }
    }
    if (ብኢድ_ርክብ >= 0 && ሓበሬታ < 0) {
        int 반환값 = 망연결받기(ብኢድ_ርክብ);
        if (반환값 >= 0) {
            if (상대통신주소(반환값) != 상대통신주소(ቁጽጽር)) ዕጸው_ማሕበራዊ_ኔትወርክ(반환값);
            else { ሓበሬታ = 반환값; ዕጸው_ማሕበራዊ_ኔትወርክ(ብኢድ_ርክብ); ብኢድ_ርክብ = -1; ተግባር = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && ሓበሬታ >= 0) for (unsigned 처리한도 = 0; 처리한도 < 8; 처리한도++) {
        unsigned char ሓበሬታ_ምዕጋት[512]; int 개수 = 통신읽기(ሓበሬታ, ሓበሬታ_ምዕጋት, sizeof(ሓበሬታ_ምዕጋት));
        if (개수 == -11) break;
        if (개수 < 0) { ኣቑም_ምስጋር(); መልስ("426 Data connection failed\r\n"); break; }
        ተግባር = 보드밀리초();
        if (개수 == 0) {
            int 결과 = -1;
            if (!실패여부) {
                int ፋይል_መትሓዚ = pk_open(ምስጋር_ሽም, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (ፋይል_መትሓዚ >= 0) { 결과 = pk_write(ፋይል_መትሓዚ, ምስጋር_ደረጃ, 사용량); pk_close(ፋይል_መትሓዚ); }
            }
            int 성공여부 = !실패여부 && 결과 == (int)사용량; ኣቑም_ምስጋር(); መልስ(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)개수 > sizeof(ምስጋር_ደረጃ) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(ምስጋር_ደረጃ + 사용량, ሓበሬታ_ምዕጋት, 개수); 사용량 += 개수; }
    }
    if (수행작업 == 2 && ሓበሬታ >= 0) {
        int 개수 = 통신쓰기(ሓበሬታ, ምስጋር_ደረጃ + 보낸수, 사용량 - 보낸수);
        if (개수 >= 0) { 보낸수 += 개수; ተግባር = 보드밀리초(); if (보낸수 == 사용량) { ኣቑም_ምስጋር(); መልስ("226 Transfer complete\r\n"); } }
        else if (개수 != -11) { ኣቑም_ምስጋር(); መልስ("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < መልስ_መጠን) {
        int 개수 = 통신쓰기(ቁጽጽር, 응답모음 + 응답전송량, መልስ_መጠን - 응답전송량);
        if (개수 > 0) 응답전송량 += 개수; else if (개수 != -11) { ብተኽ(); return; }
    }
    if (응답전송량 == መልስ_መጠን) { መልስ_መጠን = 응답전송량 = 0; if (끝내기) ብተኽ(); }
}
