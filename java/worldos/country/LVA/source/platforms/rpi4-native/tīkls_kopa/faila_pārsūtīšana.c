#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "tīkls_kopa.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int saņemt_ports = -1, vadība = -1, roku_paziņa = -1, dati = -1;
static unsigned 로그인됨, lietotājs_Labi, līnija_mainīt_izmērus, 줄오류, iziet_programma, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned atbilde_mainīt_izmērus, 응답전송량, Tālāk_porta_numurs;
static uint32_t darbība;
static char Līniju[256], 응답모음[2048], Fails_ievade_nosaukums[64], nodot_nosaukums[64];
static unsigned char nodot_Statuss[16384];
static int 같은지(const char *첫째값, const char *SECOND_VALUE) { while (*첫째값 && *첫째값 == *SECOND_VALUE) { 첫째값++; SECOND_VALUE++; } return *첫째값 == *SECOND_VALUE; }
static void atbilde(const char *virkne_dati) {
    size_t krājums_COUNT = strlen(virkne_dati);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, atbilde_mainīt_izmērus - 응답전송량); atbilde_mainīt_izmērus -= 응답전송량; 응답전송량 = 0; }
    if (krājums_COUNT > sizeof(응답모음) - atbilde_mainīt_izmērus) { iziet_programma = 1; return; }
    memcpy(응답모음 + atbilde_mainīt_izmērus, virkne_dati, krājums_COUNT); atbilde_mainīt_izmērus += krājums_COUNT;
}
static void 수치(unsigned VALUE, char *mērs_dati, unsigned *krājums_COUNT) {
    char cipars_COUNT[10]; unsigned ievade_COUNT = 0;
    do { cipars_COUNT[ievade_COUNT++] = '0' + VALUE % 10; VALUE /= 10; } while (VALUE);
    while (ievade_COUNT) mērs_dati[(*krājums_COUNT)++] = cipars_COUNT[--ievade_COUNT];
}
static void Stop_nodot(void) {
    if (dati >= 0) Aizvērt_tīkls(dati); if (roku_paziņa >= 0) Aizvērt_tīkls(roku_paziņa);
    dati = roku_paziņa = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void atvienot(void) {
    Stop_nodot(); if (vadība >= 0) Aizvērt_tīkls(vadība); vadība = -1;
    로그인됨 = lietotājs_Labi = līnija_mainīt_izmērus = 줄오류 = atbilde_mainīt_izmērus = 응답전송량 = iziet_programma = 0;
}
int faila_pārsūtīšana_vadība(int Darbība) {
    if (Darbība == 2) return saņemt_ports >= 0;
    if (Darbība == 0) { atvienot(); if (saņemt_ports >= 0) Aizvērt_tīkls(saņemt_ports); saņemt_ports = -1; return 0; }
    if (Darbība != 1) return -22; if (saņemt_ports >= 0) return 0;
    saņemt_ports = 통신끝점만들기(1); if (saņemt_ports < 0) return saņemt_ports;
    int 반환값 = NET_BIND(saņemt_ports, 망상태읽기(0,0), 21); if (!반환값) 반환값 = NET_klausīties(saņemt_ports);
    if (반환값 < 0) { Aizvērt_tīkls(saņemt_ports); saņemt_ports = -1; } return 반환값;
}
static int CEĻŠ(const char *Nosaukums) {
    unsigned krājums_COUNT = 0; if (*Nosaukums == '/') Nosaukums++;
    if (!*Nosaukums || 같은지(Nosaukums, ".") || 같은지(Nosaukums, "..")) return 0;
    Fails_ievade_nosaukums[krājums_COUNT++] = '/';
    while (*Nosaukums) {
        unsigned char koda_punkts = *Nosaukums++;
        if (krājums_COUNT >= 63 || koda_punkts < 32 || koda_punkts == 127 || koda_punkts == '/' || koda_punkts == '\\') return 0;
        Fails_ievade_nosaukums[krājums_COUNT++] = koda_punkts;
    }
    Fails_ievade_nosaukums[krājums_COUNT] = 0; return 1;
}
static void sūtīt_Saraksts(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int krājums_COUNT = 자바파일항목길이(순번); if (krājums_COUNT <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned ievade_COUNT = strlen(앞부분); memcpy(nodot_Statuss + 사용량, 앞부분, ievade_COUNT); 사용량 += ievade_COUNT;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)nodot_Statuss, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        ievade_COUNT = strlen(뒷부분); memcpy(nodot_Statuss + 사용량, 뒷부분, ievade_COUNT); 사용량 += ievade_COUNT;
        for (int 안쪽순번 = 0; 안쪽순번 < krājums_COUNT; 안쪽순번++) nodot_Statuss[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        nodot_Statuss[사용량++] = '\r'; nodot_Statuss[사용량++] = '\n';
    }
}
static void Sagatavot_roku_paziņa(int 확장여부) {
    if (수행작업) { atbilde("450 Transfer in progress\r\n"); return; }
    Stop_nodot(); roku_paziņa = 통신끝점만들기(1);
    if (roku_paziņa >= 0) 통신주소재사용(roku_paziņa);
    unsigned porta_numurs = 50000 + Tālāk_porta_numurs++ % 8;
    if (roku_paziņa < 0 || NET_BIND(roku_paziņa, 망상태읽기(0,0), porta_numurs) || NET_klausīties(roku_paziņa)) {
        Stop_nodot(); atbilde("425 Cannot open passive listener\r\n"); return;
    }
    char atbilde_1262b476[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned krājums_COUNT = strlen(앞부분); memcpy(atbilde_1262b476, 앞부분, krājums_COUNT);
    if (확장여부) { 수치(porta_numurs, atbilde_1262b476, &krājums_COUNT); atbilde_1262b476[krājums_COUNT++] = '|'; }
    else {
        uint32_t adrese=망상태읽기(0,0);
        for (int pozīcijas_indekss=24;pozīcijas_indekss>=0;pozīcijas_indekss-=8) { 수치((adrese>>pozīcijas_indekss)&255,atbilde_1262b476,&krājums_COUNT);atbilde_1262b476[krājums_COUNT++]=','; }
        수치(porta_numurs / 256, atbilde_1262b476, &krājums_COUNT); atbilde_1262b476[krājums_COUNT++] = ','; 수치(porta_numurs % 256, atbilde_1262b476, &krājums_COUNT);
    }
    atbilde_1262b476[krājums_COUNT++] = ')'; atbilde_1262b476[krājums_COUNT++] = '\r'; atbilde_1262b476[krājums_COUNT++] = '\n'; atbilde_1262b476[krājums_COUNT] = 0; atbilde(atbilde_1262b476);
}
static void Komanda(void) {
    Līniju[līnija_mainīt_izmērus] = 0;
    char *부가인수 = Līniju; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(Līniju, "QUIT")) { Stop_nodot(); atbilde("221 Goodbye\r\n"); iziet_programma = 1; return; }
    if (같은지(Līniju, "NOOP")) { atbilde("200 OK\r\n"); return; }
    if (같은지(Līniju, "SYST")) { atbilde("215 UNIX Type: L8\r\n"); return; }
    if (같은지(Līniju, "FEAT")) { atbilde("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(Līniju, "USER")) { 로그인됨 = 0; lietotājs_Labi = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); atbilde(lietotājs_Labi ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(Līniju, "PASS")) { 로그인됨 = lietotājs_Labi; atbilde(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { atbilde("530 Login first\r\n"); return; }
    if (같은지(Līniju, "PWD")) atbilde("257 \"/\"\r\n");
    else if (같은지(Līniju, "CWD")) atbilde(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(Līniju, "TYPE")) atbilde(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(Līniju, "OPTS")) atbilde(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(Līniju, "PASV")) Sagatavot_roku_paziņa(0);
    else if (같은지(Līniju, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) atbilde("522 IPv4 only\r\n"); else Sagatavot_roku_paziņa(1); }
    else if (같은지(Līniju, "ABOR")) { Stop_nodot(); atbilde("226 Transfer aborted\r\n"); }
    else if (같은지(Līniju, "DELE")) { atbilde(CEĻŠ(부가인수) && pk_unlink(Fails_ievade_nosaukums) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(Līniju, "LIST") || 같은지(Līniju, "NLST") || 같은지(Līniju, "MLSD")) {
        if (수행작업) { atbilde("450 Transfer in progress\r\n"); return; }
        if (roku_paziņa < 0 && dati < 0) { atbilde("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { atbilde("550 Root listing only\r\n"); return; }
        sūtīt_Saraksts(같은지(Līniju,"MLSD") ? 2 : 같은지(Līniju,"LIST") ? 1 : 0); 수행작업 = 2;
        atbilde("150 Opening directory listing\r\n");
    }
    else if (같은지(Līniju, "SIZE")) {
        if (!CEĻŠ(부가인수)) { atbilde("550 Invalid filename\r\n"); return; }
        int Fails_turis = pk_open(Fails_ievade_nosaukums, tikai_lasāms_VALUE, 0); if (Fails_turis < 0) { atbilde("550 File unavailable\r\n"); return; }
        int Izmērs = pk_size(Fails_turis); pk_close(Fails_turis); char atbilde_1262b476[32] = "213 "; unsigned krājums_COUNT = 4;
        수치(Izmērs, atbilde_1262b476, &krājums_COUNT); atbilde_1262b476[krājums_COUNT++] = '\r'; atbilde_1262b476[krājums_COUNT++] = '\n'; atbilde_1262b476[krājums_COUNT] = 0; atbilde(atbilde_1262b476);
    } else if (같은지(Līniju, "STOR") || 같은지(Līniju, "RETR")) {
        if (수행작업) { atbilde("450 Transfer in progress\r\n"); return; }
        if (roku_paziņa < 0 && dati < 0) { atbilde("425 Use PASV or EPSV\r\n"); return; }
        if (!CEĻŠ(부가인수)) { atbilde("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(Līniju, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(nodot_nosaukums, Fails_ievade_nosaukums, strlen(Fails_ievade_nosaukums) + 1);
        if (수행작업 == 2) {
            int Fails_turis = pk_open(Fails_ievade_nosaukums, tikai_lasāms_VALUE, 0);
            if (Fails_turis < 0) { 수행작업 = 0; atbilde("550 File unavailable\r\n"); return; }
            int krājums_COUNT = pk_read(Fails_turis, nodot_Statuss, sizeof(nodot_Statuss)); pk_close(Fails_turis);
            if (krājums_COUNT < 0) { 수행작업 = 0; atbilde("451 Read failed\r\n"); return; } 사용량 = krājums_COUNT;
        }
        atbilde("150 Opening binary data connection\r\n");
    } else atbilde("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (saņemt_ports < 0) return;
    int Ienākošs_paziņa = NET_akceptēt(saņemt_ports);
    if (Ienākošs_paziņa >= 0) {
        if (vadība >= 0) { NET_rakstīšana(Ienākošs_paziņa, "421 One session at a time\r\n", 27); Aizvērt_tīkls(Ienākošs_paziņa); }
        else { vadība = Ienākošs_paziņa; darbība = 보드밀리초(); atbilde("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (vadība < 0) return;
    if ((uint32_t)(보드밀리초() - darbība) > 60000) { atvienot(); return; }
    if (!iziet_programma) for (unsigned budžets = 0; budžets < 256; budžets++) {
        unsigned char koda_punkts; int 반환값 = 통신읽기(vadība, &koda_punkts, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { atvienot(); return; } darbība = 보드밀리초();
        if (koda_punkts == '\n') { if (줄오류) atbilde("500 Command too long or invalid\r\n"); else Komanda(); līnija_mainīt_izmērus = 줄오류 = 0; if (iziet_programma) break; }
        else if (koda_punkts != '\r') { if (!koda_punkts || līnija_mainīt_izmērus >= sizeof(Līniju) - 1) 줄오류 = 1; else Līniju[līnija_mainīt_izmērus++] = koda_punkts; }
    }
    if (roku_paziņa >= 0 && dati < 0) {
        int 반환값 = NET_akceptēt(roku_paziņa);
        if (반환값 >= 0) {
            if (NET_vienranga_adrese(반환값) != NET_vienranga_adrese(vadība)) Aizvērt_tīkls(반환값);
            else { dati = 반환값; Aizvērt_tīkls(roku_paziņa); roku_paziņa = -1; darbība = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && dati >= 0) for (unsigned budžets = 0; budžets < 8; budžets++) {
        unsigned char datu_bloks[512]; int krājums_COUNT = 통신읽기(dati, datu_bloks, sizeof(datu_bloks));
        if (krājums_COUNT == -11) break;
        if (krājums_COUNT < 0) { Stop_nodot(); atbilde("426 Data connection failed\r\n"); break; }
        darbība = 보드밀리초();
        if (krājums_COUNT == 0) {
            int mērs = -1;
            if (!실패여부) {
                int Fails_turis = pk_open(nodot_nosaukums, 쓰기전용 | 없으면만들기 | apraut_Satura_rādītājs, 0600);
                if (Fails_turis >= 0) { mērs = pk_write(Fails_turis, nodot_Statuss, 사용량); pk_close(Fails_turis); }
            }
            int 성공여부 = !실패여부 && mērs == (int)사용량; Stop_nodot(); atbilde(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)krājums_COUNT > sizeof(nodot_Statuss) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(nodot_Statuss + 사용량, datu_bloks, krājums_COUNT); 사용량 += krājums_COUNT; }
    }
    if (수행작업 == 2 && dati >= 0) {
        int krājums_COUNT = NET_rakstīšana(dati, nodot_Statuss + 보낸수, 사용량 - 보낸수);
        if (krājums_COUNT >= 0) { 보낸수 += krājums_COUNT; darbība = 보드밀리초(); if (보낸수 == 사용량) { Stop_nodot(); atbilde("226 Transfer complete\r\n"); } }
        else if (krājums_COUNT != -11) { Stop_nodot(); atbilde("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < atbilde_mainīt_izmērus) {
        int krājums_COUNT = NET_rakstīšana(vadība, 응답모음 + 응답전송량, atbilde_mainīt_izmērus - 응답전송량);
        if (krājums_COUNT > 0) 응답전송량 += krājums_COUNT; else if (krājums_COUNT != -11) { atvienot(); return; }
    }
    if (응답전송량 == atbilde_mainīt_izmērus) { atbilde_mainīt_izmērus = 응답전송량 = 0; if (iziet_programma) atvienot(); }
}
