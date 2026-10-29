#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 keyra_skipun vél lag_VALUE. Skrá gögn/정책은 기존 AOT Java 커널에 위임한다.
#include "notandi.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../Net_bunki/Net_bunki.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define vél_skrá(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_dreifingaraðili 0xff841000ul
#define IRQ_örgjörvi_viðmót 0xff842000ul
#define síðustærð 4096ul
#define 접근표시 (1ul << 10)
#define Nei_keyra_leyfi (1ul << 53)
#define notandi_Nei_keyra (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | 접근표시)
#define kjarni_síða (3ul | 보통기억 | Nei_keyra_leyfi | notandi_Nei_keyra)
#define notandi_les_skrifheimild (3ul | 보통기억 | (1ul << 6) | Nei_keyra_leyfi | notandi_Nei_keyra)
#define notandi_skrifvarið (3ul | 보통기억 | (3ul << 6) | Nei_keyra_leyfi | notandi_Nei_keyra)
#define 사용자읽고실행 (3ul | 보통기억 | (3ul << 6) | Nei_keyra_leyfi)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t bretti_díll(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t bretti_Endastöð(uintptr_t);
extern int Endastöð_Í_bið(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int notandi_ferilskrá(notandi_ramma *,void *);
extern void 사용자실수보관(void *);
extern int notandi_slá_inn(uintptr_t færsla_P, uintptr_t bunki_geymsla, uintptr_t 전달값);
extern void notandi_skila(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t rót_slóð[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t síða_Listi[notandi_síða_COUNT] __attribute__((aligned(4096)));
static uint8_t Heimildir_Listi[notandi_síða_COUNT];
static int Laus, skrá_Listi[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned skrá_hald){return skrá_hald<40?자바전문닫기(skrá_hald):자바흐름닫기(skrá_hald);}
static uint64_t FREQUENCY, 마감시각;
static uintptr_t 동적기억끝;
// kjarni_VALUE 셸이 준비한 UTF-8 Viðföng. EL0에는 afrita_VALUE 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,gagnvirkur,리눅스규약,skrá_Listi[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char frumbreyta_ARRAY[8][256],Heimildir_Listi[notandi_síða_COUNT];
    uintptr_t 동적기억공간; notandi_ramma 실행틀;
    unsigned char 실수저장상태[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int eigandi_hlutur,gagnvirkur;
static uint32_t notandanúmer[4], notandi_Opna_TIME[4], 사용자누적시각[4], 사용자실행시각[4], Áfram_notandanúmer=10;
static unsigned char notandi_skipun_heiti[4][288];
uint32_t 사용자상태읽기(unsigned færsla_VALUE, unsigned INDEX) {
    unsigned staða_INDEX=INDEX&3;
    int staða_VALUE_e10195a1=(Laus && eigandi_hlutur==(int)staða_INDEX) ? 1 : 저장값[staða_INDEX].멈춤상태 ? 2 : 0;
    if (færsla_VALUE==0) return staða_VALUE_e10195a1;
    if (!staða_VALUE_e10195a1) return 0;
    if (færsla_VALUE==1) return notandanúmer[staða_INDEX];
    if (færsla_VALUE==2) {
        unsigned char *쪽들=staða_VALUE_e10195a1==1?Heimildir_Listi:저장값[staða_INDEX].Heimildir_Listi;
        unsigned síða_COUNT=0; for (unsigned 순번=0; 순번<notandi_síða_COUNT; 순번++) if(쪽들[순번]) síða_COUNT++;
        return síða_COUNT*4;
    }
    if (færsla_VALUE==3) return (uint32_t)보드밀리초()-notandi_Opna_TIME[staða_INDEX];
    if (færsla_VALUE==4) return 사용자누적시각[staða_INDEX]+(staða_VALUE_e10195a1==1?(uint32_t)보드밀리초()-사용자실행시각[staða_INDEX]:0);
    if (færsla_VALUE==5) return INDEX/4<sizeof(notandi_skipun_heiti[0])?notandi_skipun_heiti[staða_INDEX][INDEX/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t færsla_COUNT) {
    if (Laus || færsla_COUNT > 8) return (uint32_t)-22;
    전달인수개수 = færsla_COUNT;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t LOOKUP_INDEX, uintptr_t 현재위치, uintptr_t bæti_gögn) {
    if (Laus || LOOKUP_INDEX >= 전달인수개수 || 현재위치 >= 255 || 현재위치 != 전달인수길이[LOOKUP_INDEX] || !bæti_gögn || bæti_gögn > 255)
        return (uint32_t)-22;
    전달인수[LOOKUP_INDEX][현재위치] = bæti_gögn;
    전달인수길이[LOOKUP_INDEX] = 현재위치 + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t klukka_VALUE(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Stopp_TIMEOUT(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    vél_skrá(IRQ_dreifingaraðili + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void Opna_TIMEOUT(void) {
    uint64_t 간격 = FREQUENCY * 2, kveikja = 1;
    마감시각 = klukka_VALUE() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(kveikja) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned gögn_útiloka = 0; gögn_útiloka < 4; gögn_útiloka++) {
        rót_slóð[gögn_útiloka] = (uintptr_t)가운데[gögn_útiloka] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t slóð = ((uintptr_t)gögn_útiloka << 30) | ((uintptr_t)순번 << 21);
            가운데[gögn_útiloka][순번] = slóð | 1 | 접근표시 | notandi_Nei_keyra;
            if (slóð >= 0xfc000000ul) 가운데[gögn_útiloka][순번] |= Nei_keyra_leyfi; // Device-nGnRnE
            else 가운데[gögn_útiloka][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned SECOND_VALUE = 0; SECOND_VALUE < notandi_síða_COUNT / 512; SECOND_VALUE++)
        가운데[0][(notandi_BASE >> 21) + SECOND_VALUE] = (uintptr_t)(síða_Listi + SECOND_VALUE * 512) | 3;
    for (unsigned 순번 = 0; 순번 < notandi_síða_COUNT; 순번++) síða_Listi[순번] = (notandi_BASE + 순번 * síðustærð) | kjarni_síða;
    uint64_t Minni_eigind_skrá = 0x4400, slóð_Þýðing_stýring = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Minni_eigind_skrá), "r"(slóð_Þýðing_stýring), "r"((uintptr_t)rót_slóð) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t 실수저장상태 = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(실수저장상태) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    Stopp_TIMEOUT();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 færsla_P_VALUE 때만 leyfa_VALUE.
    vél_skrá(IRQ_dreifingaraðili) = 0;
    vél_skrá(IRQ_dreifingaraðili + 0x180) = 0xffffffff;
    vél_skrá(IRQ_dreifingaraðili + 0x80) = 0xffffffff;
    vél_skrá(IRQ_dreifingaraðili + 0x280) = 1u << 30;
    vél_skrá(IRQ_dreifingaraðili + 0x41c) = 0x80808080;
    vél_skrá(IRQ_dreifingaraðili + 0x100) = 1u << 30;
    vél_skrá(IRQ_örgjörvi_viðmót + 4) = 0xff;
    vél_skrá(IRQ_örgjörvi_viðmót + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 númer 있다.
    int Öryggi = (vél_skrá(IRQ_dreifingaraðili + 4) & (1u << 10)) != 0;
    vél_skrá(IRQ_dreifingaraðili) = Öryggi ? 1 : 3;
    vél_skrá(IRQ_örgjörvi_viðmót) = Öryggi ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t TYPE_tegund, vél_TYPE; uint32_t útgáfa_númer;
    uint64_t færsla_P, forrit_Haus_OFFSET, hluti_Haus_OFFSET; uint32_t afbrigði_Background_Intelligent_Transfer_Service;
    uint16_t 실행머리크기, forrit_Haus_færsla_breyta_stærð, forrit_Haus_COUNT, hluti_Haus_færsla_breyta_stærð, hluti_Haus_COUNT, hluti_heiti_tafla_INDEX;
} 실행파일머리;
typedef struct { uint32_t TYPE_tegund, afbrigði_Background_Intelligent_Transfer_Service; uint64_t OFFSET_VALUE, slóð, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(notandi_ramma) == 272, "exception assembly layout");
static int 포함된범위(uint64_t OFFSET_VALUE, uint64_t Stærð, uint64_t ljúka_OFFSET) {
    return OFFSET_VALUE <= ljúka_OFFSET && Stærð <= ljúka_OFFSET - OFFSET_VALUE;
}
static int 부가정보검사(const unsigned char *gögn_staða, size_t Stærð) {
    size_t 현재위치 = 0;
    while (포함된범위(현재위치, 12, Stærð)) {
        uint32_t 낱말들[3]; memcpy(낱말들, gögn_staða + 현재위치, 12); 현재위치 += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(현재위치, 이름영역크기, Stærð) || !포함된범위(현재위치 + 이름영역크기, 설명크기, Stærð)) return 0;
        const unsigned char Heiti[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Heiti) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Heiti); 순번++) if (gögn_staða[현재위치 + 순번] != Heiti[순번]) 일치 = 0;
        uint32_t útgáfa_númer = 0;
        if (일치) memcpy(&útgáfa_númer, gögn_staða + 현재위치 + 이름영역크기, 4);
        if (일치 && útgáfa_númer == 1) return 1;
        현재위치 += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *gögn, size_t Stærð, int 리눅스방식) {
    if (Stærð < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, gögn, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.TYPE_tegund != 2 || 실행머리.vél_TYPE != 183 || 실행머리.útgáfa_númer != 1 || 실행머리.afbrigði_Background_Intelligent_Transfer_Service || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.forrit_Haus_færsla_breyta_stærð != sizeof(실행파일구획) || !실행머리.forrit_Haus_COUNT || 실행머리.forrit_Haus_COUNT > 16 ||
        실행머리.forrit_Haus_OFFSET < sizeof(실행머리) || !포함된범위(실행머리.forrit_Haus_OFFSET, (uint64_t)실행머리.forrit_Haus_COUNT * sizeof(실행파일구획), Stærð)) return 사용자실행파일오류;
    uint8_t 사용량[(notandi_mynd_ljúka - notandi_BASE) / síðustærð] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.forrit_Haus_COUNT; 순번++) {
        실행파일구획 gögn_staða; memcpy(&gögn_staða, gögn + 실행머리.forrit_Haus_OFFSET + 순번 * sizeof(gögn_staða), sizeof(gögn_staða));
        if (gögn_staða.TYPE_tegund == 4) {
            if (!포함된범위(gögn_staða.OFFSET_VALUE, gögn_staða.파일영역크기, Stærð)) return 사용자실행파일오류;
            if (부가정보검사(gögn + gögn_staða.OFFSET_VALUE, gögn_staða.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (gögn_staða.TYPE_tegund == 0 || gögn_staða.TYPE_tegund == 6 || (gögn_staða.TYPE_tegund == 0x6474e551 && !(gögn_staða.afbrigði_Background_Intelligent_Transfer_Service & 1))) continue;
        if (gögn_staða.TYPE_tegund != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!gögn_staða.기억영역크기) continue;
        if (gögn_staða.afbrigði_Background_Intelligent_Transfer_Service & ~7u || !(gögn_staða.afbrigði_Background_Intelligent_Transfer_Service & 4) || (gögn_staða.afbrigði_Background_Intelligent_Transfer_Service & 3) == 3 || gögn_staða.파일영역크기 > gögn_staða.기억영역크기 ||
            (gögn_staða.파일영역크기 && !포함된범위(gögn_staða.OFFSET_VALUE, gögn_staða.파일영역크기, Stærð)) || gögn_staða.slóð < notandi_BASE ||
            !포함된범위(gögn_staða.slóð, gögn_staða.기억영역크기, notandi_mynd_ljúka) ||
            (!리눅스방식 && ((gögn_staða.slóð & (síðustærð - 1)) || (gögn_staða.OFFSET_VALUE & (síðustærð - 1)) || gögn_staða.맞춤 != síðustærð)) ||
            (리눅스방식 && (((gögn_staða.slóð ^ gögn_staða.OFFSET_VALUE) & (síðustærð - 1)) || !gögn_staða.맞춤 ||
                (gögn_staða.맞춤 & (gögn_staða.맞춤 - 1)) || gögn_staða.맞춤 > 0x200000 || ((gögn_staða.slóð ^ gögn_staða.OFFSET_VALUE) & (gögn_staða.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (gögn_staða.slóð - notandi_BASE) / síðustærð;
        unsigned færsla_COUNT = ((gögn_staða.slóð & (síðustærð - 1)) + gögn_staða.기억영역크기 + síðustærð - 1) / síðustærð;
        for (unsigned síða_VALUE = 첫항목; síða_VALUE < 첫항목 + færsla_COUNT; síða_VALUE++) {
            if (사용량[síða_VALUE]) return 사용자실행파일오류;
            사용량[síða_VALUE] = 1;
        }
        if ((gögn_staða.afbrigði_Background_Intelligent_Transfer_Service & 1) && 실행머리.færsla_P >= gögn_staða.slóð && 실행머리.færsla_P < gögn_staða.slóð + gögn_staða.파일영역크기 && !(실행머리.færsla_P & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *gögn, size_t Stærð) { return 실행파일검사(gögn, Stærð, 0); }
static void útlit_síðu(uintptr_t slóð, uint64_t afbrigði_Background_Intelligent_Transfer_Service, unsigned heimildir) {
    unsigned LOOKUP_INDEX = (slóð - notandi_BASE) / síðustærð;
    síða_Listi[LOOKUP_INDEX] = slóð | afbrigði_Background_Intelligent_Transfer_Service;
    Heimildir_Listi[LOOKUP_INDEX] = heimildir;
}
static int 사용자범위(uintptr_t slóð, size_t færsla_COUNT, int 쓰는중) {
    if (slóð < notandi_BASE || !포함된범위(slóð, færsla_COUNT, notandi_ljúka)) return 0;
    if (!færsla_COUNT) return 1;
    unsigned 첫항목 = (slóð - notandi_BASE) / síðustærð, 마지막 = (slóð + færsla_COUNT - 1 - notandi_BASE) / síðustærð;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(Heimildir_Listi[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int afrita_slóð(uintptr_t slóð, char *SLÓÐ) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!사용자범위(slóð, 1, 0)) return -14;
        SLÓÐ[순번] = *(const char *)slóð++;
        if (!SLÓÐ[순번]) return 0;
    }
    return -36;
}
static intptr_t kjarni_mæld_stærð(intptr_t NIÐURSTAÐA) { return NIÐURSTAÐA < 0 ? -villa_númer : NIÐURSTAÐA; }
static int 대응파일기술자(uint64_t skrá_hald) { return skrá_hald >= 3 && skrá_hald < 19 ? skrá_Listi[skrá_hald - 3] : -1; }
static int 통신끝점소유(uint64_t skrá_hald) { return skrá_hald >= 32 && skrá_hald < 56 && 통신끝점들[skrá_hald - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t lengd_VALUE, struct pk_sockaddr_in *slóð) {
    if (lengd_VALUE != sizeof(*slóð)) return -22;
    if (!사용자범위(가리킴값, lengd_VALUE, 0)) return -14;
    memcpy(slóð, (const void *)가리킴값, sizeof(*slóð));
    return slóð->sin_family == AF_INET ? 0 : -97;
}
static int slóð_úttak_athuga(uintptr_t 가리킴값, uintptr_t lengd_bendill, pk_socklen_t *biðminni_afkastageta) {
    if (!사용자범위(lengd_bendill, sizeof(*biðminni_afkastageta), 1)) return -14;
    memcpy(biðminni_afkastageta, (const void *)lengd_bendill, sizeof(*biðminni_afkastageta));
    if (*biðminni_afkastageta > sizeof(struct pk_sockaddr_in)) *biðminni_afkastageta = sizeof(struct pk_sockaddr_in);
    if (*biðminni_afkastageta && !사용자범위(가리킴값, *biðminni_afkastageta, 1)) return -14;
    return 0;
}
static void slóð_úttak(uintptr_t 가리킴값, uintptr_t lengd_bendill, pk_socklen_t biðminni_afkastageta, int slóð, int tengisnúmer) {
    struct pk_sockaddr_in VALUE; memset(&VALUE, 0, sizeof(VALUE));
    VALUE.sin_family = AF_INET; VALUE.sin_port = pk_htons(tengisnúmer); VALUE.sin_addr.s_addr = pk_htonl(slóð);
    if (biðminni_afkastageta) memcpy((void *)가리킴값, &VALUE, biðminni_afkastageta);
    pk_socklen_t lengd_VALUE = sizeof(VALUE); memcpy((void *)lengd_bendill, &lengd_VALUE, sizeof(lengd_VALUE));
}
extern uintptr_t bretti_rás(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(notandi_ramma *skrá_færsla_3d0c1245) {
    uintptr_t 첫째값 = skrá_færsla_3d0c1245->skrá_gögn[0], SECOND_VALUE = skrá_færsla_3d0c1245->skrá_gögn[1], stafkóði = skrá_færsla_3d0c1245->skrá_gögn[2];
    char SLÓÐ[65];
    int skrá_hald, NIÐURSTAÐA;
    switch (skrá_færsla_3d0c1245->skrá_gögn[8]) {
    case 0: return 1; // eigin ABI 버전
    case 1: // write: bendill 전체를 검사한 TIL_BAKA_VALUE úttak/Skrá breyta_VALUE_16f64fe4
        if (stafkóði > 65536) return -22;
        if (!사용자범위(SECOND_VALUE, stafkóði, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t Opna_úttak=klukka_VALUE();
            for (size_t 순번 = 0; 순번 < stafkóði; 순번++) bretti_rás(첫째값, ((const unsigned char *)SECOND_VALUE)[순번]);
            /* 큰 tty를 그린 kjarni_VALUE 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(gagnvirkur){
                마감시각+=klukka_VALUE()-Opna_úttak;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(마감시각) : "memory");
            }
            return stafkóði;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t vara_COUNT=stafkóði>512?512:stafkóði;for(size_t 순번=0;순번<vara_COUNT;순번++)자바전문넣기(순번,((const unsigned char *)SECOND_VALUE)[순번]);return 자바흐름쓰기(첫째값,vara_COUNT);
        }
        skrá_hald = 대응파일기술자(첫째값); if (skrá_hald < 0) return -9;
        return kjarni_mæld_stærð(pk_write(skrá_hald, (const void *)SECOND_VALUE, stafkóði));
    case 2:
        if (stafkóði > 65536) return -22;
        if (!사용자범위(SECOND_VALUE, stafkóði, 1)) return -14;
        if (첫째값 == 0) {
            size_t vara_COUNT = 0;
            while (vara_COUNT < stafkóði) {
                int stafur_VALUE = (int32_t)보드글자읽기(); if (stafur_VALUE == -2) return vara_COUNT; if (stafur_VALUE < 0) break;
                ((unsigned char *)SECOND_VALUE)[vara_COUNT++] = stafur_VALUE;
            }
            return vara_COUNT ? (intptr_t)vara_COUNT : (stafkóði ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            NIÐURSTAÐA=자바흐름읽기(첫째값,stafkóði>512?512:stafkóði);if(NIÐURSTAÐA>0)for(int 순번=0;순번<NIÐURSTAÐA;순번++)((unsigned char *)SECOND_VALUE)[순번]=자바전문얻기(순번);return NIÐURSTAÐA;
        }
        skrá_hald = 대응파일기술자(첫째값); if (skrá_hald < 0) return -9;
        return kjarni_mæld_stærð(pk_read(skrá_hald, (void *)SECOND_VALUE, stafkóði));
    case 3:
        NIÐURSTAÐA = afrita_slóð(첫째값, SLÓÐ); if (NIÐURSTAÐA) return NIÐURSTAÐA;
        if (SECOND_VALUE > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (skrá_Listi[순번] < 0) {
            skrá_hald = pk_open(SLÓÐ, (int)SECOND_VALUE, 0600);
            if (skrá_hald < 0) return -villa_númer;
            skrá_Listi[순번] = skrá_hald; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { NIÐURSTAÐA = 통신끝점닫기(첫째값); if (!NIÐURSTAÐA) 통신끝점들[첫째값 - 32] = 0; return NIÐURSTAÐA; }
        skrá_hald = 대응파일기술자(첫째값); if (skrá_hald < 0) return -9;
        NIÐURSTAÐA = pk_close(skrá_hald); if (!NIÐURSTAÐA) skrá_Listi[첫째값 - 3] = -1;
        return kjarni_mæld_stærð(NIÐURSTAÐA);
    case 5:
        skrá_hald = 대응파일기술자(첫째값); if (skrá_hald < 0) return -9;
        if (stafkóði > 2) return -22;
        return kjarni_mæld_stærð(pk_lseek(skrá_hald, (int64_t)SECOND_VALUE, stafkóði));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 notandi RW/NX 힙, 새로 노출되는 페이지는 0으로 frumstilla
        if (!첫째값) return 동적기억끝;
        if (첫째값 < notandi_mynd_ljúka || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + síðustærð - 1) & ~(síðustærð - 1);
        uintptr_t 새쪽들 = (첫째값 + síðustærð - 1) & ~(síðustærð - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t gögn_staða = 이전쪽들; gögn_staða < 새쪽들; gögn_staða += síðustærð) útlit_síðu(gögn_staða, kjarni_síða, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t gögn_staða = 이전쪽들; gögn_staða < 새쪽들; gögn_staða += síðustærð) útlit_síðu(gögn_staða, notandi_les_skrifheimild, 3);
        } else {
            for (uintptr_t gögn_staða = 새쪽들; gögn_staða < 이전쪽들; gögn_staða += síðustærð) {
                síða_Listi[(gögn_staða - notandi_BASE) / síðustærð] = 0; Heimildir_Listi[(gögn_staða - notandi_BASE) / síðustærð] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        skrá_hald = 대응파일기술자(첫째값); return skrá_hald < 0 ? -9 : kjarni_mæld_stærð(pk_size(skrá_hald));
    case 10:
        skrá_hald = 대응파일기술자(첫째값); return skrá_hald < 0 ? -9 : kjarni_mæld_stærð(pk_ftruncate(skrá_hald, (int64_t)SECOND_VALUE));
    case 11:
        NIÐURSTAÐA = afrita_slóð(첫째값, SLÓÐ); return NIÐURSTAÐA ? NIÐURSTAÐA : kjarni_mæld_stærð(pk_unlink(SLÓÐ));
    case 12:
        skrá_hald = 대응파일기술자(첫째값); return skrá_hald < 0 ? -9 : kjarni_mæld_stærð(pk_fsync(skrá_hald));
    case 13: { // 그래픽 기초 API: notandi 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = skrá_færsla_3d0c1245->skrá_gögn[3], 높이값 = skrá_færsla_3d0c1245->skrá_gögn[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SECOND_VALUE > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - SECOND_VALUE) return -22;
        for (uintptr_t Y_hnit = SECOND_VALUE; Y_hnit < SECOND_VALUE + 높이값; Y_hnit++) for (uintptr_t x_hnit = 첫째값; x_hnit < 첫째값 + 너비값; x_hnit++) bretti_díll(x_hnit, Y_hnit, stafkóði);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=vara_COUNT; args(index,buffer,capacity)=UTF-8 lengd_VALUE
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (stafkóði <= 전달인수길이[첫째값]) return -36;
        if (!사용자범위(SECOND_VALUE, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SECOND_VALUE, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;gagnvirkur=1;return bretti_Endastöð(13);}
        if(첫째값==2){gagnvirkur=0;return 0;}
        if(첫째값==3)return bretti_Endastöð(13);
        if(첫째값!=1||!gagnvirkur)return -22;
        NIÐURSTAÐA=(int32_t)보드글자읽기();
        if(NIÐURSTAÐA==-4096)return NIÐURSTAÐA;
        Opna_TIMEOUT();return NIÐURSTAÐA<0?-11:NIÐURSTAÐA;
    case 17: { // 유한한 협력 Bíddu_VALUE: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t ljúka_TIME = klukka_VALUE() + FREQUENCY * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (klukka_VALUE() < ljúka_TIME);
        Opna_TIMEOUT(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 yfireining_VALUE·빈 폴더를 검사한다.
        if (SECOND_VALUE > 2) return -22;
        NIÐURSTAÐA = afrita_slóð(첫째값, SLÓÐ); if (NIÐURSTAÐA) return NIÐURSTAÐA;
        unsigned lengd_VALUE = 0; while (SLÓÐ[lengd_VALUE]) lengd_VALUE++;
        NIÐURSTAÐA = 자바경로시작(lengd_VALUE); if (NIÐURSTAÐA < 0) return NIÐURSTAÐA;
        for (unsigned 순번 = 0; 순번 < lengd_VALUE; 순번++) 자바경로바이트(순번, (unsigned char)SLÓÐ[순번]);
        return SECOND_VALUE == 0 ? 자바항목종류() : SECOND_VALUE == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int stafur_VALUE=(int32_t)보드글자읽기();if(stafur_VALUE==-4096)return stafur_VALUE;if(stafur_VALUE>=0)화면누름(eigandi_hlutur,stafur_VALUE);Opna_TIMEOUT();}
        if(첫째값==3&&stafkóði){if(!자바셸대화형())return -95;gagnvirkur=1;bretti_Endastöð(300);}
        return 화면호출(eigandi_hlutur,첫째값,SECOND_VALUE,stafkóði,skrá_færsla_3d0c1245->skrá_gögn[3],skrá_færsla_3d0c1245->skrá_gögn[4],skrá_færsla_3d0c1245->skrá_gögn[5]);
    case 21:
        if(stafkóði>127)return -22;if(!사용자범위(SECOND_VALUE,stafkóði*sizeof(uint32_t),0))return -14;
        return 화면글(eigandi_hlutur,첫째값,(const uint32_t *)SECOND_VALUE,stafkóði);
    case 22: // 화면 Stærð fyrirspurn_VALUE: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SECOND_VALUE==SOCK_STREAM&&(stafkóði==0||stafkóði==6))NIÐURSTAÐA=자바흐름만들기();
        else if(SECOND_VALUE==SOCK_DGRAM&&(stafkóði==0||stafkóði==IPPROTO_UDP))NIÐURSTAÐA=자바전문만들기(첫째값,SECOND_VALUE,stafkóði);
        else return -93;
        if (NIÐURSTAÐA >= 32 && NIÐURSTAÐA < 56) 통신끝점들[NIÐURSTAÐA - 32] = 1;
        return NIÐURSTAÐA;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in slóð;
        NIÐURSTAÐA = 주소입력(SECOND_VALUE, stafkóði, &slóð); if (NIÐURSTAÐA) return NIÐURSTAÐA;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(slóð.sin_addr.s_addr),pk_htons(slóð.sin_port)):자바전문묶기(첫째값, pk_htonl(slóð.sin_addr.s_addr), pk_htons(slóð.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (skrá_færsla_3d0c1245->skrá_gögn[3]) return -95;
        if (stafkóði > 512) return -90;
        if (stafkóði && !사용자범위(SECOND_VALUE, stafkóði, 0)) return -14;
        struct pk_sockaddr_in slóð;
        NIÐURSTAÐA = 주소입력(skrá_færsla_3d0c1245->skrá_gögn[4], skrá_færsla_3d0c1245->skrá_gögn[5], &slóð); if (NIÐURSTAÐA) return NIÐURSTAÐA;
        for (unsigned 순번 = 0; 순번 < stafkóði; 순번++) 자바전문넣기(순번, ((const unsigned char *)SECOND_VALUE)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(slóð.sin_addr.s_addr), pk_htons(slóð.sin_port), stafkóði);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (skrá_færsla_3d0c1245->skrá_gögn[3]) return -95;
        if (stafkóði > 512) return -90;
        if (stafkóði && !사용자범위(SECOND_VALUE, stafkóði, 1)) return -14;
        pk_socklen_t biðminni_afkastageta = 0;
        if (skrá_færsla_3d0c1245->skrá_gögn[4]) { NIÐURSTAÐA = slóð_úttak_athuga(skrá_færsla_3d0c1245->skrá_gögn[4], skrá_færsla_3d0c1245->skrá_gögn[5], &biðminni_afkastageta); if (NIÐURSTAÐA) return NIÐURSTAÐA; }
        NIÐURSTAÐA = 자바전문받기(첫째값, stafkóði); if (NIÐURSTAÐA < 0) return NIÐURSTAÐA;
        for (int 순번 = 0; 순번 < NIÐURSTAÐA; 순번++) ((unsigned char *)SECOND_VALUE)[순번] = 자바전문얻기(순번);
        if (skrá_færsla_3d0c1245->skrá_gögn[4]) slóð_úttak(skrá_færsla_3d0c1245->skrá_gögn[4], skrá_færsla_3d0c1245->skrá_gögn[5], biðminni_afkastageta, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return NIÐURSTAÐA;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t biðminni_afkastageta;
        NIÐURSTAÐA = slóð_úttak_athuga(SECOND_VALUE, stafkóði, &biðminni_afkastageta); if (NIÐURSTAÐA) return NIÐURSTAÐA;
        slóð_úttak(SECOND_VALUE,stafkóði,biðminni_afkastageta,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in slóð;
        NIÐURSTAÐA=주소입력(SECOND_VALUE,stafkóði,&slóð);if(NIÐURSTAÐA)return NIÐURSTAÐA;
        return 자바흐름연결(첫째값,pk_htonl(slóð.sin_addr.s_addr),pk_htons(slóð.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,SECOND_VALUE):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(SECOND_VALUE||stafkóði)return -95;NIÐURSTAÐA=자바흐름연결받기(첫째값);if(NIÐURSTAÐA>=40&&NIÐURSTAÐA<56)통신끝점들[NIÐURSTAÐA-32]=1;return NIÐURSTAÐA;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(notandi_ramma *skrá_færsla_3d0c1245) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(skrá_færsla_3d0c1245) : 자체체계호출(skrá_færsla_3d0c1245);
}
static void skila_kjarni(notandi_ramma *skrá_færsla_3d0c1245, int NIÐURSTAÐA) {
    Stopp_TIMEOUT();
    skrá_færsla_3d0c1245->skrá_gögn[0] = (uint64_t)(int64_t)NIÐURSTAÐA;
    skrá_færsla_3d0c1245->skipun_staða = (uintptr_t)notandi_skila;
    skrá_færsla_3d0c1245->staða_CODE = 0x3c5; // EL1h, DAIF masked
}
int notandi_undantekning(notandi_ramma *skrá_færsla_3d0c1245, unsigned INTERCEPT) {
    if (!Laus || (skrá_færsla_3d0c1245->staða_CODE & 15) != 0) return 0;
    if (INTERCEPT) {
        uint32_t 승인값 = vél_skrá(IRQ_örgjörvi_viðmót + 0xc), auðkenni_VALUE = 승인값 & 1023;
        if (auðkenni_VALUE == 30) { skila_kjarni(skrá_færsla_3d0c1245, notandi_TIMEOUT); vél_skrá(IRQ_örgjörvi_viðmót + 0x10) = 승인값; return 1; }
        if (auðkenni_VALUE < 1020) vél_skrá(IRQ_örgjörvi_viðmót + 0x10) = 승인값;
        return 1;
    }
    uint64_t undantekning_staða; __asm__ volatile("mrs %0, esr_el1" : "=r"(undantekning_staða));
    if (klukka_VALUE() >= 마감시각) { skila_kjarni(skrá_færsla_3d0c1245, notandi_TIMEOUT); return 1; }
    unsigned undantekning_tegund = undantekning_staða >> 26;
    if (undantekning_tegund == 0x15 && (undantekning_staða & 0xffff) == 0) {
        if (리눅스규약 ? skrá_færsla_3d0c1245->skrá_gögn[8] == 93 || skrá_færsla_3d0c1245->skrá_gögn[8] == 94 : skrá_færsla_3d0c1245->skrá_gögn[8] == 6) skila_kjarni(skrá_færsla_3d0c1245, (int)(skrá_færsla_3d0c1245->skrá_gögn[0] & 255));
        else {
            intptr_t NIÐURSTAÐA=체계호출(skrá_færsla_3d0c1245);
            if(NIÐURSTAÐA==-4096&&gagnvirkur){
                저장값[eigandi_hlutur].실행틀=*skrá_færsla_3d0c1245;저장값[eigandi_hlutur].실행틀.skipun_staða-=4;
                사용자실수보관(저장값[eigandi_hlutur].실수저장상태);skila_kjarni(skrá_færsla_3d0c1245,사용자중단됨);
            }else skrá_færsla_3d0c1245->skrá_gögn[0]=(uint64_t)NIÐURSTAÐA;
        }
    } else skila_kjarni(skrá_færsla_3d0c1245, undantekning_tegund == 0x24 ? notandi_gögn_villa : undantekning_tegund == 0x20 ? 사용자실행오류 : notandi_ógilt_skipun);
    return 1;
}

// 생성된 const ELF Hópur_VALUE: 실행은 반드시 forrit_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *gögn; size_t Stærð; unsigned 전달값; } forrit;
#include "programs.h"
static void *skyndimynd(unsigned staða_INDEX){return (void *)(0x04000000ul+staða_INDEX*(notandi_ljúka-notandi_BASE));}
static int Ljúka_forrit(int NIÐURSTAÐA){
    사용자누적시각[eigandi_hlutur]+=(uint32_t)보드밀리초()-사용자실행시각[eigandi_hlutur];
    Stopp_TIMEOUT();Laus=0;
    if(NIÐURSTAÐA==사용자중단됨){
        저장된작업 *strengur_gögn=&저장값[eigandi_hlutur];strengur_gögn->멈춤상태=1;strengur_gögn->gagnvirkur=gagnvirkur;strengur_gögn->리눅스규약=리눅스규약;strengur_gögn->동적기억공간=동적기억끝;strengur_gögn->인수개수=전달인수개수;
        memcpy(strengur_gögn->Heimildir_Listi,Heimildir_Listi,sizeof(Heimildir_Listi));memcpy(strengur_gögn->skrá_Listi,skrá_Listi,sizeof(skrá_Listi));memcpy(strengur_gögn->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(strengur_gögn->frumbreyta_ARRAY,전달인수,sizeof(전달인수));memcpy(strengur_gögn->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<notandi_síða_COUNT;순번++)if(Heimildir_Listi[순번])memcpy((unsigned char *)skyndimynd(eigandi_hlutur)+순번*síðustærð,(void *)(notandi_BASE+순번*síðustærð),síðustærð);
    }else{
        저장값[eigandi_hlutur].멈춤상태=0;화면초기화(eigandi_hlutur);
        for(unsigned 순번=0;순번<16;순번++)if(skrá_Listi[순번]>=0)pk_close(skrá_Listi[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<notandi_síða_COUNT;순번++){síða_Listi[순번]=0;Heimildir_Listi[순번]=0;}변환표맞추기();return NIÐURSTAÐA;
}
uintptr_t bretti_notandastjórn(uintptr_t Aðgerð){
    unsigned staða_INDEX=Aðgerð&15;if(staða_INDEX>=4||Laus)return (uint32_t)-22;
    저장된작업 *strengur_gögn=&저장값[staða_INDEX];
    if(Aðgerð>=32){if(strengur_gögn->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(strengur_gögn->skrá_Listi[순번]>=0)pk_close(strengur_gögn->skrá_Listi[순번]);for(unsigned 순번=0;순번<24;순번++)if(strengur_gögn->통신끝점들[순번])통신끝점닫기(순번+32);}strengur_gögn->멈춤상태=0;화면초기화(staða_INDEX);return 0;}
    if(Aðgerð>=16)return strengur_gögn->멈춤상태;
    if(!strengur_gögn->멈춤상태)return (uint32_t)-22;
    eigandi_hlutur=staða_INDEX;gagnvirkur=strengur_gögn->gagnvirkur;리눅스규약=strengur_gögn->리눅스규약;동적기억끝=strengur_gögn->동적기억공간;전달인수개수=strengur_gögn->인수개수;
    memcpy(skrá_Listi,strengur_gögn->skrá_Listi,sizeof(skrá_Listi));memcpy(통신끝점들,strengur_gögn->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,strengur_gögn->frumbreyta_ARRAY,sizeof(전달인수));memcpy(전달인수길이,strengur_gögn->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<notandi_síða_COUNT;순번++)síða_Listi[순번]=(notandi_BASE+순번*síðustærð)|kjarni_síða;변환표맞추기();
    memset((void *)notandi_BASE,0,notandi_ljúka-notandi_BASE);
    for(unsigned 순번=0;순번<notandi_síða_COUNT;순번++)if(strengur_gögn->Heimildir_Listi[순번])memcpy((void *)(notandi_BASE+순번*síðustærð),(unsigned char *)skyndimynd(staða_INDEX)+순번*síðustærð,síðustærð);
    memcpy(Heimildir_Listi,strengur_gögn->Heimildir_Listi,sizeof(Heimildir_Listi));
    for(unsigned 순번=0;순번<notandi_síða_COUNT;순번++){unsigned gögn_staða=Heimildir_Listi[순번];síða_Listi[순번]=gögn_staða?(notandi_BASE+순번*síðustærð)|(gögn_staða==3?notandi_les_skrifheimild:gögn_staða==5?사용자읽고실행:notandi_skrifvarið):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");Laus=1;strengur_gögn->멈춤상태=0;Opna_TIMEOUT();
    사용자실행시각[eigandi_hlutur]=보드밀리초();
    return (uint32_t)Ljúka_forrit(notandi_ferilskrá(&strengur_gögn->실행틀,strengur_gögn->실수저장상태));
}
static int runa_forrit(const unsigned char *gögn, size_t Stærð, unsigned 전달값, int 리눅스방식, const char *Heiti) {
    if (Laus) return -16;
    eigandi_hlutur=bretti_Endastöð(11);if(eigandi_hlutur<0||eigandi_hlutur>3||저장값[eigandi_hlutur].멈춤상태)return -16;gagnvirkur=0;
    int 유효함 = 실행파일검사(gögn, Stærð, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned heiti_INDEX=0;
    while (*Heiti && heiti_INDEX<31) notandi_skipun_heiti[eigandi_hlutur][heiti_INDEX++]=(unsigned char)*Heiti++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (heiti_INDEX) notandi_skipun_heiti[eigandi_hlutur][heiti_INDEX++]=' ';
        for (unsigned staða_INDEX=0; staða_INDEX<전달인수길이[0]; staða_INDEX++) notandi_skipun_heiti[eigandi_hlutur][heiti_INDEX++]=전달인수[0][staða_INDEX];
    }
    notandi_skipun_heiti[eigandi_hlutur][heiti_INDEX]=0; notandanúmer[eigandi_hlutur]=Áfram_notandanúmer++;
    if (Áfram_notandanúmer>0x7fffffffu) Áfram_notandanúmer=10;
    notandi_Opna_TIME[eigandi_hlutur]=보드밀리초(); 사용자누적시각[eigandi_hlutur]=0;
    for (unsigned 순번 = 0; 순번 < notandi_síða_COUNT; 순번++) síða_Listi[순번] = (notandi_BASE + 순번 * síðustærð) | kjarni_síða;
    변환표맞추기();
    memset((void *)notandi_BASE, 0, notandi_ljúka - notandi_BASE);
    memset(Heimildir_Listi, 0, sizeof(Heimildir_Listi));
    실행파일머리 실행머리; memcpy(&실행머리, gögn, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.forrit_Haus_COUNT; 순번++) {
        실행파일구획 gögn_staða; memcpy(&gögn_staða, gögn + 실행머리.forrit_Haus_OFFSET + 순번 * sizeof(gögn_staða), sizeof(gögn_staða));
        if (gögn_staða.TYPE_tegund != 1 || !gögn_staða.기억영역크기) continue;
        if (gögn_staða.파일영역크기) memcpy((void *)(uintptr_t)gögn_staða.slóð, gögn + gögn_staða.OFFSET_VALUE, gögn_staða.파일영역크기);
        for (uintptr_t 현재위치 = gögn_staða.slóð & ~(síðustærð - 1); 현재위치 < gögn_staða.slóð + gögn_staða.기억영역크기; 현재위치 += síðustærð) {
            Heimildir_Listi[(현재위치 - notandi_BASE) / síðustærð] = (gögn_staða.afbrigði_Background_Intelligent_Transfer_Service & 2) ? 3 : ((gögn_staða.afbrigði_Background_Intelligent_Transfer_Service & 1) ? 5 : 1);
        }
    }
    for (uintptr_t 현재위치 = notandi_bunki_slóð; 현재위치 < notandi_ljúka; 현재위치 += síðustærð) Heimildir_Listi[(현재위치 - notandi_BASE) / síðustærð] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.færsla_P) : notandi_ljúka;
    for (unsigned 순번 = 0; 순번 < notandi_síða_COUNT; 순번++) {
        unsigned heimildir = Heimildir_Listi[순번];
        síða_Listi[순번] = heimildir ? (notandi_BASE + 순번 * síðustærð) | (heimildir == 3 ? notandi_les_skrifheimild : heimildir == 5 ? 사용자읽고실행 : notandi_skrifvarið) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) skrá_Listi[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = notandi_mynd_ljúka;
    Laus = 1; Opna_TIMEOUT();
    사용자실행시각[eigandi_hlutur]=보드밀리초();
    int NIÐURSTAÐA = notandi_slá_inn(실행머리.færsla_P, 초기쌓임공간, 전달값);
    return Ljúka_forrit(NIÐURSTAÐA);
}
uintptr_t bretti_notandi_runa(uintptr_t LOOKUP_INDEX) {
    if (LOOKUP_INDEX >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Heiti=LOOKUP_INDEX==10?"javac":LOOKUP_INDEX==11?"java":LOOKUP_INDEX==12?"python":LOOKUP_INDEX==13?"vi":LOOKUP_INDEX==14?"jar":LOOKUP_INDEX==15?"cc":LOOKUP_INDEX==16?"jaot":"ELF";
    return (uint32_t)runa_forrit(실행항목들[LOOKUP_INDEX].gögn, 실행항목들[LOOKUP_INDEX].Stærð, 실행항목들[LOOKUP_INDEX].전달값, 0, Heiti);
}
static uintptr_t keyra_skrá(int 리눅스방식) {
    static unsigned char mynd[16384];
    if (Laus || !전달인수개수) return (uint32_t)-22;
    int skrá_hald = pk_open((const char *)전달인수[0], skrifvarið_VALUE, 0);
    if (skrá_hald < 0) return (uint32_t)-villa_númer;
    int Stærð = pk_size(skrá_hald);
    if (Stærð < 0 || (unsigned)Stærð > sizeof(mynd)) { pk_close(skrá_hald); return (uint32_t)-27; }
    int RECEIVED_COUNT = pk_read(skrá_hald, mynd, Stærð); pk_close(skrá_hald);
    if (RECEIVED_COUNT != Stærð) return (uint32_t)-5;
    return (uint32_t)runa_forrit(mynd, Stærð, 0, 리눅스방식, "");
}
uintptr_t bretti_notandi_skrá(void) { return keyra_skrá(0); }
uintptr_t 보드사용자리눅스파일(void) { return keyra_skrá(1); }
uintptr_t bretti_notandi_staðfesta(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].gögn, 잘못된실행항목들[순번].Stærð) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
