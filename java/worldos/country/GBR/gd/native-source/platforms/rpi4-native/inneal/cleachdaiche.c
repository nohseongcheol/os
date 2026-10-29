#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 gnìomhaich_àithne inneal breath_VALUE. faidhle dàta/정책은 기존 AOT Java 커널에 위임한다.
#include "cleachdaiche.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../lìonra_stac/lìonra_stac.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define inneal_clàraich(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define interrupt_sgaoileadair 0xff841000ul
#define interrupt_CPU_eadar_aghaidh 0xff842000ul
#define meud_na_duilleige 4096ul
#define 접근표시 (1ul << 10)
#define chan_eil_gnìomhaich_cead (1ul << 53)
#define cleachdaiche_chan_eil_gnìomhaich (1ul << 54)
#define àbhaisteach_cuimhne ((1ul << 2) | (3ul << 8) | 접근표시)
#define eitean_duilleag (3ul | àbhaisteach_cuimhne | chan_eil_gnìomhaich_cead | cleachdaiche_chan_eil_gnìomhaich)
#define cleachdaiche_so_leughte_so_sgrìobhte (3ul | àbhaisteach_cuimhne | (1ul << 6) | chan_eil_gnìomhaich_cead | cleachdaiche_chan_eil_gnìomhaich)
#define cleachdaiche_ri_leughadh_a_mhàin (3ul | àbhaisteach_cuimhne | (3ul << 6) | chan_eil_gnìomhaich_cead | cleachdaiche_chan_eil_gnìomhaich)
#define 사용자읽고실행 (3ul | àbhaisteach_cuimhne | (3ul << 6) | chan_eil_gnìomhaich_cead)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t bòrd_pel(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t bòrd_tèirmineal(uintptr_t);
extern int tèirmineal_ri_dhèiligeadh(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int cleachdaiche_cunntas_beatha_goirid(cleachdaiche_frèam *,void *);
extern void 사용자실수보관(void *);
extern int cleachdaiche_cuir_a_steach(uintptr_t cur_a_steach_puing, uintptr_t stac_stòras, uintptr_t 전달값);
extern void cleachdaiche_return(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t freumh_ADDRESS[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t duilleag_Liosta[cleachdaiche_duilleag_COUNT] __attribute__((aligned(4096)));
static uint8_t ceadan_Liosta[cleachdaiche_duilleag_COUNT];
static int gnìomhach, faidhle_Liosta[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned faidhle_làmhrachan){return faidhle_làmhrachan<40?자바전문닫기(faidhle_làmhrachan):자바흐름닫기(faidhle_làmhrachan);}
static uint64_t FREQUENCY, 마감시각;
static uintptr_t 동적기억끝;
// eitean_VALUE 셸이 준비한 UTF-8 인수. EL0에는 ionstans_VALUE 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,eadar_ghnìomhach,리눅스규약,faidhle_Liosta[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char argamaid_ARRAY[8][256],ceadan_Liosta[cleachdaiche_duilleag_COUNT];
    uintptr_t 동적기억공간; cleachdaiche_frèam 실행틀;
    unsigned char 실수저장상태[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int sealbhadair_nì,eadar_ghnìomhach;
static uint32_t àireamh_cleachdaiche[4], cleachdaiche_Start_TIME[4], 사용자누적시각[4], 사용자실행시각[4], air_adhart_àireamh_cleachdaiche=10;
static unsigned char cleachdaiche_àithne_ainm[4][288];
uint32_t 사용자상태읽기(unsigned cur_a_steach_VALUE, unsigned INDEX) {
    unsigned suidhich_INDEX=INDEX&3;
    int cor_VALUE=(gnìomhach && sealbhadair_nì==(int)suidhich_INDEX) ? 1 : 저장값[suidhich_INDEX].멈춤상태 ? 2 : 0;
    if (cur_a_steach_VALUE==0) return cor_VALUE;
    if (!cor_VALUE) return 0;
    if (cur_a_steach_VALUE==1) return àireamh_cleachdaiche[suidhich_INDEX];
    if (cur_a_steach_VALUE==2) {
        unsigned char *쪽들=cor_VALUE==1?ceadan_Liosta:저장값[suidhich_INDEX].ceadan_Liosta;
        unsigned duilleag_COUNT=0; for (unsigned 순번=0; 순번<cleachdaiche_duilleag_COUNT; 순번++) if(쪽들[순번]) duilleag_COUNT++;
        return duilleag_COUNT*4;
    }
    if (cur_a_steach_VALUE==3) return (uint32_t)보드밀리초()-cleachdaiche_Start_TIME[suidhich_INDEX];
    if (cur_a_steach_VALUE==4) return 사용자누적시각[suidhich_INDEX]+(cor_VALUE==1?(uint32_t)보드밀리초()-사용자실행시각[suidhich_INDEX]:0);
    if (cur_a_steach_VALUE==5) return INDEX/4<sizeof(cleachdaiche_àithne_ainm[0])?cleachdaiche_àithne_ainm[suidhich_INDEX][INDEX/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t cur_a_steach_COUNT) {
    if (gnìomhach || cur_a_steach_COUNT > 8) return (uint32_t)-22;
    전달인수개수 = cur_a_steach_COUNT;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t LOOKUP_INDEX, uintptr_t 현재위치, uintptr_t baidht_dàta) {
    if (gnìomhach || LOOKUP_INDEX >= 전달인수개수 || 현재위치 >= 255 || 현재위치 != 전달인수길이[LOOKUP_INDEX] || !baidht_dàta || baidht_dàta > 255)
        return (uint32_t)-22;
    전달인수[LOOKUP_INDEX][현재위치] = baidht_dàta;
    전달인수길이[LOOKUP_INDEX] = 현재위치 + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t cleoc_VALUE(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Stad_TIMEOUT(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    inneal_clàraich(interrupt_sgaoileadair + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void Start_TIMEOUT(void) {
    uint64_t 간격 = FREQUENCY * 2, cuir_an_comas = 1;
    마감시각 = cleoc_VALUE() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(cuir_an_comas) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned dàta_bac = 0; dàta_bac < 4; dàta_bac++) {
        freumh_ADDRESS[dàta_bac] = (uintptr_t)가운데[dàta_bac] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t ADDRESS = ((uintptr_t)dàta_bac << 30) | ((uintptr_t)순번 << 21);
            가운데[dàta_bac][순번] = ADDRESS | 1 | 접근표시 | cleachdaiche_chan_eil_gnìomhaich;
            if (ADDRESS >= 0xfc000000ul) 가운데[dàta_bac][순번] |= chan_eil_gnìomhaich_cead; // Device-nGnRnE
            else 가운데[dàta_bac][순번] |= àbhaisteach_cuimhne; // Normal, non-cacheable
        }
    }
    for (unsigned SECOND_VALUE = 0; SECOND_VALUE < cleachdaiche_duilleag_COUNT / 512; SECOND_VALUE++)
        가운데[0][(cleachdaiche_BASE >> 21) + SECOND_VALUE] = (uintptr_t)(duilleag_Liosta + SECOND_VALUE * 512) | 3;
    for (unsigned 순번 = 0; 순번 < cleachdaiche_duilleag_COUNT; 순번++) duilleag_Liosta[순번] = (cleachdaiche_BASE + 순번 * meud_na_duilleige) | eitean_duilleag;
    uint64_t cuimhne_buadh_clàraich = 0x4400, ADDRESS_eadar_theangachadh_smachd = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(cuimhne_buadh_clàraich), "r"(ADDRESS_eadar_theangachadh_smachd), "r"((uintptr_t)freumh_ADDRESS) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t 실수저장상태 = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(실수저장상태) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    Stad_TIMEOUT();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 cur_a_steach_puing_VALUE 때만 Ceadaich_VALUE.
    inneal_clàraich(interrupt_sgaoileadair) = 0;
    inneal_clàraich(interrupt_sgaoileadair + 0x180) = 0xffffffff;
    inneal_clàraich(interrupt_sgaoileadair + 0x80) = 0xffffffff;
    inneal_clàraich(interrupt_sgaoileadair + 0x280) = 1u << 30;
    inneal_clàraich(interrupt_sgaoileadair + 0x41c) = 0x80808080;
    inneal_clàraich(interrupt_sgaoileadair + 0x100) = 1u << 30;
    inneal_clàraich(interrupt_CPU_eadar_aghaidh + 4) = 0xff;
    inneal_clàraich(interrupt_CPU_eadar_aghaidh + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 수 있다.
    int tèarainteachd = (inneal_clàraich(interrupt_sgaoileadair + 4) & (1u << 10)) != 0;
    inneal_clàraich(interrupt_sgaoileadair) = tèarainteachd ? 1 : 3;
    inneal_clàraich(interrupt_CPU_eadar_aghaidh) = tèarainteachd ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t TYPE_roinn_seòrsa, inneal_TYPE; uint32_t 판번호;
    uint64_t cur_a_steach_puing, ap_bann_cinn_OFFSET, earrann_bann_cinn_OFFSET; uint32_t 설정비트;
    uint16_t 실행머리크기, ap_bann_cinn_cur_a_steach_atharraich_am_meud, ap_bann_cinn_COUNT, earrann_bann_cinn_cur_a_steach_atharraich_am_meud, earrann_bann_cinn_COUNT, earrann_ainm_clàr_INDEX;
} 실행파일머리;
typedef struct { uint32_t TYPE_roinn_seòrsa, 설정비트; uint64_t OFFSET_VALUE, ADDRESS, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(cleachdaiche_frèam) == 272, "exception assembly layout");
static int 포함된범위(uint64_t OFFSET_VALUE, uint64_t atharraich_am_meud, uint64_t crìochnaich_OFFSET) {
    return OFFSET_VALUE <= crìochnaich_OFFSET && atharraich_am_meud <= crìochnaich_OFFSET - OFFSET_VALUE;
}
static int 부가정보검사(const unsigned char *dàta_suidhich, size_t atharraich_am_meud) {
    size_t 현재위치 = 0;
    while (포함된범위(현재위치, 12, atharraich_am_meud)) {
        uint32_t 낱말들[3]; memcpy(낱말들, dàta_suidhich + 현재위치, 12); 현재위치 += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(현재위치, 이름영역크기, atharraich_am_meud) || !포함된범위(현재위치 + 이름영역크기, 설명크기, atharraich_am_meud)) return 0;
        const unsigned char Ainm[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Ainm) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Ainm); 순번++) if (dàta_suidhich[현재위치 + 순번] != Ainm[순번]) 일치 = 0;
        uint32_t 판번호 = 0;
        if (일치) memcpy(&판번호, dàta_suidhich + 현재위치 + 이름영역크기, 4);
        if (일치 && 판번호 == 1) return 1;
        현재위치 += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *dàta, size_t atharraich_am_meud, int 리눅스방식) {
    if (atharraich_am_meud < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, dàta, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.TYPE_roinn_seòrsa != 2 || 실행머리.inneal_TYPE != 183 || 실행머리.판번호 != 1 || 실행머리.설정비트 || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.ap_bann_cinn_cur_a_steach_atharraich_am_meud != sizeof(실행파일구획) || !실행머리.ap_bann_cinn_COUNT || 실행머리.ap_bann_cinn_COUNT > 16 ||
        실행머리.ap_bann_cinn_OFFSET < sizeof(실행머리) || !포함된범위(실행머리.ap_bann_cinn_OFFSET, (uint64_t)실행머리.ap_bann_cinn_COUNT * sizeof(실행파일구획), atharraich_am_meud)) return 사용자실행파일오류;
    uint8_t 사용량[(cleachdaiche_IMAGE_crìochnaich - cleachdaiche_BASE) / meud_na_duilleige] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.ap_bann_cinn_COUNT; 순번++) {
        실행파일구획 dàta_suidhich; memcpy(&dàta_suidhich, dàta + 실행머리.ap_bann_cinn_OFFSET + 순번 * sizeof(dàta_suidhich), sizeof(dàta_suidhich));
        if (dàta_suidhich.TYPE_roinn_seòrsa == 4) {
            if (!포함된범위(dàta_suidhich.OFFSET_VALUE, dàta_suidhich.파일영역크기, atharraich_am_meud)) return 사용자실행파일오류;
            if (부가정보검사(dàta + dàta_suidhich.OFFSET_VALUE, dàta_suidhich.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (dàta_suidhich.TYPE_roinn_seòrsa == 0 || dàta_suidhich.TYPE_roinn_seòrsa == 6 || (dàta_suidhich.TYPE_roinn_seòrsa == 0x6474e551 && !(dàta_suidhich.설정비트 & 1))) continue;
        if (dàta_suidhich.TYPE_roinn_seòrsa != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!dàta_suidhich.기억영역크기) continue;
        if (dàta_suidhich.설정비트 & ~7u || !(dàta_suidhich.설정비트 & 4) || (dàta_suidhich.설정비트 & 3) == 3 || dàta_suidhich.파일영역크기 > dàta_suidhich.기억영역크기 ||
            (dàta_suidhich.파일영역크기 && !포함된범위(dàta_suidhich.OFFSET_VALUE, dàta_suidhich.파일영역크기, atharraich_am_meud)) || dàta_suidhich.ADDRESS < cleachdaiche_BASE ||
            !포함된범위(dàta_suidhich.ADDRESS, dàta_suidhich.기억영역크기, cleachdaiche_IMAGE_crìochnaich) ||
            (!리눅스방식 && ((dàta_suidhich.ADDRESS & (meud_na_duilleige - 1)) || (dàta_suidhich.OFFSET_VALUE & (meud_na_duilleige - 1)) || dàta_suidhich.맞춤 != meud_na_duilleige)) ||
            (리눅스방식 && (((dàta_suidhich.ADDRESS ^ dàta_suidhich.OFFSET_VALUE) & (meud_na_duilleige - 1)) || !dàta_suidhich.맞춤 ||
                (dàta_suidhich.맞춤 & (dàta_suidhich.맞춤 - 1)) || dàta_suidhich.맞춤 > 0x200000 || ((dàta_suidhich.ADDRESS ^ dàta_suidhich.OFFSET_VALUE) & (dàta_suidhich.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (dàta_suidhich.ADDRESS - cleachdaiche_BASE) / meud_na_duilleige;
        unsigned cur_a_steach_COUNT = ((dàta_suidhich.ADDRESS & (meud_na_duilleige - 1)) + dàta_suidhich.기억영역크기 + meud_na_duilleige - 1) / meud_na_duilleige;
        for (unsigned duilleag_VALUE = 첫항목; duilleag_VALUE < 첫항목 + cur_a_steach_COUNT; duilleag_VALUE++) {
            if (사용량[duilleag_VALUE]) return 사용자실행파일오류;
            사용량[duilleag_VALUE] = 1;
        }
        if ((dàta_suidhich.설정비트 & 1) && 실행머리.cur_a_steach_puing >= dàta_suidhich.ADDRESS && 실행머리.cur_a_steach_puing < dàta_suidhich.ADDRESS + dàta_suidhich.파일영역크기 && !(실행머리.cur_a_steach_puing & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *dàta, size_t atharraich_am_meud) { return 실행파일검사(dàta, atharraich_am_meud, 0); }
static void co_dhealbhachd_na_duilleige(uintptr_t ADDRESS, uint64_t 설정비트, unsigned ceadan) {
    unsigned LOOKUP_INDEX = (ADDRESS - cleachdaiche_BASE) / meud_na_duilleige;
    duilleag_Liosta[LOOKUP_INDEX] = ADDRESS | 설정비트;
    ceadan_Liosta[LOOKUP_INDEX] = ceadan;
}
static int 사용자범위(uintptr_t ADDRESS, size_t cur_a_steach_COUNT, int 쓰는중) {
    if (ADDRESS < cleachdaiche_BASE || !포함된범위(ADDRESS, cur_a_steach_COUNT, cleachdaiche_crìochnaich)) return 0;
    if (!cur_a_steach_COUNT) return 1;
    unsigned 첫항목 = (ADDRESS - cleachdaiche_BASE) / meud_na_duilleige, 마지막 = (ADDRESS + cur_a_steach_COUNT - 1 - cleachdaiche_BASE) / meud_na_duilleige;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(ceadan_Liosta[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int ionstans_slighe(uintptr_t ADDRESS, char *Slighe) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!사용자범위(ADDRESS, 1, 0)) return -14;
        Slighe[순번] = *(const char *)ADDRESS++;
        if (!Slighe[순번]) return 0;
    }
    return -36;
}
static intptr_t eitean_tomhas(intptr_t tomhas) { return tomhas < 0 ? -오류번호 : tomhas; }
static int 대응파일기술자(uint64_t faidhle_làmhrachan) { return faidhle_làmhrachan >= 3 && faidhle_làmhrachan < 19 ? faidhle_Liosta[faidhle_làmhrachan - 3] : -1; }
static int 통신끝점소유(uint64_t faidhle_làmhrachan) { return faidhle_làmhrachan >= 32 && faidhle_làmhrachan < 56 && 통신끝점들[faidhle_làmhrachan - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t faid_VALUE, struct pk_sockaddr_in *ADDRESS) {
    if (faid_VALUE != sizeof(*ADDRESS)) return -22;
    if (!사용자범위(가리킴값, faid_VALUE, 0)) return -14;
    memcpy(ADDRESS, (const void *)가리킴값, sizeof(*ADDRESS));
    return ADDRESS->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t faid_tomhaire, pk_socklen_t *수용량) {
    if (!사용자범위(faid_tomhaire, sizeof(*수용량), 1)) return -14;
    memcpy(수용량, (const void *)faid_tomhaire, sizeof(*수용량));
    if (*수용량 > sizeof(struct pk_sockaddr_in)) *수용량 = sizeof(struct pk_sockaddr_in);
    if (*수용량 && !사용자범위(가리킴값, *수용량, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t faid_tomhaire, pk_socklen_t 수용량, int ADDRESS, int 접속번호) {
    struct pk_sockaddr_in VALUE; memset(&VALUE, 0, sizeof(VALUE));
    VALUE.sin_family = AF_INET; VALUE.sin_port = pk_htons(접속번호); VALUE.sin_addr.s_addr = pk_htonl(ADDRESS);
    if (수용량) memcpy((void *)가리킴값, &VALUE, 수용량);
    pk_socklen_t faid_VALUE = sizeof(VALUE); memcpy((void *)faid_tomhaire, &faid_VALUE, sizeof(faid_VALUE));
}
extern uintptr_t bòrd_seanail(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(cleachdaiche_frèam *faidhle_cur_a_steach) {
    uintptr_t 첫째값 = faidhle_cur_a_steach->clàraich_dàta[0], SECOND_VALUE = faidhle_cur_a_steach->clàraich_dàta[1], còd_a_charactair = faidhle_cur_a_steach->clàraich_dàta[2];
    char Slighe[65];
    int faidhle_làmhrachan, tomhas;
    switch (faidhle_cur_a_steach->clàraich_dàta[8]) {
    case 0: return 1; // 자체 ABI 버전
    case 1: // write: tomhaire 전체를 검사한 Air_ais_VALUE 출력/faidhle atharraich_VALUE
        if (còd_a_charactair > 65536) return -22;
        if (!사용자범위(SECOND_VALUE, còd_a_charactair, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=cleoc_VALUE();
            for (size_t 순번 = 0; 순번 < còd_a_charactair; 순번++) bòrd_seanail(첫째값, ((const unsigned char *)SECOND_VALUE)[순번]);
            /* 큰 tty를 그린 eitean_VALUE 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(eadar_ghnìomhach){
                마감시각+=cleoc_VALUE()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(마감시각) : "memory");
            }
            return còd_a_charactair;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t nì_COUNT=còd_a_charactair>512?512:còd_a_charactair;for(size_t 순번=0;순번<nì_COUNT;순번++)자바전문넣기(순번,((const unsigned char *)SECOND_VALUE)[순번]);return 자바흐름쓰기(첫째값,nì_COUNT);
        }
        faidhle_làmhrachan = 대응파일기술자(첫째값); if (faidhle_làmhrachan < 0) return -9;
        return eitean_tomhas(pk_write(faidhle_làmhrachan, (const void *)SECOND_VALUE, còd_a_charactair));
    case 2:
        if (còd_a_charactair > 65536) return -22;
        if (!사용자범위(SECOND_VALUE, còd_a_charactair, 1)) return -14;
        if (첫째값 == 0) {
            size_t nì_COUNT = 0;
            while (nì_COUNT < còd_a_charactair) {
                int caractar_VALUE = (int32_t)보드글자읽기(); if (caractar_VALUE == -2) return nì_COUNT; if (caractar_VALUE < 0) break;
                ((unsigned char *)SECOND_VALUE)[nì_COUNT++] = caractar_VALUE;
            }
            return nì_COUNT ? (intptr_t)nì_COUNT : (còd_a_charactair ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            tomhas=자바흐름읽기(첫째값,còd_a_charactair>512?512:còd_a_charactair);if(tomhas>0)for(int 순번=0;순번<tomhas;순번++)((unsigned char *)SECOND_VALUE)[순번]=자바전문얻기(순번);return tomhas;
        }
        faidhle_làmhrachan = 대응파일기술자(첫째값); if (faidhle_làmhrachan < 0) return -9;
        return eitean_tomhas(pk_read(faidhle_làmhrachan, (void *)SECOND_VALUE, còd_a_charactair));
    case 3:
        tomhas = ionstans_slighe(첫째값, Slighe); if (tomhas) return tomhas;
        if (SECOND_VALUE > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (faidhle_Liosta[순번] < 0) {
            faidhle_làmhrachan = pk_open(Slighe, (int)SECOND_VALUE, 0600);
            if (faidhle_làmhrachan < 0) return -오류번호;
            faidhle_Liosta[순번] = faidhle_làmhrachan; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { tomhas = 통신끝점닫기(첫째값); if (!tomhas) 통신끝점들[첫째값 - 32] = 0; return tomhas; }
        faidhle_làmhrachan = 대응파일기술자(첫째값); if (faidhle_làmhrachan < 0) return -9;
        tomhas = pk_close(faidhle_làmhrachan); if (!tomhas) faidhle_Liosta[첫째값 - 3] = -1;
        return eitean_tomhas(tomhas);
    case 5:
        faidhle_làmhrachan = 대응파일기술자(첫째값); if (faidhle_làmhrachan < 0) return -9;
        if (còd_a_charactair > 2) return -22;
        return eitean_tomhas(pk_lseek(faidhle_làmhrachan, (int64_t)SECOND_VALUE, còd_a_charactair));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 cleachdaiche RW/NX 힙, 새로 노출되는 페이지는 0으로 ro_shuidhich
        if (!첫째값) return 동적기억끝;
        if (첫째값 < cleachdaiche_IMAGE_crìochnaich || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + meud_na_duilleige - 1) & ~(meud_na_duilleige - 1);
        uintptr_t 새쪽들 = (첫째값 + meud_na_duilleige - 1) & ~(meud_na_duilleige - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t dàta_suidhich = 이전쪽들; dàta_suidhich < 새쪽들; dàta_suidhich += meud_na_duilleige) co_dhealbhachd_na_duilleige(dàta_suidhich, eitean_duilleag, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t dàta_suidhich = 이전쪽들; dàta_suidhich < 새쪽들; dàta_suidhich += meud_na_duilleige) co_dhealbhachd_na_duilleige(dàta_suidhich, cleachdaiche_so_leughte_so_sgrìobhte, 3);
        } else {
            for (uintptr_t dàta_suidhich = 새쪽들; dàta_suidhich < 이전쪽들; dàta_suidhich += meud_na_duilleige) {
                duilleag_Liosta[(dàta_suidhich - cleachdaiche_BASE) / meud_na_duilleige] = 0; ceadan_Liosta[(dàta_suidhich - cleachdaiche_BASE) / meud_na_duilleige] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        faidhle_làmhrachan = 대응파일기술자(첫째값); return faidhle_làmhrachan < 0 ? -9 : eitean_tomhas(pk_size(faidhle_làmhrachan));
    case 10:
        faidhle_làmhrachan = 대응파일기술자(첫째값); return faidhle_làmhrachan < 0 ? -9 : eitean_tomhas(pk_ftruncate(faidhle_làmhrachan, (int64_t)SECOND_VALUE));
    case 11:
        tomhas = ionstans_slighe(첫째값, Slighe); return tomhas ? tomhas : eitean_tomhas(pk_unlink(Slighe));
    case 12:
        faidhle_làmhrachan = 대응파일기술자(첫째값); return faidhle_làmhrachan < 0 ? -9 : eitean_tomhas(pk_fsync(faidhle_làmhrachan));
    case 13: { // 그래픽 기초 API: cleachdaiche 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = faidhle_cur_a_steach->clàraich_dàta[3], 높이값 = faidhle_cur_a_steach->clàraich_dàta[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SECOND_VALUE > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - SECOND_VALUE) return -22;
        for (uintptr_t 세로좌표 = SECOND_VALUE; 세로좌표 < SECOND_VALUE + 높이값; 세로좌표++) for (uintptr_t co_chomharra_x = 첫째값; co_chomharra_x < 첫째값 + 너비값; co_chomharra_x++) bòrd_pel(co_chomharra_x, 세로좌표, còd_a_charactair);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=nì_COUNT; args(index,buffer,capacity)=UTF-8 faid_VALUE
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (còd_a_charactair <= 전달인수길이[첫째값]) return -36;
        if (!사용자범위(SECOND_VALUE, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SECOND_VALUE, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;eadar_ghnìomhach=1;return bòrd_tèirmineal(13);}
        if(첫째값==2){eadar_ghnìomhach=0;return 0;}
        if(첫째값==3)return bòrd_tèirmineal(13);
        if(첫째값!=1||!eadar_ghnìomhach)return -22;
        tomhas=(int32_t)보드글자읽기();
        if(tomhas==-4096)return tomhas;
        Start_TIMEOUT();return tomhas<0?-11:tomhas;
    case 17: { // 유한한 협력 fuirich_VALUE: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t crìochnaich_TIME = cleoc_VALUE() + FREQUENCY * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (cleoc_VALUE() < crìochnaich_TIME);
        Start_TIMEOUT(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 부모·빈 폴더를 검사한다.
        if (SECOND_VALUE > 2) return -22;
        tomhas = ionstans_slighe(첫째값, Slighe); if (tomhas) return tomhas;
        unsigned faid_VALUE = 0; while (Slighe[faid_VALUE]) faid_VALUE++;
        tomhas = 자바경로시작(faid_VALUE); if (tomhas < 0) return tomhas;
        for (unsigned 순번 = 0; 순번 < faid_VALUE; 순번++) 자바경로바이트(순번, (unsigned char)Slighe[순번]);
        return SECOND_VALUE == 0 ? 자바항목종류() : SECOND_VALUE == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int caractar_VALUE=(int32_t)보드글자읽기();if(caractar_VALUE==-4096)return caractar_VALUE;if(caractar_VALUE>=0)화면누름(sealbhadair_nì,caractar_VALUE);Start_TIMEOUT();}
        if(첫째값==3&&còd_a_charactair){if(!자바셸대화형())return -95;eadar_ghnìomhach=1;bòrd_tèirmineal(300);}
        return 화면호출(sealbhadair_nì,첫째값,SECOND_VALUE,còd_a_charactair,faidhle_cur_a_steach->clàraich_dàta[3],faidhle_cur_a_steach->clàraich_dàta[4],faidhle_cur_a_steach->clàraich_dàta[5]);
    case 21:
        if(còd_a_charactair>127)return -22;if(!사용자범위(SECOND_VALUE,còd_a_charactair*sizeof(uint32_t),0))return -14;
        return 화면글(sealbhadair_nì,첫째값,(const uint32_t *)SECOND_VALUE,còd_a_charactair);
    case 22: // 화면 atharraich_am_meud ceist_VALUE: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SECOND_VALUE==SOCK_STREAM&&(còd_a_charactair==0||còd_a_charactair==6))tomhas=자바흐름만들기();
        else if(SECOND_VALUE==SOCK_DGRAM&&(còd_a_charactair==0||còd_a_charactair==IPPROTO_UDP))tomhas=자바전문만들기(첫째값,SECOND_VALUE,còd_a_charactair);
        else return -93;
        if (tomhas >= 32 && tomhas < 56) 통신끝점들[tomhas - 32] = 1;
        return tomhas;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in ADDRESS;
        tomhas = 주소입력(SECOND_VALUE, còd_a_charactair, &ADDRESS); if (tomhas) return tomhas;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(ADDRESS.sin_addr.s_addr),pk_htons(ADDRESS.sin_port)):자바전문묶기(첫째값, pk_htonl(ADDRESS.sin_addr.s_addr), pk_htons(ADDRESS.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (faidhle_cur_a_steach->clàraich_dàta[3]) return -95;
        if (còd_a_charactair > 512) return -90;
        if (còd_a_charactair && !사용자범위(SECOND_VALUE, còd_a_charactair, 0)) return -14;
        struct pk_sockaddr_in ADDRESS;
        tomhas = 주소입력(faidhle_cur_a_steach->clàraich_dàta[4], faidhle_cur_a_steach->clàraich_dàta[5], &ADDRESS); if (tomhas) return tomhas;
        for (unsigned 순번 = 0; 순번 < còd_a_charactair; 순번++) 자바전문넣기(순번, ((const unsigned char *)SECOND_VALUE)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(ADDRESS.sin_addr.s_addr), pk_htons(ADDRESS.sin_port), còd_a_charactair);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (faidhle_cur_a_steach->clàraich_dàta[3]) return -95;
        if (còd_a_charactair > 512) return -90;
        if (còd_a_charactair && !사용자범위(SECOND_VALUE, còd_a_charactair, 1)) return -14;
        pk_socklen_t 수용량 = 0;
        if (faidhle_cur_a_steach->clàraich_dàta[4]) { tomhas = 주소출력검사(faidhle_cur_a_steach->clàraich_dàta[4], faidhle_cur_a_steach->clàraich_dàta[5], &수용량); if (tomhas) return tomhas; }
        tomhas = 자바전문받기(첫째값, còd_a_charactair); if (tomhas < 0) return tomhas;
        for (int 순번 = 0; 순번 < tomhas; 순번++) ((unsigned char *)SECOND_VALUE)[순번] = 자바전문얻기(순번);
        if (faidhle_cur_a_steach->clàraich_dàta[4]) 주소출력(faidhle_cur_a_steach->clàraich_dàta[4], faidhle_cur_a_steach->clàraich_dàta[5], 수용량, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return tomhas;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t 수용량;
        tomhas = 주소출력검사(SECOND_VALUE, còd_a_charactair, &수용량); if (tomhas) return tomhas;
        주소출력(SECOND_VALUE,còd_a_charactair,수용량,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in ADDRESS;
        tomhas=주소입력(SECOND_VALUE,còd_a_charactair,&ADDRESS);if(tomhas)return tomhas;
        return 자바흐름연결(첫째값,pk_htonl(ADDRESS.sin_addr.s_addr),pk_htons(ADDRESS.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,SECOND_VALUE):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(SECOND_VALUE||còd_a_charactair)return -95;tomhas=자바흐름연결받기(첫째값);if(tomhas>=40&&tomhas<56)통신끝점들[tomhas-32]=1;return tomhas;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(cleachdaiche_frèam *faidhle_cur_a_steach) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(faidhle_cur_a_steach) : 자체체계호출(faidhle_cur_a_steach);
}
static void return_eitean(cleachdaiche_frèam *faidhle_cur_a_steach, int tomhas) {
    Stad_TIMEOUT();
    faidhle_cur_a_steach->clàraich_dàta[0] = (uint64_t)(int64_t)tomhas;
    faidhle_cur_a_steach->àithne_suidhich = (uintptr_t)cleachdaiche_return;
    faidhle_cur_a_steach->cor_CODE = 0x3c5; // EL1h, DAIF masked
}
int 사용자예외(cleachdaiche_frèam *faidhle_cur_a_steach, unsigned INTERCEPT) {
    if (!gnìomhach || (faidhle_cur_a_steach->cor_CODE & 15) != 0) return 0;
    if (INTERCEPT) {
        uint32_t 승인값 = inneal_clàraich(interrupt_CPU_eadar_aghaidh + 0xc), aithnichear_VALUE = 승인값 & 1023;
        if (aithnichear_VALUE == 30) { return_eitean(faidhle_cur_a_steach, cleachdaiche_TIMEOUT); inneal_clàraich(interrupt_CPU_eadar_aghaidh + 0x10) = 승인값; return 1; }
        if (aithnichear_VALUE < 1020) inneal_clàraich(interrupt_CPU_eadar_aghaidh + 0x10) = 승인값;
        return 1;
    }
    uint64_t 예외상태; __asm__ volatile("mrs %0, esr_el1" : "=r"(예외상태));
    if (cleoc_VALUE() >= 마감시각) { return_eitean(faidhle_cur_a_steach, cleachdaiche_TIMEOUT); return 1; }
    unsigned 예외분류 = 예외상태 >> 26;
    if (예외분류 == 0x15 && (예외상태 & 0xffff) == 0) {
        if (리눅스규약 ? faidhle_cur_a_steach->clàraich_dàta[8] == 93 || faidhle_cur_a_steach->clàraich_dàta[8] == 94 : faidhle_cur_a_steach->clàraich_dàta[8] == 6) return_eitean(faidhle_cur_a_steach, (int)(faidhle_cur_a_steach->clàraich_dàta[0] & 255));
        else {
            intptr_t tomhas=체계호출(faidhle_cur_a_steach);
            if(tomhas==-4096&&eadar_ghnìomhach){
                저장값[sealbhadair_nì].실행틀=*faidhle_cur_a_steach;저장값[sealbhadair_nì].실행틀.àithne_suidhich-=4;
                사용자실수보관(저장값[sealbhadair_nì].실수저장상태);return_eitean(faidhle_cur_a_steach,사용자중단됨);
            }else faidhle_cur_a_steach->clàraich_dàta[0]=(uint64_t)tomhas;
        }
    } else return_eitean(faidhle_cur_a_steach, 예외분류 == 0x24 ? cleachdaiche_dàta_mearachd : 예외분류 == 0x20 ? 사용자실행오류 : cleachdaiche_mì_dhligheach_treòrachadh);
    return 1;
}

// 생성된 const ELF buidheann_VALUE: 실행은 반드시 ap_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *dàta; size_t atharraich_am_meud; unsigned 전달값; } ap;
#include "programs.h"
static void *snapshot(unsigned suidhich_INDEX){return (void *)(0x04000000ul+suidhich_INDEX*(cleachdaiche_crìochnaich-cleachdaiche_BASE));}
static int Coilean_ap(int tomhas){
    사용자누적시각[sealbhadair_nì]+=(uint32_t)보드밀리초()-사용자실행시각[sealbhadair_nì];
    Stad_TIMEOUT();gnìomhach=0;
    if(tomhas==사용자중단됨){
        저장된작업 *sreang_dàta=&저장값[sealbhadair_nì];sreang_dàta->멈춤상태=1;sreang_dàta->eadar_ghnìomhach=eadar_ghnìomhach;sreang_dàta->리눅스규약=리눅스규약;sreang_dàta->동적기억공간=동적기억끝;sreang_dàta->인수개수=전달인수개수;
        memcpy(sreang_dàta->ceadan_Liosta,ceadan_Liosta,sizeof(ceadan_Liosta));memcpy(sreang_dàta->faidhle_Liosta,faidhle_Liosta,sizeof(faidhle_Liosta));memcpy(sreang_dàta->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(sreang_dàta->argamaid_ARRAY,전달인수,sizeof(전달인수));memcpy(sreang_dàta->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<cleachdaiche_duilleag_COUNT;순번++)if(ceadan_Liosta[순번])memcpy((unsigned char *)snapshot(sealbhadair_nì)+순번*meud_na_duilleige,(void *)(cleachdaiche_BASE+순번*meud_na_duilleige),meud_na_duilleige);
    }else{
        저장값[sealbhadair_nì].멈춤상태=0;화면초기화(sealbhadair_nì);
        for(unsigned 순번=0;순번<16;순번++)if(faidhle_Liosta[순번]>=0)pk_close(faidhle_Liosta[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<cleachdaiche_duilleag_COUNT;순번++){duilleag_Liosta[순번]=0;ceadan_Liosta[순번]=0;}변환표맞추기();return tomhas;
}
uintptr_t bòrd_uidheam_smachd_cleachdaiche(uintptr_t Gnìomh){
    unsigned suidhich_INDEX=Gnìomh&15;if(suidhich_INDEX>=4||gnìomhach)return (uint32_t)-22;
    저장된작업 *sreang_dàta=&저장값[suidhich_INDEX];
    if(Gnìomh>=32){if(sreang_dàta->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(sreang_dàta->faidhle_Liosta[순번]>=0)pk_close(sreang_dàta->faidhle_Liosta[순번]);for(unsigned 순번=0;순번<24;순번++)if(sreang_dàta->통신끝점들[순번])통신끝점닫기(순번+32);}sreang_dàta->멈춤상태=0;화면초기화(suidhich_INDEX);return 0;}
    if(Gnìomh>=16)return sreang_dàta->멈춤상태;
    if(!sreang_dàta->멈춤상태)return (uint32_t)-22;
    sealbhadair_nì=suidhich_INDEX;eadar_ghnìomhach=sreang_dàta->eadar_ghnìomhach;리눅스규약=sreang_dàta->리눅스규약;동적기억끝=sreang_dàta->동적기억공간;전달인수개수=sreang_dàta->인수개수;
    memcpy(faidhle_Liosta,sreang_dàta->faidhle_Liosta,sizeof(faidhle_Liosta));memcpy(통신끝점들,sreang_dàta->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,sreang_dàta->argamaid_ARRAY,sizeof(전달인수));memcpy(전달인수길이,sreang_dàta->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<cleachdaiche_duilleag_COUNT;순번++)duilleag_Liosta[순번]=(cleachdaiche_BASE+순번*meud_na_duilleige)|eitean_duilleag;변환표맞추기();
    memset((void *)cleachdaiche_BASE,0,cleachdaiche_crìochnaich-cleachdaiche_BASE);
    for(unsigned 순번=0;순번<cleachdaiche_duilleag_COUNT;순번++)if(sreang_dàta->ceadan_Liosta[순번])memcpy((void *)(cleachdaiche_BASE+순번*meud_na_duilleige),(unsigned char *)snapshot(suidhich_INDEX)+순번*meud_na_duilleige,meud_na_duilleige);
    memcpy(ceadan_Liosta,sreang_dàta->ceadan_Liosta,sizeof(ceadan_Liosta));
    for(unsigned 순번=0;순번<cleachdaiche_duilleag_COUNT;순번++){unsigned dàta_suidhich=ceadan_Liosta[순번];duilleag_Liosta[순번]=dàta_suidhich?(cleachdaiche_BASE+순번*meud_na_duilleige)|(dàta_suidhich==3?cleachdaiche_so_leughte_so_sgrìobhte:dàta_suidhich==5?사용자읽고실행:cleachdaiche_ri_leughadh_a_mhàin):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");gnìomhach=1;sreang_dàta->멈춤상태=0;Start_TIMEOUT();
    사용자실행시각[sealbhadair_nì]=보드밀리초();
    return (uint32_t)Coilean_ap(cleachdaiche_cunntas_beatha_goirid(&sreang_dàta->실행틀,sreang_dàta->실수저장상태));
}
static int ruith_ap(const unsigned char *dàta, size_t atharraich_am_meud, unsigned 전달값, int 리눅스방식, const char *Ainm) {
    if (gnìomhach) return -16;
    sealbhadair_nì=bòrd_tèirmineal(11);if(sealbhadair_nì<0||sealbhadair_nì>3||저장값[sealbhadair_nì].멈춤상태)return -16;eadar_ghnìomhach=0;
    int 유효함 = 실행파일검사(dàta, atharraich_am_meud, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned ainm_INDEX=0;
    while (*Ainm && ainm_INDEX<31) cleachdaiche_àithne_ainm[sealbhadair_nì][ainm_INDEX++]=(unsigned char)*Ainm++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (ainm_INDEX) cleachdaiche_àithne_ainm[sealbhadair_nì][ainm_INDEX++]=' ';
        for (unsigned suidhich_INDEX=0; suidhich_INDEX<전달인수길이[0]; suidhich_INDEX++) cleachdaiche_àithne_ainm[sealbhadair_nì][ainm_INDEX++]=전달인수[0][suidhich_INDEX];
    }
    cleachdaiche_àithne_ainm[sealbhadair_nì][ainm_INDEX]=0; àireamh_cleachdaiche[sealbhadair_nì]=air_adhart_àireamh_cleachdaiche++;
    if (air_adhart_àireamh_cleachdaiche>0x7fffffffu) air_adhart_àireamh_cleachdaiche=10;
    cleachdaiche_Start_TIME[sealbhadair_nì]=보드밀리초(); 사용자누적시각[sealbhadair_nì]=0;
    for (unsigned 순번 = 0; 순번 < cleachdaiche_duilleag_COUNT; 순번++) duilleag_Liosta[순번] = (cleachdaiche_BASE + 순번 * meud_na_duilleige) | eitean_duilleag;
    변환표맞추기();
    memset((void *)cleachdaiche_BASE, 0, cleachdaiche_crìochnaich - cleachdaiche_BASE);
    memset(ceadan_Liosta, 0, sizeof(ceadan_Liosta));
    실행파일머리 실행머리; memcpy(&실행머리, dàta, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.ap_bann_cinn_COUNT; 순번++) {
        실행파일구획 dàta_suidhich; memcpy(&dàta_suidhich, dàta + 실행머리.ap_bann_cinn_OFFSET + 순번 * sizeof(dàta_suidhich), sizeof(dàta_suidhich));
        if (dàta_suidhich.TYPE_roinn_seòrsa != 1 || !dàta_suidhich.기억영역크기) continue;
        if (dàta_suidhich.파일영역크기) memcpy((void *)(uintptr_t)dàta_suidhich.ADDRESS, dàta + dàta_suidhich.OFFSET_VALUE, dàta_suidhich.파일영역크기);
        for (uintptr_t 현재위치 = dàta_suidhich.ADDRESS & ~(meud_na_duilleige - 1); 현재위치 < dàta_suidhich.ADDRESS + dàta_suidhich.기억영역크기; 현재위치 += meud_na_duilleige) {
            ceadan_Liosta[(현재위치 - cleachdaiche_BASE) / meud_na_duilleige] = (dàta_suidhich.설정비트 & 2) ? 3 : ((dàta_suidhich.설정비트 & 1) ? 5 : 1);
        }
    }
    for (uintptr_t 현재위치 = cleachdaiche_stac_ADDRESS; 현재위치 < cleachdaiche_crìochnaich; 현재위치 += meud_na_duilleige) ceadan_Liosta[(현재위치 - cleachdaiche_BASE) / meud_na_duilleige] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.cur_a_steach_puing) : cleachdaiche_crìochnaich;
    for (unsigned 순번 = 0; 순번 < cleachdaiche_duilleag_COUNT; 순번++) {
        unsigned ceadan = ceadan_Liosta[순번];
        duilleag_Liosta[순번] = ceadan ? (cleachdaiche_BASE + 순번 * meud_na_duilleige) | (ceadan == 3 ? cleachdaiche_so_leughte_so_sgrìobhte : ceadan == 5 ? 사용자읽고실행 : cleachdaiche_ri_leughadh_a_mhàin) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) faidhle_Liosta[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = cleachdaiche_IMAGE_crìochnaich;
    gnìomhach = 1; Start_TIMEOUT();
    사용자실행시각[sealbhadair_nì]=보드밀리초();
    int tomhas = cleachdaiche_cuir_a_steach(실행머리.cur_a_steach_puing, 초기쌓임공간, 전달값);
    return Coilean_ap(tomhas);
}
uintptr_t bòrd_cleachdaiche_ruith(uintptr_t LOOKUP_INDEX) {
    if (LOOKUP_INDEX >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Ainm=LOOKUP_INDEX==10?"javac":LOOKUP_INDEX==11?"java":LOOKUP_INDEX==12?"python":LOOKUP_INDEX==13?"vi":LOOKUP_INDEX==14?"jar":LOOKUP_INDEX==15?"cc":LOOKUP_INDEX==16?"jaot":"ELF";
    return (uint32_t)ruith_ap(실행항목들[LOOKUP_INDEX].dàta, 실행항목들[LOOKUP_INDEX].atharraich_am_meud, 실행항목들[LOOKUP_INDEX].전달값, 0, Ainm);
}
static uintptr_t gnìomhaich_faidhle(int 리눅스방식) {
    static unsigned char IMAGE[16384];
    if (gnìomhach || !전달인수개수) return (uint32_t)-22;
    int faidhle_làmhrachan = pk_open((const char *)전달인수[0], ri_leughadh_a_mhàin_VALUE, 0);
    if (faidhle_làmhrachan < 0) return (uint32_t)-오류번호;
    int atharraich_am_meud = pk_size(faidhle_làmhrachan);
    if (atharraich_am_meud < 0 || (unsigned)atharraich_am_meud > sizeof(IMAGE)) { pk_close(faidhle_làmhrachan); return (uint32_t)-27; }
    int RECEIVED_COUNT = pk_read(faidhle_làmhrachan, IMAGE, atharraich_am_meud); pk_close(faidhle_làmhrachan);
    if (RECEIVED_COUNT != atharraich_am_meud) return (uint32_t)-5;
    return (uint32_t)ruith_ap(IMAGE, atharraich_am_meud, 0, 리눅스방식, "");
}
uintptr_t bòrd_cleachdaiche_faidhle(void) { return gnìomhaich_faidhle(0); }
uintptr_t 보드사용자리눅스파일(void) { return gnìomhaich_faidhle(1); }
uintptr_t bòrd_cleachdaiche_dearbh(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].dàta, 잘못된실행항목들[순번].atharraich_am_meud) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
