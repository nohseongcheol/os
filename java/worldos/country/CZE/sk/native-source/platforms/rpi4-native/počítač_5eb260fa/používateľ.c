#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 Vykonať_príkaz počítač_5eb260fa vrstva_VALUE. Súbor údaje/정책은 기존 AOT Java 커널에 위임한다.
#include "používateľ.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../sieť_Vrstvy/sieť_Vrstvy.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define počítač_register(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_distribútor 0xff841000ul
#define IRQ_procesor_rozhranie 0xff842000ul
#define veľkosť_stránky 4096ul
#define prístup_fixka (1ul << 10)
#define nie_Vykonať_povolenie (1ul << 53)
#define používateľ_nie_Vykonať (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | prístup_fixka)
#define jadro_strana (3ul | 보통기억 | nie_Vykonať_povolenie | používateľ_nie_Vykonať)
#define používateľ_na_čítanie_a_zapisovanie (3ul | 보통기억 | (1ul << 6) | nie_Vykonať_povolenie | používateľ_nie_Vykonať)
#define používateľ_iba_na_čítanie (3ul | 보통기억 | (3ul << 6) | nie_Vykonať_povolenie | používateľ_nie_Vykonať)
#define 사용자읽고실행 (3ul | 보통기억 | (3ul << 6) | nie_Vykonať_povolenie)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t Panel_pixel(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t Panel_Terminál(uintptr_t);
extern int Terminál_čakajúci(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int používateľ_životopis(používateľ_rám *,void *);
extern void 사용자실수보관(void *);
extern int používateľ_zadať(uintptr_t položka_bod, uintptr_t Vrstvy_Úložisko, uintptr_t 전달값);
extern void používateľ_vrátiť(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t koreň_adresa[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t strana_Zoznam[používateľ_strana_COUNT] __attribute__((aligned(4096)));
static uint8_t Povolenia_Zoznam[používateľ_strana_COUNT];
static int Aktívny, Súbor_Zoznam[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int Zavrieť_soket_účastník(unsigned Súbor_rukoväť){return Súbor_rukoväť<40?자바전문닫기(Súbor_rukoväť):자바흐름닫기(Súbor_rukoväť);}
static uint64_t FREQUENCY, termín_čas;
static uintptr_t halda_ukončiť_hovor;
// jadro_VALUE 셸이 준비한 UTF-8 Argumenty. EL0에는 inštancia_VALUE 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,interaktívny,리눅스규약,Súbor_Zoznam[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char argument_pole[8][256],Povolenia_Zoznam[používateľ_strana_COUNT];
    uintptr_t halda_Úložisko; používateľ_rám 실행틀;
    unsigned char plávajúci_bod_Stav[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int vlastník_objekt,interaktívny;
static uint32_t číslo_používateľa[4], používateľ_START_čas[4], 사용자누적시각[4], 사용자실행시각[4], Ďalej_číslo_používateľa=10;
static unsigned char používateľ_príkaz_názov[4][288];
uint32_t 사용자상태읽기(unsigned položka_VALUE, unsigned INDEX) {
    unsigned pozičný_index=INDEX&3;
    int Stav_VALUE=(Aktívny && vlastník_objekt==(int)pozičný_index) ? 1 : 저장값[pozičný_index].멈춤상태 ? 2 : 0;
    if (položka_VALUE==0) return Stav_VALUE;
    if (!Stav_VALUE) return 0;
    if (položka_VALUE==1) return číslo_používateľa[pozičný_index];
    if (položka_VALUE==2) {
        unsigned char *쪽들=Stav_VALUE==1?Povolenia_Zoznam:저장값[pozičný_index].Povolenia_Zoznam;
        unsigned strana_COUNT=0; for (unsigned 순번=0; 순번<používateľ_strana_COUNT; 순번++) if(쪽들[순번]) strana_COUNT++;
        return strana_COUNT*4;
    }
    if (položka_VALUE==3) return (uint32_t)보드밀리초()-používateľ_START_čas[pozičný_index];
    if (položka_VALUE==4) return 사용자누적시각[pozičný_index]+(Stav_VALUE==1?(uint32_t)보드밀리초()-사용자실행시각[pozičný_index]:0);
    if (položka_VALUE==5) return INDEX/4<sizeof(používateľ_príkaz_názov[0])?používateľ_príkaz_názov[pozičný_index][INDEX/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t položka_COUNT_8f7753a1) {
    if (Aktívny || položka_COUNT_8f7753a1 > 8) return (uint32_t)-22;
    전달인수개수 = položka_COUNT_8f7753a1;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t LOOKUP_INDEX, uintptr_t v_termíne_splatnosti_pozícia, uintptr_t Byte_údaje) {
    if (Aktívny || LOOKUP_INDEX >= 전달인수개수 || v_termíne_splatnosti_pozícia >= 255 || v_termíne_splatnosti_pozícia != 전달인수길이[LOOKUP_INDEX] || !Byte_údaje || Byte_údaje > 255)
        return (uint32_t)-22;
    전달인수[LOOKUP_INDEX][v_termíne_splatnosti_pozícia] = Byte_údaje;
    전달인수길이[LOOKUP_INDEX] = v_termíne_splatnosti_pozícia + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Hodiny_VALUE(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Stop_TIMEOUT(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    počítač_register(IRQ_distribútor + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void START_TIMEOUT(void) {
    uint64_t 간격 = FREQUENCY * 2, zapnúť = 1;
    termín_čas = Hodiny_VALUE() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(zapnúť) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned blok_údajov = 0; blok_údajov < 4; blok_údajov++) {
        koreň_adresa[blok_údajov] = (uintptr_t)가운데[blok_údajov] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t adresa = ((uintptr_t)blok_údajov << 30) | ((uintptr_t)순번 << 21);
            가운데[blok_údajov][순번] = adresa | 1 | prístup_fixka | používateľ_nie_Vykonať;
            if (adresa >= 0xfc000000ul) 가운데[blok_údajov][순번] |= nie_Vykonať_povolenie; // Device-nGnRnE
            else 가운데[blok_údajov][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned SECOND_VALUE = 0; SECOND_VALUE < používateľ_strana_COUNT / 512; SECOND_VALUE++)
        가운데[0][(používateľ_BASE >> 21) + SECOND_VALUE] = (uintptr_t)(strana_Zoznam + SECOND_VALUE * 512) | 3;
    for (unsigned 순번 = 0; 순번 < používateľ_strana_COUNT; 순번++) strana_Zoznam[순번] = (používateľ_BASE + 순번 * veľkosť_stránky) | jadro_strana;
    uint64_t Pamäť_atribút_register = 0x4400, adresa_Preklad_riadenie = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Pamäť_atribút_register), "r"(adresa_Preklad_riadenie), "r"((uintptr_t)koreň_adresa) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t plávajúci_bod_Stav = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(plávajúci_bod_Stav) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    Stop_TIMEOUT();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 položka_bod_VALUE 때만 Povoliť_VALUE.
    počítač_register(IRQ_distribútor) = 0;
    počítač_register(IRQ_distribútor + 0x180) = 0xffffffff;
    počítač_register(IRQ_distribútor + 0x80) = 0xffffffff;
    počítač_register(IRQ_distribútor + 0x280) = 1u << 30;
    počítač_register(IRQ_distribútor + 0x41c) = 0x80808080;
    počítač_register(IRQ_distribútor + 0x100) = 1u << 30;
    počítač_register(IRQ_procesor_rozhranie + 4) = 0xff;
    počítač_register(IRQ_procesor_rozhranie + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 수 있다.
    int Zabezpečenie = (počítač_register(IRQ_distribútor + 4) & (1u << 10)) != 0;
    počítač_register(IRQ_distribútor) = Zabezpečenie ? 1 : 3;
    počítač_register(IRQ_procesor_rozhranie) = Zabezpečenie ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t Typ_oblasť, počítač_Typ; uint32_t číslo_verzie;
    uint64_t položka_bod, program_Nadpis_Posun, hlavička_sekcie_Posun; uint32_t konfigurácia_Background_Intelligent_Transfer_Service;
    uint16_t spustiteľný_súbor_Nadpis_zmeniť_veľkosť, program_Nadpis_položka_zmeniť_veľkosť, program_Nadpis_COUNT, hlavička_sekcie_položka_zmeniť_veľkosť, hlavička_sekcie_COUNT, sekcia_názov_tabuľka_INDEX;
} 실행파일머리;
typedef struct { uint32_t Typ_oblasť, konfigurácia_Background_Intelligent_Transfer_Service; uint64_t Posun_VALUE, adresa, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(používateľ_rám) == 272, "exception assembly layout");
static int 포함된범위(uint64_t Posun_VALUE, uint64_t Veľkosť, uint64_t ukončiť_hovor_Posun) {
    return Posun_VALUE <= ukončiť_hovor_Posun && Veľkosť <= ukončiť_hovor_Posun - Posun_VALUE;
}
static int 부가정보검사(const unsigned char *údaje_pozícia, size_t Veľkosť) {
    size_t v_termíne_splatnosti_pozícia = 0;
    while (포함된범위(v_termíne_splatnosti_pozícia, 12, Veľkosť)) {
        uint32_t 낱말들[3]; memcpy(낱말들, údaje_pozícia + v_termíne_splatnosti_pozícia, 12); v_termíne_splatnosti_pozícia += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(v_termíne_splatnosti_pozícia, 이름영역크기, Veľkosť) || !포함된범위(v_termíne_splatnosti_pozícia + 이름영역크기, 설명크기, Veľkosť)) return 0;
        const unsigned char Názov[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Názov) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Názov); 순번++) if (údaje_pozícia[v_termíne_splatnosti_pozícia + 순번] != Názov[순번]) 일치 = 0;
        uint32_t číslo_verzie = 0;
        if (일치) memcpy(&číslo_verzie, údaje_pozícia + v_termíne_splatnosti_pozícia + 이름영역크기, 4);
        if (일치 && číslo_verzie == 1) return 1;
        v_termíne_splatnosti_pozícia += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *údaje, size_t Veľkosť, int 리눅스방식) {
    if (Veľkosť < sizeof(실행파일머리)) return používateľ_spustiteľný_súbor_Chyba;
    실행파일머리 spustiteľný_súbor_Nadpis; memcpy(&spustiteľný_súbor_Nadpis, údaje, sizeof(spustiteľný_súbor_Nadpis));
    if (spustiteľný_súbor_Nadpis.형식식별[0] != 127 || spustiteľný_súbor_Nadpis.형식식별[1] != 'E' || spustiteľný_súbor_Nadpis.형식식별[2] != 'L' || spustiteľný_súbor_Nadpis.형식식별[3] != 'F' ||
        spustiteľný_súbor_Nadpis.형식식별[4] != 2 || spustiteľný_súbor_Nadpis.형식식별[5] != 1 || spustiteľný_súbor_Nadpis.형식식별[6] != 1 || (spustiteľný_súbor_Nadpis.형식식별[7] != 0 && (!리눅스방식 || spustiteľný_súbor_Nadpis.형식식별[7] != 3)) ||
        spustiteľný_súbor_Nadpis.Typ_oblasť != 2 || spustiteľný_súbor_Nadpis.počítač_Typ != 183 || spustiteľný_súbor_Nadpis.číslo_verzie != 1 || spustiteľný_súbor_Nadpis.konfigurácia_Background_Intelligent_Transfer_Service || spustiteľný_súbor_Nadpis.spustiteľný_súbor_Nadpis_zmeniť_veľkosť != sizeof(spustiteľný_súbor_Nadpis) ||
        spustiteľný_súbor_Nadpis.program_Nadpis_položka_zmeniť_veľkosť != sizeof(실행파일구획) || !spustiteľný_súbor_Nadpis.program_Nadpis_COUNT || spustiteľný_súbor_Nadpis.program_Nadpis_COUNT > 16 ||
        spustiteľný_súbor_Nadpis.program_Nadpis_Posun < sizeof(spustiteľný_súbor_Nadpis) || !포함된범위(spustiteľný_súbor_Nadpis.program_Nadpis_Posun, (uint64_t)spustiteľný_súbor_Nadpis.program_Nadpis_COUNT * sizeof(실행파일구획), Veľkosť)) return používateľ_spustiteľný_súbor_Chyba;
    uint8_t 사용량[(používateľ_IMAGE_ukončiť_hovor - používateľ_BASE) / veľkosť_stránky] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < spustiteľný_súbor_Nadpis.program_Nadpis_COUNT; 순번++) {
        실행파일구획 údaje_pozícia; memcpy(&údaje_pozícia, údaje + spustiteľný_súbor_Nadpis.program_Nadpis_Posun + 순번 * sizeof(údaje_pozícia), sizeof(údaje_pozícia));
        if (údaje_pozícia.Typ_oblasť == 4) {
            if (!포함된범위(údaje_pozícia.Posun_VALUE, údaje_pozícia.파일영역크기, Veľkosť)) return používateľ_spustiteľný_súbor_Chyba;
            if (부가정보검사(údaje + údaje_pozícia.Posun_VALUE, údaje_pozícia.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (údaje_pozícia.Typ_oblasť == 0 || údaje_pozícia.Typ_oblasť == 6 || (údaje_pozícia.Typ_oblasť == 0x6474e551 && !(údaje_pozícia.konfigurácia_Background_Intelligent_Transfer_Service & 1))) continue;
        if (údaje_pozícia.Typ_oblasť != 1) return používateľ_spustiteľný_súbor_Chyba; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!údaje_pozícia.기억영역크기) continue;
        if (údaje_pozícia.konfigurácia_Background_Intelligent_Transfer_Service & ~7u || !(údaje_pozícia.konfigurácia_Background_Intelligent_Transfer_Service & 4) || (údaje_pozícia.konfigurácia_Background_Intelligent_Transfer_Service & 3) == 3 || údaje_pozícia.파일영역크기 > údaje_pozícia.기억영역크기 ||
            (údaje_pozícia.파일영역크기 && !포함된범위(údaje_pozícia.Posun_VALUE, údaje_pozícia.파일영역크기, Veľkosť)) || údaje_pozícia.adresa < používateľ_BASE ||
            !포함된범위(údaje_pozícia.adresa, údaje_pozícia.기억영역크기, používateľ_IMAGE_ukončiť_hovor) ||
            (!리눅스방식 && ((údaje_pozícia.adresa & (veľkosť_stránky - 1)) || (údaje_pozícia.Posun_VALUE & (veľkosť_stránky - 1)) || údaje_pozícia.맞춤 != veľkosť_stránky)) ||
            (리눅스방식 && (((údaje_pozícia.adresa ^ údaje_pozícia.Posun_VALUE) & (veľkosť_stránky - 1)) || !údaje_pozícia.맞춤 ||
                (údaje_pozícia.맞춤 & (údaje_pozícia.맞춤 - 1)) || údaje_pozícia.맞춤 > 0x200000 || ((údaje_pozícia.adresa ^ údaje_pozícia.Posun_VALUE) & (údaje_pozícia.맞춤 - 1))))) return používateľ_spustiteľný_súbor_Chyba;
        unsigned 첫항목 = (údaje_pozícia.adresa - používateľ_BASE) / veľkosť_stránky;
        unsigned položka_COUNT_8f7753a1 = ((údaje_pozícia.adresa & (veľkosť_stránky - 1)) + údaje_pozícia.기억영역크기 + veľkosť_stránky - 1) / veľkosť_stránky;
        for (unsigned strana_VALUE = 첫항목; strana_VALUE < 첫항목 + položka_COUNT_8f7753a1; strana_VALUE++) {
            if (사용량[strana_VALUE]) return používateľ_spustiteľný_súbor_Chyba;
            사용량[strana_VALUE] = 1;
        }
        if ((údaje_pozícia.konfigurácia_Background_Intelligent_Transfer_Service & 1) && spustiteľný_súbor_Nadpis.položka_bod >= údaje_pozícia.adresa && spustiteľný_súbor_Nadpis.položka_bod < údaje_pozícia.adresa + údaje_pozícia.파일영역크기 && !(spustiteľný_súbor_Nadpis.položka_bod & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : používateľ_spustiteľný_súbor_Chyba;
}
int 사용자실행파일검사(const unsigned char *údaje, size_t Veľkosť) { return 실행파일검사(údaje, Veľkosť, 0); }
static void rozloženie_strany(uintptr_t adresa, uint64_t konfigurácia_Background_Intelligent_Transfer_Service, unsigned povolenia) {
    unsigned LOOKUP_INDEX = (adresa - používateľ_BASE) / veľkosť_stránky;
    strana_Zoznam[LOOKUP_INDEX] = adresa | konfigurácia_Background_Intelligent_Transfer_Service;
    Povolenia_Zoznam[LOOKUP_INDEX] = povolenia;
}
static int používateľ_rozsah(uintptr_t adresa, size_t položka_COUNT_8f7753a1, int 쓰는중) {
    if (adresa < používateľ_BASE || !포함된범위(adresa, položka_COUNT_8f7753a1, používateľ_ukončiť_hovor)) return 0;
    if (!položka_COUNT_8f7753a1) return 1;
    unsigned 첫항목 = (adresa - používateľ_BASE) / veľkosť_stránky, 마지막 = (adresa + položka_COUNT_8f7753a1 - 1 - používateľ_BASE) / veľkosť_stránky;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(Povolenia_Zoznam[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int inštancia_cesta(uintptr_t adresa, char *Cesta) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!používateľ_rozsah(adresa, 1, 0)) return -14;
        Cesta[순번] = *(const char *)adresa++;
        if (!Cesta[순번]) return 0;
    }
    return -36;
}
static intptr_t jadro_KR(intptr_t KR) { return KR < 0 ? -chybové_číslo : KR; }
static int 대응파일기술자(uint64_t Súbor_rukoväť) { return Súbor_rukoväť >= 3 && Súbor_rukoväť < 19 ? Súbor_Zoznam[Súbor_rukoväť - 3] : -1; }
static int soket_účastník_vlastník(uint64_t Súbor_rukoväť) { return Súbor_rukoväť >= 32 && Súbor_rukoväť < 56 && 통신끝점들[Súbor_rukoväť - 32]; }
static int adresa_vstup(uintptr_t 가리킴값, size_t dĺžka_VALUE, struct pk_sockaddr_in *adresa) {
    if (dĺžka_VALUE != sizeof(*adresa)) return -22;
    if (!používateľ_rozsah(가리킴값, dĺžka_VALUE, 0)) return -14;
    memcpy(adresa, (const void *)가리킴값, sizeof(*adresa));
    return adresa->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t dĺžka_ukazovateľ, pk_socklen_t *medzipamäť_kapacita) {
    if (!používateľ_rozsah(dĺžka_ukazovateľ, sizeof(*medzipamäť_kapacita), 1)) return -14;
    memcpy(medzipamäť_kapacita, (const void *)dĺžka_ukazovateľ, sizeof(*medzipamäť_kapacita));
    if (*medzipamäť_kapacita > sizeof(struct pk_sockaddr_in)) *medzipamäť_kapacita = sizeof(struct pk_sockaddr_in);
    if (*medzipamäť_kapacita && !používateľ_rozsah(가리킴값, *medzipamäť_kapacita, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t dĺžka_ukazovateľ, pk_socklen_t medzipamäť_kapacita, int adresa, int číslo_portu) {
    struct pk_sockaddr_in VALUE; memset(&VALUE, 0, sizeof(VALUE));
    VALUE.sin_family = AF_INET; VALUE.sin_port = pk_htons(číslo_portu); VALUE.sin_addr.s_addr = pk_htonl(adresa);
    if (medzipamäť_kapacita) memcpy((void *)가리킴값, &VALUE, medzipamäť_kapacita);
    pk_socklen_t dĺžka_VALUE = sizeof(VALUE); memcpy((void *)dĺžka_ukazovateľ, &dĺžka_VALUE, sizeof(dĺžka_VALUE));
}
extern uintptr_t Panel_Kanál(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(používateľ_rám *Súbor_položka) {
    uintptr_t 첫째값 = Súbor_položka->register_údaje[0], SECOND_VALUE = Súbor_položka->register_údaje[1], bod_kódu = Súbor_položka->register_údaje[2];
    char Cesta[65];
    int Súbor_rukoväť, KR;
    switch (Súbor_položka->register_údaje[8]) {
    case 0: return 1; // vlastné ABI 버전
    case 1: // write: ukazovateľ 전체를 검사한 BACK_VALUE Výstup/Súbor zmeniť_VALUE
        if (bod_kódu > 65536) return -22;
        if (!používateľ_rozsah(SECOND_VALUE, bod_kódu, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=Hodiny_VALUE();
            for (size_t 순번 = 0; 순번 < bod_kódu; 순번++) Panel_Kanál(첫째값, ((const unsigned char *)SECOND_VALUE)[순번]);
            /* 큰 tty를 그린 jadro_VALUE 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(interaktívny){
                termín_čas+=Hodiny_VALUE()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(termín_čas) : "memory");
            }
            return bod_kódu;
        }
        if(첫째값>=40&&soket_účastník_vlastník(첫째값)){
            size_t položka_COUNT=bod_kódu>512?512:bod_kódu;for(size_t 순번=0;순번<položka_COUNT;순번++)자바전문넣기(순번,((const unsigned char *)SECOND_VALUE)[순번]);return 자바흐름쓰기(첫째값,položka_COUNT);
        }
        Súbor_rukoväť = 대응파일기술자(첫째값); if (Súbor_rukoväť < 0) return -9;
        return jadro_KR(pk_write(Súbor_rukoväť, (const void *)SECOND_VALUE, bod_kódu));
    case 2:
        if (bod_kódu > 65536) return -22;
        if (!používateľ_rozsah(SECOND_VALUE, bod_kódu, 1)) return -14;
        if (첫째값 == 0) {
            size_t položka_COUNT = 0;
            while (položka_COUNT < bod_kódu) {
                int znak_VALUE = (int32_t)보드글자읽기(); if (znak_VALUE == -2) return položka_COUNT; if (znak_VALUE < 0) break;
                ((unsigned char *)SECOND_VALUE)[položka_COUNT++] = znak_VALUE;
            }
            return položka_COUNT ? (intptr_t)položka_COUNT : (bod_kódu ? -11 : 0);
        }
        if(첫째값>=40&&soket_účastník_vlastník(첫째값)){
            KR=자바흐름읽기(첫째값,bod_kódu>512?512:bod_kódu);if(KR>0)for(int 순번=0;순번<KR;순번++)((unsigned char *)SECOND_VALUE)[순번]=자바전문얻기(순번);return KR;
        }
        Súbor_rukoväť = 대응파일기술자(첫째값); if (Súbor_rukoväť < 0) return -9;
        return jadro_KR(pk_read(Súbor_rukoväť, (void *)SECOND_VALUE, bod_kódu));
    case 3:
        KR = inštancia_cesta(첫째값, Cesta); if (KR) return KR;
        if (SECOND_VALUE > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (Súbor_Zoznam[순번] < 0) {
            Súbor_rukoväť = pk_open(Cesta, (int)SECOND_VALUE, 0600);
            if (Súbor_rukoväť < 0) return -chybové_číslo;
            Súbor_Zoznam[순번] = Súbor_rukoväť; return 순번 + 3;
        }
        return -24;
    case 4:
        if (soket_účastník_vlastník(첫째값)) { KR = Zavrieť_soket_účastník(첫째값); if (!KR) 통신끝점들[첫째값 - 32] = 0; return KR; }
        Súbor_rukoväť = 대응파일기술자(첫째값); if (Súbor_rukoväť < 0) return -9;
        KR = pk_close(Súbor_rukoväť); if (!KR) Súbor_Zoznam[첫째값 - 3] = -1;
        return jadro_KR(KR);
    case 5:
        Súbor_rukoväť = 대응파일기술자(첫째값); if (Súbor_rukoväť < 0) return -9;
        if (bod_kódu > 2) return -22;
        return jadro_KR(pk_lseek(Súbor_rukoväť, (int64_t)SECOND_VALUE, bod_kódu));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 používateľ RW/NX halda_VALUE, 새로 노출되는 페이지는 0으로 incializovať
        if (!첫째값) return halda_ukončiť_hovor;
        if (첫째값 < používateľ_IMAGE_ukončiť_hovor || 첫째값 > používateľ_halda_ukončiť_hovor) return -12;
        uintptr_t 이전쪽들 = (halda_ukončiť_hovor + veľkosť_stránky - 1) & ~(veľkosť_stránky - 1);
        uintptr_t 새쪽들 = (첫째값 + veľkosť_stránky - 1) & ~(veľkosť_stránky - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t údaje_pozícia = 이전쪽들; údaje_pozícia < 새쪽들; údaje_pozícia += veľkosť_stránky) rozloženie_strany(údaje_pozícia, jadro_strana, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t údaje_pozícia = 이전쪽들; údaje_pozícia < 새쪽들; údaje_pozícia += veľkosť_stránky) rozloženie_strany(údaje_pozícia, používateľ_na_čítanie_a_zapisovanie, 3);
        } else {
            for (uintptr_t údaje_pozícia = 새쪽들; údaje_pozícia < 이전쪽들; údaje_pozícia += veľkosť_stránky) {
                strana_Zoznam[(údaje_pozícia - používateľ_BASE) / veľkosť_stránky] = 0; Povolenia_Zoznam[(údaje_pozícia - používateľ_BASE) / veľkosť_stránky] = 0;
            }
        }
        halda_ukončiť_hovor = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        Súbor_rukoväť = 대응파일기술자(첫째값); return Súbor_rukoväť < 0 ? -9 : jadro_KR(pk_size(Súbor_rukoväť));
    case 10:
        Súbor_rukoväť = 대응파일기술자(첫째값); return Súbor_rukoväť < 0 ? -9 : jadro_KR(pk_ftruncate(Súbor_rukoväť, (int64_t)SECOND_VALUE));
    case 11:
        KR = inštancia_cesta(첫째값, Cesta); return KR ? KR : jadro_KR(pk_unlink(Cesta));
    case 12:
        Súbor_rukoväť = 대응파일기술자(첫째값); return Súbor_rukoväť < 0 ? -9 : jadro_KR(pk_fsync(Súbor_rukoväť));
    case 13: { // 그래픽 기초 API: používateľ 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = Súbor_položka->register_údaje[3], 높이값 = Súbor_položka->register_údaje[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SECOND_VALUE > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - SECOND_VALUE) return -22;
        for (uintptr_t Y_súradnica = SECOND_VALUE; Y_súradnica < SECOND_VALUE + 높이값; Y_súradnica++) for (uintptr_t X_súradnica = 첫째값; X_súradnica < 첫째값 + 너비값; X_súradnica++) Panel_pixel(X_súradnica, Y_súradnica, bod_kódu);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=položka_COUNT; args(index,buffer,capacity)=UTF-8 dĺžka_VALUE
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (bod_kódu <= 전달인수길이[첫째값]) return -36;
        if (!používateľ_rozsah(SECOND_VALUE, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SECOND_VALUE, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;interaktívny=1;return Panel_Terminál(13);}
        if(첫째값==2){interaktívny=0;return 0;}
        if(첫째값==3)return Panel_Terminál(13);
        if(첫째값!=1||!interaktívny)return -22;
        KR=(int32_t)보드글자읽기();
        if(KR==-4096)return KR;
        START_TIMEOUT();return KR<0?-11:KR;
    case 17: { // 유한한 협력 počkaj_VALUE: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t ukončiť_hovor_čas = Hodiny_VALUE() + FREQUENCY * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Hodiny_VALUE() < ukončiť_hovor_čas);
        START_TIMEOUT(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 nadradený_VALUE·빈 폴더를 검사한다.
        if (SECOND_VALUE > 2) return -22;
        KR = inštancia_cesta(첫째값, Cesta); if (KR) return KR;
        unsigned dĺžka_VALUE = 0; while (Cesta[dĺžka_VALUE]) dĺžka_VALUE++;
        KR = 자바경로시작(dĺžka_VALUE); if (KR < 0) return KR;
        for (unsigned 순번 = 0; 순번 < dĺžka_VALUE; 순번++) 자바경로바이트(순번, (unsigned char)Cesta[순번]);
        return SECOND_VALUE == 0 ? 자바항목종류() : SECOND_VALUE == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int znak_VALUE=(int32_t)보드글자읽기();if(znak_VALUE==-4096)return znak_VALUE;if(znak_VALUE>=0)화면누름(vlastník_objekt,znak_VALUE);START_TIMEOUT();}
        if(첫째값==3&&bod_kódu){if(!자바셸대화형())return -95;interaktívny=1;Panel_Terminál(300);}
        return 화면호출(vlastník_objekt,첫째값,SECOND_VALUE,bod_kódu,Súbor_položka->register_údaje[3],Súbor_položka->register_údaje[4],Súbor_položka->register_údaje[5]);
    case 21:
        if(bod_kódu>127)return -22;if(!používateľ_rozsah(SECOND_VALUE,bod_kódu*sizeof(uint32_t),0))return -14;
        return 화면글(vlastník_objekt,첫째값,(const uint32_t *)SECOND_VALUE,bod_kódu);
    case 22: // 화면 Veľkosť dotaz_VALUE: 0=너비, 1=výška_VALUE. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SECOND_VALUE==SOCK_STREAM&&(bod_kódu==0||bod_kódu==6))KR=자바흐름만들기();
        else if(SECOND_VALUE==SOCK_DGRAM&&(bod_kódu==0||bod_kódu==IPPROTO_UDP))KR=자바전문만들기(첫째값,SECOND_VALUE,bod_kódu);
        else return -93;
        if (KR >= 32 && KR < 56) 통신끝점들[KR - 32] = 1;
        return KR;
    case 33: {
        if (!soket_účastník_vlastník(첫째값)) return -9;
        struct pk_sockaddr_in adresa;
        KR = adresa_vstup(SECOND_VALUE, bod_kódu, &adresa); if (KR) return KR;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(adresa.sin_addr.s_addr),pk_htons(adresa.sin_port)):자바전문묶기(첫째값, pk_htonl(adresa.sin_addr.s_addr), pk_htons(adresa.sin_port));
    }
    case 34: {
        if (!soket_účastník_vlastník(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Súbor_položka->register_údaje[3]) return -95;
        if (bod_kódu > 512) return -90;
        if (bod_kódu && !používateľ_rozsah(SECOND_VALUE, bod_kódu, 0)) return -14;
        struct pk_sockaddr_in adresa;
        KR = adresa_vstup(Súbor_položka->register_údaje[4], Súbor_položka->register_údaje[5], &adresa); if (KR) return KR;
        for (unsigned 순번 = 0; 순번 < bod_kódu; 순번++) 자바전문넣기(순번, ((const unsigned char *)SECOND_VALUE)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(adresa.sin_addr.s_addr), pk_htons(adresa.sin_port), bod_kódu);
    }
    case 35: {
        if (!soket_účastník_vlastník(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Súbor_položka->register_údaje[3]) return -95;
        if (bod_kódu > 512) return -90;
        if (bod_kódu && !používateľ_rozsah(SECOND_VALUE, bod_kódu, 1)) return -14;
        pk_socklen_t medzipamäť_kapacita = 0;
        if (Súbor_položka->register_údaje[4]) { KR = 주소출력검사(Súbor_položka->register_údaje[4], Súbor_položka->register_údaje[5], &medzipamäť_kapacita); if (KR) return KR; }
        KR = 자바전문받기(첫째값, bod_kódu); if (KR < 0) return KR;
        for (int 순번 = 0; 순번 < KR; 순번++) ((unsigned char *)SECOND_VALUE)[순번] = 자바전문얻기(순번);
        if (Súbor_položka->register_údaje[4]) 주소출력(Súbor_položka->register_údaje[4], Súbor_položka->register_údaje[5], medzipamäť_kapacita, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return KR;
    }
    case 36: {
        if (!soket_účastník_vlastník(첫째값)) return -9;
        pk_socklen_t medzipamäť_kapacita;
        KR = 주소출력검사(SECOND_VALUE, bod_kódu, &medzipamäť_kapacita); if (KR) return KR;
        주소출력(SECOND_VALUE,bod_kódu,medzipamäť_kapacita,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!soket_účastník_vlastník(첫째값))return -9;struct pk_sockaddr_in adresa;
        KR=adresa_vstup(SECOND_VALUE,bod_kódu,&adresa);if(KR)return KR;
        return 자바흐름연결(첫째값,pk_htonl(adresa.sin_addr.s_addr),pk_htons(adresa.sin_port));
    }
    case 38: return 첫째값>=40&&soket_účastník_vlastník(첫째값)?자바흐름듣기(첫째값,SECOND_VALUE):-9;
    case 39:
        if(첫째값<40||!soket_účastník_vlastník(첫째값))return -9;
        if(SECOND_VALUE||bod_kódu)return -95;KR=자바흐름연결받기(첫째값);if(KR>=40&&KR<56)통신끝점들[KR-32]=1;return KR;
    case 40: return 첫째값>=40&&soket_účastník_vlastník(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(používateľ_rám *Súbor_položka) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(Súbor_položka) : 자체체계호출(Súbor_položka);
}
static void vrátiť_jadro(používateľ_rám *Súbor_položka, int KR) {
    Stop_TIMEOUT();
    Súbor_položka->register_údaje[0] = (uint64_t)(int64_t)KR;
    Súbor_položka->príkaz_pozícia = (uintptr_t)používateľ_vrátiť;
    Súbor_položka->Stav_kód = 0x3c5; // EL1h, DAIF masked
}
int používateľská_výnimka(používateľ_rám *Súbor_položka, unsigned INTERCEPT) {
    if (!Aktívny || (Súbor_položka->Stav_kód & 15) != 0) return 0;
    if (INTERCEPT) {
        uint32_t uznanie_VALUE = počítač_register(IRQ_procesor_rozhranie + 0xc), identifikátor_VALUE = uznanie_VALUE & 1023;
        if (identifikátor_VALUE == 30) { vrátiť_jadro(Súbor_položka, používateľ_TIMEOUT); počítač_register(IRQ_procesor_rozhranie + 0x10) = uznanie_VALUE; return 1; }
        if (identifikátor_VALUE < 1020) počítač_register(IRQ_procesor_rozhranie + 0x10) = uznanie_VALUE;
        return 1;
    }
    uint64_t výnimka_Stav; __asm__ volatile("mrs %0, esr_el1" : "=r"(výnimka_Stav));
    if (Hodiny_VALUE() >= termín_čas) { vrátiť_jadro(Súbor_položka, používateľ_TIMEOUT); return 1; }
    unsigned výnimka_oblasť = výnimka_Stav >> 26;
    if (výnimka_oblasť == 0x15 && (výnimka_Stav & 0xffff) == 0) {
        if (리눅스규약 ? Súbor_položka->register_údaje[8] == 93 || Súbor_položka->register_údaje[8] == 94 : Súbor_položka->register_údaje[8] == 6) vrátiť_jadro(Súbor_položka, (int)(Súbor_položka->register_údaje[0] & 255));
        else {
            intptr_t KR=체계호출(Súbor_položka);
            if(KR==-4096&&interaktívny){
                저장값[vlastník_objekt].실행틀=*Súbor_položka;저장값[vlastník_objekt].실행틀.príkaz_pozícia-=4;
                사용자실수보관(저장값[vlastník_objekt].plávajúci_bod_Stav);vrátiť_jadro(Súbor_položka,사용자중단됨);
            }else Súbor_položka->register_údaje[0]=(uint64_t)KR;
        }
    } else vrátiť_jadro(Súbor_položka, výnimka_oblasť == 0x24 ? používateľ_údaje_Chyba : výnimka_oblasť == 0x20 ? 사용자실행오류 : používateľ_neplatné_inštrukcia);
    return 1;
}

// 생성된 const ELF Skupina_VALUE: 실행은 반드시 program_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *údaje; size_t Veľkosť; unsigned 전달값; } program;
#include "programs.h"
static void *snímka(unsigned pozičný_index){return (void *)(0x04000000ul+pozičný_index*(používateľ_ukončiť_hovor-používateľ_BASE));}
static int Dokončiť_program(int KR){
    사용자누적시각[vlastník_objekt]+=(uint32_t)보드밀리초()-사용자실행시각[vlastník_objekt];
    Stop_TIMEOUT();Aktívny=0;
    if(KR==사용자중단됨){
        저장된작업 *reťazec_údaje=&저장값[vlastník_objekt];reťazec_údaje->멈춤상태=1;reťazec_údaje->interaktívny=interaktívny;reťazec_údaje->리눅스규약=리눅스규약;reťazec_údaje->halda_Úložisko=halda_ukončiť_hovor;reťazec_údaje->인수개수=전달인수개수;
        memcpy(reťazec_údaje->Povolenia_Zoznam,Povolenia_Zoznam,sizeof(Povolenia_Zoznam));memcpy(reťazec_údaje->Súbor_Zoznam,Súbor_Zoznam,sizeof(Súbor_Zoznam));memcpy(reťazec_údaje->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(reťazec_údaje->argument_pole,전달인수,sizeof(전달인수));memcpy(reťazec_údaje->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<používateľ_strana_COUNT;순번++)if(Povolenia_Zoznam[순번])memcpy((unsigned char *)snímka(vlastník_objekt)+순번*veľkosť_stránky,(void *)(používateľ_BASE+순번*veľkosť_stránky),veľkosť_stránky);
    }else{
        저장값[vlastník_objekt].멈춤상태=0;화면초기화(vlastník_objekt);
        for(unsigned 순번=0;순번<16;순번++)if(Súbor_Zoznam[순번]>=0)pk_close(Súbor_Zoznam[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])Zavrieť_soket_účastník(순번+32);
    }
    for(unsigned 순번=0;순번<používateľ_strana_COUNT;순번++){strana_Zoznam[순번]=0;Povolenia_Zoznam[순번]=0;}변환표맞추기();return KR;
}
uintptr_t Panel_používateľský_ovládací_prvok(uintptr_t Akcia){
    unsigned pozičný_index=Akcia&15;if(pozičný_index>=4||Aktívny)return (uint32_t)-22;
    저장된작업 *reťazec_údaje=&저장값[pozičný_index];
    if(Akcia>=32){if(reťazec_údaje->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(reťazec_údaje->Súbor_Zoznam[순번]>=0)pk_close(reťazec_údaje->Súbor_Zoznam[순번]);for(unsigned 순번=0;순번<24;순번++)if(reťazec_údaje->통신끝점들[순번])Zavrieť_soket_účastník(순번+32);}reťazec_údaje->멈춤상태=0;화면초기화(pozičný_index);return 0;}
    if(Akcia>=16)return reťazec_údaje->멈춤상태;
    if(!reťazec_údaje->멈춤상태)return (uint32_t)-22;
    vlastník_objekt=pozičný_index;interaktívny=reťazec_údaje->interaktívny;리눅스규약=reťazec_údaje->리눅스규약;halda_ukončiť_hovor=reťazec_údaje->halda_Úložisko;전달인수개수=reťazec_údaje->인수개수;
    memcpy(Súbor_Zoznam,reťazec_údaje->Súbor_Zoznam,sizeof(Súbor_Zoznam));memcpy(통신끝점들,reťazec_údaje->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,reťazec_údaje->argument_pole,sizeof(전달인수));memcpy(전달인수길이,reťazec_údaje->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<používateľ_strana_COUNT;순번++)strana_Zoznam[순번]=(používateľ_BASE+순번*veľkosť_stránky)|jadro_strana;변환표맞추기();
    memset((void *)používateľ_BASE,0,používateľ_ukončiť_hovor-používateľ_BASE);
    for(unsigned 순번=0;순번<používateľ_strana_COUNT;순번++)if(reťazec_údaje->Povolenia_Zoznam[순번])memcpy((void *)(používateľ_BASE+순번*veľkosť_stránky),(unsigned char *)snímka(pozičný_index)+순번*veľkosť_stránky,veľkosť_stránky);
    memcpy(Povolenia_Zoznam,reťazec_údaje->Povolenia_Zoznam,sizeof(Povolenia_Zoznam));
    for(unsigned 순번=0;순번<používateľ_strana_COUNT;순번++){unsigned údaje_pozícia=Povolenia_Zoznam[순번];strana_Zoznam[순번]=údaje_pozícia?(používateľ_BASE+순번*veľkosť_stránky)|(údaje_pozícia==3?používateľ_na_čítanie_a_zapisovanie:údaje_pozícia==5?사용자읽고실행:používateľ_iba_na_čítanie):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");Aktívny=1;reťazec_údaje->멈춤상태=0;START_TIMEOUT();
    사용자실행시각[vlastník_objekt]=보드밀리초();
    return (uint32_t)Dokončiť_program(používateľ_životopis(&reťazec_údaje->실행틀,reťazec_údaje->plávajúci_bod_Stav));
}
static int spustiť_program(const unsigned char *údaje, size_t Veľkosť, unsigned 전달값, int 리눅스방식, const char *Názov) {
    if (Aktívny) return -16;
    vlastník_objekt=Panel_Terminál(11);if(vlastník_objekt<0||vlastník_objekt>3||저장값[vlastník_objekt].멈춤상태)return -16;interaktívny=0;
    int 유효함 = 실행파일검사(údaje, Veľkosť, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned názov_INDEX=0;
    while (*Názov && názov_INDEX<31) používateľ_príkaz_názov[vlastník_objekt][názov_INDEX++]=(unsigned char)*Názov++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (názov_INDEX) používateľ_príkaz_názov[vlastník_objekt][názov_INDEX++]=' ';
        for (unsigned pozičný_index=0; pozičný_index<전달인수길이[0]; pozičný_index++) používateľ_príkaz_názov[vlastník_objekt][názov_INDEX++]=전달인수[0][pozičný_index];
    }
    používateľ_príkaz_názov[vlastník_objekt][názov_INDEX]=0; číslo_používateľa[vlastník_objekt]=Ďalej_číslo_používateľa++;
    if (Ďalej_číslo_používateľa>0x7fffffffu) Ďalej_číslo_používateľa=10;
    používateľ_START_čas[vlastník_objekt]=보드밀리초(); 사용자누적시각[vlastník_objekt]=0;
    for (unsigned 순번 = 0; 순번 < používateľ_strana_COUNT; 순번++) strana_Zoznam[순번] = (používateľ_BASE + 순번 * veľkosť_stránky) | jadro_strana;
    변환표맞추기();
    memset((void *)používateľ_BASE, 0, používateľ_ukončiť_hovor - používateľ_BASE);
    memset(Povolenia_Zoznam, 0, sizeof(Povolenia_Zoznam));
    실행파일머리 spustiteľný_súbor_Nadpis; memcpy(&spustiteľný_súbor_Nadpis, údaje, sizeof(spustiteľný_súbor_Nadpis));
    for (unsigned 순번 = 0; 순번 < spustiteľný_súbor_Nadpis.program_Nadpis_COUNT; 순번++) {
        실행파일구획 údaje_pozícia; memcpy(&údaje_pozícia, údaje + spustiteľný_súbor_Nadpis.program_Nadpis_Posun + 순번 * sizeof(údaje_pozícia), sizeof(údaje_pozícia));
        if (údaje_pozícia.Typ_oblasť != 1 || !údaje_pozícia.기억영역크기) continue;
        if (údaje_pozícia.파일영역크기) memcpy((void *)(uintptr_t)údaje_pozícia.adresa, údaje + údaje_pozícia.Posun_VALUE, údaje_pozícia.파일영역크기);
        for (uintptr_t v_termíne_splatnosti_pozícia = údaje_pozícia.adresa & ~(veľkosť_stránky - 1); v_termíne_splatnosti_pozícia < údaje_pozícia.adresa + údaje_pozícia.기억영역크기; v_termíne_splatnosti_pozícia += veľkosť_stránky) {
            Povolenia_Zoznam[(v_termíne_splatnosti_pozícia - používateľ_BASE) / veľkosť_stránky] = (údaje_pozícia.konfigurácia_Background_Intelligent_Transfer_Service & 2) ? 3 : ((údaje_pozícia.konfigurácia_Background_Intelligent_Transfer_Service & 1) ? 5 : 1);
        }
    }
    for (uintptr_t v_termíne_splatnosti_pozícia = používateľ_Vrstvy_adresa; v_termíne_splatnosti_pozícia < používateľ_ukončiť_hovor; v_termíne_splatnosti_pozícia += veľkosť_stránky) Povolenia_Zoznam[(v_termíne_splatnosti_pozícia - používateľ_BASE) / veľkosť_stránky] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(spustiteľný_súbor_Nadpis.položka_bod) : používateľ_ukončiť_hovor;
    for (unsigned 순번 = 0; 순번 < používateľ_strana_COUNT; 순번++) {
        unsigned povolenia = Povolenia_Zoznam[순번];
        strana_Zoznam[순번] = povolenia ? (používateľ_BASE + 순번 * veľkosť_stránky) | (povolenia == 3 ? používateľ_na_čítanie_a_zapisovanie : povolenia == 5 ? 사용자읽고실행 : používateľ_iba_na_čítanie) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) Súbor_Zoznam[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    halda_ukončiť_hovor = používateľ_IMAGE_ukončiť_hovor;
    Aktívny = 1; START_TIMEOUT();
    사용자실행시각[vlastník_objekt]=보드밀리초();
    int KR = používateľ_zadať(spustiteľný_súbor_Nadpis.položka_bod, 초기쌓임공간, 전달값);
    return Dokončiť_program(KR);
}
uintptr_t Panel_používateľ_spustiť(uintptr_t LOOKUP_INDEX) {
    if (LOOKUP_INDEX >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Názov=LOOKUP_INDEX==10?"javac":LOOKUP_INDEX==11?"java":LOOKUP_INDEX==12?"python":LOOKUP_INDEX==13?"vi":LOOKUP_INDEX==14?"jar":LOOKUP_INDEX==15?"cc":LOOKUP_INDEX==16?"jaot":"ELF";
    return (uint32_t)spustiť_program(실행항목들[LOOKUP_INDEX].údaje, 실행항목들[LOOKUP_INDEX].Veľkosť, 실행항목들[LOOKUP_INDEX].전달값, 0, Názov);
}
static uintptr_t Vykonať_Súbor(int 리눅스방식) {
    static unsigned char IMAGE[16384];
    if (Aktívny || !전달인수개수) return (uint32_t)-22;
    int Súbor_rukoväť = pk_open((const char *)전달인수[0], iba_na_čítanie_VALUE, 0);
    if (Súbor_rukoväť < 0) return (uint32_t)-chybové_číslo;
    int Veľkosť = pk_size(Súbor_rukoväť);
    if (Veľkosť < 0 || (unsigned)Veľkosť > sizeof(IMAGE)) { pk_close(Súbor_rukoväť); return (uint32_t)-27; }
    int RECEIVED_COUNT = pk_read(Súbor_rukoväť, IMAGE, Veľkosť); pk_close(Súbor_rukoväť);
    if (RECEIVED_COUNT != Veľkosť) return (uint32_t)-5;
    return (uint32_t)spustiť_program(IMAGE, Veľkosť, 0, 리눅스방식, "");
}
uintptr_t Panel_používateľ_Súbor(void) { return Vykonať_Súbor(0); }
uintptr_t 보드사용자리눅스파일(void) { return Vykonať_Súbor(1); }
uintptr_t Panel_používateľ_overiť(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].údaje, 잘못된실행항목들[순번].Veľkosť) != používateľ_spustiteľný_súbor_Chyba) return 순번 + 1;
    return 0;
}
