#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 Izvrši_komanda mašina sloj_VALUE. Fajl podaci/정책은 기존 AOT Java 커널에 위임한다.
#include "korisnik.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../Mreža_snop/Mreža_snop.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define mašina_registrirati(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_distributer 0xff841000ul
#define IRQ_CPU_interfejs 0xff842000ul
#define veličina_stranice 4096ul
#define 접근표시 (1ul << 10)
#define ne_Izvrši_dozvola (1ul << 53)
#define korisnik_ne_Izvrši (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | 접근표시)
#define jezgro_stranica (3ul | 보통기억 | ne_Izvrši_dozvola | korisnik_ne_Izvrši)
#define korisnik_i_za_čitanje_i_za_pisanje (3ul | 보통기억 | (1ul << 6) | ne_Izvrši_dozvola | korisnik_ne_Izvrši)
#define korisnik_samo_za_čitanje (3ul | 보통기억 | (3ul << 6) | ne_Izvrši_dozvola | korisnik_ne_Izvrši)
#define 사용자읽고실행 (3ul | 보통기억 | (3ul << 6) | ne_Izvrši_dozvola)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t ploča_pel(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t ploča_Terminal(uintptr_t);
extern int Terminal_na_čekanju(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int korisnik_CV(korisnik_kadar *,void *);
extern void 사용자실수보관(void *);
extern int korisnik_unijeti(uintptr_t unos_p, uintptr_t snop_Pohrana, uintptr_t 전달값);
extern void korisnik_vratiti(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t koijen_adresa[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t stranica_spisak[korisnik_stranica_COUNT] __attribute__((aligned(4096)));
static uint8_t dozvole_spisak[korisnik_stranica_COUNT];
static int aktivno, fajl_spisak[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned fajl_hvatište){return fajl_hvatište<40?자바전문닫기(fajl_hvatište):자바흐름닫기(fajl_hvatište);}
static uint64_t FREQUENCY, 마감시각;
static uintptr_t 동적기억끝;
// jezgro_VALUE 셸이 준비한 UTF-8 Argumenti. EL0에는 instanca_VALUE 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,interaktivno,리눅스규약,fajl_spisak[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char argument_niz[8][256],dozvole_spisak[korisnik_stranica_COUNT];
    uintptr_t 동적기억공간; korisnik_kadar 실행틀;
    unsigned char plutajuće_p_stanje[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int vlasnik_objekt,interaktivno;
static uint32_t broj_korisnika[4], korisnik_START_TIME[4], 사용자누적시각[4], 사용자실행시각[4], Dalje_broj_korisnika=10;
static unsigned char korisnik_komanda_naziv[4][288];
uint32_t 사용자상태읽기(unsigned unos_VALUE, unsigned INDEX) {
    unsigned položaj_INDEX=INDEX&3;
    int stanje_VALUE=(aktivno && vlasnik_objekt==(int)položaj_INDEX) ? 1 : 저장값[položaj_INDEX].멈춤상태 ? 2 : 0;
    if (unos_VALUE==0) return stanje_VALUE;
    if (!stanje_VALUE) return 0;
    if (unos_VALUE==1) return broj_korisnika[položaj_INDEX];
    if (unos_VALUE==2) {
        unsigned char *쪽들=stanje_VALUE==1?dozvole_spisak:저장값[položaj_INDEX].dozvole_spisak;
        unsigned stranica_COUNT=0; for (unsigned 순번=0; 순번<korisnik_stranica_COUNT; 순번++) if(쪽들[순번]) stranica_COUNT++;
        return stranica_COUNT*4;
    }
    if (unos_VALUE==3) return (uint32_t)보드밀리초()-korisnik_START_TIME[položaj_INDEX];
    if (unos_VALUE==4) return 사용자누적시각[položaj_INDEX]+(stanje_VALUE==1?(uint32_t)보드밀리초()-사용자실행시각[položaj_INDEX]:0);
    if (unos_VALUE==5) return INDEX/4<sizeof(korisnik_komanda_naziv[0])?korisnik_komanda_naziv[položaj_INDEX][INDEX/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t unos_COUNT) {
    if (aktivno || unos_COUNT > 8) return (uint32_t)-22;
    전달인수개수 = unos_COUNT;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t LOOKUP_INDEX, uintptr_t trenutno_položaj, uintptr_t bajt_podaci) {
    if (aktivno || LOOKUP_INDEX >= 전달인수개수 || trenutno_položaj >= 255 || trenutno_položaj != 전달인수길이[LOOKUP_INDEX] || !bajt_podaci || bajt_podaci > 255)
        return (uint32_t)-22;
    전달인수[LOOKUP_INDEX][trenutno_položaj] = bajt_podaci;
    전달인수길이[LOOKUP_INDEX] = trenutno_položaj + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Sat_VALUE(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void stati_TIMEOUT(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    mašina_registrirati(IRQ_distributer + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void START_TIMEOUT(void) {
    uint64_t 간격 = FREQUENCY * 2, omogućiti = 1;
    마감시각 = Sat_VALUE() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(omogućiti) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned podaci_blokirati = 0; podaci_blokirati < 4; podaci_blokirati++) {
        koijen_adresa[podaci_blokirati] = (uintptr_t)가운데[podaci_blokirati] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t adresa = ((uintptr_t)podaci_blokirati << 30) | ((uintptr_t)순번 << 21);
            가운데[podaci_blokirati][순번] = adresa | 1 | 접근표시 | korisnik_ne_Izvrši;
            if (adresa >= 0xfc000000ul) 가운데[podaci_blokirati][순번] |= ne_Izvrši_dozvola; // Device-nGnRnE
            else 가운데[podaci_blokirati][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned SECOND_VALUE = 0; SECOND_VALUE < korisnik_stranica_COUNT / 512; SECOND_VALUE++)
        가운데[0][(korisnik_BASE >> 21) + SECOND_VALUE] = (uintptr_t)(stranica_spisak + SECOND_VALUE * 512) | 3;
    for (unsigned 순번 = 0; 순번 < korisnik_stranica_COUNT; 순번++) stranica_spisak[순번] = (korisnik_BASE + 순번 * veličina_stranice) | jezgro_stranica;
    uint64_t Memorija_atribut_registrirati = 0x4400, adresa_Prevođenje_kontrola = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Memorija_atribut_registrirati), "r"(adresa_Prevođenje_kontrola), "r"((uintptr_t)koijen_adresa) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t plutajuće_p_stanje = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(plutajuće_p_stanje) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    stati_TIMEOUT();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 unos_p_VALUE 때만 Dozvoliti_VALUE.
    mašina_registrirati(IRQ_distributer) = 0;
    mašina_registrirati(IRQ_distributer + 0x180) = 0xffffffff;
    mašina_registrirati(IRQ_distributer + 0x80) = 0xffffffff;
    mašina_registrirati(IRQ_distributer + 0x280) = 1u << 30;
    mašina_registrirati(IRQ_distributer + 0x41c) = 0x80808080;
    mašina_registrirati(IRQ_distributer + 0x100) = 1u << 30;
    mašina_registrirati(IRQ_CPU_interfejs + 4) = 0xff;
    mašina_registrirati(IRQ_CPU_interfejs + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 수 있다.
    int Sigurnost = (mašina_registrirati(IRQ_distributer + 4) & (1u << 10)) != 0;
    mašina_registrirati(IRQ_distributer) = Sigurnost ? 1 : 3;
    mašina_registrirati(IRQ_CPU_interfejs) = Sigurnost ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t TYPE_oblast, mašina_TYPE; uint32_t broj_verzije;
    uint64_t unos_p, program_Zaglavlje_Pomak, sekcija_Zaglavlje_Pomak; uint32_t 설정비트;
    uint16_t 실행머리크기, program_Zaglavlje_unos_podesiti_veličinu, program_Zaglavlje_COUNT, sekcija_Zaglavlje_unos_podesiti_veličinu, sekcija_Zaglavlje_COUNT, sekcija_naziv_tabela_INDEX;
} 실행파일머리;
typedef struct { uint32_t TYPE_oblast, 설정비트; uint64_t Pomak_VALUE, adresa, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(korisnik_kadar) == 272, "exception assembly layout");
static int 포함된범위(uint64_t Pomak_VALUE, uint64_t Veličina, uint64_t završiti_Pomak) {
    return Pomak_VALUE <= završiti_Pomak && Veličina <= završiti_Pomak - Pomak_VALUE;
}
static int 부가정보검사(const unsigned char *podaci_položaj, size_t Veličina) {
    size_t trenutno_položaj = 0;
    while (포함된범위(trenutno_položaj, 12, Veličina)) {
        uint32_t 낱말들[3]; memcpy(낱말들, podaci_položaj + trenutno_položaj, 12); trenutno_položaj += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(trenutno_položaj, 이름영역크기, Veličina) || !포함된범위(trenutno_položaj + 이름영역크기, 설명크기, Veličina)) return 0;
        const unsigned char Naziv[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Naziv) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Naziv); 순번++) if (podaci_položaj[trenutno_položaj + 순번] != Naziv[순번]) 일치 = 0;
        uint32_t broj_verzije = 0;
        if (일치) memcpy(&broj_verzije, podaci_položaj + trenutno_položaj + 이름영역크기, 4);
        if (일치 && broj_verzije == 1) return 1;
        trenutno_položaj += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *podaci, size_t Veličina, int 리눅스방식) {
    if (Veličina < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, podaci, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.TYPE_oblast != 2 || 실행머리.mašina_TYPE != 183 || 실행머리.broj_verzije != 1 || 실행머리.설정비트 || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.program_Zaglavlje_unos_podesiti_veličinu != sizeof(실행파일구획) || !실행머리.program_Zaglavlje_COUNT || 실행머리.program_Zaglavlje_COUNT > 16 ||
        실행머리.program_Zaglavlje_Pomak < sizeof(실행머리) || !포함된범위(실행머리.program_Zaglavlje_Pomak, (uint64_t)실행머리.program_Zaglavlje_COUNT * sizeof(실행파일구획), Veličina)) return 사용자실행파일오류;
    uint8_t 사용량[(korisnik_IMAGE_završiti - korisnik_BASE) / veličina_stranice] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.program_Zaglavlje_COUNT; 순번++) {
        실행파일구획 podaci_položaj; memcpy(&podaci_položaj, podaci + 실행머리.program_Zaglavlje_Pomak + 순번 * sizeof(podaci_položaj), sizeof(podaci_položaj));
        if (podaci_položaj.TYPE_oblast == 4) {
            if (!포함된범위(podaci_položaj.Pomak_VALUE, podaci_položaj.파일영역크기, Veličina)) return 사용자실행파일오류;
            if (부가정보검사(podaci + podaci_položaj.Pomak_VALUE, podaci_položaj.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (podaci_položaj.TYPE_oblast == 0 || podaci_položaj.TYPE_oblast == 6 || (podaci_položaj.TYPE_oblast == 0x6474e551 && !(podaci_položaj.설정비트 & 1))) continue;
        if (podaci_položaj.TYPE_oblast != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!podaci_položaj.기억영역크기) continue;
        if (podaci_položaj.설정비트 & ~7u || !(podaci_položaj.설정비트 & 4) || (podaci_položaj.설정비트 & 3) == 3 || podaci_položaj.파일영역크기 > podaci_položaj.기억영역크기 ||
            (podaci_položaj.파일영역크기 && !포함된범위(podaci_položaj.Pomak_VALUE, podaci_položaj.파일영역크기, Veličina)) || podaci_položaj.adresa < korisnik_BASE ||
            !포함된범위(podaci_položaj.adresa, podaci_položaj.기억영역크기, korisnik_IMAGE_završiti) ||
            (!리눅스방식 && ((podaci_položaj.adresa & (veličina_stranice - 1)) || (podaci_položaj.Pomak_VALUE & (veličina_stranice - 1)) || podaci_položaj.맞춤 != veličina_stranice)) ||
            (리눅스방식 && (((podaci_položaj.adresa ^ podaci_položaj.Pomak_VALUE) & (veličina_stranice - 1)) || !podaci_položaj.맞춤 ||
                (podaci_položaj.맞춤 & (podaci_položaj.맞춤 - 1)) || podaci_položaj.맞춤 > 0x200000 || ((podaci_položaj.adresa ^ podaci_položaj.Pomak_VALUE) & (podaci_položaj.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (podaci_položaj.adresa - korisnik_BASE) / veličina_stranice;
        unsigned unos_COUNT = ((podaci_položaj.adresa & (veličina_stranice - 1)) + podaci_položaj.기억영역크기 + veličina_stranice - 1) / veličina_stranice;
        for (unsigned stranica_VALUE = 첫항목; stranica_VALUE < 첫항목 + unos_COUNT; stranica_VALUE++) {
            if (사용량[stranica_VALUE]) return 사용자실행파일오류;
            사용량[stranica_VALUE] = 1;
        }
        if ((podaci_položaj.설정비트 & 1) && 실행머리.unos_p >= podaci_položaj.adresa && 실행머리.unos_p < podaci_položaj.adresa + podaci_položaj.파일영역크기 && !(실행머리.unos_p & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *podaci, size_t Veličina) { return 실행파일검사(podaci, Veličina, 0); }
static void prikaz_stranice(uintptr_t adresa, uint64_t 설정비트, unsigned dozvole) {
    unsigned LOOKUP_INDEX = (adresa - korisnik_BASE) / veličina_stranice;
    stranica_spisak[LOOKUP_INDEX] = adresa | 설정비트;
    dozvole_spisak[LOOKUP_INDEX] = dozvole;
}
static int 사용자범위(uintptr_t adresa, size_t unos_COUNT, int 쓰는중) {
    if (adresa < korisnik_BASE || !포함된범위(adresa, unos_COUNT, korisnik_završiti)) return 0;
    if (!unos_COUNT) return 1;
    unsigned 첫항목 = (adresa - korisnik_BASE) / veličina_stranice, 마지막 = (adresa + unos_COUNT - 1 - korisnik_BASE) / veličina_stranice;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(dozvole_spisak[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int instanca_put(uintptr_t adresa, char *Putanja) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!사용자범위(adresa, 1, 0)) return -14;
        Putanja[순번] = *(const char *)adresa++;
        if (!Putanja[순번]) return 0;
    }
    return -36;
}
static intptr_t jezgro_mjera(intptr_t mjera) { return mjera < 0 ? -broj_greške : mjera; }
static int 대응파일기술자(uint64_t fajl_hvatište) { return fajl_hvatište >= 3 && fajl_hvatište < 19 ? fajl_spisak[fajl_hvatište - 3] : -1; }
static int 통신끝점소유(uint64_t fajl_hvatište) { return fajl_hvatište >= 32 && fajl_hvatište < 56 && 통신끝점들[fajl_hvatište - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t dužina_VALUE, struct pk_sockaddr_in *adresa) {
    if (dužina_VALUE != sizeof(*adresa)) return -22;
    if (!사용자범위(가리킴값, dužina_VALUE, 0)) return -14;
    memcpy(adresa, (const void *)가리킴값, sizeof(*adresa));
    return adresa->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t dužina_pokazivač, pk_socklen_t *수용량) {
    if (!사용자범위(dužina_pokazivač, sizeof(*수용량), 1)) return -14;
    memcpy(수용량, (const void *)dužina_pokazivač, sizeof(*수용량));
    if (*수용량 > sizeof(struct pk_sockaddr_in)) *수용량 = sizeof(struct pk_sockaddr_in);
    if (*수용량 && !사용자범위(가리킴값, *수용량, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t dužina_pokazivač, pk_socklen_t 수용량, int adresa, int broj_priključka) {
    struct pk_sockaddr_in VALUE; memset(&VALUE, 0, sizeof(VALUE));
    VALUE.sin_family = AF_INET; VALUE.sin_port = pk_htons(broj_priključka); VALUE.sin_addr.s_addr = pk_htonl(adresa);
    if (수용량) memcpy((void *)가리킴값, &VALUE, 수용량);
    pk_socklen_t dužina_VALUE = sizeof(VALUE); memcpy((void *)dužina_pokazivač, &dužina_VALUE, sizeof(dužina_VALUE));
}
extern uintptr_t ploča_kanal(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(korisnik_kadar *fajl_unos) {
    uintptr_t 첫째값 = fajl_unos->registrirati_podaci[0], SECOND_VALUE = fajl_unos->registrirati_podaci[1], kôd_znaka = fajl_unos->registrirati_podaci[2];
    char Putanja[65];
    int fajl_hvatište, mjera;
    switch (fajl_unos->registrirati_podaci[8]) {
    case 0: return 1; // 자체 ABI 버전
    case 1: // write: pokazivač 전체를 검사한 ZAD_VALUE Ispis/Fajl promijeniti_VALUE
        if (kôd_znaka > 65536) return -22;
        if (!사용자범위(SECOND_VALUE, kôd_znaka, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=Sat_VALUE();
            for (size_t 순번 = 0; 순번 < kôd_znaka; 순번++) ploča_kanal(첫째값, ((const unsigned char *)SECOND_VALUE)[순번]);
            /* 큰 tty를 그린 jezgro_VALUE 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(interaktivno){
                마감시각+=Sat_VALUE()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(마감시각) : "memory");
            }
            return kôd_znaka;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t stavka_COUNT=kôd_znaka>512?512:kôd_znaka;for(size_t 순번=0;순번<stavka_COUNT;순번++)자바전문넣기(순번,((const unsigned char *)SECOND_VALUE)[순번]);return 자바흐름쓰기(첫째값,stavka_COUNT);
        }
        fajl_hvatište = 대응파일기술자(첫째값); if (fajl_hvatište < 0) return -9;
        return jezgro_mjera(pk_write(fajl_hvatište, (const void *)SECOND_VALUE, kôd_znaka));
    case 2:
        if (kôd_znaka > 65536) return -22;
        if (!사용자범위(SECOND_VALUE, kôd_znaka, 1)) return -14;
        if (첫째값 == 0) {
            size_t stavka_COUNT = 0;
            while (stavka_COUNT < kôd_znaka) {
                int znak_VALUE = (int32_t)보드글자읽기(); if (znak_VALUE == -2) return stavka_COUNT; if (znak_VALUE < 0) break;
                ((unsigned char *)SECOND_VALUE)[stavka_COUNT++] = znak_VALUE;
            }
            return stavka_COUNT ? (intptr_t)stavka_COUNT : (kôd_znaka ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            mjera=자바흐름읽기(첫째값,kôd_znaka>512?512:kôd_znaka);if(mjera>0)for(int 순번=0;순번<mjera;순번++)((unsigned char *)SECOND_VALUE)[순번]=자바전문얻기(순번);return mjera;
        }
        fajl_hvatište = 대응파일기술자(첫째값); if (fajl_hvatište < 0) return -9;
        return jezgro_mjera(pk_read(fajl_hvatište, (void *)SECOND_VALUE, kôd_znaka));
    case 3:
        mjera = instanca_put(첫째값, Putanja); if (mjera) return mjera;
        if (SECOND_VALUE > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (fajl_spisak[순번] < 0) {
            fajl_hvatište = pk_open(Putanja, (int)SECOND_VALUE, 0600);
            if (fajl_hvatište < 0) return -broj_greške;
            fajl_spisak[순번] = fajl_hvatište; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { mjera = 통신끝점닫기(첫째값); if (!mjera) 통신끝점들[첫째값 - 32] = 0; return mjera; }
        fajl_hvatište = 대응파일기술자(첫째값); if (fajl_hvatište < 0) return -9;
        mjera = pk_close(fajl_hvatište); if (!mjera) fajl_spisak[첫째값 - 3] = -1;
        return jezgro_mjera(mjera);
    case 5:
        fajl_hvatište = 대응파일기술자(첫째값); if (fajl_hvatište < 0) return -9;
        if (kôd_znaka > 2) return -22;
        return jezgro_mjera(pk_lseek(fajl_hvatište, (int64_t)SECOND_VALUE, kôd_znaka));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 korisnik RW/NX 힙, 새로 노출되는 페이지는 0으로 inicijalizirati
        if (!첫째값) return 동적기억끝;
        if (첫째값 < korisnik_IMAGE_završiti || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + veličina_stranice - 1) & ~(veličina_stranice - 1);
        uintptr_t 새쪽들 = (첫째값 + veličina_stranice - 1) & ~(veličina_stranice - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t podaci_položaj = 이전쪽들; podaci_položaj < 새쪽들; podaci_položaj += veličina_stranice) prikaz_stranice(podaci_položaj, jezgro_stranica, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t podaci_položaj = 이전쪽들; podaci_položaj < 새쪽들; podaci_položaj += veličina_stranice) prikaz_stranice(podaci_položaj, korisnik_i_za_čitanje_i_za_pisanje, 3);
        } else {
            for (uintptr_t podaci_položaj = 새쪽들; podaci_položaj < 이전쪽들; podaci_položaj += veličina_stranice) {
                stranica_spisak[(podaci_položaj - korisnik_BASE) / veličina_stranice] = 0; dozvole_spisak[(podaci_položaj - korisnik_BASE) / veličina_stranice] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        fajl_hvatište = 대응파일기술자(첫째값); return fajl_hvatište < 0 ? -9 : jezgro_mjera(pk_size(fajl_hvatište));
    case 10:
        fajl_hvatište = 대응파일기술자(첫째값); return fajl_hvatište < 0 ? -9 : jezgro_mjera(pk_ftruncate(fajl_hvatište, (int64_t)SECOND_VALUE));
    case 11:
        mjera = instanca_put(첫째값, Putanja); return mjera ? mjera : jezgro_mjera(pk_unlink(Putanja));
    case 12:
        fajl_hvatište = 대응파일기술자(첫째값); return fajl_hvatište < 0 ? -9 : jezgro_mjera(pk_fsync(fajl_hvatište));
    case 13: { // 그래픽 기초 API: korisnik 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = fajl_unos->registrirati_podaci[3], 높이값 = fajl_unos->registrirati_podaci[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SECOND_VALUE > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - SECOND_VALUE) return -22;
        for (uintptr_t Y_koordinata = SECOND_VALUE; Y_koordinata < SECOND_VALUE + 높이값; Y_koordinata++) for (uintptr_t koordinata_x = 첫째값; koordinata_x < 첫째값 + 너비값; koordinata_x++) ploča_pel(koordinata_x, Y_koordinata, kôd_znaka);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=stavka_COUNT; args(index,buffer,capacity)=UTF-8 dužina_VALUE
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (kôd_znaka <= 전달인수길이[첫째값]) return -36;
        if (!사용자범위(SECOND_VALUE, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SECOND_VALUE, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;interaktivno=1;return ploča_Terminal(13);}
        if(첫째값==2){interaktivno=0;return 0;}
        if(첫째값==3)return ploča_Terminal(13);
        if(첫째값!=1||!interaktivno)return -22;
        mjera=(int32_t)보드글자읽기();
        if(mjera==-4096)return mjera;
        START_TIMEOUT();return mjera<0?-11:mjera;
    case 17: { // 유한한 협력 čekaj_VALUE: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t završiti_TIME = Sat_VALUE() + FREQUENCY * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Sat_VALUE() < završiti_TIME);
        START_TIMEOUT(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 roditelj_VALUE·빈 폴더를 검사한다.
        if (SECOND_VALUE > 2) return -22;
        mjera = instanca_put(첫째값, Putanja); if (mjera) return mjera;
        unsigned dužina_VALUE = 0; while (Putanja[dužina_VALUE]) dužina_VALUE++;
        mjera = 자바경로시작(dužina_VALUE); if (mjera < 0) return mjera;
        for (unsigned 순번 = 0; 순번 < dužina_VALUE; 순번++) 자바경로바이트(순번, (unsigned char)Putanja[순번]);
        return SECOND_VALUE == 0 ? 자바항목종류() : SECOND_VALUE == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int znak_VALUE=(int32_t)보드글자읽기();if(znak_VALUE==-4096)return znak_VALUE;if(znak_VALUE>=0)화면누름(vlasnik_objekt,znak_VALUE);START_TIMEOUT();}
        if(첫째값==3&&kôd_znaka){if(!자바셸대화형())return -95;interaktivno=1;ploča_Terminal(300);}
        return 화면호출(vlasnik_objekt,첫째값,SECOND_VALUE,kôd_znaka,fajl_unos->registrirati_podaci[3],fajl_unos->registrirati_podaci[4],fajl_unos->registrirati_podaci[5]);
    case 21:
        if(kôd_znaka>127)return -22;if(!사용자범위(SECOND_VALUE,kôd_znaka*sizeof(uint32_t),0))return -14;
        return 화면글(vlasnik_objekt,첫째값,(const uint32_t *)SECOND_VALUE,kôd_znaka);
    case 22: // 화면 Veličina upit_VALUE: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SECOND_VALUE==SOCK_STREAM&&(kôd_znaka==0||kôd_znaka==6))mjera=자바흐름만들기();
        else if(SECOND_VALUE==SOCK_DGRAM&&(kôd_znaka==0||kôd_znaka==IPPROTO_UDP))mjera=자바전문만들기(첫째값,SECOND_VALUE,kôd_znaka);
        else return -93;
        if (mjera >= 32 && mjera < 56) 통신끝점들[mjera - 32] = 1;
        return mjera;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in adresa;
        mjera = 주소입력(SECOND_VALUE, kôd_znaka, &adresa); if (mjera) return mjera;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(adresa.sin_addr.s_addr),pk_htons(adresa.sin_port)):자바전문묶기(첫째값, pk_htonl(adresa.sin_addr.s_addr), pk_htons(adresa.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (fajl_unos->registrirati_podaci[3]) return -95;
        if (kôd_znaka > 512) return -90;
        if (kôd_znaka && !사용자범위(SECOND_VALUE, kôd_znaka, 0)) return -14;
        struct pk_sockaddr_in adresa;
        mjera = 주소입력(fajl_unos->registrirati_podaci[4], fajl_unos->registrirati_podaci[5], &adresa); if (mjera) return mjera;
        for (unsigned 순번 = 0; 순번 < kôd_znaka; 순번++) 자바전문넣기(순번, ((const unsigned char *)SECOND_VALUE)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(adresa.sin_addr.s_addr), pk_htons(adresa.sin_port), kôd_znaka);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (fajl_unos->registrirati_podaci[3]) return -95;
        if (kôd_znaka > 512) return -90;
        if (kôd_znaka && !사용자범위(SECOND_VALUE, kôd_znaka, 1)) return -14;
        pk_socklen_t 수용량 = 0;
        if (fajl_unos->registrirati_podaci[4]) { mjera = 주소출력검사(fajl_unos->registrirati_podaci[4], fajl_unos->registrirati_podaci[5], &수용량); if (mjera) return mjera; }
        mjera = 자바전문받기(첫째값, kôd_znaka); if (mjera < 0) return mjera;
        for (int 순번 = 0; 순번 < mjera; 순번++) ((unsigned char *)SECOND_VALUE)[순번] = 자바전문얻기(순번);
        if (fajl_unos->registrirati_podaci[4]) 주소출력(fajl_unos->registrirati_podaci[4], fajl_unos->registrirati_podaci[5], 수용량, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return mjera;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t 수용량;
        mjera = 주소출력검사(SECOND_VALUE, kôd_znaka, &수용량); if (mjera) return mjera;
        주소출력(SECOND_VALUE,kôd_znaka,수용량,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in adresa;
        mjera=주소입력(SECOND_VALUE,kôd_znaka,&adresa);if(mjera)return mjera;
        return 자바흐름연결(첫째값,pk_htonl(adresa.sin_addr.s_addr),pk_htons(adresa.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,SECOND_VALUE):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(SECOND_VALUE||kôd_znaka)return -95;mjera=자바흐름연결받기(첫째값);if(mjera>=40&&mjera<56)통신끝점들[mjera-32]=1;return mjera;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(korisnik_kadar *fajl_unos) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(fajl_unos) : 자체체계호출(fajl_unos);
}
static void vratiti_jezgro(korisnik_kadar *fajl_unos, int mjera) {
    stati_TIMEOUT();
    fajl_unos->registrirati_podaci[0] = (uint64_t)(int64_t)mjera;
    fajl_unos->komanda_položaj = (uintptr_t)korisnik_vratiti;
    fajl_unos->stanje_kod = 0x3c5; // EL1h, DAIF masked
}
int korisnik_izuzetak(korisnik_kadar *fajl_unos, unsigned presjek) {
    if (!aktivno || (fajl_unos->stanje_kod & 15) != 0) return 0;
    if (presjek) {
        uint32_t 승인값 = mašina_registrirati(IRQ_CPU_interfejs + 0xc), identifikator_VALUE = 승인값 & 1023;
        if (identifikator_VALUE == 30) { vratiti_jezgro(fajl_unos, korisnik_TIMEOUT); mašina_registrirati(IRQ_CPU_interfejs + 0x10) = 승인값; return 1; }
        if (identifikator_VALUE < 1020) mašina_registrirati(IRQ_CPU_interfejs + 0x10) = 승인값;
        return 1;
    }
    uint64_t izuzetak_stanje; __asm__ volatile("mrs %0, esr_el1" : "=r"(izuzetak_stanje));
    if (Sat_VALUE() >= 마감시각) { vratiti_jezgro(fajl_unos, korisnik_TIMEOUT); return 1; }
    unsigned izuzetak_oblast = izuzetak_stanje >> 26;
    if (izuzetak_oblast == 0x15 && (izuzetak_stanje & 0xffff) == 0) {
        if (리눅스규약 ? fajl_unos->registrirati_podaci[8] == 93 || fajl_unos->registrirati_podaci[8] == 94 : fajl_unos->registrirati_podaci[8] == 6) vratiti_jezgro(fajl_unos, (int)(fajl_unos->registrirati_podaci[0] & 255));
        else {
            intptr_t mjera=체계호출(fajl_unos);
            if(mjera==-4096&&interaktivno){
                저장값[vlasnik_objekt].실행틀=*fajl_unos;저장값[vlasnik_objekt].실행틀.komanda_položaj-=4;
                사용자실수보관(저장값[vlasnik_objekt].plutajuće_p_stanje);vratiti_jezgro(fajl_unos,사용자중단됨);
            }else fajl_unos->registrirati_podaci[0]=(uint64_t)mjera;
        }
    } else vratiti_jezgro(fajl_unos, izuzetak_oblast == 0x24 ? korisnik_podaci_greška : izuzetak_oblast == 0x20 ? 사용자실행오류 : korisnik_nevažeće_programska_naredba);
    return 1;
}

// 생성된 const ELF Grupa_VALUE: 실행은 반드시 program_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *podaci; size_t Veličina; unsigned 전달값; } program;
#include "programs.h"
static void *snimak(unsigned položaj_INDEX){return (void *)(0x04000000ul+položaj_INDEX*(korisnik_završiti-korisnik_BASE));}
static int Kraj_program(int mjera){
    사용자누적시각[vlasnik_objekt]+=(uint32_t)보드밀리초()-사용자실행시각[vlasnik_objekt];
    stati_TIMEOUT();aktivno=0;
    if(mjera==사용자중단됨){
        저장된작업 *string_podaci=&저장값[vlasnik_objekt];string_podaci->멈춤상태=1;string_podaci->interaktivno=interaktivno;string_podaci->리눅스규약=리눅스규약;string_podaci->동적기억공간=동적기억끝;string_podaci->인수개수=전달인수개수;
        memcpy(string_podaci->dozvole_spisak,dozvole_spisak,sizeof(dozvole_spisak));memcpy(string_podaci->fajl_spisak,fajl_spisak,sizeof(fajl_spisak));memcpy(string_podaci->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(string_podaci->argument_niz,전달인수,sizeof(전달인수));memcpy(string_podaci->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<korisnik_stranica_COUNT;순번++)if(dozvole_spisak[순번])memcpy((unsigned char *)snimak(vlasnik_objekt)+순번*veličina_stranice,(void *)(korisnik_BASE+순번*veličina_stranice),veličina_stranice);
    }else{
        저장값[vlasnik_objekt].멈춤상태=0;화면초기화(vlasnik_objekt);
        for(unsigned 순번=0;순번<16;순번++)if(fajl_spisak[순번]>=0)pk_close(fajl_spisak[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<korisnik_stranica_COUNT;순번++){stranica_spisak[순번]=0;dozvole_spisak[순번]=0;}변환표맞추기();return mjera;
}
uintptr_t ploča_korisnička_kontrola(uintptr_t radnja){
    unsigned položaj_INDEX=radnja&15;if(položaj_INDEX>=4||aktivno)return (uint32_t)-22;
    저장된작업 *string_podaci=&저장값[položaj_INDEX];
    if(radnja>=32){if(string_podaci->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(string_podaci->fajl_spisak[순번]>=0)pk_close(string_podaci->fajl_spisak[순번]);for(unsigned 순번=0;순번<24;순번++)if(string_podaci->통신끝점들[순번])통신끝점닫기(순번+32);}string_podaci->멈춤상태=0;화면초기화(položaj_INDEX);return 0;}
    if(radnja>=16)return string_podaci->멈춤상태;
    if(!string_podaci->멈춤상태)return (uint32_t)-22;
    vlasnik_objekt=položaj_INDEX;interaktivno=string_podaci->interaktivno;리눅스규약=string_podaci->리눅스규약;동적기억끝=string_podaci->동적기억공간;전달인수개수=string_podaci->인수개수;
    memcpy(fajl_spisak,string_podaci->fajl_spisak,sizeof(fajl_spisak));memcpy(통신끝점들,string_podaci->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,string_podaci->argument_niz,sizeof(전달인수));memcpy(전달인수길이,string_podaci->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<korisnik_stranica_COUNT;순번++)stranica_spisak[순번]=(korisnik_BASE+순번*veličina_stranice)|jezgro_stranica;변환표맞추기();
    memset((void *)korisnik_BASE,0,korisnik_završiti-korisnik_BASE);
    for(unsigned 순번=0;순번<korisnik_stranica_COUNT;순번++)if(string_podaci->dozvole_spisak[순번])memcpy((void *)(korisnik_BASE+순번*veličina_stranice),(unsigned char *)snimak(položaj_INDEX)+순번*veličina_stranice,veličina_stranice);
    memcpy(dozvole_spisak,string_podaci->dozvole_spisak,sizeof(dozvole_spisak));
    for(unsigned 순번=0;순번<korisnik_stranica_COUNT;순번++){unsigned podaci_položaj=dozvole_spisak[순번];stranica_spisak[순번]=podaci_položaj?(korisnik_BASE+순번*veličina_stranice)|(podaci_položaj==3?korisnik_i_za_čitanje_i_za_pisanje:podaci_položaj==5?사용자읽고실행:korisnik_samo_za_čitanje):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");aktivno=1;string_podaci->멈춤상태=0;START_TIMEOUT();
    사용자실행시각[vlasnik_objekt]=보드밀리초();
    return (uint32_t)Kraj_program(korisnik_CV(&string_podaci->실행틀,string_podaci->plutajuće_p_stanje));
}
static int niz_program(const unsigned char *podaci, size_t Veličina, unsigned 전달값, int 리눅스방식, const char *Naziv) {
    if (aktivno) return -16;
    vlasnik_objekt=ploča_Terminal(11);if(vlasnik_objekt<0||vlasnik_objekt>3||저장값[vlasnik_objekt].멈춤상태)return -16;interaktivno=0;
    int 유효함 = 실행파일검사(podaci, Veličina, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned naziv_INDEX=0;
    while (*Naziv && naziv_INDEX<31) korisnik_komanda_naziv[vlasnik_objekt][naziv_INDEX++]=(unsigned char)*Naziv++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (naziv_INDEX) korisnik_komanda_naziv[vlasnik_objekt][naziv_INDEX++]=' ';
        for (unsigned položaj_INDEX=0; položaj_INDEX<전달인수길이[0]; položaj_INDEX++) korisnik_komanda_naziv[vlasnik_objekt][naziv_INDEX++]=전달인수[0][položaj_INDEX];
    }
    korisnik_komanda_naziv[vlasnik_objekt][naziv_INDEX]=0; broj_korisnika[vlasnik_objekt]=Dalje_broj_korisnika++;
    if (Dalje_broj_korisnika>0x7fffffffu) Dalje_broj_korisnika=10;
    korisnik_START_TIME[vlasnik_objekt]=보드밀리초(); 사용자누적시각[vlasnik_objekt]=0;
    for (unsigned 순번 = 0; 순번 < korisnik_stranica_COUNT; 순번++) stranica_spisak[순번] = (korisnik_BASE + 순번 * veličina_stranice) | jezgro_stranica;
    변환표맞추기();
    memset((void *)korisnik_BASE, 0, korisnik_završiti - korisnik_BASE);
    memset(dozvole_spisak, 0, sizeof(dozvole_spisak));
    실행파일머리 실행머리; memcpy(&실행머리, podaci, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.program_Zaglavlje_COUNT; 순번++) {
        실행파일구획 podaci_položaj; memcpy(&podaci_položaj, podaci + 실행머리.program_Zaglavlje_Pomak + 순번 * sizeof(podaci_položaj), sizeof(podaci_položaj));
        if (podaci_položaj.TYPE_oblast != 1 || !podaci_položaj.기억영역크기) continue;
        if (podaci_položaj.파일영역크기) memcpy((void *)(uintptr_t)podaci_položaj.adresa, podaci + podaci_položaj.Pomak_VALUE, podaci_položaj.파일영역크기);
        for (uintptr_t trenutno_položaj = podaci_položaj.adresa & ~(veličina_stranice - 1); trenutno_položaj < podaci_položaj.adresa + podaci_položaj.기억영역크기; trenutno_položaj += veličina_stranice) {
            dozvole_spisak[(trenutno_položaj - korisnik_BASE) / veličina_stranice] = (podaci_položaj.설정비트 & 2) ? 3 : ((podaci_položaj.설정비트 & 1) ? 5 : 1);
        }
    }
    for (uintptr_t trenutno_položaj = korisnik_snop_adresa; trenutno_položaj < korisnik_završiti; trenutno_položaj += veličina_stranice) dozvole_spisak[(trenutno_položaj - korisnik_BASE) / veličina_stranice] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.unos_p) : korisnik_završiti;
    for (unsigned 순번 = 0; 순번 < korisnik_stranica_COUNT; 순번++) {
        unsigned dozvole = dozvole_spisak[순번];
        stranica_spisak[순번] = dozvole ? (korisnik_BASE + 순번 * veličina_stranice) | (dozvole == 3 ? korisnik_i_za_čitanje_i_za_pisanje : dozvole == 5 ? 사용자읽고실행 : korisnik_samo_za_čitanje) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) fajl_spisak[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = korisnik_IMAGE_završiti;
    aktivno = 1; START_TIMEOUT();
    사용자실행시각[vlasnik_objekt]=보드밀리초();
    int mjera = korisnik_unijeti(실행머리.unos_p, 초기쌓임공간, 전달값);
    return Kraj_program(mjera);
}
uintptr_t ploča_korisnik_niz(uintptr_t LOOKUP_INDEX) {
    if (LOOKUP_INDEX >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Naziv=LOOKUP_INDEX==10?"javac":LOOKUP_INDEX==11?"java":LOOKUP_INDEX==12?"python":LOOKUP_INDEX==13?"vi":LOOKUP_INDEX==14?"jar":LOOKUP_INDEX==15?"cc":LOOKUP_INDEX==16?"jaot":"ELF";
    return (uint32_t)niz_program(실행항목들[LOOKUP_INDEX].podaci, 실행항목들[LOOKUP_INDEX].Veličina, 실행항목들[LOOKUP_INDEX].전달값, 0, Naziv);
}
static uintptr_t Izvrši_fajl(int 리눅스방식) {
    static unsigned char IMAGE[16384];
    if (aktivno || !전달인수개수) return (uint32_t)-22;
    int fajl_hvatište = pk_open((const char *)전달인수[0], samo_za_čitanje_VALUE, 0);
    if (fajl_hvatište < 0) return (uint32_t)-broj_greške;
    int Veličina = pk_size(fajl_hvatište);
    if (Veličina < 0 || (unsigned)Veličina > sizeof(IMAGE)) { pk_close(fajl_hvatište); return (uint32_t)-27; }
    int RECEIVED_COUNT = pk_read(fajl_hvatište, IMAGE, Veličina); pk_close(fajl_hvatište);
    if (RECEIVED_COUNT != Veličina) return (uint32_t)-5;
    return (uint32_t)niz_program(IMAGE, Veličina, 0, 리눅스방식, "");
}
uintptr_t ploča_korisnik_fajl(void) { return Izvrši_fajl(0); }
uintptr_t 보드사용자리눅스파일(void) { return Izvrši_fajl(1); }
uintptr_t ploča_korisnik_ovjeriti(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].podaci, 잘못된실행항목들[순번].Veličina) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
