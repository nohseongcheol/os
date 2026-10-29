#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "przestrzeń_użytkownika.h"
#include "../sieć_Stos/sieć_Stos.h"
typedef uintptr_t maszyna_Word;
#define maszyna_rejestr(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define skrzynka_pocztowa_ADRES 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Zegar_ILE_LICZB(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t CZĘSTOŚĆ;
static volatile uint32_t skrzynka_pocztowa_dane[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *dane_stanowisko, int kod_znaku, size_t towar_ILE_LICZB) { unsigned char *Dalej_przesunąć = dane_stanowisko; while (towar_ILE_LICZB--) *Dalej_przesunąć++ = kod_znaku; return dane_stanowisko; }
void *memcpy(void *cel_dane, const void *ciąg_dane, size_t towar_ILE_LICZB) { unsigned char *첫째값 = cel_dane; const unsigned char *SEKUNDA_WARTOŚĆ = ciąg_dane; while (towar_ILE_LICZB--) *첫째값++ = *SEKUNDA_WARTOŚĆ++; return cel_dane; }

static int skrzynka_pocztowa(void) {
    uint32_t żądanie = (uint32_t)(uintptr_t)skrzynka_pocztowa_dane | 8;
    uint64_t Uruchom_2 = Zegar_ILE_LICZB();
    기억장벽();
    while (maszyna_rejestr(skrzynka_pocztowa_ADRES + 0x38) & 0x80000000u)
        if (Zegar_ILE_LICZB() - Uruchom_2 > CZĘSTOŚĆ) return 0;
    maszyna_rejestr(skrzynka_pocztowa_ADRES + 0x20) = żądanie;
    for (;;) {
        if (!(maszyna_rejestr(skrzynka_pocztowa_ADRES + 0x18) & 0x40000000u)) {
            uint32_t odpowiedź = maszyna_rejestr(skrzynka_pocztowa_ADRES);
            if (odpowiedź == żądanie) { 기억장벽(); return skrzynka_pocztowa_dane[1] == 0x80000000u; }
        }
        if (Zegar_ILE_LICZB() - Uruchom_2 > CZĘSTOŚĆ) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terminal_bajt(unsigned);
extern int Terminal_oczekujący(void);
extern void Terminal_wskaźnik(unsigned,int,int),터미널바로가기키(unsigned);
extern void Terminal_wejście_tryb(unsigned);
#include "../zdalny_WARTOŚĆ/zdalny_WARTOŚĆ.h"
static int Strumienie;
static unsigned 직렬이전글자;
maszyna_Word Tablica_Strumienie(maszyna_Word 사용여부) { Strumienie=사용여부!=0; return 0; }
maszyna_Word Tablica_Kanał(maszyna_Word Kanał, maszyna_Word kod_znaku) {
    if(Strumienie && 자바셸출력((int32_t)Kanał,(int32_t)(kod_znaku&255))) return 0;
    Terminal_bajt(kod_znaku&255);
    zdalny_produkt_wyjściowy(kod_znaku&255);
    if ((kod_znaku&255)==10 && 직렬이전글자!=13) {
        while (maszyna_rejestr(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        maszyna_rejestr(직렬장치)=13;
    }
    직렬이전글자=kod_znaku&255;
    while (maszyna_rejestr(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    maszyna_rejestr(직렬장치) = (uint32_t)kod_znaku & 255;
    return 0;
}
maszyna_Word 보드글자쓰기(maszyna_Word kod_znaku) { return Tablica_Kanał(1,kod_znaku); }
maszyna_Word 보드원시글자읽기(void) {
    int zdalny_znak=zdalny_wejście();if(zdalny_znak>=0)return zdalny_znak;
    if (maszyna_rejestr(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t WARTOŚĆ = maszyna_rejestr(직렬장치);
    if (WARTOŚĆ & 0xf00) { maszyna_rejestr(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return WARTOŚĆ & 255;
}
maszyna_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char pakiet_dane[6];
    if(Terminal_oczekujący())return (uint32_t)-4096;
    if(Strumienie){int32_t kod_znaku=자바셸입력();if(kod_znaku!=-3)return (uint32_t)kod_znaku;}
    for(;;){
        int kod_znaku=(int32_t)보드원시글자읽기();if(kod_znaku<0)return (uint32_t)kod_znaku;
        if(!꾸러미안쪽){if(kod_znaku!=30)return kod_znaku;꾸러미안쪽=1;사용량=0;continue;}
        pakiet_dane[사용량++]=kod_znaku;if(사용량<6)continue;꾸러미안쪽=0;
        if(pakiet_dane[0]==1)Terminal_wskaźnik(pakiet_dane[1],pakiet_dane[2]+pakiet_dane[3]*256,pakiet_dane[4]+pakiet_dane[5]*256);
        if(pakiet_dane[0]==2)터미널바로가기키(pakiet_dane[1]);
        if(pakiet_dane[0]==3)Terminal_wejście_tryb(pakiet_dane[1]);
        if(Terminal_oczekujący())return (uint32_t)-4096;
    }
}
maszyna_Word 보드밀리초(void) { return (uint32_t)(Zegar_ILE_LICZB() / (CZĘSTOŚĆ / 1000)); }
maszyna_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *ciąg_dane) { while (*ciąg_dane) 보드글자쓰기((unsigned char)*ciąg_dane++); }
static void 직렬열여섯진출력(maszyna_Word towar_ILE_LICZB) { const char *열여섯진숫자 = "0123456789abcdef"; for (int ciąg_dane = 60; ciąg_dane >= 0; ciąg_dane -= 4) 보드글자쓰기(열여섯진숫자[(towar_ILE_LICZB >> ciąg_dane) & 15]); }
maszyna_Word Tablica_Stop(maszyna_Word Stan_WARTOŚĆ) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(Stan_WARTOŚĆ); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); Tablica_Stop(1); __builtin_unreachable(); }
void Tablica_wyjątek(maszyna_Word wyjątek_Stan, maszyna_Word polecenie_stanowisko, maszyna_Word nieważny_ADRES) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(wyjątek_Stan);
    직렬글출력(" PC="); 직렬열여섯진출력(polecenie_stanowisko); 직렬글출력(" FAR="); 직렬열여섯진출력(nieważny_ADRES);
    Tablica_Stop(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    skrzynka_pocztowa_dane[0]=32;skrzynka_pocztowa_dane[1]=0;skrzynka_pocztowa_dane[2]=0x10004;skrzynka_pocztowa_dane[3]=8;skrzynka_pocztowa_dane[4]=0;
    skrzynka_pocztowa_dane[5]=skrzynka_pocztowa_dane[6]=skrzynka_pocztowa_dane[7]=0;
    return skrzynka_pocztowa()&&skrzynka_pocztowa_dane[4]==0x80000008u&&(skrzynka_pocztowa_dane[5]||skrzynka_pocztowa_dane[6]);
}
int Tablica_adres_bezwzględny(unsigned char *Adres) {
    skrzynka_pocztowa_dane[0]=32;skrzynka_pocztowa_dane[1]=0;skrzynka_pocztowa_dane[2]=0x10003;skrzynka_pocztowa_dane[3]=8;skrzynka_pocztowa_dane[4]=0;
    skrzynka_pocztowa_dane[5]=skrzynka_pocztowa_dane[6]=skrzynka_pocztowa_dane[7]=0;
    if(!skrzynka_pocztowa()||(skrzynka_pocztowa_dane[4]&0x80000000u)==0||(skrzynka_pocztowa_dane[4]&0xffff)!=6)return 0;
    const unsigned char *dane=(const unsigned char*)&skrzynka_pocztowa_dane[5];unsigned SUMA_WARTOŚĆ=0;
    for(unsigned 순번=0;순번<6;순번++){Adres[순번]=dane[순번];SUMA_WARTOŚĆ|=dane[순번];}return SUMA_WARTOŚĆ&&!(Adres[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(CZĘSTOŚĆ));
    maszyna_rejestr(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    maszyna_rejestr(범용입출력 + 4) = (maszyna_rejestr(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    maszyna_rejestr(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. awaria_WARTOŚĆ 시 config.txt의 48MHz를 사용한다.
    skrzynka_pocztowa_dane[0] = 36; skrzynka_pocztowa_dane[1] = 0; skrzynka_pocztowa_dane[2] = 0x38002; skrzynka_pocztowa_dane[3] = 12;
    skrzynka_pocztowa_dane[4] = 0; skrzynka_pocztowa_dane[5] = 2; skrzynka_pocztowa_dane[6] = 48000000; skrzynka_pocztowa_dane[7] = 0; skrzynka_pocztowa_dane[8] = 0;
    int Zegar_w_dobrej_kondycji = skrzynka_pocztowa();
    uint32_t 속도 = Zegar_w_dobrej_kondycji && skrzynka_pocztowa_dane[6] >= 1843200 ? skrzynka_pocztowa_dane[6] : 48000000;
    skrzynka_pocztowa_dane[0]=32; skrzynka_pocztowa_dane[1]=0; skrzynka_pocztowa_dane[2]=0x10005; skrzynka_pocztowa_dane[3]=8; skrzynka_pocztowa_dane[4]=0;
    skrzynka_pocztowa_dane[5]=skrzynka_pocztowa_dane[6]=skrzynka_pocztowa_dane[7]=0;
    if (skrzynka_pocztowa() && skrzynka_pocztowa_dane[4]==0x80000008u) 팔기억킬로바이트=skrzynka_pocztowa_dane[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    maszyna_rejestr(직렬장치 + 0x44) = 0x7ff;
    maszyna_rejestr(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    maszyna_rejestr(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    maszyna_rejestr(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    maszyna_rejestr(직렬장치 + 0x38) = 0;
    maszyna_rejestr(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
maszyna_Word Tablica_FTP(maszyna_Word Akcja) { return (uint32_t)ftp_control((int)Akcja); }
maszyna_Word Tablica_sieć_stan(maszyna_Word wpis_WARTOŚĆ, maszyna_Word INDEKS) { return 망상태읽기(wpis_WARTOŚĆ, INDEKS); }
maszyna_Word Tablica_sieć_Ustawienia(maszyna_Word Akcja, maszyna_Word Adres, maszyna_Word maska_WARTOŚĆ, maszyna_Word brama_WARTOŚĆ) { return (uint32_t)konfigurować_sieć(Akcja, Adres, maska_WARTOŚĆ, brama_WARTOŚĆ); }
maszyna_Word Tablica_wysłać_odpowiedź(maszyna_Word Adres, maszyna_Word zamówić_WARTOŚĆ) { return (uint32_t)START_odpowiedź_test(Adres, zamówić_WARTOŚĆ); }
maszyna_Word 보드응답읽기(maszyna_Word wpis_WARTOŚĆ) { return (uint32_t)응답시험읽기(wpis_WARTOŚĆ); }
maszyna_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEKS=0; INDEKS<32; INDEKS++) Zamknij_sieć(INDEKS);
    for (unsigned INDEKS=0; INDEKS<4; INDEKS++) Tablica_formant_użytkownika(32+INDEKS);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (maszyna_rejestr(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    maszyna_rejestr(0xfe100020ul)=0x5a000000u | (maszyna_rejestr(0xfe100020ul)&~0xfffu) | 0x555;
    maszyna_rejestr(0xfe100024ul)=0x5a000000u | 10;
    maszyna_rejestr(0xfe10001cul)=0x5a000000u | (maszyna_rejestr(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

maszyna_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 bieżący_towar 크기를 읽는다. */
    const uint32_t zapytanie_WARTOŚĆ[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, wymagane_wysokość = 480;
    for (size_t 순번 = 0; 순번 < sizeof(zapytanie_WARTOŚĆ)/4; 순번++) skrzynka_pocztowa_dane[순번] = zapytanie_WARTOŚĆ[순번];
    if (skrzynka_pocztowa() && skrzynka_pocztowa_dane[4] == 0x80000008u &&
        skrzynka_pocztowa_dane[5] >= 640 && skrzynka_pocztowa_dane[5] <= 1920 &&
        skrzynka_pocztowa_dane[6] >= 480 && skrzynka_pocztowa_dane[6] <= 1080) {
        요청너비 = skrzynka_pocztowa_dane[5]; wymagane_wysokość = skrzynka_pocztowa_dane[6];
    }
    const uint32_t żądanie[] = {
        35 * 4, 0,
        0x48003, 8, 0, 요청너비, wymagane_wysokość,
        0x48004, 8, 0, 요청너비, wymagane_wysokość,
        0x48005, 4, 0, 32,
        0x48006, 4, 0, 1,
        0x48009, 8, 0, 0, 0,
        0x40001, 8, 0, 4096, 0,
        0x40008, 4, 0, 0,
        0
    };
    for (size_t 순번 = 0; 순번 < sizeof(żądanie)/4; 순번++) skrzynka_pocztowa_dane[순번] = żądanie[순번];
    // 위 메시지의 rzeczywisty_dane 길이를 używać_WARTOŚĆ: 태그 dołączać_wpis 시 długość_WARTOŚĆ 불일치를 방지한다.
    skrzynka_pocztowa_dane[0] = sizeof(żądanie);
    if (!skrzynka_pocztowa()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned odpowiedź_długość[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (skrzynka_pocztowa_dane[응답들[순번]] != (0x80000000u | odpowiedź_długość[순번])) return 0;
    uint32_t Tło_WARTOŚĆ = skrzynka_pocztowa_dane[28] & 0x3fffffffu;
    uint32_t Rozmiar = skrzynka_pocztowa_dane[29];
    uint32_t 받은너비 = skrzynka_pocztowa_dane[5], KWOTA_WYKUP_wysokość = skrzynka_pocztowa_dane[6], KWOTA_WYKUP_interlinia = skrzynka_pocztowa_dane[33];
    if (skrzynka_pocztowa_dane[15] != 32 || skrzynka_pocztowa_dane[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || KWOTA_WYKUP_wysokość < 480 || KWOTA_WYKUP_wysokość > 1080 ||
        skrzynka_pocztowa_dane[10] < 받은너비 || skrzynka_pocztowa_dane[11] < KWOTA_WYKUP_wysokość || skrzynka_pocztowa_dane[23] || skrzynka_pocztowa_dane[24] ||
        !Tło_WARTOŚĆ || Tło_WARTOŚĆ < 0x1000000 || (Tło_WARTOŚĆ & 3) || KWOTA_WYKUP_interlinia < 받은너비 * 4 || (KWOTA_WYKUP_interlinia & 3) ||
        (uint64_t)KWOTA_WYKUP_interlinia * KWOTA_WYKUP_wysokość > Rozmiar || (uint64_t)Tło_WARTOŚĆ + Rozmiar > 0x40000000u)
        return 0;
    Tablica_Przygotuj_rysunek((volatile uint32_t *)(uintptr_t)Tło_WARTOŚĆ, 받은너비, KWOTA_WYKUP_wysokość, KWOTA_WYKUP_interlinia);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 wątek_WARTOŚĆ. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } kontekst;
static kontekst 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int systemy_informacyjne_Bieganie[3] = {1, 0, 0};
static int bieżący_zadanie;
extern void przełączanie_kontekstu(kontekst *, kontekst *);
extern void 자바작업(int32_t);
maszyna_Word Tablica_Dochód(void) {
    network_poll();
    int Wstecz_towar = bieżący_zadanie, Dalej_towar = (Wstecz_towar + 1) % 3;
    while (Dalej_towar != Wstecz_towar && !systemy_informacyjne_Bieganie[Dalej_towar]) Dalej_towar = (Dalej_towar + 1) % 3;
    if (Dalej_towar != Wstecz_towar) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (systemy_informacyjne_Bieganie[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        bieżący_zadanie = Dalej_towar;
        przełączanie_kontekstu(&작업문맥들[Wstecz_towar], &작업문맥들[Dalej_towar]);
    }
    return 0;
}
static void zadanie_uruchomienie(void) {
    자바작업(bieżący_zadanie);
    systemy_informacyjne_Bieganie[bieżący_zadanie] = 0;
    Tablica_Dochód();
    커널중단("finished task resumed");
}
maszyna_Word Tablica_zadanie_Twórca(maszyna_Word identyfikator_WARTOŚĆ) {
    if (identyfikator_WARTOŚĆ < 1 || identyfikator_WARTOŚĆ > 2 || systemy_informacyjne_Bieganie[identyfikator_WARTOŚĆ]) return (uint32_t)-1;
    memset(&작업문맥들[identyfikator_WARTOŚĆ], 0, sizeof(kontekst));
    *(uint64_t *)쌓임공간들[identyfikator_WARTOŚĆ - 1] = 0x6b6f726f7373746bull;
    작업문맥들[identyfikator_WARTOŚĆ].저장값[11] = (uintptr_t)zadanie_uruchomienie;
    작업문맥들[identyfikator_WARTOŚĆ].저장값[12] = (uintptr_t)(쌓임공간들[identyfikator_WARTOŚĆ - 1] + sizeof(쌓임공간들[0]));
    systemy_informacyjne_Bieganie[identyfikator_WARTOŚĆ] = 1;
    return 0;
}
maszyna_Word Tablica_zadanie_Stan(maszyna_Word identyfikator_WARTOŚĆ) { return identyfikator_WARTOŚĆ < 3 ? systemy_informacyjne_Bieganie[identyfikator_WARTOŚĆ] : (uint32_t)-1; }
extern maszyna_Word drzewo_obiektów_aplikacji_Pamięć_WYSZUKAJ(maszyna_Word);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
maszyna_Word Tablica_zapytanie_System(maszyna_Word wpis_WARTOŚĆ, maszyna_Word INDEKS) {
    if (wpis_WARTOŚĆ==0) return 팔기억킬로바이트;
    if (wpis_WARTOŚĆ==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (wpis_WARTOŚĆ==2 || wpis_WARTOŚĆ==3) return drzewo_obiektów_aplikacji_Pamięć_WYSZUKAJ(wpis_WARTOŚĆ==3);
    if (wpis_WARTOŚĆ==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (wpis_WARTOŚĆ==5) return 80*1024; /* Wykonaj_polecenie ADRES_region 16 MiB + 네 세션 보관 ADRES_region. */
    if (wpis_WARTOŚĆ>=20) return 사용자상태읽기(wpis_WARTOŚĆ-20, INDEKS);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[bieżący_zadanie]; }
