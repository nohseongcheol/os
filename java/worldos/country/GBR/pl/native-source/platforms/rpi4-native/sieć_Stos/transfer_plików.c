#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "sieć_Stos.h"
#include "string.h"
#include "Plik_ABI.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int odbierać_port = -1, kontrola = -1, 수동연결 = -1, dane = -1;
static unsigned 로그인됨, użytkownik_OK, linia_zmienić_rozmiar, 줄오류, zakończ_program, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned odpowiedź_zmienić_rozmiar, 응답전송량, Dalej_numer_portu;
static uint32_t Aktywność;
static char wiersz_wejścia[256], 응답모음[2048], Plik_wpis_nazwa[64], transfer_nazwa[64];
static unsigned char transfer_Stan[16384];
static int 같은지(const char *첫째값, const char *SEKUNDA_WARTOŚĆ) { while (*첫째값 && *첫째값 == *SEKUNDA_WARTOŚĆ) { 첫째값++; SEKUNDA_WARTOŚĆ++; } return *첫째값 == *SEKUNDA_WARTOŚĆ; }
static void odpowiedź(const char *ciąg_dane) {
    size_t towar_ILE_LICZB = strlen(ciąg_dane);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, odpowiedź_zmienić_rozmiar - 응답전송량); odpowiedź_zmienić_rozmiar -= 응답전송량; 응답전송량 = 0; }
    if (towar_ILE_LICZB > sizeof(응답모음) - odpowiedź_zmienić_rozmiar) { zakończ_program = 1; return; }
    memcpy(응답모음 + odpowiedź_zmienić_rozmiar, ciąg_dane, towar_ILE_LICZB); odpowiedź_zmienić_rozmiar += towar_ILE_LICZB;
}
static void 수치(unsigned WARTOŚĆ, char *KR_dane, unsigned *towar_ILE_LICZB) {
    char cyfra_ILE_LICZB[10]; unsigned wpis_ILE_LICZB = 0;
    do { cyfra_ILE_LICZB[wpis_ILE_LICZB++] = '0' + WARTOŚĆ % 10; WARTOŚĆ /= 10; } while (WARTOŚĆ);
    while (wpis_ILE_LICZB) KR_dane[(*towar_ILE_LICZB)++] = cyfra_ILE_LICZB[--wpis_ILE_LICZB];
}
static void Stop_transfer(void) {
    if (dane >= 0) Zamknij_sieć(dane); if (수동연결 >= 0) Zamknij_sieć(수동연결);
    dane = 수동연결 = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void rozłączać(void) {
    Stop_transfer(); if (kontrola >= 0) Zamknij_sieć(kontrola); kontrola = -1;
    로그인됨 = użytkownik_OK = linia_zmienić_rozmiar = 줄오류 = odpowiedź_zmienić_rozmiar = 응답전송량 = zakończ_program = 0;
}
int transfer_plików_kontrola(int Akcja) {
    if (Akcja == 2) return odbierać_port >= 0;
    if (Akcja == 0) { rozłączać(); if (odbierać_port >= 0) Zamknij_sieć(odbierać_port); odbierać_port = -1; return 0; }
    if (Akcja != 1) return -22; if (odbierać_port >= 0) return 0;
    odbierać_port = Twórca_gniazdo_uczestnik(1); if (odbierać_port < 0) return odbierać_port;
    int 반환값 = NET_BIND(odbierać_port, 망상태읽기(0,0), 21); if (!반환값) 반환값 = NET_nasłuchiwać(odbierać_port);
    if (반환값 < 0) { Zamknij_sieć(odbierać_port); odbierać_port = -1; } return 반환값;
}
static int ścieżka_2(const char *Nazwa) {
    unsigned towar_ILE_LICZB = 0; if (*Nazwa == '/') Nazwa++;
    if (!*Nazwa || 같은지(Nazwa, ".") || 같은지(Nazwa, "..")) return 0;
    Plik_wpis_nazwa[towar_ILE_LICZB++] = '/';
    while (*Nazwa) {
        unsigned char kod_znaku = *Nazwa++;
        if (towar_ILE_LICZB >= 63 || kod_znaku < 32 || kod_znaku == 127 || kod_znaku == '/' || kod_znaku == '\\') return 0;
        Plik_wpis_nazwa[towar_ILE_LICZB++] = kod_znaku;
    }
    Plik_wpis_nazwa[towar_ILE_LICZB] = 0; return 1;
}
static void wysłać_Lista(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int towar_ILE_LICZB = 자바파일항목길이(순번); if (towar_ILE_LICZB <= 0) continue;
        const char *interlinia_część = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned wpis_ILE_LICZB = strlen(interlinia_część); memcpy(transfer_Stan + 사용량, interlinia_część, wpis_ILE_LICZB); 사용량 += wpis_ILE_LICZB;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)transfer_Stan, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        wpis_ILE_LICZB = strlen(뒷부분); memcpy(transfer_Stan + 사용량, 뒷부분, wpis_ILE_LICZB); 사용량 += wpis_ILE_LICZB;
        for (int 안쪽순번 = 0; 안쪽순번 < towar_ILE_LICZB; 안쪽순번++) transfer_Stan[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        transfer_Stan[사용량++] = '\r'; transfer_Stan[사용량++] = '\n';
    }
}
static void 수동연결준비(int 확장여부) {
    if (수행작업) { odpowiedź("450 Transfer in progress\r\n"); return; }
    Stop_transfer(); 수동연결 = Twórca_gniazdo_uczestnik(1);
    if (수동연결 >= 0) 통신주소재사용(수동연결);
    unsigned numer_portu = 50000 + Dalej_numer_portu++ % 8;
    if (수동연결 < 0 || NET_BIND(수동연결, 망상태읽기(0,0), numer_portu) || NET_nasłuchiwać(수동연결)) {
        Stop_transfer(); odpowiedź("425 Cannot open passive listener\r\n"); return;
    }
    char odpowiedź_1262b476[96]; const char *interlinia_część = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned towar_ILE_LICZB = strlen(interlinia_część); memcpy(odpowiedź_1262b476, interlinia_część, towar_ILE_LICZB);
    if (확장여부) { 수치(numer_portu, odpowiedź_1262b476, &towar_ILE_LICZB); odpowiedź_1262b476[towar_ILE_LICZB++] = '|'; }
    else {
        uint32_t Adres=망상태읽기(0,0);
        for (int indeks_pozycji=24;indeks_pozycji>=0;indeks_pozycji-=8) { 수치((Adres>>indeks_pozycji)&255,odpowiedź_1262b476,&towar_ILE_LICZB);odpowiedź_1262b476[towar_ILE_LICZB++]=','; }
        수치(numer_portu / 256, odpowiedź_1262b476, &towar_ILE_LICZB); odpowiedź_1262b476[towar_ILE_LICZB++] = ','; 수치(numer_portu % 256, odpowiedź_1262b476, &towar_ILE_LICZB);
    }
    odpowiedź_1262b476[towar_ILE_LICZB++] = ')'; odpowiedź_1262b476[towar_ILE_LICZB++] = '\r'; odpowiedź_1262b476[towar_ILE_LICZB++] = '\n'; odpowiedź_1262b476[towar_ILE_LICZB] = 0; odpowiedź(odpowiedź_1262b476);
}
static void polecenie(void) {
    wiersz_wejścia[linia_zmienić_rozmiar] = 0;
    char *부가인수 = wiersz_wejścia; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(wiersz_wejścia, "QUIT")) { Stop_transfer(); odpowiedź("221 Goodbye\r\n"); zakończ_program = 1; return; }
    if (같은지(wiersz_wejścia, "NOOP")) { odpowiedź("200 OK\r\n"); return; }
    if (같은지(wiersz_wejścia, "SYST")) { odpowiedź("215 UNIX Type: L8\r\n"); return; }
    if (같은지(wiersz_wejścia, "FEAT")) { odpowiedź("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(wiersz_wejścia, "USER")) { 로그인됨 = 0; użytkownik_OK = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); odpowiedź(użytkownik_OK ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(wiersz_wejścia, "PASS")) { 로그인됨 = użytkownik_OK; odpowiedź(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { odpowiedź("530 Login first\r\n"); return; }
    if (같은지(wiersz_wejścia, "PWD")) odpowiedź("257 \"/\"\r\n");
    else if (같은지(wiersz_wejścia, "CWD")) odpowiedź(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(wiersz_wejścia, "TYPE")) odpowiedź(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(wiersz_wejścia, "OPTS")) odpowiedź(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(wiersz_wejścia, "PASV")) 수동연결준비(0);
    else if (같은지(wiersz_wejścia, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) odpowiedź("522 IPv4 only\r\n"); else 수동연결준비(1); }
    else if (같은지(wiersz_wejścia, "ABOR")) { Stop_transfer(); odpowiedź("226 Transfer aborted\r\n"); }
    else if (같은지(wiersz_wejścia, "DELE")) { odpowiedź(ścieżka_2(부가인수) && pk_unlink(Plik_wpis_nazwa) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(wiersz_wejścia, "LIST") || 같은지(wiersz_wejścia, "NLST") || 같은지(wiersz_wejścia, "MLSD")) {
        if (수행작업) { odpowiedź("450 Transfer in progress\r\n"); return; }
        if (수동연결 < 0 && dane < 0) { odpowiedź("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { odpowiedź("550 Root listing only\r\n"); return; }
        wysłać_Lista(같은지(wiersz_wejścia,"MLSD") ? 2 : 같은지(wiersz_wejścia,"LIST") ? 1 : 0); 수행작업 = 2;
        odpowiedź("150 Opening directory listing\r\n");
    }
    else if (같은지(wiersz_wejścia, "SIZE")) {
        if (!ścieżka_2(부가인수)) { odpowiedź("550 Invalid filename\r\n"); return; }
        int dojście_do_pliku = pk_open(Plik_wpis_nazwa, tylko_do_odczytu_WARTOŚĆ, 0); if (dojście_do_pliku < 0) { odpowiedź("550 File unavailable\r\n"); return; }
        int Rozmiar = pk_size(dojście_do_pliku); pk_close(dojście_do_pliku); char odpowiedź_1262b476[32] = "213 "; unsigned towar_ILE_LICZB = 4;
        수치(Rozmiar, odpowiedź_1262b476, &towar_ILE_LICZB); odpowiedź_1262b476[towar_ILE_LICZB++] = '\r'; odpowiedź_1262b476[towar_ILE_LICZB++] = '\n'; odpowiedź_1262b476[towar_ILE_LICZB] = 0; odpowiedź(odpowiedź_1262b476);
    } else if (같은지(wiersz_wejścia, "STOR") || 같은지(wiersz_wejścia, "RETR")) {
        if (수행작업) { odpowiedź("450 Transfer in progress\r\n"); return; }
        if (수동연결 < 0 && dane < 0) { odpowiedź("425 Use PASV or EPSV\r\n"); return; }
        if (!ścieżka_2(부가인수)) { odpowiedź("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(wiersz_wejścia, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(transfer_nazwa, Plik_wpis_nazwa, strlen(Plik_wpis_nazwa) + 1);
        if (수행작업 == 2) {
            int dojście_do_pliku = pk_open(Plik_wpis_nazwa, tylko_do_odczytu_WARTOŚĆ, 0);
            if (dojście_do_pliku < 0) { 수행작업 = 0; odpowiedź("550 File unavailable\r\n"); return; }
            int towar_ILE_LICZB = pk_read(dojście_do_pliku, transfer_Stan, sizeof(transfer_Stan)); pk_close(dojście_do_pliku);
            if (towar_ILE_LICZB < 0) { 수행작업 = 0; odpowiedź("451 Read failed\r\n"); return; } 사용량 = towar_ILE_LICZB;
        }
        odpowiedź("150 Opening binary data connection\r\n");
    } else odpowiedź("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (odbierać_port < 0) return;
    int przychodzące_połączenie = NET_akceptować(odbierać_port);
    if (przychodzące_połączenie >= 0) {
        if (kontrola >= 0) { NET_zapis(przychodzące_połączenie, "421 One session at a time\r\n", 27); Zamknij_sieć(przychodzące_połączenie); }
        else { kontrola = przychodzące_połączenie; Aktywność = 보드밀리초(); odpowiedź("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (kontrola < 0) return;
    if ((uint32_t)(보드밀리초() - Aktywność) > 60000) { rozłączać(); return; }
    if (!zakończ_program) for (unsigned budżet = 0; budżet < 256; budżet++) {
        unsigned char kod_znaku; int 반환값 = 통신읽기(kontrola, &kod_znaku, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { rozłączać(); return; } Aktywność = 보드밀리초();
        if (kod_znaku == '\n') { if (줄오류) odpowiedź("500 Command too long or invalid\r\n"); else polecenie(); linia_zmienić_rozmiar = 줄오류 = 0; if (zakończ_program) break; }
        else if (kod_znaku != '\r') { if (!kod_znaku || linia_zmienić_rozmiar >= sizeof(wiersz_wejścia) - 1) 줄오류 = 1; else wiersz_wejścia[linia_zmienić_rozmiar++] = kod_znaku; }
    }
    if (수동연결 >= 0 && dane < 0) {
        int 반환값 = NET_akceptować(수동연결);
        if (반환값 >= 0) {
            if (NET_węzeł_równorzędny_ADRES(반환값) != NET_węzeł_równorzędny_ADRES(kontrola)) Zamknij_sieć(반환값);
            else { dane = 반환값; Zamknij_sieć(수동연결); 수동연결 = -1; Aktywność = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && dane >= 0) for (unsigned budżet = 0; budżet < 8; budżet++) {
        unsigned char blok_danych[512]; int towar_ILE_LICZB = 통신읽기(dane, blok_danych, sizeof(blok_danych));
        if (towar_ILE_LICZB == -11) break;
        if (towar_ILE_LICZB < 0) { Stop_transfer(); odpowiedź("426 Data connection failed\r\n"); break; }
        Aktywność = 보드밀리초();
        if (towar_ILE_LICZB == 0) {
            int WYNIK = -1;
            if (!실패여부) {
                int dojście_do_pliku = pk_open(transfer_nazwa, tylko_do_zapisu_WARTOŚĆ | 없으면만들기 | obcinać_Spis_treści, 0600);
                if (dojście_do_pliku >= 0) { WYNIK = pk_write(dojście_do_pliku, transfer_Stan, 사용량); pk_close(dojście_do_pliku); }
            }
            int 성공여부 = !실패여부 && WYNIK == (int)사용량; Stop_transfer(); odpowiedź(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)towar_ILE_LICZB > sizeof(transfer_Stan) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(transfer_Stan + 사용량, blok_danych, towar_ILE_LICZB); 사용량 += towar_ILE_LICZB; }
    }
    if (수행작업 == 2 && dane >= 0) {
        int towar_ILE_LICZB = NET_zapis(dane, transfer_Stan + 보낸수, 사용량 - 보낸수);
        if (towar_ILE_LICZB >= 0) { 보낸수 += towar_ILE_LICZB; Aktywność = 보드밀리초(); if (보낸수 == 사용량) { Stop_transfer(); odpowiedź("226 Transfer complete\r\n"); } }
        else if (towar_ILE_LICZB != -11) { Stop_transfer(); odpowiedź("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < odpowiedź_zmienić_rozmiar) {
        int towar_ILE_LICZB = NET_zapis(kontrola, 응답모음 + 응답전송량, odpowiedź_zmienić_rozmiar - 응답전송량);
        if (towar_ILE_LICZB > 0) 응답전송량 += towar_ILE_LICZB; else if (towar_ILE_LICZB != -11) { rozłączać(); return; }
    }
    if (응답전송량 == odpowiedź_zmienić_rozmiar) { odpowiedź_zmienić_rozmiar = 응답전송량 = 0; if (zakończ_program) rozłączać(); }
}
