#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "tinklas_eilė.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int gauti_jungtis = -1, valdymas = -1, rankinis_ryšys = -1, duomenys = -1;
static unsigned 로그인됨, naudotojas_Gerai, eilutė_dydis, 줄오류, išeiti_programa, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned atsakyti_dydis, 응답전송량, toliau_prievado_numeris;
static uint32_t Veikla;
static char Eilutė[256], 응답모음[2048], Failas_įrašas_pavadinimas[64], perduoti_pavadinimas[64];
static unsigned char perduoti_Būsena[16384];
static int 같은지(const char *첫째값, const char *SECOND_VALUE) { while (*첫째값 && *첫째값 == *SECOND_VALUE) { 첫째값++; SECOND_VALUE++; } return *첫째값 == *SECOND_VALUE; }
static void atsakyti(const char *eilutė_duomenys) {
    size_t prekė_COUNT = strlen(eilutė_duomenys);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, atsakyti_dydis - 응답전송량); atsakyti_dydis -= 응답전송량; 응답전송량 = 0; }
    if (prekė_COUNT > sizeof(응답모음) - atsakyti_dydis) { išeiti_programa = 1; return; }
    memcpy(응답모음 + atsakyti_dydis, eilutė_duomenys, prekė_COUNT); atsakyti_dydis += prekė_COUNT;
}
static void 수치(unsigned VALUE, char *KR_duomenys, unsigned *prekė_COUNT) {
    char skaitmuo_COUNT[10]; unsigned įrašas_COUNT = 0;
    do { skaitmuo_COUNT[įrašas_COUNT++] = '0' + VALUE % 10; VALUE /= 10; } while (VALUE);
    while (įrašas_COUNT) KR_duomenys[(*prekė_COUNT)++] = skaitmuo_COUNT[--įrašas_COUNT];
}
static void Stok_perduoti(void) {
    if (duomenys >= 0) Uždaryti_tinklas(duomenys); if (rankinis_ryšys >= 0) Uždaryti_tinklas(rankinis_ryšys);
    duomenys = rankinis_ryšys = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void atjungti(void) {
    Stok_perduoti(); if (valdymas >= 0) Uždaryti_tinklas(valdymas); valdymas = -1;
    로그인됨 = naudotojas_Gerai = eilutė_dydis = 줄오류 = atsakyti_dydis = 응답전송량 = išeiti_programa = 0;
}
int failo_perdavimas_valdymas(int Veiksmas) {
    if (Veiksmas == 2) return gauti_jungtis >= 0;
    if (Veiksmas == 0) { atjungti(); if (gauti_jungtis >= 0) Uždaryti_tinklas(gauti_jungtis); gauti_jungtis = -1; return 0; }
    if (Veiksmas != 1) return -22; if (gauti_jungtis >= 0) return 0;
    gauti_jungtis = 통신끝점만들기(1); if (gauti_jungtis < 0) return gauti_jungtis;
    int 반환값 = NET_BIND(gauti_jungtis, 망상태읽기(0,0), 21); if (!반환값) 반환값 = NET_laukti(gauti_jungtis);
    if (반환값 < 0) { Uždaryti_tinklas(gauti_jungtis); gauti_jungtis = -1; } return 반환값;
}
static int KELIAS(const char *Pavadinimas_2) {
    unsigned prekė_COUNT = 0; if (*Pavadinimas_2 == '/') Pavadinimas_2++;
    if (!*Pavadinimas_2 || 같은지(Pavadinimas_2, ".") || 같은지(Pavadinimas_2, "..")) return 0;
    Failas_įrašas_pavadinimas[prekė_COUNT++] = '/';
    while (*Pavadinimas_2) {
        unsigned char simbolio_kodas = *Pavadinimas_2++;
        if (prekė_COUNT >= 63 || simbolio_kodas < 32 || simbolio_kodas == 127 || simbolio_kodas == '/' || simbolio_kodas == '\\') return 0;
        Failas_įrašas_pavadinimas[prekė_COUNT++] = simbolio_kodas;
    }
    Failas_įrašas_pavadinimas[prekė_COUNT] = 0; return 1;
}
static void siųsti_Sąrašas(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int prekė_COUNT = 자바파일항목길이(순번); if (prekė_COUNT <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned įrašas_COUNT = strlen(앞부분); memcpy(perduoti_Būsena + 사용량, 앞부분, įrašas_COUNT); 사용량 += įrašas_COUNT;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)perduoti_Būsena, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        įrašas_COUNT = strlen(뒷부분); memcpy(perduoti_Būsena + 사용량, 뒷부분, įrašas_COUNT); 사용량 += įrašas_COUNT;
        for (int 안쪽순번 = 0; 안쪽순번 < prekė_COUNT; 안쪽순번++) perduoti_Būsena[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        perduoti_Būsena[사용량++] = '\r'; perduoti_Būsena[사용량++] = '\n';
    }
}
static void Parengti_rankinis_ryšys(int 확장여부) {
    if (수행작업) { atsakyti("450 Transfer in progress\r\n"); return; }
    Stok_perduoti(); rankinis_ryšys = 통신끝점만들기(1);
    if (rankinis_ryšys >= 0) 통신주소재사용(rankinis_ryšys);
    unsigned prievado_numeris = 50000 + toliau_prievado_numeris++ % 8;
    if (rankinis_ryšys < 0 || NET_BIND(rankinis_ryšys, 망상태읽기(0,0), prievado_numeris) || NET_laukti(rankinis_ryšys)) {
        Stok_perduoti(); atsakyti("425 Cannot open passive listener\r\n"); return;
    }
    char atsakas[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned prekė_COUNT = strlen(앞부분); memcpy(atsakas, 앞부분, prekė_COUNT);
    if (확장여부) { 수치(prievado_numeris, atsakas, &prekė_COUNT); atsakas[prekė_COUNT++] = '|'; }
    else {
        uint32_t ADDRESS=망상태읽기(0,0);
        for (int vietos_rodyklė=24;vietos_rodyklė>=0;vietos_rodyklė-=8) { 수치((ADDRESS>>vietos_rodyklė)&255,atsakas,&prekė_COUNT);atsakas[prekė_COUNT++]=','; }
        수치(prievado_numeris / 256, atsakas, &prekė_COUNT); atsakas[prekė_COUNT++] = ','; 수치(prievado_numeris % 256, atsakas, &prekė_COUNT);
    }
    atsakas[prekė_COUNT++] = ')'; atsakas[prekė_COUNT++] = '\r'; atsakas[prekė_COUNT++] = '\n'; atsakas[prekė_COUNT] = 0; atsakyti(atsakas);
}
static void Komanda(void) {
    Eilutė[eilutė_dydis] = 0;
    char *부가인수 = Eilutė; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(Eilutė, "QUIT")) { Stok_perduoti(); atsakyti("221 Goodbye\r\n"); išeiti_programa = 1; return; }
    if (같은지(Eilutė, "NOOP")) { atsakyti("200 OK\r\n"); return; }
    if (같은지(Eilutė, "SYST")) { atsakyti("215 UNIX Type: L8\r\n"); return; }
    if (같은지(Eilutė, "FEAT")) { atsakyti("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(Eilutė, "USER")) { 로그인됨 = 0; naudotojas_Gerai = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); atsakyti(naudotojas_Gerai ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(Eilutė, "PASS")) { 로그인됨 = naudotojas_Gerai; atsakyti(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { atsakyti("530 Login first\r\n"); return; }
    if (같은지(Eilutė, "PWD")) atsakyti("257 \"/\"\r\n");
    else if (같은지(Eilutė, "CWD")) atsakyti(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(Eilutė, "TYPE")) atsakyti(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(Eilutė, "OPTS")) atsakyti(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(Eilutė, "PASV")) Parengti_rankinis_ryšys(0);
    else if (같은지(Eilutė, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) atsakyti("522 IPv4 only\r\n"); else Parengti_rankinis_ryšys(1); }
    else if (같은지(Eilutė, "ABOR")) { Stok_perduoti(); atsakyti("226 Transfer aborted\r\n"); }
    else if (같은지(Eilutė, "DELE")) { atsakyti(KELIAS(부가인수) && pk_unlink(Failas_įrašas_pavadinimas) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(Eilutė, "LIST") || 같은지(Eilutė, "NLST") || 같은지(Eilutė, "MLSD")) {
        if (수행작업) { atsakyti("450 Transfer in progress\r\n"); return; }
        if (rankinis_ryšys < 0 && duomenys < 0) { atsakyti("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { atsakyti("550 Root listing only\r\n"); return; }
        siųsti_Sąrašas(같은지(Eilutė,"MLSD") ? 2 : 같은지(Eilutė,"LIST") ? 1 : 0); 수행작업 = 2;
        atsakyti("150 Opening directory listing\r\n");
    }
    else if (같은지(Eilutė, "SIZE")) {
        if (!KELIAS(부가인수)) { atsakyti("550 Invalid filename\r\n"); return; }
        int Failas_rodyklė = pk_open(Failas_įrašas_pavadinimas, tik_skaitomas_VALUE, 0); if (Failas_rodyklė < 0) { atsakyti("550 File unavailable\r\n"); return; }
        int Dydis = pk_size(Failas_rodyklė); pk_close(Failas_rodyklė); char atsakas[32] = "213 "; unsigned prekė_COUNT = 4;
        수치(Dydis, atsakas, &prekė_COUNT); atsakas[prekė_COUNT++] = '\r'; atsakas[prekė_COUNT++] = '\n'; atsakas[prekė_COUNT] = 0; atsakyti(atsakas);
    } else if (같은지(Eilutė, "STOR") || 같은지(Eilutė, "RETR")) {
        if (수행작업) { atsakyti("450 Transfer in progress\r\n"); return; }
        if (rankinis_ryšys < 0 && duomenys < 0) { atsakyti("425 Use PASV or EPSV\r\n"); return; }
        if (!KELIAS(부가인수)) { atsakyti("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(Eilutė, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(perduoti_pavadinimas, Failas_įrašas_pavadinimas, strlen(Failas_įrašas_pavadinimas) + 1);
        if (수행작업 == 2) {
            int Failas_rodyklė = pk_open(Failas_įrašas_pavadinimas, tik_skaitomas_VALUE, 0);
            if (Failas_rodyklė < 0) { 수행작업 = 0; atsakyti("550 File unavailable\r\n"); return; }
            int prekė_COUNT = pk_read(Failas_rodyklė, perduoti_Būsena, sizeof(perduoti_Būsena)); pk_close(Failas_rodyklė);
            if (prekė_COUNT < 0) { 수행작업 = 0; atsakyti("451 Read failed\r\n"); return; } 사용량 = prekė_COUNT;
        }
        atsakyti("150 Opening binary data connection\r\n");
    } else atsakyti("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (gauti_jungtis < 0) return;
    int priimta_ryšys = NET_priimti(gauti_jungtis);
    if (priimta_ryšys >= 0) {
        if (valdymas >= 0) { NET_rašymas(priimta_ryšys, "421 One session at a time\r\n", 27); Uždaryti_tinklas(priimta_ryšys); }
        else { valdymas = priimta_ryšys; Veikla = 보드밀리초(); atsakyti("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (valdymas < 0) return;
    if ((uint32_t)(보드밀리초() - Veikla) > 60000) { atjungti(); return; }
    if (!išeiti_programa) for (unsigned biudžetas = 0; biudžetas < 256; biudžetas++) {
        unsigned char simbolio_kodas; int 반환값 = 통신읽기(valdymas, &simbolio_kodas, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { atjungti(); return; } Veikla = 보드밀리초();
        if (simbolio_kodas == '\n') { if (줄오류) atsakyti("500 Command too long or invalid\r\n"); else Komanda(); eilutė_dydis = 줄오류 = 0; if (išeiti_programa) break; }
        else if (simbolio_kodas != '\r') { if (!simbolio_kodas || eilutė_dydis >= sizeof(Eilutė) - 1) 줄오류 = 1; else Eilutė[eilutė_dydis++] = simbolio_kodas; }
    }
    if (rankinis_ryšys >= 0 && duomenys < 0) {
        int 반환값 = NET_priimti(rankinis_ryšys);
        if (반환값 >= 0) {
            if (NET_lygiavertis_mazgas_ADDRESS(반환값) != NET_lygiavertis_mazgas_ADDRESS(valdymas)) Uždaryti_tinklas(반환값);
            else { duomenys = 반환값; Uždaryti_tinklas(rankinis_ryšys); rankinis_ryšys = -1; Veikla = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && duomenys >= 0) for (unsigned biudžetas = 0; biudžetas < 8; biudžetas++) {
        unsigned char duomenų_blokas[512]; int prekė_COUNT = 통신읽기(duomenys, duomenų_blokas, sizeof(duomenų_blokas));
        if (prekė_COUNT == -11) break;
        if (prekė_COUNT < 0) { Stok_perduoti(); atsakyti("426 Data connection failed\r\n"); break; }
        Veikla = 보드밀리초();
        if (prekė_COUNT == 0) {
            int REZULTATAS = -1;
            if (!실패여부) {
                int Failas_rodyklė = pk_open(perduoti_pavadinimas, 쓰기전용 | 없으면만들기 | trumpinti_Turinys, 0600);
                if (Failas_rodyklė >= 0) { REZULTATAS = pk_write(Failas_rodyklė, perduoti_Būsena, 사용량); pk_close(Failas_rodyklė); }
            }
            int 성공여부 = !실패여부 && REZULTATAS == (int)사용량; Stok_perduoti(); atsakyti(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)prekė_COUNT > sizeof(perduoti_Būsena) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(perduoti_Būsena + 사용량, duomenų_blokas, prekė_COUNT); 사용량 += prekė_COUNT; }
    }
    if (수행작업 == 2 && duomenys >= 0) {
        int prekė_COUNT = NET_rašymas(duomenys, perduoti_Būsena + 보낸수, 사용량 - 보낸수);
        if (prekė_COUNT >= 0) { 보낸수 += prekė_COUNT; Veikla = 보드밀리초(); if (보낸수 == 사용량) { Stok_perduoti(); atsakyti("226 Transfer complete\r\n"); } }
        else if (prekė_COUNT != -11) { Stok_perduoti(); atsakyti("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < atsakyti_dydis) {
        int prekė_COUNT = NET_rašymas(valdymas, 응답모음 + 응답전송량, atsakyti_dydis - 응답전송량);
        if (prekė_COUNT > 0) 응답전송량 += prekė_COUNT; else if (prekė_COUNT != -11) { atjungti(); return; }
    }
    if (응답전송량 == atsakyti_dydis) { atsakyti_dydis = 응답전송량 = 0; if (išeiti_programa) atjungti(); }
}
