#include "File_ABI.h"
#include "호출.h"
static int inizializzatore_VALORE;
static volatile int inizializzatore_seme = 72;
static volatile double virgola_mobile_seme = 1.25;
static int 소멸횟수;
struct test_inizializzazione { test_inizializzazione() { inizializzatore_VALORE = inizializzatore_seme + 1; } } 정적초기화;
class Automatico_File {
    int INDICE;
public:
    explicit Automatico_File(const char *Nome) : INDICE(aperto_File(Nome, in_lettura_scrittura | 없으면만들기 | tagliare_Sommario, 0600)) {}
    ~Automatico_File() { if (INDICE >= 0) Chiudi_File(INDICE); 소멸횟수++; }
    int descrittore_voce() const { return INDICE; }
};
extern "C" int START_USER_app(int) {
    if (inizializzatore_VALORE != 73 || 사용자호출(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double virgola_mobile_VALORE = virgola_mobile_seme * 2.0 + 0.5;
    if (사용자호출(0, 0, 0, 0, 0, 0, 0) != 1 || virgola_mobile_VALORE != 3.0) return 16;
    static const char Contenuto_VALORE[] = "EL0 C++ → posix-kor → Java file · 안녕하세요 😀\n";
    char 읽은값[sizeof(Contenuto_VALORE)] = {};
    {
        Automatico_File file("spazio_utente.txt");
        int INDICE = file.descrittore_voce();
        if (INDICE < 0 || scrivere_File_dati(INDICE, Contenuto_VALORE, sizeof(Contenuto_VALORE)) != sizeof(Contenuto_VALORE)) return 2;
        if (cercare_File(INDICE, 0, 처음기준) || 파일자료읽기(INDICE, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 3;
        for (unsigned 순번 = 0; 순번 < sizeof(Contenuto_VALORE); 순번++) if (읽은값[순번] != Contenuto_VALORE[순번]) return 4;
    }
    if (소멸횟수 != 1) return 5;
    if (scrivere_File_dati(1, Contenuto_VALORE, sizeof(Contenuto_VALORE) - 1) != sizeof(Contenuto_VALORE) - 1) return 6;
    uintptr_t 바닥 = USER_Memoria_chiudere(0);
    if (바닥 != 0x02c00000 || USER_Memoria_chiudere(바닥 + 8192) != (intptr_t)(바닥 + 8192)) return 7;
    volatile unsigned char *Memoria_VALORE = (volatile unsigned char *)바닥;
    if (Memoria_VALORE[0] || Memoria_VALORE[8191]) return 8;
    Memoria_VALORE[8191] = 137;
    if (USER_Memoria_chiudere(바닥) != (intptr_t)바닥 || USER_Memoria_chiudere(바닥 + 8192) != (intptr_t)(바닥 + 8192) || Memoria_VALORE[8191]) return 9;
    // 잘못된 spazio_utente puntatore/번호는 오류이며 커널을 중단하지 않는다.
    if (scrivere_File_dati(1, (const void *)0x80000, 8) != -1 || numero_errore != 14) return 10;
    if (파일자료읽기(0, (void *)Contenuto_VALORE, 1) != -1 || numero_errore != 14) return 11;
    if (사용자호출(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t 화면폭 = 화면너비읽기(), schermata_durata = 화면높이읽기();
    if (화면폭 <= 0 || schermata_durata <= 0 || 사용자호출(13, 화면폭-1, schermata_durata-1, 0, 2, 2, 0) != -22) return 13;
    if (schermata_rettangolo(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 Esci_app 시 열린 서술자가 자동 정리되어야 한다.
    if (aperto_File("spazio_utente.txt", di_sola_lettura_VALORE) < 0) return 15;
    return 0;
}
