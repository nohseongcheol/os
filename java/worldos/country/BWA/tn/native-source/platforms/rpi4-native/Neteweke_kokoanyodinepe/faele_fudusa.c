#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "Neteweke_kokoanyodinepe.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int 수신창구 = -1, taolo = -1, kaela_tiriso_Kgolagano = -1, tshedimosetso = -1;
static unsigned 로그인됨, 사용자확인, Mola_lekanya, 줄오류, 끝내기, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned araba_lekanya, 응답전송량, 다음접속번호;
static uint32_t Tiro;
static char Mola[256], 응답모음[2048], faele_tsenyo_leina[64], fudusa_leina[64];
static unsigned char fudusa_kemo[16384];
static int 같은지(const char *첫째값, const char *둘째값) { while (*첫째값 && *첫째값 == *둘째값) { 첫째값++; 둘째값++; } return *첫째값 == *둘째값; }
static void araba(const char *dikwalwa_tshedimosetso) {
    size_t 개수 = strlen(dikwalwa_tshedimosetso);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, araba_lekanya - 응답전송량); araba_lekanya -= 응답전송량; 응답전송량 = 0; }
    if (개수 > sizeof(응답모음) - araba_lekanya) { 끝내기 = 1; return; }
    memcpy(응답모음 + araba_lekanya, dikwalwa_tshedimosetso, 개수); araba_lekanya += 개수;
}
static void 수치(unsigned Boleng, char *결과자료, unsigned *개수) {
    char 숫자수[10]; unsigned 항목수 = 0;
    do { 숫자수[항목수++] = '0' + Boleng % 10; Boleng /= 10; } while (Boleng);
    while (항목수) 결과자료[(*개수)++] = 숫자수[--항목수];
}
static void emisa_fudusa(void) {
    if (tshedimosetso >= 0) tswala_Neteweke(tshedimosetso); if (kaela_tiriso_Kgolagano >= 0) tswala_Neteweke(kaela_tiriso_Kgolagano);
    tshedimosetso = kaela_tiriso_Kgolagano = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void gokaganyolola(void) {
    emisa_fudusa(); if (taolo >= 0) tswala_Neteweke(taolo); taolo = -1;
    로그인됨 = 사용자확인 = Mola_lekanya = 줄오류 = araba_lekanya = 응답전송량 = 끝내기 = 0;
}
int faele_fudusa_taolo(int tiro) {
    if (tiro == 2) return 수신창구 >= 0;
    if (tiro == 0) { gokaganyolola(); if (수신창구 >= 0) tswala_Neteweke(수신창구); 수신창구 = -1; return 0; }
    if (tiro != 1) return -22; if (수신창구 >= 0) return 0;
    수신창구 = 통신끝점만들기(1); if (수신창구 < 0) return 수신창구;
    int 반환값 = 망주소묶기(수신창구, 망상태읽기(0,0), 21); if (!반환값) 반환값 = 연결기다리기(수신창구);
    if (반환값 < 0) { tswala_Neteweke(수신창구); 수신창구 = -1; } return 반환값;
}
static int tsela(const char *leina) {
    unsigned 개수 = 0; if (*leina == '/') leina++;
    if (!*leina || 같은지(leina, ".") || 같은지(leina, "..")) return 0;
    faele_tsenyo_leina[개수++] = '/';
    while (*leina) {
        unsigned char khoutuletshwao = *leina++;
        if (개수 >= 63 || khoutuletshwao < 32 || khoutuletshwao == 127 || khoutuletshwao == '/' || khoutuletshwao == '\\') return 0;
        faele_tsenyo_leina[개수++] = khoutuletshwao;
    }
    faele_tsenyo_leina[개수] = 0; return 1;
}
static void romela_lenaane(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int 개수 = 자바파일항목길이(순번); if (개수 <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned 항목수 = strlen(앞부분); memcpy(fudusa_kemo + 사용량, 앞부분, 항목수); 사용량 += 항목수;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)fudusa_kemo, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        항목수 = strlen(뒷부분); memcpy(fudusa_kemo + 사용량, 뒷부분, 항목수); 사용량 += 항목수;
        for (int 안쪽순번 = 0; 안쪽순번 < 개수; 안쪽순번++) fudusa_kemo[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        fudusa_kemo[사용량++] = '\r'; fudusa_kemo[사용량++] = '\n';
    }
}
static void Baakanya_kaela_tiriso_Kgolagano(int 확장여부) {
    if (수행작업) { araba("450 Transfer in progress\r\n"); return; }
    emisa_fudusa(); kaela_tiriso_Kgolagano = 통신끝점만들기(1);
    if (kaela_tiriso_Kgolagano >= 0) 통신주소재사용(kaela_tiriso_Kgolagano);
    unsigned 접속번호 = 50000 + 다음접속번호++ % 8;
    if (kaela_tiriso_Kgolagano < 0 || 망주소묶기(kaela_tiriso_Kgolagano, 망상태읽기(0,0), 접속번호) || 연결기다리기(kaela_tiriso_Kgolagano)) {
        emisa_fudusa(); araba("425 Cannot open passive listener\r\n"); return;
    }
    char 응답자료[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned 개수 = strlen(앞부분); memcpy(응답자료, 앞부분, 개수);
    if (확장여부) { 수치(접속번호, 응답자료, &개수); 응답자료[개수++] = '|'; }
    else {
        uint32_t aterese=망상태읽기(0,0);
        for (int 자리=24;자리>=0;자리-=8) { 수치((aterese>>자리)&255,응답자료,&개수);응답자료[개수++]=','; }
        수치(접속번호 / 256, 응답자료, &개수); 응답자료[개수++] = ','; 수치(접속번호 % 256, 응답자료, &개수);
    }
    응답자료[개수++] = ')'; 응답자료[개수++] = '\r'; 응답자료[개수++] = '\n'; 응답자료[개수] = 0; araba(응답자료);
}
static void Taelo(void) {
    Mola[Mola_lekanya] = 0;
    char *부가인수 = Mola; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(Mola, "QUIT")) { emisa_fudusa(); araba("221 Goodbye\r\n"); 끝내기 = 1; return; }
    if (같은지(Mola, "NOOP")) { araba("200 OK\r\n"); return; }
    if (같은지(Mola, "SYST")) { araba("215 UNIX Type: L8\r\n"); return; }
    if (같은지(Mola, "FEAT")) { araba("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(Mola, "USER")) { 로그인됨 = 0; 사용자확인 = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); araba(사용자확인 ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(Mola, "PASS")) { 로그인됨 = 사용자확인; araba(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { araba("530 Login first\r\n"); return; }
    if (같은지(Mola, "PWD")) araba("257 \"/\"\r\n");
    else if (같은지(Mola, "CWD")) araba(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(Mola, "TYPE")) araba(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(Mola, "OPTS")) araba(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(Mola, "PASV")) Baakanya_kaela_tiriso_Kgolagano(0);
    else if (같은지(Mola, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) araba("522 IPv4 only\r\n"); else Baakanya_kaela_tiriso_Kgolagano(1); }
    else if (같은지(Mola, "ABOR")) { emisa_fudusa(); araba("226 Transfer aborted\r\n"); }
    else if (같은지(Mola, "DELE")) { araba(tsela(부가인수) && pk_unlink(faele_tsenyo_leina) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(Mola, "LIST") || 같은지(Mola, "NLST") || 같은지(Mola, "MLSD")) {
        if (수행작업) { araba("450 Transfer in progress\r\n"); return; }
        if (kaela_tiriso_Kgolagano < 0 && tshedimosetso < 0) { araba("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { araba("550 Root listing only\r\n"); return; }
        romela_lenaane(같은지(Mola,"MLSD") ? 2 : 같은지(Mola,"LIST") ? 1 : 0); 수행작업 = 2;
        araba("150 Opening directory listing\r\n");
    }
    else if (같은지(Mola, "SIZE")) {
        if (!tsela(부가인수)) { araba("550 Invalid filename\r\n"); return; }
        int faele_mokgwakamogelo = pk_open(faele_tsenyo_leina, puiso_fela_Boleng, 0); if (faele_mokgwakamogelo < 0) { araba("550 File unavailable\r\n"); return; }
        int lekanya = pk_size(faele_mokgwakamogelo); pk_close(faele_mokgwakamogelo); char 응답자료[32] = "213 "; unsigned 개수 = 4;
        수치(lekanya, 응답자료, &개수); 응답자료[개수++] = '\r'; 응답자료[개수++] = '\n'; 응답자료[개수] = 0; araba(응답자료);
    } else if (같은지(Mola, "STOR") || 같은지(Mola, "RETR")) {
        if (수행작업) { araba("450 Transfer in progress\r\n"); return; }
        if (kaela_tiriso_Kgolagano < 0 && tshedimosetso < 0) { araba("425 Use PASV or EPSV\r\n"); return; }
        if (!tsela(부가인수)) { araba("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(Mola, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(fudusa_leina, faele_tsenyo_leina, strlen(faele_tsenyo_leina) + 1);
        if (수행작업 == 2) {
            int faele_mokgwakamogelo = pk_open(faele_tsenyo_leina, puiso_fela_Boleng, 0);
            if (faele_mokgwakamogelo < 0) { 수행작업 = 0; araba("550 File unavailable\r\n"); return; }
            int 개수 = pk_read(faele_mokgwakamogelo, fudusa_kemo, sizeof(fudusa_kemo)); pk_close(faele_mokgwakamogelo);
            if (개수 < 0) { 수행작업 = 0; araba("451 Read failed\r\n"); return; } 사용량 = 개수;
        }
        araba("150 Opening binary data connection\r\n");
    } else araba("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (수신창구 < 0) return;
    int 들어온연결 = 망연결받기(수신창구);
    if (들어온연결 >= 0) {
        if (taolo >= 0) { 통신쓰기(들어온연결, "421 One session at a time\r\n", 27); tswala_Neteweke(들어온연결); }
        else { taolo = 들어온연결; Tiro = 보드밀리초(); araba("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (taolo < 0) return;
    if ((uint32_t)(보드밀리초() - Tiro) > 60000) { gokaganyolola(); return; }
    if (!끝내기) for (unsigned 처리한도 = 0; 처리한도 < 256; 처리한도++) {
        unsigned char khoutuletshwao; int 반환값 = 통신읽기(taolo, &khoutuletshwao, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { gokaganyolola(); return; } Tiro = 보드밀리초();
        if (khoutuletshwao == '\n') { if (줄오류) araba("500 Command too long or invalid\r\n"); else Taelo(); Mola_lekanya = 줄오류 = 0; if (끝내기) break; }
        else if (khoutuletshwao != '\r') { if (!khoutuletshwao || Mola_lekanya >= sizeof(Mola) - 1) 줄오류 = 1; else Mola[Mola_lekanya++] = khoutuletshwao; }
    }
    if (kaela_tiriso_Kgolagano >= 0 && tshedimosetso < 0) {
        int 반환값 = 망연결받기(kaela_tiriso_Kgolagano);
        if (반환값 >= 0) {
            if (상대통신주소(반환값) != 상대통신주소(taolo)) tswala_Neteweke(반환값);
            else { tshedimosetso = 반환값; tswala_Neteweke(kaela_tiriso_Kgolagano); kaela_tiriso_Kgolagano = -1; Tiro = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && tshedimosetso >= 0) for (unsigned 처리한도 = 0; 처리한도 < 8; 처리한도++) {
        unsigned char tshedimosetso_thibela[512]; int 개수 = 통신읽기(tshedimosetso, tshedimosetso_thibela, sizeof(tshedimosetso_thibela));
        if (개수 == -11) break;
        if (개수 < 0) { emisa_fudusa(); araba("426 Data connection failed\r\n"); break; }
        Tiro = 보드밀리초();
        if (개수 == 0) {
            int 결과 = -1;
            if (!실패여부) {
                int faele_mokgwakamogelo = pk_open(fudusa_leina, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (faele_mokgwakamogelo >= 0) { 결과 = pk_write(faele_mokgwakamogelo, fudusa_kemo, 사용량); pk_close(faele_mokgwakamogelo); }
            }
            int 성공여부 = !실패여부 && 결과 == (int)사용량; emisa_fudusa(); araba(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)개수 > sizeof(fudusa_kemo) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(fudusa_kemo + 사용량, tshedimosetso_thibela, 개수); 사용량 += 개수; }
    }
    if (수행작업 == 2 && tshedimosetso >= 0) {
        int 개수 = 통신쓰기(tshedimosetso, fudusa_kemo + 보낸수, 사용량 - 보낸수);
        if (개수 >= 0) { 보낸수 += 개수; Tiro = 보드밀리초(); if (보낸수 == 사용량) { emisa_fudusa(); araba("226 Transfer complete\r\n"); } }
        else if (개수 != -11) { emisa_fudusa(); araba("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < araba_lekanya) {
        int 개수 = 통신쓰기(taolo, 응답모음 + 응답전송량, araba_lekanya - 응답전송량);
        if (개수 > 0) 응답전송량 += 개수; else if (개수 != -11) { gokaganyolola(); return; }
    }
    if (응답전송량 == araba_lekanya) { araba_lekanya = 응답전송량 = 0; if (끝내기) gokaganyolola(); }
}
