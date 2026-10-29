#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 uitvoer_bevel masjien laag_VALUE. Lêer data/정책은 기존 AOT Java 커널에 위임한다.
#include "gebruiker.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../Netwerk_Stapel/Netwerk_Stapel.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define masjien_registreer(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_verspreider 0xff841000ul
#define IRQ_SVE_koppelvlak 0xff842000ul
#define bladsygrootte 4096ul
#define 접근표시 (1ul << 10)
#define nee_uitvoer_toestemming (1ul << 53)
#define gebruiker_nee_uitvoer (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | 접근표시)
#define kern_bladsy (3ul | 보통기억 | nee_uitvoer_toestemming | gebruiker_nee_uitvoer)
#define gebruiker_lees_skryf (3ul | 보통기억 | (1ul << 6) | nee_uitvoer_toestemming | gebruiker_nee_uitvoer)
#define gebruiker_leesalleen (3ul | 보통기억 | (3ul << 6) | nee_uitvoer_toestemming | gebruiker_nee_uitvoer)
#define 사용자읽고실행 (3ul | 보통기억 | (3ul << 6) | nee_uitvoer_toestemming)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t bord_pieksel(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t bord_Terminaal(uintptr_t);
extern int Terminaal_hangend(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int gebruiker_CV(gebruiker_raam *,void *);
extern void 사용자실수보관(void *);
extern int gebruiker_invoer(uintptr_t inskrywing_p, uintptr_t Stapel_Berging, uintptr_t 전달값);
extern void gebruiker_teruggee(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t wortel_adres[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t bladsy_Lys[gebruiker_bladsy_COUNT] __attribute__((aligned(4096)));
static uint8_t Toestemmings_Lys[gebruiker_bladsy_COUNT];
static int Aktief, lêer_Lys[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned lêer_handvatsel){return lêer_handvatsel<40?자바전문닫기(lêer_handvatsel):자바흐름닫기(lêer_handvatsel);}
static uint64_t FREQUENCY, 마감시각;
static uintptr_t 동적기억끝;
// kern_VALUE 셸이 준비한 UTF-8 인수. EL0에는 geval_VALUE 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,interaktief,리눅스규약,lêer_Lys[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char argument_ARRAY[8][256],Toestemmings_Lys[gebruiker_bladsy_COUNT];
    uintptr_t 동적기억공간; gebruiker_raam 실행틀;
    unsigned char 실수저장상태[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int eienaar_objek,interaktief;
static uint32_t gebruikernommer[4], gebruiker_BEGIN_tyd[4], 사용자누적시각[4], 사용자실행시각[4], Volgende_gebruikernommer=10;
static unsigned char gebruiker_bevel_naam[4][288];
uint32_t 사용자상태읽기(unsigned inskrywing_VALUE, unsigned INDEX) {
    unsigned plaas_INDEX=INDEX&3;
    int stand_VALUE=(Aktief && eienaar_objek==(int)plaas_INDEX) ? 1 : 저장값[plaas_INDEX].멈춤상태 ? 2 : 0;
    if (inskrywing_VALUE==0) return stand_VALUE;
    if (!stand_VALUE) return 0;
    if (inskrywing_VALUE==1) return gebruikernommer[plaas_INDEX];
    if (inskrywing_VALUE==2) {
        unsigned char *쪽들=stand_VALUE==1?Toestemmings_Lys:저장값[plaas_INDEX].Toestemmings_Lys;
        unsigned bladsy_COUNT=0; for (unsigned 순번=0; 순번<gebruiker_bladsy_COUNT; 순번++) if(쪽들[순번]) bladsy_COUNT++;
        return bladsy_COUNT*4;
    }
    if (inskrywing_VALUE==3) return (uint32_t)보드밀리초()-gebruiker_BEGIN_tyd[plaas_INDEX];
    if (inskrywing_VALUE==4) return 사용자누적시각[plaas_INDEX]+(stand_VALUE==1?(uint32_t)보드밀리초()-사용자실행시각[plaas_INDEX]:0);
    if (inskrywing_VALUE==5) return INDEX/4<sizeof(gebruiker_bevel_naam[0])?gebruiker_bevel_naam[plaas_INDEX][INDEX/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t inskrywing_COUNT) {
    if (Aktief || inskrywing_COUNT > 8) return (uint32_t)-22;
    전달인수개수 = inskrywing_COUNT;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t LOOKUP_INDEX, uintptr_t 현재위치, uintptr_t greep_data) {
    if (Aktief || LOOKUP_INDEX >= 전달인수개수 || 현재위치 >= 255 || 현재위치 != 전달인수길이[LOOKUP_INDEX] || !greep_data || greep_data > 255)
        return (uint32_t)-22;
    전달인수[LOOKUP_INDEX][현재위치] = greep_data;
    전달인수길이[LOOKUP_INDEX] = 현재위치 + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Klok_VALUE(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Stop_UITTELLING(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    masjien_registreer(IRQ_verspreider + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void BEGIN_UITTELLING(void) {
    uint64_t 간격 = FREQUENCY * 2, aktiveer = 1;
    마감시각 = Klok_VALUE() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(aktiveer) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned data_blokkeer = 0; data_blokkeer < 4; data_blokkeer++) {
        wortel_adres[data_blokkeer] = (uintptr_t)가운데[data_blokkeer] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t adres = ((uintptr_t)data_blokkeer << 30) | ((uintptr_t)순번 << 21);
            가운데[data_blokkeer][순번] = adres | 1 | 접근표시 | gebruiker_nee_uitvoer;
            if (adres >= 0xfc000000ul) 가운데[data_blokkeer][순번] |= nee_uitvoer_toestemming; // Device-nGnRnE
            else 가운데[data_blokkeer][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned SECOND_VALUE = 0; SECOND_VALUE < gebruiker_bladsy_COUNT / 512; SECOND_VALUE++)
        가운데[0][(gebruiker_BASE >> 21) + SECOND_VALUE] = (uintptr_t)(bladsy_Lys + SECOND_VALUE * 512) | 3;
    for (unsigned 순번 = 0; 순번 < gebruiker_bladsy_COUNT; 순번++) bladsy_Lys[순번] = (gebruiker_BASE + 순번 * bladsygrootte) | kern_bladsy;
    uint64_t Geheue_kenmerk_registreer = 0x4400, adres_Vertaling_kontrole = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Geheue_kenmerk_registreer), "r"(adres_Vertaling_kontrole), "r"((uintptr_t)wortel_adres) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t 실수저장상태 = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(실수저장상태) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    Stop_UITTELLING();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 inskrywing_p_VALUE 때만 toelaat_VALUE.
    masjien_registreer(IRQ_verspreider) = 0;
    masjien_registreer(IRQ_verspreider + 0x180) = 0xffffffff;
    masjien_registreer(IRQ_verspreider + 0x80) = 0xffffffff;
    masjien_registreer(IRQ_verspreider + 0x280) = 1u << 30;
    masjien_registreer(IRQ_verspreider + 0x41c) = 0x80808080;
    masjien_registreer(IRQ_verspreider + 0x100) = 1u << 30;
    masjien_registreer(IRQ_SVE_koppelvlak + 4) = 0xff;
    masjien_registreer(IRQ_SVE_koppelvlak + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 수 있다.
    int Sekuriteit = (masjien_registreer(IRQ_verspreider + 4) & (1u << 10)) != 0;
    masjien_registreer(IRQ_verspreider) = Sekuriteit ? 1 : 3;
    masjien_registreer(IRQ_SVE_koppelvlak) = Sekuriteit ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t TYPE_kategorie, masjien_TYPE; uint32_t 판번호;
    uint64_t inskrywing_p, program_Loopkop_OFFSET, seksie_Loopkop_OFFSET; uint32_t konfigurasie_Agtergrond_intelligente_oordragdiens;
    uint16_t 실행머리크기, program_Loopkop_inskrywing_verstel, program_Loopkop_COUNT, seksie_Loopkop_inskrywing_verstel, seksie_Loopkop_COUNT, seksie_naam_tabel_INDEX;
} 실행파일머리;
typedef struct { uint32_t TYPE_kategorie, konfigurasie_Agtergrond_intelligente_oordragdiens; uint64_t OFFSET_VALUE, adres, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(gebruiker_raam) == 272, "exception assembly layout");
static int 포함된범위(uint64_t OFFSET_VALUE, uint64_t Grootte, uint64_t beëindig_OFFSET) {
    return OFFSET_VALUE <= beëindig_OFFSET && Grootte <= beëindig_OFFSET - OFFSET_VALUE;
}
static int 부가정보검사(const unsigned char *data_plaas, size_t Grootte) {
    size_t 현재위치 = 0;
    while (포함된범위(현재위치, 12, Grootte)) {
        uint32_t 낱말들[3]; memcpy(낱말들, data_plaas + 현재위치, 12); 현재위치 += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(현재위치, 이름영역크기, Grootte) || !포함된범위(현재위치 + 이름영역크기, 설명크기, Grootte)) return 0;
        const unsigned char Naam[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Naam) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Naam); 순번++) if (data_plaas[현재위치 + 순번] != Naam[순번]) 일치 = 0;
        uint32_t 판번호 = 0;
        if (일치) memcpy(&판번호, data_plaas + 현재위치 + 이름영역크기, 4);
        if (일치 && 판번호 == 1) return 1;
        현재위치 += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *data, size_t Grootte, int 리눅스방식) {
    if (Grootte < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, data, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.TYPE_kategorie != 2 || 실행머리.masjien_TYPE != 183 || 실행머리.판번호 != 1 || 실행머리.konfigurasie_Agtergrond_intelligente_oordragdiens || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.program_Loopkop_inskrywing_verstel != sizeof(실행파일구획) || !실행머리.program_Loopkop_COUNT || 실행머리.program_Loopkop_COUNT > 16 ||
        실행머리.program_Loopkop_OFFSET < sizeof(실행머리) || !포함된범위(실행머리.program_Loopkop_OFFSET, (uint64_t)실행머리.program_Loopkop_COUNT * sizeof(실행파일구획), Grootte)) return 사용자실행파일오류;
    uint8_t 사용량[(gebruiker_foto_beëindig - gebruiker_BASE) / bladsygrootte] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.program_Loopkop_COUNT; 순번++) {
        실행파일구획 data_plaas; memcpy(&data_plaas, data + 실행머리.program_Loopkop_OFFSET + 순번 * sizeof(data_plaas), sizeof(data_plaas));
        if (data_plaas.TYPE_kategorie == 4) {
            if (!포함된범위(data_plaas.OFFSET_VALUE, data_plaas.파일영역크기, Grootte)) return 사용자실행파일오류;
            if (부가정보검사(data + data_plaas.OFFSET_VALUE, data_plaas.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (data_plaas.TYPE_kategorie == 0 || data_plaas.TYPE_kategorie == 6 || (data_plaas.TYPE_kategorie == 0x6474e551 && !(data_plaas.konfigurasie_Agtergrond_intelligente_oordragdiens & 1))) continue;
        if (data_plaas.TYPE_kategorie != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!data_plaas.기억영역크기) continue;
        if (data_plaas.konfigurasie_Agtergrond_intelligente_oordragdiens & ~7u || !(data_plaas.konfigurasie_Agtergrond_intelligente_oordragdiens & 4) || (data_plaas.konfigurasie_Agtergrond_intelligente_oordragdiens & 3) == 3 || data_plaas.파일영역크기 > data_plaas.기억영역크기 ||
            (data_plaas.파일영역크기 && !포함된범위(data_plaas.OFFSET_VALUE, data_plaas.파일영역크기, Grootte)) || data_plaas.adres < gebruiker_BASE ||
            !포함된범위(data_plaas.adres, data_plaas.기억영역크기, gebruiker_foto_beëindig) ||
            (!리눅스방식 && ((data_plaas.adres & (bladsygrootte - 1)) || (data_plaas.OFFSET_VALUE & (bladsygrootte - 1)) || data_plaas.맞춤 != bladsygrootte)) ||
            (리눅스방식 && (((data_plaas.adres ^ data_plaas.OFFSET_VALUE) & (bladsygrootte - 1)) || !data_plaas.맞춤 ||
                (data_plaas.맞춤 & (data_plaas.맞춤 - 1)) || data_plaas.맞춤 > 0x200000 || ((data_plaas.adres ^ data_plaas.OFFSET_VALUE) & (data_plaas.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (data_plaas.adres - gebruiker_BASE) / bladsygrootte;
        unsigned inskrywing_COUNT = ((data_plaas.adres & (bladsygrootte - 1)) + data_plaas.기억영역크기 + bladsygrootte - 1) / bladsygrootte;
        for (unsigned bladsy_VALUE = 첫항목; bladsy_VALUE < 첫항목 + inskrywing_COUNT; bladsy_VALUE++) {
            if (사용량[bladsy_VALUE]) return 사용자실행파일오류;
            사용량[bladsy_VALUE] = 1;
        }
        if ((data_plaas.konfigurasie_Agtergrond_intelligente_oordragdiens & 1) && 실행머리.inskrywing_p >= data_plaas.adres && 실행머리.inskrywing_p < data_plaas.adres + data_plaas.파일영역크기 && !(실행머리.inskrywing_p & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *data, size_t Grootte) { return 실행파일검사(data, Grootte, 0); }
static void bladsyuitleg(uintptr_t adres, uint64_t konfigurasie_Agtergrond_intelligente_oordragdiens, unsigned toestemmings) {
    unsigned LOOKUP_INDEX = (adres - gebruiker_BASE) / bladsygrootte;
    bladsy_Lys[LOOKUP_INDEX] = adres | konfigurasie_Agtergrond_intelligente_oordragdiens;
    Toestemmings_Lys[LOOKUP_INDEX] = toestemmings;
}
static int 사용자범위(uintptr_t adres, size_t inskrywing_COUNT, int 쓰는중) {
    if (adres < gebruiker_BASE || !포함된범위(adres, inskrywing_COUNT, gebruiker_beëindig)) return 0;
    if (!inskrywing_COUNT) return 1;
    unsigned 첫항목 = (adres - gebruiker_BASE) / bladsygrootte, 마지막 = (adres + inskrywing_COUNT - 1 - gebruiker_BASE) / bladsygrootte;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(Toestemmings_Lys[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int geval_pad(uintptr_t adres, char *Pad) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!사용자범위(adres, 1, 0)) return -14;
        Pad[순번] = *(const char *)adres++;
        if (!Pad[순번]) return 0;
    }
    return -36;
}
static intptr_t kern_maatreël(intptr_t maatreël) { return maatreël < 0 ? -오류번호 : maatreël; }
static int 대응파일기술자(uint64_t lêer_handvatsel) { return lêer_handvatsel >= 3 && lêer_handvatsel < 19 ? lêer_Lys[lêer_handvatsel - 3] : -1; }
static int 통신끝점소유(uint64_t lêer_handvatsel) { return lêer_handvatsel >= 32 && lêer_handvatsel < 56 && 통신끝점들[lêer_handvatsel - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t lengte_VALUE, struct pk_sockaddr_in *adres) {
    if (lengte_VALUE != sizeof(*adres)) return -22;
    if (!사용자범위(가리킴값, lengte_VALUE, 0)) return -14;
    memcpy(adres, (const void *)가리킴값, sizeof(*adres));
    return adres->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t lengte_wyser, pk_socklen_t *수용량) {
    if (!사용자범위(lengte_wyser, sizeof(*수용량), 1)) return -14;
    memcpy(수용량, (const void *)lengte_wyser, sizeof(*수용량));
    if (*수용량 > sizeof(struct pk_sockaddr_in)) *수용량 = sizeof(struct pk_sockaddr_in);
    if (*수용량 && !사용자범위(가리킴값, *수용량, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t lengte_wyser, pk_socklen_t 수용량, int adres, int 접속번호) {
    struct pk_sockaddr_in VALUE; memset(&VALUE, 0, sizeof(VALUE));
    VALUE.sin_family = AF_INET; VALUE.sin_port = pk_htons(접속번호); VALUE.sin_addr.s_addr = pk_htonl(adres);
    if (수용량) memcpy((void *)가리킴값, &VALUE, 수용량);
    pk_socklen_t lengte_VALUE = sizeof(VALUE); memcpy((void *)lengte_wyser, &lengte_VALUE, sizeof(lengte_VALUE));
}
extern uintptr_t bord_kanaal(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(gebruiker_raam *lêer_inskrywing) {
    uintptr_t 첫째값 = lêer_inskrywing->registreer_data[0], SECOND_VALUE = lêer_inskrywing->registreer_data[1], karakterkode = lêer_inskrywing->registreer_data[2];
    char Pad[65];
    int lêer_handvatsel, maatreël;
    switch (lêer_inskrywing->registreer_data[8]) {
    case 0: return 1; // 자체 ABI 버전
    case 1: // write: wyser 전체를 검사한 TERUG_VALUE Afvoer/Lêer verander_VALUE
        if (karakterkode > 65536) return -22;
        if (!사용자범위(SECOND_VALUE, karakterkode, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=Klok_VALUE();
            for (size_t 순번 = 0; 순번 < karakterkode; 순번++) bord_kanaal(첫째값, ((const unsigned char *)SECOND_VALUE)[순번]);
            /* 큰 tty를 그린 kern_VALUE 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(interaktief){
                마감시각+=Klok_VALUE()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(마감시각) : "memory");
            }
            return karakterkode;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t item_COUNT=karakterkode>512?512:karakterkode;for(size_t 순번=0;순번<item_COUNT;순번++)자바전문넣기(순번,((const unsigned char *)SECOND_VALUE)[순번]);return 자바흐름쓰기(첫째값,item_COUNT);
        }
        lêer_handvatsel = 대응파일기술자(첫째값); if (lêer_handvatsel < 0) return -9;
        return kern_maatreël(pk_write(lêer_handvatsel, (const void *)SECOND_VALUE, karakterkode));
    case 2:
        if (karakterkode > 65536) return -22;
        if (!사용자범위(SECOND_VALUE, karakterkode, 1)) return -14;
        if (첫째값 == 0) {
            size_t item_COUNT = 0;
            while (item_COUNT < karakterkode) {
                int karakter_VALUE = (int32_t)보드글자읽기(); if (karakter_VALUE == -2) return item_COUNT; if (karakter_VALUE < 0) break;
                ((unsigned char *)SECOND_VALUE)[item_COUNT++] = karakter_VALUE;
            }
            return item_COUNT ? (intptr_t)item_COUNT : (karakterkode ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            maatreël=자바흐름읽기(첫째값,karakterkode>512?512:karakterkode);if(maatreël>0)for(int 순번=0;순번<maatreël;순번++)((unsigned char *)SECOND_VALUE)[순번]=자바전문얻기(순번);return maatreël;
        }
        lêer_handvatsel = 대응파일기술자(첫째값); if (lêer_handvatsel < 0) return -9;
        return kern_maatreël(pk_read(lêer_handvatsel, (void *)SECOND_VALUE, karakterkode));
    case 3:
        maatreël = geval_pad(첫째값, Pad); if (maatreël) return maatreël;
        if (SECOND_VALUE > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (lêer_Lys[순번] < 0) {
            lêer_handvatsel = pk_open(Pad, (int)SECOND_VALUE, 0600);
            if (lêer_handvatsel < 0) return -오류번호;
            lêer_Lys[순번] = lêer_handvatsel; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { maatreël = 통신끝점닫기(첫째값); if (!maatreël) 통신끝점들[첫째값 - 32] = 0; return maatreël; }
        lêer_handvatsel = 대응파일기술자(첫째값); if (lêer_handvatsel < 0) return -9;
        maatreël = pk_close(lêer_handvatsel); if (!maatreël) lêer_Lys[첫째값 - 3] = -1;
        return kern_maatreël(maatreël);
    case 5:
        lêer_handvatsel = 대응파일기술자(첫째값); if (lêer_handvatsel < 0) return -9;
        if (karakterkode > 2) return -22;
        return kern_maatreël(pk_lseek(lêer_handvatsel, (int64_t)SECOND_VALUE, karakterkode));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 gebruiker RW/NX 힙, 새로 노출되는 페이지는 0으로 inisialiseer
        if (!첫째값) return 동적기억끝;
        if (첫째값 < gebruiker_foto_beëindig || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + bladsygrootte - 1) & ~(bladsygrootte - 1);
        uintptr_t 새쪽들 = (첫째값 + bladsygrootte - 1) & ~(bladsygrootte - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t data_plaas = 이전쪽들; data_plaas < 새쪽들; data_plaas += bladsygrootte) bladsyuitleg(data_plaas, kern_bladsy, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t data_plaas = 이전쪽들; data_plaas < 새쪽들; data_plaas += bladsygrootte) bladsyuitleg(data_plaas, gebruiker_lees_skryf, 3);
        } else {
            for (uintptr_t data_plaas = 새쪽들; data_plaas < 이전쪽들; data_plaas += bladsygrootte) {
                bladsy_Lys[(data_plaas - gebruiker_BASE) / bladsygrootte] = 0; Toestemmings_Lys[(data_plaas - gebruiker_BASE) / bladsygrootte] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        lêer_handvatsel = 대응파일기술자(첫째값); return lêer_handvatsel < 0 ? -9 : kern_maatreël(pk_size(lêer_handvatsel));
    case 10:
        lêer_handvatsel = 대응파일기술자(첫째값); return lêer_handvatsel < 0 ? -9 : kern_maatreël(pk_ftruncate(lêer_handvatsel, (int64_t)SECOND_VALUE));
    case 11:
        maatreël = geval_pad(첫째값, Pad); return maatreël ? maatreël : kern_maatreël(pk_unlink(Pad));
    case 12:
        lêer_handvatsel = 대응파일기술자(첫째값); return lêer_handvatsel < 0 ? -9 : kern_maatreël(pk_fsync(lêer_handvatsel));
    case 13: { // 그래픽 기초 API: gebruiker 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = lêer_inskrywing->registreer_data[3], 높이값 = lêer_inskrywing->registreer_data[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SECOND_VALUE > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - SECOND_VALUE) return -22;
        for (uintptr_t Y_koördinaat = SECOND_VALUE; Y_koördinaat < SECOND_VALUE + 높이값; Y_koördinaat++) for (uintptr_t x_koördinaat = 첫째값; x_koördinaat < 첫째값 + 너비값; x_koördinaat++) bord_pieksel(x_koördinaat, Y_koördinaat, karakterkode);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=item_COUNT; args(index,buffer,capacity)=UTF-8 lengte_VALUE
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (karakterkode <= 전달인수길이[첫째값]) return -36;
        if (!사용자범위(SECOND_VALUE, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SECOND_VALUE, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;interaktief=1;return bord_Terminaal(13);}
        if(첫째값==2){interaktief=0;return 0;}
        if(첫째값==3)return bord_Terminaal(13);
        if(첫째값!=1||!interaktief)return -22;
        maatreël=(int32_t)보드글자읽기();
        if(maatreël==-4096)return maatreël;
        BEGIN_UITTELLING();return maatreël<0?-11:maatreël;
    case 17: { // 유한한 협력 wag_VALUE: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t beëindig_tyd = Klok_VALUE() + FREQUENCY * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Klok_VALUE() < beëindig_tyd);
        BEGIN_UITTELLING(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 부모·빈 폴더를 검사한다.
        if (SECOND_VALUE > 2) return -22;
        maatreël = geval_pad(첫째값, Pad); if (maatreël) return maatreël;
        unsigned lengte_VALUE = 0; while (Pad[lengte_VALUE]) lengte_VALUE++;
        maatreël = 자바경로시작(lengte_VALUE); if (maatreël < 0) return maatreël;
        for (unsigned 순번 = 0; 순번 < lengte_VALUE; 순번++) 자바경로바이트(순번, (unsigned char)Pad[순번]);
        return SECOND_VALUE == 0 ? 자바항목종류() : SECOND_VALUE == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int karakter_VALUE=(int32_t)보드글자읽기();if(karakter_VALUE==-4096)return karakter_VALUE;if(karakter_VALUE>=0)화면누름(eienaar_objek,karakter_VALUE);BEGIN_UITTELLING();}
        if(첫째값==3&&karakterkode){if(!자바셸대화형())return -95;interaktief=1;bord_Terminaal(300);}
        return 화면호출(eienaar_objek,첫째값,SECOND_VALUE,karakterkode,lêer_inskrywing->registreer_data[3],lêer_inskrywing->registreer_data[4],lêer_inskrywing->registreer_data[5]);
    case 21:
        if(karakterkode>127)return -22;if(!사용자범위(SECOND_VALUE,karakterkode*sizeof(uint32_t),0))return -14;
        return 화면글(eienaar_objek,첫째값,(const uint32_t *)SECOND_VALUE,karakterkode);
    case 22: // 화면 Grootte navraag_VALUE: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SECOND_VALUE==SOCK_STREAM&&(karakterkode==0||karakterkode==6))maatreël=자바흐름만들기();
        else if(SECOND_VALUE==SOCK_DGRAM&&(karakterkode==0||karakterkode==IPPROTO_UDP))maatreël=자바전문만들기(첫째값,SECOND_VALUE,karakterkode);
        else return -93;
        if (maatreël >= 32 && maatreël < 56) 통신끝점들[maatreël - 32] = 1;
        return maatreël;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in adres;
        maatreël = 주소입력(SECOND_VALUE, karakterkode, &adres); if (maatreël) return maatreël;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(adres.sin_addr.s_addr),pk_htons(adres.sin_port)):자바전문묶기(첫째값, pk_htonl(adres.sin_addr.s_addr), pk_htons(adres.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (lêer_inskrywing->registreer_data[3]) return -95;
        if (karakterkode > 512) return -90;
        if (karakterkode && !사용자범위(SECOND_VALUE, karakterkode, 0)) return -14;
        struct pk_sockaddr_in adres;
        maatreël = 주소입력(lêer_inskrywing->registreer_data[4], lêer_inskrywing->registreer_data[5], &adres); if (maatreël) return maatreël;
        for (unsigned 순번 = 0; 순번 < karakterkode; 순번++) 자바전문넣기(순번, ((const unsigned char *)SECOND_VALUE)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(adres.sin_addr.s_addr), pk_htons(adres.sin_port), karakterkode);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (lêer_inskrywing->registreer_data[3]) return -95;
        if (karakterkode > 512) return -90;
        if (karakterkode && !사용자범위(SECOND_VALUE, karakterkode, 1)) return -14;
        pk_socklen_t 수용량 = 0;
        if (lêer_inskrywing->registreer_data[4]) { maatreël = 주소출력검사(lêer_inskrywing->registreer_data[4], lêer_inskrywing->registreer_data[5], &수용량); if (maatreël) return maatreël; }
        maatreël = 자바전문받기(첫째값, karakterkode); if (maatreël < 0) return maatreël;
        for (int 순번 = 0; 순번 < maatreël; 순번++) ((unsigned char *)SECOND_VALUE)[순번] = 자바전문얻기(순번);
        if (lêer_inskrywing->registreer_data[4]) 주소출력(lêer_inskrywing->registreer_data[4], lêer_inskrywing->registreer_data[5], 수용량, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return maatreël;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t 수용량;
        maatreël = 주소출력검사(SECOND_VALUE, karakterkode, &수용량); if (maatreël) return maatreël;
        주소출력(SECOND_VALUE,karakterkode,수용량,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in adres;
        maatreël=주소입력(SECOND_VALUE,karakterkode,&adres);if(maatreël)return maatreël;
        return 자바흐름연결(첫째값,pk_htonl(adres.sin_addr.s_addr),pk_htons(adres.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,SECOND_VALUE):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(SECOND_VALUE||karakterkode)return -95;maatreël=자바흐름연결받기(첫째값);if(maatreël>=40&&maatreël<56)통신끝점들[maatreël-32]=1;return maatreël;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(gebruiker_raam *lêer_inskrywing) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(lêer_inskrywing) : 자체체계호출(lêer_inskrywing);
}
static void teruggee_kern(gebruiker_raam *lêer_inskrywing, int maatreël) {
    Stop_UITTELLING();
    lêer_inskrywing->registreer_data[0] = (uint64_t)(int64_t)maatreël;
    lêer_inskrywing->bevel_plaas = (uintptr_t)gebruiker_teruggee;
    lêer_inskrywing->stand_CODE = 0x3c5; // EL1h, DAIF masked
}
int gebruiker_uitsondering(gebruiker_raam *lêer_inskrywing, unsigned intersep) {
    if (!Aktief || (lêer_inskrywing->stand_CODE & 15) != 0) return 0;
    if (intersep) {
        uint32_t 승인값 = masjien_registreer(IRQ_SVE_koppelvlak + 0xc), waarde_VALUE = 승인값 & 1023;
        if (waarde_VALUE == 30) { teruggee_kern(lêer_inskrywing, gebruiker_UITTELLING); masjien_registreer(IRQ_SVE_koppelvlak + 0x10) = 승인값; return 1; }
        if (waarde_VALUE < 1020) masjien_registreer(IRQ_SVE_koppelvlak + 0x10) = 승인값;
        return 1;
    }
    uint64_t uitsondering_stand; __asm__ volatile("mrs %0, esr_el1" : "=r"(uitsondering_stand));
    if (Klok_VALUE() >= 마감시각) { teruggee_kern(lêer_inskrywing, gebruiker_UITTELLING); return 1; }
    unsigned uitsondering_kategorie = uitsondering_stand >> 26;
    if (uitsondering_kategorie == 0x15 && (uitsondering_stand & 0xffff) == 0) {
        if (리눅스규약 ? lêer_inskrywing->registreer_data[8] == 93 || lêer_inskrywing->registreer_data[8] == 94 : lêer_inskrywing->registreer_data[8] == 6) teruggee_kern(lêer_inskrywing, (int)(lêer_inskrywing->registreer_data[0] & 255));
        else {
            intptr_t maatreël=체계호출(lêer_inskrywing);
            if(maatreël==-4096&&interaktief){
                저장값[eienaar_objek].실행틀=*lêer_inskrywing;저장값[eienaar_objek].실행틀.bevel_plaas-=4;
                사용자실수보관(저장값[eienaar_objek].실수저장상태);teruggee_kern(lêer_inskrywing,사용자중단됨);
            }else lêer_inskrywing->registreer_data[0]=(uint64_t)maatreël;
        }
    } else teruggee_kern(lêer_inskrywing, uitsondering_kategorie == 0x24 ? gebruiker_data_fout : uitsondering_kategorie == 0x20 ? 사용자실행오류 : gebruiker_ongeldig_instruksie);
    return 1;
}

// 생성된 const ELF Groep_VALUE: 실행은 반드시 program_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *data; size_t Grootte; unsigned 전달값; } program;
#include "programs.h"
static void *flitsbeeld(unsigned plaas_INDEX){return (void *)(0x04000000ul+plaas_INDEX*(gebruiker_beëindig-gebruiker_BASE));}
static int Klaar_program(int maatreël){
    사용자누적시각[eienaar_objek]+=(uint32_t)보드밀리초()-사용자실행시각[eienaar_objek];
    Stop_UITTELLING();Aktief=0;
    if(maatreël==사용자중단됨){
        저장된작업 *string_data=&저장값[eienaar_objek];string_data->멈춤상태=1;string_data->interaktief=interaktief;string_data->리눅스규약=리눅스규약;string_data->동적기억공간=동적기억끝;string_data->인수개수=전달인수개수;
        memcpy(string_data->Toestemmings_Lys,Toestemmings_Lys,sizeof(Toestemmings_Lys));memcpy(string_data->lêer_Lys,lêer_Lys,sizeof(lêer_Lys));memcpy(string_data->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(string_data->argument_ARRAY,전달인수,sizeof(전달인수));memcpy(string_data->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<gebruiker_bladsy_COUNT;순번++)if(Toestemmings_Lys[순번])memcpy((unsigned char *)flitsbeeld(eienaar_objek)+순번*bladsygrootte,(void *)(gebruiker_BASE+순번*bladsygrootte),bladsygrootte);
    }else{
        저장값[eienaar_objek].멈춤상태=0;화면초기화(eienaar_objek);
        for(unsigned 순번=0;순번<16;순번++)if(lêer_Lys[순번]>=0)pk_close(lêer_Lys[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<gebruiker_bladsy_COUNT;순번++){bladsy_Lys[순번]=0;Toestemmings_Lys[순번]=0;}변환표맞추기();return maatreël;
}
uintptr_t bord_gebruikersbeheer(uintptr_t Aksie){
    unsigned plaas_INDEX=Aksie&15;if(plaas_INDEX>=4||Aktief)return (uint32_t)-22;
    저장된작업 *string_data=&저장값[plaas_INDEX];
    if(Aksie>=32){if(string_data->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(string_data->lêer_Lys[순번]>=0)pk_close(string_data->lêer_Lys[순번]);for(unsigned 순번=0;순번<24;순번++)if(string_data->통신끝점들[순번])통신끝점닫기(순번+32);}string_data->멈춤상태=0;화면초기화(plaas_INDEX);return 0;}
    if(Aksie>=16)return string_data->멈춤상태;
    if(!string_data->멈춤상태)return (uint32_t)-22;
    eienaar_objek=plaas_INDEX;interaktief=string_data->interaktief;리눅스규약=string_data->리눅스규약;동적기억끝=string_data->동적기억공간;전달인수개수=string_data->인수개수;
    memcpy(lêer_Lys,string_data->lêer_Lys,sizeof(lêer_Lys));memcpy(통신끝점들,string_data->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,string_data->argument_ARRAY,sizeof(전달인수));memcpy(전달인수길이,string_data->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<gebruiker_bladsy_COUNT;순번++)bladsy_Lys[순번]=(gebruiker_BASE+순번*bladsygrootte)|kern_bladsy;변환표맞추기();
    memset((void *)gebruiker_BASE,0,gebruiker_beëindig-gebruiker_BASE);
    for(unsigned 순번=0;순번<gebruiker_bladsy_COUNT;순번++)if(string_data->Toestemmings_Lys[순번])memcpy((void *)(gebruiker_BASE+순번*bladsygrootte),(unsigned char *)flitsbeeld(plaas_INDEX)+순번*bladsygrootte,bladsygrootte);
    memcpy(Toestemmings_Lys,string_data->Toestemmings_Lys,sizeof(Toestemmings_Lys));
    for(unsigned 순번=0;순번<gebruiker_bladsy_COUNT;순번++){unsigned data_plaas=Toestemmings_Lys[순번];bladsy_Lys[순번]=data_plaas?(gebruiker_BASE+순번*bladsygrootte)|(data_plaas==3?gebruiker_lees_skryf:data_plaas==5?사용자읽고실행:gebruiker_leesalleen):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");Aktief=1;string_data->멈춤상태=0;BEGIN_UITTELLING();
    사용자실행시각[eienaar_objek]=보드밀리초();
    return (uint32_t)Klaar_program(gebruiker_CV(&string_data->실행틀,string_data->실수저장상태));
}
static int ry_program(const unsigned char *data, size_t Grootte, unsigned 전달값, int 리눅스방식, const char *Naam) {
    if (Aktief) return -16;
    eienaar_objek=bord_Terminaal(11);if(eienaar_objek<0||eienaar_objek>3||저장값[eienaar_objek].멈춤상태)return -16;interaktief=0;
    int 유효함 = 실행파일검사(data, Grootte, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned naam_INDEX=0;
    while (*Naam && naam_INDEX<31) gebruiker_bevel_naam[eienaar_objek][naam_INDEX++]=(unsigned char)*Naam++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (naam_INDEX) gebruiker_bevel_naam[eienaar_objek][naam_INDEX++]=' ';
        for (unsigned plaas_INDEX=0; plaas_INDEX<전달인수길이[0]; plaas_INDEX++) gebruiker_bevel_naam[eienaar_objek][naam_INDEX++]=전달인수[0][plaas_INDEX];
    }
    gebruiker_bevel_naam[eienaar_objek][naam_INDEX]=0; gebruikernommer[eienaar_objek]=Volgende_gebruikernommer++;
    if (Volgende_gebruikernommer>0x7fffffffu) Volgende_gebruikernommer=10;
    gebruiker_BEGIN_tyd[eienaar_objek]=보드밀리초(); 사용자누적시각[eienaar_objek]=0;
    for (unsigned 순번 = 0; 순번 < gebruiker_bladsy_COUNT; 순번++) bladsy_Lys[순번] = (gebruiker_BASE + 순번 * bladsygrootte) | kern_bladsy;
    변환표맞추기();
    memset((void *)gebruiker_BASE, 0, gebruiker_beëindig - gebruiker_BASE);
    memset(Toestemmings_Lys, 0, sizeof(Toestemmings_Lys));
    실행파일머리 실행머리; memcpy(&실행머리, data, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.program_Loopkop_COUNT; 순번++) {
        실행파일구획 data_plaas; memcpy(&data_plaas, data + 실행머리.program_Loopkop_OFFSET + 순번 * sizeof(data_plaas), sizeof(data_plaas));
        if (data_plaas.TYPE_kategorie != 1 || !data_plaas.기억영역크기) continue;
        if (data_plaas.파일영역크기) memcpy((void *)(uintptr_t)data_plaas.adres, data + data_plaas.OFFSET_VALUE, data_plaas.파일영역크기);
        for (uintptr_t 현재위치 = data_plaas.adres & ~(bladsygrootte - 1); 현재위치 < data_plaas.adres + data_plaas.기억영역크기; 현재위치 += bladsygrootte) {
            Toestemmings_Lys[(현재위치 - gebruiker_BASE) / bladsygrootte] = (data_plaas.konfigurasie_Agtergrond_intelligente_oordragdiens & 2) ? 3 : ((data_plaas.konfigurasie_Agtergrond_intelligente_oordragdiens & 1) ? 5 : 1);
        }
    }
    for (uintptr_t 현재위치 = gebruiker_Stapel_adres; 현재위치 < gebruiker_beëindig; 현재위치 += bladsygrootte) Toestemmings_Lys[(현재위치 - gebruiker_BASE) / bladsygrootte] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.inskrywing_p) : gebruiker_beëindig;
    for (unsigned 순번 = 0; 순번 < gebruiker_bladsy_COUNT; 순번++) {
        unsigned toestemmings = Toestemmings_Lys[순번];
        bladsy_Lys[순번] = toestemmings ? (gebruiker_BASE + 순번 * bladsygrootte) | (toestemmings == 3 ? gebruiker_lees_skryf : toestemmings == 5 ? 사용자읽고실행 : gebruiker_leesalleen) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) lêer_Lys[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = gebruiker_foto_beëindig;
    Aktief = 1; BEGIN_UITTELLING();
    사용자실행시각[eienaar_objek]=보드밀리초();
    int maatreël = gebruiker_invoer(실행머리.inskrywing_p, 초기쌓임공간, 전달값);
    return Klaar_program(maatreël);
}
uintptr_t bord_gebruiker_ry(uintptr_t LOOKUP_INDEX) {
    if (LOOKUP_INDEX >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Naam=LOOKUP_INDEX==10?"javac":LOOKUP_INDEX==11?"java":LOOKUP_INDEX==12?"python":LOOKUP_INDEX==13?"vi":LOOKUP_INDEX==14?"jar":LOOKUP_INDEX==15?"cc":LOOKUP_INDEX==16?"jaot":"ELF";
    return (uint32_t)ry_program(실행항목들[LOOKUP_INDEX].data, 실행항목들[LOOKUP_INDEX].Grootte, 실행항목들[LOOKUP_INDEX].전달값, 0, Naam);
}
static uintptr_t uitvoer_lêer(int 리눅스방식) {
    static unsigned char foto[16384];
    if (Aktief || !전달인수개수) return (uint32_t)-22;
    int lêer_handvatsel = pk_open((const char *)전달인수[0], leesalleen_VALUE, 0);
    if (lêer_handvatsel < 0) return (uint32_t)-오류번호;
    int Grootte = pk_size(lêer_handvatsel);
    if (Grootte < 0 || (unsigned)Grootte > sizeof(foto)) { pk_close(lêer_handvatsel); return (uint32_t)-27; }
    int RECEIVED_COUNT = pk_read(lêer_handvatsel, foto, Grootte); pk_close(lêer_handvatsel);
    if (RECEIVED_COUNT != Grootte) return (uint32_t)-5;
    return (uint32_t)ry_program(foto, Grootte, 0, 리눅스방식, "");
}
uintptr_t bord_gebruiker_lêer(void) { return uitvoer_lêer(0); }
uintptr_t 보드사용자리눅스파일(void) { return uitvoer_lêer(1); }
uintptr_t bord_gebruiker_valideer(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].data, 잘못된실행항목들[순번].Grootte) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
