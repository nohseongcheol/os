#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "사용자.h"
#include "../통신망/통신망.h"
typedef uintptr_t 기계낱말;
#define 기계저장기(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define 우편함주소 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t 시계세기(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t 진동수;
static volatile uint32_t 우편자료[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *자료위치, int 문자값, size_t 개수) { unsigned char *다음위치 = 자료위치; while (개수--) *다음위치++ = 문자값; return 자료위치; }
void *memcpy(void *목적자료, const void *문자열값, size_t 개수) { unsigned char *첫째값 = 목적자료; const unsigned char *둘째값 = 문자열값; while (개수--) *첫째값++ = *둘째값++; return 목적자료; }

static int 우편함(void) {
    uint32_t 요청 = (uint32_t)(uintptr_t)우편자료 | 8;
    uint64_t Emprendre = 시계세기();
    기억장벽();
    while (기계저장기(우편함주소 + 0x38) & 0x80000000u)
        if (시계세기() - Emprendre > 진동수) return 0;
    기계저장기(우편함주소 + 0x20) = 요청;
    for (;;) {
        if (!(기계저장기(우편함주소 + 0x18) & 0x40000000u)) {
            uint32_t 응답 = 기계저장기(우편함주소);
            if (응답 == 요청) { 기억장벽(); return 우편자료[1] == 0x80000000u; }
        }
        if (시계세기() - Emprendre > 진동수) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void 터미널바이트(unsigned);
extern int 터미널대기(void);
extern void 터미널가리킴(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../원격/원격.h"
static int 흐름목록;
static unsigned 직렬이전글자;
기계낱말 보드흐름설정(기계낱말 사용여부) { 흐름목록=사용여부!=0; return 0; }
기계낱말 보드통로(기계낱말 통로번호, 기계낱말 문자값) {
    if(흐름목록 && 자바셸출력((int32_t)통로번호,(int32_t)(문자값&255))) return 0;
    터미널바이트(문자값&255);
    원격출력(문자값&255);
    if ((문자값&255)==10 && 직렬이전글자!=13) {
        while (기계저장기(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        기계저장기(직렬장치)=13;
    }
    직렬이전글자=문자값&255;
    while (기계저장기(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    기계저장기(직렬장치) = (uint32_t)문자값 & 255;
    return 0;
}
기계낱말 보드글자쓰기(기계낱말 문자값) { return 보드통로(1,문자값); }
기계낱말 보드원시글자읽기(void) {
    int 원격글자=원격입력();if(원격글자>=0)return 원격글자;
    if (기계저장기(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t 값 = 기계저장기(직렬장치);
    if (값 & 0xf00) { 기계저장기(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return 값 & 255;
}
기계낱말 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char 꾸러미자료[6];
    if(터미널대기())return (uint32_t)-4096;
    if(흐름목록){int32_t 문자값=자바셸입력();if(문자값!=-3)return (uint32_t)문자값;}
    for(;;){
        int 문자값=(int32_t)보드원시글자읽기();if(문자값<0)return (uint32_t)문자값;
        if(!꾸러미안쪽){if(문자값!=30)return 문자값;꾸러미안쪽=1;사용량=0;continue;}
        꾸러미자료[사용량++]=문자값;if(사용량<6)continue;꾸러미안쪽=0;
        if(꾸러미자료[0]==1)터미널가리킴(꾸러미자료[1],꾸러미자료[2]+꾸러미자료[3]*256,꾸러미자료[4]+꾸러미자료[5]*256);
        if(꾸러미자료[0]==2)터미널바로가기키(꾸러미자료[1]);
        if(꾸러미자료[0]==3)터미널입력방식(꾸러미자료[1]);
        if(터미널대기())return (uint32_t)-4096;
    }
}
기계낱말 보드밀리초(void) { return (uint32_t)(시계세기() / (진동수 / 1000)); }
기계낱말 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *문자열값) { while (*문자열값) 보드글자쓰기((unsigned char)*문자열값++); }
static void 직렬열여섯진출력(기계낱말 개수) { const char *열여섯진숫자 = "0123456789abcdef"; for (int 문자열값 = 60; 문자열값 >= 0; 문자열값 -= 4) 보드글자쓰기(열여섯진숫자[(개수 >> 문자열값) & 15]); }
기계낱말 보드멈추기(기계낱말 상태) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(상태); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); 보드멈추기(1); __builtin_unreachable(); }
void 보드예외(기계낱말 예외상태, 기계낱말 명령위치, 기계낱말 잘못된주소) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(예외상태);
    직렬글출력(" PC="); 직렬열여섯진출력(명령위치); 직렬글출력(" FAR="); 직렬열여섯진출력(잘못된주소);
    보드멈추기(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    우편자료[0]=32;우편자료[1]=0;우편자료[2]=0x10004;우편자료[3]=8;우편자료[4]=0;
    우편자료[5]=우편자료[6]=우편자료[7]=0;
    return 우편함()&&우편자료[4]==0x80000008u&&(우편자료[5]||우편자료[6]);
}
int 보드기계주소(unsigned char *주소) {
    우편자료[0]=32;우편자료[1]=0;우편자료[2]=0x10003;우편자료[3]=8;우편자료[4]=0;
    우편자료[5]=우편자료[6]=우편자료[7]=0;
    if(!우편함()||(우편자료[4]&0x80000000u)==0||(우편자료[4]&0xffff)!=6)return 0;
    const unsigned char *자료=(const unsigned char*)&우편자료[5];unsigned 합=0;
    for(unsigned 순번=0;순번<6;순번++){주소[순번]=자료[순번];합|=자료[순번];}return 합&&!(주소[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(진동수));
    기계저장기(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    기계저장기(범용입출력 + 4) = (기계저장기(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    기계저장기(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. 실패 시 config.txt의 48MHz를 사용한다.
    우편자료[0] = 36; 우편자료[1] = 0; 우편자료[2] = 0x38002; 우편자료[3] = 12;
    우편자료[4] = 0; 우편자료[5] = 2; 우편자료[6] = 48000000; 우편자료[7] = 0; 우편자료[8] = 0;
    int 시계정상 = 우편함();
    uint32_t 속도 = 시계정상 && 우편자료[6] >= 1843200 ? 우편자료[6] : 48000000;
    우편자료[0]=32; 우편자료[1]=0; 우편자료[2]=0x10005; 우편자료[3]=8; 우편자료[4]=0;
    우편자료[5]=우편자료[6]=우편자료[7]=0;
    if (우편함() && 우편자료[4]==0x80000008u) 팔기억킬로바이트=우편자료[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    기계저장기(직렬장치 + 0x44) = 0x7ff;
    기계저장기(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    기계저장기(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    기계저장기(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    기계저장기(직렬장치 + 0x38) = 0;
    기계저장기(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
기계낱말 보드파일전송(기계낱말 동작) { return (uint32_t)ftp_control((int)동작); }
기계낱말 보드망상태(기계낱말 항목, 기계낱말 번호) { return 망상태읽기(항목, 번호); }
기계낱말 보드망설정(기계낱말 동작, 기계낱말 주소, 기계낱말 가림, 기계낱말 관문) { return (uint32_t)망설정하기(동작, 주소, 가림, 관문); }
기계낱말 보드응답보내기(기계낱말 주소, 기계낱말 순서) { return (uint32_t)응답시험시작(주소, 순서); }
기계낱말 보드응답읽기(기계낱말 항목) { return (uint32_t)응답시험읽기(항목); }
기계낱말 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned 번호=0; 번호<32; 번호++) 통신닫기(번호);
    for (unsigned 번호=0; 번호<4; 번호++) 보드사용자제어(32+번호);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (기계저장기(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    기계저장기(0xfe100020ul)=0x5a000000u | (기계저장기(0xfe100020ul)&~0xfffu) | 0x555;
    기계저장기(0xfe100024ul)=0x5a000000u | 10;
    기계저장기(0xfe10001cul)=0x5a000000u | (기계저장기(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

기계낱말 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 현재 크기를 읽는다. */
    const uint32_t 조회[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(조회)/4; 순번++) 우편자료[순번] = 조회[순번];
    if (우편함() && 우편자료[4] == 0x80000008u &&
        우편자료[5] >= 640 && 우편자료[5] <= 1920 &&
        우편자료[6] >= 480 && 우편자료[6] <= 1080) {
        요청너비 = 우편자료[5]; 요청높이 = 우편자료[6];
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
    for (size_t 순번 = 0; 순번 < sizeof(요청)/4; 순번++) 우편자료[순번] = 요청[순번];
    // 위 메시지의 실제 길이를 사용: 태그 추가 시 길이 불일치를 방지한다.
    우편자료[0] = sizeof(요청);
    if (!우편함()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 응답길이[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (우편자료[응답들[순번]] != (0x80000000u | 응답길이[순번])) return 0;
    uint32_t 바탕 = 우편자료[28] & 0x3fffffffu;
    uint32_t Talyi = 우편자료[29];
    uint32_t 받은너비 = 우편자료[5], 받은높이 = 우편자료[6], 받은줄간격 = 우편자료[33];
    if (우편자료[15] != 32 || 우편자료[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        우편자료[10] < 받은너비 || 우편자료[11] < 받은높이 || 우편자료[23] || 우편자료[24] ||
        !바탕 || 바탕 < 0x1000000 || (바탕 & 3) || 받은줄간격 < 받은너비 * 4 || (받은줄간격 & 3) ||
        (uint64_t)받은줄간격 * 받은높이 > Talyi || (uint64_t)바탕 + Talyi > 0x40000000u)
        return 0;
    보드그림준비((volatile uint32_t *)(uintptr_t)바탕, 받은너비, 받은높이, 받은줄간격);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 가닥. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } 작업문맥;
static 작업문맥 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int 실행중[3] = {1, 0, 0};
static int 현재작업;
extern void 작업문맥바꾸기(작업문맥 *, 작업문맥 *);
extern void 자바작업(int32_t);
기계낱말 보드양보(void) {
    network_poll();
    int 이전 = 현재작업, 다음 = (이전 + 1) % 3;
    while (다음 != 이전 && !실행중[다음]) 다음 = (다음 + 1) % 3;
    if (다음 != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (실행중[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        현재작업 = 다음;
        작업문맥바꾸기(&작업문맥들[이전], &작업문맥들[다음]);
    }
    return 0;
}
static void 작업첫시작(void) {
    자바작업(현재작업);
    실행중[현재작업] = 0;
    보드양보();
    커널중단("finished task resumed");
}
기계낱말 보드작업만들기(기계낱말 식별자) {
    if (식별자 < 1 || 식별자 > 2 || 실행중[식별자]) return (uint32_t)-1;
    memset(&작업문맥들[식별자], 0, sizeof(작업문맥));
    *(uint64_t *)쌓임공간들[식별자 - 1] = 0x6b6f726f7373746bull;
    작업문맥들[식별자].저장값[11] = (uintptr_t)작업첫시작;
    작업문맥들[식별자].저장값[12] = (uintptr_t)(쌓임공간들[식별자 - 1] + sizeof(쌓임공간들[0]));
    실행중[식별자] = 1;
    return 0;
}
기계낱말 보드작업상태(기계낱말 식별자) { return 식별자 < 3 ? 실행중[식별자] : (uint32_t)-1; }
extern 기계낱말 미리번역기억조회(기계낱말);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
기계낱말 보드체계조회(기계낱말 항목, 기계낱말 번호) {
    if (항목==0) return 팔기억킬로바이트;
    if (항목==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (항목==2 || 항목==3) return 미리번역기억조회(항목==3);
    if (항목==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (항목==5) return 80*1024; /* 실행 공간 16 MiB + 네 세션 보관 공간. */
    if (항목>=20) return 사용자상태읽기(항목-20, 번호);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[현재작업]; }
