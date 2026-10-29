#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "võrk_Virn.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int saama_port = -1, meede = -1, käsitsi_ühendus = -1, andmed = -1;
static unsigned 로그인됨, kasutaja_OK, liin_suurust_muutma, 줄오류, välju_programm, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned vastus_suurust_muutma, 응답전송량, Edasi_pordinumber;
static uint32_t Tegevus;
static char Joon[256], 응답모음[2048], Fail_kirje_nimetus[64], Edasta_nimetus[64];
static unsigned char Edasta_Olek[16384];
static int 같은지(const char *첫째값, const char *SECOND_VALUE) { while (*첫째값 && *첫째값 == *SECOND_VALUE) { 첫째값++; SECOND_VALUE++; } return *첫째값 == *SECOND_VALUE; }
static void vastus(const char *string_andmed) {
    size_t kaup_COUNT = strlen(string_andmed);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, vastus_suurust_muutma - 응답전송량); vastus_suurust_muutma -= 응답전송량; 응답전송량 = 0; }
    if (kaup_COUNT > sizeof(응답모음) - vastus_suurust_muutma) { välju_programm = 1; return; }
    memcpy(응답모음 + vastus_suurust_muutma, string_andmed, kaup_COUNT); vastus_suurust_muutma += kaup_COUNT;
}
static void 수치(unsigned VALUE, char *näitaja_andmed, unsigned *kaup_COUNT) {
    char number_COUNT[10]; unsigned kirje_COUNT = 0;
    do { number_COUNT[kirje_COUNT++] = '0' + VALUE % 10; VALUE /= 10; } while (VALUE);
    while (kirje_COUNT) näitaja_andmed[(*kaup_COUNT)++] = number_COUNT[--kirje_COUNT];
}
static void Peata_Edasta(void) {
    if (andmed >= 0) Sule_võrk(andmed); if (käsitsi_ühendus >= 0) Sule_võrk(käsitsi_ühendus);
    andmed = käsitsi_ühendus = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void ühendust_katkestama(void) {
    Peata_Edasta(); if (meede >= 0) Sule_võrk(meede); meede = -1;
    로그인됨 = kasutaja_OK = liin_suurust_muutma = 줄오류 = vastus_suurust_muutma = 응답전송량 = välju_programm = 0;
}
int failiedastus_meede(int Nimi) {
    if (Nimi == 2) return saama_port >= 0;
    if (Nimi == 0) { ühendust_katkestama(); if (saama_port >= 0) Sule_võrk(saama_port); saama_port = -1; return 0; }
    if (Nimi != 1) return -22; if (saama_port >= 0) return 0;
    saama_port = 통신끝점만들기(1); if (saama_port < 0) return saama_port;
    int 반환값 = NET_BIND(saama_port, 망상태읽기(0,0), 21); if (!반환값) 반환값 = NET_jälgima(saama_port);
    if (반환값 < 0) { Sule_võrk(saama_port); saama_port = -1; } return 반환값;
}
static int RADA(const char *Nimi_2) {
    unsigned kaup_COUNT = 0; if (*Nimi_2 == '/') Nimi_2++;
    if (!*Nimi_2 || 같은지(Nimi_2, ".") || 같은지(Nimi_2, "..")) return 0;
    Fail_kirje_nimetus[kaup_COUNT++] = '/';
    while (*Nimi_2) {
        unsigned char koodipunkt = *Nimi_2++;
        if (kaup_COUNT >= 63 || koodipunkt < 32 || koodipunkt == 127 || koodipunkt == '/' || koodipunkt == '\\') return 0;
        Fail_kirje_nimetus[kaup_COUNT++] = koodipunkt;
    }
    Fail_kirje_nimetus[kaup_COUNT] = 0; return 1;
}
static void saatma_Loend(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int kaup_COUNT = 자바파일항목길이(순번); if (kaup_COUNT <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned kirje_COUNT = strlen(앞부분); memcpy(Edasta_Olek + 사용량, 앞부분, kirje_COUNT); 사용량 += kirje_COUNT;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)Edasta_Olek, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        kirje_COUNT = strlen(뒷부분); memcpy(Edasta_Olek + 사용량, 뒷부분, kirje_COUNT); 사용량 += kirje_COUNT;
        for (int 안쪽순번 = 0; 안쪽순번 < kaup_COUNT; 안쪽순번++) Edasta_Olek[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        Edasta_Olek[사용량++] = '\r'; Edasta_Olek[사용량++] = '\n';
    }
}
static void Ettevalmistamine_käsitsi_ühendus(int 확장여부) {
    if (수행작업) { vastus("450 Transfer in progress\r\n"); return; }
    Peata_Edasta(); käsitsi_ühendus = 통신끝점만들기(1);
    if (käsitsi_ühendus >= 0) 통신주소재사용(käsitsi_ühendus);
    unsigned pordinumber = 50000 + Edasi_pordinumber++ % 8;
    if (käsitsi_ühendus < 0 || NET_BIND(käsitsi_ühendus, 망상태읽기(0,0), pordinumber) || NET_jälgima(käsitsi_ühendus)) {
        Peata_Edasta(); vastus("425 Cannot open passive listener\r\n"); return;
    }
    char vastus_1262b476[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned kaup_COUNT = strlen(앞부분); memcpy(vastus_1262b476, 앞부분, kaup_COUNT);
    if (확장여부) { 수치(pordinumber, vastus_1262b476, &kaup_COUNT); vastus_1262b476[kaup_COUNT++] = '|'; }
    else {
        uint32_t ADDRESS=망상태읽기(0,0);
        for (int asukohaindeks=24;asukohaindeks>=0;asukohaindeks-=8) { 수치((ADDRESS>>asukohaindeks)&255,vastus_1262b476,&kaup_COUNT);vastus_1262b476[kaup_COUNT++]=','; }
        수치(pordinumber / 256, vastus_1262b476, &kaup_COUNT); vastus_1262b476[kaup_COUNT++] = ','; 수치(pordinumber % 256, vastus_1262b476, &kaup_COUNT);
    }
    vastus_1262b476[kaup_COUNT++] = ')'; vastus_1262b476[kaup_COUNT++] = '\r'; vastus_1262b476[kaup_COUNT++] = '\n'; vastus_1262b476[kaup_COUNT] = 0; vastus(vastus_1262b476);
}
static void Käsk(void) {
    Joon[liin_suurust_muutma] = 0;
    char *부가인수 = Joon; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(Joon, "QUIT")) { Peata_Edasta(); vastus("221 Goodbye\r\n"); välju_programm = 1; return; }
    if (같은지(Joon, "NOOP")) { vastus("200 OK\r\n"); return; }
    if (같은지(Joon, "SYST")) { vastus("215 UNIX Type: L8\r\n"); return; }
    if (같은지(Joon, "FEAT")) { vastus("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(Joon, "USER")) { 로그인됨 = 0; kasutaja_OK = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); vastus(kasutaja_OK ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(Joon, "PASS")) { 로그인됨 = kasutaja_OK; vastus(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { vastus("530 Login first\r\n"); return; }
    if (같은지(Joon, "PWD")) vastus("257 \"/\"\r\n");
    else if (같은지(Joon, "CWD")) vastus(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(Joon, "TYPE")) vastus(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(Joon, "OPTS")) vastus(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(Joon, "PASV")) Ettevalmistamine_käsitsi_ühendus(0);
    else if (같은지(Joon, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) vastus("522 IPv4 only\r\n"); else Ettevalmistamine_käsitsi_ühendus(1); }
    else if (같은지(Joon, "ABOR")) { Peata_Edasta(); vastus("226 Transfer aborted\r\n"); }
    else if (같은지(Joon, "DELE")) { vastus(RADA(부가인수) && pk_unlink(Fail_kirje_nimetus) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(Joon, "LIST") || 같은지(Joon, "NLST") || 같은지(Joon, "MLSD")) {
        if (수행작업) { vastus("450 Transfer in progress\r\n"); return; }
        if (käsitsi_ühendus < 0 && andmed < 0) { vastus("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { vastus("550 Root listing only\r\n"); return; }
        saatma_Loend(같은지(Joon,"MLSD") ? 2 : 같은지(Joon,"LIST") ? 1 : 0); 수행작업 = 2;
        vastus("150 Opening directory listing\r\n");
    }
    else if (같은지(Joon, "SIZE")) {
        if (!RADA(부가인수)) { vastus("550 Invalid filename\r\n"); return; }
        int Fail_pide = pk_open(Fail_kirje_nimetus, kirjutuskaitstud_VALUE, 0); if (Fail_pide < 0) { vastus("550 File unavailable\r\n"); return; }
        int Suurus = pk_size(Fail_pide); pk_close(Fail_pide); char vastus_1262b476[32] = "213 "; unsigned kaup_COUNT = 4;
        수치(Suurus, vastus_1262b476, &kaup_COUNT); vastus_1262b476[kaup_COUNT++] = '\r'; vastus_1262b476[kaup_COUNT++] = '\n'; vastus_1262b476[kaup_COUNT] = 0; vastus(vastus_1262b476);
    } else if (같은지(Joon, "STOR") || 같은지(Joon, "RETR")) {
        if (수행작업) { vastus("450 Transfer in progress\r\n"); return; }
        if (käsitsi_ühendus < 0 && andmed < 0) { vastus("425 Use PASV or EPSV\r\n"); return; }
        if (!RADA(부가인수)) { vastus("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(Joon, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(Edasta_nimetus, Fail_kirje_nimetus, strlen(Fail_kirje_nimetus) + 1);
        if (수행작업 == 2) {
            int Fail_pide = pk_open(Fail_kirje_nimetus, kirjutuskaitstud_VALUE, 0);
            if (Fail_pide < 0) { 수행작업 = 0; vastus("550 File unavailable\r\n"); return; }
            int kaup_COUNT = pk_read(Fail_pide, Edasta_Olek, sizeof(Edasta_Olek)); pk_close(Fail_pide);
            if (kaup_COUNT < 0) { 수행작업 = 0; vastus("451 Read failed\r\n"); return; } 사용량 = kaup_COUNT;
        }
        vastus("150 Opening binary data connection\r\n");
    } else vastus("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (saama_port < 0) return;
    int Sissetulev_ühendus = NET_aktsepteerima(saama_port);
    if (Sissetulev_ühendus >= 0) {
        if (meede >= 0) { NET_kirjutamine(Sissetulev_ühendus, "421 One session at a time\r\n", 27); Sule_võrk(Sissetulev_ühendus); }
        else { meede = Sissetulev_ühendus; Tegevus = 보드밀리초(); vastus("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (meede < 0) return;
    if ((uint32_t)(보드밀리초() - Tegevus) > 60000) { ühendust_katkestama(); return; }
    if (!välju_programm) for (unsigned eelarve = 0; eelarve < 256; eelarve++) {
        unsigned char koodipunkt; int 반환값 = 통신읽기(meede, &koodipunkt, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { ühendust_katkestama(); return; } Tegevus = 보드밀리초();
        if (koodipunkt == '\n') { if (줄오류) vastus("500 Command too long or invalid\r\n"); else Käsk(); liin_suurust_muutma = 줄오류 = 0; if (välju_programm) break; }
        else if (koodipunkt != '\r') { if (!koodipunkt || liin_suurust_muutma >= sizeof(Joon) - 1) 줄오류 = 1; else Joon[liin_suurust_muutma++] = koodipunkt; }
    }
    if (käsitsi_ühendus >= 0 && andmed < 0) {
        int 반환값 = NET_aktsepteerima(käsitsi_ühendus);
        if (반환값 >= 0) {
            if (NET_partner_ADDRESS(반환값) != NET_partner_ADDRESS(meede)) Sule_võrk(반환값);
            else { andmed = 반환값; Sule_võrk(käsitsi_ühendus); käsitsi_ühendus = -1; Tegevus = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && andmed >= 0) for (unsigned eelarve = 0; eelarve < 8; eelarve++) {
        unsigned char andmeplokk[512]; int kaup_COUNT = 통신읽기(andmed, andmeplokk, sizeof(andmeplokk));
        if (kaup_COUNT == -11) break;
        if (kaup_COUNT < 0) { Peata_Edasta(); vastus("426 Data connection failed\r\n"); break; }
        Tegevus = 보드밀리초();
        if (kaup_COUNT == 0) {
            int TULEMUS = -1;
            if (!실패여부) {
                int Fail_pide = pk_open(Edasta_nimetus, 쓰기전용 | 없으면만들기 | lühendama_Sisu, 0600);
                if (Fail_pide >= 0) { TULEMUS = pk_write(Fail_pide, Edasta_Olek, 사용량); pk_close(Fail_pide); }
            }
            int 성공여부 = !실패여부 && TULEMUS == (int)사용량; Peata_Edasta(); vastus(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)kaup_COUNT > sizeof(Edasta_Olek) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(Edasta_Olek + 사용량, andmeplokk, kaup_COUNT); 사용량 += kaup_COUNT; }
    }
    if (수행작업 == 2 && andmed >= 0) {
        int kaup_COUNT = NET_kirjutamine(andmed, Edasta_Olek + 보낸수, 사용량 - 보낸수);
        if (kaup_COUNT >= 0) { 보낸수 += kaup_COUNT; Tegevus = 보드밀리초(); if (보낸수 == 사용량) { Peata_Edasta(); vastus("226 Transfer complete\r\n"); } }
        else if (kaup_COUNT != -11) { Peata_Edasta(); vastus("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < vastus_suurust_muutma) {
        int kaup_COUNT = NET_kirjutamine(meede, 응답모음 + 응답전송량, vastus_suurust_muutma - 응답전송량);
        if (kaup_COUNT > 0) 응답전송량 += kaup_COUNT; else if (kaup_COUNT != -11) { ühendust_katkestama(); return; }
    }
    if (응답전송량 == vastus_suurust_muutma) { vastus_suurust_muutma = 응답전송량 = 0; if (välju_programm) ühendust_katkestama(); }
}
