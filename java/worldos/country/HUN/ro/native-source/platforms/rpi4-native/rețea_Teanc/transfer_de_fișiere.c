#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "rețea_Teanc.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int primi_muta = -1, control = -1, manual_conexiune = -1, date = -1;
static unsigned 로그인됨, utilizator_OK, linie_dimensiona, 줄오류, ieșire_program, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned replică_dimensiona, 응답전송량, Următorul_număr_port;
static uint32_t Activitate;
static char Linie[256], 응답모음[2048], Fișier_intrare_nume[64], Transfer_nume[64];
static unsigned char Transfer_Stare[16384];
static int 같은지(const char *첫째값, const char *SECOND_VALUE) { while (*첫째값 && *첫째값 == *SECOND_VALUE) { 첫째값++; SECOND_VALUE++; } return *첫째값 == *SECOND_VALUE; }
static void replică(const char *șir_date) {
    size_t element_COUNT = strlen(șir_date);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, replică_dimensiona - 응답전송량); replică_dimensiona -= 응답전송량; 응답전송량 = 0; }
    if (element_COUNT > sizeof(응답모음) - replică_dimensiona) { ieșire_program = 1; return; }
    memcpy(응답모음 + replică_dimensiona, șir_date, element_COUNT); replică_dimensiona += element_COUNT;
}
static void 수치(unsigned VALUE, char *KR_date, unsigned *element_COUNT) {
    char cifră_COUNT[10]; unsigned intrare_COUNT = 0;
    do { cifră_COUNT[intrare_COUNT++] = '0' + VALUE % 10; VALUE /= 10; } while (VALUE);
    while (intrare_COUNT) KR_date[(*element_COUNT)++] = cifră_COUNT[--intrare_COUNT];
}
static void Stop_Transfer(void) {
    if (date >= 0) închide_rețea(date); if (manual_conexiune >= 0) închide_rețea(manual_conexiune);
    date = manual_conexiune = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void deconecta(void) {
    Stop_Transfer(); if (control >= 0) închide_rețea(control); control = -1;
    로그인됨 = utilizator_OK = linie_dimensiona = 줄오류 = replică_dimensiona = 응답전송량 = ieșire_program = 0;
}
int transfer_de_fișiere_control(int Acțiuni) {
    if (Acțiuni == 2) return primi_muta >= 0;
    if (Acțiuni == 0) { deconecta(); if (primi_muta >= 0) închide_rețea(primi_muta); primi_muta = -1; return 0; }
    if (Acțiuni != 1) return -22; if (primi_muta >= 0) return 0;
    primi_muta = 통신끝점만들기(1); if (primi_muta < 0) return primi_muta;
    int 반환값 = NET_BIND(primi_muta, 망상태읽기(0,0), 21); if (!반환값) 반환값 = NET_asculta(primi_muta);
    if (반환값 < 0) { închide_rețea(primi_muta); primi_muta = -1; } return 반환값;
}
static int Cale(const char *Nume) {
    unsigned element_COUNT = 0; if (*Nume == '/') Nume++;
    if (!*Nume || 같은지(Nume, ".") || 같은지(Nume, "..")) return 0;
    Fișier_intrare_nume[element_COUNT++] = '/';
    while (*Nume) {
        unsigned char cod_caracter = *Nume++;
        if (element_COUNT >= 63 || cod_caracter < 32 || cod_caracter == 127 || cod_caracter == '/' || cod_caracter == '\\') return 0;
        Fișier_intrare_nume[element_COUNT++] = cod_caracter;
    }
    Fișier_intrare_nume[element_COUNT] = 0; return 1;
}
static void trimite_Listă(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int element_COUNT = 자바파일항목길이(순번); if (element_COUNT <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned intrare_COUNT = strlen(앞부분); memcpy(Transfer_Stare + 사용량, 앞부분, intrare_COUNT); 사용량 += intrare_COUNT;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)Transfer_Stare, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        intrare_COUNT = strlen(뒷부분); memcpy(Transfer_Stare + 사용량, 뒷부분, intrare_COUNT); 사용량 += intrare_COUNT;
        for (int 안쪽순번 = 0; 안쪽순번 < element_COUNT; 안쪽순번++) Transfer_Stare[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        Transfer_Stare[사용량++] = '\r'; Transfer_Stare[사용량++] = '\n';
    }
}
static void Pregătiți_manual_conexiune(int 확장여부) {
    if (수행작업) { replică("450 Transfer in progress\r\n"); return; }
    Stop_Transfer(); manual_conexiune = 통신끝점만들기(1);
    if (manual_conexiune >= 0) 통신주소재사용(manual_conexiune);
    unsigned număr_port = 50000 + Următorul_număr_port++ % 8;
    if (manual_conexiune < 0 || NET_BIND(manual_conexiune, 망상태읽기(0,0), număr_port) || NET_asculta(manual_conexiune)) {
        Stop_Transfer(); replică("425 Cannot open passive listener\r\n"); return;
    }
    char răspuns[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned element_COUNT = strlen(앞부분); memcpy(răspuns, 앞부분, element_COUNT);
    if (확장여부) { 수치(număr_port, răspuns, &element_COUNT); răspuns[element_COUNT++] = '|'; }
    else {
        uint32_t adresa=망상태읽기(0,0);
        for (int index_de_poziție=24;index_de_poziție>=0;index_de_poziție-=8) { 수치((adresa>>index_de_poziție)&255,răspuns,&element_COUNT);răspuns[element_COUNT++]=','; }
        수치(număr_port / 256, răspuns, &element_COUNT); răspuns[element_COUNT++] = ','; 수치(număr_port % 256, răspuns, &element_COUNT);
    }
    răspuns[element_COUNT++] = ')'; răspuns[element_COUNT++] = '\r'; răspuns[element_COUNT++] = '\n'; răspuns[element_COUNT] = 0; replică(răspuns);
}
static void Comandă(void) {
    Linie[linie_dimensiona] = 0;
    char *부가인수 = Linie; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(Linie, "QUIT")) { Stop_Transfer(); replică("221 Goodbye\r\n"); ieșire_program = 1; return; }
    if (같은지(Linie, "NOOP")) { replică("200 OK\r\n"); return; }
    if (같은지(Linie, "SYST")) { replică("215 UNIX Type: L8\r\n"); return; }
    if (같은지(Linie, "FEAT")) { replică("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(Linie, "USER")) { 로그인됨 = 0; utilizator_OK = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); replică(utilizator_OK ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(Linie, "PASS")) { 로그인됨 = utilizator_OK; replică(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { replică("530 Login first\r\n"); return; }
    if (같은지(Linie, "PWD")) replică("257 \"/\"\r\n");
    else if (같은지(Linie, "CWD")) replică(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(Linie, "TYPE")) replică(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(Linie, "OPTS")) replică(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(Linie, "PASV")) Pregătiți_manual_conexiune(0);
    else if (같은지(Linie, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) replică("522 IPv4 only\r\n"); else Pregătiți_manual_conexiune(1); }
    else if (같은지(Linie, "ABOR")) { Stop_Transfer(); replică("226 Transfer aborted\r\n"); }
    else if (같은지(Linie, "DELE")) { replică(Cale(부가인수) && pk_unlink(Fișier_intrare_nume) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(Linie, "LIST") || 같은지(Linie, "NLST") || 같은지(Linie, "MLSD")) {
        if (수행작업) { replică("450 Transfer in progress\r\n"); return; }
        if (manual_conexiune < 0 && date < 0) { replică("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { replică("550 Root listing only\r\n"); return; }
        trimite_Listă(같은지(Linie,"MLSD") ? 2 : 같은지(Linie,"LIST") ? 1 : 0); 수행작업 = 2;
        replică("150 Opening directory listing\r\n");
    }
    else if (같은지(Linie, "SIZE")) {
        if (!Cale(부가인수)) { replică("550 Invalid filename\r\n"); return; }
        int Fișier_handle = pk_open(Fișier_intrare_nume, doar_în_citire_VALUE, 0); if (Fișier_handle < 0) { replică("550 File unavailable\r\n"); return; }
        int Mărime = pk_size(Fișier_handle); pk_close(Fișier_handle); char răspuns[32] = "213 "; unsigned element_COUNT = 4;
        수치(Mărime, răspuns, &element_COUNT); răspuns[element_COUNT++] = '\r'; răspuns[element_COUNT++] = '\n'; răspuns[element_COUNT] = 0; replică(răspuns);
    } else if (같은지(Linie, "STOR") || 같은지(Linie, "RETR")) {
        if (수행작업) { replică("450 Transfer in progress\r\n"); return; }
        if (manual_conexiune < 0 && date < 0) { replică("425 Use PASV or EPSV\r\n"); return; }
        if (!Cale(부가인수)) { replică("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(Linie, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(Transfer_nume, Fișier_intrare_nume, strlen(Fișier_intrare_nume) + 1);
        if (수행작업 == 2) {
            int Fișier_handle = pk_open(Fișier_intrare_nume, doar_în_citire_VALUE, 0);
            if (Fișier_handle < 0) { 수행작업 = 0; replică("550 File unavailable\r\n"); return; }
            int element_COUNT = pk_read(Fișier_handle, Transfer_Stare, sizeof(Transfer_Stare)); pk_close(Fișier_handle);
            if (element_COUNT < 0) { 수행작업 = 0; replică("451 Read failed\r\n"); return; } 사용량 = element_COUNT;
        }
        replică("150 Opening binary data connection\r\n");
    } else replică("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (primi_muta < 0) return;
    int Primit_conexiune = NET_accepta(primi_muta);
    if (Primit_conexiune >= 0) {
        if (control >= 0) { NET_scriere(Primit_conexiune, "421 One session at a time\r\n", 27); închide_rețea(Primit_conexiune); }
        else { control = Primit_conexiune; Activitate = 보드밀리초(); replică("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (control < 0) return;
    if ((uint32_t)(보드밀리초() - Activitate) > 60000) { deconecta(); return; }
    if (!ieșire_program) for (unsigned buget = 0; buget < 256; buget++) {
        unsigned char cod_caracter; int 반환값 = 통신읽기(control, &cod_caracter, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { deconecta(); return; } Activitate = 보드밀리초();
        if (cod_caracter == '\n') { if (줄오류) replică("500 Command too long or invalid\r\n"); else Comandă(); linie_dimensiona = 줄오류 = 0; if (ieșire_program) break; }
        else if (cod_caracter != '\r') { if (!cod_caracter || linie_dimensiona >= sizeof(Linie) - 1) 줄오류 = 1; else Linie[linie_dimensiona++] = cod_caracter; }
    }
    if (manual_conexiune >= 0 && date < 0) {
        int 반환값 = NET_accepta(manual_conexiune);
        if (반환값 >= 0) {
            if (NET_pereche_adresa(반환값) != NET_pereche_adresa(control)) închide_rețea(반환값);
            else { date = 반환값; închide_rețea(manual_conexiune); manual_conexiune = -1; Activitate = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && date >= 0) for (unsigned buget = 0; buget < 8; buget++) {
        unsigned char bloc_de_date[512]; int element_COUNT = 통신읽기(date, bloc_de_date, sizeof(bloc_de_date));
        if (element_COUNT == -11) break;
        if (element_COUNT < 0) { Stop_Transfer(); replică("426 Data connection failed\r\n"); break; }
        Activitate = 보드밀리초();
        if (element_COUNT == 0) {
            int KR = -1;
            if (!실패여부) {
                int Fișier_handle = pk_open(Transfer_nume, 쓰기전용 | 없으면만들기 | trunchia_TOC, 0600);
                if (Fișier_handle >= 0) { KR = pk_write(Fișier_handle, Transfer_Stare, 사용량); pk_close(Fișier_handle); }
            }
            int 성공여부 = !실패여부 && KR == (int)사용량; Stop_Transfer(); replică(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)element_COUNT > sizeof(Transfer_Stare) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(Transfer_Stare + 사용량, bloc_de_date, element_COUNT); 사용량 += element_COUNT; }
    }
    if (수행작업 == 2 && date >= 0) {
        int element_COUNT = NET_scriere(date, Transfer_Stare + 보낸수, 사용량 - 보낸수);
        if (element_COUNT >= 0) { 보낸수 += element_COUNT; Activitate = 보드밀리초(); if (보낸수 == 사용량) { Stop_Transfer(); replică("226 Transfer complete\r\n"); } }
        else if (element_COUNT != -11) { Stop_Transfer(); replică("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < replică_dimensiona) {
        int element_COUNT = NET_scriere(control, 응답모음 + 응답전송량, replică_dimensiona - 응답전송량);
        if (element_COUNT > 0) 응답전송량 += element_COUNT; else if (element_COUNT != -11) { deconecta(); return; }
    }
    if (응답전송량 == replică_dimensiona) { replică_dimensiona = 응답전송량 = 0; if (ieșire_program) deconecta(); }
}
