#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 Wykonaj_polecenie maszyna warstwa_WARTOŚĆ. nazwa_pliku dane/정책은 기존 AOT Java 커널에 위임한다.
#include "przestrzeń_użytkownika.h"
#include "Plik_ABI.h"
#include "sieć_ABI.h"
#include "../sieć_Stos/sieć_Stos.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define maszyna_rejestr(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define przerwanie_dystrybutor 0xff841000ul
#define przerwanie_CPU_interfejs 0xff842000ul
#define rozmiar_strony 4096ul
#define dostęp_pisak (1ul << 10)
#define nie_Wykonaj_pozwolenie (1ul << 53)
#define użytkownik_nie_Wykonaj (1ul << 54)
#define zwykła_Pamięć ((1ul << 2) | (3ul << 8) | dostęp_pisak)
#define jądro_strona (3ul | zwykła_Pamięć | nie_Wykonaj_pozwolenie | użytkownik_nie_Wykonaj)
#define użytkownik_R_W (3ul | zwykła_Pamięć | (1ul << 6) | nie_Wykonaj_pozwolenie | użytkownik_nie_Wykonaj)
#define użytkownik_tylko_do_odczytu (3ul | zwykła_Pamięć | (3ul << 6) | nie_Wykonaj_pozwolenie | użytkownik_nie_Wykonaj)
#define 사용자읽고실행 (3ul | zwykła_Pamięć | (3ul << 6) | nie_Wykonaj_pozwolenie)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t Tablica_piksel(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t Tablica_Terminal(uintptr_t);
extern int Terminal_oczekujący(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int użytkownik_CV(użytkownik_kadr *,void *);
extern void 사용자실수보관(void *);
extern int użytkownik_wprowadzić(uintptr_t punkt_wejścia, uintptr_t pamięć_stosu, uintptr_t 전달값);
extern void użytkownik_Zwrot(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t korzeń_ADRES[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t strona_Lista[użytkownik_strona_ILE_LICZB] __attribute__((aligned(4096)));
static uint8_t Uprawnienia_Lista[użytkownik_strona_ILE_LICZB];
static int Aktywny, lista_plików[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int Zamknij_gniazdo_uczestnik(unsigned dojście_do_pliku){return dojście_do_pliku<40?자바전문닫기(dojście_do_pliku):자바흐름닫기(dojście_do_pliku);}
static uint64_t CZĘSTOŚĆ, termin_ostateczny_CZAS;
static uintptr_t sterta_Koniec;
// jądro_WARTOŚĆ 셸이 준비한 UTF-8 argumenty. EL0에는 kopiować_WARTOŚĆ 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int wstrzymany_Stan,interakcyjny,리눅스규약,lista_plików[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char argument_TABLICA[8][256],Uprawnienia_Lista[użytkownik_strona_ILE_LICZB];
    uintptr_t pamięć_dynamiczna; użytkownik_kadr wykonanie_kadr;
    unsigned char liczba_zmiennoprzecinkowa_Stan[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int właściciel_obiekt,interakcyjny;
static uint32_t numer_użytkownika[4], użytkownik_START_CZAS[4], 사용자누적시각[4], użytkownik_wykonanie_CZAS[4], Dalej_numer_użytkownika=10;
static unsigned char użytkownik_polecenie_nazwa[4][288];
uint32_t 사용자상태읽기(unsigned wpis_WARTOŚĆ, unsigned INDEKS) {
    unsigned indeks_pozycji=INDEKS&3;
    int Stan_WARTOŚĆ=(Aktywny && właściciel_obiekt==(int)indeks_pozycji) ? 1 : 저장값[indeks_pozycji].wstrzymany_Stan ? 2 : 0;
    if (wpis_WARTOŚĆ==0) return Stan_WARTOŚĆ;
    if (!Stan_WARTOŚĆ) return 0;
    if (wpis_WARTOŚĆ==1) return numer_użytkownika[indeks_pozycji];
    if (wpis_WARTOŚĆ==2) {
        unsigned char *쪽들=Stan_WARTOŚĆ==1?Uprawnienia_Lista:저장값[indeks_pozycji].Uprawnienia_Lista;
        unsigned strona_ILE_LICZB=0; for (unsigned 순번=0; 순번<użytkownik_strona_ILE_LICZB; 순번++) if(쪽들[순번]) strona_ILE_LICZB++;
        return strona_ILE_LICZB*4;
    }
    if (wpis_WARTOŚĆ==3) return (uint32_t)보드밀리초()-użytkownik_START_CZAS[indeks_pozycji];
    if (wpis_WARTOŚĆ==4) return 사용자누적시각[indeks_pozycji]+(Stan_WARTOŚĆ==1?(uint32_t)보드밀리초()-użytkownik_wykonanie_CZAS[indeks_pozycji]:0);
    if (wpis_WARTOŚĆ==5) return INDEKS/4<sizeof(użytkownik_polecenie_nazwa[0])?użytkownik_polecenie_nazwa[indeks_pozycji][INDEKS/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t wpis_ILE_LICZB) {
    if (Aktywny || wpis_ILE_LICZB > 8) return (uint32_t)-22;
    전달인수개수 = wpis_ILE_LICZB;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t WYSZUKAJ_INDEKS, uintptr_t bieżący_stanowisko, uintptr_t bajt_dane) {
    if (Aktywny || WYSZUKAJ_INDEKS >= 전달인수개수 || bieżący_stanowisko >= 255 || bieżący_stanowisko != 전달인수길이[WYSZUKAJ_INDEKS] || !bajt_dane || bajt_dane > 255)
        return (uint32_t)-22;
    전달인수[WYSZUKAJ_INDEKS][bieżący_stanowisko] = bajt_dane;
    전달인수길이[WYSZUKAJ_INDEKS] = bieżący_stanowisko + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Zegar_WARTOŚĆ(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Stop_TIMEOUT(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    maszyna_rejestr(przerwanie_dystrybutor + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void START_TIMEOUT(void) {
    uint64_t 간격 = CZĘSTOŚĆ * 2, włączyć = 1;
    termin_ostateczny_CZAS = Zegar_WARTOŚĆ() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(włączyć) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned blok_danych = 0; blok_danych < 4; blok_danych++) {
        korzeń_ADRES[blok_danych] = (uintptr_t)가운데[blok_danych] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t Adres = ((uintptr_t)blok_danych << 30) | ((uintptr_t)순번 << 21);
            가운데[blok_danych][순번] = Adres | 1 | dostęp_pisak | użytkownik_nie_Wykonaj;
            if (Adres >= 0xfc000000ul) 가운데[blok_danych][순번] |= nie_Wykonaj_pozwolenie; // Device-nGnRnE
            else 가운데[blok_danych][순번] |= zwykła_Pamięć; // Normal, non-cacheable
        }
    }
    for (unsigned SEKUNDA_WARTOŚĆ = 0; SEKUNDA_WARTOŚĆ < użytkownik_strona_ILE_LICZB / 512; SEKUNDA_WARTOŚĆ++)
        가운데[0][(użytkownik_baza >> 21) + SEKUNDA_WARTOŚĆ] = (uintptr_t)(strona_Lista + SEKUNDA_WARTOŚĆ * 512) | 3;
    for (unsigned 순번 = 0; 순번 < użytkownik_strona_ILE_LICZB; 순번++) strona_Lista[순번] = (użytkownik_baza + 순번 * rozmiar_strony) | jądro_strona;
    uint64_t Pamięć_atrybut_rejestr = 0x4400, ADRES_translacja_kontrola = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Pamięć_atrybut_rejestr), "r"(ADRES_translacja_kontrola), "r"((uintptr_t)korzeń_ADRES) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t liczba_zmiennoprzecinkowa_Stan = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(liczba_zmiennoprzecinkowa_Stan) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(CZĘSTOŚĆ));
    Stop_TIMEOUT();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 punkt_wejścia_WARTOŚĆ 때만 Zezwalaj_WARTOŚĆ.
    maszyna_rejestr(przerwanie_dystrybutor) = 0;
    maszyna_rejestr(przerwanie_dystrybutor + 0x180) = 0xffffffff;
    maszyna_rejestr(przerwanie_dystrybutor + 0x80) = 0xffffffff;
    maszyna_rejestr(przerwanie_dystrybutor + 0x280) = 1u << 30;
    maszyna_rejestr(przerwanie_dystrybutor + 0x41c) = 0x80808080;
    maszyna_rejestr(przerwanie_dystrybutor + 0x100) = 1u << 30;
    maszyna_rejestr(przerwanie_CPU_interfejs + 4) = 0xff;
    maszyna_rejestr(przerwanie_CPU_interfejs + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 systemy_informacyjne_zwykła 확인할 identyfikator 있다.
    int Zabezpieczenia = (maszyna_rejestr(przerwanie_dystrybutor + 4) & (1u << 10)) != 0;
    maszyna_rejestr(przerwanie_dystrybutor) = Zabezpieczenia ? 1 : 3;
    maszyna_rejestr(przerwanie_CPU_interfejs) = Zabezpieczenia ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t TYP_obszar, maszyna_TYP; uint32_t numer_wersji;
    uint64_t punkt_wejścia, program_Nagłówek_przesunąć, nagłówek_sekcji_przesunąć; uint32_t konfiguracja_BITS;
    uint16_t wykonywalny_Nagłówek_zmienić_rozmiar, program_Nagłówek_wpis_zmienić_rozmiar, program_Nagłówek_ILE_LICZB, nagłówek_sekcji_wpis_zmienić_rozmiar, nagłówek_sekcji_ILE_LICZB, obszar_nazwa_tabela_INDEKS;
} 실행파일머리;
typedef struct { uint32_t TYP_obszar, konfiguracja_BITS; uint64_t przesunąć_WARTOŚĆ_450fc799, Adres, 물리주소, 파일영역크기, 기억영역크기, wyrównać_granica; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(użytkownik_kadr) == 272, "exception assembly layout");
static int 포함된범위(uint64_t przesunąć_WARTOŚĆ_450fc799, uint64_t Rozmiar, uint64_t Koniec_przesunąć) {
    return przesunąć_WARTOŚĆ_450fc799 <= Koniec_przesunąć && Rozmiar <= Koniec_przesunąć - przesunąć_WARTOŚĆ_450fc799;
}
static int 부가정보검사(const unsigned char *dane_stanowisko, size_t Rozmiar) {
    size_t bieżący_stanowisko = 0;
    while (포함된범위(bieżący_stanowisko, 12, Rozmiar)) {
        uint32_t 낱말들[3]; memcpy(낱말들, dane_stanowisko + bieżący_stanowisko, 12); bieżący_stanowisko += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(bieżący_stanowisko, 이름영역크기, Rozmiar) || !포함된범위(bieżący_stanowisko + 이름영역크기, 설명크기, Rozmiar)) return 0;
        const unsigned char Nazwa[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Nazwa) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Nazwa); 순번++) if (dane_stanowisko[bieżący_stanowisko + 순번] != Nazwa[순번]) 일치 = 0;
        uint32_t numer_wersji = 0;
        if (일치) memcpy(&numer_wersji, dane_stanowisko + bieżący_stanowisko + 이름영역크기, 4);
        if (일치 && numer_wersji == 1) return 1;
        bieżący_stanowisko += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *dane, size_t Rozmiar, int 리눅스방식) {
    if (Rozmiar < sizeof(실행파일머리)) return użytkownik_wykonywalny_błąd;
    실행파일머리 wykonywalny_Nagłówek; memcpy(&wykonywalny_Nagłówek, dane, sizeof(wykonywalny_Nagłówek));
    if (wykonywalny_Nagłówek.형식식별[0] != 127 || wykonywalny_Nagłówek.형식식별[1] != 'E' || wykonywalny_Nagłówek.형식식별[2] != 'L' || wykonywalny_Nagłówek.형식식별[3] != 'F' ||
        wykonywalny_Nagłówek.형식식별[4] != 2 || wykonywalny_Nagłówek.형식식별[5] != 1 || wykonywalny_Nagłówek.형식식별[6] != 1 || (wykonywalny_Nagłówek.형식식별[7] != 0 && (!리눅스방식 || wykonywalny_Nagłówek.형식식별[7] != 3)) ||
        wykonywalny_Nagłówek.TYP_obszar != 2 || wykonywalny_Nagłówek.maszyna_TYP != 183 || wykonywalny_Nagłówek.numer_wersji != 1 || wykonywalny_Nagłówek.konfiguracja_BITS || wykonywalny_Nagłówek.wykonywalny_Nagłówek_zmienić_rozmiar != sizeof(wykonywalny_Nagłówek) ||
        wykonywalny_Nagłówek.program_Nagłówek_wpis_zmienić_rozmiar != sizeof(실행파일구획) || !wykonywalny_Nagłówek.program_Nagłówek_ILE_LICZB || wykonywalny_Nagłówek.program_Nagłówek_ILE_LICZB > 16 ||
        wykonywalny_Nagłówek.program_Nagłówek_przesunąć < sizeof(wykonywalny_Nagłówek) || !포함된범위(wykonywalny_Nagłówek.program_Nagłówek_przesunąć, (uint64_t)wykonywalny_Nagłówek.program_Nagłówek_ILE_LICZB * sizeof(실행파일구획), Rozmiar)) return użytkownik_wykonywalny_błąd;
    uint8_t 사용량[(użytkownik_OBRAZ_Koniec - użytkownik_baza) / rozmiar_strony] = {0};
    int prawidłowy_punkt_wejścia = 0, ABI_OK = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < wykonywalny_Nagłówek.program_Nagłówek_ILE_LICZB; 순번++) {
        실행파일구획 dane_stanowisko; memcpy(&dane_stanowisko, dane + wykonywalny_Nagłówek.program_Nagłówek_przesunąć + 순번 * sizeof(dane_stanowisko), sizeof(dane_stanowisko));
        if (dane_stanowisko.TYP_obszar == 4) {
            if (!포함된범위(dane_stanowisko.przesunąć_WARTOŚĆ_450fc799, dane_stanowisko.파일영역크기, Rozmiar)) return użytkownik_wykonywalny_błąd;
            if (부가정보검사(dane + dane_stanowisko.przesunąć_WARTOŚĆ_450fc799, dane_stanowisko.파일영역크기)) ABI_OK = 1;
            continue;
        }
        if (dane_stanowisko.TYP_obszar == 0 || dane_stanowisko.TYP_obszar == 6 || (dane_stanowisko.TYP_obszar == 0x6474e551 && !(dane_stanowisko.konfiguracja_BITS & 1))) continue;
        if (dane_stanowisko.TYP_obszar != 1) return użytkownik_wykonywalny_błąd; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!dane_stanowisko.기억영역크기) continue;
        if (dane_stanowisko.konfiguracja_BITS & ~7u || !(dane_stanowisko.konfiguracja_BITS & 4) || (dane_stanowisko.konfiguracja_BITS & 3) == 3 || dane_stanowisko.파일영역크기 > dane_stanowisko.기억영역크기 ||
            (dane_stanowisko.파일영역크기 && !포함된범위(dane_stanowisko.przesunąć_WARTOŚĆ_450fc799, dane_stanowisko.파일영역크기, Rozmiar)) || dane_stanowisko.Adres < użytkownik_baza ||
            !포함된범위(dane_stanowisko.Adres, dane_stanowisko.기억영역크기, użytkownik_OBRAZ_Koniec) ||
            (!리눅스방식 && ((dane_stanowisko.Adres & (rozmiar_strony - 1)) || (dane_stanowisko.przesunąć_WARTOŚĆ_450fc799 & (rozmiar_strony - 1)) || dane_stanowisko.wyrównać_granica != rozmiar_strony)) ||
            (리눅스방식 && (((dane_stanowisko.Adres ^ dane_stanowisko.przesunąć_WARTOŚĆ_450fc799) & (rozmiar_strony - 1)) || !dane_stanowisko.wyrównać_granica ||
                (dane_stanowisko.wyrównać_granica & (dane_stanowisko.wyrównać_granica - 1)) || dane_stanowisko.wyrównać_granica > 0x200000 || ((dane_stanowisko.Adres ^ dane_stanowisko.przesunąć_WARTOŚĆ_450fc799) & (dane_stanowisko.wyrównać_granica - 1))))) return użytkownik_wykonywalny_błąd;
        unsigned 첫항목 = (dane_stanowisko.Adres - użytkownik_baza) / rozmiar_strony;
        unsigned wpis_ILE_LICZB = ((dane_stanowisko.Adres & (rozmiar_strony - 1)) + dane_stanowisko.기억영역크기 + rozmiar_strony - 1) / rozmiar_strony;
        for (unsigned strona_WARTOŚĆ = 첫항목; strona_WARTOŚĆ < 첫항목 + wpis_ILE_LICZB; strona_WARTOŚĆ++) {
            if (사용량[strona_WARTOŚĆ]) return użytkownik_wykonywalny_błąd;
            사용량[strona_WARTOŚĆ] = 1;
        }
        if ((dane_stanowisko.konfiguracja_BITS & 1) && wykonywalny_Nagłówek.punkt_wejścia >= dane_stanowisko.Adres && wykonywalny_Nagłówek.punkt_wejścia < dane_stanowisko.Adres + dane_stanowisko.파일영역크기 && !(wykonywalny_Nagłówek.punkt_wejścia & 3)) prawidłowy_punkt_wejścia = 1;
        적재구획++;
    }
    return prawidłowy_punkt_wejścia && (리눅스방식 ? !ABI_OK : ABI_OK) && 적재구획 ? 0 : użytkownik_wykonywalny_błąd;
}
int 사용자실행파일검사(const unsigned char *dane, size_t Rozmiar) { return 실행파일검사(dane, Rozmiar, 0); }
static void układ_strony(uintptr_t Adres, uint64_t konfiguracja_BITS, unsigned uprawnienia) {
    unsigned WYSZUKAJ_INDEKS = (Adres - użytkownik_baza) / rozmiar_strony;
    strona_Lista[WYSZUKAJ_INDEKS] = Adres | konfiguracja_BITS;
    Uprawnienia_Lista[WYSZUKAJ_INDEKS] = uprawnienia;
}
static int użytkownik_zakres(uintptr_t Adres, size_t wpis_ILE_LICZB, int 쓰는중) {
    if (Adres < użytkownik_baza || !포함된범위(Adres, wpis_ILE_LICZB, użytkownik_Koniec)) return 0;
    if (!wpis_ILE_LICZB) return 1;
    unsigned 첫항목 = (Adres - użytkownik_baza) / rozmiar_strony, 마지막 = (Adres + wpis_ILE_LICZB - 1 - użytkownik_baza) / rozmiar_strony;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(Uprawnienia_Lista[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int kopiować_ścieżka(uintptr_t Adres, char *ścieżka_2) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!użytkownik_zakres(Adres, 1, 0)) return -14;
        ścieżka_2[순번] = *(const char *)Adres++;
        if (!ścieżka_2[순번]) return 0;
    }
    return -36;
}
static intptr_t jądro_KR(intptr_t WYNIK) { return WYNIK < 0 ? -numer_błędu : WYNIK; }
static int 대응파일기술자(uint64_t dojście_do_pliku) { return dojście_do_pliku >= 3 && dojście_do_pliku < 19 ? lista_plików[dojście_do_pliku - 3] : -1; }
static int gniazdo_uczestnik_właściciel(uint64_t dojście_do_pliku) { return dojście_do_pliku >= 32 && dojście_do_pliku < 56 && 통신끝점들[dojście_do_pliku - 32]; }
static int ADRES_wejście(uintptr_t 가리킴값, size_t długość_WARTOŚĆ, struct pk_sockaddr_in *Adres) {
    if (długość_WARTOŚĆ != sizeof(*Adres)) return -22;
    if (!użytkownik_zakres(가리킴값, długość_WARTOŚĆ, 0)) return -14;
    memcpy(Adres, (const void *)가리킴값, sizeof(*Adres));
    return Adres->sin_family == AF_INET ? 0 : -97;
}
static int ADRES_produkt_wyjściowy_czek(uintptr_t 가리킴값, uintptr_t długość_wskaźnik, pk_socklen_t *bufor_pojemność) {
    if (!użytkownik_zakres(długość_wskaźnik, sizeof(*bufor_pojemność), 1)) return -14;
    memcpy(bufor_pojemność, (const void *)długość_wskaźnik, sizeof(*bufor_pojemność));
    if (*bufor_pojemność > sizeof(struct pk_sockaddr_in)) *bufor_pojemność = sizeof(struct pk_sockaddr_in);
    if (*bufor_pojemność && !użytkownik_zakres(가리킴값, *bufor_pojemność, 1)) return -14;
    return 0;
}
static void ADRES_produkt_wyjściowy(uintptr_t 가리킴값, uintptr_t długość_wskaźnik, pk_socklen_t bufor_pojemność, int Adres, int numer_portu) {
    struct pk_sockaddr_in WARTOŚĆ; memset(&WARTOŚĆ, 0, sizeof(WARTOŚĆ));
    WARTOŚĆ.sin_family = AF_INET; WARTOŚĆ.sin_port = pk_htons(numer_portu); WARTOŚĆ.sin_addr.s_addr = pk_htonl(Adres);
    if (bufor_pojemność) memcpy((void *)가리킴값, &WARTOŚĆ, bufor_pojemność);
    pk_socklen_t długość_WARTOŚĆ = sizeof(WARTOŚĆ); memcpy((void *)długość_wskaźnik, &długość_WARTOŚĆ, sizeof(długość_WARTOŚĆ));
}
extern uintptr_t Tablica_Kanał(uintptr_t, uintptr_t);
static intptr_t natywny_System_Połącz(użytkownik_kadr *Plik_wpis) {
    uintptr_t 첫째값 = Plik_wpis->rejestr_dane[0], SEKUNDA_WARTOŚĆ = Plik_wpis->rejestr_dane[1], kod_znaku = Plik_wpis->rejestr_dane[2];
    char ścieżka_2[65];
    int dojście_do_pliku, WYNIK;
    switch (Plik_wpis->rejestr_dane[8]) {
    case 0: return 1; // własny ABI 버전
    case 1: // write: wskaźnik 전체를 검사한 BACK_WARTOŚĆ pozycja_wyjścia/nazwa_pliku zmienić_WARTOŚĆ
        if (kod_znaku > 65536) return -22;
        if (!użytkownik_zakres(SEKUNDA_WARTOŚĆ, kod_znaku, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t START_produkt_wyjściowy=Zegar_WARTOŚĆ();
            for (size_t 순번 = 0; 순번 < kod_znaku; 순번++) Tablica_Kanał(첫째값, ((const unsigned char *)SEKUNDA_WARTOŚĆ)[순번]);
            /* 큰 tty를 그린 jądro_WARTOŚĆ 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(interakcyjny){
                termin_ostateczny_CZAS+=Zegar_WARTOŚĆ()-START_produkt_wyjściowy;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(termin_ostateczny_CZAS) : "memory");
            }
            return kod_znaku;
        }
        if(첫째값>=40&&gniazdo_uczestnik_właściciel(첫째값)){
            size_t towar_ILE_LICZB=kod_znaku>512?512:kod_znaku;for(size_t 순번=0;순번<towar_ILE_LICZB;순번++)자바전문넣기(순번,((const unsigned char *)SEKUNDA_WARTOŚĆ)[순번]);return 자바흐름쓰기(첫째값,towar_ILE_LICZB);
        }
        dojście_do_pliku = 대응파일기술자(첫째값); if (dojście_do_pliku < 0) return -9;
        return jądro_KR(pk_write(dojście_do_pliku, (const void *)SEKUNDA_WARTOŚĆ, kod_znaku));
    case 2:
        if (kod_znaku > 65536) return -22;
        if (!użytkownik_zakres(SEKUNDA_WARTOŚĆ, kod_znaku, 1)) return -14;
        if (첫째값 == 0) {
            size_t towar_ILE_LICZB = 0;
            while (towar_ILE_LICZB < kod_znaku) {
                int znak_WARTOŚĆ = (int32_t)보드글자읽기(); if (znak_WARTOŚĆ == -2) return towar_ILE_LICZB; if (znak_WARTOŚĆ < 0) break;
                ((unsigned char *)SEKUNDA_WARTOŚĆ)[towar_ILE_LICZB++] = znak_WARTOŚĆ;
            }
            return towar_ILE_LICZB ? (intptr_t)towar_ILE_LICZB : (kod_znaku ? -11 : 0);
        }
        if(첫째값>=40&&gniazdo_uczestnik_właściciel(첫째값)){
            WYNIK=자바흐름읽기(첫째값,kod_znaku>512?512:kod_znaku);if(WYNIK>0)for(int 순번=0;순번<WYNIK;순번++)((unsigned char *)SEKUNDA_WARTOŚĆ)[순번]=자바전문얻기(순번);return WYNIK;
        }
        dojście_do_pliku = 대응파일기술자(첫째값); if (dojście_do_pliku < 0) return -9;
        return jądro_KR(pk_read(dojście_do_pliku, (void *)SEKUNDA_WARTOŚĆ, kod_znaku));
    case 3:
        WYNIK = kopiować_ścieżka(첫째값, ścieżka_2); if (WYNIK) return WYNIK;
        if (SEKUNDA_WARTOŚĆ > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (lista_plików[순번] < 0) {
            dojście_do_pliku = pk_open(ścieżka_2, (int)SEKUNDA_WARTOŚĆ, 0600);
            if (dojście_do_pliku < 0) return -numer_błędu;
            lista_plików[순번] = dojście_do_pliku; return 순번 + 3;
        }
        return -24;
    case 4:
        if (gniazdo_uczestnik_właściciel(첫째값)) { WYNIK = Zamknij_gniazdo_uczestnik(첫째값); if (!WYNIK) 통신끝점들[첫째값 - 32] = 0; return WYNIK; }
        dojście_do_pliku = 대응파일기술자(첫째값); if (dojście_do_pliku < 0) return -9;
        WYNIK = pk_close(dojście_do_pliku); if (!WYNIK) lista_plików[첫째값 - 3] = -1;
        return jądro_KR(WYNIK);
    case 5:
        dojście_do_pliku = 대응파일기술자(첫째값); if (dojście_do_pliku < 0) return -9;
        if (kod_znaku > 2) return -22;
        return jądro_KR(pk_lseek(dojście_do_pliku, (int64_t)SEKUNDA_WARTOŚĆ, kod_znaku));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 przestrzeń_użytkownika RW/NX sterta_WARTOŚĆ, 새로 노출되는 페이지는 0으로 inicjuj
        if (!첫째값) return sterta_Koniec;
        if (첫째값 < użytkownik_OBRAZ_Koniec || 첫째값 > użytkownik_sterta_Koniec) return -12;
        uintptr_t 이전쪽들 = (sterta_Koniec + rozmiar_strony - 1) & ~(rozmiar_strony - 1);
        uintptr_t 새쪽들 = (첫째값 + rozmiar_strony - 1) & ~(rozmiar_strony - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t dane_stanowisko = 이전쪽들; dane_stanowisko < 새쪽들; dane_stanowisko += rozmiar_strony) układ_strony(dane_stanowisko, jądro_strona, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t dane_stanowisko = 이전쪽들; dane_stanowisko < 새쪽들; dane_stanowisko += rozmiar_strony) układ_strony(dane_stanowisko, użytkownik_R_W, 3);
        } else {
            for (uintptr_t dane_stanowisko = 새쪽들; dane_stanowisko < 이전쪽들; dane_stanowisko += rozmiar_strony) {
                strona_Lista[(dane_stanowisko - użytkownik_baza) / rozmiar_strony] = 0; Uprawnienia_Lista[(dane_stanowisko - użytkownik_baza) / rozmiar_strony] = 0;
            }
        }
        sterta_Koniec = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        dojście_do_pliku = 대응파일기술자(첫째값); return dojście_do_pliku < 0 ? -9 : jądro_KR(pk_size(dojście_do_pliku));
    case 10:
        dojście_do_pliku = 대응파일기술자(첫째값); return dojście_do_pliku < 0 ? -9 : jądro_KR(pk_ftruncate(dojście_do_pliku, (int64_t)SEKUNDA_WARTOŚĆ));
    case 11:
        WYNIK = kopiować_ścieżka(첫째값, ścieżka_2); return WYNIK ? WYNIK : jądro_KR(pk_unlink(ścieżka_2));
    case 12:
        dojście_do_pliku = 대응파일기술자(첫째값); return dojście_do_pliku < 0 ? -9 : jądro_KR(pk_fsync(dojście_do_pliku));
    case 13: { // 그래픽 기초 API: przestrzeń_użytkownika 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = Plik_wpis->rejestr_dane[3], wymagane_wysokość_WARTOŚĆ = Plik_wpis->rejestr_dane[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SEKUNDA_WARTOŚĆ > 화면길이 || 너비값 > 화면폭 - 첫째값 || wymagane_wysokość_WARTOŚĆ > 화면길이 - SEKUNDA_WARTOŚĆ) return -22;
        for (uintptr_t Y_współrzędna = SEKUNDA_WARTOŚĆ; Y_współrzędna < SEKUNDA_WARTOŚĆ + wymagane_wysokość_WARTOŚĆ; Y_współrzędna++) for (uintptr_t współrzędna_X = 첫째값; współrzędna_X < 첫째값 + 너비값; współrzędna_X++) Tablica_piksel(współrzędna_X, Y_współrzędna, kod_znaku);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=towar_ILE_LICZB; args(index,buffer,capacity)=UTF-8 długość_WARTOŚĆ
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (kod_znaku <= 전달인수길이[첫째값]) return -36;
        if (!użytkownik_zakres(SEKUNDA_WARTOŚĆ, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SEKUNDA_WARTOŚĆ, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;interakcyjny=1;return Tablica_Terminal(13);}
        if(첫째값==2){interakcyjny=0;return 0;}
        if(첫째값==3)return Tablica_Terminal(13);
        if(첫째값!=1||!interakcyjny)return -22;
        WYNIK=(int32_t)보드글자읽기();
        if(WYNIK==-4096)return WYNIK;
        START_TIMEOUT();return WYNIK<0?-11:WYNIK;
    case 17: { // 유한한 협력 chwileczkę_WARTOŚĆ: komunikacja 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t Koniec_CZAS = Zegar_WARTOŚĆ() + CZĘSTOŚĆ * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Zegar_WARTOŚĆ() < Koniec_CZAS);
        START_TIMEOUT(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 nadrzędny_WARTOŚĆ·빈 폴더를 검사한다.
        if (SEKUNDA_WARTOŚĆ > 2) return -22;
        WYNIK = kopiować_ścieżka(첫째값, ścieżka_2); if (WYNIK) return WYNIK;
        unsigned długość_WARTOŚĆ = 0; while (ścieżka_2[długość_WARTOŚĆ]) długość_WARTOŚĆ++;
        WYNIK = 자바경로시작(długość_WARTOŚĆ); if (WYNIK < 0) return WYNIK;
        for (unsigned 순번 = 0; 순번 < długość_WARTOŚĆ; 순번++) 자바경로바이트(순번, (unsigned char)ścieżka_2[순번]);
        return SEKUNDA_WARTOŚĆ == 0 ? 자바항목종류() : SEKUNDA_WARTOŚĆ == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int znak_WARTOŚĆ=(int32_t)보드글자읽기();if(znak_WARTOŚĆ==-4096)return znak_WARTOŚĆ;if(znak_WARTOŚĆ>=0)화면누름(właściciel_obiekt,znak_WARTOŚĆ);START_TIMEOUT();}
        if(첫째값==3&&kod_znaku){if(!자바셸대화형())return -95;interakcyjny=1;Tablica_Terminal(300);}
        return 화면호출(właściciel_obiekt,첫째값,SEKUNDA_WARTOŚĆ,kod_znaku,Plik_wpis->rejestr_dane[3],Plik_wpis->rejestr_dane[4],Plik_wpis->rejestr_dane[5]);
    case 21:
        if(kod_znaku>127)return -22;if(!użytkownik_zakres(SEKUNDA_WARTOŚĆ,kod_znaku*sizeof(uint32_t),0))return -14;
        return 화면글(właściciel_obiekt,첫째값,(const uint32_t *)SEKUNDA_WARTOŚĆ,kod_znaku);
    case 22: // 화면 Rozmiar zapytanie_WARTOŚĆ: 0=너비, 1=wysokość_WARTOŚĆ. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SEKUNDA_WARTOŚĆ==SOCK_STREAM&&(kod_znaku==0||kod_znaku==6))WYNIK=자바흐름만들기();
        else if(SEKUNDA_WARTOŚĆ==SOCK_DGRAM&&(kod_znaku==0||kod_znaku==IPPROTO_UDP))WYNIK=자바전문만들기(첫째값,SEKUNDA_WARTOŚĆ,kod_znaku);
        else return -93;
        if (WYNIK >= 32 && WYNIK < 56) 통신끝점들[WYNIK - 32] = 1;
        return WYNIK;
    case 33: {
        if (!gniazdo_uczestnik_właściciel(첫째값)) return -9;
        struct pk_sockaddr_in Adres;
        WYNIK = ADRES_wejście(SEKUNDA_WARTOŚĆ, kod_znaku, &Adres); if (WYNIK) return WYNIK;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(Adres.sin_addr.s_addr),pk_htons(Adres.sin_port)):자바전문묶기(첫째값, pk_htonl(Adres.sin_addr.s_addr), pk_htons(Adres.sin_port));
    }
    case 34: {
        if (!gniazdo_uczestnik_właściciel(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Plik_wpis->rejestr_dane[3]) return -95;
        if (kod_znaku > 512) return -90;
        if (kod_znaku && !użytkownik_zakres(SEKUNDA_WARTOŚĆ, kod_znaku, 0)) return -14;
        struct pk_sockaddr_in Adres;
        WYNIK = ADRES_wejście(Plik_wpis->rejestr_dane[4], Plik_wpis->rejestr_dane[5], &Adres); if (WYNIK) return WYNIK;
        for (unsigned 순번 = 0; 순번 < kod_znaku; 순번++) 자바전문넣기(순번, ((const unsigned char *)SEKUNDA_WARTOŚĆ)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(Adres.sin_addr.s_addr), pk_htons(Adres.sin_port), kod_znaku);
    }
    case 35: {
        if (!gniazdo_uczestnik_właściciel(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Plik_wpis->rejestr_dane[3]) return -95;
        if (kod_znaku > 512) return -90;
        if (kod_znaku && !użytkownik_zakres(SEKUNDA_WARTOŚĆ, kod_znaku, 1)) return -14;
        pk_socklen_t bufor_pojemność = 0;
        if (Plik_wpis->rejestr_dane[4]) { WYNIK = ADRES_produkt_wyjściowy_czek(Plik_wpis->rejestr_dane[4], Plik_wpis->rejestr_dane[5], &bufor_pojemność); if (WYNIK) return WYNIK; }
        WYNIK = 자바전문받기(첫째값, kod_znaku); if (WYNIK < 0) return WYNIK;
        for (int 순번 = 0; 순번 < WYNIK; 순번++) ((unsigned char *)SEKUNDA_WARTOŚĆ)[순번] = 자바전문얻기(순번);
        if (Plik_wpis->rejestr_dane[4]) ADRES_produkt_wyjściowy(Plik_wpis->rejestr_dane[4], Plik_wpis->rejestr_dane[5], bufor_pojemność, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return WYNIK;
    }
    case 36: {
        if (!gniazdo_uczestnik_właściciel(첫째값)) return -9;
        pk_socklen_t bufor_pojemność;
        WYNIK = ADRES_produkt_wyjściowy_czek(SEKUNDA_WARTOŚĆ, kod_znaku, &bufor_pojemność); if (WYNIK) return WYNIK;
        ADRES_produkt_wyjściowy(SEKUNDA_WARTOŚĆ,kod_znaku,bufor_pojemność,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!gniazdo_uczestnik_właściciel(첫째값))return -9;struct pk_sockaddr_in Adres;
        WYNIK=ADRES_wejście(SEKUNDA_WARTOŚĆ,kod_znaku,&Adres);if(WYNIK)return WYNIK;
        return 자바흐름연결(첫째값,pk_htonl(Adres.sin_addr.s_addr),pk_htons(Adres.sin_port));
    }
    case 38: return 첫째값>=40&&gniazdo_uczestnik_właściciel(첫째값)?자바흐름듣기(첫째값,SEKUNDA_WARTOŚĆ):-9;
    case 39:
        if(첫째값<40||!gniazdo_uczestnik_właściciel(첫째값))return -9;
        if(SEKUNDA_WARTOŚĆ||kod_znaku)return -95;WYNIK=자바흐름연결받기(첫째값);if(WYNIK>=40&&WYNIK<56)통신끝점들[WYNIK-32]=1;return WYNIK;
    case 40: return 첫째값>=40&&gniazdo_uczestnik_właściciel(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t wywołanie_systemowe(użytkownik_kadr *Plik_wpis) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(Plik_wpis) : natywny_System_Połącz(Plik_wpis);
}
static void Zwrot_jądro(użytkownik_kadr *Plik_wpis, int WYNIK) {
    Stop_TIMEOUT();
    Plik_wpis->rejestr_dane[0] = (uint64_t)(int64_t)WYNIK;
    Plik_wpis->polecenie_stanowisko = (uintptr_t)użytkownik_Zwrot;
    Plik_wpis->Stan_KOD = 0x3c5; // EL1h, DAIF masked
}
int wyjątek_użytkownika(użytkownik_kadr *Plik_wpis, unsigned ODCIĘTA) {
    if (!Aktywny || (Plik_wpis->Stan_KOD & 15) != 0) return 0;
    if (ODCIĘTA) {
        uint32_t potwierdzenie_WARTOŚĆ = maszyna_rejestr(przerwanie_CPU_interfejs + 0xc), identyfikator_WARTOŚĆ = potwierdzenie_WARTOŚĆ & 1023;
        if (identyfikator_WARTOŚĆ == 30) { Zwrot_jądro(Plik_wpis, użytkownik_TIMEOUT); maszyna_rejestr(przerwanie_CPU_interfejs + 0x10) = potwierdzenie_WARTOŚĆ; return 1; }
        if (identyfikator_WARTOŚĆ < 1020) maszyna_rejestr(przerwanie_CPU_interfejs + 0x10) = potwierdzenie_WARTOŚĆ;
        return 1;
    }
    uint64_t wyjątek_Stan; __asm__ volatile("mrs %0, esr_el1" : "=r"(wyjątek_Stan));
    if (Zegar_WARTOŚĆ() >= termin_ostateczny_CZAS) { Zwrot_jądro(Plik_wpis, użytkownik_TIMEOUT); return 1; }
    unsigned wyjątek_obszar = wyjątek_Stan >> 26;
    if (wyjątek_obszar == 0x15 && (wyjątek_Stan & 0xffff) == 0) {
        if (리눅스규약 ? Plik_wpis->rejestr_dane[8] == 93 || Plik_wpis->rejestr_dane[8] == 94 : Plik_wpis->rejestr_dane[8] == 6) Zwrot_jądro(Plik_wpis, (int)(Plik_wpis->rejestr_dane[0] & 255));
        else {
            intptr_t WYNIK=wywołanie_systemowe(Plik_wpis);
            if(WYNIK==-4096&&interakcyjny){
                저장값[właściciel_obiekt].wykonanie_kadr=*Plik_wpis;저장값[właściciel_obiekt].wykonanie_kadr.polecenie_stanowisko-=4;
                사용자실수보관(저장값[właściciel_obiekt].liczba_zmiennoprzecinkowa_Stan);Zwrot_jądro(Plik_wpis,사용자중단됨);
            }else Plik_wpis->rejestr_dane[0]=(uint64_t)WYNIK;
        }
    } else Zwrot_jądro(Plik_wpis, wyjątek_obszar == 0x24 ? użytkownik_dane_błąd : wyjątek_obszar == 0x20 ? użytkownik_wykonanie_błąd : użytkownik_nieważny_instrukcja);
    return 1;
}

// 생성된 const ELF grupa_WARTOŚĆ: 실행은 반드시 program_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *dane; size_t Rozmiar; unsigned 전달값; } program;
#include "programs.h"
static void *migawka(unsigned indeks_pozycji){return (void *)(0x04000000ul+indeks_pozycji*(użytkownik_Koniec-użytkownik_baza));}
static int Zakończ_program(int WYNIK){
    사용자누적시각[właściciel_obiekt]+=(uint32_t)보드밀리초()-użytkownik_wykonanie_CZAS[właściciel_obiekt];
    Stop_TIMEOUT();Aktywny=0;
    if(WYNIK==사용자중단됨){
        저장된작업 *ciąg_dane=&저장값[właściciel_obiekt];ciąg_dane->wstrzymany_Stan=1;ciąg_dane->interakcyjny=interakcyjny;ciąg_dane->리눅스규약=리눅스규약;ciąg_dane->pamięć_dynamiczna=sterta_Koniec;ciąg_dane->인수개수=전달인수개수;
        memcpy(ciąg_dane->Uprawnienia_Lista,Uprawnienia_Lista,sizeof(Uprawnienia_Lista));memcpy(ciąg_dane->lista_plików,lista_plików,sizeof(lista_plików));memcpy(ciąg_dane->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(ciąg_dane->argument_TABLICA,전달인수,sizeof(전달인수));memcpy(ciąg_dane->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<użytkownik_strona_ILE_LICZB;순번++)if(Uprawnienia_Lista[순번])memcpy((unsigned char *)migawka(właściciel_obiekt)+순번*rozmiar_strony,(void *)(użytkownik_baza+순번*rozmiar_strony),rozmiar_strony);
    }else{
        저장값[właściciel_obiekt].wstrzymany_Stan=0;화면초기화(właściciel_obiekt);
        for(unsigned 순번=0;순번<16;순번++)if(lista_plików[순번]>=0)pk_close(lista_plików[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])Zamknij_gniazdo_uczestnik(순번+32);
    }
    for(unsigned 순번=0;순번<użytkownik_strona_ILE_LICZB;순번++){strona_Lista[순번]=0;Uprawnienia_Lista[순번]=0;}변환표맞추기();return WYNIK;
}
uintptr_t Tablica_formant_użytkownika(uintptr_t Akcja){
    unsigned indeks_pozycji=Akcja&15;if(indeks_pozycji>=4||Aktywny)return (uint32_t)-22;
    저장된작업 *ciąg_dane=&저장값[indeks_pozycji];
    if(Akcja>=32){if(ciąg_dane->wstrzymany_Stan){for(unsigned 순번=0;순번<16;순번++)if(ciąg_dane->lista_plików[순번]>=0)pk_close(ciąg_dane->lista_plików[순번]);for(unsigned 순번=0;순번<24;순번++)if(ciąg_dane->통신끝점들[순번])Zamknij_gniazdo_uczestnik(순번+32);}ciąg_dane->wstrzymany_Stan=0;화면초기화(indeks_pozycji);return 0;}
    if(Akcja>=16)return ciąg_dane->wstrzymany_Stan;
    if(!ciąg_dane->wstrzymany_Stan)return (uint32_t)-22;
    właściciel_obiekt=indeks_pozycji;interakcyjny=ciąg_dane->interakcyjny;리눅스규약=ciąg_dane->리눅스규약;sterta_Koniec=ciąg_dane->pamięć_dynamiczna;전달인수개수=ciąg_dane->인수개수;
    memcpy(lista_plików,ciąg_dane->lista_plików,sizeof(lista_plików));memcpy(통신끝점들,ciąg_dane->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,ciąg_dane->argument_TABLICA,sizeof(전달인수));memcpy(전달인수길이,ciąg_dane->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<użytkownik_strona_ILE_LICZB;순번++)strona_Lista[순번]=(użytkownik_baza+순번*rozmiar_strony)|jądro_strona;변환표맞추기();
    memset((void *)użytkownik_baza,0,użytkownik_Koniec-użytkownik_baza);
    for(unsigned 순번=0;순번<użytkownik_strona_ILE_LICZB;순번++)if(ciąg_dane->Uprawnienia_Lista[순번])memcpy((void *)(użytkownik_baza+순번*rozmiar_strony),(unsigned char *)migawka(indeks_pozycji)+순번*rozmiar_strony,rozmiar_strony);
    memcpy(Uprawnienia_Lista,ciąg_dane->Uprawnienia_Lista,sizeof(Uprawnienia_Lista));
    for(unsigned 순번=0;순번<użytkownik_strona_ILE_LICZB;순번++){unsigned dane_stanowisko=Uprawnienia_Lista[순번];strona_Lista[순번]=dane_stanowisko?(użytkownik_baza+순번*rozmiar_strony)|(dane_stanowisko==3?użytkownik_R_W:dane_stanowisko==5?사용자읽고실행:użytkownik_tylko_do_odczytu):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");Aktywny=1;ciąg_dane->wstrzymany_Stan=0;START_TIMEOUT();
    użytkownik_wykonanie_CZAS[właściciel_obiekt]=보드밀리초();
    return (uint32_t)Zakończ_program(użytkownik_CV(&ciąg_dane->wykonanie_kadr,ciąg_dane->liczba_zmiennoprzecinkowa_Stan));
}
static int przebieg_program(const unsigned char *dane, size_t Rozmiar, unsigned 전달값, int 리눅스방식, const char *Nazwa) {
    if (Aktywny) return -16;
    właściciel_obiekt=Tablica_Terminal(11);if(właściciel_obiekt<0||właściciel_obiekt>3||저장값[właściciel_obiekt].wstrzymany_Stan)return -16;interakcyjny=0;
    int prawidłowy = 실행파일검사(dane, Rozmiar, 리눅스방식); if (prawidłowy) return prawidłowy;
    리눅스규약 = 리눅스방식;
    unsigned nazwa_INDEKS=0;
    while (*Nazwa && nazwa_INDEKS<31) użytkownik_polecenie_nazwa[właściciel_obiekt][nazwa_INDEKS++]=(unsigned char)*Nazwa++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (nazwa_INDEKS) użytkownik_polecenie_nazwa[właściciel_obiekt][nazwa_INDEKS++]=' ';
        for (unsigned indeks_pozycji=0; indeks_pozycji<전달인수길이[0]; indeks_pozycji++) użytkownik_polecenie_nazwa[właściciel_obiekt][nazwa_INDEKS++]=전달인수[0][indeks_pozycji];
    }
    użytkownik_polecenie_nazwa[właściciel_obiekt][nazwa_INDEKS]=0; numer_użytkownika[właściciel_obiekt]=Dalej_numer_użytkownika++;
    if (Dalej_numer_użytkownika>0x7fffffffu) Dalej_numer_użytkownika=10;
    użytkownik_START_CZAS[właściciel_obiekt]=보드밀리초(); 사용자누적시각[właściciel_obiekt]=0;
    for (unsigned 순번 = 0; 순번 < użytkownik_strona_ILE_LICZB; 순번++) strona_Lista[순번] = (użytkownik_baza + 순번 * rozmiar_strony) | jądro_strona;
    변환표맞추기();
    memset((void *)użytkownik_baza, 0, użytkownik_Koniec - użytkownik_baza);
    memset(Uprawnienia_Lista, 0, sizeof(Uprawnienia_Lista));
    실행파일머리 wykonywalny_Nagłówek; memcpy(&wykonywalny_Nagłówek, dane, sizeof(wykonywalny_Nagłówek));
    for (unsigned 순번 = 0; 순번 < wykonywalny_Nagłówek.program_Nagłówek_ILE_LICZB; 순번++) {
        실행파일구획 dane_stanowisko; memcpy(&dane_stanowisko, dane + wykonywalny_Nagłówek.program_Nagłówek_przesunąć + 순번 * sizeof(dane_stanowisko), sizeof(dane_stanowisko));
        if (dane_stanowisko.TYP_obszar != 1 || !dane_stanowisko.기억영역크기) continue;
        if (dane_stanowisko.파일영역크기) memcpy((void *)(uintptr_t)dane_stanowisko.Adres, dane + dane_stanowisko.przesunąć_WARTOŚĆ_450fc799, dane_stanowisko.파일영역크기);
        for (uintptr_t bieżący_stanowisko = dane_stanowisko.Adres & ~(rozmiar_strony - 1); bieżący_stanowisko < dane_stanowisko.Adres + dane_stanowisko.기억영역크기; bieżący_stanowisko += rozmiar_strony) {
            Uprawnienia_Lista[(bieżący_stanowisko - użytkownik_baza) / rozmiar_strony] = (dane_stanowisko.konfiguracja_BITS & 2) ? 3 : ((dane_stanowisko.konfiguracja_BITS & 1) ? 5 : 1);
        }
    }
    for (uintptr_t bieżący_stanowisko = użytkownik_Stos_ADRES; bieżący_stanowisko < użytkownik_Koniec; bieżący_stanowisko += rozmiar_strony) Uprawnienia_Lista[(bieżący_stanowisko - użytkownik_baza) / rozmiar_strony] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(wykonywalny_Nagłówek.punkt_wejścia) : użytkownik_Koniec;
    for (unsigned 순번 = 0; 순번 < użytkownik_strona_ILE_LICZB; 순번++) {
        unsigned uprawnienia = Uprawnienia_Lista[순번];
        strona_Lista[순번] = uprawnienia ? (użytkownik_baza + 순번 * rozmiar_strony) | (uprawnienia == 3 ? użytkownik_R_W : uprawnienia == 5 ? 사용자읽고실행 : użytkownik_tylko_do_odczytu) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) lista_plików[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    sterta_Koniec = użytkownik_OBRAZ_Koniec;
    Aktywny = 1; START_TIMEOUT();
    użytkownik_wykonanie_CZAS[właściciel_obiekt]=보드밀리초();
    int WYNIK = użytkownik_wprowadzić(wykonywalny_Nagłówek.punkt_wejścia, 초기쌓임공간, 전달값);
    return Zakończ_program(WYNIK);
}
uintptr_t Tablica_użytkownik_przebieg(uintptr_t WYSZUKAJ_INDEKS) {
    if (WYSZUKAJ_INDEKS >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Nazwa=WYSZUKAJ_INDEKS==10?"javac":WYSZUKAJ_INDEKS==11?"java":WYSZUKAJ_INDEKS==12?"python":WYSZUKAJ_INDEKS==13?"vi":WYSZUKAJ_INDEKS==14?"jar":WYSZUKAJ_INDEKS==15?"cc":WYSZUKAJ_INDEKS==16?"jaot":"ELF";
    return (uint32_t)przebieg_program(실행항목들[WYSZUKAJ_INDEKS].dane, 실행항목들[WYSZUKAJ_INDEKS].Rozmiar, 실행항목들[WYSZUKAJ_INDEKS].전달값, 0, Nazwa);
}
static uintptr_t Wykonaj_Plik(int 리눅스방식) {
    static unsigned char OBRAZ[16384];
    if (Aktywny || !전달인수개수) return (uint32_t)-22;
    int dojście_do_pliku = pk_open((const char *)전달인수[0], tylko_do_odczytu_WARTOŚĆ, 0);
    if (dojście_do_pliku < 0) return (uint32_t)-numer_błędu;
    int Rozmiar = pk_size(dojście_do_pliku);
    if (Rozmiar < 0 || (unsigned)Rozmiar > sizeof(OBRAZ)) { pk_close(dojście_do_pliku); return (uint32_t)-27; }
    int KWOTA_WYKUP_ILE_LICZB = pk_read(dojście_do_pliku, OBRAZ, Rozmiar); pk_close(dojście_do_pliku);
    if (KWOTA_WYKUP_ILE_LICZB != Rozmiar) return (uint32_t)-5;
    return (uint32_t)przebieg_program(OBRAZ, Rozmiar, 0, 리눅스방식, "");
}
uintptr_t Tablica_użytkownik_Plik(void) { return Wykonaj_Plik(0); }
uintptr_t 보드사용자리눅스파일(void) { return Wykonaj_Plik(1); }
uintptr_t Tablica_użytkownik_walidować(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].dane, 잘못된실행항목들[순번].Rozmiar) != użytkownik_wykonywalny_błąd) return 순번 + 1;
    return 0;
}
