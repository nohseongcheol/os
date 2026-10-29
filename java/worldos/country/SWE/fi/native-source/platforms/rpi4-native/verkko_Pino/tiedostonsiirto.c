#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "verkko_Pino.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int saada_portti = -1, ohjain = -1, manuaalinen_yhteys = -1, data = -1;
static unsigned 로그인됨, käyttäjä_OK, rivi_muuttaa_kokoa, 줄오류, lopeta_ohjelma, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned palaute_muuttaa_kokoa, 응답전송량, Seuraava_portin_numero;
static uint32_t tehtävä;
static char syöterivi[256], 응답모음[2048], Tiedosto_merkintä_nimi[64], Siirrä_nimi[64];
static unsigned char Siirrä_Tila[16384];
static int 같은지(const char *첫째값, const char *SEKUNNIT_ARVO) { while (*첫째값 && *첫째값 == *SEKUNNIT_ARVO) { 첫째값++; SEKUNNIT_ARVO++; } return *첫째값 == *SEKUNNIT_ARVO; }
static void palaute(const char *merkkijono_data) {
    size_t kohde_LASKE = strlen(merkkijono_data);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, palaute_muuttaa_kokoa - 응답전송량); palaute_muuttaa_kokoa -= 응답전송량; 응답전송량 = 0; }
    if (kohde_LASKE > sizeof(응답모음) - palaute_muuttaa_kokoa) { lopeta_ohjelma = 1; return; }
    memcpy(응답모음 + palaute_muuttaa_kokoa, merkkijono_data, kohde_LASKE); palaute_muuttaa_kokoa += kohde_LASKE;
}
static void 수치(unsigned ARVO, char *KR_data, unsigned *kohde_LASKE) {
    char numero_LASKE[10]; unsigned merkintä_LASKE = 0;
    do { numero_LASKE[merkintä_LASKE++] = '0' + ARVO % 10; ARVO /= 10; } while (ARVO);
    while (merkintä_LASKE) KR_data[(*kohde_LASKE)++] = numero_LASKE[--merkintä_LASKE];
}
static void Seis_Siirrä(void) {
    if (data >= 0) Sulje_verkko(data); if (manuaalinen_yhteys >= 0) Sulje_verkko(manuaalinen_yhteys);
    data = manuaalinen_yhteys = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void katkaise(void) {
    Seis_Siirrä(); if (ohjain >= 0) Sulje_verkko(ohjain); ohjain = -1;
    로그인됨 = käyttäjä_OK = rivi_muuttaa_kokoa = 줄오류 = palaute_muuttaa_kokoa = 응답전송량 = lopeta_ohjelma = 0;
}
int tiedostonsiirto_ohjain(int Toiminto) {
    if (Toiminto == 2) return saada_portti >= 0;
    if (Toiminto == 0) { katkaise(); if (saada_portti >= 0) Sulje_verkko(saada_portti); saada_portti = -1; return 0; }
    if (Toiminto != 1) return -22; if (saada_portti >= 0) return 0;
    saada_portti = Luo_vastake_päätepiste(1); if (saada_portti < 0) return saada_portti;
    int 반환값 = NET_BIND(saada_portti, lukea_verkko_tila(0,0), 21); if (!반환값) 반환값 = NET_kuunnella(saada_portti);
    if (반환값 < 0) { Sulje_verkko(saada_portti); saada_portti = -1; } return 반환값;
}
static int polku_2(const char *Nimi) {
    unsigned kohde_LASKE = 0; if (*Nimi == '/') Nimi++;
    if (!*Nimi || 같은지(Nimi, ".") || 같은지(Nimi, "..")) return 0;
    Tiedosto_merkintä_nimi[kohde_LASKE++] = '/';
    while (*Nimi) {
        unsigned char merkkikoodi = *Nimi++;
        if (kohde_LASKE >= 63 || merkkikoodi < 32 || merkkikoodi == 127 || merkkikoodi == '/' || merkkikoodi == '\\') return 0;
        Tiedosto_merkintä_nimi[kohde_LASKE++] = merkkikoodi;
    }
    Tiedosto_merkintä_nimi[kohde_LASKE] = 0; return 1;
}
static void lähettää_luettelo(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int kohde_LASKE = 자바파일항목길이(순번); if (kohde_LASKE <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned merkintä_LASKE = strlen(앞부분); memcpy(Siirrä_Tila + 사용량, 앞부분, merkintä_LASKE); 사용량 += merkintä_LASKE;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)Siirrä_Tila, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        merkintä_LASKE = strlen(뒷부분); memcpy(Siirrä_Tila + 사용량, 뒷부분, merkintä_LASKE); 사용량 += merkintä_LASKE;
        for (int 안쪽순번 = 0; 안쪽순번 < kohde_LASKE; 안쪽순번++) Siirrä_Tila[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        Siirrä_Tila[사용량++] = '\r'; Siirrä_Tila[사용량++] = '\n';
    }
}
static void Valmistele_manuaalinen_yhteys(int 확장여부) {
    if (수행작업) { palaute("450 Transfer in progress\r\n"); return; }
    Seis_Siirrä(); manuaalinen_yhteys = Luo_vastake_päätepiste(1);
    if (manuaalinen_yhteys >= 0) 통신주소재사용(manuaalinen_yhteys);
    unsigned portin_numero = 50000 + Seuraava_portin_numero++ % 8;
    if (manuaalinen_yhteys < 0 || NET_BIND(manuaalinen_yhteys, lukea_verkko_tila(0,0), portin_numero) || NET_kuunnella(manuaalinen_yhteys)) {
        Seis_Siirrä(); palaute("425 Cannot open passive listener\r\n"); return;
    }
    char vastaus[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned kohde_LASKE = strlen(앞부분); memcpy(vastaus, 앞부분, kohde_LASKE);
    if (확장여부) { 수치(portin_numero, vastaus, &kohde_LASKE); vastaus[kohde_LASKE++] = '|'; }
    else {
        uint32_t OSOITE=lukea_verkko_tila(0,0);
        for (int sijainti=24;sijainti>=0;sijainti-=8) { 수치((OSOITE>>sijainti)&255,vastaus,&kohde_LASKE);vastaus[kohde_LASKE++]=','; }
        수치(portin_numero / 256, vastaus, &kohde_LASKE); vastaus[kohde_LASKE++] = ','; 수치(portin_numero % 256, vastaus, &kohde_LASKE);
    }
    vastaus[kohde_LASKE++] = ')'; vastaus[kohde_LASKE++] = '\r'; vastaus[kohde_LASKE++] = '\n'; vastaus[kohde_LASKE] = 0; palaute(vastaus);
}
static void komento(void) {
    syöterivi[rivi_muuttaa_kokoa] = 0;
    char *부가인수 = syöterivi; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(syöterivi, "QUIT")) { Seis_Siirrä(); palaute("221 Goodbye\r\n"); lopeta_ohjelma = 1; return; }
    if (같은지(syöterivi, "NOOP")) { palaute("200 OK\r\n"); return; }
    if (같은지(syöterivi, "SYST")) { palaute("215 UNIX Type: L8\r\n"); return; }
    if (같은지(syöterivi, "FEAT")) { palaute("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(syöterivi, "USER")) { 로그인됨 = 0; käyttäjä_OK = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); palaute(käyttäjä_OK ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(syöterivi, "PASS")) { 로그인됨 = käyttäjä_OK; palaute(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { palaute("530 Login first\r\n"); return; }
    if (같은지(syöterivi, "PWD")) palaute("257 \"/\"\r\n");
    else if (같은지(syöterivi, "CWD")) palaute(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(syöterivi, "TYPE")) palaute(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(syöterivi, "OPTS")) palaute(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(syöterivi, "PASV")) Valmistele_manuaalinen_yhteys(0);
    else if (같은지(syöterivi, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) palaute("522 IPv4 only\r\n"); else Valmistele_manuaalinen_yhteys(1); }
    else if (같은지(syöterivi, "ABOR")) { Seis_Siirrä(); palaute("226 Transfer aborted\r\n"); }
    else if (같은지(syöterivi, "DELE")) { palaute(polku_2(부가인수) && pk_unlink(Tiedosto_merkintä_nimi) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(syöterivi, "LIST") || 같은지(syöterivi, "NLST") || 같은지(syöterivi, "MLSD")) {
        if (수행작업) { palaute("450 Transfer in progress\r\n"); return; }
        if (manuaalinen_yhteys < 0 && data < 0) { palaute("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { palaute("550 Root listing only\r\n"); return; }
        lähettää_luettelo(같은지(syöterivi,"MLSD") ? 2 : 같은지(syöterivi,"LIST") ? 1 : 0); 수행작업 = 2;
        palaute("150 Opening directory listing\r\n");
    }
    else if (같은지(syöterivi, "SIZE")) {
        if (!polku_2(부가인수)) { palaute("550 Invalid filename\r\n"); return; }
        int Tiedosto_kahva = pk_open(Tiedosto_merkintä_nimi, vain_luku_ARVO, 0); if (Tiedosto_kahva < 0) { palaute("550 File unavailable\r\n"); return; }
        int Koko = pk_size(Tiedosto_kahva); pk_close(Tiedosto_kahva); char vastaus[32] = "213 "; unsigned kohde_LASKE = 4;
        수치(Koko, vastaus, &kohde_LASKE); vastaus[kohde_LASKE++] = '\r'; vastaus[kohde_LASKE++] = '\n'; vastaus[kohde_LASKE] = 0; palaute(vastaus);
    } else if (같은지(syöterivi, "STOR") || 같은지(syöterivi, "RETR")) {
        if (수행작업) { palaute("450 Transfer in progress\r\n"); return; }
        if (manuaalinen_yhteys < 0 && data < 0) { palaute("425 Use PASV or EPSV\r\n"); return; }
        if (!polku_2(부가인수)) { palaute("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(syöterivi, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(Siirrä_nimi, Tiedosto_merkintä_nimi, strlen(Tiedosto_merkintä_nimi) + 1);
        if (수행작업 == 2) {
            int Tiedosto_kahva = pk_open(Tiedosto_merkintä_nimi, vain_luku_ARVO, 0);
            if (Tiedosto_kahva < 0) { 수행작업 = 0; palaute("550 File unavailable\r\n"); return; }
            int kohde_LASKE = pk_read(Tiedosto_kahva, Siirrä_Tila, sizeof(Siirrä_Tila)); pk_close(Tiedosto_kahva);
            if (kohde_LASKE < 0) { 수행작업 = 0; palaute("451 Read failed\r\n"); return; } 사용량 = kohde_LASKE;
        }
        palaute("150 Opening binary data connection\r\n");
    } else palaute("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (saada_portti < 0) return;
    int Vastattu_yhteys = NET_hyväksyä(saada_portti);
    if (Vastattu_yhteys >= 0) {
        if (ohjain >= 0) { NET_kirjoitus(Vastattu_yhteys, "421 One session at a time\r\n", 27); Sulje_verkko(Vastattu_yhteys); }
        else { ohjain = Vastattu_yhteys; tehtävä = 보드밀리초(); palaute("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (ohjain < 0) return;
    if ((uint32_t)(보드밀리초() - tehtävä) > 60000) { katkaise(); return; }
    if (!lopeta_ohjelma) for (unsigned budjetti = 0; budjetti < 256; budjetti++) {
        unsigned char merkkikoodi; int 반환값 = NET_lukea(ohjain, &merkkikoodi, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { katkaise(); return; } tehtävä = 보드밀리초();
        if (merkkikoodi == '\n') { if (줄오류) palaute("500 Command too long or invalid\r\n"); else komento(); rivi_muuttaa_kokoa = 줄오류 = 0; if (lopeta_ohjelma) break; }
        else if (merkkikoodi != '\r') { if (!merkkikoodi || rivi_muuttaa_kokoa >= sizeof(syöterivi) - 1) 줄오류 = 1; else syöterivi[rivi_muuttaa_kokoa++] = merkkikoodi; }
    }
    if (manuaalinen_yhteys >= 0 && data < 0) {
        int 반환값 = NET_hyväksyä(manuaalinen_yhteys);
        if (반환값 >= 0) {
            if (NET_vertaissolmu_OSOITE(반환값) != NET_vertaissolmu_OSOITE(ohjain)) Sulje_verkko(반환값);
            else { data = 반환값; Sulje_verkko(manuaalinen_yhteys); manuaalinen_yhteys = -1; tehtävä = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && data >= 0) for (unsigned budjetti = 0; budjetti < 8; budjetti++) {
        unsigned char tietolohko[512]; int kohde_LASKE = NET_lukea(data, tietolohko, sizeof(tietolohko));
        if (kohde_LASKE == -11) break;
        if (kohde_LASKE < 0) { Seis_Siirrä(); palaute("426 Data connection failed\r\n"); break; }
        tehtävä = 보드밀리초();
        if (kohde_LASKE == 0) {
            int TULOS = -1;
            if (!실패여부) {
                int Tiedosto_kahva = pk_open(Siirrä_nimi, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (Tiedosto_kahva >= 0) { TULOS = pk_write(Tiedosto_kahva, Siirrä_Tila, 사용량); pk_close(Tiedosto_kahva); }
            }
            int 성공여부 = !실패여부 && TULOS == (int)사용량; Seis_Siirrä(); palaute(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)kohde_LASKE > sizeof(Siirrä_Tila) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(Siirrä_Tila + 사용량, tietolohko, kohde_LASKE); 사용량 += kohde_LASKE; }
    }
    if (수행작업 == 2 && data >= 0) {
        int kohde_LASKE = NET_kirjoitus(data, Siirrä_Tila + 보낸수, 사용량 - 보낸수);
        if (kohde_LASKE >= 0) { 보낸수 += kohde_LASKE; tehtävä = 보드밀리초(); if (보낸수 == 사용량) { Seis_Siirrä(); palaute("226 Transfer complete\r\n"); } }
        else if (kohde_LASKE != -11) { Seis_Siirrä(); palaute("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < palaute_muuttaa_kokoa) {
        int kohde_LASKE = NET_kirjoitus(ohjain, 응답모음 + 응답전송량, palaute_muuttaa_kokoa - 응답전송량);
        if (kohde_LASKE > 0) 응답전송량 += kohde_LASKE; else if (kohde_LASKE != -11) { katkaise(); return; }
    }
    if (응답전송량 == palaute_muuttaa_kokoa) { palaute_muuttaa_kokoa = 응답전송량 = 0; if (lopeta_ohjelma) katkaise(); }
}
