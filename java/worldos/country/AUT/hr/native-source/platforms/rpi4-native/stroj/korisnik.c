#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 Izvrši_naredba stroj sloj_VALUE. Datoteka podaci/정책은 기존 AOT Java 커널에 위임한다.
#include "korisnik.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../mreža_hrpa/mreža_hrpa.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define stroj_registar(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_distributer 0xff841000ul
#define IRQ_CPU_sučelje 0xff842000ul
#define veličina_stranice 4096ul
#define pristup_marker (1ul << 10)
#define ne_Izvrši_dozvola (1ul << 53)
#define korisnik_ne_Izvrši (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | pristup_marker)
#define jezgra_sustava_dojaviti (3ul | 보통기억 | ne_Izvrši_dozvola | korisnik_ne_Izvrši)
#define 사용자읽고쓰기 (3ul | 보통기억 | (1ul << 6) | ne_Izvrši_dozvola | korisnik_ne_Izvrši)
#define korisnik_samo_za_čitanje (3ul | 보통기억 | (3ul << 6) | ne_Izvrši_dozvola | korisnik_ne_Izvrši)
#define 사용자읽고실행 (3ul | 보통기억 | (3ul << 6) | ne_Izvrši_dozvola)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t pano_slikovni_element(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t pano_Terminal(uintptr_t);
extern int Terminal_na_čekanju(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int korisnik_nastaviti(korisnik_kadar *,void *);
extern void 사용자실수보관(void *);
extern int korisnik_unijeti(uintptr_t unos_p, uintptr_t hrpa_Pohrana, uintptr_t 전달값);
extern void korisnik_vratiti(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t korijen_adresa[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t dojaviti_Popis[korisnik_dojaviti_COUNT] __attribute__((aligned(4096)));
static uint8_t Dozvole_Popis[korisnik_dojaviti_COUNT];
static int Aktivan, Datoteka_Popis[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned Datoteka_ustroj){return Datoteka_ustroj<40?자바전문닫기(Datoteka_ustroj):자바흐름닫기(Datoteka_ustroj);}
static uint64_t FREQUENCY, rok_za_dovršetak_TIME;
static uintptr_t 동적기억끝;
// jezgra_sustava_VALUE 셸이 준비한 UTF-8 Argumenti. EL0에는 instanca_VALUE 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,대화형,리눅스규약,Datoteka_Popis[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char argument_ARRAY[8][256],Dozvole_Popis[korisnik_dojaviti_COUNT];
    uintptr_t 동적기억공간; korisnik_kadar 실행틀;
    unsigned char plutajući_p_Stanje[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int vlasnik_objekt,대화형;
static uint32_t broj_korisnika[4], korisnik_START_TIME[4], 사용자누적시각[4], 사용자실행시각[4], Dalje_broj_korisnika=10;
static unsigned char korisnik_naredba_naziv[4][288];
uint32_t 사용자상태읽기(unsigned unos_VALUE, unsigned INDEX) {
    unsigned indeks_položaja=INDEX&3;
    int Stanje_VALUE=(Aktivan && vlasnik_objekt==(int)indeks_položaja) ? 1 : 저장값[indeks_položaja].멈춤상태 ? 2 : 0;
    if (unos_VALUE==0) return Stanje_VALUE;
    if (!Stanje_VALUE) return 0;
    if (unos_VALUE==1) return broj_korisnika[indeks_položaja];
    if (unos_VALUE==2) {
        unsigned char *쪽들=Stanje_VALUE==1?Dozvole_Popis:저장값[indeks_položaja].Dozvole_Popis;
        unsigned dojaviti_COUNT=0; for (unsigned 순번=0; 순번<korisnik_dojaviti_COUNT; 순번++) if(쪽들[순번]) dojaviti_COUNT++;
        return dojaviti_COUNT*4;
    }
    if (unos_VALUE==3) return (uint32_t)보드밀리초()-korisnik_START_TIME[indeks_položaja];
    if (unos_VALUE==4) return 사용자누적시각[indeks_položaja]+(Stanje_VALUE==1?(uint32_t)보드밀리초()-사용자실행시각[indeks_položaja]:0);
    if (unos_VALUE==5) return INDEX/4<sizeof(korisnik_naredba_naziv[0])?korisnik_naredba_naziv[indeks_položaja][INDEX/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t unos_COUNT) {
    if (Aktivan || unos_COUNT > 8) return (uint32_t)-22;
    전달인수개수 = unos_COUNT;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t LOOKUP_INDEX, uintptr_t redovno_položaj, uintptr_t bajt_podaci) {
    if (Aktivan || LOOKUP_INDEX >= 전달인수개수 || redovno_položaj >= 255 || redovno_položaj != 전달인수길이[LOOKUP_INDEX] || !bajt_podaci || bajt_podaci > 255)
        return (uint32_t)-22;
    전달인수[LOOKUP_INDEX][redovno_položaj] = bajt_podaci;
    전달인수길이[LOOKUP_INDEX] = redovno_položaj + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Sat_VALUE(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Stani_TIMEOUT(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    stroj_registar(IRQ_distributer + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void START_TIMEOUT(void) {
    uint64_t 간격 = FREQUENCY * 2, omogućiti = 1;
    rok_za_dovršetak_TIME = Sat_VALUE() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(omogućiti) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned podatkovni_blok = 0; podatkovni_blok < 4; podatkovni_blok++) {
        korijen_adresa[podatkovni_blok] = (uintptr_t)가운데[podatkovni_blok] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t adresa = ((uintptr_t)podatkovni_blok << 30) | ((uintptr_t)순번 << 21);
            가운데[podatkovni_blok][순번] = adresa | 1 | pristup_marker | korisnik_ne_Izvrši;
            if (adresa >= 0xfc000000ul) 가운데[podatkovni_blok][순번] |= ne_Izvrši_dozvola; // Device-nGnRnE
            else 가운데[podatkovni_blok][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned SECOND_VALUE = 0; SECOND_VALUE < korisnik_dojaviti_COUNT / 512; SECOND_VALUE++)
        가운데[0][(korisnik_BASE >> 21) + SECOND_VALUE] = (uintptr_t)(dojaviti_Popis + SECOND_VALUE * 512) | 3;
    for (unsigned 순번 = 0; 순번 < korisnik_dojaviti_COUNT; 순번++) dojaviti_Popis[순번] = (korisnik_BASE + 순번 * veličina_stranice) | jezgra_sustava_dojaviti;
    uint64_t Memorija_atribut_registar = 0x4400, adresa_Prevođenje_kontrola = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Memorija_atribut_registar), "r"(adresa_Prevođenje_kontrola), "r"((uintptr_t)korijen_adresa) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t plutajući_p_Stanje = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(plutajući_p_Stanje) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    Stani_TIMEOUT();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 unos_p_VALUE 때만 Dopusti_VALUE.
    stroj_registar(IRQ_distributer) = 0;
    stroj_registar(IRQ_distributer + 0x180) = 0xffffffff;
    stroj_registar(IRQ_distributer + 0x80) = 0xffffffff;
    stroj_registar(IRQ_distributer + 0x280) = 1u << 30;
    stroj_registar(IRQ_distributer + 0x41c) = 0x80808080;
    stroj_registar(IRQ_distributer + 0x100) = 1u << 30;
    stroj_registar(IRQ_CPU_sučelje + 4) = 0xff;
    stroj_registar(IRQ_CPU_sučelje + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 수 있다.
    int Sigurnost = (stroj_registar(IRQ_distributer + 4) & (1u << 10)) != 0;
    stroj_registar(IRQ_distributer) = Sigurnost ? 1 : 3;
    stroj_registar(IRQ_CPU_sučelje) = Sigurnost ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t TYPE_područje, stroj_TYPE; uint32_t broj_verzije;
    uint64_t unos_p, program_Zaglavlje_pomak, zaglavlje_sekcije_pomak; uint32_t konfiguracija_Pozadinski_pametni_servis_za_transfer;
    uint16_t 실행머리크기, program_Zaglavlje_unos_promijeniti_veličinu, program_Zaglavlje_COUNT, zaglavlje_sekcije_unos_promijeniti_veličinu, zaglavlje_sekcije_COUNT, sekcija_naziv_tablica_INDEX;
} 실행파일머리;
typedef struct { uint32_t TYPE_područje, konfiguracija_Pozadinski_pametni_servis_za_transfer; uint64_t pomak_VALUE, adresa, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(korisnik_kadar) == 272, "exception assembly layout");
static int 포함된범위(uint64_t pomak_VALUE, uint64_t Veličina, uint64_t završiti_razgovor_pomak) {
    return pomak_VALUE <= završiti_razgovor_pomak && Veličina <= završiti_razgovor_pomak - pomak_VALUE;
}
static int 부가정보검사(const unsigned char *podaci_položaj, size_t Veličina) {
    size_t redovno_položaj = 0;
    while (포함된범위(redovno_položaj, 12, Veličina)) {
        uint32_t 낱말들[3]; memcpy(낱말들, podaci_položaj + redovno_položaj, 12); redovno_položaj += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(redovno_položaj, 이름영역크기, Veličina) || !포함된범위(redovno_položaj + 이름영역크기, 설명크기, Veličina)) return 0;
        const unsigned char Ime[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Ime) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Ime); 순번++) if (podaci_položaj[redovno_položaj + 순번] != Ime[순번]) 일치 = 0;
        uint32_t broj_verzije = 0;
        if (일치) memcpy(&broj_verzije, podaci_položaj + redovno_položaj + 이름영역크기, 4);
        if (일치 && broj_verzije == 1) return 1;
        redovno_položaj += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *podaci, size_t Veličina, int 리눅스방식) {
    if (Veličina < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, podaci, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.TYPE_područje != 2 || 실행머리.stroj_TYPE != 183 || 실행머리.broj_verzije != 1 || 실행머리.konfiguracija_Pozadinski_pametni_servis_za_transfer || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.program_Zaglavlje_unos_promijeniti_veličinu != sizeof(실행파일구획) || !실행머리.program_Zaglavlje_COUNT || 실행머리.program_Zaglavlje_COUNT > 16 ||
        실행머리.program_Zaglavlje_pomak < sizeof(실행머리) || !포함된범위(실행머리.program_Zaglavlje_pomak, (uint64_t)실행머리.program_Zaglavlje_COUNT * sizeof(실행파일구획), Veličina)) return 사용자실행파일오류;
    uint8_t 사용량[(korisnik_IMAGE_završiti_razgovor - korisnik_BASE) / veličina_stranice] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.program_Zaglavlje_COUNT; 순번++) {
        실행파일구획 podaci_položaj; memcpy(&podaci_položaj, podaci + 실행머리.program_Zaglavlje_pomak + 순번 * sizeof(podaci_položaj), sizeof(podaci_položaj));
        if (podaci_položaj.TYPE_područje == 4) {
            if (!포함된범위(podaci_položaj.pomak_VALUE, podaci_položaj.파일영역크기, Veličina)) return 사용자실행파일오류;
            if (부가정보검사(podaci + podaci_položaj.pomak_VALUE, podaci_položaj.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (podaci_položaj.TYPE_područje == 0 || podaci_položaj.TYPE_područje == 6 || (podaci_položaj.TYPE_područje == 0x6474e551 && !(podaci_položaj.konfiguracija_Pozadinski_pametni_servis_za_transfer & 1))) continue;
        if (podaci_položaj.TYPE_područje != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!podaci_položaj.기억영역크기) continue;
        if (podaci_položaj.konfiguracija_Pozadinski_pametni_servis_za_transfer & ~7u || !(podaci_položaj.konfiguracija_Pozadinski_pametni_servis_za_transfer & 4) || (podaci_položaj.konfiguracija_Pozadinski_pametni_servis_za_transfer & 3) == 3 || podaci_položaj.파일영역크기 > podaci_položaj.기억영역크기 ||
            (podaci_položaj.파일영역크기 && !포함된범위(podaci_položaj.pomak_VALUE, podaci_položaj.파일영역크기, Veličina)) || podaci_položaj.adresa < korisnik_BASE ||
            !포함된범위(podaci_položaj.adresa, podaci_položaj.기억영역크기, korisnik_IMAGE_završiti_razgovor) ||
            (!리눅스방식 && ((podaci_položaj.adresa & (veličina_stranice - 1)) || (podaci_položaj.pomak_VALUE & (veličina_stranice - 1)) || podaci_položaj.맞춤 != veličina_stranice)) ||
            (리눅스방식 && (((podaci_položaj.adresa ^ podaci_položaj.pomak_VALUE) & (veličina_stranice - 1)) || !podaci_položaj.맞춤 ||
                (podaci_položaj.맞춤 & (podaci_položaj.맞춤 - 1)) || podaci_položaj.맞춤 > 0x200000 || ((podaci_položaj.adresa ^ podaci_položaj.pomak_VALUE) & (podaci_položaj.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (podaci_položaj.adresa - korisnik_BASE) / veličina_stranice;
        unsigned unos_COUNT = ((podaci_položaj.adresa & (veličina_stranice - 1)) + podaci_položaj.기억영역크기 + veličina_stranice - 1) / veličina_stranice;
        for (unsigned dojaviti_VALUE = 첫항목; dojaviti_VALUE < 첫항목 + unos_COUNT; dojaviti_VALUE++) {
            if (사용량[dojaviti_VALUE]) return 사용자실행파일오류;
            사용량[dojaviti_VALUE] = 1;
        }
        if ((podaci_položaj.konfiguracija_Pozadinski_pametni_servis_za_transfer & 1) && 실행머리.unos_p >= podaci_položaj.adresa && 실행머리.unos_p < podaci_položaj.adresa + podaci_položaj.파일영역크기 && !(실행머리.unos_p & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *podaci, size_t Veličina) { return 실행파일검사(podaci, Veličina, 0); }
static void raspored_stranice(uintptr_t adresa, uint64_t konfiguracija_Pozadinski_pametni_servis_za_transfer, unsigned dozvole) {
    unsigned LOOKUP_INDEX = (adresa - korisnik_BASE) / veličina_stranice;
    dojaviti_Popis[LOOKUP_INDEX] = adresa | konfiguracija_Pozadinski_pametni_servis_za_transfer;
    Dozvole_Popis[LOOKUP_INDEX] = dozvole;
}
static int korisnik_raspon(uintptr_t adresa, size_t unos_COUNT, int 쓰는중) {
    if (adresa < korisnik_BASE || !포함된범위(adresa, unos_COUNT, korisnik_završiti_razgovor)) return 0;
    if (!unos_COUNT) return 1;
    unsigned 첫항목 = (adresa - korisnik_BASE) / veličina_stranice, 마지막 = (adresa + unos_COUNT - 1 - korisnik_BASE) / veličina_stranice;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(Dozvole_Popis[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int instanca_put(uintptr_t adresa, char *PUTANJA) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!korisnik_raspon(adresa, 1, 0)) return -14;
        PUTANJA[순번] = *(const char *)adresa++;
        if (!PUTANJA[순번]) return 0;
    }
    return -36;
}
static intptr_t jezgra_sustava_KR(intptr_t REZULTAT) { return REZULTAT < 0 ? -broj_pogreške : REZULTAT; }
static int 대응파일기술자(uint64_t Datoteka_ustroj) { return Datoteka_ustroj >= 3 && Datoteka_ustroj < 19 ? Datoteka_Popis[Datoteka_ustroj - 3] : -1; }
static int 통신끝점소유(uint64_t Datoteka_ustroj) { return Datoteka_ustroj >= 32 && Datoteka_ustroj < 56 && 통신끝점들[Datoteka_ustroj - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t 길이, struct pk_sockaddr_in *adresa) {
    if (길이 != sizeof(*adresa)) return -22;
    if (!korisnik_raspon(가리킴값, 길이, 0)) return -14;
    memcpy(adresa, (const void *)가리킴값, sizeof(*adresa));
    return adresa->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t 길이포인터, pk_socklen_t *međuspremnik_kapacitet) {
    if (!korisnik_raspon(길이포인터, sizeof(*međuspremnik_kapacitet), 1)) return -14;
    memcpy(međuspremnik_kapacitet, (const void *)길이포인터, sizeof(*međuspremnik_kapacitet));
    if (*međuspremnik_kapacitet > sizeof(struct pk_sockaddr_in)) *međuspremnik_kapacitet = sizeof(struct pk_sockaddr_in);
    if (*međuspremnik_kapacitet && !korisnik_raspon(가리킴값, *međuspremnik_kapacitet, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t 길이포인터, pk_socklen_t međuspremnik_kapacitet, int adresa, int broj_priključka) {
    struct pk_sockaddr_in VALUE; memset(&VALUE, 0, sizeof(VALUE));
    VALUE.sin_family = AF_INET; VALUE.sin_port = pk_htons(broj_priključka); VALUE.sin_addr.s_addr = pk_htonl(adresa);
    if (međuspremnik_kapacitet) memcpy((void *)가리킴값, &VALUE, međuspremnik_kapacitet);
    pk_socklen_t 길이 = sizeof(VALUE); memcpy((void *)길이포인터, &길이, sizeof(길이));
}
extern uintptr_t pano_kanal(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(korisnik_kadar *Datoteka_unos) {
    uintptr_t 첫째값 = Datoteka_unos->registar_podaci[0], SECOND_VALUE = Datoteka_unos->registar_podaci[1], kodna_točka = Datoteka_unos->registar_podaci[2];
    char PUTANJA[65];
    int Datoteka_ustroj, REZULTAT;
    switch (Datoteka_unos->registar_podaci[8]) {
    case 0: return 1; // vlastiti ABI 버전
    case 1: // write: pokazivač 전체를 검사한 TRAG_VALUE Izlaz/Datoteka promijeniti_VALUE
        if (kodna_točka > 65536) return -22;
        if (!korisnik_raspon(SECOND_VALUE, kodna_točka, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=Sat_VALUE();
            for (size_t 순번 = 0; 순번 < kodna_točka; 순번++) pano_kanal(첫째값, ((const unsigned char *)SECOND_VALUE)[순번]);
            /* 큰 tty를 그린 jezgra_sustava_VALUE 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(대화형){
                rok_za_dovršetak_TIME+=Sat_VALUE()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(rok_za_dovršetak_TIME) : "memory");
            }
            return kodna_točka;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t artikl_COUNT=kodna_točka>512?512:kodna_točka;for(size_t 순번=0;순번<artikl_COUNT;순번++)자바전문넣기(순번,((const unsigned char *)SECOND_VALUE)[순번]);return 자바흐름쓰기(첫째값,artikl_COUNT);
        }
        Datoteka_ustroj = 대응파일기술자(첫째값); if (Datoteka_ustroj < 0) return -9;
        return jezgra_sustava_KR(pk_write(Datoteka_ustroj, (const void *)SECOND_VALUE, kodna_točka));
    case 2:
        if (kodna_točka > 65536) return -22;
        if (!korisnik_raspon(SECOND_VALUE, kodna_točka, 1)) return -14;
        if (첫째값 == 0) {
            size_t artikl_COUNT = 0;
            while (artikl_COUNT < kodna_točka) {
                int znak_VALUE = (int32_t)보드글자읽기(); if (znak_VALUE == -2) return artikl_COUNT; if (znak_VALUE < 0) break;
                ((unsigned char *)SECOND_VALUE)[artikl_COUNT++] = znak_VALUE;
            }
            return artikl_COUNT ? (intptr_t)artikl_COUNT : (kodna_točka ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            REZULTAT=자바흐름읽기(첫째값,kodna_točka>512?512:kodna_točka);if(REZULTAT>0)for(int 순번=0;순번<REZULTAT;순번++)((unsigned char *)SECOND_VALUE)[순번]=자바전문얻기(순번);return REZULTAT;
        }
        Datoteka_ustroj = 대응파일기술자(첫째값); if (Datoteka_ustroj < 0) return -9;
        return jezgra_sustava_KR(pk_read(Datoteka_ustroj, (void *)SECOND_VALUE, kodna_točka));
    case 3:
        REZULTAT = instanca_put(첫째값, PUTANJA); if (REZULTAT) return REZULTAT;
        if (SECOND_VALUE > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (Datoteka_Popis[순번] < 0) {
            Datoteka_ustroj = pk_open(PUTANJA, (int)SECOND_VALUE, 0600);
            if (Datoteka_ustroj < 0) return -broj_pogreške;
            Datoteka_Popis[순번] = Datoteka_ustroj; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { REZULTAT = 통신끝점닫기(첫째값); if (!REZULTAT) 통신끝점들[첫째값 - 32] = 0; return REZULTAT; }
        Datoteka_ustroj = 대응파일기술자(첫째값); if (Datoteka_ustroj < 0) return -9;
        REZULTAT = pk_close(Datoteka_ustroj); if (!REZULTAT) Datoteka_Popis[첫째값 - 3] = -1;
        return jezgra_sustava_KR(REZULTAT);
    case 5:
        Datoteka_ustroj = 대응파일기술자(첫째값); if (Datoteka_ustroj < 0) return -9;
        if (kodna_točka > 2) return -22;
        return jezgra_sustava_KR(pk_lseek(Datoteka_ustroj, (int64_t)SECOND_VALUE, kodna_točka));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 korisnik RW/NX 힙, 새로 노출되는 페이지는 0으로 초기화
        if (!첫째값) return 동적기억끝;
        if (첫째값 < korisnik_IMAGE_završiti_razgovor || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + veličina_stranice - 1) & ~(veličina_stranice - 1);
        uintptr_t 새쪽들 = (첫째값 + veličina_stranice - 1) & ~(veličina_stranice - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t podaci_položaj = 이전쪽들; podaci_položaj < 새쪽들; podaci_položaj += veličina_stranice) raspored_stranice(podaci_položaj, jezgra_sustava_dojaviti, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t podaci_položaj = 이전쪽들; podaci_položaj < 새쪽들; podaci_položaj += veličina_stranice) raspored_stranice(podaci_položaj, 사용자읽고쓰기, 3);
        } else {
            for (uintptr_t podaci_položaj = 새쪽들; podaci_položaj < 이전쪽들; podaci_položaj += veličina_stranice) {
                dojaviti_Popis[(podaci_položaj - korisnik_BASE) / veličina_stranice] = 0; Dozvole_Popis[(podaci_položaj - korisnik_BASE) / veličina_stranice] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        Datoteka_ustroj = 대응파일기술자(첫째값); return Datoteka_ustroj < 0 ? -9 : jezgra_sustava_KR(pk_size(Datoteka_ustroj));
    case 10:
        Datoteka_ustroj = 대응파일기술자(첫째값); return Datoteka_ustroj < 0 ? -9 : jezgra_sustava_KR(pk_ftruncate(Datoteka_ustroj, (int64_t)SECOND_VALUE));
    case 11:
        REZULTAT = instanca_put(첫째값, PUTANJA); return REZULTAT ? REZULTAT : jezgra_sustava_KR(pk_unlink(PUTANJA));
    case 12:
        Datoteka_ustroj = 대응파일기술자(첫째값); return Datoteka_ustroj < 0 ? -9 : jezgra_sustava_KR(pk_fsync(Datoteka_ustroj));
    case 13: { // 그래픽 기초 API: korisnik 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = Datoteka_unos->registar_podaci[3], 높이값 = Datoteka_unos->registar_podaci[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SECOND_VALUE > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - SECOND_VALUE) return -22;
        for (uintptr_t 세로좌표 = SECOND_VALUE; 세로좌표 < SECOND_VALUE + 높이값; 세로좌표++) for (uintptr_t koordinata_x = 첫째값; koordinata_x < 첫째값 + 너비값; koordinata_x++) pano_slikovni_element(koordinata_x, 세로좌표, kodna_točka);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=artikl_COUNT; args(index,buffer,capacity)=UTF-8 길이
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (kodna_točka <= 전달인수길이[첫째값]) return -36;
        if (!korisnik_raspon(SECOND_VALUE, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SECOND_VALUE, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;대화형=1;return pano_Terminal(13);}
        if(첫째값==2){대화형=0;return 0;}
        if(첫째값==3)return pano_Terminal(13);
        if(첫째값!=1||!대화형)return -22;
        REZULTAT=(int32_t)보드글자읽기();
        if(REZULTAT==-4096)return REZULTAT;
        START_TIMEOUT();return REZULTAT<0?-11:REZULTAT;
    case 17: { // 유한한 협력 čekaj_VALUE: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t završiti_razgovor_TIME = Sat_VALUE() + FREQUENCY * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Sat_VALUE() < završiti_razgovor_TIME);
        START_TIMEOUT(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 roditeljski_VALUE·빈 폴더를 검사한다.
        if (SECOND_VALUE > 2) return -22;
        REZULTAT = instanca_put(첫째값, PUTANJA); if (REZULTAT) return REZULTAT;
        unsigned 길이 = 0; while (PUTANJA[길이]) 길이++;
        REZULTAT = 자바경로시작(길이); if (REZULTAT < 0) return REZULTAT;
        for (unsigned 순번 = 0; 순번 < 길이; 순번++) 자바경로바이트(순번, (unsigned char)PUTANJA[순번]);
        return SECOND_VALUE == 0 ? 자바항목종류() : SECOND_VALUE == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int znak_VALUE=(int32_t)보드글자읽기();if(znak_VALUE==-4096)return znak_VALUE;if(znak_VALUE>=0)화면누름(vlasnik_objekt,znak_VALUE);START_TIMEOUT();}
        if(첫째값==3&&kodna_točka){if(!자바셸대화형())return -95;대화형=1;pano_Terminal(300);}
        return 화면호출(vlasnik_objekt,첫째값,SECOND_VALUE,kodna_točka,Datoteka_unos->registar_podaci[3],Datoteka_unos->registar_podaci[4],Datoteka_unos->registar_podaci[5]);
    case 21:
        if(kodna_točka>127)return -22;if(!korisnik_raspon(SECOND_VALUE,kodna_točka*sizeof(uint32_t),0))return -14;
        return 화면글(vlasnik_objekt,첫째값,(const uint32_t *)SECOND_VALUE,kodna_točka);
    case 22: // 화면 Veličina upit_VALUE: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SECOND_VALUE==SOCK_STREAM&&(kodna_točka==0||kodna_točka==6))REZULTAT=자바흐름만들기();
        else if(SECOND_VALUE==SOCK_DGRAM&&(kodna_točka==0||kodna_točka==IPPROTO_UDP))REZULTAT=자바전문만들기(첫째값,SECOND_VALUE,kodna_točka);
        else return -93;
        if (REZULTAT >= 32 && REZULTAT < 56) 통신끝점들[REZULTAT - 32] = 1;
        return REZULTAT;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in adresa;
        REZULTAT = 주소입력(SECOND_VALUE, kodna_točka, &adresa); if (REZULTAT) return REZULTAT;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(adresa.sin_addr.s_addr),pk_htons(adresa.sin_port)):자바전문묶기(첫째값, pk_htonl(adresa.sin_addr.s_addr), pk_htons(adresa.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Datoteka_unos->registar_podaci[3]) return -95;
        if (kodna_točka > 512) return -90;
        if (kodna_točka && !korisnik_raspon(SECOND_VALUE, kodna_točka, 0)) return -14;
        struct pk_sockaddr_in adresa;
        REZULTAT = 주소입력(Datoteka_unos->registar_podaci[4], Datoteka_unos->registar_podaci[5], &adresa); if (REZULTAT) return REZULTAT;
        for (unsigned 순번 = 0; 순번 < kodna_točka; 순번++) 자바전문넣기(순번, ((const unsigned char *)SECOND_VALUE)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(adresa.sin_addr.s_addr), pk_htons(adresa.sin_port), kodna_točka);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Datoteka_unos->registar_podaci[3]) return -95;
        if (kodna_točka > 512) return -90;
        if (kodna_točka && !korisnik_raspon(SECOND_VALUE, kodna_točka, 1)) return -14;
        pk_socklen_t međuspremnik_kapacitet = 0;
        if (Datoteka_unos->registar_podaci[4]) { REZULTAT = 주소출력검사(Datoteka_unos->registar_podaci[4], Datoteka_unos->registar_podaci[5], &međuspremnik_kapacitet); if (REZULTAT) return REZULTAT; }
        REZULTAT = 자바전문받기(첫째값, kodna_točka); if (REZULTAT < 0) return REZULTAT;
        for (int 순번 = 0; 순번 < REZULTAT; 순번++) ((unsigned char *)SECOND_VALUE)[순번] = 자바전문얻기(순번);
        if (Datoteka_unos->registar_podaci[4]) 주소출력(Datoteka_unos->registar_podaci[4], Datoteka_unos->registar_podaci[5], međuspremnik_kapacitet, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return REZULTAT;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t međuspremnik_kapacitet;
        REZULTAT = 주소출력검사(SECOND_VALUE, kodna_točka, &međuspremnik_kapacitet); if (REZULTAT) return REZULTAT;
        주소출력(SECOND_VALUE,kodna_točka,međuspremnik_kapacitet,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in adresa;
        REZULTAT=주소입력(SECOND_VALUE,kodna_točka,&adresa);if(REZULTAT)return REZULTAT;
        return 자바흐름연결(첫째값,pk_htonl(adresa.sin_addr.s_addr),pk_htons(adresa.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,SECOND_VALUE):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(SECOND_VALUE||kodna_točka)return -95;REZULTAT=자바흐름연결받기(첫째값);if(REZULTAT>=40&&REZULTAT<56)통신끝점들[REZULTAT-32]=1;return REZULTAT;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(korisnik_kadar *Datoteka_unos) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(Datoteka_unos) : 자체체계호출(Datoteka_unos);
}
static void vratiti_jezgra_sustava(korisnik_kadar *Datoteka_unos, int REZULTAT) {
    Stani_TIMEOUT();
    Datoteka_unos->registar_podaci[0] = (uint64_t)(int64_t)REZULTAT;
    Datoteka_unos->naredba_položaj = (uintptr_t)korisnik_vratiti;
    Datoteka_unos->Stanje_kod = 0x3c5; // EL1h, DAIF masked
}
int korisnik_iznimka(korisnik_kadar *Datoteka_unos, unsigned INTERCEPT) {
    if (!Aktivan || (Datoteka_unos->Stanje_kod & 15) != 0) return 0;
    if (INTERCEPT) {
        uint32_t potvrda_VALUE = stroj_registar(IRQ_CPU_sučelje + 0xc), identifikator_VALUE = potvrda_VALUE & 1023;
        if (identifikator_VALUE == 30) { vratiti_jezgra_sustava(Datoteka_unos, korisnik_TIMEOUT); stroj_registar(IRQ_CPU_sučelje + 0x10) = potvrda_VALUE; return 1; }
        if (identifikator_VALUE < 1020) stroj_registar(IRQ_CPU_sučelje + 0x10) = potvrda_VALUE;
        return 1;
    }
    uint64_t iznimka_Stanje; __asm__ volatile("mrs %0, esr_el1" : "=r"(iznimka_Stanje));
    if (Sat_VALUE() >= rok_za_dovršetak_TIME) { vratiti_jezgra_sustava(Datoteka_unos, korisnik_TIMEOUT); return 1; }
    unsigned iznimka_područje = iznimka_Stanje >> 26;
    if (iznimka_područje == 0x15 && (iznimka_Stanje & 0xffff) == 0) {
        if (리눅스규약 ? Datoteka_unos->registar_podaci[8] == 93 || Datoteka_unos->registar_podaci[8] == 94 : Datoteka_unos->registar_podaci[8] == 6) vratiti_jezgra_sustava(Datoteka_unos, (int)(Datoteka_unos->registar_podaci[0] & 255));
        else {
            intptr_t REZULTAT=체계호출(Datoteka_unos);
            if(REZULTAT==-4096&&대화형){
                저장값[vlasnik_objekt].실행틀=*Datoteka_unos;저장값[vlasnik_objekt].실행틀.naredba_položaj-=4;
                사용자실수보관(저장값[vlasnik_objekt].plutajući_p_Stanje);vratiti_jezgra_sustava(Datoteka_unos,사용자중단됨);
            }else Datoteka_unos->registar_podaci[0]=(uint64_t)REZULTAT;
        }
    } else vratiti_jezgra_sustava(Datoteka_unos, iznimka_područje == 0x24 ? korisnik_podaci_pogreška : iznimka_područje == 0x20 ? 사용자실행오류 : 사용자잘못된명령);
    return 1;
}

// 생성된 const ELF Grupa_VALUE: 실행은 반드시 program_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *podaci; size_t Veličina; unsigned 전달값; } program;
#include "programs.h"
static void *snimka(unsigned indeks_položaja){return (void *)(0x04000000ul+indeks_položaja*(korisnik_završiti_razgovor-korisnik_BASE));}
static int Završi_program(int REZULTAT){
    사용자누적시각[vlasnik_objekt]+=(uint32_t)보드밀리초()-사용자실행시각[vlasnik_objekt];
    Stani_TIMEOUT();Aktivan=0;
    if(REZULTAT==사용자중단됨){
        저장된작업 *niz_podaci=&저장값[vlasnik_objekt];niz_podaci->멈춤상태=1;niz_podaci->대화형=대화형;niz_podaci->리눅스규약=리눅스규약;niz_podaci->동적기억공간=동적기억끝;niz_podaci->인수개수=전달인수개수;
        memcpy(niz_podaci->Dozvole_Popis,Dozvole_Popis,sizeof(Dozvole_Popis));memcpy(niz_podaci->Datoteka_Popis,Datoteka_Popis,sizeof(Datoteka_Popis));memcpy(niz_podaci->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(niz_podaci->argument_ARRAY,전달인수,sizeof(전달인수));memcpy(niz_podaci->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<korisnik_dojaviti_COUNT;순번++)if(Dozvole_Popis[순번])memcpy((unsigned char *)snimka(vlasnik_objekt)+순번*veličina_stranice,(void *)(korisnik_BASE+순번*veličina_stranice),veličina_stranice);
    }else{
        저장값[vlasnik_objekt].멈춤상태=0;화면초기화(vlasnik_objekt);
        for(unsigned 순번=0;순번<16;순번++)if(Datoteka_Popis[순번]>=0)pk_close(Datoteka_Popis[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<korisnik_dojaviti_COUNT;순번++){dojaviti_Popis[순번]=0;Dozvole_Popis[순번]=0;}변환표맞추기();return REZULTAT;
}
uintptr_t pano_korisnička_kontrola(uintptr_t Aktivnost){
    unsigned indeks_položaja=Aktivnost&15;if(indeks_položaja>=4||Aktivan)return (uint32_t)-22;
    저장된작업 *niz_podaci=&저장값[indeks_položaja];
    if(Aktivnost>=32){if(niz_podaci->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(niz_podaci->Datoteka_Popis[순번]>=0)pk_close(niz_podaci->Datoteka_Popis[순번]);for(unsigned 순번=0;순번<24;순번++)if(niz_podaci->통신끝점들[순번])통신끝점닫기(순번+32);}niz_podaci->멈춤상태=0;화면초기화(indeks_položaja);return 0;}
    if(Aktivnost>=16)return niz_podaci->멈춤상태;
    if(!niz_podaci->멈춤상태)return (uint32_t)-22;
    vlasnik_objekt=indeks_položaja;대화형=niz_podaci->대화형;리눅스규약=niz_podaci->리눅스규약;동적기억끝=niz_podaci->동적기억공간;전달인수개수=niz_podaci->인수개수;
    memcpy(Datoteka_Popis,niz_podaci->Datoteka_Popis,sizeof(Datoteka_Popis));memcpy(통신끝점들,niz_podaci->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,niz_podaci->argument_ARRAY,sizeof(전달인수));memcpy(전달인수길이,niz_podaci->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<korisnik_dojaviti_COUNT;순번++)dojaviti_Popis[순번]=(korisnik_BASE+순번*veličina_stranice)|jezgra_sustava_dojaviti;변환표맞추기();
    memset((void *)korisnik_BASE,0,korisnik_završiti_razgovor-korisnik_BASE);
    for(unsigned 순번=0;순번<korisnik_dojaviti_COUNT;순번++)if(niz_podaci->Dozvole_Popis[순번])memcpy((void *)(korisnik_BASE+순번*veličina_stranice),(unsigned char *)snimka(indeks_položaja)+순번*veličina_stranice,veličina_stranice);
    memcpy(Dozvole_Popis,niz_podaci->Dozvole_Popis,sizeof(Dozvole_Popis));
    for(unsigned 순번=0;순번<korisnik_dojaviti_COUNT;순번++){unsigned podaci_položaj=Dozvole_Popis[순번];dojaviti_Popis[순번]=podaci_položaj?(korisnik_BASE+순번*veličina_stranice)|(podaci_položaj==3?사용자읽고쓰기:podaci_položaj==5?사용자읽고실행:korisnik_samo_za_čitanje):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");Aktivan=1;niz_podaci->멈춤상태=0;START_TIMEOUT();
    사용자실행시각[vlasnik_objekt]=보드밀리초();
    return (uint32_t)Završi_program(korisnik_nastaviti(&niz_podaci->실행틀,niz_podaci->plutajući_p_Stanje));
}
static int izvršiti_program(const unsigned char *podaci, size_t Veličina, unsigned 전달값, int 리눅스방식, const char *Ime) {
    if (Aktivan) return -16;
    vlasnik_objekt=pano_Terminal(11);if(vlasnik_objekt<0||vlasnik_objekt>3||저장값[vlasnik_objekt].멈춤상태)return -16;대화형=0;
    int 유효함 = 실행파일검사(podaci, Veličina, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned naziv_INDEX=0;
    while (*Ime && naziv_INDEX<31) korisnik_naredba_naziv[vlasnik_objekt][naziv_INDEX++]=(unsigned char)*Ime++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (naziv_INDEX) korisnik_naredba_naziv[vlasnik_objekt][naziv_INDEX++]=' ';
        for (unsigned indeks_položaja=0; indeks_položaja<전달인수길이[0]; indeks_položaja++) korisnik_naredba_naziv[vlasnik_objekt][naziv_INDEX++]=전달인수[0][indeks_položaja];
    }
    korisnik_naredba_naziv[vlasnik_objekt][naziv_INDEX]=0; broj_korisnika[vlasnik_objekt]=Dalje_broj_korisnika++;
    if (Dalje_broj_korisnika>0x7fffffffu) Dalje_broj_korisnika=10;
    korisnik_START_TIME[vlasnik_objekt]=보드밀리초(); 사용자누적시각[vlasnik_objekt]=0;
    for (unsigned 순번 = 0; 순번 < korisnik_dojaviti_COUNT; 순번++) dojaviti_Popis[순번] = (korisnik_BASE + 순번 * veličina_stranice) | jezgra_sustava_dojaviti;
    변환표맞추기();
    memset((void *)korisnik_BASE, 0, korisnik_završiti_razgovor - korisnik_BASE);
    memset(Dozvole_Popis, 0, sizeof(Dozvole_Popis));
    실행파일머리 실행머리; memcpy(&실행머리, podaci, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.program_Zaglavlje_COUNT; 순번++) {
        실행파일구획 podaci_položaj; memcpy(&podaci_položaj, podaci + 실행머리.program_Zaglavlje_pomak + 순번 * sizeof(podaci_položaj), sizeof(podaci_položaj));
        if (podaci_položaj.TYPE_područje != 1 || !podaci_položaj.기억영역크기) continue;
        if (podaci_položaj.파일영역크기) memcpy((void *)(uintptr_t)podaci_položaj.adresa, podaci + podaci_položaj.pomak_VALUE, podaci_položaj.파일영역크기);
        for (uintptr_t redovno_položaj = podaci_položaj.adresa & ~(veličina_stranice - 1); redovno_položaj < podaci_položaj.adresa + podaci_položaj.기억영역크기; redovno_položaj += veličina_stranice) {
            Dozvole_Popis[(redovno_položaj - korisnik_BASE) / veličina_stranice] = (podaci_položaj.konfiguracija_Pozadinski_pametni_servis_za_transfer & 2) ? 3 : ((podaci_položaj.konfiguracija_Pozadinski_pametni_servis_za_transfer & 1) ? 5 : 1);
        }
    }
    for (uintptr_t redovno_položaj = korisnik_hrpa_adresa; redovno_položaj < korisnik_završiti_razgovor; redovno_položaj += veličina_stranice) Dozvole_Popis[(redovno_položaj - korisnik_BASE) / veličina_stranice] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.unos_p) : korisnik_završiti_razgovor;
    for (unsigned 순번 = 0; 순번 < korisnik_dojaviti_COUNT; 순번++) {
        unsigned dozvole = Dozvole_Popis[순번];
        dojaviti_Popis[순번] = dozvole ? (korisnik_BASE + 순번 * veličina_stranice) | (dozvole == 3 ? 사용자읽고쓰기 : dozvole == 5 ? 사용자읽고실행 : korisnik_samo_za_čitanje) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) Datoteka_Popis[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = korisnik_IMAGE_završiti_razgovor;
    Aktivan = 1; START_TIMEOUT();
    사용자실행시각[vlasnik_objekt]=보드밀리초();
    int REZULTAT = korisnik_unijeti(실행머리.unos_p, 초기쌓임공간, 전달값);
    return Završi_program(REZULTAT);
}
uintptr_t pano_korisnik_izvršiti(uintptr_t LOOKUP_INDEX) {
    if (LOOKUP_INDEX >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Ime=LOOKUP_INDEX==10?"javac":LOOKUP_INDEX==11?"java":LOOKUP_INDEX==12?"python":LOOKUP_INDEX==13?"vi":LOOKUP_INDEX==14?"jar":LOOKUP_INDEX==15?"cc":LOOKUP_INDEX==16?"jaot":"ELF";
    return (uint32_t)izvršiti_program(실행항목들[LOOKUP_INDEX].podaci, 실행항목들[LOOKUP_INDEX].Veličina, 실행항목들[LOOKUP_INDEX].전달값, 0, Ime);
}
static uintptr_t Izvrši_Datoteka(int 리눅스방식) {
    static unsigned char IMAGE[16384];
    if (Aktivan || !전달인수개수) return (uint32_t)-22;
    int Datoteka_ustroj = pk_open((const char *)전달인수[0], samo_za_čitanje_VALUE, 0);
    if (Datoteka_ustroj < 0) return (uint32_t)-broj_pogreške;
    int Veličina = pk_size(Datoteka_ustroj);
    if (Veličina < 0 || (unsigned)Veličina > sizeof(IMAGE)) { pk_close(Datoteka_ustroj); return (uint32_t)-27; }
    int RECEIVED_COUNT = pk_read(Datoteka_ustroj, IMAGE, Veličina); pk_close(Datoteka_ustroj);
    if (RECEIVED_COUNT != Veličina) return (uint32_t)-5;
    return (uint32_t)izvršiti_program(IMAGE, Veličina, 0, 리눅스방식, "");
}
uintptr_t pano_korisnik_Datoteka(void) { return Izvrši_Datoteka(0); }
uintptr_t 보드사용자리눅스파일(void) { return Izvrši_Datoteka(1); }
uintptr_t pano_korisnik_potvrditi(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].podaci, 잘못된실행항목들[순번].Veličina) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
