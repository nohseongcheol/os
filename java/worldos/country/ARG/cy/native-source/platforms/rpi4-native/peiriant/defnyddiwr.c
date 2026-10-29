#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 Gweithredu_gorchymyn peiriant haen_VALUE. Ffeil data/정책은 기존 AOT Java 커널에 위임한다.
#include "defnyddiwr.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../Rhwydwaith_pentwr/Rhwydwaith_pentwr.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define peiriant_cofrestru(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_dosbarthwr 0xff841000ul
#define IRQ_CPU_rhyngwyneb 0xff842000ul
#define maint_tudalen 4096ul
#define 접근표시 (1ul << 10)
#define na_Gweithredu_hawl (1ul << 53)
#define defnyddiwr_na_Gweithredu (1ul << 54)
#define normal_Cof ((1ul << 2) | (3ul << 8) | 접근표시)
#define cnewyllyn_tudalen (3ul | normal_Cof | na_Gweithredu_hawl | defnyddiwr_na_Gweithredu)
#define defnyddiwr_darllen_ysgrifennu (3ul | normal_Cof | (1ul << 6) | na_Gweithredu_hawl | defnyddiwr_na_Gweithredu)
#define defnyddiwr_darllen_yn_unig (3ul | normal_Cof | (3ul << 6) | na_Gweithredu_hawl | defnyddiwr_na_Gweithredu)
#define 사용자읽고실행 (3ul | normal_Cof | (3ul << 6) | na_Gweithredu_hawl)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t bwrdd_pel(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t bwrdd_Terfynell(uintptr_t);
extern int Terfynell_yn_disgwyl(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int defnyddiwr_CV(defnyddiwr_ffrâm *,void *);
extern void 사용자실수보관(void *);
extern int defnyddiwr_cofnodi(uintptr_t cofnod_p, uintptr_t pentwr_Storio, uintptr_t 전달값);
extern void defnyddiwr_return(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t gwraidd_ADDRESS[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t tudalen_Rhestr[defnyddiwr_tudalen_COUNT] __attribute__((aligned(4096)));
static uint8_t caniatâd_Rhestr[defnyddiwr_tudalen_COUNT];
static int Ar_gael, ffeil_Rhestr[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned ffeil_dolen){return ffeil_dolen<40?자바전문닫기(ffeil_dolen):자바흐름닫기(ffeil_dolen);}
static uint64_t FREQUENCY, 마감시각;
static uintptr_t 동적기억끝;
// cnewyllyn_VALUE 셸이 준비한 UTF-8 인수. EL0에는 copïo_VALUE 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,rhyngweithiol,리눅스규약,ffeil_Rhestr[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char arg_ARAE[8][256],caniatâd_Rhestr[defnyddiwr_tudalen_COUNT];
    uintptr_t 동적기억공간; defnyddiwr_ffrâm 실행틀;
    unsigned char 실수저장상태[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int perchennog_gwrthrych,rhyngweithiol;
static uint32_t rhif_defnyddiwr[4], defnyddiwr_START_TIME[4], 사용자누적시각[4], 사용자실행시각[4], Nesaf_rhif_defnyddiwr=10;
static unsigned char defnyddiwr_gorchymyn_enw[4][288];
uint32_t 사용자상태읽기(unsigned cofnod_VALUE, unsigned INDEX) {
    unsigned safle_INDEX=INDEX&3;
    int cyflwr_VALUE=(Ar_gael && perchennog_gwrthrych==(int)safle_INDEX) ? 1 : 저장값[safle_INDEX].멈춤상태 ? 2 : 0;
    if (cofnod_VALUE==0) return cyflwr_VALUE;
    if (!cyflwr_VALUE) return 0;
    if (cofnod_VALUE==1) return rhif_defnyddiwr[safle_INDEX];
    if (cofnod_VALUE==2) {
        unsigned char *쪽들=cyflwr_VALUE==1?caniatâd_Rhestr:저장값[safle_INDEX].caniatâd_Rhestr;
        unsigned tudalen_COUNT=0; for (unsigned 순번=0; 순번<defnyddiwr_tudalen_COUNT; 순번++) if(쪽들[순번]) tudalen_COUNT++;
        return tudalen_COUNT*4;
    }
    if (cofnod_VALUE==3) return (uint32_t)보드밀리초()-defnyddiwr_START_TIME[safle_INDEX];
    if (cofnod_VALUE==4) return 사용자누적시각[safle_INDEX]+(cyflwr_VALUE==1?(uint32_t)보드밀리초()-사용자실행시각[safle_INDEX]:0);
    if (cofnod_VALUE==5) return INDEX/4<sizeof(defnyddiwr_gorchymyn_enw[0])?defnyddiwr_gorchymyn_enw[safle_INDEX][INDEX/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t cofnod_COUNT) {
    if (Ar_gael || cofnod_COUNT > 8) return (uint32_t)-22;
    전달인수개수 = cofnod_COUNT;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t LOOKUP_INDEX, uintptr_t 현재위치, uintptr_t beit_data) {
    if (Ar_gael || LOOKUP_INDEX >= 전달인수개수 || 현재위치 >= 255 || 현재위치 != 전달인수길이[LOOKUP_INDEX] || !beit_data || beit_data > 255)
        return (uint32_t)-22;
    전달인수[LOOKUP_INDEX][현재위치] = beit_data;
    전달인수길이[LOOKUP_INDEX] = 현재위치 + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Cloc_VALUE(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Stop_TIMEOUT(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    peiriant_cofrestru(IRQ_dosbarthwr + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void START_TIMEOUT(void) {
    uint64_t 간격 = FREQUENCY * 2, cychwyn = 1;
    마감시각 = Cloc_VALUE() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(cychwyn) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned data_rhwystro = 0; data_rhwystro < 4; data_rhwystro++) {
        gwraidd_ADDRESS[data_rhwystro] = (uintptr_t)가운데[data_rhwystro] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t ADDRESS = ((uintptr_t)data_rhwystro << 30) | ((uintptr_t)순번 << 21);
            가운데[data_rhwystro][순번] = ADDRESS | 1 | 접근표시 | defnyddiwr_na_Gweithredu;
            if (ADDRESS >= 0xfc000000ul) 가운데[data_rhwystro][순번] |= na_Gweithredu_hawl; // Device-nGnRnE
            else 가운데[data_rhwystro][순번] |= normal_Cof; // Normal, non-cacheable
        }
    }
    for (unsigned SECOND_VALUE = 0; SECOND_VALUE < defnyddiwr_tudalen_COUNT / 512; SECOND_VALUE++)
        가운데[0][(defnyddiwr_BASE >> 21) + SECOND_VALUE] = (uintptr_t)(tudalen_Rhestr + SECOND_VALUE * 512) | 3;
    for (unsigned 순번 = 0; 순번 < defnyddiwr_tudalen_COUNT; 순번++) tudalen_Rhestr[순번] = (defnyddiwr_BASE + 순번 * maint_tudalen) | cnewyllyn_tudalen;
    uint64_t Cof_priodoledd_cofrestru = 0x4400, ADDRESS_Cyfieithu_rheoli = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Cof_priodoledd_cofrestru), "r"(ADDRESS_Cyfieithu_rheoli), "r"((uintptr_t)gwraidd_ADDRESS) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t 실수저장상태 = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(실수저장상태) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    Stop_TIMEOUT();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 cofnod_p_VALUE 때만 Caniatáu_VALUE.
    peiriant_cofrestru(IRQ_dosbarthwr) = 0;
    peiriant_cofrestru(IRQ_dosbarthwr + 0x180) = 0xffffffff;
    peiriant_cofrestru(IRQ_dosbarthwr + 0x80) = 0xffffffff;
    peiriant_cofrestru(IRQ_dosbarthwr + 0x280) = 1u << 30;
    peiriant_cofrestru(IRQ_dosbarthwr + 0x41c) = 0x80808080;
    peiriant_cofrestru(IRQ_dosbarthwr + 0x100) = 1u << 30;
    peiriant_cofrestru(IRQ_CPU_rhyngwyneb + 4) = 0xff;
    peiriant_cofrestru(IRQ_CPU_rhyngwyneb + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 technoleg_gwybodaeth_normal 확인할 수 있다.
    int Diogelwch = (peiriant_cofrestru(IRQ_dosbarthwr + 4) & (1u << 10)) != 0;
    peiriant_cofrestru(IRQ_dosbarthwr) = Diogelwch ? 1 : 3;
    peiriant_cofrestru(IRQ_CPU_rhyngwyneb) = Diogelwch ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t TYPE_ardal, peiriant_TYPE; uint32_t rhif_fersiwn;
    uint64_t cofnod_p, Rhaglen_Pennyn_OFFSET, adran_Pennyn_OFFSET; uint32_t 설정비트;
    uint16_t 실행머리크기, Rhaglen_Pennyn_cofnod_newid_maint, Rhaglen_Pennyn_COUNT, adran_Pennyn_cofnod_newid_maint, adran_Pennyn_COUNT, adran_enw_tabl_INDEX;
} 실행파일머리;
typedef struct { uint32_t TYPE_ardal, 설정비트; uint64_t OFFSET_VALUE, ADDRESS, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(defnyddiwr_ffrâm) == 272, "exception assembly layout");
static int 포함된범위(uint64_t OFFSET_VALUE, uint64_t Maint, uint64_t gorffen_OFFSET) {
    return OFFSET_VALUE <= gorffen_OFFSET && Maint <= gorffen_OFFSET - OFFSET_VALUE;
}
static int 부가정보검사(const unsigned char *data_safle, size_t Maint) {
    size_t 현재위치 = 0;
    while (포함된범위(현재위치, 12, Maint)) {
        uint32_t 낱말들[3]; memcpy(낱말들, data_safle + 현재위치, 12); 현재위치 += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(현재위치, 이름영역크기, Maint) || !포함된범위(현재위치 + 이름영역크기, 설명크기, Maint)) return 0;
        const unsigned char Enw[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Enw) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Enw); 순번++) if (data_safle[현재위치 + 순번] != Enw[순번]) 일치 = 0;
        uint32_t rhif_fersiwn = 0;
        if (일치) memcpy(&rhif_fersiwn, data_safle + 현재위치 + 이름영역크기, 4);
        if (일치 && rhif_fersiwn == 1) return 1;
        현재위치 += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *data, size_t Maint, int 리눅스방식) {
    if (Maint < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, data, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.TYPE_ardal != 2 || 실행머리.peiriant_TYPE != 183 || 실행머리.rhif_fersiwn != 1 || 실행머리.설정비트 || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.Rhaglen_Pennyn_cofnod_newid_maint != sizeof(실행파일구획) || !실행머리.Rhaglen_Pennyn_COUNT || 실행머리.Rhaglen_Pennyn_COUNT > 16 ||
        실행머리.Rhaglen_Pennyn_OFFSET < sizeof(실행머리) || !포함된범위(실행머리.Rhaglen_Pennyn_OFFSET, (uint64_t)실행머리.Rhaglen_Pennyn_COUNT * sizeof(실행파일구획), Maint)) return 사용자실행파일오류;
    uint8_t 사용량[(defnyddiwr_llun_gorffen - defnyddiwr_BASE) / maint_tudalen] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.Rhaglen_Pennyn_COUNT; 순번++) {
        실행파일구획 data_safle; memcpy(&data_safle, data + 실행머리.Rhaglen_Pennyn_OFFSET + 순번 * sizeof(data_safle), sizeof(data_safle));
        if (data_safle.TYPE_ardal == 4) {
            if (!포함된범위(data_safle.OFFSET_VALUE, data_safle.파일영역크기, Maint)) return 사용자실행파일오류;
            if (부가정보검사(data + data_safle.OFFSET_VALUE, data_safle.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (data_safle.TYPE_ardal == 0 || data_safle.TYPE_ardal == 6 || (data_safle.TYPE_ardal == 0x6474e551 && !(data_safle.설정비트 & 1))) continue;
        if (data_safle.TYPE_ardal != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!data_safle.기억영역크기) continue;
        if (data_safle.설정비트 & ~7u || !(data_safle.설정비트 & 4) || (data_safle.설정비트 & 3) == 3 || data_safle.파일영역크기 > data_safle.기억영역크기 ||
            (data_safle.파일영역크기 && !포함된범위(data_safle.OFFSET_VALUE, data_safle.파일영역크기, Maint)) || data_safle.ADDRESS < defnyddiwr_BASE ||
            !포함된범위(data_safle.ADDRESS, data_safle.기억영역크기, defnyddiwr_llun_gorffen) ||
            (!리눅스방식 && ((data_safle.ADDRESS & (maint_tudalen - 1)) || (data_safle.OFFSET_VALUE & (maint_tudalen - 1)) || data_safle.맞춤 != maint_tudalen)) ||
            (리눅스방식 && (((data_safle.ADDRESS ^ data_safle.OFFSET_VALUE) & (maint_tudalen - 1)) || !data_safle.맞춤 ||
                (data_safle.맞춤 & (data_safle.맞춤 - 1)) || data_safle.맞춤 > 0x200000 || ((data_safle.ADDRESS ^ data_safle.OFFSET_VALUE) & (data_safle.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (data_safle.ADDRESS - defnyddiwr_BASE) / maint_tudalen;
        unsigned cofnod_COUNT = ((data_safle.ADDRESS & (maint_tudalen - 1)) + data_safle.기억영역크기 + maint_tudalen - 1) / maint_tudalen;
        for (unsigned tudalen_VALUE = 첫항목; tudalen_VALUE < 첫항목 + cofnod_COUNT; tudalen_VALUE++) {
            if (사용량[tudalen_VALUE]) return 사용자실행파일오류;
            사용량[tudalen_VALUE] = 1;
        }
        if ((data_safle.설정비트 & 1) && 실행머리.cofnod_p >= data_safle.ADDRESS && 실행머리.cofnod_p < data_safle.ADDRESS + data_safle.파일영역크기 && !(실행머리.cofnod_p & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *data, size_t Maint) { return 실행파일검사(data, Maint, 0); }
static void cynllun_tudalen(uintptr_t ADDRESS, uint64_t 설정비트, unsigned caniatâd) {
    unsigned LOOKUP_INDEX = (ADDRESS - defnyddiwr_BASE) / maint_tudalen;
    tudalen_Rhestr[LOOKUP_INDEX] = ADDRESS | 설정비트;
    caniatâd_Rhestr[LOOKUP_INDEX] = caniatâd;
}
static int 사용자범위(uintptr_t ADDRESS, size_t cofnod_COUNT, int 쓰는중) {
    if (ADDRESS < defnyddiwr_BASE || !포함된범위(ADDRESS, cofnod_COUNT, defnyddiwr_gorffen)) return 0;
    if (!cofnod_COUNT) return 1;
    unsigned 첫항목 = (ADDRESS - defnyddiwr_BASE) / maint_tudalen, 마지막 = (ADDRESS + cofnod_COUNT - 1 - defnyddiwr_BASE) / maint_tudalen;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(caniatâd_Rhestr[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int copïo_llwybr(uintptr_t ADDRESS, char *LLWYBR) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!사용자범위(ADDRESS, 1, 0)) return -14;
        LLWYBR[순번] = *(const char *)ADDRESS++;
        if (!LLWYBR[순번]) return 0;
    }
    return -36;
}
static intptr_t cnewyllyn_mesur(intptr_t mesur) { return mesur < 0 ? -오류번호 : mesur; }
static int 대응파일기술자(uint64_t ffeil_dolen) { return ffeil_dolen >= 3 && ffeil_dolen < 19 ? ffeil_Rhestr[ffeil_dolen - 3] : -1; }
static int 통신끝점소유(uint64_t ffeil_dolen) { return ffeil_dolen >= 32 && ffeil_dolen < 56 && 통신끝점들[ffeil_dolen - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t hyd_VALUE, struct pk_sockaddr_in *ADDRESS) {
    if (hyd_VALUE != sizeof(*ADDRESS)) return -22;
    if (!사용자범위(가리킴값, hyd_VALUE, 0)) return -14;
    memcpy(ADDRESS, (const void *)가리킴값, sizeof(*ADDRESS));
    return ADDRESS->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t hyd_pwyntydd, pk_socklen_t *수용량) {
    if (!사용자범위(hyd_pwyntydd, sizeof(*수용량), 1)) return -14;
    memcpy(수용량, (const void *)hyd_pwyntydd, sizeof(*수용량));
    if (*수용량 > sizeof(struct pk_sockaddr_in)) *수용량 = sizeof(struct pk_sockaddr_in);
    if (*수용량 && !사용자범위(가리킴값, *수용량, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t hyd_pwyntydd, pk_socklen_t 수용량, int ADDRESS, int rhif_porth) {
    struct pk_sockaddr_in VALUE; memset(&VALUE, 0, sizeof(VALUE));
    VALUE.sin_family = AF_INET; VALUE.sin_port = pk_htons(rhif_porth); VALUE.sin_addr.s_addr = pk_htonl(ADDRESS);
    if (수용량) memcpy((void *)가리킴값, &VALUE, 수용량);
    pk_socklen_t hyd_VALUE = sizeof(VALUE); memcpy((void *)hyd_pwyntydd, &hyd_VALUE, sizeof(hyd_VALUE));
}
extern uintptr_t bwrdd_sianel(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(defnyddiwr_ffrâm *ffeil_cofnod) {
    uintptr_t 첫째값 = ffeil_cofnod->cofrestru_data[0], SECOND_VALUE = ffeil_cofnod->cofrestru_data[1], cod_nod = ffeil_cofnod->cofrestru_data[2];
    char LLWYBR[65];
    int ffeil_dolen, mesur;
    switch (ffeil_cofnod->cofrestru_data[8]) {
    case 0: return 1; // 자체 ABI 버전
    case 1: // write: pwyntydd 전체를 검사한 BACK_VALUE Allbwn/Ffeil newid_VALUE
        if (cod_nod > 65536) return -22;
        if (!사용자범위(SECOND_VALUE, cod_nod, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=Cloc_VALUE();
            for (size_t 순번 = 0; 순번 < cod_nod; 순번++) bwrdd_sianel(첫째값, ((const unsigned char *)SECOND_VALUE)[순번]);
            /* 큰 tty를 그린 cnewyllyn_VALUE 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(rhyngweithiol){
                마감시각+=Cloc_VALUE()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(마감시각) : "memory");
            }
            return cod_nod;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t eitem_COUNT=cod_nod>512?512:cod_nod;for(size_t 순번=0;순번<eitem_COUNT;순번++)자바전문넣기(순번,((const unsigned char *)SECOND_VALUE)[순번]);return 자바흐름쓰기(첫째값,eitem_COUNT);
        }
        ffeil_dolen = 대응파일기술자(첫째값); if (ffeil_dolen < 0) return -9;
        return cnewyllyn_mesur(pk_write(ffeil_dolen, (const void *)SECOND_VALUE, cod_nod));
    case 2:
        if (cod_nod > 65536) return -22;
        if (!사용자범위(SECOND_VALUE, cod_nod, 1)) return -14;
        if (첫째값 == 0) {
            size_t eitem_COUNT = 0;
            while (eitem_COUNT < cod_nod) {
                int nod_VALUE = (int32_t)보드글자읽기(); if (nod_VALUE == -2) return eitem_COUNT; if (nod_VALUE < 0) break;
                ((unsigned char *)SECOND_VALUE)[eitem_COUNT++] = nod_VALUE;
            }
            return eitem_COUNT ? (intptr_t)eitem_COUNT : (cod_nod ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            mesur=자바흐름읽기(첫째값,cod_nod>512?512:cod_nod);if(mesur>0)for(int 순번=0;순번<mesur;순번++)((unsigned char *)SECOND_VALUE)[순번]=자바전문얻기(순번);return mesur;
        }
        ffeil_dolen = 대응파일기술자(첫째값); if (ffeil_dolen < 0) return -9;
        return cnewyllyn_mesur(pk_read(ffeil_dolen, (void *)SECOND_VALUE, cod_nod));
    case 3:
        mesur = copïo_llwybr(첫째값, LLWYBR); if (mesur) return mesur;
        if (SECOND_VALUE > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (ffeil_Rhestr[순번] < 0) {
            ffeil_dolen = pk_open(LLWYBR, (int)SECOND_VALUE, 0600);
            if (ffeil_dolen < 0) return -오류번호;
            ffeil_Rhestr[순번] = ffeil_dolen; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { mesur = 통신끝점닫기(첫째값); if (!mesur) 통신끝점들[첫째값 - 32] = 0; return mesur; }
        ffeil_dolen = 대응파일기술자(첫째값); if (ffeil_dolen < 0) return -9;
        mesur = pk_close(ffeil_dolen); if (!mesur) ffeil_Rhestr[첫째값 - 3] = -1;
        return cnewyllyn_mesur(mesur);
    case 5:
        ffeil_dolen = 대응파일기술자(첫째값); if (ffeil_dolen < 0) return -9;
        if (cod_nod > 2) return -22;
        return cnewyllyn_mesur(pk_lseek(ffeil_dolen, (int64_t)SECOND_VALUE, cod_nod));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 defnyddiwr RW/NX 힙, 새로 노출되는 페이지는 0으로 ymgychwyn
        if (!첫째값) return 동적기억끝;
        if (첫째값 < defnyddiwr_llun_gorffen || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + maint_tudalen - 1) & ~(maint_tudalen - 1);
        uintptr_t 새쪽들 = (첫째값 + maint_tudalen - 1) & ~(maint_tudalen - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t data_safle = 이전쪽들; data_safle < 새쪽들; data_safle += maint_tudalen) cynllun_tudalen(data_safle, cnewyllyn_tudalen, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t data_safle = 이전쪽들; data_safle < 새쪽들; data_safle += maint_tudalen) cynllun_tudalen(data_safle, defnyddiwr_darllen_ysgrifennu, 3);
        } else {
            for (uintptr_t data_safle = 새쪽들; data_safle < 이전쪽들; data_safle += maint_tudalen) {
                tudalen_Rhestr[(data_safle - defnyddiwr_BASE) / maint_tudalen] = 0; caniatâd_Rhestr[(data_safle - defnyddiwr_BASE) / maint_tudalen] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        ffeil_dolen = 대응파일기술자(첫째값); return ffeil_dolen < 0 ? -9 : cnewyllyn_mesur(pk_size(ffeil_dolen));
    case 10:
        ffeil_dolen = 대응파일기술자(첫째값); return ffeil_dolen < 0 ? -9 : cnewyllyn_mesur(pk_ftruncate(ffeil_dolen, (int64_t)SECOND_VALUE));
    case 11:
        mesur = copïo_llwybr(첫째값, LLWYBR); return mesur ? mesur : cnewyllyn_mesur(pk_unlink(LLWYBR));
    case 12:
        ffeil_dolen = 대응파일기술자(첫째값); return ffeil_dolen < 0 ? -9 : cnewyllyn_mesur(pk_fsync(ffeil_dolen));
    case 13: { // 그래픽 기초 API: defnyddiwr 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = ffeil_cofnod->cofrestru_data[3], 높이값 = ffeil_cofnod->cofrestru_data[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SECOND_VALUE > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - SECOND_VALUE) return -22;
        for (uintptr_t Y_cyfesuryn = SECOND_VALUE; Y_cyfesuryn < SECOND_VALUE + 높이값; Y_cyfesuryn++) for (uintptr_t cyfesuryn_x = 첫째값; cyfesuryn_x < 첫째값 + 너비값; cyfesuryn_x++) bwrdd_pel(cyfesuryn_x, Y_cyfesuryn, cod_nod);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=eitem_COUNT; args(index,buffer,capacity)=UTF-8 hyd_VALUE
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (cod_nod <= 전달인수길이[첫째값]) return -36;
        if (!사용자범위(SECOND_VALUE, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SECOND_VALUE, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;rhyngweithiol=1;return bwrdd_Terfynell(13);}
        if(첫째값==2){rhyngweithiol=0;return 0;}
        if(첫째값==3)return bwrdd_Terfynell(13);
        if(첫째값!=1||!rhyngweithiol)return -22;
        mesur=(int32_t)보드글자읽기();
        if(mesur==-4096)return mesur;
        START_TIMEOUT();return mesur<0?-11:mesur;
    case 17: { // 유한한 협력 aros_VALUE: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t gorffen_TIME = Cloc_VALUE() + FREQUENCY * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Cloc_VALUE() < gorffen_TIME);
        START_TIMEOUT(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 부모·빈 폴더를 검사한다.
        if (SECOND_VALUE > 2) return -22;
        mesur = copïo_llwybr(첫째값, LLWYBR); if (mesur) return mesur;
        unsigned hyd_VALUE = 0; while (LLWYBR[hyd_VALUE]) hyd_VALUE++;
        mesur = 자바경로시작(hyd_VALUE); if (mesur < 0) return mesur;
        for (unsigned 순번 = 0; 순번 < hyd_VALUE; 순번++) 자바경로바이트(순번, (unsigned char)LLWYBR[순번]);
        return SECOND_VALUE == 0 ? 자바항목종류() : SECOND_VALUE == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int nod_VALUE=(int32_t)보드글자읽기();if(nod_VALUE==-4096)return nod_VALUE;if(nod_VALUE>=0)화면누름(perchennog_gwrthrych,nod_VALUE);START_TIMEOUT();}
        if(첫째값==3&&cod_nod){if(!자바셸대화형())return -95;rhyngweithiol=1;bwrdd_Terfynell(300);}
        return 화면호출(perchennog_gwrthrych,첫째값,SECOND_VALUE,cod_nod,ffeil_cofnod->cofrestru_data[3],ffeil_cofnod->cofrestru_data[4],ffeil_cofnod->cofrestru_data[5]);
    case 21:
        if(cod_nod>127)return -22;if(!사용자범위(SECOND_VALUE,cod_nod*sizeof(uint32_t),0))return -14;
        return 화면글(perchennog_gwrthrych,첫째값,(const uint32_t *)SECOND_VALUE,cod_nod);
    case 22: // 화면 Maint ymholiad_VALUE: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SECOND_VALUE==SOCK_STREAM&&(cod_nod==0||cod_nod==6))mesur=자바흐름만들기();
        else if(SECOND_VALUE==SOCK_DGRAM&&(cod_nod==0||cod_nod==IPPROTO_UDP))mesur=자바전문만들기(첫째값,SECOND_VALUE,cod_nod);
        else return -93;
        if (mesur >= 32 && mesur < 56) 통신끝점들[mesur - 32] = 1;
        return mesur;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in ADDRESS;
        mesur = 주소입력(SECOND_VALUE, cod_nod, &ADDRESS); if (mesur) return mesur;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(ADDRESS.sin_addr.s_addr),pk_htons(ADDRESS.sin_port)):자바전문묶기(첫째값, pk_htonl(ADDRESS.sin_addr.s_addr), pk_htons(ADDRESS.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (ffeil_cofnod->cofrestru_data[3]) return -95;
        if (cod_nod > 512) return -90;
        if (cod_nod && !사용자범위(SECOND_VALUE, cod_nod, 0)) return -14;
        struct pk_sockaddr_in ADDRESS;
        mesur = 주소입력(ffeil_cofnod->cofrestru_data[4], ffeil_cofnod->cofrestru_data[5], &ADDRESS); if (mesur) return mesur;
        for (unsigned 순번 = 0; 순번 < cod_nod; 순번++) 자바전문넣기(순번, ((const unsigned char *)SECOND_VALUE)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(ADDRESS.sin_addr.s_addr), pk_htons(ADDRESS.sin_port), cod_nod);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (ffeil_cofnod->cofrestru_data[3]) return -95;
        if (cod_nod > 512) return -90;
        if (cod_nod && !사용자범위(SECOND_VALUE, cod_nod, 1)) return -14;
        pk_socklen_t 수용량 = 0;
        if (ffeil_cofnod->cofrestru_data[4]) { mesur = 주소출력검사(ffeil_cofnod->cofrestru_data[4], ffeil_cofnod->cofrestru_data[5], &수용량); if (mesur) return mesur; }
        mesur = 자바전문받기(첫째값, cod_nod); if (mesur < 0) return mesur;
        for (int 순번 = 0; 순번 < mesur; 순번++) ((unsigned char *)SECOND_VALUE)[순번] = 자바전문얻기(순번);
        if (ffeil_cofnod->cofrestru_data[4]) 주소출력(ffeil_cofnod->cofrestru_data[4], ffeil_cofnod->cofrestru_data[5], 수용량, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return mesur;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t 수용량;
        mesur = 주소출력검사(SECOND_VALUE, cod_nod, &수용량); if (mesur) return mesur;
        주소출력(SECOND_VALUE,cod_nod,수용량,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in ADDRESS;
        mesur=주소입력(SECOND_VALUE,cod_nod,&ADDRESS);if(mesur)return mesur;
        return 자바흐름연결(첫째값,pk_htonl(ADDRESS.sin_addr.s_addr),pk_htons(ADDRESS.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,SECOND_VALUE):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(SECOND_VALUE||cod_nod)return -95;mesur=자바흐름연결받기(첫째값);if(mesur>=40&&mesur<56)통신끝점들[mesur-32]=1;return mesur;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(defnyddiwr_ffrâm *ffeil_cofnod) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(ffeil_cofnod) : 자체체계호출(ffeil_cofnod);
}
static void return_cnewyllyn(defnyddiwr_ffrâm *ffeil_cofnod, int mesur) {
    Stop_TIMEOUT();
    ffeil_cofnod->cofrestru_data[0] = (uint64_t)(int64_t)mesur;
    ffeil_cofnod->gorchymyn_safle = (uintptr_t)defnyddiwr_return;
    ffeil_cofnod->cyflwr_cod = 0x3c5; // EL1h, DAIF masked
}
int defnyddiwr_eithriad(defnyddiwr_ffrâm *ffeil_cofnod, unsigned INTERCEPT) {
    if (!Ar_gael || (ffeil_cofnod->cyflwr_cod & 15) != 0) return 0;
    if (INTERCEPT) {
        uint32_t 승인값 = peiriant_cofrestru(IRQ_CPU_rhyngwyneb + 0xc), dynodwr_VALUE = 승인값 & 1023;
        if (dynodwr_VALUE == 30) { return_cnewyllyn(ffeil_cofnod, defnyddiwr_TIMEOUT); peiriant_cofrestru(IRQ_CPU_rhyngwyneb + 0x10) = 승인값; return 1; }
        if (dynodwr_VALUE < 1020) peiriant_cofrestru(IRQ_CPU_rhyngwyneb + 0x10) = 승인값;
        return 1;
    }
    uint64_t eithriad_cyflwr; __asm__ volatile("mrs %0, esr_el1" : "=r"(eithriad_cyflwr));
    if (Cloc_VALUE() >= 마감시각) { return_cnewyllyn(ffeil_cofnod, defnyddiwr_TIMEOUT); return 1; }
    unsigned eithriad_ardal = eithriad_cyflwr >> 26;
    if (eithriad_ardal == 0x15 && (eithriad_cyflwr & 0xffff) == 0) {
        if (리눅스규약 ? ffeil_cofnod->cofrestru_data[8] == 93 || ffeil_cofnod->cofrestru_data[8] == 94 : ffeil_cofnod->cofrestru_data[8] == 6) return_cnewyllyn(ffeil_cofnod, (int)(ffeil_cofnod->cofrestru_data[0] & 255));
        else {
            intptr_t mesur=체계호출(ffeil_cofnod);
            if(mesur==-4096&&rhyngweithiol){
                저장값[perchennog_gwrthrych].실행틀=*ffeil_cofnod;저장값[perchennog_gwrthrych].실행틀.gorchymyn_safle-=4;
                사용자실수보관(저장값[perchennog_gwrthrych].실수저장상태);return_cnewyllyn(ffeil_cofnod,사용자중단됨);
            }else ffeil_cofnod->cofrestru_data[0]=(uint64_t)mesur;
        }
    } else return_cnewyllyn(ffeil_cofnod, eithriad_ardal == 0x24 ? defnyddiwr_data_gwall : eithriad_ardal == 0x20 ? 사용자실행오류 : defnyddiwr_annilys_cyfarwyddyd);
    return 1;
}

// 생성된 const ELF Grŵp_VALUE: 실행은 반드시 Rhaglen_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *data; size_t Maint; unsigned 전달값; } Rhaglen;
#include "programs.h"
static void *ciplun(unsigned safle_INDEX){return (void *)(0x04000000ul+safle_INDEX*(defnyddiwr_gorffen-defnyddiwr_BASE));}
static int Gorffen_Rhaglen(int mesur){
    사용자누적시각[perchennog_gwrthrych]+=(uint32_t)보드밀리초()-사용자실행시각[perchennog_gwrthrych];
    Stop_TIMEOUT();Ar_gael=0;
    if(mesur==사용자중단됨){
        저장된작업 *testun_data=&저장값[perchennog_gwrthrych];testun_data->멈춤상태=1;testun_data->rhyngweithiol=rhyngweithiol;testun_data->리눅스규약=리눅스규약;testun_data->동적기억공간=동적기억끝;testun_data->인수개수=전달인수개수;
        memcpy(testun_data->caniatâd_Rhestr,caniatâd_Rhestr,sizeof(caniatâd_Rhestr));memcpy(testun_data->ffeil_Rhestr,ffeil_Rhestr,sizeof(ffeil_Rhestr));memcpy(testun_data->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(testun_data->arg_ARAE,전달인수,sizeof(전달인수));memcpy(testun_data->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<defnyddiwr_tudalen_COUNT;순번++)if(caniatâd_Rhestr[순번])memcpy((unsigned char *)ciplun(perchennog_gwrthrych)+순번*maint_tudalen,(void *)(defnyddiwr_BASE+순번*maint_tudalen),maint_tudalen);
    }else{
        저장값[perchennog_gwrthrych].멈춤상태=0;화면초기화(perchennog_gwrthrych);
        for(unsigned 순번=0;순번<16;순번++)if(ffeil_Rhestr[순번]>=0)pk_close(ffeil_Rhestr[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<defnyddiwr_tudalen_COUNT;순번++){tudalen_Rhestr[순번]=0;caniatâd_Rhestr[순번]=0;}변환표맞추기();return mesur;
}
uintptr_t bwrdd_rheolaeth_defnyddiwr(uintptr_t Gweithrediad){
    unsigned safle_INDEX=Gweithrediad&15;if(safle_INDEX>=4||Ar_gael)return (uint32_t)-22;
    저장된작업 *testun_data=&저장값[safle_INDEX];
    if(Gweithrediad>=32){if(testun_data->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(testun_data->ffeil_Rhestr[순번]>=0)pk_close(testun_data->ffeil_Rhestr[순번]);for(unsigned 순번=0;순번<24;순번++)if(testun_data->통신끝점들[순번])통신끝점닫기(순번+32);}testun_data->멈춤상태=0;화면초기화(safle_INDEX);return 0;}
    if(Gweithrediad>=16)return testun_data->멈춤상태;
    if(!testun_data->멈춤상태)return (uint32_t)-22;
    perchennog_gwrthrych=safle_INDEX;rhyngweithiol=testun_data->rhyngweithiol;리눅스규약=testun_data->리눅스규약;동적기억끝=testun_data->동적기억공간;전달인수개수=testun_data->인수개수;
    memcpy(ffeil_Rhestr,testun_data->ffeil_Rhestr,sizeof(ffeil_Rhestr));memcpy(통신끝점들,testun_data->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,testun_data->arg_ARAE,sizeof(전달인수));memcpy(전달인수길이,testun_data->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<defnyddiwr_tudalen_COUNT;순번++)tudalen_Rhestr[순번]=(defnyddiwr_BASE+순번*maint_tudalen)|cnewyllyn_tudalen;변환표맞추기();
    memset((void *)defnyddiwr_BASE,0,defnyddiwr_gorffen-defnyddiwr_BASE);
    for(unsigned 순번=0;순번<defnyddiwr_tudalen_COUNT;순번++)if(testun_data->caniatâd_Rhestr[순번])memcpy((void *)(defnyddiwr_BASE+순번*maint_tudalen),(unsigned char *)ciplun(safle_INDEX)+순번*maint_tudalen,maint_tudalen);
    memcpy(caniatâd_Rhestr,testun_data->caniatâd_Rhestr,sizeof(caniatâd_Rhestr));
    for(unsigned 순번=0;순번<defnyddiwr_tudalen_COUNT;순번++){unsigned data_safle=caniatâd_Rhestr[순번];tudalen_Rhestr[순번]=data_safle?(defnyddiwr_BASE+순번*maint_tudalen)|(data_safle==3?defnyddiwr_darllen_ysgrifennu:data_safle==5?사용자읽고실행:defnyddiwr_darllen_yn_unig):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");Ar_gael=1;testun_data->멈춤상태=0;START_TIMEOUT();
    사용자실행시각[perchennog_gwrthrych]=보드밀리초();
    return (uint32_t)Gorffen_Rhaglen(defnyddiwr_CV(&testun_data->실행틀,testun_data->실수저장상태));
}
static int rhedeg_Rhaglen(const unsigned char *data, size_t Maint, unsigned 전달값, int 리눅스방식, const char *Enw) {
    if (Ar_gael) return -16;
    perchennog_gwrthrych=bwrdd_Terfynell(11);if(perchennog_gwrthrych<0||perchennog_gwrthrych>3||저장값[perchennog_gwrthrych].멈춤상태)return -16;rhyngweithiol=0;
    int 유효함 = 실행파일검사(data, Maint, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned enw_INDEX=0;
    while (*Enw && enw_INDEX<31) defnyddiwr_gorchymyn_enw[perchennog_gwrthrych][enw_INDEX++]=(unsigned char)*Enw++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (enw_INDEX) defnyddiwr_gorchymyn_enw[perchennog_gwrthrych][enw_INDEX++]=' ';
        for (unsigned safle_INDEX=0; safle_INDEX<전달인수길이[0]; safle_INDEX++) defnyddiwr_gorchymyn_enw[perchennog_gwrthrych][enw_INDEX++]=전달인수[0][safle_INDEX];
    }
    defnyddiwr_gorchymyn_enw[perchennog_gwrthrych][enw_INDEX]=0; rhif_defnyddiwr[perchennog_gwrthrych]=Nesaf_rhif_defnyddiwr++;
    if (Nesaf_rhif_defnyddiwr>0x7fffffffu) Nesaf_rhif_defnyddiwr=10;
    defnyddiwr_START_TIME[perchennog_gwrthrych]=보드밀리초(); 사용자누적시각[perchennog_gwrthrych]=0;
    for (unsigned 순번 = 0; 순번 < defnyddiwr_tudalen_COUNT; 순번++) tudalen_Rhestr[순번] = (defnyddiwr_BASE + 순번 * maint_tudalen) | cnewyllyn_tudalen;
    변환표맞추기();
    memset((void *)defnyddiwr_BASE, 0, defnyddiwr_gorffen - defnyddiwr_BASE);
    memset(caniatâd_Rhestr, 0, sizeof(caniatâd_Rhestr));
    실행파일머리 실행머리; memcpy(&실행머리, data, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.Rhaglen_Pennyn_COUNT; 순번++) {
        실행파일구획 data_safle; memcpy(&data_safle, data + 실행머리.Rhaglen_Pennyn_OFFSET + 순번 * sizeof(data_safle), sizeof(data_safle));
        if (data_safle.TYPE_ardal != 1 || !data_safle.기억영역크기) continue;
        if (data_safle.파일영역크기) memcpy((void *)(uintptr_t)data_safle.ADDRESS, data + data_safle.OFFSET_VALUE, data_safle.파일영역크기);
        for (uintptr_t 현재위치 = data_safle.ADDRESS & ~(maint_tudalen - 1); 현재위치 < data_safle.ADDRESS + data_safle.기억영역크기; 현재위치 += maint_tudalen) {
            caniatâd_Rhestr[(현재위치 - defnyddiwr_BASE) / maint_tudalen] = (data_safle.설정비트 & 2) ? 3 : ((data_safle.설정비트 & 1) ? 5 : 1);
        }
    }
    for (uintptr_t 현재위치 = defnyddiwr_pentwr_ADDRESS; 현재위치 < defnyddiwr_gorffen; 현재위치 += maint_tudalen) caniatâd_Rhestr[(현재위치 - defnyddiwr_BASE) / maint_tudalen] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.cofnod_p) : defnyddiwr_gorffen;
    for (unsigned 순번 = 0; 순번 < defnyddiwr_tudalen_COUNT; 순번++) {
        unsigned caniatâd = caniatâd_Rhestr[순번];
        tudalen_Rhestr[순번] = caniatâd ? (defnyddiwr_BASE + 순번 * maint_tudalen) | (caniatâd == 3 ? defnyddiwr_darllen_ysgrifennu : caniatâd == 5 ? 사용자읽고실행 : defnyddiwr_darllen_yn_unig) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) ffeil_Rhestr[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = defnyddiwr_llun_gorffen;
    Ar_gael = 1; START_TIMEOUT();
    사용자실행시각[perchennog_gwrthrych]=보드밀리초();
    int mesur = defnyddiwr_cofnodi(실행머리.cofnod_p, 초기쌓임공간, 전달값);
    return Gorffen_Rhaglen(mesur);
}
uintptr_t bwrdd_defnyddiwr_rhedeg(uintptr_t LOOKUP_INDEX) {
    if (LOOKUP_INDEX >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Enw=LOOKUP_INDEX==10?"javac":LOOKUP_INDEX==11?"java":LOOKUP_INDEX==12?"python":LOOKUP_INDEX==13?"vi":LOOKUP_INDEX==14?"jar":LOOKUP_INDEX==15?"cc":LOOKUP_INDEX==16?"jaot":"ELF";
    return (uint32_t)rhedeg_Rhaglen(실행항목들[LOOKUP_INDEX].data, 실행항목들[LOOKUP_INDEX].Maint, 실행항목들[LOOKUP_INDEX].전달값, 0, Enw);
}
static uintptr_t Gweithredu_ffeil(int 리눅스방식) {
    static unsigned char llun[16384];
    if (Ar_gael || !전달인수개수) return (uint32_t)-22;
    int ffeil_dolen = pk_open((const char *)전달인수[0], darllen_yn_unig_VALUE, 0);
    if (ffeil_dolen < 0) return (uint32_t)-오류번호;
    int Maint = pk_size(ffeil_dolen);
    if (Maint < 0 || (unsigned)Maint > sizeof(llun)) { pk_close(ffeil_dolen); return (uint32_t)-27; }
    int RECEIVED_COUNT = pk_read(ffeil_dolen, llun, Maint); pk_close(ffeil_dolen);
    if (RECEIVED_COUNT != Maint) return (uint32_t)-5;
    return (uint32_t)rhedeg_Rhaglen(llun, Maint, 0, 리눅스방식, "");
}
uintptr_t bwrdd_defnyddiwr_ffeil(void) { return Gweithredu_ffeil(0); }
uintptr_t 보드사용자리눅스파일(void) { return Gweithredu_ffeil(1); }
uintptr_t bwrdd_defnyddiwr_dilysu(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].data, 잘못된실행항목들[순번].Maint) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
