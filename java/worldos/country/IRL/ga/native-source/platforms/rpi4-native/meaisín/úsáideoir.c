#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 Rith_ordú meaisín sraith_VALUE. Comhad sonraí/정책은 기존 AOT Java 커널에 위임한다.
#include "úsáideoir.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../Líonra_Cruach/Líonra_Cruach.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define meaisín_cláraigh(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_dáileoir 0xff841000ul
#define IRQ_CPU_comhéadan 0xff842000ul
#define méid_leathanaigh 4096ul
#define 접근표시 (1ul << 10)
#define 권한실행금지 (1ul << 53)
#define 사용자실행금지 (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | 접근표시)
#define eithne_leathanach (3ul | 보통기억 | 권한실행금지 | 사용자실행금지)
#define úsáideoir_inléite_inscríofa (3ul | 보통기억 | (1ul << 6) | 권한실행금지 | 사용자실행금지)
#define úsáideoir_inléite_amháin (3ul | 보통기억 | (3ul << 6) | 권한실행금지 | 사용자실행금지)
#define 사용자읽고실행 (3ul | 보통기억 | (3ul << 6) | 권한실행금지)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t clár_picteilín(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t clár_Teirminéal(uintptr_t);
extern int Teirminéal_Ar_feitheamh(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int úsáideoir_CV(úsáideoir_fráma *,void *);
extern void 사용자실수보관(void *);
extern int úsáideoir_iontráil(uintptr_t iontráil_pointe, uintptr_t Cruach_Stóras, uintptr_t 전달값);
extern void úsáideoir_return(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t fréamh_ADDRESS[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t leathanach_Liosta[úsáideoir_leathanach_COUNT] __attribute__((aligned(4096)));
static uint8_t ceadanna_rochtana_Liosta[úsáideoir_leathanach_COUNT];
static int gníomhach, comhad_Liosta[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned comhad_hanla){return comhad_hanla<40?자바전문닫기(comhad_hanla):자바흐름닫기(comhad_hanla);}
static uint64_t FREQUENCY, 마감시각;
static uintptr_t 동적기억끝;
// eithne_VALUE 셸이 준비한 UTF-8 Argóintí. EL0에는 ásc_VALUE 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,idirghníomhach,리눅스규약,comhad_Liosta[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char argóint_ARRAY[8][256],ceadanna_rochtana_Liosta[úsáideoir_leathanach_COUNT];
    uintptr_t 동적기억공간; úsáideoir_fráma 실행틀;
    unsigned char 실수저장상태[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int úinéir_oibiacht,idirghníomhach;
static uint32_t uimhir_úsáideora[4], úsáideoir_Start_TIME[4], 사용자누적시각[4], 사용자실행시각[4], Ar_aghaidh_uimhir_úsáideora=10;
static unsigned char úsáideoir_ordú_ainm[4][288];
uint32_t 사용자상태읽기(unsigned iontráil_VALUE, unsigned INDEX) {
    unsigned suíomh_INDEX=INDEX&3;
    int staid_VALUE=(gníomhach && úinéir_oibiacht==(int)suíomh_INDEX) ? 1 : 저장값[suíomh_INDEX].멈춤상태 ? 2 : 0;
    if (iontráil_VALUE==0) return staid_VALUE;
    if (!staid_VALUE) return 0;
    if (iontráil_VALUE==1) return uimhir_úsáideora[suíomh_INDEX];
    if (iontráil_VALUE==2) {
        unsigned char *쪽들=staid_VALUE==1?ceadanna_rochtana_Liosta:저장값[suíomh_INDEX].ceadanna_rochtana_Liosta;
        unsigned leathanach_COUNT=0; for (unsigned 순번=0; 순번<úsáideoir_leathanach_COUNT; 순번++) if(쪽들[순번]) leathanach_COUNT++;
        return leathanach_COUNT*4;
    }
    if (iontráil_VALUE==3) return (uint32_t)보드밀리초()-úsáideoir_Start_TIME[suíomh_INDEX];
    if (iontráil_VALUE==4) return 사용자누적시각[suíomh_INDEX]+(staid_VALUE==1?(uint32_t)보드밀리초()-사용자실행시각[suíomh_INDEX]:0);
    if (iontráil_VALUE==5) return INDEX/4<sizeof(úsáideoir_ordú_ainm[0])?úsáideoir_ordú_ainm[suíomh_INDEX][INDEX/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t iontráil_COUNT) {
    if (gníomhach || iontráil_COUNT > 8) return (uint32_t)-22;
    전달인수개수 = iontráil_COUNT;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t LOOKUP_INDEX, uintptr_t 현재위치, uintptr_t beart_sonraí) {
    if (gníomhach || LOOKUP_INDEX >= 전달인수개수 || 현재위치 >= 255 || 현재위치 != 전달인수길이[LOOKUP_INDEX] || !beart_sonraí || beart_sonraí > 255)
        return (uint32_t)-22;
    전달인수[LOOKUP_INDEX][현재위치] = beart_sonraí;
    전달인수길이[LOOKUP_INDEX] = 현재위치 + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Clog_VALUE(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void stop_TIMEOUT(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    meaisín_cláraigh(IRQ_dáileoir + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void Start_TIMEOUT(void) {
    uint64_t 간격 = FREQUENCY * 2, cas_air = 1;
    마감시각 = Clog_VALUE() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(cas_air) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned sonraí_bac = 0; sonraí_bac < 4; sonraí_bac++) {
        fréamh_ADDRESS[sonraí_bac] = (uintptr_t)가운데[sonraí_bac] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t ADDRESS = ((uintptr_t)sonraí_bac << 30) | ((uintptr_t)순번 << 21);
            가운데[sonraí_bac][순번] = ADDRESS | 1 | 접근표시 | 사용자실행금지;
            if (ADDRESS >= 0xfc000000ul) 가운데[sonraí_bac][순번] |= 권한실행금지; // Device-nGnRnE
            else 가운데[sonraí_bac][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned SECOND_VALUE = 0; SECOND_VALUE < úsáideoir_leathanach_COUNT / 512; SECOND_VALUE++)
        가운데[0][(úsáideoir_BASE >> 21) + SECOND_VALUE] = (uintptr_t)(leathanach_Liosta + SECOND_VALUE * 512) | 3;
    for (unsigned 순번 = 0; 순번 < úsáideoir_leathanach_COUNT; 순번++) leathanach_Liosta[순번] = (úsáideoir_BASE + 순번 * méid_leathanaigh) | eithne_leathanach;
    uint64_t Cuimhne_tréith_cláraigh = 0x4400, ADDRESS_Aistriúchán_rialú = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Cuimhne_tréith_cláraigh), "r"(ADDRESS_Aistriúchán_rialú), "r"((uintptr_t)fréamh_ADDRESS) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t 실수저장상태 = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(실수저장상태) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    stop_TIMEOUT();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 iontráil_pointe_VALUE 때만 Ceadaigh_VALUE.
    meaisín_cláraigh(IRQ_dáileoir) = 0;
    meaisín_cláraigh(IRQ_dáileoir + 0x180) = 0xffffffff;
    meaisín_cláraigh(IRQ_dáileoir + 0x80) = 0xffffffff;
    meaisín_cláraigh(IRQ_dáileoir + 0x280) = 1u << 30;
    meaisín_cláraigh(IRQ_dáileoir + 0x41c) = 0x80808080;
    meaisín_cláraigh(IRQ_dáileoir + 0x100) = 1u << 30;
    meaisín_cláraigh(IRQ_CPU_comhéadan + 4) = 0xff;
    meaisín_cláraigh(IRQ_CPU_comhéadan + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 수 있다.
    int Slándáil = (meaisín_cláraigh(IRQ_dáileoir + 4) & (1u << 10)) != 0;
    meaisín_cláraigh(IRQ_dáileoir) = Slándáil ? 1 : 3;
    meaisín_cláraigh(IRQ_CPU_comhéadan) = Slándáil ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t TYPE_catagóir, meaisín_TYPE; uint32_t uimhir_an_leagain;
    uint64_t iontráil_pointe, clár_Ceanntásc_OFFSET, rannán_Ceanntásc_OFFSET; uint32_t 설정비트;
    uint16_t 실행머리크기, clár_Ceanntásc_iontráil_socraigh_méid, clár_Ceanntásc_COUNT, rannán_Ceanntásc_iontráil_socraigh_méid, rannán_Ceanntásc_COUNT, rannán_ainm_tábla_INDEX;
} 실행파일머리;
typedef struct { uint32_t TYPE_catagóir, 설정비트; uint64_t OFFSET_VALUE, ADDRESS, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(úsáideoir_fráma) == 272, "exception assembly layout");
static int 포함된범위(uint64_t OFFSET_VALUE, uint64_t Méid, uint64_t cuir_deireadh_le_OFFSET) {
    return OFFSET_VALUE <= cuir_deireadh_le_OFFSET && Méid <= cuir_deireadh_le_OFFSET - OFFSET_VALUE;
}
static int 부가정보검사(const unsigned char *sonraí_suíomh, size_t Méid) {
    size_t 현재위치 = 0;
    while (포함된범위(현재위치, 12, Méid)) {
        uint32_t 낱말들[3]; memcpy(낱말들, sonraí_suíomh + 현재위치, 12); 현재위치 += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(현재위치, 이름영역크기, Méid) || !포함된범위(현재위치 + 이름영역크기, 설명크기, Méid)) return 0;
        const unsigned char Ainm[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Ainm) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Ainm); 순번++) if (sonraí_suíomh[현재위치 + 순번] != Ainm[순번]) 일치 = 0;
        uint32_t uimhir_an_leagain = 0;
        if (일치) memcpy(&uimhir_an_leagain, sonraí_suíomh + 현재위치 + 이름영역크기, 4);
        if (일치 && uimhir_an_leagain == 1) return 1;
        현재위치 += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *sonraí, size_t Méid, int 리눅스방식) {
    if (Méid < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, sonraí, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.TYPE_catagóir != 2 || 실행머리.meaisín_TYPE != 183 || 실행머리.uimhir_an_leagain != 1 || 실행머리.설정비트 || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.clár_Ceanntásc_iontráil_socraigh_méid != sizeof(실행파일구획) || !실행머리.clár_Ceanntásc_COUNT || 실행머리.clár_Ceanntásc_COUNT > 16 ||
        실행머리.clár_Ceanntásc_OFFSET < sizeof(실행머리) || !포함된범위(실행머리.clár_Ceanntásc_OFFSET, (uint64_t)실행머리.clár_Ceanntásc_COUNT * sizeof(실행파일구획), Méid)) return 사용자실행파일오류;
    uint8_t 사용량[(úsáideoir_IMAGE_cuir_deireadh_le - úsáideoir_BASE) / méid_leathanaigh] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.clár_Ceanntásc_COUNT; 순번++) {
        실행파일구획 sonraí_suíomh; memcpy(&sonraí_suíomh, sonraí + 실행머리.clár_Ceanntásc_OFFSET + 순번 * sizeof(sonraí_suíomh), sizeof(sonraí_suíomh));
        if (sonraí_suíomh.TYPE_catagóir == 4) {
            if (!포함된범위(sonraí_suíomh.OFFSET_VALUE, sonraí_suíomh.파일영역크기, Méid)) return 사용자실행파일오류;
            if (부가정보검사(sonraí + sonraí_suíomh.OFFSET_VALUE, sonraí_suíomh.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (sonraí_suíomh.TYPE_catagóir == 0 || sonraí_suíomh.TYPE_catagóir == 6 || (sonraí_suíomh.TYPE_catagóir == 0x6474e551 && !(sonraí_suíomh.설정비트 & 1))) continue;
        if (sonraí_suíomh.TYPE_catagóir != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!sonraí_suíomh.기억영역크기) continue;
        if (sonraí_suíomh.설정비트 & ~7u || !(sonraí_suíomh.설정비트 & 4) || (sonraí_suíomh.설정비트 & 3) == 3 || sonraí_suíomh.파일영역크기 > sonraí_suíomh.기억영역크기 ||
            (sonraí_suíomh.파일영역크기 && !포함된범위(sonraí_suíomh.OFFSET_VALUE, sonraí_suíomh.파일영역크기, Méid)) || sonraí_suíomh.ADDRESS < úsáideoir_BASE ||
            !포함된범위(sonraí_suíomh.ADDRESS, sonraí_suíomh.기억영역크기, úsáideoir_IMAGE_cuir_deireadh_le) ||
            (!리눅스방식 && ((sonraí_suíomh.ADDRESS & (méid_leathanaigh - 1)) || (sonraí_suíomh.OFFSET_VALUE & (méid_leathanaigh - 1)) || sonraí_suíomh.맞춤 != méid_leathanaigh)) ||
            (리눅스방식 && (((sonraí_suíomh.ADDRESS ^ sonraí_suíomh.OFFSET_VALUE) & (méid_leathanaigh - 1)) || !sonraí_suíomh.맞춤 ||
                (sonraí_suíomh.맞춤 & (sonraí_suíomh.맞춤 - 1)) || sonraí_suíomh.맞춤 > 0x200000 || ((sonraí_suíomh.ADDRESS ^ sonraí_suíomh.OFFSET_VALUE) & (sonraí_suíomh.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (sonraí_suíomh.ADDRESS - úsáideoir_BASE) / méid_leathanaigh;
        unsigned iontráil_COUNT = ((sonraí_suíomh.ADDRESS & (méid_leathanaigh - 1)) + sonraí_suíomh.기억영역크기 + méid_leathanaigh - 1) / méid_leathanaigh;
        for (unsigned leathanach_VALUE = 첫항목; leathanach_VALUE < 첫항목 + iontráil_COUNT; leathanach_VALUE++) {
            if (사용량[leathanach_VALUE]) return 사용자실행파일오류;
            사용량[leathanach_VALUE] = 1;
        }
        if ((sonraí_suíomh.설정비트 & 1) && 실행머리.iontráil_pointe >= sonraí_suíomh.ADDRESS && 실행머리.iontráil_pointe < sonraí_suíomh.ADDRESS + sonraí_suíomh.파일영역크기 && !(실행머리.iontráil_pointe & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *sonraí, size_t Méid) { return 실행파일검사(sonraí, Méid, 0); }
static void leagan_amach_an_leathanaigh(uintptr_t ADDRESS, uint64_t 설정비트, unsigned ceadanna_rochtana) {
    unsigned LOOKUP_INDEX = (ADDRESS - úsáideoir_BASE) / méid_leathanaigh;
    leathanach_Liosta[LOOKUP_INDEX] = ADDRESS | 설정비트;
    ceadanna_rochtana_Liosta[LOOKUP_INDEX] = ceadanna_rochtana;
}
static int 사용자범위(uintptr_t ADDRESS, size_t iontráil_COUNT, int 쓰는중) {
    if (ADDRESS < úsáideoir_BASE || !포함된범위(ADDRESS, iontráil_COUNT, úsáideoir_cuir_deireadh_le)) return 0;
    if (!iontráil_COUNT) return 1;
    unsigned 첫항목 = (ADDRESS - úsáideoir_BASE) / méid_leathanaigh, 마지막 = (ADDRESS + iontráil_COUNT - 1 - úsáideoir_BASE) / méid_leathanaigh;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(ceadanna_rochtana_Liosta[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int ásc_cosán(uintptr_t ADDRESS, char *CONAIR) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!사용자범위(ADDRESS, 1, 0)) return -14;
        CONAIR[순번] = *(const char *)ADDRESS++;
        if (!CONAIR[순번]) return 0;
    }
    return -36;
}
static intptr_t eithne_tomhas(intptr_t tomhas) { return tomhas < 0 ? -오류번호 : tomhas; }
static int 대응파일기술자(uint64_t comhad_hanla) { return comhad_hanla >= 3 && comhad_hanla < 19 ? comhad_Liosta[comhad_hanla - 3] : -1; }
static int 통신끝점소유(uint64_t comhad_hanla) { return comhad_hanla >= 32 && comhad_hanla < 56 && 통신끝점들[comhad_hanla - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t fad_VALUE, struct pk_sockaddr_in *ADDRESS) {
    if (fad_VALUE != sizeof(*ADDRESS)) return -22;
    if (!사용자범위(가리킴값, fad_VALUE, 0)) return -14;
    memcpy(ADDRESS, (const void *)가리킴값, sizeof(*ADDRESS));
    return ADDRESS->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t fad_pointeoir, pk_socklen_t *수용량) {
    if (!사용자범위(fad_pointeoir, sizeof(*수용량), 1)) return -14;
    memcpy(수용량, (const void *)fad_pointeoir, sizeof(*수용량));
    if (*수용량 > sizeof(struct pk_sockaddr_in)) *수용량 = sizeof(struct pk_sockaddr_in);
    if (*수용량 && !사용자범위(가리킴값, *수용량, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t fad_pointeoir, pk_socklen_t 수용량, int ADDRESS, int uimhir_phoirt) {
    struct pk_sockaddr_in VALUE; memset(&VALUE, 0, sizeof(VALUE));
    VALUE.sin_family = AF_INET; VALUE.sin_port = pk_htons(uimhir_phoirt); VALUE.sin_addr.s_addr = pk_htonl(ADDRESS);
    if (수용량) memcpy((void *)가리킴값, &VALUE, 수용량);
    pk_socklen_t fad_VALUE = sizeof(VALUE); memcpy((void *)fad_pointeoir, &fad_VALUE, sizeof(fad_VALUE));
}
extern uintptr_t clár_cainéal(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(úsáideoir_fráma *comhad_iontráil) {
    uintptr_t 첫째값 = comhad_iontráil->cláraigh_sonraí[0], SECOND_VALUE = comhad_iontráil->cláraigh_sonraí[1], pointe_cóid = comhad_iontráil->cláraigh_sonraí[2];
    char CONAIR[65];
    int comhad_hanla, tomhas;
    switch (comhad_iontráil->cláraigh_sonraí[8]) {
    case 0: return 1; // 자체 ABI 버전
    case 1: // write: pointeoir 전체를 검사한 Siar_VALUE Aschur/Comhad athraigh_VALUE
        if (pointe_cóid > 65536) return -22;
        if (!사용자범위(SECOND_VALUE, pointe_cóid, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=Clog_VALUE();
            for (size_t 순번 = 0; 순번 < pointe_cóid; 순번++) clár_cainéal(첫째값, ((const unsigned char *)SECOND_VALUE)[순번]);
            /* 큰 tty를 그린 eithne_VALUE 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(idirghníomhach){
                마감시각+=Clog_VALUE()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(마감시각) : "memory");
            }
            return pointe_cóid;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t mír_COUNT=pointe_cóid>512?512:pointe_cóid;for(size_t 순번=0;순번<mír_COUNT;순번++)자바전문넣기(순번,((const unsigned char *)SECOND_VALUE)[순번]);return 자바흐름쓰기(첫째값,mír_COUNT);
        }
        comhad_hanla = 대응파일기술자(첫째값); if (comhad_hanla < 0) return -9;
        return eithne_tomhas(pk_write(comhad_hanla, (const void *)SECOND_VALUE, pointe_cóid));
    case 2:
        if (pointe_cóid > 65536) return -22;
        if (!사용자범위(SECOND_VALUE, pointe_cóid, 1)) return -14;
        if (첫째값 == 0) {
            size_t mír_COUNT = 0;
            while (mír_COUNT < pointe_cóid) {
                int carachtar_VALUE = (int32_t)보드글자읽기(); if (carachtar_VALUE == -2) return mír_COUNT; if (carachtar_VALUE < 0) break;
                ((unsigned char *)SECOND_VALUE)[mír_COUNT++] = carachtar_VALUE;
            }
            return mír_COUNT ? (intptr_t)mír_COUNT : (pointe_cóid ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            tomhas=자바흐름읽기(첫째값,pointe_cóid>512?512:pointe_cóid);if(tomhas>0)for(int 순번=0;순번<tomhas;순번++)((unsigned char *)SECOND_VALUE)[순번]=자바전문얻기(순번);return tomhas;
        }
        comhad_hanla = 대응파일기술자(첫째값); if (comhad_hanla < 0) return -9;
        return eithne_tomhas(pk_read(comhad_hanla, (void *)SECOND_VALUE, pointe_cóid));
    case 3:
        tomhas = ásc_cosán(첫째값, CONAIR); if (tomhas) return tomhas;
        if (SECOND_VALUE > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (comhad_Liosta[순번] < 0) {
            comhad_hanla = pk_open(CONAIR, (int)SECOND_VALUE, 0600);
            if (comhad_hanla < 0) return -오류번호;
            comhad_Liosta[순번] = comhad_hanla; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { tomhas = 통신끝점닫기(첫째값); if (!tomhas) 통신끝점들[첫째값 - 32] = 0; return tomhas; }
        comhad_hanla = 대응파일기술자(첫째값); if (comhad_hanla < 0) return -9;
        tomhas = pk_close(comhad_hanla); if (!tomhas) comhad_Liosta[첫째값 - 3] = -1;
        return eithne_tomhas(tomhas);
    case 5:
        comhad_hanla = 대응파일기술자(첫째값); if (comhad_hanla < 0) return -9;
        if (pointe_cóid > 2) return -22;
        return eithne_tomhas(pk_lseek(comhad_hanla, (int64_t)SECOND_VALUE, pointe_cóid));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 úsáideoir RW/NX 힙, 새로 노출되는 페이지는 0으로 túsaigh
        if (!첫째값) return 동적기억끝;
        if (첫째값 < úsáideoir_IMAGE_cuir_deireadh_le || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + méid_leathanaigh - 1) & ~(méid_leathanaigh - 1);
        uintptr_t 새쪽들 = (첫째값 + méid_leathanaigh - 1) & ~(méid_leathanaigh - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t sonraí_suíomh = 이전쪽들; sonraí_suíomh < 새쪽들; sonraí_suíomh += méid_leathanaigh) leagan_amach_an_leathanaigh(sonraí_suíomh, eithne_leathanach, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t sonraí_suíomh = 이전쪽들; sonraí_suíomh < 새쪽들; sonraí_suíomh += méid_leathanaigh) leagan_amach_an_leathanaigh(sonraí_suíomh, úsáideoir_inléite_inscríofa, 3);
        } else {
            for (uintptr_t sonraí_suíomh = 새쪽들; sonraí_suíomh < 이전쪽들; sonraí_suíomh += méid_leathanaigh) {
                leathanach_Liosta[(sonraí_suíomh - úsáideoir_BASE) / méid_leathanaigh] = 0; ceadanna_rochtana_Liosta[(sonraí_suíomh - úsáideoir_BASE) / méid_leathanaigh] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        comhad_hanla = 대응파일기술자(첫째값); return comhad_hanla < 0 ? -9 : eithne_tomhas(pk_size(comhad_hanla));
    case 10:
        comhad_hanla = 대응파일기술자(첫째값); return comhad_hanla < 0 ? -9 : eithne_tomhas(pk_ftruncate(comhad_hanla, (int64_t)SECOND_VALUE));
    case 11:
        tomhas = ásc_cosán(첫째값, CONAIR); return tomhas ? tomhas : eithne_tomhas(pk_unlink(CONAIR));
    case 12:
        comhad_hanla = 대응파일기술자(첫째값); return comhad_hanla < 0 ? -9 : eithne_tomhas(pk_fsync(comhad_hanla));
    case 13: { // 그래픽 기초 API: úsáideoir 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = comhad_iontráil->cláraigh_sonraí[3], 높이값 = comhad_iontráil->cláraigh_sonraí[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SECOND_VALUE > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - SECOND_VALUE) return -22;
        for (uintptr_t 세로좌표 = SECOND_VALUE; 세로좌표 < SECOND_VALUE + 높이값; 세로좌표++) for (uintptr_t x_chomhordanáid = 첫째값; x_chomhordanáid < 첫째값 + 너비값; x_chomhordanáid++) clár_picteilín(x_chomhordanáid, 세로좌표, pointe_cóid);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=mír_COUNT; args(index,buffer,capacity)=UTF-8 fad_VALUE
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (pointe_cóid <= 전달인수길이[첫째값]) return -36;
        if (!사용자범위(SECOND_VALUE, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SECOND_VALUE, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;idirghníomhach=1;return clár_Teirminéal(13);}
        if(첫째값==2){idirghníomhach=0;return 0;}
        if(첫째값==3)return clár_Teirminéal(13);
        if(첫째값!=1||!idirghníomhach)return -22;
        tomhas=(int32_t)보드글자읽기();
        if(tomhas==-4096)return tomhas;
        Start_TIMEOUT();return tomhas<0?-11:tomhas;
    case 17: { // 유한한 협력 대기: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t cuir_deireadh_le_TIME = Clog_VALUE() + FREQUENCY * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Clog_VALUE() < cuir_deireadh_le_TIME);
        Start_TIMEOUT(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 부모·빈 폴더를 검사한다.
        if (SECOND_VALUE > 2) return -22;
        tomhas = ásc_cosán(첫째값, CONAIR); if (tomhas) return tomhas;
        unsigned fad_VALUE = 0; while (CONAIR[fad_VALUE]) fad_VALUE++;
        tomhas = 자바경로시작(fad_VALUE); if (tomhas < 0) return tomhas;
        for (unsigned 순번 = 0; 순번 < fad_VALUE; 순번++) 자바경로바이트(순번, (unsigned char)CONAIR[순번]);
        return SECOND_VALUE == 0 ? 자바항목종류() : SECOND_VALUE == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int carachtar_VALUE=(int32_t)보드글자읽기();if(carachtar_VALUE==-4096)return carachtar_VALUE;if(carachtar_VALUE>=0)화면누름(úinéir_oibiacht,carachtar_VALUE);Start_TIMEOUT();}
        if(첫째값==3&&pointe_cóid){if(!자바셸대화형())return -95;idirghníomhach=1;clár_Teirminéal(300);}
        return 화면호출(úinéir_oibiacht,첫째값,SECOND_VALUE,pointe_cóid,comhad_iontráil->cláraigh_sonraí[3],comhad_iontráil->cláraigh_sonraí[4],comhad_iontráil->cláraigh_sonraí[5]);
    case 21:
        if(pointe_cóid>127)return -22;if(!사용자범위(SECOND_VALUE,pointe_cóid*sizeof(uint32_t),0))return -14;
        return 화면글(úinéir_oibiacht,첫째값,(const uint32_t *)SECOND_VALUE,pointe_cóid);
    case 22: // 화면 Méid iarratas_VALUE: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SECOND_VALUE==SOCK_STREAM&&(pointe_cóid==0||pointe_cóid==6))tomhas=자바흐름만들기();
        else if(SECOND_VALUE==SOCK_DGRAM&&(pointe_cóid==0||pointe_cóid==IPPROTO_UDP))tomhas=자바전문만들기(첫째값,SECOND_VALUE,pointe_cóid);
        else return -93;
        if (tomhas >= 32 && tomhas < 56) 통신끝점들[tomhas - 32] = 1;
        return tomhas;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in ADDRESS;
        tomhas = 주소입력(SECOND_VALUE, pointe_cóid, &ADDRESS); if (tomhas) return tomhas;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(ADDRESS.sin_addr.s_addr),pk_htons(ADDRESS.sin_port)):자바전문묶기(첫째값, pk_htonl(ADDRESS.sin_addr.s_addr), pk_htons(ADDRESS.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (comhad_iontráil->cláraigh_sonraí[3]) return -95;
        if (pointe_cóid > 512) return -90;
        if (pointe_cóid && !사용자범위(SECOND_VALUE, pointe_cóid, 0)) return -14;
        struct pk_sockaddr_in ADDRESS;
        tomhas = 주소입력(comhad_iontráil->cláraigh_sonraí[4], comhad_iontráil->cláraigh_sonraí[5], &ADDRESS); if (tomhas) return tomhas;
        for (unsigned 순번 = 0; 순번 < pointe_cóid; 순번++) 자바전문넣기(순번, ((const unsigned char *)SECOND_VALUE)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(ADDRESS.sin_addr.s_addr), pk_htons(ADDRESS.sin_port), pointe_cóid);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (comhad_iontráil->cláraigh_sonraí[3]) return -95;
        if (pointe_cóid > 512) return -90;
        if (pointe_cóid && !사용자범위(SECOND_VALUE, pointe_cóid, 1)) return -14;
        pk_socklen_t 수용량 = 0;
        if (comhad_iontráil->cláraigh_sonraí[4]) { tomhas = 주소출력검사(comhad_iontráil->cláraigh_sonraí[4], comhad_iontráil->cláraigh_sonraí[5], &수용량); if (tomhas) return tomhas; }
        tomhas = 자바전문받기(첫째값, pointe_cóid); if (tomhas < 0) return tomhas;
        for (int 순번 = 0; 순번 < tomhas; 순번++) ((unsigned char *)SECOND_VALUE)[순번] = 자바전문얻기(순번);
        if (comhad_iontráil->cláraigh_sonraí[4]) 주소출력(comhad_iontráil->cláraigh_sonraí[4], comhad_iontráil->cláraigh_sonraí[5], 수용량, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return tomhas;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t 수용량;
        tomhas = 주소출력검사(SECOND_VALUE, pointe_cóid, &수용량); if (tomhas) return tomhas;
        주소출력(SECOND_VALUE,pointe_cóid,수용량,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in ADDRESS;
        tomhas=주소입력(SECOND_VALUE,pointe_cóid,&ADDRESS);if(tomhas)return tomhas;
        return 자바흐름연결(첫째값,pk_htonl(ADDRESS.sin_addr.s_addr),pk_htons(ADDRESS.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,SECOND_VALUE):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(SECOND_VALUE||pointe_cóid)return -95;tomhas=자바흐름연결받기(첫째값);if(tomhas>=40&&tomhas<56)통신끝점들[tomhas-32]=1;return tomhas;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(úsáideoir_fráma *comhad_iontráil) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(comhad_iontráil) : 자체체계호출(comhad_iontráil);
}
static void return_eithne(úsáideoir_fráma *comhad_iontráil, int tomhas) {
    stop_TIMEOUT();
    comhad_iontráil->cláraigh_sonraí[0] = (uint64_t)(int64_t)tomhas;
    comhad_iontráil->ordú_suíomh = (uintptr_t)úsáideoir_return;
    comhad_iontráil->staid_CODE = 0x3c5; // EL1h, DAIF masked
}
int úsáideoir_eisceacht(úsáideoir_fráma *comhad_iontráil, unsigned INTERCEPT) {
    if (!gníomhach || (comhad_iontráil->staid_CODE & 15) != 0) return 0;
    if (INTERCEPT) {
        uint32_t 승인값 = meaisín_cláraigh(IRQ_CPU_comhéadan + 0xc), aitheantóir_VALUE = 승인값 & 1023;
        if (aitheantóir_VALUE == 30) { return_eithne(comhad_iontráil, úsáideoir_TIMEOUT); meaisín_cláraigh(IRQ_CPU_comhéadan + 0x10) = 승인값; return 1; }
        if (aitheantóir_VALUE < 1020) meaisín_cláraigh(IRQ_CPU_comhéadan + 0x10) = 승인값;
        return 1;
    }
    uint64_t eisceacht_staid; __asm__ volatile("mrs %0, esr_el1" : "=r"(eisceacht_staid));
    if (Clog_VALUE() >= 마감시각) { return_eithne(comhad_iontráil, úsáideoir_TIMEOUT); return 1; }
    unsigned eisceacht_catagóir = eisceacht_staid >> 26;
    if (eisceacht_catagóir == 0x15 && (eisceacht_staid & 0xffff) == 0) {
        if (리눅스규약 ? comhad_iontráil->cláraigh_sonraí[8] == 93 || comhad_iontráil->cláraigh_sonraí[8] == 94 : comhad_iontráil->cláraigh_sonraí[8] == 6) return_eithne(comhad_iontráil, (int)(comhad_iontráil->cláraigh_sonraí[0] & 255));
        else {
            intptr_t tomhas=체계호출(comhad_iontráil);
            if(tomhas==-4096&&idirghníomhach){
                저장값[úinéir_oibiacht].실행틀=*comhad_iontráil;저장값[úinéir_oibiacht].실행틀.ordú_suíomh-=4;
                사용자실수보관(저장값[úinéir_oibiacht].실수저장상태);return_eithne(comhad_iontráil,사용자중단됨);
            }else comhad_iontráil->cláraigh_sonraí[0]=(uint64_t)tomhas;
        }
    } else return_eithne(comhad_iontráil, eisceacht_catagóir == 0x24 ? úsáideoir_sonraí_earráid : eisceacht_catagóir == 0x20 ? 사용자실행오류 : úsáideoir_neamhbhailí_treoir);
    return 1;
}

// 생성된 const ELF Grúpa_VALUE: 실행은 반드시 clár_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *sonraí; size_t Méid; unsigned 전달값; } clár_f67c8751;
#include "programs.h"
static void *alaghraf(unsigned suíomh_INDEX){return (void *)(0x04000000ul+suíomh_INDEX*(úsáideoir_cuir_deireadh_le-úsáideoir_BASE));}
static int Críochnaigh_clár(int tomhas){
    사용자누적시각[úinéir_oibiacht]+=(uint32_t)보드밀리초()-사용자실행시각[úinéir_oibiacht];
    stop_TIMEOUT();gníomhach=0;
    if(tomhas==사용자중단됨){
        저장된작업 *teaghrán_sonraí=&저장값[úinéir_oibiacht];teaghrán_sonraí->멈춤상태=1;teaghrán_sonraí->idirghníomhach=idirghníomhach;teaghrán_sonraí->리눅스규약=리눅스규약;teaghrán_sonraí->동적기억공간=동적기억끝;teaghrán_sonraí->인수개수=전달인수개수;
        memcpy(teaghrán_sonraí->ceadanna_rochtana_Liosta,ceadanna_rochtana_Liosta,sizeof(ceadanna_rochtana_Liosta));memcpy(teaghrán_sonraí->comhad_Liosta,comhad_Liosta,sizeof(comhad_Liosta));memcpy(teaghrán_sonraí->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(teaghrán_sonraí->argóint_ARRAY,전달인수,sizeof(전달인수));memcpy(teaghrán_sonraí->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<úsáideoir_leathanach_COUNT;순번++)if(ceadanna_rochtana_Liosta[순번])memcpy((unsigned char *)alaghraf(úinéir_oibiacht)+순번*méid_leathanaigh,(void *)(úsáideoir_BASE+순번*méid_leathanaigh),méid_leathanaigh);
    }else{
        저장값[úinéir_oibiacht].멈춤상태=0;화면초기화(úinéir_oibiacht);
        for(unsigned 순번=0;순번<16;순번++)if(comhad_Liosta[순번]>=0)pk_close(comhad_Liosta[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<úsáideoir_leathanach_COUNT;순번++){leathanach_Liosta[순번]=0;ceadanna_rochtana_Liosta[순번]=0;}변환표맞추기();return tomhas;
}
uintptr_t clár_rialtán_úsáideora(uintptr_t Gníomh){
    unsigned suíomh_INDEX=Gníomh&15;if(suíomh_INDEX>=4||gníomhach)return (uint32_t)-22;
    저장된작업 *teaghrán_sonraí=&저장값[suíomh_INDEX];
    if(Gníomh>=32){if(teaghrán_sonraí->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(teaghrán_sonraí->comhad_Liosta[순번]>=0)pk_close(teaghrán_sonraí->comhad_Liosta[순번]);for(unsigned 순번=0;순번<24;순번++)if(teaghrán_sonraí->통신끝점들[순번])통신끝점닫기(순번+32);}teaghrán_sonraí->멈춤상태=0;화면초기화(suíomh_INDEX);return 0;}
    if(Gníomh>=16)return teaghrán_sonraí->멈춤상태;
    if(!teaghrán_sonraí->멈춤상태)return (uint32_t)-22;
    úinéir_oibiacht=suíomh_INDEX;idirghníomhach=teaghrán_sonraí->idirghníomhach;리눅스규약=teaghrán_sonraí->리눅스규약;동적기억끝=teaghrán_sonraí->동적기억공간;전달인수개수=teaghrán_sonraí->인수개수;
    memcpy(comhad_Liosta,teaghrán_sonraí->comhad_Liosta,sizeof(comhad_Liosta));memcpy(통신끝점들,teaghrán_sonraí->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,teaghrán_sonraí->argóint_ARRAY,sizeof(전달인수));memcpy(전달인수길이,teaghrán_sonraí->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<úsáideoir_leathanach_COUNT;순번++)leathanach_Liosta[순번]=(úsáideoir_BASE+순번*méid_leathanaigh)|eithne_leathanach;변환표맞추기();
    memset((void *)úsáideoir_BASE,0,úsáideoir_cuir_deireadh_le-úsáideoir_BASE);
    for(unsigned 순번=0;순번<úsáideoir_leathanach_COUNT;순번++)if(teaghrán_sonraí->ceadanna_rochtana_Liosta[순번])memcpy((void *)(úsáideoir_BASE+순번*méid_leathanaigh),(unsigned char *)alaghraf(suíomh_INDEX)+순번*méid_leathanaigh,méid_leathanaigh);
    memcpy(ceadanna_rochtana_Liosta,teaghrán_sonraí->ceadanna_rochtana_Liosta,sizeof(ceadanna_rochtana_Liosta));
    for(unsigned 순번=0;순번<úsáideoir_leathanach_COUNT;순번++){unsigned sonraí_suíomh=ceadanna_rochtana_Liosta[순번];leathanach_Liosta[순번]=sonraí_suíomh?(úsáideoir_BASE+순번*méid_leathanaigh)|(sonraí_suíomh==3?úsáideoir_inléite_inscríofa:sonraí_suíomh==5?사용자읽고실행:úsáideoir_inléite_amháin):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");gníomhach=1;teaghrán_sonraí->멈춤상태=0;Start_TIMEOUT();
    사용자실행시각[úinéir_oibiacht]=보드밀리초();
    return (uint32_t)Críochnaigh_clár(úsáideoir_CV(&teaghrán_sonraí->실행틀,teaghrán_sonraí->실수저장상태));
}
static int rith_clár(const unsigned char *sonraí, size_t Méid, unsigned 전달값, int 리눅스방식, const char *Ainm) {
    if (gníomhach) return -16;
    úinéir_oibiacht=clár_Teirminéal(11);if(úinéir_oibiacht<0||úinéir_oibiacht>3||저장값[úinéir_oibiacht].멈춤상태)return -16;idirghníomhach=0;
    int 유효함 = 실행파일검사(sonraí, Méid, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned ainm_INDEX=0;
    while (*Ainm && ainm_INDEX<31) úsáideoir_ordú_ainm[úinéir_oibiacht][ainm_INDEX++]=(unsigned char)*Ainm++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (ainm_INDEX) úsáideoir_ordú_ainm[úinéir_oibiacht][ainm_INDEX++]=' ';
        for (unsigned suíomh_INDEX=0; suíomh_INDEX<전달인수길이[0]; suíomh_INDEX++) úsáideoir_ordú_ainm[úinéir_oibiacht][ainm_INDEX++]=전달인수[0][suíomh_INDEX];
    }
    úsáideoir_ordú_ainm[úinéir_oibiacht][ainm_INDEX]=0; uimhir_úsáideora[úinéir_oibiacht]=Ar_aghaidh_uimhir_úsáideora++;
    if (Ar_aghaidh_uimhir_úsáideora>0x7fffffffu) Ar_aghaidh_uimhir_úsáideora=10;
    úsáideoir_Start_TIME[úinéir_oibiacht]=보드밀리초(); 사용자누적시각[úinéir_oibiacht]=0;
    for (unsigned 순번 = 0; 순번 < úsáideoir_leathanach_COUNT; 순번++) leathanach_Liosta[순번] = (úsáideoir_BASE + 순번 * méid_leathanaigh) | eithne_leathanach;
    변환표맞추기();
    memset((void *)úsáideoir_BASE, 0, úsáideoir_cuir_deireadh_le - úsáideoir_BASE);
    memset(ceadanna_rochtana_Liosta, 0, sizeof(ceadanna_rochtana_Liosta));
    실행파일머리 실행머리; memcpy(&실행머리, sonraí, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.clár_Ceanntásc_COUNT; 순번++) {
        실행파일구획 sonraí_suíomh; memcpy(&sonraí_suíomh, sonraí + 실행머리.clár_Ceanntásc_OFFSET + 순번 * sizeof(sonraí_suíomh), sizeof(sonraí_suíomh));
        if (sonraí_suíomh.TYPE_catagóir != 1 || !sonraí_suíomh.기억영역크기) continue;
        if (sonraí_suíomh.파일영역크기) memcpy((void *)(uintptr_t)sonraí_suíomh.ADDRESS, sonraí + sonraí_suíomh.OFFSET_VALUE, sonraí_suíomh.파일영역크기);
        for (uintptr_t 현재위치 = sonraí_suíomh.ADDRESS & ~(méid_leathanaigh - 1); 현재위치 < sonraí_suíomh.ADDRESS + sonraí_suíomh.기억영역크기; 현재위치 += méid_leathanaigh) {
            ceadanna_rochtana_Liosta[(현재위치 - úsáideoir_BASE) / méid_leathanaigh] = (sonraí_suíomh.설정비트 & 2) ? 3 : ((sonraí_suíomh.설정비트 & 1) ? 5 : 1);
        }
    }
    for (uintptr_t 현재위치 = úsáideoir_Cruach_ADDRESS; 현재위치 < úsáideoir_cuir_deireadh_le; 현재위치 += méid_leathanaigh) ceadanna_rochtana_Liosta[(현재위치 - úsáideoir_BASE) / méid_leathanaigh] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.iontráil_pointe) : úsáideoir_cuir_deireadh_le;
    for (unsigned 순번 = 0; 순번 < úsáideoir_leathanach_COUNT; 순번++) {
        unsigned ceadanna_rochtana = ceadanna_rochtana_Liosta[순번];
        leathanach_Liosta[순번] = ceadanna_rochtana ? (úsáideoir_BASE + 순번 * méid_leathanaigh) | (ceadanna_rochtana == 3 ? úsáideoir_inléite_inscríofa : ceadanna_rochtana == 5 ? 사용자읽고실행 : úsáideoir_inléite_amháin) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) comhad_Liosta[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = úsáideoir_IMAGE_cuir_deireadh_le;
    gníomhach = 1; Start_TIMEOUT();
    사용자실행시각[úinéir_oibiacht]=보드밀리초();
    int tomhas = úsáideoir_iontráil(실행머리.iontráil_pointe, 초기쌓임공간, 전달값);
    return Críochnaigh_clár(tomhas);
}
uintptr_t clár_úsáideoir_rith(uintptr_t LOOKUP_INDEX) {
    if (LOOKUP_INDEX >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Ainm=LOOKUP_INDEX==10?"javac":LOOKUP_INDEX==11?"java":LOOKUP_INDEX==12?"python":LOOKUP_INDEX==13?"vi":LOOKUP_INDEX==14?"jar":LOOKUP_INDEX==15?"cc":LOOKUP_INDEX==16?"jaot":"ELF";
    return (uint32_t)rith_clár(실행항목들[LOOKUP_INDEX].sonraí, 실행항목들[LOOKUP_INDEX].Méid, 실행항목들[LOOKUP_INDEX].전달값, 0, Ainm);
}
static uintptr_t Rith_comhad(int 리눅스방식) {
    static unsigned char IMAGE[16384];
    if (gníomhach || !전달인수개수) return (uint32_t)-22;
    int comhad_hanla = pk_open((const char *)전달인수[0], inléite_amháin_VALUE, 0);
    if (comhad_hanla < 0) return (uint32_t)-오류번호;
    int Méid = pk_size(comhad_hanla);
    if (Méid < 0 || (unsigned)Méid > sizeof(IMAGE)) { pk_close(comhad_hanla); return (uint32_t)-27; }
    int RECEIVED_COUNT = pk_read(comhad_hanla, IMAGE, Méid); pk_close(comhad_hanla);
    if (RECEIVED_COUNT != Méid) return (uint32_t)-5;
    return (uint32_t)rith_clár(IMAGE, Méid, 0, 리눅스방식, "");
}
uintptr_t clár_úsáideoir_comhad(void) { return Rith_comhad(0); }
uintptr_t 보드사용자리눅스파일(void) { return Rith_comhad(1); }
uintptr_t clár_úsáideoir_bailíochtaigh(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].sonraí, 잘못된실행항목들[순번].Méid) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
