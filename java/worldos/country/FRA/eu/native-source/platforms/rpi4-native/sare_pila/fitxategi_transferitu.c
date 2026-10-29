#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "sare_pila.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int 수신창구 = -1, kontrol = -1, eskuzko_konexio = -1, datuak = -1;
static unsigned 로그인됨, erabiltzaile_Ados, 줄길이, 줄오류, irten_aplik_55b3a1cd, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned 응답크기, 응답전송량, Hurrengoa_ataka_zenbaki;
static uint32_t jarduera;
static char Marra[256], 응답모음[2048], fitxategi_sarrera_izen[64], transferitu_izen[64];
static unsigned char transferitu_Egoera[16384];
static int 같은지(const char *첫째값, const char *SEGUNDOA_balio) { while (*첫째값 && *첫째값 == *SEGUNDOA_balio) { 첫째값++; SEGUNDOA_balio++; } return *첫째값 == *SEGUNDOA_balio; }
static void erantzun(const char *kate_datuak) {
    size_t elementu_ZENBATU = strlen(kate_datuak);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, 응답크기 - 응답전송량); 응답크기 -= 응답전송량; 응답전송량 = 0; }
    if (elementu_ZENBATU > sizeof(응답모음) - 응답크기) { irten_aplik_55b3a1cd = 1; return; }
    memcpy(응답모음 + 응답크기, kate_datuak, elementu_ZENBATU); 응답크기 += elementu_ZENBATU;
}
static void 수치(unsigned balio, char *neurria_datuak, unsigned *elementu_ZENBATU) {
    char digitu_ZENBATU[10]; unsigned sarrera_ZENBATU = 0;
    do { digitu_ZENBATU[sarrera_ZENBATU++] = '0' + balio % 10; balio /= 10; } while (balio);
    while (sarrera_ZENBATU) neurria_datuak[(*elementu_ZENBATU)++] = digitu_ZENBATU[--sarrera_ZENBATU];
}
static void Stop_transferitu(void) {
    if (datuak >= 0) itxi_sare(datuak); if (eskuzko_konexio >= 0) itxi_sare(eskuzko_konexio);
    datuak = eskuzko_konexio = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void deskonektatu(void) {
    Stop_transferitu(); if (kontrol >= 0) itxi_sare(kontrol); kontrol = -1;
    로그인됨 = erabiltzaile_Ados = 줄길이 = 줄오류 = 응답크기 = 응답전송량 = irten_aplik_55b3a1cd = 0;
}
int fitxategi_transferitu_kontrol(int Ekintza) {
    if (Ekintza == 2) return 수신창구 >= 0;
    if (Ekintza == 0) { deskonektatu(); if (수신창구 >= 0) itxi_sare(수신창구); 수신창구 = -1; return 0; }
    if (Ekintza != 1) return -22; if (수신창구 >= 0) return 0;
    수신창구 = 통신끝점만들기(1); if (수신창구 < 0) return 수신창구;
    int 반환값 = 망주소묶기(수신창구, 망상태읽기(0,0), 21); if (!반환값) 반환값 = 연결기다리기(수신창구);
    if (반환값 < 0) { itxi_sare(수신창구); 수신창구 = -1; } return 반환값;
}
static int Bide_izena(const char *Izena) {
    unsigned elementu_ZENBATU = 0; if (*Izena == '/') Izena++;
    if (!*Izena || 같은지(Izena, ".") || 같은지(Izena, "..")) return 0;
    fitxategi_sarrera_izen[elementu_ZENBATU++] = '/';
    while (*Izena) {
        unsigned char karaktere_kode = *Izena++;
        if (elementu_ZENBATU >= 63 || karaktere_kode < 32 || karaktere_kode == 127 || karaktere_kode == '/' || karaktere_kode == '\\') return 0;
        fitxategi_sarrera_izen[elementu_ZENBATU++] = karaktere_kode;
    }
    fitxategi_sarrera_izen[elementu_ZENBATU] = 0; return 1;
}
static void bidali_Zerrenda(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int elementu_ZENBATU = 자바파일항목길이(순번); if (elementu_ZENBATU <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned sarrera_ZENBATU = strlen(앞부분); memcpy(transferitu_Egoera + 사용량, 앞부분, sarrera_ZENBATU); 사용량 += sarrera_ZENBATU;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)transferitu_Egoera, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        sarrera_ZENBATU = strlen(뒷부분); memcpy(transferitu_Egoera + 사용량, 뒷부분, sarrera_ZENBATU); 사용량 += sarrera_ZENBATU;
        for (int 안쪽순번 = 0; 안쪽순번 < elementu_ZENBATU; 안쪽순번++) transferitu_Egoera[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        transferitu_Egoera[사용량++] = '\r'; transferitu_Egoera[사용량++] = '\n';
    }
}
static void 수동연결준비(int 확장여부) {
    if (수행작업) { erantzun("450 Transfer in progress\r\n"); return; }
    Stop_transferitu(); eskuzko_konexio = 통신끝점만들기(1);
    if (eskuzko_konexio >= 0) 통신주소재사용(eskuzko_konexio);
    unsigned ataka_zenbaki = 50000 + Hurrengoa_ataka_zenbaki++ % 8;
    if (eskuzko_konexio < 0 || 망주소묶기(eskuzko_konexio, 망상태읽기(0,0), ataka_zenbaki) || 연결기다리기(eskuzko_konexio)) {
        Stop_transferitu(); erantzun("425 Cannot open passive listener\r\n"); return;
    }
    char erantzun_1262b476[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned elementu_ZENBATU = strlen(앞부분); memcpy(erantzun_1262b476, 앞부분, elementu_ZENBATU);
    if (확장여부) { 수치(ataka_zenbaki, erantzun_1262b476, &elementu_ZENBATU); erantzun_1262b476[elementu_ZENBATU++] = '|'; }
    else {
        uint32_t helbide=망상태읽기(0,0);
        for (int kargu_INDIZE=24;kargu_INDIZE>=0;kargu_INDIZE-=8) { 수치((helbide>>kargu_INDIZE)&255,erantzun_1262b476,&elementu_ZENBATU);erantzun_1262b476[elementu_ZENBATU++]=','; }
        수치(ataka_zenbaki / 256, erantzun_1262b476, &elementu_ZENBATU); erantzun_1262b476[elementu_ZENBATU++] = ','; 수치(ataka_zenbaki % 256, erantzun_1262b476, &elementu_ZENBATU);
    }
    erantzun_1262b476[elementu_ZENBATU++] = ')'; erantzun_1262b476[elementu_ZENBATU++] = '\r'; erantzun_1262b476[elementu_ZENBATU++] = '\n'; erantzun_1262b476[elementu_ZENBATU] = 0; erantzun(erantzun_1262b476);
}
static void Komandoa(void) {
    Marra[줄길이] = 0;
    char *부가인수 = Marra; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(Marra, "QUIT")) { Stop_transferitu(); erantzun("221 Goodbye\r\n"); irten_aplik_55b3a1cd = 1; return; }
    if (같은지(Marra, "NOOP")) { erantzun("200 OK\r\n"); return; }
    if (같은지(Marra, "SYST")) { erantzun("215 UNIX Type: L8\r\n"); return; }
    if (같은지(Marra, "FEAT")) { erantzun("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(Marra, "USER")) { 로그인됨 = 0; erabiltzaile_Ados = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); erantzun(erabiltzaile_Ados ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(Marra, "PASS")) { 로그인됨 = erabiltzaile_Ados; erantzun(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { erantzun("530 Login first\r\n"); return; }
    if (같은지(Marra, "PWD")) erantzun("257 \"/\"\r\n");
    else if (같은지(Marra, "CWD")) erantzun(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(Marra, "TYPE")) erantzun(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(Marra, "OPTS")) erantzun(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(Marra, "PASV")) 수동연결준비(0);
    else if (같은지(Marra, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) erantzun("522 IPv4 only\r\n"); else 수동연결준비(1); }
    else if (같은지(Marra, "ABOR")) { Stop_transferitu(); erantzun("226 Transfer aborted\r\n"); }
    else if (같은지(Marra, "DELE")) { erantzun(Bide_izena(부가인수) && pk_unlink(fitxategi_sarrera_izen) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(Marra, "LIST") || 같은지(Marra, "NLST") || 같은지(Marra, "MLSD")) {
        if (수행작업) { erantzun("450 Transfer in progress\r\n"); return; }
        if (eskuzko_konexio < 0 && datuak < 0) { erantzun("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { erantzun("550 Root listing only\r\n"); return; }
        bidali_Zerrenda(같은지(Marra,"MLSD") ? 2 : 같은지(Marra,"LIST") ? 1 : 0); 수행작업 = 2;
        erantzun("150 Opening directory listing\r\n");
    }
    else if (같은지(Marra, "SIZE")) {
        if (!Bide_izena(부가인수)) { erantzun("550 Invalid filename\r\n"); return; }
        int fitxategi_helduleku = pk_open(fitxategi_sarrera_izen, irakurtzeko_soilik_balio, 0); if (fitxategi_helduleku < 0) { erantzun("550 File unavailable\r\n"); return; }
        int Tamaina = pk_size(fitxategi_helduleku); pk_close(fitxategi_helduleku); char erantzun_1262b476[32] = "213 "; unsigned elementu_ZENBATU = 4;
        수치(Tamaina, erantzun_1262b476, &elementu_ZENBATU); erantzun_1262b476[elementu_ZENBATU++] = '\r'; erantzun_1262b476[elementu_ZENBATU++] = '\n'; erantzun_1262b476[elementu_ZENBATU] = 0; erantzun(erantzun_1262b476);
    } else if (같은지(Marra, "STOR") || 같은지(Marra, "RETR")) {
        if (수행작업) { erantzun("450 Transfer in progress\r\n"); return; }
        if (eskuzko_konexio < 0 && datuak < 0) { erantzun("425 Use PASV or EPSV\r\n"); return; }
        if (!Bide_izena(부가인수)) { erantzun("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(Marra, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(transferitu_izen, fitxategi_sarrera_izen, strlen(fitxategi_sarrera_izen) + 1);
        if (수행작업 == 2) {
            int fitxategi_helduleku = pk_open(fitxategi_sarrera_izen, irakurtzeko_soilik_balio, 0);
            if (fitxategi_helduleku < 0) { 수행작업 = 0; erantzun("550 File unavailable\r\n"); return; }
            int elementu_ZENBATU = pk_read(fitxategi_helduleku, transferitu_Egoera, sizeof(transferitu_Egoera)); pk_close(fitxategi_helduleku);
            if (elementu_ZENBATU < 0) { 수행작업 = 0; erantzun("451 Read failed\r\n"); return; } 사용량 = elementu_ZENBATU;
        }
        erantzun("150 Opening binary data connection\r\n");
    } else erantzun("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (수신창구 < 0) return;
    int Sarrerakoa_konexio = 망연결받기(수신창구);
    if (Sarrerakoa_konexio >= 0) {
        if (kontrol >= 0) { 통신쓰기(Sarrerakoa_konexio, "421 One session at a time\r\n", 27); itxi_sare(Sarrerakoa_konexio); }
        else { kontrol = Sarrerakoa_konexio; jarduera = 보드밀리초(); erantzun("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (kontrol < 0) return;
    if ((uint32_t)(보드밀리초() - jarduera) > 60000) { deskonektatu(); return; }
    if (!irten_aplik_55b3a1cd) for (unsigned esleitutako_aurrekontu = 0; esleitutako_aurrekontu < 256; esleitutako_aurrekontu++) {
        unsigned char karaktere_kode; int 반환값 = 통신읽기(kontrol, &karaktere_kode, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { deskonektatu(); return; } jarduera = 보드밀리초();
        if (karaktere_kode == '\n') { if (줄오류) erantzun("500 Command too long or invalid\r\n"); else Komandoa(); 줄길이 = 줄오류 = 0; if (irten_aplik_55b3a1cd) break; }
        else if (karaktere_kode != '\r') { if (!karaktere_kode || 줄길이 >= sizeof(Marra) - 1) 줄오류 = 1; else Marra[줄길이++] = karaktere_kode; }
    }
    if (eskuzko_konexio >= 0 && datuak < 0) {
        int 반환값 = 망연결받기(eskuzko_konexio);
        if (반환값 >= 0) {
            if (상대통신주소(반환값) != 상대통신주소(kontrol)) itxi_sare(반환값);
            else { datuak = 반환값; itxi_sare(eskuzko_konexio); eskuzko_konexio = -1; jarduera = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && datuak >= 0) for (unsigned esleitutako_aurrekontu = 0; esleitutako_aurrekontu < 8; esleitutako_aurrekontu++) {
        unsigned char datuak_blokeatu[512]; int elementu_ZENBATU = 통신읽기(datuak, datuak_blokeatu, sizeof(datuak_blokeatu));
        if (elementu_ZENBATU == -11) break;
        if (elementu_ZENBATU < 0) { Stop_transferitu(); erantzun("426 Data connection failed\r\n"); break; }
        jarduera = 보드밀리초();
        if (elementu_ZENBATU == 0) {
            int EMAITZA = -1;
            if (!실패여부) {
                int fitxategi_helduleku = pk_open(transferitu_izen, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (fitxategi_helduleku >= 0) { EMAITZA = pk_write(fitxategi_helduleku, transferitu_Egoera, 사용량); pk_close(fitxategi_helduleku); }
            }
            int 성공여부 = !실패여부 && EMAITZA == (int)사용량; Stop_transferitu(); erantzun(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)elementu_ZENBATU > sizeof(transferitu_Egoera) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(transferitu_Egoera + 사용량, datuak_blokeatu, elementu_ZENBATU); 사용량 += elementu_ZENBATU; }
    }
    if (수행작업 == 2 && datuak >= 0) {
        int elementu_ZENBATU = 통신쓰기(datuak, transferitu_Egoera + 보낸수, 사용량 - 보낸수);
        if (elementu_ZENBATU >= 0) { 보낸수 += elementu_ZENBATU; jarduera = 보드밀리초(); if (보낸수 == 사용량) { Stop_transferitu(); erantzun("226 Transfer complete\r\n"); } }
        else if (elementu_ZENBATU != -11) { Stop_transferitu(); erantzun("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < 응답크기) {
        int elementu_ZENBATU = 통신쓰기(kontrol, 응답모음 + 응답전송량, 응답크기 - 응답전송량);
        if (elementu_ZENBATU > 0) 응답전송량 += elementu_ZENBATU; else if (elementu_ZENBATU != -11) { deskonektatu(); return; }
    }
    if (응답전송량 == 응답크기) { 응답크기 = 응답전송량 = 0; if (irten_aplik_55b3a1cd) deskonektatu(); }
}
