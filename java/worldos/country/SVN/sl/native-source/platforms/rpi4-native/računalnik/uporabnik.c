#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 Izvedi_ukaz računalnik sloj_VALUE. Datoteka podatki/정책은 기존 AOT Java 커널에 위임한다.
#include "uporabnik.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../mreža_Sklad/mreža_Sklad.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define računalnik_register(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define prekinitev_distributer 0xff841000ul
#define prekinitev_CPE_vmesnik 0xff842000ul
#define velikost_strani 4096ul
#define dostop_oznaka (1ul << 10)
#define ne_Izvedi_dovoljenje (1ul << 53)
#define uporabnik_ne_Izvedi (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | dostop_oznaka)
#define jedro_stran (3ul | 보통기억 | ne_Izvedi_dovoljenje | uporabnik_ne_Izvedi)
#define uporabnik_branje_pisanje (3ul | 보통기억 | (1ul << 6) | ne_Izvedi_dovoljenje | uporabnik_ne_Izvedi)
#define uporabnik_samo_za_branje (3ul | 보통기억 | (3ul << 6) | ne_Izvedi_dovoljenje | uporabnik_ne_Izvedi)
#define 사용자읽고실행 (3ul | 보통기억 | (3ul << 6) | ne_Izvedi_dovoljenje)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t Tabla_slikovna_pika(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t Tabla_Terminal(uintptr_t);
extern int Terminal_čakajoče(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int uporabnik_nadaljevati(uporabnik_okvir *,void *);
extern void 사용자실수보관(void *);
extern int uporabnik_vnesti(uintptr_t vnos_p, uintptr_t Sklad_Senzor_prostora, uintptr_t 전달값);
extern void uporabnik_vrni(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t koren_naslov[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t stran_Seznam[uporabnik_stran_COUNT] __attribute__((aligned(4096)));
static uint8_t Dovoljenja_Seznam[uporabnik_stran_COUNT];
static int Dejaven, Datoteka_Seznam[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int Zapri_vtičnica_končna_točka(unsigned Datoteka_ročica){return Datoteka_ročica<40?자바전문닫기(Datoteka_ročica):자바흐름닫기(Datoteka_ročica);}
static uint64_t FREQUENCY, rok_čas;
static uintptr_t kopica_končati_klic;
// jedro_VALUE 셸이 준비한 UTF-8 Argumenti. EL0에는 kopirati_VALUE 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,interaktiven,리눅스규약,Datoteka_Seznam[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char argument_ARRAY[8][256],Dovoljenja_Seznam[uporabnik_stran_COUNT];
    uintptr_t kopica_Senzor_prostora; uporabnik_okvir 실행틀;
    unsigned char plavajoče_p_stanje[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int lastnik_predmet,interaktiven;
static uint32_t številka_uporabnika[4], uporabnik_Start_čas[4], 사용자누적시각[4], 사용자실행시각[4], Naprej_številka_uporabnika=10;
static unsigned char uporabnik_ukaz_ime[4][288];
uint32_t 사용자상태읽기(unsigned vnos_VALUE, unsigned INDEX) {
    unsigned kazalec_mesta=INDEX&3;
    int stanje_VALUE=(Dejaven && lastnik_predmet==(int)kazalec_mesta) ? 1 : 저장값[kazalec_mesta].멈춤상태 ? 2 : 0;
    if (vnos_VALUE==0) return stanje_VALUE;
    if (!stanje_VALUE) return 0;
    if (vnos_VALUE==1) return številka_uporabnika[kazalec_mesta];
    if (vnos_VALUE==2) {
        unsigned char *쪽들=stanje_VALUE==1?Dovoljenja_Seznam:저장값[kazalec_mesta].Dovoljenja_Seznam;
        unsigned stran_COUNT=0; for (unsigned 순번=0; 순번<uporabnik_stran_COUNT; 순번++) if(쪽들[순번]) stran_COUNT++;
        return stran_COUNT*4;
    }
    if (vnos_VALUE==3) return (uint32_t)보드밀리초()-uporabnik_Start_čas[kazalec_mesta];
    if (vnos_VALUE==4) return 사용자누적시각[kazalec_mesta]+(stanje_VALUE==1?(uint32_t)보드밀리초()-사용자실행시각[kazalec_mesta]:0);
    if (vnos_VALUE==5) return INDEX/4<sizeof(uporabnik_ukaz_ime[0])?uporabnik_ukaz_ime[kazalec_mesta][INDEX/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t vnos_COUNT) {
    if (Dejaven || vnos_COUNT > 8) return (uint32_t)-22;
    전달인수개수 = vnos_COUNT;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t LOOKUP_INDEX, uintptr_t sprotno_položaj, uintptr_t bajt_podatki) {
    if (Dejaven || LOOKUP_INDEX >= 전달인수개수 || sprotno_položaj >= 255 || sprotno_položaj != 전달인수길이[LOOKUP_INDEX] || !bajt_podatki || bajt_podatki > 255)
        return (uint32_t)-22;
    전달인수[LOOKUP_INDEX][sprotno_položaj] = bajt_podatki;
    전달인수길이[LOOKUP_INDEX] = sprotno_položaj + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Ura_VALUE(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Stop_TIMEOUT(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    računalnik_register(prekinitev_distributer + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void Start_TIMEOUT(void) {
    uint64_t 간격 = FREQUENCY * 2, vklopiti = 1;
    rok_čas = Ura_VALUE() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(vklopiti) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned blok_podatkov = 0; blok_podatkov < 4; blok_podatkov++) {
        koren_naslov[blok_podatkov] = (uintptr_t)가운데[blok_podatkov] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t naslov = ((uintptr_t)blok_podatkov << 30) | ((uintptr_t)순번 << 21);
            가운데[blok_podatkov][순번] = naslov | 1 | dostop_oznaka | uporabnik_ne_Izvedi;
            if (naslov >= 0xfc000000ul) 가운데[blok_podatkov][순번] |= ne_Izvedi_dovoljenje; // Device-nGnRnE
            else 가운데[blok_podatkov][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned SECOND_VALUE = 0; SECOND_VALUE < uporabnik_stran_COUNT / 512; SECOND_VALUE++)
        가운데[0][(uporabnik_BASE >> 21) + SECOND_VALUE] = (uintptr_t)(stran_Seznam + SECOND_VALUE * 512) | 3;
    for (unsigned 순번 = 0; 순번 < uporabnik_stran_COUNT; 순번++) stran_Seznam[순번] = (uporabnik_BASE + 순번 * velikost_strani) | jedro_stran;
    uint64_t pomnilnik_atribut_register = 0x4400, naslov_Prevod_nadzor = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(pomnilnik_atribut_register), "r"(naslov_Prevod_nadzor), "r"((uintptr_t)koren_naslov) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t plavajoče_p_stanje = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(plavajoče_p_stanje) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    Stop_TIMEOUT();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 vnos_p_VALUE 때만 Dovoli_VALUE.
    računalnik_register(prekinitev_distributer) = 0;
    računalnik_register(prekinitev_distributer + 0x180) = 0xffffffff;
    računalnik_register(prekinitev_distributer + 0x80) = 0xffffffff;
    računalnik_register(prekinitev_distributer + 0x280) = 1u << 30;
    računalnik_register(prekinitev_distributer + 0x41c) = 0x80808080;
    računalnik_register(prekinitev_distributer + 0x100) = 1u << 30;
    računalnik_register(prekinitev_CPE_vmesnik + 4) = 0xff;
    računalnik_register(prekinitev_CPE_vmesnik + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 수 있다.
    int Varnost = (računalnik_register(prekinitev_distributer + 4) & (1u << 10)) != 0;
    računalnik_register(prekinitev_distributer) = Varnost ? 1 : 3;
    računalnik_register(prekinitev_CPE_vmesnik) = Varnost ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t Tip_območje, računalnik_Tip; uint32_t številka_različice;
    uint64_t vnos_p, aplikacija_Glava_odmik, glava_odseka_odmik; uint32_t konfiguracija_storitev_Background_Intelligent_Transfer_Service;
    uint16_t 실행머리크기, aplikacija_Glava_vnos_spremeniti_velikost, aplikacija_Glava_COUNT, glava_odseka_vnos_spremeniti_velikost, glava_odseka_COUNT, odsek_ime_tabela_INDEX;
} 실행파일머리;
typedef struct { uint32_t Tip_območje, konfiguracija_storitev_Background_Intelligent_Transfer_Service; uint64_t odmik_VALUE, naslov, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(uporabnik_okvir) == 272, "exception assembly layout");
static int 포함된범위(uint64_t odmik_VALUE, uint64_t Velikost, uint64_t končati_klic_odmik) {
    return odmik_VALUE <= končati_klic_odmik && Velikost <= končati_klic_odmik - odmik_VALUE;
}
static int 부가정보검사(const unsigned char *podatki_položaj, size_t Velikost) {
    size_t sprotno_položaj = 0;
    while (포함된범위(sprotno_položaj, 12, Velikost)) {
        uint32_t 낱말들[3]; memcpy(낱말들, podatki_položaj + sprotno_položaj, 12); sprotno_položaj += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(sprotno_položaj, 이름영역크기, Velikost) || !포함된범위(sprotno_položaj + 이름영역크기, 설명크기, Velikost)) return 0;
        const unsigned char Ime[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Ime) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Ime); 순번++) if (podatki_položaj[sprotno_položaj + 순번] != Ime[순번]) 일치 = 0;
        uint32_t številka_različice = 0;
        if (일치) memcpy(&številka_različice, podatki_položaj + sprotno_položaj + 이름영역크기, 4);
        if (일치 && številka_različice == 1) return 1;
        sprotno_položaj += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *podatki, size_t Velikost, int 리눅스방식) {
    if (Velikost < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, podatki, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.Tip_območje != 2 || 실행머리.računalnik_Tip != 183 || 실행머리.številka_različice != 1 || 실행머리.konfiguracija_storitev_Background_Intelligent_Transfer_Service || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.aplikacija_Glava_vnos_spremeniti_velikost != sizeof(실행파일구획) || !실행머리.aplikacija_Glava_COUNT || 실행머리.aplikacija_Glava_COUNT > 16 ||
        실행머리.aplikacija_Glava_odmik < sizeof(실행머리) || !포함된범위(실행머리.aplikacija_Glava_odmik, (uint64_t)실행머리.aplikacija_Glava_COUNT * sizeof(실행파일구획), Velikost)) return 사용자실행파일오류;
    uint8_t 사용량[(uporabnik_IMAGE_končati_klic - uporabnik_BASE) / velikost_strani] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.aplikacija_Glava_COUNT; 순번++) {
        실행파일구획 podatki_položaj; memcpy(&podatki_položaj, podatki + 실행머리.aplikacija_Glava_odmik + 순번 * sizeof(podatki_položaj), sizeof(podatki_položaj));
        if (podatki_položaj.Tip_območje == 4) {
            if (!포함된범위(podatki_položaj.odmik_VALUE, podatki_položaj.파일영역크기, Velikost)) return 사용자실행파일오류;
            if (부가정보검사(podatki + podatki_položaj.odmik_VALUE, podatki_položaj.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (podatki_položaj.Tip_območje == 0 || podatki_položaj.Tip_območje == 6 || (podatki_položaj.Tip_območje == 0x6474e551 && !(podatki_položaj.konfiguracija_storitev_Background_Intelligent_Transfer_Service & 1))) continue;
        if (podatki_položaj.Tip_območje != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!podatki_položaj.기억영역크기) continue;
        if (podatki_položaj.konfiguracija_storitev_Background_Intelligent_Transfer_Service & ~7u || !(podatki_položaj.konfiguracija_storitev_Background_Intelligent_Transfer_Service & 4) || (podatki_položaj.konfiguracija_storitev_Background_Intelligent_Transfer_Service & 3) == 3 || podatki_položaj.파일영역크기 > podatki_položaj.기억영역크기 ||
            (podatki_položaj.파일영역크기 && !포함된범위(podatki_položaj.odmik_VALUE, podatki_položaj.파일영역크기, Velikost)) || podatki_položaj.naslov < uporabnik_BASE ||
            !포함된범위(podatki_položaj.naslov, podatki_položaj.기억영역크기, uporabnik_IMAGE_končati_klic) ||
            (!리눅스방식 && ((podatki_položaj.naslov & (velikost_strani - 1)) || (podatki_položaj.odmik_VALUE & (velikost_strani - 1)) || podatki_položaj.맞춤 != velikost_strani)) ||
            (리눅스방식 && (((podatki_položaj.naslov ^ podatki_položaj.odmik_VALUE) & (velikost_strani - 1)) || !podatki_položaj.맞춤 ||
                (podatki_položaj.맞춤 & (podatki_položaj.맞춤 - 1)) || podatki_položaj.맞춤 > 0x200000 || ((podatki_položaj.naslov ^ podatki_položaj.odmik_VALUE) & (podatki_položaj.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (podatki_položaj.naslov - uporabnik_BASE) / velikost_strani;
        unsigned vnos_COUNT = ((podatki_položaj.naslov & (velikost_strani - 1)) + podatki_položaj.기억영역크기 + velikost_strani - 1) / velikost_strani;
        for (unsigned stran_VALUE = 첫항목; stran_VALUE < 첫항목 + vnos_COUNT; stran_VALUE++) {
            if (사용량[stran_VALUE]) return 사용자실행파일오류;
            사용량[stran_VALUE] = 1;
        }
        if ((podatki_položaj.konfiguracija_storitev_Background_Intelligent_Transfer_Service & 1) && 실행머리.vnos_p >= podatki_položaj.naslov && 실행머리.vnos_p < podatki_položaj.naslov + podatki_položaj.파일영역크기 && !(실행머리.vnos_p & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *podatki, size_t Velikost) { return 실행파일검사(podatki, Velikost, 0); }
static void postavitev_strani(uintptr_t naslov, uint64_t konfiguracija_storitev_Background_Intelligent_Transfer_Service, unsigned dovoljenja) {
    unsigned LOOKUP_INDEX = (naslov - uporabnik_BASE) / velikost_strani;
    stran_Seznam[LOOKUP_INDEX] = naslov | konfiguracija_storitev_Background_Intelligent_Transfer_Service;
    Dovoljenja_Seznam[LOOKUP_INDEX] = dovoljenja;
}
static int uporabnik_obseg(uintptr_t naslov, size_t vnos_COUNT, int 쓰는중) {
    if (naslov < uporabnik_BASE || !포함된범위(naslov, vnos_COUNT, uporabnik_končati_klic)) return 0;
    if (!vnos_COUNT) return 1;
    unsigned 첫항목 = (naslov - uporabnik_BASE) / velikost_strani, 마지막 = (naslov + vnos_COUNT - 1 - uporabnik_BASE) / velikost_strani;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(Dovoljenja_Seznam[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int kopirati_pot(uintptr_t naslov, char *POT) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!uporabnik_obseg(naslov, 1, 0)) return -14;
        POT[순번] = *(const char *)naslov++;
        if (!POT[순번]) return 0;
    }
    return -36;
}
static intptr_t jedro_KR(intptr_t REZULTAT) { return REZULTAT < 0 ? -številka_napake : REZULTAT; }
static int 대응파일기술자(uint64_t Datoteka_ročica) { return Datoteka_ročica >= 3 && Datoteka_ročica < 19 ? Datoteka_Seznam[Datoteka_ročica - 3] : -1; }
static int vtičnica_končna_točka_lastnik(uint64_t Datoteka_ročica) { return Datoteka_ročica >= 32 && Datoteka_ročica < 56 && 통신끝점들[Datoteka_ročica - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t 길이, struct pk_sockaddr_in *naslov) {
    if (길이 != sizeof(*naslov)) return -22;
    if (!uporabnik_obseg(가리킴값, 길이, 0)) return -14;
    memcpy(naslov, (const void *)가리킴값, sizeof(*naslov));
    return naslov->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t 길이포인터, pk_socklen_t *medpomnilnik_zmogljivost) {
    if (!uporabnik_obseg(길이포인터, sizeof(*medpomnilnik_zmogljivost), 1)) return -14;
    memcpy(medpomnilnik_zmogljivost, (const void *)길이포인터, sizeof(*medpomnilnik_zmogljivost));
    if (*medpomnilnik_zmogljivost > sizeof(struct pk_sockaddr_in)) *medpomnilnik_zmogljivost = sizeof(struct pk_sockaddr_in);
    if (*medpomnilnik_zmogljivost && !uporabnik_obseg(가리킴값, *medpomnilnik_zmogljivost, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t 길이포인터, pk_socklen_t medpomnilnik_zmogljivost, int naslov, int številka_vrat) {
    struct pk_sockaddr_in VALUE; memset(&VALUE, 0, sizeof(VALUE));
    VALUE.sin_family = AF_INET; VALUE.sin_port = pk_htons(številka_vrat); VALUE.sin_addr.s_addr = pk_htonl(naslov);
    if (medpomnilnik_zmogljivost) memcpy((void *)가리킴값, &VALUE, medpomnilnik_zmogljivost);
    pk_socklen_t 길이 = sizeof(VALUE); memcpy((void *)길이포인터, &길이, sizeof(길이));
}
extern uintptr_t Tabla_Kanal(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(uporabnik_okvir *Datoteka_vnos) {
    uintptr_t 첫째값 = Datoteka_vnos->register_podatki[0], SECOND_VALUE = Datoteka_vnos->register_podatki[1], koda_znaka = Datoteka_vnos->register_podatki[2];
    char POT[65];
    int Datoteka_ročica, REZULTAT;
    switch (Datoteka_vnos->register_podatki[8]) {
    case 0: return 1; // lastno ABI 버전
    case 1: // write: kazalec 전체를 검사한 ZAJ_VALUE Izpis/Datoteka spremeniti_VALUE
        if (koda_znaka > 65536) return -22;
        if (!uporabnik_obseg(SECOND_VALUE, koda_znaka, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=Ura_VALUE();
            for (size_t 순번 = 0; 순번 < koda_znaka; 순번++) Tabla_Kanal(첫째값, ((const unsigned char *)SECOND_VALUE)[순번]);
            /* 큰 tty를 그린 jedro_VALUE 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(interaktiven){
                rok_čas+=Ura_VALUE()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(rok_čas) : "memory");
            }
            return koda_znaka;
        }
        if(첫째값>=40&&vtičnica_končna_točka_lastnik(첫째값)){
            size_t element_COUNT=koda_znaka>512?512:koda_znaka;for(size_t 순번=0;순번<element_COUNT;순번++)자바전문넣기(순번,((const unsigned char *)SECOND_VALUE)[순번]);return 자바흐름쓰기(첫째값,element_COUNT);
        }
        Datoteka_ročica = 대응파일기술자(첫째값); if (Datoteka_ročica < 0) return -9;
        return jedro_KR(pk_write(Datoteka_ročica, (const void *)SECOND_VALUE, koda_znaka));
    case 2:
        if (koda_znaka > 65536) return -22;
        if (!uporabnik_obseg(SECOND_VALUE, koda_znaka, 1)) return -14;
        if (첫째값 == 0) {
            size_t element_COUNT = 0;
            while (element_COUNT < koda_znaka) {
                int znak_VALUE = (int32_t)보드글자읽기(); if (znak_VALUE == -2) return element_COUNT; if (znak_VALUE < 0) break;
                ((unsigned char *)SECOND_VALUE)[element_COUNT++] = znak_VALUE;
            }
            return element_COUNT ? (intptr_t)element_COUNT : (koda_znaka ? -11 : 0);
        }
        if(첫째값>=40&&vtičnica_končna_točka_lastnik(첫째값)){
            REZULTAT=자바흐름읽기(첫째값,koda_znaka>512?512:koda_znaka);if(REZULTAT>0)for(int 순번=0;순번<REZULTAT;순번++)((unsigned char *)SECOND_VALUE)[순번]=자바전문얻기(순번);return REZULTAT;
        }
        Datoteka_ročica = 대응파일기술자(첫째값); if (Datoteka_ročica < 0) return -9;
        return jedro_KR(pk_read(Datoteka_ročica, (void *)SECOND_VALUE, koda_znaka));
    case 3:
        REZULTAT = kopirati_pot(첫째값, POT); if (REZULTAT) return REZULTAT;
        if (SECOND_VALUE > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (Datoteka_Seznam[순번] < 0) {
            Datoteka_ročica = pk_open(POT, (int)SECOND_VALUE, 0600);
            if (Datoteka_ročica < 0) return -številka_napake;
            Datoteka_Seznam[순번] = Datoteka_ročica; return 순번 + 3;
        }
        return -24;
    case 4:
        if (vtičnica_končna_točka_lastnik(첫째값)) { REZULTAT = Zapri_vtičnica_končna_točka(첫째값); if (!REZULTAT) 통신끝점들[첫째값 - 32] = 0; return REZULTAT; }
        Datoteka_ročica = 대응파일기술자(첫째값); if (Datoteka_ročica < 0) return -9;
        REZULTAT = pk_close(Datoteka_ročica); if (!REZULTAT) Datoteka_Seznam[첫째값 - 3] = -1;
        return jedro_KR(REZULTAT);
    case 5:
        Datoteka_ročica = 대응파일기술자(첫째값); if (Datoteka_ročica < 0) return -9;
        if (koda_znaka > 2) return -22;
        return jedro_KR(pk_lseek(Datoteka_ročica, (int64_t)SECOND_VALUE, koda_znaka));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 uporabnik RW/NX kopica_VALUE, 새로 노출되는 페이지는 0으로 inicializirati
        if (!첫째값) return kopica_končati_klic;
        if (첫째값 < uporabnik_IMAGE_končati_klic || 첫째값 > uporabnik_kopica_končati_klic) return -12;
        uintptr_t 이전쪽들 = (kopica_končati_klic + velikost_strani - 1) & ~(velikost_strani - 1);
        uintptr_t 새쪽들 = (첫째값 + velikost_strani - 1) & ~(velikost_strani - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t podatki_položaj = 이전쪽들; podatki_položaj < 새쪽들; podatki_položaj += velikost_strani) postavitev_strani(podatki_položaj, jedro_stran, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t podatki_položaj = 이전쪽들; podatki_položaj < 새쪽들; podatki_položaj += velikost_strani) postavitev_strani(podatki_položaj, uporabnik_branje_pisanje, 3);
        } else {
            for (uintptr_t podatki_položaj = 새쪽들; podatki_položaj < 이전쪽들; podatki_položaj += velikost_strani) {
                stran_Seznam[(podatki_položaj - uporabnik_BASE) / velikost_strani] = 0; Dovoljenja_Seznam[(podatki_položaj - uporabnik_BASE) / velikost_strani] = 0;
            }
        }
        kopica_končati_klic = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        Datoteka_ročica = 대응파일기술자(첫째값); return Datoteka_ročica < 0 ? -9 : jedro_KR(pk_size(Datoteka_ročica));
    case 10:
        Datoteka_ročica = 대응파일기술자(첫째값); return Datoteka_ročica < 0 ? -9 : jedro_KR(pk_ftruncate(Datoteka_ročica, (int64_t)SECOND_VALUE));
    case 11:
        REZULTAT = kopirati_pot(첫째값, POT); return REZULTAT ? REZULTAT : jedro_KR(pk_unlink(POT));
    case 12:
        Datoteka_ročica = 대응파일기술자(첫째값); return Datoteka_ročica < 0 ? -9 : jedro_KR(pk_fsync(Datoteka_ročica));
    case 13: { // 그래픽 기초 API: uporabnik 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = Datoteka_vnos->register_podatki[3], 높이값 = Datoteka_vnos->register_podatki[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SECOND_VALUE > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - SECOND_VALUE) return -22;
        for (uintptr_t 세로좌표 = SECOND_VALUE; 세로좌표 < SECOND_VALUE + 높이값; 세로좌표++) for (uintptr_t koordinata_x = 첫째값; koordinata_x < 첫째값 + 너비값; koordinata_x++) Tabla_slikovna_pika(koordinata_x, 세로좌표, koda_znaka);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=element_COUNT; args(index,buffer,capacity)=UTF-8 길이
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (koda_znaka <= 전달인수길이[첫째값]) return -36;
        if (!uporabnik_obseg(SECOND_VALUE, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SECOND_VALUE, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;interaktiven=1;return Tabla_Terminal(13);}
        if(첫째값==2){interaktiven=0;return 0;}
        if(첫째값==3)return Tabla_Terminal(13);
        if(첫째값!=1||!interaktiven)return -22;
        REZULTAT=(int32_t)보드글자읽기();
        if(REZULTAT==-4096)return REZULTAT;
        Start_TIMEOUT();return REZULTAT<0?-11:REZULTAT;
    case 17: { // 유한한 협력 počakaj_VALUE: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t končati_klic_čas = Ura_VALUE() + FREQUENCY * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Ura_VALUE() < končati_klic_čas);
        Start_TIMEOUT(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 nadrejen_VALUE·빈 폴더를 검사한다.
        if (SECOND_VALUE > 2) return -22;
        REZULTAT = kopirati_pot(첫째값, POT); if (REZULTAT) return REZULTAT;
        unsigned 길이 = 0; while (POT[길이]) 길이++;
        REZULTAT = 자바경로시작(길이); if (REZULTAT < 0) return REZULTAT;
        for (unsigned 순번 = 0; 순번 < 길이; 순번++) 자바경로바이트(순번, (unsigned char)POT[순번]);
        return SECOND_VALUE == 0 ? 자바항목종류() : SECOND_VALUE == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int znak_VALUE=(int32_t)보드글자읽기();if(znak_VALUE==-4096)return znak_VALUE;if(znak_VALUE>=0)화면누름(lastnik_predmet,znak_VALUE);Start_TIMEOUT();}
        if(첫째값==3&&koda_znaka){if(!자바셸대화형())return -95;interaktiven=1;Tabla_Terminal(300);}
        return 화면호출(lastnik_predmet,첫째값,SECOND_VALUE,koda_znaka,Datoteka_vnos->register_podatki[3],Datoteka_vnos->register_podatki[4],Datoteka_vnos->register_podatki[5]);
    case 21:
        if(koda_znaka>127)return -22;if(!uporabnik_obseg(SECOND_VALUE,koda_znaka*sizeof(uint32_t),0))return -14;
        return 화면글(lastnik_predmet,첫째값,(const uint32_t *)SECOND_VALUE,koda_znaka);
    case 22: // 화면 Velikost poizvedba_VALUE: 0=너비, 1=višina_VALUE. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SECOND_VALUE==SOCK_STREAM&&(koda_znaka==0||koda_znaka==6))REZULTAT=자바흐름만들기();
        else if(SECOND_VALUE==SOCK_DGRAM&&(koda_znaka==0||koda_znaka==IPPROTO_UDP))REZULTAT=자바전문만들기(첫째값,SECOND_VALUE,koda_znaka);
        else return -93;
        if (REZULTAT >= 32 && REZULTAT < 56) 통신끝점들[REZULTAT - 32] = 1;
        return REZULTAT;
    case 33: {
        if (!vtičnica_končna_točka_lastnik(첫째값)) return -9;
        struct pk_sockaddr_in naslov;
        REZULTAT = 주소입력(SECOND_VALUE, koda_znaka, &naslov); if (REZULTAT) return REZULTAT;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(naslov.sin_addr.s_addr),pk_htons(naslov.sin_port)):자바전문묶기(첫째값, pk_htonl(naslov.sin_addr.s_addr), pk_htons(naslov.sin_port));
    }
    case 34: {
        if (!vtičnica_končna_točka_lastnik(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Datoteka_vnos->register_podatki[3]) return -95;
        if (koda_znaka > 512) return -90;
        if (koda_znaka && !uporabnik_obseg(SECOND_VALUE, koda_znaka, 0)) return -14;
        struct pk_sockaddr_in naslov;
        REZULTAT = 주소입력(Datoteka_vnos->register_podatki[4], Datoteka_vnos->register_podatki[5], &naslov); if (REZULTAT) return REZULTAT;
        for (unsigned 순번 = 0; 순번 < koda_znaka; 순번++) 자바전문넣기(순번, ((const unsigned char *)SECOND_VALUE)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(naslov.sin_addr.s_addr), pk_htons(naslov.sin_port), koda_znaka);
    }
    case 35: {
        if (!vtičnica_končna_točka_lastnik(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Datoteka_vnos->register_podatki[3]) return -95;
        if (koda_znaka > 512) return -90;
        if (koda_znaka && !uporabnik_obseg(SECOND_VALUE, koda_znaka, 1)) return -14;
        pk_socklen_t medpomnilnik_zmogljivost = 0;
        if (Datoteka_vnos->register_podatki[4]) { REZULTAT = 주소출력검사(Datoteka_vnos->register_podatki[4], Datoteka_vnos->register_podatki[5], &medpomnilnik_zmogljivost); if (REZULTAT) return REZULTAT; }
        REZULTAT = 자바전문받기(첫째값, koda_znaka); if (REZULTAT < 0) return REZULTAT;
        for (int 순번 = 0; 순번 < REZULTAT; 순번++) ((unsigned char *)SECOND_VALUE)[순번] = 자바전문얻기(순번);
        if (Datoteka_vnos->register_podatki[4]) 주소출력(Datoteka_vnos->register_podatki[4], Datoteka_vnos->register_podatki[5], medpomnilnik_zmogljivost, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return REZULTAT;
    }
    case 36: {
        if (!vtičnica_končna_točka_lastnik(첫째값)) return -9;
        pk_socklen_t medpomnilnik_zmogljivost;
        REZULTAT = 주소출력검사(SECOND_VALUE, koda_znaka, &medpomnilnik_zmogljivost); if (REZULTAT) return REZULTAT;
        주소출력(SECOND_VALUE,koda_znaka,medpomnilnik_zmogljivost,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!vtičnica_končna_točka_lastnik(첫째값))return -9;struct pk_sockaddr_in naslov;
        REZULTAT=주소입력(SECOND_VALUE,koda_znaka,&naslov);if(REZULTAT)return REZULTAT;
        return 자바흐름연결(첫째값,pk_htonl(naslov.sin_addr.s_addr),pk_htons(naslov.sin_port));
    }
    case 38: return 첫째값>=40&&vtičnica_končna_točka_lastnik(첫째값)?자바흐름듣기(첫째값,SECOND_VALUE):-9;
    case 39:
        if(첫째값<40||!vtičnica_končna_točka_lastnik(첫째값))return -9;
        if(SECOND_VALUE||koda_znaka)return -95;REZULTAT=자바흐름연결받기(첫째값);if(REZULTAT>=40&&REZULTAT<56)통신끝점들[REZULTAT-32]=1;return REZULTAT;
    case 40: return 첫째값>=40&&vtičnica_končna_točka_lastnik(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(uporabnik_okvir *Datoteka_vnos) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(Datoteka_vnos) : 자체체계호출(Datoteka_vnos);
}
static void vrni_jedro(uporabnik_okvir *Datoteka_vnos, int REZULTAT) {
    Stop_TIMEOUT();
    Datoteka_vnos->register_podatki[0] = (uint64_t)(int64_t)REZULTAT;
    Datoteka_vnos->ukaz_položaj = (uintptr_t)uporabnik_vrni;
    Datoteka_vnos->stanje_CODE = 0x3c5; // EL1h, DAIF masked
}
int izjema_uporabniškega_načina(uporabnik_okvir *Datoteka_vnos, unsigned odsek) {
    if (!Dejaven || (Datoteka_vnos->stanje_CODE & 15) != 0) return 0;
    if (odsek) {
        uint32_t potrditev_VALUE = računalnik_register(prekinitev_CPE_vmesnik + 0xc), identifikator_VALUE = potrditev_VALUE & 1023;
        if (identifikator_VALUE == 30) { vrni_jedro(Datoteka_vnos, uporabnik_TIMEOUT); računalnik_register(prekinitev_CPE_vmesnik + 0x10) = potrditev_VALUE; return 1; }
        if (identifikator_VALUE < 1020) računalnik_register(prekinitev_CPE_vmesnik + 0x10) = potrditev_VALUE;
        return 1;
    }
    uint64_t izjema_stanje; __asm__ volatile("mrs %0, esr_el1" : "=r"(izjema_stanje));
    if (Ura_VALUE() >= rok_čas) { vrni_jedro(Datoteka_vnos, uporabnik_TIMEOUT); return 1; }
    unsigned izjema_območje = izjema_stanje >> 26;
    if (izjema_območje == 0x15 && (izjema_stanje & 0xffff) == 0) {
        if (리눅스규약 ? Datoteka_vnos->register_podatki[8] == 93 || Datoteka_vnos->register_podatki[8] == 94 : Datoteka_vnos->register_podatki[8] == 6) vrni_jedro(Datoteka_vnos, (int)(Datoteka_vnos->register_podatki[0] & 255));
        else {
            intptr_t REZULTAT=체계호출(Datoteka_vnos);
            if(REZULTAT==-4096&&interaktiven){
                저장값[lastnik_predmet].실행틀=*Datoteka_vnos;저장값[lastnik_predmet].실행틀.ukaz_položaj-=4;
                사용자실수보관(저장값[lastnik_predmet].plavajoče_p_stanje);vrni_jedro(Datoteka_vnos,사용자중단됨);
            }else Datoteka_vnos->register_podatki[0]=(uint64_t)REZULTAT;
        }
    } else vrni_jedro(Datoteka_vnos, izjema_območje == 0x24 ? 사용자자료오류 : izjema_območje == 0x20 ? 사용자실행오류 : uporabnik_neveljaven_navodilo);
    return 1;
}

// 생성된 const ELF Skupina_VALUE: 실행은 반드시 aplikacija_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *podatki; size_t Velikost; unsigned 전달값; } aplikacija;
#include "programs.h"
static void *posnetek(unsigned kazalec_mesta){return (void *)(0x04000000ul+kazalec_mesta*(uporabnik_končati_klic-uporabnik_BASE));}
static int konec_aplikacija(int REZULTAT){
    사용자누적시각[lastnik_predmet]+=(uint32_t)보드밀리초()-사용자실행시각[lastnik_predmet];
    Stop_TIMEOUT();Dejaven=0;
    if(REZULTAT==사용자중단됨){
        저장된작업 *niz_podatki=&저장값[lastnik_predmet];niz_podatki->멈춤상태=1;niz_podatki->interaktiven=interaktiven;niz_podatki->리눅스규약=리눅스규약;niz_podatki->kopica_Senzor_prostora=kopica_končati_klic;niz_podatki->인수개수=전달인수개수;
        memcpy(niz_podatki->Dovoljenja_Seznam,Dovoljenja_Seznam,sizeof(Dovoljenja_Seznam));memcpy(niz_podatki->Datoteka_Seznam,Datoteka_Seznam,sizeof(Datoteka_Seznam));memcpy(niz_podatki->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(niz_podatki->argument_ARRAY,전달인수,sizeof(전달인수));memcpy(niz_podatki->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<uporabnik_stran_COUNT;순번++)if(Dovoljenja_Seznam[순번])memcpy((unsigned char *)posnetek(lastnik_predmet)+순번*velikost_strani,(void *)(uporabnik_BASE+순번*velikost_strani),velikost_strani);
    }else{
        저장값[lastnik_predmet].멈춤상태=0;화면초기화(lastnik_predmet);
        for(unsigned 순번=0;순번<16;순번++)if(Datoteka_Seznam[순번]>=0)pk_close(Datoteka_Seznam[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])Zapri_vtičnica_končna_točka(순번+32);
    }
    for(unsigned 순번=0;순번<uporabnik_stran_COUNT;순번++){stran_Seznam[순번]=0;Dovoljenja_Seznam[순번]=0;}변환표맞추기();return REZULTAT;
}
uintptr_t Tabla_uporabniški_kontrolnik(uintptr_t Dejanje){
    unsigned kazalec_mesta=Dejanje&15;if(kazalec_mesta>=4||Dejaven)return (uint32_t)-22;
    저장된작업 *niz_podatki=&저장값[kazalec_mesta];
    if(Dejanje>=32){if(niz_podatki->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(niz_podatki->Datoteka_Seznam[순번]>=0)pk_close(niz_podatki->Datoteka_Seznam[순번]);for(unsigned 순번=0;순번<24;순번++)if(niz_podatki->통신끝점들[순번])Zapri_vtičnica_končna_točka(순번+32);}niz_podatki->멈춤상태=0;화면초기화(kazalec_mesta);return 0;}
    if(Dejanje>=16)return niz_podatki->멈춤상태;
    if(!niz_podatki->멈춤상태)return (uint32_t)-22;
    lastnik_predmet=kazalec_mesta;interaktiven=niz_podatki->interaktiven;리눅스규약=niz_podatki->리눅스규약;kopica_končati_klic=niz_podatki->kopica_Senzor_prostora;전달인수개수=niz_podatki->인수개수;
    memcpy(Datoteka_Seznam,niz_podatki->Datoteka_Seznam,sizeof(Datoteka_Seznam));memcpy(통신끝점들,niz_podatki->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,niz_podatki->argument_ARRAY,sizeof(전달인수));memcpy(전달인수길이,niz_podatki->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<uporabnik_stran_COUNT;순번++)stran_Seznam[순번]=(uporabnik_BASE+순번*velikost_strani)|jedro_stran;변환표맞추기();
    memset((void *)uporabnik_BASE,0,uporabnik_končati_klic-uporabnik_BASE);
    for(unsigned 순번=0;순번<uporabnik_stran_COUNT;순번++)if(niz_podatki->Dovoljenja_Seznam[순번])memcpy((void *)(uporabnik_BASE+순번*velikost_strani),(unsigned char *)posnetek(kazalec_mesta)+순번*velikost_strani,velikost_strani);
    memcpy(Dovoljenja_Seznam,niz_podatki->Dovoljenja_Seznam,sizeof(Dovoljenja_Seznam));
    for(unsigned 순번=0;순번<uporabnik_stran_COUNT;순번++){unsigned podatki_položaj=Dovoljenja_Seznam[순번];stran_Seznam[순번]=podatki_položaj?(uporabnik_BASE+순번*velikost_strani)|(podatki_položaj==3?uporabnik_branje_pisanje:podatki_položaj==5?사용자읽고실행:uporabnik_samo_za_branje):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");Dejaven=1;niz_podatki->멈춤상태=0;Start_TIMEOUT();
    사용자실행시각[lastnik_predmet]=보드밀리초();
    return (uint32_t)konec_aplikacija(uporabnik_nadaljevati(&niz_podatki->실행틀,niz_podatki->plavajoče_p_stanje));
}
static int izvajati_aplikacija(const unsigned char *podatki, size_t Velikost, unsigned 전달값, int 리눅스방식, const char *Ime) {
    if (Dejaven) return -16;
    lastnik_predmet=Tabla_Terminal(11);if(lastnik_predmet<0||lastnik_predmet>3||저장값[lastnik_predmet].멈춤상태)return -16;interaktiven=0;
    int 유효함 = 실행파일검사(podatki, Velikost, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned ime_INDEX=0;
    while (*Ime && ime_INDEX<31) uporabnik_ukaz_ime[lastnik_predmet][ime_INDEX++]=(unsigned char)*Ime++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (ime_INDEX) uporabnik_ukaz_ime[lastnik_predmet][ime_INDEX++]=' ';
        for (unsigned kazalec_mesta=0; kazalec_mesta<전달인수길이[0]; kazalec_mesta++) uporabnik_ukaz_ime[lastnik_predmet][ime_INDEX++]=전달인수[0][kazalec_mesta];
    }
    uporabnik_ukaz_ime[lastnik_predmet][ime_INDEX]=0; številka_uporabnika[lastnik_predmet]=Naprej_številka_uporabnika++;
    if (Naprej_številka_uporabnika>0x7fffffffu) Naprej_številka_uporabnika=10;
    uporabnik_Start_čas[lastnik_predmet]=보드밀리초(); 사용자누적시각[lastnik_predmet]=0;
    for (unsigned 순번 = 0; 순번 < uporabnik_stran_COUNT; 순번++) stran_Seznam[순번] = (uporabnik_BASE + 순번 * velikost_strani) | jedro_stran;
    변환표맞추기();
    memset((void *)uporabnik_BASE, 0, uporabnik_končati_klic - uporabnik_BASE);
    memset(Dovoljenja_Seznam, 0, sizeof(Dovoljenja_Seznam));
    실행파일머리 실행머리; memcpy(&실행머리, podatki, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.aplikacija_Glava_COUNT; 순번++) {
        실행파일구획 podatki_položaj; memcpy(&podatki_položaj, podatki + 실행머리.aplikacija_Glava_odmik + 순번 * sizeof(podatki_položaj), sizeof(podatki_položaj));
        if (podatki_položaj.Tip_območje != 1 || !podatki_položaj.기억영역크기) continue;
        if (podatki_položaj.파일영역크기) memcpy((void *)(uintptr_t)podatki_položaj.naslov, podatki + podatki_položaj.odmik_VALUE, podatki_položaj.파일영역크기);
        for (uintptr_t sprotno_položaj = podatki_položaj.naslov & ~(velikost_strani - 1); sprotno_položaj < podatki_položaj.naslov + podatki_položaj.기억영역크기; sprotno_položaj += velikost_strani) {
            Dovoljenja_Seznam[(sprotno_položaj - uporabnik_BASE) / velikost_strani] = (podatki_položaj.konfiguracija_storitev_Background_Intelligent_Transfer_Service & 2) ? 3 : ((podatki_položaj.konfiguracija_storitev_Background_Intelligent_Transfer_Service & 1) ? 5 : 1);
        }
    }
    for (uintptr_t sprotno_položaj = uporabnik_Sklad_naslov; sprotno_položaj < uporabnik_končati_klic; sprotno_položaj += velikost_strani) Dovoljenja_Seznam[(sprotno_položaj - uporabnik_BASE) / velikost_strani] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.vnos_p) : uporabnik_končati_klic;
    for (unsigned 순번 = 0; 순번 < uporabnik_stran_COUNT; 순번++) {
        unsigned dovoljenja = Dovoljenja_Seznam[순번];
        stran_Seznam[순번] = dovoljenja ? (uporabnik_BASE + 순번 * velikost_strani) | (dovoljenja == 3 ? uporabnik_branje_pisanje : dovoljenja == 5 ? 사용자읽고실행 : uporabnik_samo_za_branje) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) Datoteka_Seznam[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    kopica_končati_klic = uporabnik_IMAGE_končati_klic;
    Dejaven = 1; Start_TIMEOUT();
    사용자실행시각[lastnik_predmet]=보드밀리초();
    int REZULTAT = uporabnik_vnesti(실행머리.vnos_p, 초기쌓임공간, 전달값);
    return konec_aplikacija(REZULTAT);
}
uintptr_t Tabla_uporabnik_izvajati(uintptr_t LOOKUP_INDEX) {
    if (LOOKUP_INDEX >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Ime=LOOKUP_INDEX==10?"javac":LOOKUP_INDEX==11?"java":LOOKUP_INDEX==12?"python":LOOKUP_INDEX==13?"vi":LOOKUP_INDEX==14?"jar":LOOKUP_INDEX==15?"cc":LOOKUP_INDEX==16?"jaot":"ELF";
    return (uint32_t)izvajati_aplikacija(실행항목들[LOOKUP_INDEX].podatki, 실행항목들[LOOKUP_INDEX].Velikost, 실행항목들[LOOKUP_INDEX].전달값, 0, Ime);
}
static uintptr_t Izvedi_Datoteka(int 리눅스방식) {
    static unsigned char IMAGE[16384];
    if (Dejaven || !전달인수개수) return (uint32_t)-22;
    int Datoteka_ročica = pk_open((const char *)전달인수[0], samo_za_branje_VALUE, 0);
    if (Datoteka_ročica < 0) return (uint32_t)-številka_napake;
    int Velikost = pk_size(Datoteka_ročica);
    if (Velikost < 0 || (unsigned)Velikost > sizeof(IMAGE)) { pk_close(Datoteka_ročica); return (uint32_t)-27; }
    int RECEIVED_COUNT = pk_read(Datoteka_ročica, IMAGE, Velikost); pk_close(Datoteka_ročica);
    if (RECEIVED_COUNT != Velikost) return (uint32_t)-5;
    return (uint32_t)izvajati_aplikacija(IMAGE, Velikost, 0, 리눅스방식, "");
}
uintptr_t Tabla_uporabnik_Datoteka(void) { return Izvedi_Datoteka(0); }
uintptr_t 보드사용자리눅스파일(void) { return Izvedi_Datoteka(1); }
uintptr_t Tabla_uporabnik_preveriti_veljavnost(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].podatki, 잘못된실행항목들[순번].Velikost) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
