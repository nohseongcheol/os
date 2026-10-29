#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "defnyddiwr.h"
#include "../Rhwydwaith_pentwr/Rhwydwaith_pentwr.h"
typedef uintptr_t peiriant_Word;
#define peiriant_cofrestru(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define blwch_post_ADDRESS 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Cloc_COUNT(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t FREQUENCY;
static volatile uint32_t blwch_post_data[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *data_safle, int cod_nod, size_t eitem_COUNT) { unsigned char *Nesaf_OFFSET = data_safle; while (eitem_COUNT--) *Nesaf_OFFSET++ = cod_nod; return data_safle; }
void *memcpy(void *cyrchfan_data, const void *testun_data, size_t eitem_COUNT) { unsigned char *첫째값 = cyrchfan_data; const unsigned char *SECOND_VALUE = testun_data; while (eitem_COUNT--) *첫째값++ = *SECOND_VALUE++; return cyrchfan_data; }

static int blwch_post(void) {
    uint32_t cais_HTTP = (uint32_t)(uintptr_t)blwch_post_data | 8;
    uint64_t Gweithredu_2 = Cloc_COUNT();
    기억장벽();
    while (peiriant_cofrestru(blwch_post_ADDRESS + 0x38) & 0x80000000u)
        if (Cloc_COUNT() - Gweithredu_2 > FREQUENCY) return 0;
    peiriant_cofrestru(blwch_post_ADDRESS + 0x20) = cais_HTTP;
    for (;;) {
        if (!(peiriant_cofrestru(blwch_post_ADDRESS + 0x18) & 0x40000000u)) {
            uint32_t ateb = peiriant_cofrestru(blwch_post_ADDRESS);
            if (ateb == cais_HTTP) { 기억장벽(); return blwch_post_data[1] == 0x80000000u; }
        }
        if (Cloc_COUNT() - Gweithredu_2 > FREQUENCY) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terfynell_beit(unsigned);
extern int Terfynell_yn_disgwyl(void);
extern void Terfynell_pwyntydd(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../pell_VALUE/pell_VALUE.h"
static int 흐름목록;
static unsigned 직렬이전글자;
peiriant_Word 보드흐름설정(peiriant_Word 사용여부) { 흐름목록=사용여부!=0; return 0; }
peiriant_Word bwrdd_sianel(peiriant_Word sianel, peiriant_Word cod_nod) {
    if(흐름목록 && 자바셸출력((int32_t)sianel,(int32_t)(cod_nod&255))) return 0;
    Terfynell_beit(cod_nod&255);
    원격출력(cod_nod&255);
    if ((cod_nod&255)==10 && 직렬이전글자!=13) {
        while (peiriant_cofrestru(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        peiriant_cofrestru(직렬장치)=13;
    }
    직렬이전글자=cod_nod&255;
    while (peiriant_cofrestru(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    peiriant_cofrestru(직렬장치) = (uint32_t)cod_nod & 255;
    return 0;
}
peiriant_Word 보드글자쓰기(peiriant_Word cod_nod) { return bwrdd_sianel(1,cod_nod); }
peiriant_Word 보드원시글자읽기(void) {
    int pell_nod=원격입력();if(pell_nod>=0)return pell_nod;
    if (peiriant_cofrestru(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t VALUE = peiriant_cofrestru(직렬장치);
    if (VALUE & 0xf00) { peiriant_cofrestru(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return VALUE & 255;
}
peiriant_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char 꾸러미자료[6];
    if(Terfynell_yn_disgwyl())return (uint32_t)-4096;
    if(흐름목록){int32_t cod_nod=자바셸입력();if(cod_nod!=-3)return (uint32_t)cod_nod;}
    for(;;){
        int cod_nod=(int32_t)보드원시글자읽기();if(cod_nod<0)return (uint32_t)cod_nod;
        if(!꾸러미안쪽){if(cod_nod!=30)return cod_nod;꾸러미안쪽=1;사용량=0;continue;}
        꾸러미자료[사용량++]=cod_nod;if(사용량<6)continue;꾸러미안쪽=0;
        if(꾸러미자료[0]==1)Terfynell_pwyntydd(꾸러미자료[1],꾸러미자료[2]+꾸러미자료[3]*256,꾸러미자료[4]+꾸러미자료[5]*256);
        if(꾸러미자료[0]==2)터미널바로가기키(꾸러미자료[1]);
        if(꾸러미자료[0]==3)터미널입력방식(꾸러미자료[1]);
        if(Terfynell_yn_disgwyl())return (uint32_t)-4096;
    }
}
peiriant_Word 보드밀리초(void) { return (uint32_t)(Cloc_COUNT() / (FREQUENCY / 1000)); }
peiriant_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *testun_data) { while (*testun_data) 보드글자쓰기((unsigned char)*testun_data++); }
static void 직렬열여섯진출력(peiriant_Word eitem_COUNT) { const char *열여섯진숫자 = "0123456789abcdef"; for (int testun_data = 60; testun_data >= 0; testun_data -= 4) 보드글자쓰기(열여섯진숫자[(eitem_COUNT >> testun_data) & 15]); }
peiriant_Word bwrdd_Stop(peiriant_Word cyflwr_VALUE) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(cyflwr_VALUE); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); bwrdd_Stop(1); __builtin_unreachable(); }
void bwrdd_eithriad(peiriant_Word eithriad_cyflwr, peiriant_Word gorchymyn_safle, peiriant_Word annilys_ADDRESS) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(eithriad_cyflwr);
    직렬글출력(" PC="); 직렬열여섯진출력(gorchymyn_safle); 직렬글출력(" FAR="); 직렬열여섯진출력(annilys_ADDRESS);
    bwrdd_Stop(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    blwch_post_data[0]=32;blwch_post_data[1]=0;blwch_post_data[2]=0x10004;blwch_post_data[3]=8;blwch_post_data[4]=0;
    blwch_post_data[5]=blwch_post_data[6]=blwch_post_data[7]=0;
    return blwch_post()&&blwch_post_data[4]==0x80000008u&&(blwch_post_data[5]||blwch_post_data[6]);
}
int bwrdd_peiriant_ADDRESS(unsigned char *ADDRESS) {
    blwch_post_data[0]=32;blwch_post_data[1]=0;blwch_post_data[2]=0x10003;blwch_post_data[3]=8;blwch_post_data[4]=0;
    blwch_post_data[5]=blwch_post_data[6]=blwch_post_data[7]=0;
    if(!blwch_post()||(blwch_post_data[4]&0x80000000u)==0||(blwch_post_data[4]&0xffff)!=6)return 0;
    const unsigned char *data=(const unsigned char*)&blwch_post_data[5];unsigned SUM_VALUE=0;
    for(unsigned 순번=0;순번<6;순번++){ADDRESS[순번]=data[순번];SUM_VALUE|=data[순번];}return SUM_VALUE&&!(ADDRESS[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    peiriant_cofrestru(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    peiriant_cofrestru(범용입출력 + 4) = (peiriant_cofrestru(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    peiriant_cofrestru(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. methiant_VALUE 시 config.txt의 48MHz를 사용한다.
    blwch_post_data[0] = 36; blwch_post_data[1] = 0; blwch_post_data[2] = 0x38002; blwch_post_data[3] = 12;
    blwch_post_data[4] = 0; blwch_post_data[5] = 2; blwch_post_data[6] = 48000000; blwch_post_data[7] = 0; blwch_post_data[8] = 0;
    int 시계정상 = blwch_post();
    uint32_t 속도 = 시계정상 && blwch_post_data[6] >= 1843200 ? blwch_post_data[6] : 48000000;
    blwch_post_data[0]=32; blwch_post_data[1]=0; blwch_post_data[2]=0x10005; blwch_post_data[3]=8; blwch_post_data[4]=0;
    blwch_post_data[5]=blwch_post_data[6]=blwch_post_data[7]=0;
    if (blwch_post() && blwch_post_data[4]==0x80000008u) 팔기억킬로바이트=blwch_post_data[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    peiriant_cofrestru(직렬장치 + 0x44) = 0x7ff;
    peiriant_cofrestru(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    peiriant_cofrestru(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    peiriant_cofrestru(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    peiriant_cofrestru(직렬장치 + 0x38) = 0;
    peiriant_cofrestru(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
peiriant_Word bwrdd_FTP(peiriant_Word Gweithrediad) { return (uint32_t)ftp_control((int)Gweithrediad); }
peiriant_Word bwrdd_Rhwydwaith_cyflwr(peiriant_Word cofnod_VALUE, peiriant_Word INDEX) { return 망상태읽기(cofnod_VALUE, INDEX); }
peiriant_Word bwrdd_Rhwydwaith_Gosodiadau(peiriant_Word Gweithrediad, peiriant_Word ADDRESS, peiriant_Word masgio_VALUE, peiriant_Word adwy_VALUE) { return (uint32_t)ffurfweddu_Rhwydwaith(Gweithrediad, ADDRESS, masgio_VALUE, adwy_VALUE); }
peiriant_Word 보드응답보내기(peiriant_Word ADDRESS, peiriant_Word trefn_VALUE) { return (uint32_t)응답시험시작(ADDRESS, trefn_VALUE); }
peiriant_Word 보드응답읽기(peiriant_Word cofnod_VALUE) { return (uint32_t)응답시험읽기(cofnod_VALUE); }
peiriant_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEX=0; INDEX<32; INDEX++) cau_Rhwydwaith(INDEX);
    for (unsigned INDEX=0; INDEX<4; INDEX++) bwrdd_rheolaeth_defnyddiwr(32+INDEX);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (peiriant_cofrestru(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    peiriant_cofrestru(0xfe100020ul)=0x5a000000u | (peiriant_cofrestru(0xfe100020ul)&~0xfffu) | 0x555;
    peiriant_cofrestru(0xfe100024ul)=0x5a000000u | 10;
    peiriant_cofrestru(0xfe10001cul)=0x5a000000u | (peiriant_cofrestru(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

peiriant_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 현재 크기를 읽는다. */
    const uint32_t ymholiad_VALUE[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(ymholiad_VALUE)/4; 순번++) blwch_post_data[순번] = ymholiad_VALUE[순번];
    if (blwch_post() && blwch_post_data[4] == 0x80000008u &&
        blwch_post_data[5] >= 640 && blwch_post_data[5] <= 1920 &&
        blwch_post_data[6] >= 480 && blwch_post_data[6] <= 1080) {
        요청너비 = blwch_post_data[5]; 요청높이 = blwch_post_data[6];
    }
    const uint32_t cais_HTTP[] = {
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
    for (size_t 순번 = 0; 순번 < sizeof(cais_HTTP)/4; 순번++) blwch_post_data[순번] = cais_HTTP[순번];
    // 위 메시지의 go_iawn_data 길이를 사용: 태그 추가 시 hyd_VALUE 불일치를 방지한다.
    blwch_post_data[0] = sizeof(cais_HTTP);
    if (!blwch_post()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 응답길이[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (blwch_post_data[응답들[순번]] != (0x80000000u | 응답길이[순번])) return 0;
    uint32_t Cefndir_VALUE = blwch_post_data[28] & 0x3fffffffu;
    uint32_t Maint = blwch_post_data[29];
    uint32_t 받은너비 = blwch_post_data[5], 받은높이 = blwch_post_data[6], RECEIVED_rhynglinellu = blwch_post_data[33];
    if (blwch_post_data[15] != 32 || blwch_post_data[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        blwch_post_data[10] < 받은너비 || blwch_post_data[11] < 받은높이 || blwch_post_data[23] || blwch_post_data[24] ||
        !Cefndir_VALUE || Cefndir_VALUE < 0x1000000 || (Cefndir_VALUE & 3) || RECEIVED_rhynglinellu < 받은너비 * 4 || (RECEIVED_rhynglinellu & 3) ||
        (uint64_t)RECEIVED_rhynglinellu * 받은높이 > Maint || (uint64_t)Cefndir_VALUE + Maint > 0x40000000u)
        return 0;
    bwrdd_Paratoi_lluniad((volatile uint32_t *)(uintptr_t)Cefndir_VALUE, 받은너비, 받은높이, RECEIVED_rhynglinellu);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 edefyn_VALUE. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } Cyd_destun;
static Cyd_destun 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int technoleg_gwybodaeth_Rhedeg[3] = {1, 0, 0};
static int 현재작업;
extern void Cyd_destun_newid(Cyd_destun *, Cyd_destun *);
extern void 자바작업(int32_t);
peiriant_Word bwrdd_atal(void) {
    network_poll();
    int 이전 = 현재작업, Nesaf_eitem = (이전 + 1) % 3;
    while (Nesaf_eitem != 이전 && !technoleg_gwybodaeth_Rhedeg[Nesaf_eitem]) Nesaf_eitem = (Nesaf_eitem + 1) % 3;
    if (Nesaf_eitem != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (technoleg_gwybodaeth_Rhedeg[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        현재작업 = Nesaf_eitem;
        Cyd_destun_newid(&작업문맥들[이전], &작업문맥들[Nesaf_eitem]);
    }
    return 0;
}
static void tasg_bwtio(void) {
    자바작업(현재작업);
    technoleg_gwybodaeth_Rhedeg[현재작업] = 0;
    bwrdd_atal();
    커널중단("finished task resumed");
}
peiriant_Word bwrdd_tasg_Creu(peiriant_Word dynodwr_VALUE) {
    if (dynodwr_VALUE < 1 || dynodwr_VALUE > 2 || technoleg_gwybodaeth_Rhedeg[dynodwr_VALUE]) return (uint32_t)-1;
    memset(&작업문맥들[dynodwr_VALUE], 0, sizeof(Cyd_destun));
    *(uint64_t *)쌓임공간들[dynodwr_VALUE - 1] = 0x6b6f726f7373746bull;
    작업문맥들[dynodwr_VALUE].저장값[11] = (uintptr_t)tasg_bwtio;
    작업문맥들[dynodwr_VALUE].저장값[12] = (uintptr_t)(쌓임공간들[dynodwr_VALUE - 1] + sizeof(쌓임공간들[0]));
    technoleg_gwybodaeth_Rhedeg[dynodwr_VALUE] = 1;
    return 0;
}
peiriant_Word bwrdd_tasg_cyflwr(peiriant_Word dynodwr_VALUE) { return dynodwr_VALUE < 3 ? technoleg_gwybodaeth_Rhedeg[dynodwr_VALUE] : (uint32_t)-1; }
extern peiriant_Word 미리번역기억조회(peiriant_Word);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
peiriant_Word bwrdd_ymholiad_system(peiriant_Word cofnod_VALUE, peiriant_Word INDEX) {
    if (cofnod_VALUE==0) return 팔기억킬로바이트;
    if (cofnod_VALUE==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (cofnod_VALUE==2 || cofnod_VALUE==3) return 미리번역기억조회(cofnod_VALUE==3);
    if (cofnod_VALUE==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (cofnod_VALUE==5) return 80*1024; /* Gweithredu_gorchymyn 공간 16 MiB + 네 세션 보관 공간. */
    if (cofnod_VALUE>=20) return 사용자상태읽기(cofnod_VALUE-20, INDEX);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[현재작업]; }
