#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 Izvrši_komanda računar sloj_VALUE. Datoteka podaci/정책은 기존 AOT Java 커널에 위임한다.
#include "korisnik.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../Mreža_stek/Mreža_stek.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define računar_registar(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_distributer 0xff841000ul
#define IRQ_CPU_interfejs 0xff842000ul
#define veličina_stranice 4096ul
#define pristup_označivač (1ul << 10)
#define ne_Izvrši_dozvola (1ul << 53)
#define korisnik_ne_Izvrši (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | pristup_označivač)
#define jezgro_stranica (3ul | 보통기억 | ne_Izvrši_dozvola | korisnik_ne_Izvrši)
#define korisnik_za_čitanje_pisanje (3ul | 보통기억 | (1ul << 6) | ne_Izvrši_dozvola | korisnik_ne_Izvrši)
#define korisnik_samo_za_čitanje (3ul | 보통기억 | (3ul << 6) | ne_Izvrši_dozvola | korisnik_ne_Izvrši)
#define 사용자읽고실행 (3ul | 보통기억 | (3ul << 6) | ne_Izvrši_dozvola)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t Tabla_piksel(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t Tabla_Terminal(uintptr_t);
extern int Terminal_na_čekanju(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int korisnik_rezime(korisnik_kadar *,void *);
extern void 사용자실수보관(void *);
extern int korisnik_uneti(uintptr_t stavka_p, uintptr_t stek_Skladište, uintptr_t 전달값);
extern void korisnik_vratiti(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t koren_adresa[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t stranica_Lista[korisnik_stranica_COUNT] __attribute__((aligned(4096)));
static uint8_t Dozvole_Lista[korisnik_stranica_COUNT];
static int Aktivan, Datoteka_Lista[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned Datoteka_pokazivač){return Datoteka_pokazivač<40?자바전문닫기(Datoteka_pokazivač):자바흐름닫기(Datoteka_pokazivač);}
static uint64_t FREQUENCY, krajnji_rok_TIME;
static uintptr_t 동적기억끝;
// jezgro_VALUE 셸이 준비한 UTF-8 인수. EL0에는 instanca_VALUE 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,대화형,리눅스규약,Datoteka_Lista[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char argument_niz[8][256],Dozvole_Lista[korisnik_stranica_COUNT];
    uintptr_t 동적기억공간; korisnik_kadar 실행틀;
    unsigned char plutajući_p_Status[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int vlasnik_objekat,대화형;
static uint32_t broj_korisnika[4], korisnik_START_TIME[4], 사용자누적시각[4], 사용자실행시각[4], Dalje_broj_korisnika=10;
static unsigned char korisnik_komanda_ime[4][288];
uint32_t 사용자상태읽기(unsigned stavka_VALUE, unsigned INDEX) {
    unsigned indeks_pozicije=INDEX&3;
    int Status_VALUE=(Aktivan && vlasnik_objekat==(int)indeks_pozicije) ? 1 : 저장값[indeks_pozicije].멈춤상태 ? 2 : 0;
    if (stavka_VALUE==0) return Status_VALUE;
    if (!Status_VALUE) return 0;
    if (stavka_VALUE==1) return broj_korisnika[indeks_pozicije];
    if (stavka_VALUE==2) {
        unsigned char *쪽들=Status_VALUE==1?Dozvole_Lista:저장값[indeks_pozicije].Dozvole_Lista;
        unsigned stranica_COUNT=0; for (unsigned 순번=0; 순번<korisnik_stranica_COUNT; 순번++) if(쪽들[순번]) stranica_COUNT++;
        return stranica_COUNT*4;
    }
    if (stavka_VALUE==3) return (uint32_t)보드밀리초()-korisnik_START_TIME[indeks_pozicije];
    if (stavka_VALUE==4) return 사용자누적시각[indeks_pozicije]+(Status_VALUE==1?(uint32_t)보드밀리초()-사용자실행시각[indeks_pozicije]:0);
    if (stavka_VALUE==5) return INDEX/4<sizeof(korisnik_komanda_ime[0])?korisnik_komanda_ime[indeks_pozicije][INDEX/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t stavka_COUNT_8f7753a1) {
    if (Aktivan || stavka_COUNT_8f7753a1 > 8) return (uint32_t)-22;
    전달인수개수 = stavka_COUNT_8f7753a1;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t LOOKUP_INDEX, uintptr_t aktuelno_pozicija, uintptr_t bajt_podaci) {
    if (Aktivan || LOOKUP_INDEX >= 전달인수개수 || aktuelno_pozicija >= 255 || aktuelno_pozicija != 전달인수길이[LOOKUP_INDEX] || !bajt_podaci || bajt_podaci > 255)
        return (uint32_t)-22;
    전달인수[LOOKUP_INDEX][aktuelno_pozicija] = bajt_podaci;
    전달인수길이[LOOKUP_INDEX] = aktuelno_pozicija + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Sat_VALUE(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Stani_TIMEOUT(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    računar_registar(IRQ_distributer + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void START_TIMEOUT(void) {
    uint64_t 간격 = FREQUENCY * 2, omogućiti = 1;
    krajnji_rok_TIME = Sat_VALUE() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(omogućiti) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned blok_podataka = 0; blok_podataka < 4; blok_podataka++) {
        koren_adresa[blok_podataka] = (uintptr_t)가운데[blok_podataka] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t adresa = ((uintptr_t)blok_podataka << 30) | ((uintptr_t)순번 << 21);
            가운데[blok_podataka][순번] = adresa | 1 | pristup_označivač | korisnik_ne_Izvrši;
            if (adresa >= 0xfc000000ul) 가운데[blok_podataka][순번] |= ne_Izvrši_dozvola; // Device-nGnRnE
            else 가운데[blok_podataka][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned SECOND_VALUE = 0; SECOND_VALUE < korisnik_stranica_COUNT / 512; SECOND_VALUE++)
        가운데[0][(korisnik_BASE >> 21) + SECOND_VALUE] = (uintptr_t)(stranica_Lista + SECOND_VALUE * 512) | 3;
    for (unsigned 순번 = 0; 순번 < korisnik_stranica_COUNT; 순번++) stranica_Lista[순번] = (korisnik_BASE + 순번 * veličina_stranice) | jezgro_stranica;
    uint64_t Memorija_atribut_registar = 0x4400, adresa_Prevođenje_kontrola = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Memorija_atribut_registar), "r"(adresa_Prevođenje_kontrola), "r"((uintptr_t)koren_adresa) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t plutajući_p_Status = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(plutajući_p_Status) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    Stani_TIMEOUT();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 stavka_p_VALUE 때만 Dozvoli_VALUE.
    računar_registar(IRQ_distributer) = 0;
    računar_registar(IRQ_distributer + 0x180) = 0xffffffff;
    računar_registar(IRQ_distributer + 0x80) = 0xffffffff;
    računar_registar(IRQ_distributer + 0x280) = 1u << 30;
    računar_registar(IRQ_distributer + 0x41c) = 0x80808080;
    računar_registar(IRQ_distributer + 0x100) = 1u << 30;
    računar_registar(IRQ_CPU_interfejs + 4) = 0xff;
    računar_registar(IRQ_CPU_interfejs + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 수 있다.
    int Bezbednost = (računar_registar(IRQ_distributer + 4) & (1u << 10)) != 0;
    računar_registar(IRQ_distributer) = Bezbednost ? 1 : 3;
    računar_registar(IRQ_CPU_interfejs) = Bezbednost ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t tip_oblast, računar_tip; uint32_t broj_verzije;
    uint64_t stavka_p, program_Zaglavlje_Pomak, zaglavlje_odeljka_Pomak; uint32_t konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini;
    uint16_t 실행머리크기, program_Zaglavlje_stavka_promeniti_veličinu, program_Zaglavlje_COUNT, zaglavlje_odeljka_stavka_promeniti_veličinu, zaglavlje_odeljka_COUNT, odeljak_ime_tabela_INDEX;
} 실행파일머리;
typedef struct { uint32_t tip_oblast, konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini; uint64_t Pomak_VALUE, adresa, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(korisnik_kadar) == 272, "exception assembly layout");
static int 포함된범위(uint64_t Pomak_VALUE, uint64_t promeniti_veličinu, uint64_t završiti_razgovor_Pomak) {
    return Pomak_VALUE <= završiti_razgovor_Pomak && promeniti_veličinu <= završiti_razgovor_Pomak - Pomak_VALUE;
}
static int 부가정보검사(const unsigned char *podaci_pozicija, size_t promeniti_veličinu) {
    size_t aktuelno_pozicija = 0;
    while (포함된범위(aktuelno_pozicija, 12, promeniti_veličinu)) {
        uint32_t 낱말들[3]; memcpy(낱말들, podaci_pozicija + aktuelno_pozicija, 12); aktuelno_pozicija += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(aktuelno_pozicija, 이름영역크기, promeniti_veličinu) || !포함된범위(aktuelno_pozicija + 이름영역크기, 설명크기, promeniti_veličinu)) return 0;
        const unsigned char ime[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(ime) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(ime); 순번++) if (podaci_pozicija[aktuelno_pozicija + 순번] != ime[순번]) 일치 = 0;
        uint32_t broj_verzije = 0;
        if (일치) memcpy(&broj_verzije, podaci_pozicija + aktuelno_pozicija + 이름영역크기, 4);
        if (일치 && broj_verzije == 1) return 1;
        aktuelno_pozicija += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *podaci, size_t promeniti_veličinu, int 리눅스방식) {
    if (promeniti_veličinu < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, podaci, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.tip_oblast != 2 || 실행머리.računar_tip != 183 || 실행머리.broj_verzije != 1 || 실행머리.konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.program_Zaglavlje_stavka_promeniti_veličinu != sizeof(실행파일구획) || !실행머리.program_Zaglavlje_COUNT || 실행머리.program_Zaglavlje_COUNT > 16 ||
        실행머리.program_Zaglavlje_Pomak < sizeof(실행머리) || !포함된범위(실행머리.program_Zaglavlje_Pomak, (uint64_t)실행머리.program_Zaglavlje_COUNT * sizeof(실행파일구획), promeniti_veličinu)) return 사용자실행파일오류;
    uint8_t 사용량[(korisnik_IMAGE_završiti_razgovor - korisnik_BASE) / veličina_stranice] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.program_Zaglavlje_COUNT; 순번++) {
        실행파일구획 podaci_pozicija; memcpy(&podaci_pozicija, podaci + 실행머리.program_Zaglavlje_Pomak + 순번 * sizeof(podaci_pozicija), sizeof(podaci_pozicija));
        if (podaci_pozicija.tip_oblast == 4) {
            if (!포함된범위(podaci_pozicija.Pomak_VALUE, podaci_pozicija.파일영역크기, promeniti_veličinu)) return 사용자실행파일오류;
            if (부가정보검사(podaci + podaci_pozicija.Pomak_VALUE, podaci_pozicija.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (podaci_pozicija.tip_oblast == 0 || podaci_pozicija.tip_oblast == 6 || (podaci_pozicija.tip_oblast == 0x6474e551 && !(podaci_pozicija.konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini & 1))) continue;
        if (podaci_pozicija.tip_oblast != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!podaci_pozicija.기억영역크기) continue;
        if (podaci_pozicija.konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini & ~7u || !(podaci_pozicija.konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini & 4) || (podaci_pozicija.konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini & 3) == 3 || podaci_pozicija.파일영역크기 > podaci_pozicija.기억영역크기 ||
            (podaci_pozicija.파일영역크기 && !포함된범위(podaci_pozicija.Pomak_VALUE, podaci_pozicija.파일영역크기, promeniti_veličinu)) || podaci_pozicija.adresa < korisnik_BASE ||
            !포함된범위(podaci_pozicija.adresa, podaci_pozicija.기억영역크기, korisnik_IMAGE_završiti_razgovor) ||
            (!리눅스방식 && ((podaci_pozicija.adresa & (veličina_stranice - 1)) || (podaci_pozicija.Pomak_VALUE & (veličina_stranice - 1)) || podaci_pozicija.맞춤 != veličina_stranice)) ||
            (리눅스방식 && (((podaci_pozicija.adresa ^ podaci_pozicija.Pomak_VALUE) & (veličina_stranice - 1)) || !podaci_pozicija.맞춤 ||
                (podaci_pozicija.맞춤 & (podaci_pozicija.맞춤 - 1)) || podaci_pozicija.맞춤 > 0x200000 || ((podaci_pozicija.adresa ^ podaci_pozicija.Pomak_VALUE) & (podaci_pozicija.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (podaci_pozicija.adresa - korisnik_BASE) / veličina_stranice;
        unsigned stavka_COUNT_8f7753a1 = ((podaci_pozicija.adresa & (veličina_stranice - 1)) + podaci_pozicija.기억영역크기 + veličina_stranice - 1) / veličina_stranice;
        for (unsigned stranica_VALUE = 첫항목; stranica_VALUE < 첫항목 + stavka_COUNT_8f7753a1; stranica_VALUE++) {
            if (사용량[stranica_VALUE]) return 사용자실행파일오류;
            사용량[stranica_VALUE] = 1;
        }
        if ((podaci_pozicija.konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini & 1) && 실행머리.stavka_p >= podaci_pozicija.adresa && 실행머리.stavka_p < podaci_pozicija.adresa + podaci_pozicija.파일영역크기 && !(실행머리.stavka_p & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *podaci, size_t promeniti_veličinu) { return 실행파일검사(podaci, promeniti_veličinu, 0); }
static void raspored_na_stranici(uintptr_t adresa, uint64_t konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini, unsigned dozvole) {
    unsigned LOOKUP_INDEX = (adresa - korisnik_BASE) / veličina_stranice;
    stranica_Lista[LOOKUP_INDEX] = adresa | konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini;
    Dozvole_Lista[LOOKUP_INDEX] = dozvole;
}
static int korisnik_opseg(uintptr_t adresa, size_t stavka_COUNT_8f7753a1, int 쓰는중) {
    if (adresa < korisnik_BASE || !포함된범위(adresa, stavka_COUNT_8f7753a1, korisnik_završiti_razgovor)) return 0;
    if (!stavka_COUNT_8f7753a1) return 1;
    unsigned 첫항목 = (adresa - korisnik_BASE) / veličina_stranice, 마지막 = (adresa + stavka_COUNT_8f7753a1 - 1 - korisnik_BASE) / veličina_stranice;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(Dozvole_Lista[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int instanca_putanja(uintptr_t adresa, char *putanja) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!korisnik_opseg(adresa, 1, 0)) return -14;
        putanja[순번] = *(const char *)adresa++;
        if (!putanja[순번]) return 0;
    }
    return -36;
}
static intptr_t jezgro_KR(intptr_t KR) { return KR < 0 ? -broj_greške : KR; }
static int 대응파일기술자(uint64_t Datoteka_pokazivač) { return Datoteka_pokazivač >= 3 && Datoteka_pokazivač < 19 ? Datoteka_Lista[Datoteka_pokazivač - 3] : -1; }
static int 통신끝점소유(uint64_t Datoteka_pokazivač) { return Datoteka_pokazivač >= 32 && Datoteka_pokazivač < 56 && 통신끝점들[Datoteka_pokazivač - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t 길이, struct pk_sockaddr_in *adresa) {
    if (길이 != sizeof(*adresa)) return -22;
    if (!korisnik_opseg(가리킴값, 길이, 0)) return -14;
    memcpy(adresa, (const void *)가리킴값, sizeof(*adresa));
    return adresa->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t 길이포인터, pk_socklen_t *bafer_kapacitet) {
    if (!korisnik_opseg(길이포인터, sizeof(*bafer_kapacitet), 1)) return -14;
    memcpy(bafer_kapacitet, (const void *)길이포인터, sizeof(*bafer_kapacitet));
    if (*bafer_kapacitet > sizeof(struct pk_sockaddr_in)) *bafer_kapacitet = sizeof(struct pk_sockaddr_in);
    if (*bafer_kapacitet && !korisnik_opseg(가리킴값, *bafer_kapacitet, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t 길이포인터, pk_socklen_t bafer_kapacitet, int adresa, int broj_porta) {
    struct pk_sockaddr_in VALUE; memset(&VALUE, 0, sizeof(VALUE));
    VALUE.sin_family = AF_INET; VALUE.sin_port = pk_htons(broj_porta); VALUE.sin_addr.s_addr = pk_htonl(adresa);
    if (bafer_kapacitet) memcpy((void *)가리킴값, &VALUE, bafer_kapacitet);
    pk_socklen_t 길이 = sizeof(VALUE); memcpy((void *)길이포인터, &길이, sizeof(길이));
}
extern uintptr_t Tabla_Kanal(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(korisnik_kadar *Datoteka_stavka) {
    uintptr_t 첫째값 = Datoteka_stavka->registar_podaci[0], SECOND_VALUE = Datoteka_stavka->registar_podaci[1], kôd_znaka = Datoteka_stavka->registar_podaci[2];
    char putanja[65];
    int Datoteka_pokazivač, KR;
    switch (Datoteka_stavka->registar_podaci[8]) {
    case 0: return 1; // 자체 ABI 버전
    case 1: // write: pokazivač 전체를 검사한 NAZAD_VALUE 출력/Datoteka promeniti_VALUE
        if (kôd_znaka > 65536) return -22;
        if (!korisnik_opseg(SECOND_VALUE, kôd_znaka, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=Sat_VALUE();
            for (size_t 순번 = 0; 순번 < kôd_znaka; 순번++) Tabla_Kanal(첫째값, ((const unsigned char *)SECOND_VALUE)[순번]);
            /* 큰 tty를 그린 jezgro_VALUE 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(대화형){
                krajnji_rok_TIME+=Sat_VALUE()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(krajnji_rok_TIME) : "memory");
            }
            return kôd_znaka;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t stavka_COUNT=kôd_znaka>512?512:kôd_znaka;for(size_t 순번=0;순번<stavka_COUNT;순번++)자바전문넣기(순번,((const unsigned char *)SECOND_VALUE)[순번]);return 자바흐름쓰기(첫째값,stavka_COUNT);
        }
        Datoteka_pokazivač = 대응파일기술자(첫째값); if (Datoteka_pokazivač < 0) return -9;
        return jezgro_KR(pk_write(Datoteka_pokazivač, (const void *)SECOND_VALUE, kôd_znaka));
    case 2:
        if (kôd_znaka > 65536) return -22;
        if (!korisnik_opseg(SECOND_VALUE, kôd_znaka, 1)) return -14;
        if (첫째값 == 0) {
            size_t stavka_COUNT = 0;
            while (stavka_COUNT < kôd_znaka) {
                int znak_VALUE = (int32_t)보드글자읽기(); if (znak_VALUE == -2) return stavka_COUNT; if (znak_VALUE < 0) break;
                ((unsigned char *)SECOND_VALUE)[stavka_COUNT++] = znak_VALUE;
            }
            return stavka_COUNT ? (intptr_t)stavka_COUNT : (kôd_znaka ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            KR=자바흐름읽기(첫째값,kôd_znaka>512?512:kôd_znaka);if(KR>0)for(int 순번=0;순번<KR;순번++)((unsigned char *)SECOND_VALUE)[순번]=자바전문얻기(순번);return KR;
        }
        Datoteka_pokazivač = 대응파일기술자(첫째값); if (Datoteka_pokazivač < 0) return -9;
        return jezgro_KR(pk_read(Datoteka_pokazivač, (void *)SECOND_VALUE, kôd_znaka));
    case 3:
        KR = instanca_putanja(첫째값, putanja); if (KR) return KR;
        if (SECOND_VALUE > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (Datoteka_Lista[순번] < 0) {
            Datoteka_pokazivač = pk_open(putanja, (int)SECOND_VALUE, 0600);
            if (Datoteka_pokazivač < 0) return -broj_greške;
            Datoteka_Lista[순번] = Datoteka_pokazivač; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { KR = 통신끝점닫기(첫째값); if (!KR) 통신끝점들[첫째값 - 32] = 0; return KR; }
        Datoteka_pokazivač = 대응파일기술자(첫째값); if (Datoteka_pokazivač < 0) return -9;
        KR = pk_close(Datoteka_pokazivač); if (!KR) Datoteka_Lista[첫째값 - 3] = -1;
        return jezgro_KR(KR);
    case 5:
        Datoteka_pokazivač = 대응파일기술자(첫째값); if (Datoteka_pokazivač < 0) return -9;
        if (kôd_znaka > 2) return -22;
        return jezgro_KR(pk_lseek(Datoteka_pokazivač, (int64_t)SECOND_VALUE, kôd_znaka));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 korisnik RW/NX 힙, 새로 노출되는 페이지는 0으로 초기화
        if (!첫째값) return 동적기억끝;
        if (첫째값 < korisnik_IMAGE_završiti_razgovor || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + veličina_stranice - 1) & ~(veličina_stranice - 1);
        uintptr_t 새쪽들 = (첫째값 + veličina_stranice - 1) & ~(veličina_stranice - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t podaci_pozicija = 이전쪽들; podaci_pozicija < 새쪽들; podaci_pozicija += veličina_stranice) raspored_na_stranici(podaci_pozicija, jezgro_stranica, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t podaci_pozicija = 이전쪽들; podaci_pozicija < 새쪽들; podaci_pozicija += veličina_stranice) raspored_na_stranici(podaci_pozicija, korisnik_za_čitanje_pisanje, 3);
        } else {
            for (uintptr_t podaci_pozicija = 새쪽들; podaci_pozicija < 이전쪽들; podaci_pozicija += veličina_stranice) {
                stranica_Lista[(podaci_pozicija - korisnik_BASE) / veličina_stranice] = 0; Dozvole_Lista[(podaci_pozicija - korisnik_BASE) / veličina_stranice] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        Datoteka_pokazivač = 대응파일기술자(첫째값); return Datoteka_pokazivač < 0 ? -9 : jezgro_KR(pk_size(Datoteka_pokazivač));
    case 10:
        Datoteka_pokazivač = 대응파일기술자(첫째값); return Datoteka_pokazivač < 0 ? -9 : jezgro_KR(pk_ftruncate(Datoteka_pokazivač, (int64_t)SECOND_VALUE));
    case 11:
        KR = instanca_putanja(첫째값, putanja); return KR ? KR : jezgro_KR(pk_unlink(putanja));
    case 12:
        Datoteka_pokazivač = 대응파일기술자(첫째값); return Datoteka_pokazivač < 0 ? -9 : jezgro_KR(pk_fsync(Datoteka_pokazivač));
    case 13: { // 그래픽 기초 API: korisnik 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = Datoteka_stavka->registar_podaci[3], 높이값 = Datoteka_stavka->registar_podaci[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SECOND_VALUE > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - SECOND_VALUE) return -22;
        for (uintptr_t 세로좌표 = SECOND_VALUE; 세로좌표 < SECOND_VALUE + 높이값; 세로좌표++) for (uintptr_t x_koordinata = 첫째값; x_koordinata < 첫째값 + 너비값; x_koordinata++) Tabla_piksel(x_koordinata, 세로좌표, kôd_znaka);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=stavka_COUNT; args(index,buffer,capacity)=UTF-8 길이
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (kôd_znaka <= 전달인수길이[첫째값]) return -36;
        if (!korisnik_opseg(SECOND_VALUE, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SECOND_VALUE, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;대화형=1;return Tabla_Terminal(13);}
        if(첫째값==2){대화형=0;return 0;}
        if(첫째값==3)return Tabla_Terminal(13);
        if(첫째값!=1||!대화형)return -22;
        KR=(int32_t)보드글자읽기();
        if(KR==-4096)return KR;
        START_TIMEOUT();return KR<0?-11:KR;
    case 17: { // 유한한 협력 čekaj_VALUE: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t završiti_razgovor_TIME = Sat_VALUE() + FREQUENCY * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Sat_VALUE() < završiti_razgovor_TIME);
        START_TIMEOUT(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 nadređen_VALUE·빈 폴더를 검사한다.
        if (SECOND_VALUE > 2) return -22;
        KR = instanca_putanja(첫째값, putanja); if (KR) return KR;
        unsigned 길이 = 0; while (putanja[길이]) 길이++;
        KR = 자바경로시작(길이); if (KR < 0) return KR;
        for (unsigned 순번 = 0; 순번 < 길이; 순번++) 자바경로바이트(순번, (unsigned char)putanja[순번]);
        return SECOND_VALUE == 0 ? 자바항목종류() : SECOND_VALUE == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int znak_VALUE=(int32_t)보드글자읽기();if(znak_VALUE==-4096)return znak_VALUE;if(znak_VALUE>=0)화면누름(vlasnik_objekat,znak_VALUE);START_TIMEOUT();}
        if(첫째값==3&&kôd_znaka){if(!자바셸대화형())return -95;대화형=1;Tabla_Terminal(300);}
        return 화면호출(vlasnik_objekat,첫째값,SECOND_VALUE,kôd_znaka,Datoteka_stavka->registar_podaci[3],Datoteka_stavka->registar_podaci[4],Datoteka_stavka->registar_podaci[5]);
    case 21:
        if(kôd_znaka>127)return -22;if(!korisnik_opseg(SECOND_VALUE,kôd_znaka*sizeof(uint32_t),0))return -14;
        return 화면글(vlasnik_objekat,첫째값,(const uint32_t *)SECOND_VALUE,kôd_znaka);
    case 22: // 화면 promeniti_veličinu upit_VALUE: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SECOND_VALUE==SOCK_STREAM&&(kôd_znaka==0||kôd_znaka==6))KR=자바흐름만들기();
        else if(SECOND_VALUE==SOCK_DGRAM&&(kôd_znaka==0||kôd_znaka==IPPROTO_UDP))KR=자바전문만들기(첫째값,SECOND_VALUE,kôd_znaka);
        else return -93;
        if (KR >= 32 && KR < 56) 통신끝점들[KR - 32] = 1;
        return KR;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in adresa;
        KR = 주소입력(SECOND_VALUE, kôd_znaka, &adresa); if (KR) return KR;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(adresa.sin_addr.s_addr),pk_htons(adresa.sin_port)):자바전문묶기(첫째값, pk_htonl(adresa.sin_addr.s_addr), pk_htons(adresa.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Datoteka_stavka->registar_podaci[3]) return -95;
        if (kôd_znaka > 512) return -90;
        if (kôd_znaka && !korisnik_opseg(SECOND_VALUE, kôd_znaka, 0)) return -14;
        struct pk_sockaddr_in adresa;
        KR = 주소입력(Datoteka_stavka->registar_podaci[4], Datoteka_stavka->registar_podaci[5], &adresa); if (KR) return KR;
        for (unsigned 순번 = 0; 순번 < kôd_znaka; 순번++) 자바전문넣기(순번, ((const unsigned char *)SECOND_VALUE)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(adresa.sin_addr.s_addr), pk_htons(adresa.sin_port), kôd_znaka);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Datoteka_stavka->registar_podaci[3]) return -95;
        if (kôd_znaka > 512) return -90;
        if (kôd_znaka && !korisnik_opseg(SECOND_VALUE, kôd_znaka, 1)) return -14;
        pk_socklen_t bafer_kapacitet = 0;
        if (Datoteka_stavka->registar_podaci[4]) { KR = 주소출력검사(Datoteka_stavka->registar_podaci[4], Datoteka_stavka->registar_podaci[5], &bafer_kapacitet); if (KR) return KR; }
        KR = 자바전문받기(첫째값, kôd_znaka); if (KR < 0) return KR;
        for (int 순번 = 0; 순번 < KR; 순번++) ((unsigned char *)SECOND_VALUE)[순번] = 자바전문얻기(순번);
        if (Datoteka_stavka->registar_podaci[4]) 주소출력(Datoteka_stavka->registar_podaci[4], Datoteka_stavka->registar_podaci[5], bafer_kapacitet, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return KR;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t bafer_kapacitet;
        KR = 주소출력검사(SECOND_VALUE, kôd_znaka, &bafer_kapacitet); if (KR) return KR;
        주소출력(SECOND_VALUE,kôd_znaka,bafer_kapacitet,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in adresa;
        KR=주소입력(SECOND_VALUE,kôd_znaka,&adresa);if(KR)return KR;
        return 자바흐름연결(첫째값,pk_htonl(adresa.sin_addr.s_addr),pk_htons(adresa.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,SECOND_VALUE):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(SECOND_VALUE||kôd_znaka)return -95;KR=자바흐름연결받기(첫째값);if(KR>=40&&KR<56)통신끝점들[KR-32]=1;return KR;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(korisnik_kadar *Datoteka_stavka) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(Datoteka_stavka) : 자체체계호출(Datoteka_stavka);
}
static void vratiti_jezgro(korisnik_kadar *Datoteka_stavka, int KR) {
    Stani_TIMEOUT();
    Datoteka_stavka->registar_podaci[0] = (uint64_t)(int64_t)KR;
    Datoteka_stavka->komanda_pozicija = (uintptr_t)korisnik_vratiti;
    Datoteka_stavka->Status_kôd = 0x3c5; // EL1h, DAIF masked
}
int greška_u_korisničkom_režimu(korisnik_kadar *Datoteka_stavka, unsigned INTERCEPT) {
    if (!Aktivan || (Datoteka_stavka->Status_kôd & 15) != 0) return 0;
    if (INTERCEPT) {
        uint32_t 승인값 = računar_registar(IRQ_CPU_interfejs + 0xc), identifikator_VALUE = 승인값 & 1023;
        if (identifikator_VALUE == 30) { vratiti_jezgro(Datoteka_stavka, korisnik_TIMEOUT); računar_registar(IRQ_CPU_interfejs + 0x10) = 승인값; return 1; }
        if (identifikator_VALUE < 1020) računar_registar(IRQ_CPU_interfejs + 0x10) = 승인값;
        return 1;
    }
    uint64_t izuzetak_Status; __asm__ volatile("mrs %0, esr_el1" : "=r"(izuzetak_Status));
    if (Sat_VALUE() >= krajnji_rok_TIME) { vratiti_jezgro(Datoteka_stavka, korisnik_TIMEOUT); return 1; }
    unsigned izuzetak_oblast = izuzetak_Status >> 26;
    if (izuzetak_oblast == 0x15 && (izuzetak_Status & 0xffff) == 0) {
        if (리눅스규약 ? Datoteka_stavka->registar_podaci[8] == 93 || Datoteka_stavka->registar_podaci[8] == 94 : Datoteka_stavka->registar_podaci[8] == 6) vratiti_jezgro(Datoteka_stavka, (int)(Datoteka_stavka->registar_podaci[0] & 255));
        else {
            intptr_t KR=체계호출(Datoteka_stavka);
            if(KR==-4096&&대화형){
                저장값[vlasnik_objekat].실행틀=*Datoteka_stavka;저장값[vlasnik_objekat].실행틀.komanda_pozicija-=4;
                사용자실수보관(저장값[vlasnik_objekat].plutajući_p_Status);vratiti_jezgro(Datoteka_stavka,사용자중단됨);
            }else Datoteka_stavka->registar_podaci[0]=(uint64_t)KR;
        }
    } else vratiti_jezgro(Datoteka_stavka, izuzetak_oblast == 0x24 ? korisnik_podaci_greška : izuzetak_oblast == 0x20 ? 사용자실행오류 : 사용자잘못된명령);
    return 1;
}

// 생성된 const ELF Grupa_VALUE: 실행은 반드시 program_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *podaci; size_t promeniti_veličinu; unsigned 전달값; } program;
#include "programs.h"
static void *snimak(unsigned indeks_pozicije){return (void *)(0x04000000ul+indeks_pozicije*(korisnik_završiti_razgovor-korisnik_BASE));}
static int kraj_program(int KR){
    사용자누적시각[vlasnik_objekat]+=(uint32_t)보드밀리초()-사용자실행시각[vlasnik_objekat];
    Stani_TIMEOUT();Aktivan=0;
    if(KR==사용자중단됨){
        저장된작업 *niska_podaci=&저장값[vlasnik_objekat];niska_podaci->멈춤상태=1;niska_podaci->대화형=대화형;niska_podaci->리눅스규약=리눅스규약;niska_podaci->동적기억공간=동적기억끝;niska_podaci->인수개수=전달인수개수;
        memcpy(niska_podaci->Dozvole_Lista,Dozvole_Lista,sizeof(Dozvole_Lista));memcpy(niska_podaci->Datoteka_Lista,Datoteka_Lista,sizeof(Datoteka_Lista));memcpy(niska_podaci->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(niska_podaci->argument_niz,전달인수,sizeof(전달인수));memcpy(niska_podaci->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<korisnik_stranica_COUNT;순번++)if(Dozvole_Lista[순번])memcpy((unsigned char *)snimak(vlasnik_objekat)+순번*veličina_stranice,(void *)(korisnik_BASE+순번*veličina_stranice),veličina_stranice);
    }else{
        저장값[vlasnik_objekat].멈춤상태=0;화면초기화(vlasnik_objekat);
        for(unsigned 순번=0;순번<16;순번++)if(Datoteka_Lista[순번]>=0)pk_close(Datoteka_Lista[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<korisnik_stranica_COUNT;순번++){stranica_Lista[순번]=0;Dozvole_Lista[순번]=0;}변환표맞추기();return KR;
}
uintptr_t Tabla_korisnička_kontrola(uintptr_t radnja){
    unsigned indeks_pozicije=radnja&15;if(indeks_pozicije>=4||Aktivan)return (uint32_t)-22;
    저장된작업 *niska_podaci=&저장값[indeks_pozicije];
    if(radnja>=32){if(niska_podaci->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(niska_podaci->Datoteka_Lista[순번]>=0)pk_close(niska_podaci->Datoteka_Lista[순번]);for(unsigned 순번=0;순번<24;순번++)if(niska_podaci->통신끝점들[순번])통신끝점닫기(순번+32);}niska_podaci->멈춤상태=0;화면초기화(indeks_pozicije);return 0;}
    if(radnja>=16)return niska_podaci->멈춤상태;
    if(!niska_podaci->멈춤상태)return (uint32_t)-22;
    vlasnik_objekat=indeks_pozicije;대화형=niska_podaci->대화형;리눅스규약=niska_podaci->리눅스규약;동적기억끝=niska_podaci->동적기억공간;전달인수개수=niska_podaci->인수개수;
    memcpy(Datoteka_Lista,niska_podaci->Datoteka_Lista,sizeof(Datoteka_Lista));memcpy(통신끝점들,niska_podaci->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,niska_podaci->argument_niz,sizeof(전달인수));memcpy(전달인수길이,niska_podaci->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<korisnik_stranica_COUNT;순번++)stranica_Lista[순번]=(korisnik_BASE+순번*veličina_stranice)|jezgro_stranica;변환표맞추기();
    memset((void *)korisnik_BASE,0,korisnik_završiti_razgovor-korisnik_BASE);
    for(unsigned 순번=0;순번<korisnik_stranica_COUNT;순번++)if(niska_podaci->Dozvole_Lista[순번])memcpy((void *)(korisnik_BASE+순번*veličina_stranice),(unsigned char *)snimak(indeks_pozicije)+순번*veličina_stranice,veličina_stranice);
    memcpy(Dozvole_Lista,niska_podaci->Dozvole_Lista,sizeof(Dozvole_Lista));
    for(unsigned 순번=0;순번<korisnik_stranica_COUNT;순번++){unsigned podaci_pozicija=Dozvole_Lista[순번];stranica_Lista[순번]=podaci_pozicija?(korisnik_BASE+순번*veličina_stranice)|(podaci_pozicija==3?korisnik_za_čitanje_pisanje:podaci_pozicija==5?사용자읽고실행:korisnik_samo_za_čitanje):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");Aktivan=1;niska_podaci->멈춤상태=0;START_TIMEOUT();
    사용자실행시각[vlasnik_objekat]=보드밀리초();
    return (uint32_t)kraj_program(korisnik_rezime(&niska_podaci->실행틀,niska_podaci->plutajući_p_Status));
}
static int koristiti_program(const unsigned char *podaci, size_t promeniti_veličinu, unsigned 전달값, int 리눅스방식, const char *ime) {
    if (Aktivan) return -16;
    vlasnik_objekat=Tabla_Terminal(11);if(vlasnik_objekat<0||vlasnik_objekat>3||저장값[vlasnik_objekat].멈춤상태)return -16;대화형=0;
    int 유효함 = 실행파일검사(podaci, promeniti_veličinu, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned ime_INDEX=0;
    while (*ime && ime_INDEX<31) korisnik_komanda_ime[vlasnik_objekat][ime_INDEX++]=(unsigned char)*ime++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (ime_INDEX) korisnik_komanda_ime[vlasnik_objekat][ime_INDEX++]=' ';
        for (unsigned indeks_pozicije=0; indeks_pozicije<전달인수길이[0]; indeks_pozicije++) korisnik_komanda_ime[vlasnik_objekat][ime_INDEX++]=전달인수[0][indeks_pozicije];
    }
    korisnik_komanda_ime[vlasnik_objekat][ime_INDEX]=0; broj_korisnika[vlasnik_objekat]=Dalje_broj_korisnika++;
    if (Dalje_broj_korisnika>0x7fffffffu) Dalje_broj_korisnika=10;
    korisnik_START_TIME[vlasnik_objekat]=보드밀리초(); 사용자누적시각[vlasnik_objekat]=0;
    for (unsigned 순번 = 0; 순번 < korisnik_stranica_COUNT; 순번++) stranica_Lista[순번] = (korisnik_BASE + 순번 * veličina_stranice) | jezgro_stranica;
    변환표맞추기();
    memset((void *)korisnik_BASE, 0, korisnik_završiti_razgovor - korisnik_BASE);
    memset(Dozvole_Lista, 0, sizeof(Dozvole_Lista));
    실행파일머리 실행머리; memcpy(&실행머리, podaci, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.program_Zaglavlje_COUNT; 순번++) {
        실행파일구획 podaci_pozicija; memcpy(&podaci_pozicija, podaci + 실행머리.program_Zaglavlje_Pomak + 순번 * sizeof(podaci_pozicija), sizeof(podaci_pozicija));
        if (podaci_pozicija.tip_oblast != 1 || !podaci_pozicija.기억영역크기) continue;
        if (podaci_pozicija.파일영역크기) memcpy((void *)(uintptr_t)podaci_pozicija.adresa, podaci + podaci_pozicija.Pomak_VALUE, podaci_pozicija.파일영역크기);
        for (uintptr_t aktuelno_pozicija = podaci_pozicija.adresa & ~(veličina_stranice - 1); aktuelno_pozicija < podaci_pozicija.adresa + podaci_pozicija.기억영역크기; aktuelno_pozicija += veličina_stranice) {
            Dozvole_Lista[(aktuelno_pozicija - korisnik_BASE) / veličina_stranice] = (podaci_pozicija.konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini & 2) ? 3 : ((podaci_pozicija.konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini & 1) ? 5 : 1);
        }
    }
    for (uintptr_t aktuelno_pozicija = korisnik_stek_adresa; aktuelno_pozicija < korisnik_završiti_razgovor; aktuelno_pozicija += veličina_stranice) Dozvole_Lista[(aktuelno_pozicija - korisnik_BASE) / veličina_stranice] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.stavka_p) : korisnik_završiti_razgovor;
    for (unsigned 순번 = 0; 순번 < korisnik_stranica_COUNT; 순번++) {
        unsigned dozvole = Dozvole_Lista[순번];
        stranica_Lista[순번] = dozvole ? (korisnik_BASE + 순번 * veličina_stranice) | (dozvole == 3 ? korisnik_za_čitanje_pisanje : dozvole == 5 ? 사용자읽고실행 : korisnik_samo_za_čitanje) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) Datoteka_Lista[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = korisnik_IMAGE_završiti_razgovor;
    Aktivan = 1; START_TIMEOUT();
    사용자실행시각[vlasnik_objekat]=보드밀리초();
    int KR = korisnik_uneti(실행머리.stavka_p, 초기쌓임공간, 전달값);
    return kraj_program(KR);
}
uintptr_t Tabla_korisnik_koristiti(uintptr_t LOOKUP_INDEX) {
    if (LOOKUP_INDEX >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *ime=LOOKUP_INDEX==10?"javac":LOOKUP_INDEX==11?"java":LOOKUP_INDEX==12?"python":LOOKUP_INDEX==13?"vi":LOOKUP_INDEX==14?"jar":LOOKUP_INDEX==15?"cc":LOOKUP_INDEX==16?"jaot":"ELF";
    return (uint32_t)koristiti_program(실행항목들[LOOKUP_INDEX].podaci, 실행항목들[LOOKUP_INDEX].promeniti_veličinu, 실행항목들[LOOKUP_INDEX].전달값, 0, ime);
}
static uintptr_t Izvrši_Datoteka(int 리눅스방식) {
    static unsigned char IMAGE[16384];
    if (Aktivan || !전달인수개수) return (uint32_t)-22;
    int Datoteka_pokazivač = pk_open((const char *)전달인수[0], samo_za_čitanje_VALUE, 0);
    if (Datoteka_pokazivač < 0) return (uint32_t)-broj_greške;
    int promeniti_veličinu = pk_size(Datoteka_pokazivač);
    if (promeniti_veličinu < 0 || (unsigned)promeniti_veličinu > sizeof(IMAGE)) { pk_close(Datoteka_pokazivač); return (uint32_t)-27; }
    int RECEIVED_COUNT = pk_read(Datoteka_pokazivač, IMAGE, promeniti_veličinu); pk_close(Datoteka_pokazivač);
    if (RECEIVED_COUNT != promeniti_veličinu) return (uint32_t)-5;
    return (uint32_t)koristiti_program(IMAGE, promeniti_veličinu, 0, 리눅스방식, "");
}
uintptr_t Tabla_korisnik_Datoteka(void) { return Izvrši_Datoteka(0); }
uintptr_t 보드사용자리눅스파일(void) { return Izvrši_Datoteka(1); }
uintptr_t Tabla_korisnik_potvrditi(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].podaci, 잘못된실행항목들[순번].promeniti_veličinu) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
