#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "netwerk_Munzell.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int 수신창구 = -1, kontroll = -1, manwali_konnessjoni = -1, data = -1;
static unsigned 로그인됨, utent_OK, linja_daqqas, 줄오류, ħruġ_programm, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned wieġeb_daqqas, 응답전송량, 다음접속번호;
static uint32_t Attività;
static char linja[256], 응답모음[2048], fajl_entrata_isem[64], trasferiment_isem[64];
static unsigned char trasferiment_stat[16384];
static int 같은지(const char *첫째값, const char *SECOND_VALUE) { while (*첫째값 && *첫째값 == *SECOND_VALUE) { 첫째값++; SECOND_VALUE++; } return *첫째값 == *SECOND_VALUE; }
static void wieġeb(const char *string_data) {
    size_t element_COUNT = strlen(string_data);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, wieġeb_daqqas - 응답전송량); wieġeb_daqqas -= 응답전송량; 응답전송량 = 0; }
    if (element_COUNT > sizeof(응답모음) - wieġeb_daqqas) { ħruġ_programm = 1; return; }
    memcpy(응답모음 + wieġeb_daqqas, string_data, element_COUNT); wieġeb_daqqas += element_COUNT;
}
static void 수치(unsigned VALUE, char *miżura_data, unsigned *element_COUNT) {
    char ċifra_COUNT[10]; unsigned entrata_COUNT = 0;
    do { ċifra_COUNT[entrata_COUNT++] = '0' + VALUE % 10; VALUE /= 10; } while (VALUE);
    while (entrata_COUNT) miżura_data[(*element_COUNT)++] = ċifra_COUNT[--entrata_COUNT];
}
static void waqqaf_trasferiment(void) {
    if (data >= 0) agħlaq_netwerk(data); if (manwali_konnessjoni >= 0) agħlaq_netwerk(manwali_konnessjoni);
    data = manwali_konnessjoni = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void skonnettja(void) {
    waqqaf_trasferiment(); if (kontroll >= 0) agħlaq_netwerk(kontroll); kontroll = -1;
    로그인됨 = utent_OK = linja_daqqas = 줄오류 = wieġeb_daqqas = 응답전송량 = ħruġ_programm = 0;
}
int fajl_trasferiment_kontroll(int azzjoni) {
    if (azzjoni == 2) return 수신창구 >= 0;
    if (azzjoni == 0) { skonnettja(); if (수신창구 >= 0) agħlaq_netwerk(수신창구); 수신창구 = -1; return 0; }
    if (azzjoni != 1) return -22; if (수신창구 >= 0) return 0;
    수신창구 = 통신끝점만들기(1); if (수신창구 < 0) return 수신창구;
    int 반환값 = 망주소묶기(수신창구, 망상태읽기(0,0), 21); if (!반환값) 반환값 = 연결기다리기(수신창구);
    if (반환값 < 0) { agħlaq_netwerk(수신창구); 수신창구 = -1; } return 반환값;
}
static int mogħdija(const char *isem) {
    unsigned element_COUNT = 0; if (*isem == '/') isem++;
    if (!*isem || 같은지(isem, ".") || 같은지(isem, "..")) return 0;
    fajl_entrata_isem[element_COUNT++] = '/';
    while (*isem) {
        unsigned char kodiċi_tal_karattru = *isem++;
        if (element_COUNT >= 63 || kodiċi_tal_karattru < 32 || kodiċi_tal_karattru == 127 || kodiċi_tal_karattru == '/' || kodiċi_tal_karattru == '\\') return 0;
        fajl_entrata_isem[element_COUNT++] = kodiċi_tal_karattru;
    }
    fajl_entrata_isem[element_COUNT] = 0; return 1;
}
static void bagħat_Lista(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int element_COUNT = 자바파일항목길이(순번); if (element_COUNT <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned entrata_COUNT = strlen(앞부분); memcpy(trasferiment_stat + 사용량, 앞부분, entrata_COUNT); 사용량 += entrata_COUNT;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)trasferiment_stat, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        entrata_COUNT = strlen(뒷부분); memcpy(trasferiment_stat + 사용량, 뒷부분, entrata_COUNT); 사용량 += entrata_COUNT;
        for (int 안쪽순번 = 0; 안쪽순번 < element_COUNT; 안쪽순번++) trasferiment_stat[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        trasferiment_stat[사용량++] = '\r'; trasferiment_stat[사용량++] = '\n';
    }
}
static void Ħejji_manwali_konnessjoni(int 확장여부) {
    if (수행작업) { wieġeb("450 Transfer in progress\r\n"); return; }
    waqqaf_trasferiment(); manwali_konnessjoni = 통신끝점만들기(1);
    if (manwali_konnessjoni >= 0) 통신주소재사용(manwali_konnessjoni);
    unsigned 접속번호 = 50000 + 다음접속번호++ % 8;
    if (manwali_konnessjoni < 0 || 망주소묶기(manwali_konnessjoni, 망상태읽기(0,0), 접속번호) || 연결기다리기(manwali_konnessjoni)) {
        waqqaf_trasferiment(); wieġeb("425 Cannot open passive listener\r\n"); return;
    }
    char 응답자료[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned element_COUNT = strlen(앞부분); memcpy(응답자료, 앞부분, element_COUNT);
    if (확장여부) { 수치(접속번호, 응답자료, &element_COUNT); 응답자료[element_COUNT++] = '|'; }
    else {
        uint32_t ADDRESS=망상태읽기(0,0);
        for (int pożizzjoni_INDEX=24;pożizzjoni_INDEX>=0;pożizzjoni_INDEX-=8) { 수치((ADDRESS>>pożizzjoni_INDEX)&255,응답자료,&element_COUNT);응답자료[element_COUNT++]=','; }
        수치(접속번호 / 256, 응답자료, &element_COUNT); 응답자료[element_COUNT++] = ','; 수치(접속번호 % 256, 응답자료, &element_COUNT);
    }
    응답자료[element_COUNT++] = ')'; 응답자료[element_COUNT++] = '\r'; 응답자료[element_COUNT++] = '\n'; 응답자료[element_COUNT] = 0; wieġeb(응답자료);
}
static void kmand(void) {
    linja[linja_daqqas] = 0;
    char *부가인수 = linja; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(linja, "QUIT")) { waqqaf_trasferiment(); wieġeb("221 Goodbye\r\n"); ħruġ_programm = 1; return; }
    if (같은지(linja, "NOOP")) { wieġeb("200 OK\r\n"); return; }
    if (같은지(linja, "SYST")) { wieġeb("215 UNIX Type: L8\r\n"); return; }
    if (같은지(linja, "FEAT")) { wieġeb("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(linja, "USER")) { 로그인됨 = 0; utent_OK = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); wieġeb(utent_OK ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(linja, "PASS")) { 로그인됨 = utent_OK; wieġeb(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { wieġeb("530 Login first\r\n"); return; }
    if (같은지(linja, "PWD")) wieġeb("257 \"/\"\r\n");
    else if (같은지(linja, "CWD")) wieġeb(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(linja, "TYPE")) wieġeb(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(linja, "OPTS")) wieġeb(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(linja, "PASV")) Ħejji_manwali_konnessjoni(0);
    else if (같은지(linja, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) wieġeb("522 IPv4 only\r\n"); else Ħejji_manwali_konnessjoni(1); }
    else if (같은지(linja, "ABOR")) { waqqaf_trasferiment(); wieġeb("226 Transfer aborted\r\n"); }
    else if (같은지(linja, "DELE")) { wieġeb(mogħdija(부가인수) && pk_unlink(fajl_entrata_isem) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(linja, "LIST") || 같은지(linja, "NLST") || 같은지(linja, "MLSD")) {
        if (수행작업) { wieġeb("450 Transfer in progress\r\n"); return; }
        if (manwali_konnessjoni < 0 && data < 0) { wieġeb("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { wieġeb("550 Root listing only\r\n"); return; }
        bagħat_Lista(같은지(linja,"MLSD") ? 2 : 같은지(linja,"LIST") ? 1 : 0); 수행작업 = 2;
        wieġeb("150 Opening directory listing\r\n");
    }
    else if (같은지(linja, "SIZE")) {
        if (!mogħdija(부가인수)) { wieġeb("550 Invalid filename\r\n"); return; }
        int fajl_handle = pk_open(fajl_entrata_isem, qari_biss_VALUE, 0); if (fajl_handle < 0) { wieġeb("550 File unavailable\r\n"); return; }
        int daqqas = pk_size(fajl_handle); pk_close(fajl_handle); char 응답자료[32] = "213 "; unsigned element_COUNT = 4;
        수치(daqqas, 응답자료, &element_COUNT); 응답자료[element_COUNT++] = '\r'; 응답자료[element_COUNT++] = '\n'; 응답자료[element_COUNT] = 0; wieġeb(응답자료);
    } else if (같은지(linja, "STOR") || 같은지(linja, "RETR")) {
        if (수행작업) { wieġeb("450 Transfer in progress\r\n"); return; }
        if (manwali_konnessjoni < 0 && data < 0) { wieġeb("425 Use PASV or EPSV\r\n"); return; }
        if (!mogħdija(부가인수)) { wieġeb("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(linja, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(trasferiment_isem, fajl_entrata_isem, strlen(fajl_entrata_isem) + 1);
        if (수행작업 == 2) {
            int fajl_handle = pk_open(fajl_entrata_isem, qari_biss_VALUE, 0);
            if (fajl_handle < 0) { 수행작업 = 0; wieġeb("550 File unavailable\r\n"); return; }
            int element_COUNT = pk_read(fajl_handle, trasferiment_stat, sizeof(trasferiment_stat)); pk_close(fajl_handle);
            if (element_COUNT < 0) { 수행작업 = 0; wieġeb("451 Read failed\r\n"); return; } 사용량 = element_COUNT;
        }
        wieġeb("150 Opening binary data connection\r\n");
    } else wieġeb("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (수신창구 < 0) return;
    int 들어온연결 = 망연결받기(수신창구);
    if (들어온연결 >= 0) {
        if (kontroll >= 0) { 통신쓰기(들어온연결, "421 One session at a time\r\n", 27); agħlaq_netwerk(들어온연결); }
        else { kontroll = 들어온연결; Attività = 보드밀리초(); wieġeb("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (kontroll < 0) return;
    if ((uint32_t)(보드밀리초() - Attività) > 60000) { skonnettja(); return; }
    if (!ħruġ_programm) for (unsigned 처리한도 = 0; 처리한도 < 256; 처리한도++) {
        unsigned char kodiċi_tal_karattru; int 반환값 = 통신읽기(kontroll, &kodiċi_tal_karattru, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { skonnettja(); return; } Attività = 보드밀리초();
        if (kodiċi_tal_karattru == '\n') { if (줄오류) wieġeb("500 Command too long or invalid\r\n"); else kmand(); linja_daqqas = 줄오류 = 0; if (ħruġ_programm) break; }
        else if (kodiċi_tal_karattru != '\r') { if (!kodiċi_tal_karattru || linja_daqqas >= sizeof(linja) - 1) 줄오류 = 1; else linja[linja_daqqas++] = kodiċi_tal_karattru; }
    }
    if (manwali_konnessjoni >= 0 && data < 0) {
        int 반환값 = 망연결받기(manwali_konnessjoni);
        if (반환값 >= 0) {
            if (상대통신주소(반환값) != 상대통신주소(kontroll)) agħlaq_netwerk(반환값);
            else { data = 반환값; agħlaq_netwerk(manwali_konnessjoni); manwali_konnessjoni = -1; Attività = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && data >= 0) for (unsigned 처리한도 = 0; 처리한도 < 8; 처리한도++) {
        unsigned char data_imblokka[512]; int element_COUNT = 통신읽기(data, data_imblokka, sizeof(data_imblokka));
        if (element_COUNT == -11) break;
        if (element_COUNT < 0) { waqqaf_trasferiment(); wieġeb("426 Data connection failed\r\n"); break; }
        Attività = 보드밀리초();
        if (element_COUNT == 0) {
            int miżura = -1;
            if (!실패여부) {
                int fajl_handle = pk_open(trasferiment_isem, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (fajl_handle >= 0) { miżura = pk_write(fajl_handle, trasferiment_stat, 사용량); pk_close(fajl_handle); }
            }
            int 성공여부 = !실패여부 && miżura == (int)사용량; waqqaf_trasferiment(); wieġeb(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)element_COUNT > sizeof(trasferiment_stat) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(trasferiment_stat + 사용량, data_imblokka, element_COUNT); 사용량 += element_COUNT; }
    }
    if (수행작업 == 2 && data >= 0) {
        int element_COUNT = 통신쓰기(data, trasferiment_stat + 보낸수, 사용량 - 보낸수);
        if (element_COUNT >= 0) { 보낸수 += element_COUNT; Attività = 보드밀리초(); if (보낸수 == 사용량) { waqqaf_trasferiment(); wieġeb("226 Transfer complete\r\n"); } }
        else if (element_COUNT != -11) { waqqaf_trasferiment(); wieġeb("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < wieġeb_daqqas) {
        int element_COUNT = 통신쓰기(kontroll, 응답모음 + 응답전송량, wieġeb_daqqas - 응답전송량);
        if (element_COUNT > 0) 응답전송량 += element_COUNT; else if (element_COUNT != -11) { skonnettja(); return; }
    }
    if (응답전송량 == wieġeb_daqqas) { wieġeb_daqqas = 응답전송량 = 0; if (ħruġ_programm) skonnettja(); }
}
