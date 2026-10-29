#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "úsáideoir.h"
#include "../Líonra_Cruach/Líonra_Cruach.h"
typedef uintptr_t meaisín_Word;
#define meaisín_cláraigh(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define bosca_ríomhphoist_ADDRESS 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Clog_COUNT(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t FREQUENCY;
static volatile uint32_t bosca_ríomhphoist_sonraí[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *sonraí_suíomh, int pointe_cóid, size_t mír_COUNT) { unsigned char *Ar_aghaidh_OFFSET = sonraí_suíomh; while (mír_COUNT--) *Ar_aghaidh_OFFSET++ = pointe_cóid; return sonraí_suíomh; }
void *memcpy(void *sprioc_sonraí, const void *teaghrán_sonraí, size_t mír_COUNT) { unsigned char *첫째값 = sprioc_sonraí; const unsigned char *SECOND_VALUE = teaghrán_sonraí; while (mír_COUNT--) *첫째값++ = *SECOND_VALUE++; return sprioc_sonraí; }

static int bosca_ríomhphoist(void) {
    uint32_t iarratas_HTTP = (uint32_t)(uintptr_t)bosca_ríomhphoist_sonraí | 8;
    uint64_t Rith_2 = Clog_COUNT();
    기억장벽();
    while (meaisín_cláraigh(bosca_ríomhphoist_ADDRESS + 0x38) & 0x80000000u)
        if (Clog_COUNT() - Rith_2 > FREQUENCY) return 0;
    meaisín_cláraigh(bosca_ríomhphoist_ADDRESS + 0x20) = iarratas_HTTP;
    for (;;) {
        if (!(meaisín_cláraigh(bosca_ríomhphoist_ADDRESS + 0x18) & 0x40000000u)) {
            uint32_t freagair = meaisín_cláraigh(bosca_ríomhphoist_ADDRESS);
            if (freagair == iarratas_HTTP) { 기억장벽(); return bosca_ríomhphoist_sonraí[1] == 0x80000000u; }
        }
        if (Clog_COUNT() - Rith_2 > FREQUENCY) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Teirminéal_beart(unsigned);
extern int Teirminéal_Ar_feitheamh(void);
extern void Teirminéal_pointeoir(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../cianda_VALUE/cianda_VALUE.h"
static int 흐름목록;
static unsigned 직렬이전글자;
meaisín_Word 보드흐름설정(meaisín_Word 사용여부) { 흐름목록=사용여부!=0; return 0; }
meaisín_Word clár_cainéal(meaisín_Word cainéal, meaisín_Word pointe_cóid) {
    if(흐름목록 && 자바셸출력((int32_t)cainéal,(int32_t)(pointe_cóid&255))) return 0;
    Teirminéal_beart(pointe_cóid&255);
    원격출력(pointe_cóid&255);
    if ((pointe_cóid&255)==10 && 직렬이전글자!=13) {
        while (meaisín_cláraigh(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        meaisín_cláraigh(직렬장치)=13;
    }
    직렬이전글자=pointe_cóid&255;
    while (meaisín_cláraigh(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    meaisín_cláraigh(직렬장치) = (uint32_t)pointe_cóid & 255;
    return 0;
}
meaisín_Word 보드글자쓰기(meaisín_Word pointe_cóid) { return clár_cainéal(1,pointe_cóid); }
meaisín_Word 보드원시글자읽기(void) {
    int cianda_carachtar=원격입력();if(cianda_carachtar>=0)return cianda_carachtar;
    if (meaisín_cláraigh(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t VALUE = meaisín_cláraigh(직렬장치);
    if (VALUE & 0xf00) { meaisín_cláraigh(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return VALUE & 255;
}
meaisín_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char paicéad_sonraí[6];
    if(Teirminéal_Ar_feitheamh())return (uint32_t)-4096;
    if(흐름목록){int32_t pointe_cóid=자바셸입력();if(pointe_cóid!=-3)return (uint32_t)pointe_cóid;}
    for(;;){
        int pointe_cóid=(int32_t)보드원시글자읽기();if(pointe_cóid<0)return (uint32_t)pointe_cóid;
        if(!꾸러미안쪽){if(pointe_cóid!=30)return pointe_cóid;꾸러미안쪽=1;사용량=0;continue;}
        paicéad_sonraí[사용량++]=pointe_cóid;if(사용량<6)continue;꾸러미안쪽=0;
        if(paicéad_sonraí[0]==1)Teirminéal_pointeoir(paicéad_sonraí[1],paicéad_sonraí[2]+paicéad_sonraí[3]*256,paicéad_sonraí[4]+paicéad_sonraí[5]*256);
        if(paicéad_sonraí[0]==2)터미널바로가기키(paicéad_sonraí[1]);
        if(paicéad_sonraí[0]==3)터미널입력방식(paicéad_sonraí[1]);
        if(Teirminéal_Ar_feitheamh())return (uint32_t)-4096;
    }
}
meaisín_Word 보드밀리초(void) { return (uint32_t)(Clog_COUNT() / (FREQUENCY / 1000)); }
meaisín_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *teaghrán_sonraí) { while (*teaghrán_sonraí) 보드글자쓰기((unsigned char)*teaghrán_sonraí++); }
static void 직렬열여섯진출력(meaisín_Word mír_COUNT) { const char *열여섯진숫자 = "0123456789abcdef"; for (int teaghrán_sonraí = 60; teaghrán_sonraí >= 0; teaghrán_sonraí -= 4) 보드글자쓰기(열여섯진숫자[(mír_COUNT >> teaghrán_sonraí) & 15]); }
meaisín_Word clár_stop(meaisín_Word staid_VALUE) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(staid_VALUE); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); clár_stop(1); __builtin_unreachable(); }
void clár_eisceacht(meaisín_Word eisceacht_staid, meaisín_Word ordú_suíomh, meaisín_Word neamhbhailí_ADDRESS) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(eisceacht_staid);
    직렬글출력(" PC="); 직렬열여섯진출력(ordú_suíomh); 직렬글출력(" FAR="); 직렬열여섯진출력(neamhbhailí_ADDRESS);
    clár_stop(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    bosca_ríomhphoist_sonraí[0]=32;bosca_ríomhphoist_sonraí[1]=0;bosca_ríomhphoist_sonraí[2]=0x10004;bosca_ríomhphoist_sonraí[3]=8;bosca_ríomhphoist_sonraí[4]=0;
    bosca_ríomhphoist_sonraí[5]=bosca_ríomhphoist_sonraí[6]=bosca_ríomhphoist_sonraí[7]=0;
    return bosca_ríomhphoist()&&bosca_ríomhphoist_sonraí[4]==0x80000008u&&(bosca_ríomhphoist_sonraí[5]||bosca_ríomhphoist_sonraí[6]);
}
int clár_meaisín_ADDRESS(unsigned char *ADDRESS) {
    bosca_ríomhphoist_sonraí[0]=32;bosca_ríomhphoist_sonraí[1]=0;bosca_ríomhphoist_sonraí[2]=0x10003;bosca_ríomhphoist_sonraí[3]=8;bosca_ríomhphoist_sonraí[4]=0;
    bosca_ríomhphoist_sonraí[5]=bosca_ríomhphoist_sonraí[6]=bosca_ríomhphoist_sonraí[7]=0;
    if(!bosca_ríomhphoist()||(bosca_ríomhphoist_sonraí[4]&0x80000000u)==0||(bosca_ríomhphoist_sonraí[4]&0xffff)!=6)return 0;
    const unsigned char *sonraí=(const unsigned char*)&bosca_ríomhphoist_sonraí[5];unsigned SUM_VALUE=0;
    for(unsigned 순번=0;순번<6;순번++){ADDRESS[순번]=sonraí[순번];SUM_VALUE|=sonraí[순번];}return SUM_VALUE&&!(ADDRESS[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    meaisín_cláraigh(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    meaisín_cláraigh(범용입출력 + 4) = (meaisín_cláraigh(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    meaisín_cláraigh(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. teip_VALUE 시 config.txt의 48MHz를 사용한다.
    bosca_ríomhphoist_sonraí[0] = 36; bosca_ríomhphoist_sonraí[1] = 0; bosca_ríomhphoist_sonraí[2] = 0x38002; bosca_ríomhphoist_sonraí[3] = 12;
    bosca_ríomhphoist_sonraí[4] = 0; bosca_ríomhphoist_sonraí[5] = 2; bosca_ríomhphoist_sonraí[6] = 48000000; bosca_ríomhphoist_sonraí[7] = 0; bosca_ríomhphoist_sonraí[8] = 0;
    int 시계정상 = bosca_ríomhphoist();
    uint32_t 속도 = 시계정상 && bosca_ríomhphoist_sonraí[6] >= 1843200 ? bosca_ríomhphoist_sonraí[6] : 48000000;
    bosca_ríomhphoist_sonraí[0]=32; bosca_ríomhphoist_sonraí[1]=0; bosca_ríomhphoist_sonraí[2]=0x10005; bosca_ríomhphoist_sonraí[3]=8; bosca_ríomhphoist_sonraí[4]=0;
    bosca_ríomhphoist_sonraí[5]=bosca_ríomhphoist_sonraí[6]=bosca_ríomhphoist_sonraí[7]=0;
    if (bosca_ríomhphoist() && bosca_ríomhphoist_sonraí[4]==0x80000008u) 팔기억킬로바이트=bosca_ríomhphoist_sonraí[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    meaisín_cláraigh(직렬장치 + 0x44) = 0x7ff;
    meaisín_cláraigh(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    meaisín_cláraigh(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    meaisín_cláraigh(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    meaisín_cláraigh(직렬장치 + 0x38) = 0;
    meaisín_cláraigh(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
meaisín_Word clár_FTP(meaisín_Word Gníomh) { return (uint32_t)ftp_control((int)Gníomh); }
meaisín_Word clár_Líonra_staid(meaisín_Word iontráil_VALUE, meaisín_Word INDEX) { return 망상태읽기(iontráil_VALUE, INDEX); }
meaisín_Word clár_Líonra_Socruithe(meaisín_Word Gníomh, meaisín_Word ADDRESS, meaisín_Word masc_VALUE, meaisín_Word geata_VALUE) { return (uint32_t)cumraigh_Líonra(Gníomh, ADDRESS, masc_VALUE, geata_VALUE); }
meaisín_Word 보드응답보내기(meaisín_Word ADDRESS, meaisín_Word ord_VALUE) { return (uint32_t)응답시험시작(ADDRESS, ord_VALUE); }
meaisín_Word 보드응답읽기(meaisín_Word iontráil_VALUE) { return (uint32_t)응답시험읽기(iontráil_VALUE); }
meaisín_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEX=0; INDEX<32; INDEX++) dún_Líonra(INDEX);
    for (unsigned INDEX=0; INDEX<4; INDEX++) clár_rialtán_úsáideora(32+INDEX);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (meaisín_cláraigh(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    meaisín_cláraigh(0xfe100020ul)=0x5a000000u | (meaisín_cláraigh(0xfe100020ul)&~0xfffu) | 0x555;
    meaisín_cláraigh(0xfe100024ul)=0x5a000000u | 10;
    meaisín_cláraigh(0xfe10001cul)=0x5a000000u | (meaisín_cláraigh(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

meaisín_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 현재 크기를 읽는다. */
    const uint32_t iarratas_VALUE[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(iarratas_VALUE)/4; 순번++) bosca_ríomhphoist_sonraí[순번] = iarratas_VALUE[순번];
    if (bosca_ríomhphoist() && bosca_ríomhphoist_sonraí[4] == 0x80000008u &&
        bosca_ríomhphoist_sonraí[5] >= 640 && bosca_ríomhphoist_sonraí[5] <= 1920 &&
        bosca_ríomhphoist_sonraí[6] >= 480 && bosca_ríomhphoist_sonraí[6] <= 1080) {
        요청너비 = bosca_ríomhphoist_sonraí[5]; 요청높이 = bosca_ríomhphoist_sonraí[6];
    }
    const uint32_t iarratas_HTTP[] = {
        35 * 4, 0,
        0x48003, 8, 0, 요청너비, 요청높이,
        0x48004, 8, 0, 요청너비, 요청높이,
        0x48005, 4, 0, 32,
        0x48006, 4, 0, 1,
        0x48009, 8, 0, 0, 0,
        0x40001, 8, 0, 4096, 0,
        0x40008, 4, 0, 0,
        0
    };
    for (size_t 순번 = 0; 순번 < sizeof(iarratas_HTTP)/4; 순번++) bosca_ríomhphoist_sonraí[순번] = iarratas_HTTP[순번];
    // 위 메시지의 iarbhír_sonraí 길이를 사용: 태그 추가 시 fad_VALUE 불일치를 방지한다.
    bosca_ríomhphoist_sonraí[0] = sizeof(iarratas_HTTP);
    if (!bosca_ríomhphoist()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 응답길이[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (bosca_ríomhphoist_sonraí[응답들[순번]] != (0x80000000u | 응답길이[순번])) return 0;
    uint32_t Cúlra_VALUE = bosca_ríomhphoist_sonraí[28] & 0x3fffffffu;
    uint32_t Méid = bosca_ríomhphoist_sonraí[29];
    uint32_t 받은너비 = bosca_ríomhphoist_sonraí[5], 받은높이 = bosca_ríomhphoist_sonraí[6], RECEIVED_spásáil_línte = bosca_ríomhphoist_sonraí[33];
    if (bosca_ríomhphoist_sonraí[15] != 32 || bosca_ríomhphoist_sonraí[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        bosca_ríomhphoist_sonraí[10] < 받은너비 || bosca_ríomhphoist_sonraí[11] < 받은높이 || bosca_ríomhphoist_sonraí[23] || bosca_ríomhphoist_sonraí[24] ||
        !Cúlra_VALUE || Cúlra_VALUE < 0x1000000 || (Cúlra_VALUE & 3) || RECEIVED_spásáil_línte < 받은너비 * 4 || (RECEIVED_spásáil_línte & 3) ||
        (uint64_t)RECEIVED_spásáil_línte * 받은높이 > Méid || (uint64_t)Cúlra_VALUE + Méid > 0x40000000u)
        return 0;
    clár_Ullmhaigh_líníocht((volatile uint32_t *)(uintptr_t)Cúlra_VALUE, 받은너비, 받은높이, RECEIVED_spásáil_línte);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 snáithe_VALUE. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } Comhthéacs;
static Comhthéacs 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int 실행중[3] = {1, 0, 0};
static int 현재작업;
extern void Comhthéacs_SWITCH(Comhthéacs *, Comhthéacs *);
extern void 자바작업(int32_t);
meaisín_Word clár_YIELD(void) {
    network_poll();
    int 이전 = 현재작업, Ar_aghaidh_mír = (이전 + 1) % 3;
    while (Ar_aghaidh_mír != 이전 && !실행중[Ar_aghaidh_mír]) Ar_aghaidh_mír = (Ar_aghaidh_mír + 1) % 3;
    if (Ar_aghaidh_mír != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (실행중[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        현재작업 = Ar_aghaidh_mír;
        Comhthéacs_SWITCH(&작업문맥들[이전], &작업문맥들[Ar_aghaidh_mír]);
    }
    return 0;
}
static void tasc_tosú(void) {
    자바작업(현재작업);
    실행중[현재작업] = 0;
    clár_YIELD();
    커널중단("finished task resumed");
}
meaisín_Word clár_tasc_Create(meaisín_Word aitheantóir_VALUE) {
    if (aitheantóir_VALUE < 1 || aitheantóir_VALUE > 2 || 실행중[aitheantóir_VALUE]) return (uint32_t)-1;
    memset(&작업문맥들[aitheantóir_VALUE], 0, sizeof(Comhthéacs));
    *(uint64_t *)쌓임공간들[aitheantóir_VALUE - 1] = 0x6b6f726f7373746bull;
    작업문맥들[aitheantóir_VALUE].저장값[11] = (uintptr_t)tasc_tosú;
    작업문맥들[aitheantóir_VALUE].저장값[12] = (uintptr_t)(쌓임공간들[aitheantóir_VALUE - 1] + sizeof(쌓임공간들[0]));
    실행중[aitheantóir_VALUE] = 1;
    return 0;
}
meaisín_Word clár_tasc_staid(meaisín_Word aitheantóir_VALUE) { return aitheantóir_VALUE < 3 ? 실행중[aitheantóir_VALUE] : (uint32_t)-1; }
extern meaisín_Word 미리번역기억조회(meaisín_Word);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
meaisín_Word clár_iarratas_córas(meaisín_Word iontráil_VALUE, meaisín_Word INDEX) {
    if (iontráil_VALUE==0) return 팔기억킬로바이트;
    if (iontráil_VALUE==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (iontráil_VALUE==2 || iontráil_VALUE==3) return 미리번역기억조회(iontráil_VALUE==3);
    if (iontráil_VALUE==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (iontráil_VALUE==5) return 80*1024; /* Rith_ordú 공간 16 MiB + 네 세션 보관 공간. */
    if (iontráil_VALUE>=20) return 사용자상태읽기(iontráil_VALUE-20, INDEX);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[현재작업]; }
