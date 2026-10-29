#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "rrjet_Stivë.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int 수신창구 = -1, kontroll = -1, manual_lidhje = -1, të_dhëna = -1;
static unsigned 로그인됨, përdorues_OK, linjë_ndryshoj_përmasat, 줄오류, mbyll_program, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned replikë_ndryshoj_përmasat, 응답전송량, Tjetër_numri_i_portës;
static uint32_t Aktivitet;
static char linjë[256], 응답모음[2048], skedar_futje_emër[64], transferim_emër[64];
static unsigned char transferim_status[16384];
static int 같은지(const char *첫째값, const char *SECOND_VALUE) { while (*첫째값 && *첫째값 == *SECOND_VALUE) { 첫째값++; SECOND_VALUE++; } return *첫째값 == *SECOND_VALUE; }
static void replikë(const char *varg_të_dhëna) {
    size_t njësi_COUNT = strlen(varg_të_dhëna);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, replikë_ndryshoj_përmasat - 응답전송량); replikë_ndryshoj_përmasat -= 응답전송량; 응답전송량 = 0; }
    if (njësi_COUNT > sizeof(응답모음) - replikë_ndryshoj_përmasat) { mbyll_program = 1; return; }
    memcpy(응답모음 + replikë_ndryshoj_përmasat, varg_të_dhëna, njësi_COUNT); replikë_ndryshoj_përmasat += njësi_COUNT;
}
static void 수치(unsigned VALUE, char *llogaritje_të_dhëna, unsigned *njësi_COUNT) {
    char shifër_COUNT[10]; unsigned futje_COUNT = 0;
    do { shifër_COUNT[futje_COUNT++] = '0' + VALUE % 10; VALUE /= 10; } while (VALUE);
    while (futje_COUNT) llogaritje_të_dhëna[(*njësi_COUNT)++] = shifër_COUNT[--futje_COUNT];
}
static void Ndal_transferim(void) {
    if (të_dhëna >= 0) mbyll_rrjet(të_dhëna); if (manual_lidhje >= 0) mbyll_rrjet(manual_lidhje);
    të_dhëna = manual_lidhje = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void shkëput(void) {
    Ndal_transferim(); if (kontroll >= 0) mbyll_rrjet(kontroll); kontroll = -1;
    로그인됨 = përdorues_OK = linjë_ndryshoj_përmasat = 줄오류 = replikë_ndryshoj_përmasat = 응답전송량 = mbyll_program = 0;
}
int skedar_transferim_kontroll(int Veprim) {
    if (Veprim == 2) return 수신창구 >= 0;
    if (Veprim == 0) { shkëput(); if (수신창구 >= 0) mbyll_rrjet(수신창구); 수신창구 = -1; return 0; }
    if (Veprim != 1) return -22; if (수신창구 >= 0) return 0;
    수신창구 = 통신끝점만들기(1); if (수신창구 < 0) return 수신창구;
    int 반환값 = 망주소묶기(수신창구, 망상태읽기(0,0), 21); if (!반환값) 반환값 = 연결기다리기(수신창구);
    if (반환값 < 0) { mbyll_rrjet(수신창구); 수신창구 = -1; } return 반환값;
}
static int POZICIONI(const char *Emër) {
    unsigned njësi_COUNT = 0; if (*Emër == '/') Emër++;
    if (!*Emër || 같은지(Emër, ".") || 같은지(Emër, "..")) return 0;
    skedar_futje_emër[njësi_COUNT++] = '/';
    while (*Emër) {
        unsigned char kodi_i_karakterit = *Emër++;
        if (njësi_COUNT >= 63 || kodi_i_karakterit < 32 || kodi_i_karakterit == 127 || kodi_i_karakterit == '/' || kodi_i_karakterit == '\\') return 0;
        skedar_futje_emër[njësi_COUNT++] = kodi_i_karakterit;
    }
    skedar_futje_emër[njësi_COUNT] = 0; return 1;
}
static void dërgoj_Listë(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int njësi_COUNT = 자바파일항목길이(순번); if (njësi_COUNT <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned futje_COUNT = strlen(앞부분); memcpy(transferim_status + 사용량, 앞부분, futje_COUNT); 사용량 += futje_COUNT;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)transferim_status, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        futje_COUNT = strlen(뒷부분); memcpy(transferim_status + 사용량, 뒷부분, futje_COUNT); 사용량 += futje_COUNT;
        for (int 안쪽순번 = 0; 안쪽순번 < njësi_COUNT; 안쪽순번++) transferim_status[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        transferim_status[사용량++] = '\r'; transferim_status[사용량++] = '\n';
    }
}
static void Përgatit_manual_lidhje(int 확장여부) {
    if (수행작업) { replikë("450 Transfer in progress\r\n"); return; }
    Ndal_transferim(); manual_lidhje = 통신끝점만들기(1);
    if (manual_lidhje >= 0) 통신주소재사용(manual_lidhje);
    unsigned numri_i_portës = 50000 + Tjetër_numri_i_portës++ % 8;
    if (manual_lidhje < 0 || 망주소묶기(manual_lidhje, 망상태읽기(0,0), numri_i_portës) || 연결기다리기(manual_lidhje)) {
        Ndal_transferim(); replikë("425 Cannot open passive listener\r\n"); return;
    }
    char përgjigje[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned njësi_COUNT = strlen(앞부분); memcpy(përgjigje, 앞부분, njësi_COUNT);
    if (확장여부) { 수치(numri_i_portës, përgjigje, &njësi_COUNT); përgjigje[njësi_COUNT++] = '|'; }
    else {
        uint32_t email=망상태읽기(0,0);
        for (int pozicioni_INDEX=24;pozicioni_INDEX>=0;pozicioni_INDEX-=8) { 수치((email>>pozicioni_INDEX)&255,përgjigje,&njësi_COUNT);përgjigje[njësi_COUNT++]=','; }
        수치(numri_i_portës / 256, përgjigje, &njësi_COUNT); përgjigje[njësi_COUNT++] = ','; 수치(numri_i_portës % 256, përgjigje, &njësi_COUNT);
    }
    përgjigje[njësi_COUNT++] = ')'; përgjigje[njësi_COUNT++] = '\r'; përgjigje[njësi_COUNT++] = '\n'; përgjigje[njësi_COUNT] = 0; replikë(përgjigje);
}
static void Komanda(void) {
    linjë[linjë_ndryshoj_përmasat] = 0;
    char *부가인수 = linjë; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(linjë, "QUIT")) { Ndal_transferim(); replikë("221 Goodbye\r\n"); mbyll_program = 1; return; }
    if (같은지(linjë, "NOOP")) { replikë("200 OK\r\n"); return; }
    if (같은지(linjë, "SYST")) { replikë("215 UNIX Type: L8\r\n"); return; }
    if (같은지(linjë, "FEAT")) { replikë("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(linjë, "USER")) { 로그인됨 = 0; përdorues_OK = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); replikë(përdorues_OK ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(linjë, "PASS")) { 로그인됨 = përdorues_OK; replikë(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { replikë("530 Login first\r\n"); return; }
    if (같은지(linjë, "PWD")) replikë("257 \"/\"\r\n");
    else if (같은지(linjë, "CWD")) replikë(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(linjë, "TYPE")) replikë(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(linjë, "OPTS")) replikë(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(linjë, "PASV")) Përgatit_manual_lidhje(0);
    else if (같은지(linjë, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) replikë("522 IPv4 only\r\n"); else Përgatit_manual_lidhje(1); }
    else if (같은지(linjë, "ABOR")) { Ndal_transferim(); replikë("226 Transfer aborted\r\n"); }
    else if (같은지(linjë, "DELE")) { replikë(POZICIONI(부가인수) && pk_unlink(skedar_futje_emër) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(linjë, "LIST") || 같은지(linjë, "NLST") || 같은지(linjë, "MLSD")) {
        if (수행작업) { replikë("450 Transfer in progress\r\n"); return; }
        if (manual_lidhje < 0 && të_dhëna < 0) { replikë("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { replikë("550 Root listing only\r\n"); return; }
        dërgoj_Listë(같은지(linjë,"MLSD") ? 2 : 같은지(linjë,"LIST") ? 1 : 0); 수행작업 = 2;
        replikë("150 Opening directory listing\r\n");
    }
    else if (같은지(linjë, "SIZE")) {
        if (!POZICIONI(부가인수)) { replikë("550 Invalid filename\r\n"); return; }
        int skedar_dorezë = pk_open(skedar_futje_emër, vetëm_për_lexim_VALUE, 0); if (skedar_dorezë < 0) { replikë("550 File unavailable\r\n"); return; }
        int Madhësi = pk_size(skedar_dorezë); pk_close(skedar_dorezë); char përgjigje[32] = "213 "; unsigned njësi_COUNT = 4;
        수치(Madhësi, përgjigje, &njësi_COUNT); përgjigje[njësi_COUNT++] = '\r'; përgjigje[njësi_COUNT++] = '\n'; përgjigje[njësi_COUNT] = 0; replikë(përgjigje);
    } else if (같은지(linjë, "STOR") || 같은지(linjë, "RETR")) {
        if (수행작업) { replikë("450 Transfer in progress\r\n"); return; }
        if (manual_lidhje < 0 && të_dhëna < 0) { replikë("425 Use PASV or EPSV\r\n"); return; }
        if (!POZICIONI(부가인수)) { replikë("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(linjë, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(transferim_emër, skedar_futje_emër, strlen(skedar_futje_emër) + 1);
        if (수행작업 == 2) {
            int skedar_dorezë = pk_open(skedar_futje_emër, vetëm_për_lexim_VALUE, 0);
            if (skedar_dorezë < 0) { 수행작업 = 0; replikë("550 File unavailable\r\n"); return; }
            int njësi_COUNT = pk_read(skedar_dorezë, transferim_status, sizeof(transferim_status)); pk_close(skedar_dorezë);
            if (njësi_COUNT < 0) { 수행작업 = 0; replikë("451 Read failed\r\n"); return; } 사용량 = njësi_COUNT;
        }
        replikë("150 Opening binary data connection\r\n");
    } else replikë("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (수신창구 < 0) return;
    int Hyrëse_lidhje = 망연결받기(수신창구);
    if (Hyrëse_lidhje >= 0) {
        if (kontroll >= 0) { 통신쓰기(Hyrëse_lidhje, "421 One session at a time\r\n", 27); mbyll_rrjet(Hyrëse_lidhje); }
        else { kontroll = Hyrëse_lidhje; Aktivitet = 보드밀리초(); replikë("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (kontroll < 0) return;
    if ((uint32_t)(보드밀리초() - Aktivitet) > 60000) { shkëput(); return; }
    if (!mbyll_program) for (unsigned 처리한도 = 0; 처리한도 < 256; 처리한도++) {
        unsigned char kodi_i_karakterit; int 반환값 = 통신읽기(kontroll, &kodi_i_karakterit, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { shkëput(); return; } Aktivitet = 보드밀리초();
        if (kodi_i_karakterit == '\n') { if (줄오류) replikë("500 Command too long or invalid\r\n"); else Komanda(); linjë_ndryshoj_përmasat = 줄오류 = 0; if (mbyll_program) break; }
        else if (kodi_i_karakterit != '\r') { if (!kodi_i_karakterit || linjë_ndryshoj_përmasat >= sizeof(linjë) - 1) 줄오류 = 1; else linjë[linjë_ndryshoj_përmasat++] = kodi_i_karakterit; }
    }
    if (manual_lidhje >= 0 && të_dhëna < 0) {
        int 반환값 = 망연결받기(manual_lidhje);
        if (반환값 >= 0) {
            if (상대통신주소(반환값) != 상대통신주소(kontroll)) mbyll_rrjet(반환값);
            else { të_dhëna = 반환값; mbyll_rrjet(manual_lidhje); manual_lidhje = -1; Aktivitet = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && të_dhëna >= 0) for (unsigned 처리한도 = 0; 처리한도 < 8; 처리한도++) {
        unsigned char të_dhëna_bllokoj[512]; int njësi_COUNT = 통신읽기(të_dhëna, të_dhëna_bllokoj, sizeof(të_dhëna_bllokoj));
        if (njësi_COUNT == -11) break;
        if (njësi_COUNT < 0) { Ndal_transferim(); replikë("426 Data connection failed\r\n"); break; }
        Aktivitet = 보드밀리초();
        if (njësi_COUNT == 0) {
            int llogaritje = -1;
            if (!실패여부) {
                int skedar_dorezë = pk_open(transferim_emër, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (skedar_dorezë >= 0) { llogaritje = pk_write(skedar_dorezë, transferim_status, 사용량); pk_close(skedar_dorezë); }
            }
            int 성공여부 = !실패여부 && llogaritje == (int)사용량; Ndal_transferim(); replikë(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)njësi_COUNT > sizeof(transferim_status) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(transferim_status + 사용량, të_dhëna_bllokoj, njësi_COUNT); 사용량 += njësi_COUNT; }
    }
    if (수행작업 == 2 && të_dhëna >= 0) {
        int njësi_COUNT = 통신쓰기(të_dhëna, transferim_status + 보낸수, 사용량 - 보낸수);
        if (njësi_COUNT >= 0) { 보낸수 += njësi_COUNT; Aktivitet = 보드밀리초(); if (보낸수 == 사용량) { Ndal_transferim(); replikë("226 Transfer complete\r\n"); } }
        else if (njësi_COUNT != -11) { Ndal_transferim(); replikë("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < replikë_ndryshoj_përmasat) {
        int njësi_COUNT = 통신쓰기(kontroll, 응답모음 + 응답전송량, replikë_ndryshoj_përmasat - 응답전송량);
        if (njësi_COUNT > 0) 응답전송량 += njësi_COUNT; else if (njësi_COUNT != -11) { shkëput(); return; }
    }
    if (응답전송량 == replikë_ndryshoj_përmasat) { replikë_ndryshoj_përmasat = 응답전송량 = 0; if (mbyll_program) shkëput(); }
}
