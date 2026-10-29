#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "sieť_Vrstvy.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int dostať_port = -1, riadenie = -1, manuálny_kontakt = -1, údaje = -1;
static unsigned 로그인됨, používateľ_OK, linka_zmeniť_veľkosť, 줄오류, ukončiť_program, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned odozva_zmeniť_veľkosť, 응답전송량, Ďalej_číslo_portu;
static uint32_t Aktivita;
static char riadok[256], 응답모음[2048], Súbor_položka_názov[64], prenos_názov[64];
static unsigned char prenos_Stav[16384];
static int 같은지(const char *첫째값, const char *SECOND_VALUE) { while (*첫째값 && *첫째값 == *SECOND_VALUE) { 첫째값++; SECOND_VALUE++; } return *첫째값 == *SECOND_VALUE; }
static void odozva(const char *reťazec_údaje) {
    size_t položka_COUNT = strlen(reťazec_údaje);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, odozva_zmeniť_veľkosť - 응답전송량); odozva_zmeniť_veľkosť -= 응답전송량; 응답전송량 = 0; }
    if (položka_COUNT > sizeof(응답모음) - odozva_zmeniť_veľkosť) { ukončiť_program = 1; return; }
    memcpy(응답모음 + odozva_zmeniť_veľkosť, reťazec_údaje, položka_COUNT); odozva_zmeniť_veľkosť += položka_COUNT;
}
static void 수치(unsigned VALUE, char *KR_údaje, unsigned *položka_COUNT) {
    char číslica_COUNT[10]; unsigned položka_COUNT_8f7753a1 = 0;
    do { číslica_COUNT[položka_COUNT_8f7753a1++] = '0' + VALUE % 10; VALUE /= 10; } while (VALUE);
    while (položka_COUNT_8f7753a1) KR_údaje[(*položka_COUNT)++] = číslica_COUNT[--položka_COUNT_8f7753a1];
}
static void Stop_prenos(void) {
    if (údaje >= 0) Zavrieť_sieť(údaje); if (manuálny_kontakt >= 0) Zavrieť_sieť(manuálny_kontakt);
    údaje = manuálny_kontakt = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void odpojiť(void) {
    Stop_prenos(); if (riadenie >= 0) Zavrieť_sieť(riadenie); riadenie = -1;
    로그인됨 = používateľ_OK = linka_zmeniť_veľkosť = 줄오류 = odozva_zmeniť_veľkosť = 응답전송량 = ukončiť_program = 0;
}
int prenos_súborov_riadenie(int Akcia) {
    if (Akcia == 2) return dostať_port >= 0;
    if (Akcia == 0) { odpojiť(); if (dostať_port >= 0) Zavrieť_sieť(dostať_port); dostať_port = -1; return 0; }
    if (Akcia != 1) return -22; if (dostať_port >= 0) return 0;
    dostať_port = Create_soket_účastník(1); if (dostať_port < 0) return dostať_port;
    int 반환값 = NET_BIND(dostať_port, 망상태읽기(0,0), 21); if (!반환값) 반환값 = NET_načúvať(dostať_port);
    if (반환값 < 0) { Zavrieť_sieť(dostať_port); dostať_port = -1; } return 반환값;
}
static int Cesta(const char *Názov) {
    unsigned položka_COUNT = 0; if (*Názov == '/') Názov++;
    if (!*Názov || 같은지(Názov, ".") || 같은지(Názov, "..")) return 0;
    Súbor_položka_názov[položka_COUNT++] = '/';
    while (*Názov) {
        unsigned char bod_kódu = *Názov++;
        if (položka_COUNT >= 63 || bod_kódu < 32 || bod_kódu == 127 || bod_kódu == '/' || bod_kódu == '\\') return 0;
        Súbor_položka_názov[položka_COUNT++] = bod_kódu;
    }
    Súbor_položka_názov[položka_COUNT] = 0; return 1;
}
static void odoslať_Zoznam(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int položka_COUNT = 자바파일항목길이(순번); if (položka_COUNT <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned položka_COUNT_8f7753a1 = strlen(앞부분); memcpy(prenos_Stav + 사용량, 앞부분, položka_COUNT_8f7753a1); 사용량 += položka_COUNT_8f7753a1;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)prenos_Stav, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        položka_COUNT_8f7753a1 = strlen(뒷부분); memcpy(prenos_Stav + 사용량, 뒷부분, položka_COUNT_8f7753a1); 사용량 += položka_COUNT_8f7753a1;
        for (int 안쪽순번 = 0; 안쪽순번 < položka_COUNT; 안쪽순번++) prenos_Stav[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        prenos_Stav[사용량++] = '\r'; prenos_Stav[사용량++] = '\n';
    }
}
static void Pripraviť_manuálny_kontakt(int 확장여부) {
    if (수행작업) { odozva("450 Transfer in progress\r\n"); return; }
    Stop_prenos(); manuálny_kontakt = Create_soket_účastník(1);
    if (manuálny_kontakt >= 0) 통신주소재사용(manuálny_kontakt);
    unsigned číslo_portu = 50000 + Ďalej_číslo_portu++ % 8;
    if (manuálny_kontakt < 0 || NET_BIND(manuálny_kontakt, 망상태읽기(0,0), číslo_portu) || NET_načúvať(manuálny_kontakt)) {
        Stop_prenos(); odozva("425 Cannot open passive listener\r\n"); return;
    }
    char odpoveď[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned položka_COUNT = strlen(앞부분); memcpy(odpoveď, 앞부분, položka_COUNT);
    if (확장여부) { 수치(číslo_portu, odpoveď, &položka_COUNT); odpoveď[položka_COUNT++] = '|'; }
    else {
        uint32_t adresa=망상태읽기(0,0);
        for (int pozičný_index=24;pozičný_index>=0;pozičný_index-=8) { 수치((adresa>>pozičný_index)&255,odpoveď,&položka_COUNT);odpoveď[položka_COUNT++]=','; }
        수치(číslo_portu / 256, odpoveď, &položka_COUNT); odpoveď[položka_COUNT++] = ','; 수치(číslo_portu % 256, odpoveď, &položka_COUNT);
    }
    odpoveď[položka_COUNT++] = ')'; odpoveď[položka_COUNT++] = '\r'; odpoveď[položka_COUNT++] = '\n'; odpoveď[položka_COUNT] = 0; odozva(odpoveď);
}
static void Príkaz(void) {
    riadok[linka_zmeniť_veľkosť] = 0;
    char *부가인수 = riadok; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(riadok, "QUIT")) { Stop_prenos(); odozva("221 Goodbye\r\n"); ukončiť_program = 1; return; }
    if (같은지(riadok, "NOOP")) { odozva("200 OK\r\n"); return; }
    if (같은지(riadok, "SYST")) { odozva("215 UNIX Type: L8\r\n"); return; }
    if (같은지(riadok, "FEAT")) { odozva("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(riadok, "USER")) { 로그인됨 = 0; používateľ_OK = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); odozva(používateľ_OK ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(riadok, "PASS")) { 로그인됨 = používateľ_OK; odozva(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { odozva("530 Login first\r\n"); return; }
    if (같은지(riadok, "PWD")) odozva("257 \"/\"\r\n");
    else if (같은지(riadok, "CWD")) odozva(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(riadok, "TYPE")) odozva(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(riadok, "OPTS")) odozva(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(riadok, "PASV")) Pripraviť_manuálny_kontakt(0);
    else if (같은지(riadok, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) odozva("522 IPv4 only\r\n"); else Pripraviť_manuálny_kontakt(1); }
    else if (같은지(riadok, "ABOR")) { Stop_prenos(); odozva("226 Transfer aborted\r\n"); }
    else if (같은지(riadok, "DELE")) { odozva(Cesta(부가인수) && pk_unlink(Súbor_položka_názov) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(riadok, "LIST") || 같은지(riadok, "NLST") || 같은지(riadok, "MLSD")) {
        if (수행작업) { odozva("450 Transfer in progress\r\n"); return; }
        if (manuálny_kontakt < 0 && údaje < 0) { odozva("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { odozva("550 Root listing only\r\n"); return; }
        odoslať_Zoznam(같은지(riadok,"MLSD") ? 2 : 같은지(riadok,"LIST") ? 1 : 0); 수행작업 = 2;
        odozva("150 Opening directory listing\r\n");
    }
    else if (같은지(riadok, "SIZE")) {
        if (!Cesta(부가인수)) { odozva("550 Invalid filename\r\n"); return; }
        int Súbor_rukoväť = pk_open(Súbor_položka_názov, iba_na_čítanie_VALUE, 0); if (Súbor_rukoväť < 0) { odozva("550 File unavailable\r\n"); return; }
        int Veľkosť = pk_size(Súbor_rukoväť); pk_close(Súbor_rukoväť); char odpoveď[32] = "213 "; unsigned položka_COUNT = 4;
        수치(Veľkosť, odpoveď, &položka_COUNT); odpoveď[položka_COUNT++] = '\r'; odpoveď[položka_COUNT++] = '\n'; odpoveď[položka_COUNT] = 0; odozva(odpoveď);
    } else if (같은지(riadok, "STOR") || 같은지(riadok, "RETR")) {
        if (수행작업) { odozva("450 Transfer in progress\r\n"); return; }
        if (manuálny_kontakt < 0 && údaje < 0) { odozva("425 Use PASV or EPSV\r\n"); return; }
        if (!Cesta(부가인수)) { odozva("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(riadok, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(prenos_názov, Súbor_položka_názov, strlen(Súbor_položka_názov) + 1);
        if (수행작업 == 2) {
            int Súbor_rukoväť = pk_open(Súbor_položka_názov, iba_na_čítanie_VALUE, 0);
            if (Súbor_rukoväť < 0) { 수행작업 = 0; odozva("550 File unavailable\r\n"); return; }
            int položka_COUNT = pk_read(Súbor_rukoväť, prenos_Stav, sizeof(prenos_Stav)); pk_close(Súbor_rukoväť);
            if (položka_COUNT < 0) { 수행작업 = 0; odozva("451 Read failed\r\n"); return; } 사용량 = položka_COUNT;
        }
        odozva("150 Opening binary data connection\r\n");
    } else odozva("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (dostať_port < 0) return;
    int Prichádzajúci_kontakt = NET_prijať(dostať_port);
    if (Prichádzajúci_kontakt >= 0) {
        if (riadenie >= 0) { NET_zapísať(Prichádzajúci_kontakt, "421 One session at a time\r\n", 27); Zavrieť_sieť(Prichádzajúci_kontakt); }
        else { riadenie = Prichádzajúci_kontakt; Aktivita = 보드밀리초(); odozva("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (riadenie < 0) return;
    if ((uint32_t)(보드밀리초() - Aktivita) > 60000) { odpojiť(); return; }
    if (!ukončiť_program) for (unsigned rozpočet = 0; rozpočet < 256; rozpočet++) {
        unsigned char bod_kódu; int 반환값 = 통신읽기(riadenie, &bod_kódu, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { odpojiť(); return; } Aktivita = 보드밀리초();
        if (bod_kódu == '\n') { if (줄오류) odozva("500 Command too long or invalid\r\n"); else Príkaz(); linka_zmeniť_veľkosť = 줄오류 = 0; if (ukončiť_program) break; }
        else if (bod_kódu != '\r') { if (!bod_kódu || linka_zmeniť_veľkosť >= sizeof(riadok) - 1) 줄오류 = 1; else riadok[linka_zmeniť_veľkosť++] = bod_kódu; }
    }
    if (manuálny_kontakt >= 0 && údaje < 0) {
        int 반환값 = NET_prijať(manuálny_kontakt);
        if (반환값 >= 0) {
            if (NET_partnerský_uzol_adresa(반환값) != NET_partnerský_uzol_adresa(riadenie)) Zavrieť_sieť(반환값);
            else { údaje = 반환값; Zavrieť_sieť(manuálny_kontakt); manuálny_kontakt = -1; Aktivita = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && údaje >= 0) for (unsigned rozpočet = 0; rozpočet < 8; rozpočet++) {
        unsigned char blok_údajov[512]; int položka_COUNT = 통신읽기(údaje, blok_údajov, sizeof(blok_údajov));
        if (položka_COUNT == -11) break;
        if (položka_COUNT < 0) { Stop_prenos(); odozva("426 Data connection failed\r\n"); break; }
        Aktivita = 보드밀리초();
        if (položka_COUNT == 0) {
            int KR = -1;
            if (!실패여부) {
                int Súbor_rukoväť = pk_open(prenos_názov, 쓰기전용 | 없으면만들기 | skrátiť_Obsah, 0600);
                if (Súbor_rukoväť >= 0) { KR = pk_write(Súbor_rukoväť, prenos_Stav, 사용량); pk_close(Súbor_rukoväť); }
            }
            int 성공여부 = !실패여부 && KR == (int)사용량; Stop_prenos(); odozva(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)položka_COUNT > sizeof(prenos_Stav) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(prenos_Stav + 사용량, blok_údajov, položka_COUNT); 사용량 += položka_COUNT; }
    }
    if (수행작업 == 2 && údaje >= 0) {
        int položka_COUNT = NET_zapísať(údaje, prenos_Stav + 보낸수, 사용량 - 보낸수);
        if (položka_COUNT >= 0) { 보낸수 += položka_COUNT; Aktivita = 보드밀리초(); if (보낸수 == 사용량) { Stop_prenos(); odozva("226 Transfer complete\r\n"); } }
        else if (položka_COUNT != -11) { Stop_prenos(); odozva("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < odozva_zmeniť_veľkosť) {
        int položka_COUNT = NET_zapísať(riadenie, 응답모음 + 응답전송량, odozva_zmeniť_veľkosť - 응답전송량);
        if (položka_COUNT > 0) 응답전송량 += položka_COUNT; else if (položka_COUNT != -11) { odpojiť(); return; }
    }
    if (응답전송량 == odozva_zmeniť_veľkosť) { odozva_zmeniť_veľkosť = 응답전송량 = 0; if (ukončiť_program) odpojiť(); }
}
