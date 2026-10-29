#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "cleachdaiche.h"
#include "../lìonra_stac/lìonra_stac.h"
typedef uintptr_t inneal_Word;
#define inneal_clàraich(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define bogsa_puist_ADDRESS 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t cleoc_COUNT(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t FREQUENCY;
static volatile uint32_t bogsa_puist_dàta[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *dàta_suidhich, int còd_a_charactair, size_t nì_COUNT) { unsigned char *air_adhart_OFFSET = dàta_suidhich; while (nì_COUNT--) *air_adhart_OFFSET++ = còd_a_charactair; return dàta_suidhich; }
void *memcpy(void *ceann_uidhe_dàta, const void *sreang_dàta, size_t nì_COUNT) { unsigned char *첫째값 = ceann_uidhe_dàta; const unsigned char *SECOND_VALUE = sreang_dàta; while (nì_COUNT--) *첫째값++ = *SECOND_VALUE++; return ceann_uidhe_dàta; }

static int bogsa_puist(void) {
    uint32_t 요청 = (uint32_t)(uintptr_t)bogsa_puist_dàta | 8;
    uint64_t ruith = cleoc_COUNT();
    기억장벽();
    while (inneal_clàraich(bogsa_puist_ADDRESS + 0x38) & 0x80000000u)
        if (cleoc_COUNT() - ruith > FREQUENCY) return 0;
    inneal_clàraich(bogsa_puist_ADDRESS + 0x20) = 요청;
    for (;;) {
        if (!(inneal_clàraich(bogsa_puist_ADDRESS + 0x18) & 0x40000000u)) {
            uint32_t freagair = inneal_clàraich(bogsa_puist_ADDRESS);
            if (freagair == 요청) { 기억장벽(); return bogsa_puist_dàta[1] == 0x80000000u; }
        }
        if (cleoc_COUNT() - ruith > FREQUENCY) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void tèirmineal_baidht(unsigned);
extern int tèirmineal_ri_dhèiligeadh(void);
extern void tèirmineal_tomhaire(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../cian_VALUE/cian_VALUE.h"
static int 흐름목록;
static unsigned 직렬이전글자;
inneal_Word 보드흐름설정(inneal_Word 사용여부) { 흐름목록=사용여부!=0; return 0; }
inneal_Word bòrd_seanail(inneal_Word seanail, inneal_Word còd_a_charactair) {
    if(흐름목록 && 자바셸출력((int32_t)seanail,(int32_t)(còd_a_charactair&255))) return 0;
    tèirmineal_baidht(còd_a_charactair&255);
    원격출력(còd_a_charactair&255);
    if ((còd_a_charactair&255)==10 && 직렬이전글자!=13) {
        while (inneal_clàraich(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        inneal_clàraich(직렬장치)=13;
    }
    직렬이전글자=còd_a_charactair&255;
    while (inneal_clàraich(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    inneal_clàraich(직렬장치) = (uint32_t)còd_a_charactair & 255;
    return 0;
}
inneal_Word 보드글자쓰기(inneal_Word còd_a_charactair) { return bòrd_seanail(1,còd_a_charactair); }
inneal_Word 보드원시글자읽기(void) {
    int cian_caractar=원격입력();if(cian_caractar>=0)return cian_caractar;
    if (inneal_clàraich(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t VALUE = inneal_clàraich(직렬장치);
    if (VALUE & 0xf00) { inneal_clàraich(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return VALUE & 255;
}
inneal_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char 꾸러미자료[6];
    if(tèirmineal_ri_dhèiligeadh())return (uint32_t)-4096;
    if(흐름목록){int32_t còd_a_charactair=자바셸입력();if(còd_a_charactair!=-3)return (uint32_t)còd_a_charactair;}
    for(;;){
        int còd_a_charactair=(int32_t)보드원시글자읽기();if(còd_a_charactair<0)return (uint32_t)còd_a_charactair;
        if(!꾸러미안쪽){if(còd_a_charactair!=30)return còd_a_charactair;꾸러미안쪽=1;사용량=0;continue;}
        꾸러미자료[사용량++]=còd_a_charactair;if(사용량<6)continue;꾸러미안쪽=0;
        if(꾸러미자료[0]==1)tèirmineal_tomhaire(꾸러미자료[1],꾸러미자료[2]+꾸러미자료[3]*256,꾸러미자료[4]+꾸러미자료[5]*256);
        if(꾸러미자료[0]==2)터미널바로가기키(꾸러미자료[1]);
        if(꾸러미자료[0]==3)터미널입력방식(꾸러미자료[1]);
        if(tèirmineal_ri_dhèiligeadh())return (uint32_t)-4096;
    }
}
inneal_Word 보드밀리초(void) { return (uint32_t)(cleoc_COUNT() / (FREQUENCY / 1000)); }
inneal_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *sreang_dàta) { while (*sreang_dàta) 보드글자쓰기((unsigned char)*sreang_dàta++); }
static void 직렬열여섯진출력(inneal_Word nì_COUNT) { const char *열여섯진숫자 = "0123456789abcdef"; for (int sreang_dàta = 60; sreang_dàta >= 0; sreang_dàta -= 4) 보드글자쓰기(열여섯진숫자[(nì_COUNT >> sreang_dàta) & 15]); }
inneal_Word bòrd_Stad(inneal_Word cor_VALUE) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(cor_VALUE); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); bòrd_Stad(1); __builtin_unreachable(); }
void 보드예외(inneal_Word 예외상태, inneal_Word àithne_suidhich, inneal_Word mì_dhligheach_ADDRESS) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(예외상태);
    직렬글출력(" PC="); 직렬열여섯진출력(àithne_suidhich); 직렬글출력(" FAR="); 직렬열여섯진출력(mì_dhligheach_ADDRESS);
    bòrd_Stad(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    bogsa_puist_dàta[0]=32;bogsa_puist_dàta[1]=0;bogsa_puist_dàta[2]=0x10004;bogsa_puist_dàta[3]=8;bogsa_puist_dàta[4]=0;
    bogsa_puist_dàta[5]=bogsa_puist_dàta[6]=bogsa_puist_dàta[7]=0;
    return bogsa_puist()&&bogsa_puist_dàta[4]==0x80000008u&&(bogsa_puist_dàta[5]||bogsa_puist_dàta[6]);
}
int bòrd_inneal_ADDRESS(unsigned char *ADDRESS) {
    bogsa_puist_dàta[0]=32;bogsa_puist_dàta[1]=0;bogsa_puist_dàta[2]=0x10003;bogsa_puist_dàta[3]=8;bogsa_puist_dàta[4]=0;
    bogsa_puist_dàta[5]=bogsa_puist_dàta[6]=bogsa_puist_dàta[7]=0;
    if(!bogsa_puist()||(bogsa_puist_dàta[4]&0x80000000u)==0||(bogsa_puist_dàta[4]&0xffff)!=6)return 0;
    const unsigned char *dàta=(const unsigned char*)&bogsa_puist_dàta[5];unsigned SUM_VALUE=0;
    for(unsigned 순번=0;순번<6;순번++){ADDRESS[순번]=dàta[순번];SUM_VALUE|=dàta[순번];}return SUM_VALUE&&!(ADDRESS[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    inneal_clàraich(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    inneal_clàraich(범용입출력 + 4) = (inneal_clàraich(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    inneal_clàraich(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. fàilligeadh_VALUE 시 config.txt의 48MHz를 사용한다.
    bogsa_puist_dàta[0] = 36; bogsa_puist_dàta[1] = 0; bogsa_puist_dàta[2] = 0x38002; bogsa_puist_dàta[3] = 12;
    bogsa_puist_dàta[4] = 0; bogsa_puist_dàta[5] = 2; bogsa_puist_dàta[6] = 48000000; bogsa_puist_dàta[7] = 0; bogsa_puist_dàta[8] = 0;
    int 시계정상 = bogsa_puist();
    uint32_t 속도 = 시계정상 && bogsa_puist_dàta[6] >= 1843200 ? bogsa_puist_dàta[6] : 48000000;
    bogsa_puist_dàta[0]=32; bogsa_puist_dàta[1]=0; bogsa_puist_dàta[2]=0x10005; bogsa_puist_dàta[3]=8; bogsa_puist_dàta[4]=0;
    bogsa_puist_dàta[5]=bogsa_puist_dàta[6]=bogsa_puist_dàta[7]=0;
    if (bogsa_puist() && bogsa_puist_dàta[4]==0x80000008u) 팔기억킬로바이트=bogsa_puist_dàta[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    inneal_clàraich(직렬장치 + 0x44) = 0x7ff;
    inneal_clàraich(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    inneal_clàraich(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    inneal_clàraich(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    inneal_clàraich(직렬장치 + 0x38) = 0;
    inneal_clàraich(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
inneal_Word bòrd_FTP(inneal_Word Gnìomh) { return (uint32_t)ftp_control((int)Gnìomh); }
inneal_Word bòrd_lìonra_cor(inneal_Word cur_a_steach_VALUE, inneal_Word INDEX) { return 망상태읽기(cur_a_steach_VALUE, INDEX); }
inneal_Word bòrd_lìonra_roghainnean(inneal_Word Gnìomh, inneal_Word ADDRESS, inneal_Word 가림, inneal_Word 관문) { return (uint32_t)rèitich_lìonra(Gnìomh, ADDRESS, 가림, 관문); }
inneal_Word 보드응답보내기(inneal_Word ADDRESS, inneal_Word òrdugh_VALUE) { return (uint32_t)응답시험시작(ADDRESS, òrdugh_VALUE); }
inneal_Word 보드응답읽기(inneal_Word cur_a_steach_VALUE) { return (uint32_t)응답시험읽기(cur_a_steach_VALUE); }
inneal_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEX=0; INDEX<32; INDEX++) dùin_lìonra(INDEX);
    for (unsigned INDEX=0; INDEX<4; INDEX++) bòrd_uidheam_smachd_cleachdaiche(32+INDEX);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (inneal_clàraich(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    inneal_clàraich(0xfe100020ul)=0x5a000000u | (inneal_clàraich(0xfe100020ul)&~0xfffu) | 0x555;
    inneal_clàraich(0xfe100024ul)=0x5a000000u | 10;
    inneal_clàraich(0xfe10001cul)=0x5a000000u | (inneal_clàraich(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

inneal_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 현재 크기를 읽는다. */
    const uint32_t ceist_VALUE[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(ceist_VALUE)/4; 순번++) bogsa_puist_dàta[순번] = ceist_VALUE[순번];
    if (bogsa_puist() && bogsa_puist_dàta[4] == 0x80000008u &&
        bogsa_puist_dàta[5] >= 640 && bogsa_puist_dàta[5] <= 1920 &&
        bogsa_puist_dàta[6] >= 480 && bogsa_puist_dàta[6] <= 1080) {
        요청너비 = bogsa_puist_dàta[5]; 요청높이 = bogsa_puist_dàta[6];
    }
    const uint32_t 요청[] = {
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
    for (size_t 순번 = 0; 순번 < sizeof(요청)/4; 순번++) bogsa_puist_dàta[순번] = 요청[순번];
    // 위 메시지의 dearbh_dàta 길이를 사용: 태그 추가 시 faid_VALUE 불일치를 방지한다.
    bogsa_puist_dàta[0] = sizeof(요청);
    if (!bogsa_puist()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 응답길이[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (bogsa_puist_dàta[응답들[순번]] != (0x80000000u | 응답길이[순번])) return 0;
    uint32_t cùlaibh_VALUE = bogsa_puist_dàta[28] & 0x3fffffffu;
    uint32_t atharraich_am_meud = bogsa_puist_dàta[29];
    uint32_t 받은너비 = bogsa_puist_dàta[5], 받은높이 = bogsa_puist_dàta[6], RECEIVED_beàrn_eadar_dà_loidhne = bogsa_puist_dàta[33];
    if (bogsa_puist_dàta[15] != 32 || bogsa_puist_dàta[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        bogsa_puist_dàta[10] < 받은너비 || bogsa_puist_dàta[11] < 받은높이 || bogsa_puist_dàta[23] || bogsa_puist_dàta[24] ||
        !cùlaibh_VALUE || cùlaibh_VALUE < 0x1000000 || (cùlaibh_VALUE & 3) || RECEIVED_beàrn_eadar_dà_loidhne < 받은너비 * 4 || (RECEIVED_beàrn_eadar_dà_loidhne & 3) ||
        (uint64_t)RECEIVED_beàrn_eadar_dà_loidhne * 받은높이 > atharraich_am_meud || (uint64_t)cùlaibh_VALUE + atharraich_am_meud > 0x40000000u)
        return 0;
    bòrd_Ullaich_tarraing((volatile uint32_t *)(uintptr_t)cùlaibh_VALUE, 받은너비, 받은높이, RECEIVED_beàrn_eadar_dà_loidhne);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 snàithlean_VALUE. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } co_theacsa;
static co_theacsa 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int 실행중[3] = {1, 0, 0};
static int 현재작업;
extern void co_theacsa_SWITCH(co_theacsa *, co_theacsa *);
extern void 자바작업(int32_t);
inneal_Word bòrd_YIELD(void) {
    network_poll();
    int 이전 = 현재작업, air_adhart_nì = (이전 + 1) % 3;
    while (air_adhart_nì != 이전 && !실행중[air_adhart_nì]) air_adhart_nì = (air_adhart_nì + 1) % 3;
    if (air_adhart_nì != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (실행중[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        현재작업 = air_adhart_nì;
        co_theacsa_SWITCH(&작업문맥들[이전], &작업문맥들[air_adhart_nì]);
    }
    return 0;
}
static void saothair_tòiseachadh(void) {
    자바작업(현재작업);
    실행중[현재작업] = 0;
    bòrd_YIELD();
    커널중단("finished task resumed");
}
inneal_Word bòrd_saothair_Create(inneal_Word aithnichear_VALUE) {
    if (aithnichear_VALUE < 1 || aithnichear_VALUE > 2 || 실행중[aithnichear_VALUE]) return (uint32_t)-1;
    memset(&작업문맥들[aithnichear_VALUE], 0, sizeof(co_theacsa));
    *(uint64_t *)쌓임공간들[aithnichear_VALUE - 1] = 0x6b6f726f7373746bull;
    작업문맥들[aithnichear_VALUE].저장값[11] = (uintptr_t)saothair_tòiseachadh;
    작업문맥들[aithnichear_VALUE].저장값[12] = (uintptr_t)(쌓임공간들[aithnichear_VALUE - 1] + sizeof(쌓임공간들[0]));
    실행중[aithnichear_VALUE] = 1;
    return 0;
}
inneal_Word bòrd_saothair_cor(inneal_Word aithnichear_VALUE) { return aithnichear_VALUE < 3 ? 실행중[aithnichear_VALUE] : (uint32_t)-1; }
extern inneal_Word 미리번역기억조회(inneal_Word);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
inneal_Word bòrd_ceist_siostam(inneal_Word cur_a_steach_VALUE, inneal_Word INDEX) {
    if (cur_a_steach_VALUE==0) return 팔기억킬로바이트;
    if (cur_a_steach_VALUE==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (cur_a_steach_VALUE==2 || cur_a_steach_VALUE==3) return 미리번역기억조회(cur_a_steach_VALUE==3);
    if (cur_a_steach_VALUE==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (cur_a_steach_VALUE==5) return 80*1024; /* gnìomhaich_àithne 공간 16 MiB + 네 세션 보관 공간. */
    if (cur_a_steach_VALUE>=20) return 사용자상태읽기(cur_a_steach_VALUE-20, INDEX);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[현재작업]; }
