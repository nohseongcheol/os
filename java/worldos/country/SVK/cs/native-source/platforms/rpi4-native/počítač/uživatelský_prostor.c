#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 Provést_příkaz počítač vrstva_HODNOTA. název_souboru data/정책은 기존 AOT Java 커널에 위임한다.
#include "uživatelský_prostor.h"
#include "Soubor_ABI.h"
#include "síť_ABI.h"
#include "../síť_Štos/síť_Štos.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define počítač_registr(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define přerušení_distributor 0xff841000ul
#define přerušení_CPU_rozhraní 0xff842000ul
#define velikost_stránky 4096ul
#define přístup_značka (1ul << 10)
#define ne_Provést_oprávnění (1ul << 53)
#define uživatel_ne_Provést (1ul << 54)
#define normální_Paměť ((1ul << 2) | (3ul << 8) | přístup_značka)
#define jádro_stránka (3ul | normální_Paměť | ne_Provést_oprávnění | uživatel_ne_Provést)
#define uživatel_pro_čtení_i_zápis (3ul | normální_Paměť | (1ul << 6) | ne_Provést_oprávnění | uživatel_ne_Provést)
#define uživatel_jen_pro_čtení (3ul | normální_Paměť | (3ul << 6) | ne_Provést_oprávnění | uživatel_ne_Provést)
#define 사용자읽고실행 (3ul | normální_Paměť | (3ul << 6) | ne_Provést_oprávnění)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t Panel_pixel(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t Panel_Terminál(uintptr_t);
extern int Terminál_probíhá(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int uživatel_pokračovat(uživatel_rámec *,void *);
extern void 사용자실수보관(void *);
extern int uživatel_zadat(uintptr_t vstupní_bod, uintptr_t paměť_zásobníku, uintptr_t 전달값);
extern void uživatel_Vratka(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t kořen_ODKAZ[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t stránka_Seznam[uživatel_stránka_POČET] __attribute__((aligned(4096)));
static uint8_t Oprávnění_Seznam[uživatel_stránka_POČET];
static int Aktivní, seznam_souborů[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int Zavřít_soket_účastník(unsigned popisovač_souboru){return popisovač_souboru<40?자바전문닫기(popisovač_souboru):자바흐름닫기(popisovač_souboru);}
static uint64_t ČETNOSTI, konečný_termín_ČAS;
static uintptr_t halda_konec;
// jádro_HODNOTA 셸이 준비한 UTF-8 argumenty. EL0에는 instance_HODNOTA 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int pozastavený_Stav,interaktivní,리눅스규약,seznam_souborů[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char argument_pole[8][256],Oprávnění_Seznam[uživatel_stránka_POČET];
    uintptr_t dynamická_paměť; uživatel_rámec spuštění_rámec;
    unsigned char číslo_s_plovoucí_desetinnou_čárkou_Stav[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int vlastník_objekt,interaktivní;
static uint32_t číslo_uživatele[4], uživatel_START_ČAS[4], 사용자누적시각[4], uživatel_spuštění_ČAS[4], Další_číslo_uživatele=10;
static unsigned char uživatel_příkaz_název[4][288];
uint32_t 사용자상태읽기(unsigned položka_HODNOTA, unsigned INDEX) {
    unsigned poziční_index=INDEX&3;
    int Stav_HODNOTA=(Aktivní && vlastník_objekt==(int)poziční_index) ? 1 : 저장값[poziční_index].pozastavený_Stav ? 2 : 0;
    if (položka_HODNOTA==0) return Stav_HODNOTA;
    if (!Stav_HODNOTA) return 0;
    if (položka_HODNOTA==1) return číslo_uživatele[poziční_index];
    if (položka_HODNOTA==2) {
        unsigned char *쪽들=Stav_HODNOTA==1?Oprávnění_Seznam:저장값[poziční_index].Oprávnění_Seznam;
        unsigned stránka_POČET=0; for (unsigned 순번=0; 순번<uživatel_stránka_POČET; 순번++) if(쪽들[순번]) stránka_POČET++;
        return stránka_POČET*4;
    }
    if (položka_HODNOTA==3) return (uint32_t)보드밀리초()-uživatel_START_ČAS[poziční_index];
    if (položka_HODNOTA==4) return 사용자누적시각[poziční_index]+(Stav_HODNOTA==1?(uint32_t)보드밀리초()-uživatel_spuštění_ČAS[poziční_index]:0);
    if (položka_HODNOTA==5) return INDEX/4<sizeof(uživatel_příkaz_název[0])?uživatel_příkaz_název[poziční_index][INDEX/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t položka_POČET) {
    if (Aktivní || položka_POČET > 8) return (uint32_t)-22;
    전달인수개수 = položka_POČET;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t VYHLEDAT_INDEX, uintptr_t dobrá_pozice, uintptr_t bajt_data) {
    if (Aktivní || VYHLEDAT_INDEX >= 전달인수개수 || dobrá_pozice >= 255 || dobrá_pozice != 전달인수길이[VYHLEDAT_INDEX] || !bajt_data || bajt_data > 255)
        return (uint32_t)-22;
    전달인수[VYHLEDAT_INDEX][dobrá_pozice] = bajt_data;
    전달인수길이[VYHLEDAT_INDEX] = dobrá_pozice + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Hodiny_HODNOTA(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Stop_TIMEOUT(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    počítač_registr(přerušení_distributor + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void START_TIMEOUT(void) {
    uint64_t 간격 = ČETNOSTI * 2, povolit = 1;
    konečný_termín_ČAS = Hodiny_HODNOTA() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(povolit) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned datový_blok = 0; datový_blok < 4; datový_blok++) {
        kořen_ODKAZ[datový_blok] = (uintptr_t)가운데[datový_blok] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t Adresa = ((uintptr_t)datový_blok << 30) | ((uintptr_t)순번 << 21);
            가운데[datový_blok][순번] = Adresa | 1 | přístup_značka | uživatel_ne_Provést;
            if (Adresa >= 0xfc000000ul) 가운데[datový_blok][순번] |= ne_Provést_oprávnění; // Device-nGnRnE
            else 가운데[datový_blok][순번] |= normální_Paměť; // Normal, non-cacheable
        }
    }
    for (unsigned SEKUNDA_HODNOTA = 0; SEKUNDA_HODNOTA < uživatel_stránka_POČET / 512; SEKUNDA_HODNOTA++)
        가운데[0][(uživatel_BASE >> 21) + SEKUNDA_HODNOTA] = (uintptr_t)(stránka_Seznam + SEKUNDA_HODNOTA * 512) | 3;
    for (unsigned 순번 = 0; 순번 < uživatel_stránka_POČET; 순번++) stránka_Seznam[순번] = (uživatel_BASE + 순번 * velikost_stránky) | jádro_stránka;
    uint64_t Paměť_atribut_registr = 0x4400, ODKAZ_převod_řízení = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Paměť_atribut_registr), "r"(ODKAZ_převod_řízení), "r"((uintptr_t)kořen_ODKAZ) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t číslo_s_plovoucí_desetinnou_čárkou_Stav = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(číslo_s_plovoucí_desetinnou_čárkou_Stav) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(ČETNOSTI));
    Stop_TIMEOUT();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 vstupní_bod_HODNOTA 때만 Povolit_HODNOTA.
    počítač_registr(přerušení_distributor) = 0;
    počítač_registr(přerušení_distributor + 0x180) = 0xffffffff;
    počítač_registr(přerušení_distributor + 0x80) = 0xffffffff;
    počítač_registr(přerušení_distributor + 0x280) = 1u << 30;
    počítač_registr(přerušení_distributor + 0x41c) = 0x80808080;
    počítač_registr(přerušení_distributor + 0x100) = 1u << 30;
    počítač_registr(přerušení_CPU_rozhraní + 4) = 0xff;
    počítač_registr(přerušení_CPU_rozhraní + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 informační_systémy_normální 확인할 číslo 있다.
    int Zabezpečení = (počítač_registr(přerušení_distributor + 4) & (1u << 10)) != 0;
    počítač_registr(přerušení_distributor) = Zabezpečení ? 1 : 3;
    počítač_registr(přerušení_CPU_rozhraní) = Zabezpečení ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t TYP_oblast, počítač_TYP; uint32_t číslo_verze;
    uint64_t vstupní_bod, program_Nadpis_POSUN, záhlaví_oddílu_POSUN; uint32_t konfigurace_BITS;
    uint16_t spustitelný_Nadpis_změnit_velikost, program_Nadpis_položka_změnit_velikost, program_Nadpis_POČET, záhlaví_oddílu_položka_změnit_velikost, záhlaví_oddílu_POČET, oddíl_název_tabulka_INDEX;
} 실행파일머리;
typedef struct { uint32_t TYP_oblast, konfigurace_BITS; uint64_t POSUN_HODNOTA, Adresa, 물리주소, 파일영역크기, 기억영역크기, zarovnat_mez; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(uživatel_rámec) == 272, "exception assembly layout");
static int 포함된범위(uint64_t POSUN_HODNOTA, uint64_t Velikost, uint64_t konec_POSUN) {
    return POSUN_HODNOTA <= konec_POSUN && Velikost <= konec_POSUN - POSUN_HODNOTA;
}
static int 부가정보검사(const unsigned char *data_pozice, size_t Velikost) {
    size_t dobrá_pozice = 0;
    while (포함된범위(dobrá_pozice, 12, Velikost)) {
        uint32_t 낱말들[3]; memcpy(낱말들, data_pozice + dobrá_pozice, 12); dobrá_pozice += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(dobrá_pozice, 이름영역크기, Velikost) || !포함된범위(dobrá_pozice + 이름영역크기, 설명크기, Velikost)) return 0;
        const unsigned char Název[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Název) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Název); 순번++) if (data_pozice[dobrá_pozice + 순번] != Název[순번]) 일치 = 0;
        uint32_t číslo_verze = 0;
        if (일치) memcpy(&číslo_verze, data_pozice + dobrá_pozice + 이름영역크기, 4);
        if (일치 && číslo_verze == 1) return 1;
        dobrá_pozice += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *data, size_t Velikost, int 리눅스방식) {
    if (Velikost < sizeof(실행파일머리)) return uživatel_spustitelný_chyba;
    실행파일머리 spustitelný_Nadpis; memcpy(&spustitelný_Nadpis, data, sizeof(spustitelný_Nadpis));
    if (spustitelný_Nadpis.형식식별[0] != 127 || spustitelný_Nadpis.형식식별[1] != 'E' || spustitelný_Nadpis.형식식별[2] != 'L' || spustitelný_Nadpis.형식식별[3] != 'F' ||
        spustitelný_Nadpis.형식식별[4] != 2 || spustitelný_Nadpis.형식식별[5] != 1 || spustitelný_Nadpis.형식식별[6] != 1 || (spustitelný_Nadpis.형식식별[7] != 0 && (!리눅스방식 || spustitelný_Nadpis.형식식별[7] != 3)) ||
        spustitelný_Nadpis.TYP_oblast != 2 || spustitelný_Nadpis.počítač_TYP != 183 || spustitelný_Nadpis.číslo_verze != 1 || spustitelný_Nadpis.konfigurace_BITS || spustitelný_Nadpis.spustitelný_Nadpis_změnit_velikost != sizeof(spustitelný_Nadpis) ||
        spustitelný_Nadpis.program_Nadpis_položka_změnit_velikost != sizeof(실행파일구획) || !spustitelný_Nadpis.program_Nadpis_POČET || spustitelný_Nadpis.program_Nadpis_POČET > 16 ||
        spustitelný_Nadpis.program_Nadpis_POSUN < sizeof(spustitelný_Nadpis) || !포함된범위(spustitelný_Nadpis.program_Nadpis_POSUN, (uint64_t)spustitelný_Nadpis.program_Nadpis_POČET * sizeof(실행파일구획), Velikost)) return uživatel_spustitelný_chyba;
    uint8_t 사용량[(uživatel_image_konec - uživatel_BASE) / velikost_stránky] = {0};
    int platný_vstupní_bod = 0, ABI_OK = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < spustitelný_Nadpis.program_Nadpis_POČET; 순번++) {
        실행파일구획 data_pozice; memcpy(&data_pozice, data + spustitelný_Nadpis.program_Nadpis_POSUN + 순번 * sizeof(data_pozice), sizeof(data_pozice));
        if (data_pozice.TYP_oblast == 4) {
            if (!포함된범위(data_pozice.POSUN_HODNOTA, data_pozice.파일영역크기, Velikost)) return uživatel_spustitelný_chyba;
            if (부가정보검사(data + data_pozice.POSUN_HODNOTA, data_pozice.파일영역크기)) ABI_OK = 1;
            continue;
        }
        if (data_pozice.TYP_oblast == 0 || data_pozice.TYP_oblast == 6 || (data_pozice.TYP_oblast == 0x6474e551 && !(data_pozice.konfigurace_BITS & 1))) continue;
        if (data_pozice.TYP_oblast != 1) return uživatel_spustitelný_chyba; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!data_pozice.기억영역크기) continue;
        if (data_pozice.konfigurace_BITS & ~7u || !(data_pozice.konfigurace_BITS & 4) || (data_pozice.konfigurace_BITS & 3) == 3 || data_pozice.파일영역크기 > data_pozice.기억영역크기 ||
            (data_pozice.파일영역크기 && !포함된범위(data_pozice.POSUN_HODNOTA, data_pozice.파일영역크기, Velikost)) || data_pozice.Adresa < uživatel_BASE ||
            !포함된범위(data_pozice.Adresa, data_pozice.기억영역크기, uživatel_image_konec) ||
            (!리눅스방식 && ((data_pozice.Adresa & (velikost_stránky - 1)) || (data_pozice.POSUN_HODNOTA & (velikost_stránky - 1)) || data_pozice.zarovnat_mez != velikost_stránky)) ||
            (리눅스방식 && (((data_pozice.Adresa ^ data_pozice.POSUN_HODNOTA) & (velikost_stránky - 1)) || !data_pozice.zarovnat_mez ||
                (data_pozice.zarovnat_mez & (data_pozice.zarovnat_mez - 1)) || data_pozice.zarovnat_mez > 0x200000 || ((data_pozice.Adresa ^ data_pozice.POSUN_HODNOTA) & (data_pozice.zarovnat_mez - 1))))) return uživatel_spustitelný_chyba;
        unsigned 첫항목 = (data_pozice.Adresa - uživatel_BASE) / velikost_stránky;
        unsigned položka_POČET = ((data_pozice.Adresa & (velikost_stránky - 1)) + data_pozice.기억영역크기 + velikost_stránky - 1) / velikost_stránky;
        for (unsigned stránka_HODNOTA = 첫항목; stránka_HODNOTA < 첫항목 + položka_POČET; stránka_HODNOTA++) {
            if (사용량[stránka_HODNOTA]) return uživatel_spustitelný_chyba;
            사용량[stránka_HODNOTA] = 1;
        }
        if ((data_pozice.konfigurace_BITS & 1) && spustitelný_Nadpis.vstupní_bod >= data_pozice.Adresa && spustitelný_Nadpis.vstupní_bod < data_pozice.Adresa + data_pozice.파일영역크기 && !(spustitelný_Nadpis.vstupní_bod & 3)) platný_vstupní_bod = 1;
        적재구획++;
    }
    return platný_vstupní_bod && (리눅스방식 ? !ABI_OK : ABI_OK) && 적재구획 ? 0 : uživatel_spustitelný_chyba;
}
int 사용자실행파일검사(const unsigned char *data, size_t Velikost) { return 실행파일검사(data, Velikost, 0); }
static void rozložení_stránky(uintptr_t Adresa, uint64_t konfigurace_BITS, unsigned oprávnění) {
    unsigned VYHLEDAT_INDEX = (Adresa - uživatel_BASE) / velikost_stránky;
    stránka_Seznam[VYHLEDAT_INDEX] = Adresa | konfigurace_BITS;
    Oprávnění_Seznam[VYHLEDAT_INDEX] = oprávnění;
}
static int uživatel_oblast(uintptr_t Adresa, size_t položka_POČET, int 쓰는중) {
    if (Adresa < uživatel_BASE || !포함된범위(Adresa, položka_POČET, uživatel_konec)) return 0;
    if (!položka_POČET) return 1;
    unsigned 첫항목 = (Adresa - uživatel_BASE) / velikost_stránky, 마지막 = (Adresa + položka_POČET - 1 - uživatel_BASE) / velikost_stránky;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(Oprávnění_Seznam[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int instance_cesta(uintptr_t Adresa, char *cesta_2) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!uživatel_oblast(Adresa, 1, 0)) return -14;
        cesta_2[순번] = *(const char *)Adresa++;
        if (!cesta_2[순번]) return 0;
    }
    return -36;
}
static intptr_t jádro_KV(intptr_t VÝSLEDEK) { return VÝSLEDEK < 0 ? -číslo_chyby : VÝSLEDEK; }
static int 대응파일기술자(uint64_t popisovač_souboru) { return popisovač_souboru >= 3 && popisovač_souboru < 19 ? seznam_souborů[popisovač_souboru - 3] : -1; }
static int soket_účastník_vlastník(uint64_t popisovač_souboru) { return popisovač_souboru >= 32 && popisovač_souboru < 56 && 통신끝점들[popisovač_souboru - 32]; }
static int ODKAZ_vstup(uintptr_t 가리킴값, size_t délka_HODNOTA, struct pk_sockaddr_in *Adresa) {
    if (délka_HODNOTA != sizeof(*Adresa)) return -22;
    if (!uživatel_oblast(가리킴값, délka_HODNOTA, 0)) return -14;
    memcpy(Adresa, (const void *)가리킴값, sizeof(*Adresa));
    return Adresa->sin_family == AF_INET ? 0 : -97;
}
static int ODKAZ_výstup_šek(uintptr_t 가리킴값, uintptr_t délka_ukazatel, pk_socklen_t *zásobník_kapacita) {
    if (!uživatel_oblast(délka_ukazatel, sizeof(*zásobník_kapacita), 1)) return -14;
    memcpy(zásobník_kapacita, (const void *)délka_ukazatel, sizeof(*zásobník_kapacita));
    if (*zásobník_kapacita > sizeof(struct pk_sockaddr_in)) *zásobník_kapacita = sizeof(struct pk_sockaddr_in);
    if (*zásobník_kapacita && !uživatel_oblast(가리킴값, *zásobník_kapacita, 1)) return -14;
    return 0;
}
static void ODKAZ_výstup(uintptr_t 가리킴값, uintptr_t délka_ukazatel, pk_socklen_t zásobník_kapacita, int Adresa, int číslo_portu) {
    struct pk_sockaddr_in HODNOTA; memset(&HODNOTA, 0, sizeof(HODNOTA));
    HODNOTA.sin_family = AF_INET; HODNOTA.sin_port = pk_htons(číslo_portu); HODNOTA.sin_addr.s_addr = pk_htonl(Adresa);
    if (zásobník_kapacita) memcpy((void *)가리킴값, &HODNOTA, zásobník_kapacita);
    pk_socklen_t délka_HODNOTA = sizeof(HODNOTA); memcpy((void *)délka_ukazatel, &délka_HODNOTA, sizeof(délka_HODNOTA));
}
extern uintptr_t Panel_Kanál(uintptr_t, uintptr_t);
static intptr_t nativní_Systém_VOLAT(uživatel_rámec *Soubor_položka) {
    uintptr_t 첫째값 = Soubor_položka->registr_data[0], SEKUNDA_HODNOTA = Soubor_položka->registr_data[1], bod_kódu = Soubor_položka->registr_data[2];
    char cesta_2[65];
    int popisovač_souboru, VÝSLEDEK;
    switch (Soubor_položka->registr_data[8]) {
    case 0: return 1; // vlastní ABI 버전
    case 1: // write: ukazatel 전체를 검사한 BACK_HODNOTA výstupní_pozice/název_souboru změnit_HODNOTA
        if (bod_kódu > 65536) return -22;
        if (!uživatel_oblast(SEKUNDA_HODNOTA, bod_kódu, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t START_výstup=Hodiny_HODNOTA();
            for (size_t 순번 = 0; 순번 < bod_kódu; 순번++) Panel_Kanál(첫째값, ((const unsigned char *)SEKUNDA_HODNOTA)[순번]);
            /* 큰 tty를 그린 jádro_HODNOTA 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(interaktivní){
                konečný_termín_ČAS+=Hodiny_HODNOTA()-START_výstup;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(konečný_termín_ČAS) : "memory");
            }
            return bod_kódu;
        }
        if(첫째값>=40&&soket_účastník_vlastník(첫째값)){
            size_t zboží_POČET=bod_kódu>512?512:bod_kódu;for(size_t 순번=0;순번<zboží_POČET;순번++)자바전문넣기(순번,((const unsigned char *)SEKUNDA_HODNOTA)[순번]);return 자바흐름쓰기(첫째값,zboží_POČET);
        }
        popisovač_souboru = 대응파일기술자(첫째값); if (popisovač_souboru < 0) return -9;
        return jádro_KV(pk_write(popisovač_souboru, (const void *)SEKUNDA_HODNOTA, bod_kódu));
    case 2:
        if (bod_kódu > 65536) return -22;
        if (!uživatel_oblast(SEKUNDA_HODNOTA, bod_kódu, 1)) return -14;
        if (첫째값 == 0) {
            size_t zboží_POČET = 0;
            while (zboží_POČET < bod_kódu) {
                int znak_HODNOTA = (int32_t)보드글자읽기(); if (znak_HODNOTA == -2) return zboží_POČET; if (znak_HODNOTA < 0) break;
                ((unsigned char *)SEKUNDA_HODNOTA)[zboží_POČET++] = znak_HODNOTA;
            }
            return zboží_POČET ? (intptr_t)zboží_POČET : (bod_kódu ? -11 : 0);
        }
        if(첫째값>=40&&soket_účastník_vlastník(첫째값)){
            VÝSLEDEK=자바흐름읽기(첫째값,bod_kódu>512?512:bod_kódu);if(VÝSLEDEK>0)for(int 순번=0;순번<VÝSLEDEK;순번++)((unsigned char *)SEKUNDA_HODNOTA)[순번]=자바전문얻기(순번);return VÝSLEDEK;
        }
        popisovač_souboru = 대응파일기술자(첫째값); if (popisovač_souboru < 0) return -9;
        return jádro_KV(pk_read(popisovač_souboru, (void *)SEKUNDA_HODNOTA, bod_kódu));
    case 3:
        VÝSLEDEK = instance_cesta(첫째값, cesta_2); if (VÝSLEDEK) return VÝSLEDEK;
        if (SEKUNDA_HODNOTA > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (seznam_souborů[순번] < 0) {
            popisovač_souboru = pk_open(cesta_2, (int)SEKUNDA_HODNOTA, 0600);
            if (popisovač_souboru < 0) return -číslo_chyby;
            seznam_souborů[순번] = popisovač_souboru; return 순번 + 3;
        }
        return -24;
    case 4:
        if (soket_účastník_vlastník(첫째값)) { VÝSLEDEK = Zavřít_soket_účastník(첫째값); if (!VÝSLEDEK) 통신끝점들[첫째값 - 32] = 0; return VÝSLEDEK; }
        popisovač_souboru = 대응파일기술자(첫째값); if (popisovač_souboru < 0) return -9;
        VÝSLEDEK = pk_close(popisovač_souboru); if (!VÝSLEDEK) seznam_souborů[첫째값 - 3] = -1;
        return jádro_KV(VÝSLEDEK);
    case 5:
        popisovač_souboru = 대응파일기술자(첫째값); if (popisovač_souboru < 0) return -9;
        if (bod_kódu > 2) return -22;
        return jádro_KV(pk_lseek(popisovač_souboru, (int64_t)SEKUNDA_HODNOTA, bod_kódu));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 uživatelský_prostor RW/NX halda_HODNOTA, 새로 노출되는 페이지는 0으로 inicializovat
        if (!첫째값) return halda_konec;
        if (첫째값 < uživatel_image_konec || 첫째값 > uživatel_halda_konec) return -12;
        uintptr_t 이전쪽들 = (halda_konec + velikost_stránky - 1) & ~(velikost_stránky - 1);
        uintptr_t 새쪽들 = (첫째값 + velikost_stránky - 1) & ~(velikost_stránky - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t data_pozice = 이전쪽들; data_pozice < 새쪽들; data_pozice += velikost_stránky) rozložení_stránky(data_pozice, jádro_stránka, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t data_pozice = 이전쪽들; data_pozice < 새쪽들; data_pozice += velikost_stránky) rozložení_stránky(data_pozice, uživatel_pro_čtení_i_zápis, 3);
        } else {
            for (uintptr_t data_pozice = 새쪽들; data_pozice < 이전쪽들; data_pozice += velikost_stránky) {
                stránka_Seznam[(data_pozice - uživatel_BASE) / velikost_stránky] = 0; Oprávnění_Seznam[(data_pozice - uživatel_BASE) / velikost_stránky] = 0;
            }
        }
        halda_konec = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        popisovač_souboru = 대응파일기술자(첫째값); return popisovač_souboru < 0 ? -9 : jádro_KV(pk_size(popisovač_souboru));
    case 10:
        popisovač_souboru = 대응파일기술자(첫째값); return popisovač_souboru < 0 ? -9 : jádro_KV(pk_ftruncate(popisovač_souboru, (int64_t)SEKUNDA_HODNOTA));
    case 11:
        VÝSLEDEK = instance_cesta(첫째값, cesta_2); return VÝSLEDEK ? VÝSLEDEK : jádro_KV(pk_unlink(cesta_2));
    case 12:
        popisovač_souboru = 대응파일기술자(첫째값); return popisovač_souboru < 0 ? -9 : jádro_KV(pk_fsync(popisovač_souboru));
    case 13: { // 그래픽 기초 API: uživatelský_prostor 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = Soubor_položka->registr_data[3], vyžádáno_výška_HODNOTA = Soubor_položka->registr_data[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SEKUNDA_HODNOTA > 화면길이 || 너비값 > 화면폭 - 첫째값 || vyžádáno_výška_HODNOTA > 화면길이 - SEKUNDA_HODNOTA) return -22;
        for (uintptr_t Y_souřadnice = SEKUNDA_HODNOTA; Y_souřadnice < SEKUNDA_HODNOTA + vyžádáno_výška_HODNOTA; Y_souřadnice++) for (uintptr_t souřadnice_x = 첫째값; souřadnice_x < 첫째값 + 너비값; souřadnice_x++) Panel_pixel(souřadnice_x, Y_souřadnice, bod_kódu);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=zboží_POČET; args(index,buffer,capacity)=UTF-8 délka_HODNOTA
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (bod_kódu <= 전달인수길이[첫째값]) return -36;
        if (!uživatel_oblast(SEKUNDA_HODNOTA, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SEKUNDA_HODNOTA, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;interaktivní=1;return Panel_Terminál(13);}
        if(첫째값==2){interaktivní=0;return 0;}
        if(첫째값==3)return Panel_Terminál(13);
        if(첫째값!=1||!interaktivní)return -22;
        VÝSLEDEK=(int32_t)보드글자읽기();
        if(VÝSLEDEK==-4096)return VÝSLEDEK;
        START_TIMEOUT();return VÝSLEDEK<0?-11:VÝSLEDEK;
    case 17: { // 유한한 협력 počkej_HODNOTA: komunikace 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t konec_ČAS = Hodiny_HODNOTA() + ČETNOSTI * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Hodiny_HODNOTA() < konec_ČAS);
        START_TIMEOUT(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 nadřazený_HODNOTA·빈 폴더를 검사한다.
        if (SEKUNDA_HODNOTA > 2) return -22;
        VÝSLEDEK = instance_cesta(첫째값, cesta_2); if (VÝSLEDEK) return VÝSLEDEK;
        unsigned délka_HODNOTA = 0; while (cesta_2[délka_HODNOTA]) délka_HODNOTA++;
        VÝSLEDEK = 자바경로시작(délka_HODNOTA); if (VÝSLEDEK < 0) return VÝSLEDEK;
        for (unsigned 순번 = 0; 순번 < délka_HODNOTA; 순번++) 자바경로바이트(순번, (unsigned char)cesta_2[순번]);
        return SEKUNDA_HODNOTA == 0 ? 자바항목종류() : SEKUNDA_HODNOTA == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int znak_HODNOTA=(int32_t)보드글자읽기();if(znak_HODNOTA==-4096)return znak_HODNOTA;if(znak_HODNOTA>=0)화면누름(vlastník_objekt,znak_HODNOTA);START_TIMEOUT();}
        if(첫째값==3&&bod_kódu){if(!자바셸대화형())return -95;interaktivní=1;Panel_Terminál(300);}
        return 화면호출(vlastník_objekt,첫째값,SEKUNDA_HODNOTA,bod_kódu,Soubor_položka->registr_data[3],Soubor_položka->registr_data[4],Soubor_položka->registr_data[5]);
    case 21:
        if(bod_kódu>127)return -22;if(!uživatel_oblast(SEKUNDA_HODNOTA,bod_kódu*sizeof(uint32_t),0))return -14;
        return 화면글(vlastník_objekt,첫째값,(const uint32_t *)SEKUNDA_HODNOTA,bod_kódu);
    case 22: // 화면 Velikost dotaz_HODNOTA: 0=너비, 1=výška_HODNOTA. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SEKUNDA_HODNOTA==SOCK_STREAM&&(bod_kódu==0||bod_kódu==6))VÝSLEDEK=자바흐름만들기();
        else if(SEKUNDA_HODNOTA==SOCK_DGRAM&&(bod_kódu==0||bod_kódu==IPPROTO_UDP))VÝSLEDEK=자바전문만들기(첫째값,SEKUNDA_HODNOTA,bod_kódu);
        else return -93;
        if (VÝSLEDEK >= 32 && VÝSLEDEK < 56) 통신끝점들[VÝSLEDEK - 32] = 1;
        return VÝSLEDEK;
    case 33: {
        if (!soket_účastník_vlastník(첫째값)) return -9;
        struct pk_sockaddr_in Adresa;
        VÝSLEDEK = ODKAZ_vstup(SEKUNDA_HODNOTA, bod_kódu, &Adresa); if (VÝSLEDEK) return VÝSLEDEK;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(Adresa.sin_addr.s_addr),pk_htons(Adresa.sin_port)):자바전문묶기(첫째값, pk_htonl(Adresa.sin_addr.s_addr), pk_htons(Adresa.sin_port));
    }
    case 34: {
        if (!soket_účastník_vlastník(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Soubor_položka->registr_data[3]) return -95;
        if (bod_kódu > 512) return -90;
        if (bod_kódu && !uživatel_oblast(SEKUNDA_HODNOTA, bod_kódu, 0)) return -14;
        struct pk_sockaddr_in Adresa;
        VÝSLEDEK = ODKAZ_vstup(Soubor_položka->registr_data[4], Soubor_položka->registr_data[5], &Adresa); if (VÝSLEDEK) return VÝSLEDEK;
        for (unsigned 순번 = 0; 순번 < bod_kódu; 순번++) 자바전문넣기(순번, ((const unsigned char *)SEKUNDA_HODNOTA)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(Adresa.sin_addr.s_addr), pk_htons(Adresa.sin_port), bod_kódu);
    }
    case 35: {
        if (!soket_účastník_vlastník(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Soubor_položka->registr_data[3]) return -95;
        if (bod_kódu > 512) return -90;
        if (bod_kódu && !uživatel_oblast(SEKUNDA_HODNOTA, bod_kódu, 1)) return -14;
        pk_socklen_t zásobník_kapacita = 0;
        if (Soubor_položka->registr_data[4]) { VÝSLEDEK = ODKAZ_výstup_šek(Soubor_položka->registr_data[4], Soubor_položka->registr_data[5], &zásobník_kapacita); if (VÝSLEDEK) return VÝSLEDEK; }
        VÝSLEDEK = 자바전문받기(첫째값, bod_kódu); if (VÝSLEDEK < 0) return VÝSLEDEK;
        for (int 순번 = 0; 순번 < VÝSLEDEK; 순번++) ((unsigned char *)SEKUNDA_HODNOTA)[순번] = 자바전문얻기(순번);
        if (Soubor_položka->registr_data[4]) ODKAZ_výstup(Soubor_položka->registr_data[4], Soubor_položka->registr_data[5], zásobník_kapacita, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return VÝSLEDEK;
    }
    case 36: {
        if (!soket_účastník_vlastník(첫째값)) return -9;
        pk_socklen_t zásobník_kapacita;
        VÝSLEDEK = ODKAZ_výstup_šek(SEKUNDA_HODNOTA, bod_kódu, &zásobník_kapacita); if (VÝSLEDEK) return VÝSLEDEK;
        ODKAZ_výstup(SEKUNDA_HODNOTA,bod_kódu,zásobník_kapacita,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!soket_účastník_vlastník(첫째값))return -9;struct pk_sockaddr_in Adresa;
        VÝSLEDEK=ODKAZ_vstup(SEKUNDA_HODNOTA,bod_kódu,&Adresa);if(VÝSLEDEK)return VÝSLEDEK;
        return 자바흐름연결(첫째값,pk_htonl(Adresa.sin_addr.s_addr),pk_htons(Adresa.sin_port));
    }
    case 38: return 첫째값>=40&&soket_účastník_vlastník(첫째값)?자바흐름듣기(첫째값,SEKUNDA_HODNOTA):-9;
    case 39:
        if(첫째값<40||!soket_účastník_vlastník(첫째값))return -9;
        if(SEKUNDA_HODNOTA||bod_kódu)return -95;VÝSLEDEK=자바흐름연결받기(첫째값);if(VÝSLEDEK>=40&&VÝSLEDEK<56)통신끝점들[VÝSLEDEK-32]=1;return VÝSLEDEK;
    case 40: return 첫째값>=40&&soket_účastník_vlastník(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t systémové_volání(uživatel_rámec *Soubor_položka) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(Soubor_položka) : nativní_Systém_VOLAT(Soubor_položka);
}
static void Vratka_jádro(uživatel_rámec *Soubor_položka, int VÝSLEDEK) {
    Stop_TIMEOUT();
    Soubor_položka->registr_data[0] = (uint64_t)(int64_t)VÝSLEDEK;
    Soubor_položka->příkaz_pozice = (uintptr_t)uživatel_Vratka;
    Soubor_položka->Stav_KÓD = 0x3c5; // EL1h, DAIF masked
}
int výjimka_uživatelského_režimu(uživatel_rámec *Soubor_položka, unsigned průsečík) {
    if (!Aktivní || (Soubor_položka->Stav_KÓD & 15) != 0) return 0;
    if (průsečík) {
        uint32_t uznání_HODNOTA = počítač_registr(přerušení_CPU_rozhraní + 0xc), identifikátor_HODNOTA = uznání_HODNOTA & 1023;
        if (identifikátor_HODNOTA == 30) { Vratka_jádro(Soubor_položka, uživatel_TIMEOUT); počítač_registr(přerušení_CPU_rozhraní + 0x10) = uznání_HODNOTA; return 1; }
        if (identifikátor_HODNOTA < 1020) počítač_registr(přerušení_CPU_rozhraní + 0x10) = uznání_HODNOTA;
        return 1;
    }
    uint64_t výjimka_Stav; __asm__ volatile("mrs %0, esr_el1" : "=r"(výjimka_Stav));
    if (Hodiny_HODNOTA() >= konečný_termín_ČAS) { Vratka_jádro(Soubor_položka, uživatel_TIMEOUT); return 1; }
    unsigned výjimka_oblast = výjimka_Stav >> 26;
    if (výjimka_oblast == 0x15 && (výjimka_Stav & 0xffff) == 0) {
        if (리눅스규약 ? Soubor_položka->registr_data[8] == 93 || Soubor_položka->registr_data[8] == 94 : Soubor_položka->registr_data[8] == 6) Vratka_jádro(Soubor_položka, (int)(Soubor_položka->registr_data[0] & 255));
        else {
            intptr_t VÝSLEDEK=systémové_volání(Soubor_položka);
            if(VÝSLEDEK==-4096&&interaktivní){
                저장값[vlastník_objekt].spuštění_rámec=*Soubor_položka;저장값[vlastník_objekt].spuštění_rámec.příkaz_pozice-=4;
                사용자실수보관(저장값[vlastník_objekt].číslo_s_plovoucí_desetinnou_čárkou_Stav);Vratka_jádro(Soubor_položka,사용자중단됨);
            }else Soubor_položka->registr_data[0]=(uint64_t)VÝSLEDEK;
        }
    } else Vratka_jádro(Soubor_položka, výjimka_oblast == 0x24 ? uživatel_data_chyba : výjimka_oblast == 0x20 ? uživatel_spuštění_chyba : 사용자잘못된명령);
    return 1;
}

// 생성된 const ELF Skupina_HODNOTA: 실행은 반드시 program_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *data; size_t Velikost; unsigned 전달값; } program;
#include "programs.h"
static void *snímek(unsigned poziční_index){return (void *)(0x04000000ul+poziční_index*(uživatel_konec-uživatel_BASE));}
static int Dokončit_program(int VÝSLEDEK){
    사용자누적시각[vlastník_objekt]+=(uint32_t)보드밀리초()-uživatel_spuštění_ČAS[vlastník_objekt];
    Stop_TIMEOUT();Aktivní=0;
    if(VÝSLEDEK==사용자중단됨){
        저장된작업 *řetězec_data=&저장값[vlastník_objekt];řetězec_data->pozastavený_Stav=1;řetězec_data->interaktivní=interaktivní;řetězec_data->리눅스규약=리눅스규약;řetězec_data->dynamická_paměť=halda_konec;řetězec_data->인수개수=전달인수개수;
        memcpy(řetězec_data->Oprávnění_Seznam,Oprávnění_Seznam,sizeof(Oprávnění_Seznam));memcpy(řetězec_data->seznam_souborů,seznam_souborů,sizeof(seznam_souborů));memcpy(řetězec_data->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(řetězec_data->argument_pole,전달인수,sizeof(전달인수));memcpy(řetězec_data->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<uživatel_stránka_POČET;순번++)if(Oprávnění_Seznam[순번])memcpy((unsigned char *)snímek(vlastník_objekt)+순번*velikost_stránky,(void *)(uživatel_BASE+순번*velikost_stránky),velikost_stránky);
    }else{
        저장값[vlastník_objekt].pozastavený_Stav=0;화면초기화(vlastník_objekt);
        for(unsigned 순번=0;순번<16;순번++)if(seznam_souborů[순번]>=0)pk_close(seznam_souborů[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])Zavřít_soket_účastník(순번+32);
    }
    for(unsigned 순번=0;순번<uživatel_stránka_POČET;순번++){stránka_Seznam[순번]=0;Oprávnění_Seznam[순번]=0;}변환표맞추기();return VÝSLEDEK;
}
uintptr_t Panel_uživatelský_ovládací_prvek(uintptr_t Akce){
    unsigned poziční_index=Akce&15;if(poziční_index>=4||Aktivní)return (uint32_t)-22;
    저장된작업 *řetězec_data=&저장값[poziční_index];
    if(Akce>=32){if(řetězec_data->pozastavený_Stav){for(unsigned 순번=0;순번<16;순번++)if(řetězec_data->seznam_souborů[순번]>=0)pk_close(řetězec_data->seznam_souborů[순번]);for(unsigned 순번=0;순번<24;순번++)if(řetězec_data->통신끝점들[순번])Zavřít_soket_účastník(순번+32);}řetězec_data->pozastavený_Stav=0;화면초기화(poziční_index);return 0;}
    if(Akce>=16)return řetězec_data->pozastavený_Stav;
    if(!řetězec_data->pozastavený_Stav)return (uint32_t)-22;
    vlastník_objekt=poziční_index;interaktivní=řetězec_data->interaktivní;리눅스규약=řetězec_data->리눅스규약;halda_konec=řetězec_data->dynamická_paměť;전달인수개수=řetězec_data->인수개수;
    memcpy(seznam_souborů,řetězec_data->seznam_souborů,sizeof(seznam_souborů));memcpy(통신끝점들,řetězec_data->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,řetězec_data->argument_pole,sizeof(전달인수));memcpy(전달인수길이,řetězec_data->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<uživatel_stránka_POČET;순번++)stránka_Seznam[순번]=(uživatel_BASE+순번*velikost_stránky)|jádro_stránka;변환표맞추기();
    memset((void *)uživatel_BASE,0,uživatel_konec-uživatel_BASE);
    for(unsigned 순번=0;순번<uživatel_stránka_POČET;순번++)if(řetězec_data->Oprávnění_Seznam[순번])memcpy((void *)(uživatel_BASE+순번*velikost_stránky),(unsigned char *)snímek(poziční_index)+순번*velikost_stránky,velikost_stránky);
    memcpy(Oprávnění_Seznam,řetězec_data->Oprávnění_Seznam,sizeof(Oprávnění_Seznam));
    for(unsigned 순번=0;순번<uživatel_stránka_POČET;순번++){unsigned data_pozice=Oprávnění_Seznam[순번];stránka_Seznam[순번]=data_pozice?(uživatel_BASE+순번*velikost_stránky)|(data_pozice==3?uživatel_pro_čtení_i_zápis:data_pozice==5?사용자읽고실행:uživatel_jen_pro_čtení):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");Aktivní=1;řetězec_data->pozastavený_Stav=0;START_TIMEOUT();
    uživatel_spuštění_ČAS[vlastník_objekt]=보드밀리초();
    return (uint32_t)Dokončit_program(uživatel_pokračovat(&řetězec_data->spuštění_rámec,řetězec_data->číslo_s_plovoucí_desetinnou_čárkou_Stav));
}
static int spustit_program(const unsigned char *data, size_t Velikost, unsigned 전달값, int 리눅스방식, const char *Název) {
    if (Aktivní) return -16;
    vlastník_objekt=Panel_Terminál(11);if(vlastník_objekt<0||vlastník_objekt>3||저장값[vlastník_objekt].pozastavený_Stav)return -16;interaktivní=0;
    int platný = 실행파일검사(data, Velikost, 리눅스방식); if (platný) return platný;
    리눅스규약 = 리눅스방식;
    unsigned název_INDEX=0;
    while (*Název && název_INDEX<31) uživatel_příkaz_název[vlastník_objekt][název_INDEX++]=(unsigned char)*Název++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (název_INDEX) uživatel_příkaz_název[vlastník_objekt][název_INDEX++]=' ';
        for (unsigned poziční_index=0; poziční_index<전달인수길이[0]; poziční_index++) uživatel_příkaz_název[vlastník_objekt][název_INDEX++]=전달인수[0][poziční_index];
    }
    uživatel_příkaz_název[vlastník_objekt][název_INDEX]=0; číslo_uživatele[vlastník_objekt]=Další_číslo_uživatele++;
    if (Další_číslo_uživatele>0x7fffffffu) Další_číslo_uživatele=10;
    uživatel_START_ČAS[vlastník_objekt]=보드밀리초(); 사용자누적시각[vlastník_objekt]=0;
    for (unsigned 순번 = 0; 순번 < uživatel_stránka_POČET; 순번++) stránka_Seznam[순번] = (uživatel_BASE + 순번 * velikost_stránky) | jádro_stránka;
    변환표맞추기();
    memset((void *)uživatel_BASE, 0, uživatel_konec - uživatel_BASE);
    memset(Oprávnění_Seznam, 0, sizeof(Oprávnění_Seznam));
    실행파일머리 spustitelný_Nadpis; memcpy(&spustitelný_Nadpis, data, sizeof(spustitelný_Nadpis));
    for (unsigned 순번 = 0; 순번 < spustitelný_Nadpis.program_Nadpis_POČET; 순번++) {
        실행파일구획 data_pozice; memcpy(&data_pozice, data + spustitelný_Nadpis.program_Nadpis_POSUN + 순번 * sizeof(data_pozice), sizeof(data_pozice));
        if (data_pozice.TYP_oblast != 1 || !data_pozice.기억영역크기) continue;
        if (data_pozice.파일영역크기) memcpy((void *)(uintptr_t)data_pozice.Adresa, data + data_pozice.POSUN_HODNOTA, data_pozice.파일영역크기);
        for (uintptr_t dobrá_pozice = data_pozice.Adresa & ~(velikost_stránky - 1); dobrá_pozice < data_pozice.Adresa + data_pozice.기억영역크기; dobrá_pozice += velikost_stránky) {
            Oprávnění_Seznam[(dobrá_pozice - uživatel_BASE) / velikost_stránky] = (data_pozice.konfigurace_BITS & 2) ? 3 : ((data_pozice.konfigurace_BITS & 1) ? 5 : 1);
        }
    }
    for (uintptr_t dobrá_pozice = uživatel_Štos_ODKAZ; dobrá_pozice < uživatel_konec; dobrá_pozice += velikost_stránky) Oprávnění_Seznam[(dobrá_pozice - uživatel_BASE) / velikost_stránky] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(spustitelný_Nadpis.vstupní_bod) : uživatel_konec;
    for (unsigned 순번 = 0; 순번 < uživatel_stránka_POČET; 순번++) {
        unsigned oprávnění = Oprávnění_Seznam[순번];
        stránka_Seznam[순번] = oprávnění ? (uživatel_BASE + 순번 * velikost_stránky) | (oprávnění == 3 ? uživatel_pro_čtení_i_zápis : oprávnění == 5 ? 사용자읽고실행 : uživatel_jen_pro_čtení) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) seznam_souborů[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    halda_konec = uživatel_image_konec;
    Aktivní = 1; START_TIMEOUT();
    uživatel_spuštění_ČAS[vlastník_objekt]=보드밀리초();
    int VÝSLEDEK = uživatel_zadat(spustitelný_Nadpis.vstupní_bod, 초기쌓임공간, 전달값);
    return Dokončit_program(VÝSLEDEK);
}
uintptr_t Panel_uživatel_spustit(uintptr_t VYHLEDAT_INDEX) {
    if (VYHLEDAT_INDEX >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Název=VYHLEDAT_INDEX==10?"javac":VYHLEDAT_INDEX==11?"java":VYHLEDAT_INDEX==12?"python":VYHLEDAT_INDEX==13?"vi":VYHLEDAT_INDEX==14?"jar":VYHLEDAT_INDEX==15?"cc":VYHLEDAT_INDEX==16?"jaot":"ELF";
    return (uint32_t)spustit_program(실행항목들[VYHLEDAT_INDEX].data, 실행항목들[VYHLEDAT_INDEX].Velikost, 실행항목들[VYHLEDAT_INDEX].전달값, 0, Název);
}
static uintptr_t Provést_Soubor(int 리눅스방식) {
    static unsigned char image[16384];
    if (Aktivní || !전달인수개수) return (uint32_t)-22;
    int popisovač_souboru = pk_open((const char *)전달인수[0], jen_pro_čtení_HODNOTA, 0);
    if (popisovač_souboru < 0) return (uint32_t)-číslo_chyby;
    int Velikost = pk_size(popisovač_souboru);
    if (Velikost < 0 || (unsigned)Velikost > sizeof(image)) { pk_close(popisovač_souboru); return (uint32_t)-27; }
    int RECEIVED_POČET = pk_read(popisovač_souboru, image, Velikost); pk_close(popisovač_souboru);
    if (RECEIVED_POČET != Velikost) return (uint32_t)-5;
    return (uint32_t)spustit_program(image, Velikost, 0, 리눅스방식, "");
}
uintptr_t Panel_uživatel_Soubor(void) { return Provést_Soubor(0); }
uintptr_t 보드사용자리눅스파일(void) { return Provést_Soubor(1); }
uintptr_t Panel_uživatel_ověřit(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].data, 잘못된실행항목들[순번].Velikost) != uživatel_spustitelný_chyba) return 순번 + 1;
    return 0;
}
