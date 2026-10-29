#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "notandi.h"
#include "../Net_bunki/Net_bunki.h"
typedef uintptr_t vél_Word;
#define vél_skrá(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define pósthólf_slóð 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t klukka_COUNT(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t FREQUENCY;
static volatile uint32_t pósthólf_gögn[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *gögn_staða, int stafkóði, size_t vara_COUNT) { unsigned char *Áfram_OFFSET = gögn_staða; while (vara_COUNT--) *Áfram_OFFSET++ = stafkóði; return gögn_staða; }
void *memcpy(void *endastaður_gögn, const void *strengur_gögn, size_t vara_COUNT) { unsigned char *첫째값 = endastaður_gögn; const unsigned char *SECOND_VALUE = strengur_gögn; while (vara_COUNT--) *첫째값++ = *SECOND_VALUE++; return endastaður_gögn; }

static int pósthólf(void) {
    uint32_t 요청 = (uint32_t)(uintptr_t)pósthólf_gögn | 8;
    uint64_t Keyra_2 = klukka_COUNT();
    기억장벽();
    while (vél_skrá(pósthólf_slóð + 0x38) & 0x80000000u)
        if (klukka_COUNT() - Keyra_2 > FREQUENCY) return 0;
    vél_skrá(pósthólf_slóð + 0x20) = 요청;
    for (;;) {
        if (!(vél_skrá(pósthólf_slóð + 0x18) & 0x40000000u)) {
            uint32_t svara = vél_skrá(pósthólf_slóð);
            if (svara == 요청) { 기억장벽(); return pósthólf_gögn[1] == 0x80000000u; }
        }
        if (klukka_COUNT() - Keyra_2 > FREQUENCY) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Endastöð_bæti(unsigned);
extern int Endastöð_Í_bið(void);
extern void Endastöð_bendill(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../fjartengdur_VALUE/fjartengdur_VALUE.h"
static int 흐름목록;
static unsigned 직렬이전글자;
vél_Word 보드흐름설정(vél_Word 사용여부) { 흐름목록=사용여부!=0; return 0; }
vél_Word bretti_rás(vél_Word rás, vél_Word stafkóði) {
    if(흐름목록 && 자바셸출력((int32_t)rás,(int32_t)(stafkóði&255))) return 0;
    Endastöð_bæti(stafkóði&255);
    fjartengdur_úttak(stafkóði&255);
    if ((stafkóði&255)==10 && 직렬이전글자!=13) {
        while (vél_skrá(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        vél_skrá(직렬장치)=13;
    }
    직렬이전글자=stafkóði&255;
    while (vél_skrá(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    vél_skrá(직렬장치) = (uint32_t)stafkóði & 255;
    return 0;
}
vél_Word 보드글자쓰기(vél_Word stafkóði) { return bretti_rás(1,stafkóði); }
vél_Word 보드원시글자읽기(void) {
    int fjartengdur_stafur=원격입력();if(fjartengdur_stafur>=0)return fjartengdur_stafur;
    if (vél_skrá(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t VALUE = vél_skrá(직렬장치);
    if (VALUE & 0xf00) { vél_skrá(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return VALUE & 255;
}
vél_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char pakki_gögn[6];
    if(Endastöð_Í_bið())return (uint32_t)-4096;
    if(흐름목록){int32_t stafkóði=자바셸입력();if(stafkóði!=-3)return (uint32_t)stafkóði;}
    for(;;){
        int stafkóði=(int32_t)보드원시글자읽기();if(stafkóði<0)return (uint32_t)stafkóði;
        if(!꾸러미안쪽){if(stafkóði!=30)return stafkóði;꾸러미안쪽=1;사용량=0;continue;}
        pakki_gögn[사용량++]=stafkóði;if(사용량<6)continue;꾸러미안쪽=0;
        if(pakki_gögn[0]==1)Endastöð_bendill(pakki_gögn[1],pakki_gögn[2]+pakki_gögn[3]*256,pakki_gögn[4]+pakki_gögn[5]*256);
        if(pakki_gögn[0]==2)터미널바로가기키(pakki_gögn[1]);
        if(pakki_gögn[0]==3)터미널입력방식(pakki_gögn[1]);
        if(Endastöð_Í_bið())return (uint32_t)-4096;
    }
}
vél_Word 보드밀리초(void) { return (uint32_t)(klukka_COUNT() / (FREQUENCY / 1000)); }
vél_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *strengur_gögn) { while (*strengur_gögn) 보드글자쓰기((unsigned char)*strengur_gögn++); }
static void 직렬열여섯진출력(vél_Word vara_COUNT) { const char *열여섯진숫자 = "0123456789abcdef"; for (int strengur_gögn = 60; strengur_gögn >= 0; strengur_gögn -= 4) 보드글자쓰기(열여섯진숫자[(vara_COUNT >> strengur_gögn) & 15]); }
vél_Word bretti_Stopp(vél_Word staða_VALUE_e10195a1) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(staða_VALUE_e10195a1); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); bretti_Stopp(1); __builtin_unreachable(); }
void bretti_undantekning(vél_Word undantekning_staða, vél_Word skipun_staða, vél_Word ógilt_slóð) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(undantekning_staða);
    직렬글출력(" PC="); 직렬열여섯진출력(skipun_staða); 직렬글출력(" FAR="); 직렬열여섯진출력(ógilt_slóð);
    bretti_Stopp(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    pósthólf_gögn[0]=32;pósthólf_gögn[1]=0;pósthólf_gögn[2]=0x10004;pósthólf_gögn[3]=8;pósthólf_gögn[4]=0;
    pósthólf_gögn[5]=pósthólf_gögn[6]=pósthólf_gögn[7]=0;
    return pósthólf()&&pósthólf_gögn[4]==0x80000008u&&(pósthólf_gögn[5]||pósthólf_gögn[6]);
}
int bretti_vél_slóð(unsigned char *slóð) {
    pósthólf_gögn[0]=32;pósthólf_gögn[1]=0;pósthólf_gögn[2]=0x10003;pósthólf_gögn[3]=8;pósthólf_gögn[4]=0;
    pósthólf_gögn[5]=pósthólf_gögn[6]=pósthólf_gögn[7]=0;
    if(!pósthólf()||(pósthólf_gögn[4]&0x80000000u)==0||(pósthólf_gögn[4]&0xffff)!=6)return 0;
    const unsigned char *gögn=(const unsigned char*)&pósthólf_gögn[5];unsigned SUM_VALUE=0;
    for(unsigned 순번=0;순번<6;순번++){slóð[순번]=gögn[순번];SUM_VALUE|=gögn[순번];}return SUM_VALUE&&!(slóð[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    vél_skrá(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    vél_skrá(범용입출력 + 4) = (vél_skrá(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    vél_skrá(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. bilun_VALUE 시 config.txt의 48MHz를 사용한다.
    pósthólf_gögn[0] = 36; pósthólf_gögn[1] = 0; pósthólf_gögn[2] = 0x38002; pósthólf_gögn[3] = 12;
    pósthólf_gögn[4] = 0; pósthólf_gögn[5] = 2; pósthólf_gögn[6] = 48000000; pósthólf_gögn[7] = 0; pósthólf_gögn[8] = 0;
    int 시계정상 = pósthólf();
    uint32_t 속도 = 시계정상 && pósthólf_gögn[6] >= 1843200 ? pósthólf_gögn[6] : 48000000;
    pósthólf_gögn[0]=32; pósthólf_gögn[1]=0; pósthólf_gögn[2]=0x10005; pósthólf_gögn[3]=8; pósthólf_gögn[4]=0;
    pósthólf_gögn[5]=pósthólf_gögn[6]=pósthólf_gögn[7]=0;
    if (pósthólf() && pósthólf_gögn[4]==0x80000008u) 팔기억킬로바이트=pósthólf_gögn[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    vél_skrá(직렬장치 + 0x44) = 0x7ff;
    vél_skrá(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    vél_skrá(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    vél_skrá(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    vél_skrá(직렬장치 + 0x38) = 0;
    vél_skrá(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
vél_Word bretti_FTP(vél_Word Aðgerð) { return (uint32_t)ftp_control((int)Aðgerð); }
vél_Word bretti_Net_staða(vél_Word færsla_VALUE, vél_Word INDEX) { return 망상태읽기(færsla_VALUE, INDEX); }
vél_Word bretti_Net_Stillingar(vél_Word Aðgerð, vél_Word slóð, vél_Word sía_VALUE_3fef50ae, vél_Word gátt_VALUE_cfee51e8) { return (uint32_t)grunnstilla_Net(Aðgerð, slóð, sía_VALUE_3fef50ae, gátt_VALUE_cfee51e8); }
vél_Word 보드응답보내기(vél_Word slóð, vél_Word röð_VALUE) { return (uint32_t)응답시험시작(slóð, röð_VALUE); }
vél_Word 보드응답읽기(vél_Word færsla_VALUE) { return (uint32_t)응답시험읽기(færsla_VALUE); }
vél_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEX=0; INDEX<32; INDEX++) loka_Net(INDEX);
    for (unsigned INDEX=0; INDEX<4; INDEX++) bretti_notandastjórn(32+INDEX);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (vél_skrá(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    vél_skrá(0xfe100020ul)=0x5a000000u | (vél_skrá(0xfe100020ul)&~0xfffu) | 0x555;
    vél_skrá(0xfe100024ul)=0x5a000000u | 10;
    vél_skrá(0xfe10001cul)=0x5a000000u | (vél_skrá(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

vél_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 현재 크기를 읽는다. */
    const uint32_t fyrirspurn_VALUE[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(fyrirspurn_VALUE)/4; 순번++) pósthólf_gögn[순번] = fyrirspurn_VALUE[순번];
    if (pósthólf() && pósthólf_gögn[4] == 0x80000008u &&
        pósthólf_gögn[5] >= 640 && pósthólf_gögn[5] <= 1920 &&
        pósthólf_gögn[6] >= 480 && pósthólf_gögn[6] <= 1080) {
        요청너비 = pósthólf_gögn[5]; 요청높이 = pósthólf_gögn[6];
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
    for (size_t 순번 = 0; 순번 < sizeof(요청)/4; 순번++) pósthólf_gögn[순번] = 요청[순번];
    // 위 메시지의 raun_gögn 길이를 사용: 태그 추가 시 lengd_VALUE 불일치를 방지한다.
    pósthólf_gögn[0] = sizeof(요청);
    if (!pósthólf()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 응답길이[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (pósthólf_gögn[응답들[순번]] != (0x80000000u | 응답길이[순번])) return 0;
    uint32_t veggfóður_VALUE = pósthólf_gögn[28] & 0x3fffffffu;
    uint32_t Stærð = pósthólf_gögn[29];
    uint32_t 받은너비 = pósthólf_gögn[5], 받은높이 = pósthólf_gögn[6], RECEIVED_línubil = pósthólf_gögn[33];
    if (pósthólf_gögn[15] != 32 || pósthólf_gögn[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        pósthólf_gögn[10] < 받은너비 || pósthólf_gögn[11] < 받은높이 || pósthólf_gögn[23] || pósthólf_gögn[24] ||
        !veggfóður_VALUE || veggfóður_VALUE < 0x1000000 || (veggfóður_VALUE & 3) || RECEIVED_línubil < 받은너비 * 4 || (RECEIVED_línubil & 3) ||
        (uint64_t)RECEIVED_línubil * 받은높이 > Stærð || (uint64_t)veggfóður_VALUE + Stærð > 0x40000000u)
        return 0;
    bretti_Undirbúa_teikning((volatile uint32_t *)(uintptr_t)veggfóður_VALUE, 받은너비, 받은높이, RECEIVED_línubil);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 þráður_VALUE. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } Samhengi;
static Samhengi 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int upplýsingatækni_Hlaup[3] = {1, 0, 0};
static int 현재작업;
extern void Samhengi_SWITCH(Samhengi *, Samhengi *);
extern void 자바작업(int32_t);
vél_Word bretti_YIELD(void) {
    network_poll();
    int 이전 = 현재작업, Áfram_vara = (이전 + 1) % 3;
    while (Áfram_vara != 이전 && !upplýsingatækni_Hlaup[Áfram_vara]) Áfram_vara = (Áfram_vara + 1) % 3;
    if (Áfram_vara != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (upplýsingatækni_Hlaup[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        현재작업 = Áfram_vara;
        Samhengi_SWITCH(&작업문맥들[이전], &작업문맥들[Áfram_vara]);
    }
    return 0;
}
static void verk_ræsa(void) {
    자바작업(현재작업);
    upplýsingatækni_Hlaup[현재작업] = 0;
    bretti_YIELD();
    커널중단("finished task resumed");
}
vél_Word bretti_verk_stofna(vél_Word auðkenni_VALUE) {
    if (auðkenni_VALUE < 1 || auðkenni_VALUE > 2 || upplýsingatækni_Hlaup[auðkenni_VALUE]) return (uint32_t)-1;
    memset(&작업문맥들[auðkenni_VALUE], 0, sizeof(Samhengi));
    *(uint64_t *)쌓임공간들[auðkenni_VALUE - 1] = 0x6b6f726f7373746bull;
    작업문맥들[auðkenni_VALUE].저장값[11] = (uintptr_t)verk_ræsa;
    작업문맥들[auðkenni_VALUE].저장값[12] = (uintptr_t)(쌓임공간들[auðkenni_VALUE - 1] + sizeof(쌓임공간들[0]));
    upplýsingatækni_Hlaup[auðkenni_VALUE] = 1;
    return 0;
}
vél_Word bretti_verk_staða(vél_Word auðkenni_VALUE) { return auðkenni_VALUE < 3 ? upplýsingatækni_Hlaup[auðkenni_VALUE] : (uint32_t)-1; }
extern vél_Word AOT_Minni_LOOKUP(vél_Word);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
vél_Word bretti_fyrirspurn_kerfi(vél_Word færsla_VALUE, vél_Word INDEX) {
    if (færsla_VALUE==0) return 팔기억킬로바이트;
    if (færsla_VALUE==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (færsla_VALUE==2 || færsla_VALUE==3) return AOT_Minni_LOOKUP(færsla_VALUE==3);
    if (færsla_VALUE==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (færsla_VALUE==5) return 80*1024; /* keyra_skipun 공간 16 MiB + 네 세션 보관 공간. */
    if (færsla_VALUE>=20) return 사용자상태읽기(færsla_VALUE-20, INDEX);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[현재작업]; }
