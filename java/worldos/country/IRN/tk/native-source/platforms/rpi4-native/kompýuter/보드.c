#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "ulanyjy.h"
#include "../Tor_Desse/Tor_Desse.h"
typedef uintptr_t kompýuter_Söz;
#define 기계저장기(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define poçta_gutusy_salgy 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t 시계세기(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t 진동수;
static volatile uint32_t poçta_gutusy_maglumat[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *자료위치, int nyşanyň_kody, size_t 개수) { unsigned char *다음위치 = 자료위치; while (개수--) *다음위치++ = nyşanyň_kody; return 자료위치; }
void *memcpy(void *barylmaly_ýer_maglumat, const void *setir_maglumat, size_t 개수) { unsigned char *첫째값 = barylmaly_ýer_maglumat; const unsigned char *둘째값 = setir_maglumat; while (개수--) *첫째값++ = *둘째값++; return barylmaly_ýer_maglumat; }

static int poçta_gutusy(void) {
    uint32_t 요청 = (uint32_t)(uintptr_t)poçta_gutusy_maglumat | 8;
    uint64_t Bitir = 시계세기();
    기억장벽();
    while (기계저장기(poçta_gutusy_salgy + 0x38) & 0x80000000u)
        if (시계세기() - Bitir > 진동수) return 0;
    기계저장기(poçta_gutusy_salgy + 0x20) = 요청;
    for (;;) {
        if (!(기계저장기(poçta_gutusy_salgy + 0x18) & 0x40000000u)) {
            uint32_t jogap_bermek = 기계저장기(poçta_gutusy_salgy);
            if (jogap_bermek == 요청) { 기억장벽(); return poçta_gutusy_maglumat[1] == 0x80000000u; }
        }
        if (시계세기() - Bitir > 진동수) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void 터미널바이트(unsigned);
extern int 터미널대기(void);
extern void 터미널가리킴(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../uzakdan_baha/uzakdan_baha.h"
static int 흐름목록;
static unsigned 직렬이전글자;
kompýuter_Söz 보드흐름설정(kompýuter_Söz 사용여부) { 흐름목록=사용여부!=0; return 0; }
kompýuter_Söz 보드통로(kompýuter_Söz kanal, kompýuter_Söz nyşanyň_kody) {
    if(흐름목록 && 자바셸출력((int32_t)kanal,(int32_t)(nyşanyň_kody&255))) return 0;
    터미널바이트(nyşanyň_kody&255);
    원격출력(nyşanyň_kody&255);
    if ((nyşanyň_kody&255)==10 && 직렬이전글자!=13) {
        while (기계저장기(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        기계저장기(직렬장치)=13;
    }
    직렬이전글자=nyşanyň_kody&255;
    while (기계저장기(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    기계저장기(직렬장치) = (uint32_t)nyşanyň_kody & 255;
    return 0;
}
kompýuter_Söz 보드글자쓰기(kompýuter_Söz nyşanyň_kody) { return 보드통로(1,nyşanyň_kody); }
kompýuter_Söz 보드원시글자읽기(void) {
    int uzakdan_nyşan=원격입력();if(uzakdan_nyşan>=0)return uzakdan_nyşan;
    if (기계저장기(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t baha = 기계저장기(직렬장치);
    if (baha & 0xf00) { 기계저장기(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return baha & 255;
}
kompýuter_Söz 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char 꾸러미자료[6];
    if(터미널대기())return (uint32_t)-4096;
    if(흐름목록){int32_t nyşanyň_kody=자바셸입력();if(nyşanyň_kody!=-3)return (uint32_t)nyşanyň_kody;}
    for(;;){
        int nyşanyň_kody=(int32_t)보드원시글자읽기();if(nyşanyň_kody<0)return (uint32_t)nyşanyň_kody;
        if(!꾸러미안쪽){if(nyşanyň_kody!=30)return nyşanyň_kody;꾸러미안쪽=1;사용량=0;continue;}
        꾸러미자료[사용량++]=nyşanyň_kody;if(사용량<6)continue;꾸러미안쪽=0;
        if(꾸러미자료[0]==1)터미널가리킴(꾸러미자료[1],꾸러미자료[2]+꾸러미자료[3]*256,꾸러미자료[4]+꾸러미자료[5]*256);
        if(꾸러미자료[0]==2)터미널바로가기키(꾸러미자료[1]);
        if(꾸러미자료[0]==3)터미널입력방식(꾸러미자료[1]);
        if(터미널대기())return (uint32_t)-4096;
    }
}
kompýuter_Söz 보드밀리초(void) { return (uint32_t)(시계세기() / (진동수 / 1000)); }
kompýuter_Söz 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *setir_maglumat) { while (*setir_maglumat) 보드글자쓰기((unsigned char)*setir_maglumat++); }
static void 직렬열여섯진출력(kompýuter_Söz 개수) { const char *열여섯진숫자 = "0123456789abcdef"; for (int setir_maglumat = 60; setir_maglumat >= 0; setir_maglumat -= 4) 보드글자쓰기(열여섯진숫자[(개수 >> setir_maglumat) & 15]); }
kompýuter_Söz 보드멈추기(kompýuter_Söz ýagdaý_baha) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(ýagdaý_baha); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); 보드멈추기(1); __builtin_unreachable(); }
void 보드예외(kompýuter_Söz 예외상태, kompýuter_Söz 명령위치, kompýuter_Söz nädogry_salgy) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(예외상태);
    직렬글출력(" PC="); 직렬열여섯진출력(명령위치); 직렬글출력(" FAR="); 직렬열여섯진출력(nädogry_salgy);
    보드멈추기(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    poçta_gutusy_maglumat[0]=32;poçta_gutusy_maglumat[1]=0;poçta_gutusy_maglumat[2]=0x10004;poçta_gutusy_maglumat[3]=8;poçta_gutusy_maglumat[4]=0;
    poçta_gutusy_maglumat[5]=poçta_gutusy_maglumat[6]=poçta_gutusy_maglumat[7]=0;
    return poçta_gutusy()&&poçta_gutusy_maglumat[4]==0x80000008u&&(poçta_gutusy_maglumat[5]||poçta_gutusy_maglumat[6]);
}
int 보드기계주소(unsigned char *salgy) {
    poçta_gutusy_maglumat[0]=32;poçta_gutusy_maglumat[1]=0;poçta_gutusy_maglumat[2]=0x10003;poçta_gutusy_maglumat[3]=8;poçta_gutusy_maglumat[4]=0;
    poçta_gutusy_maglumat[5]=poçta_gutusy_maglumat[6]=poçta_gutusy_maglumat[7]=0;
    if(!poçta_gutusy()||(poçta_gutusy_maglumat[4]&0x80000000u)==0||(poçta_gutusy_maglumat[4]&0xffff)!=6)return 0;
    const unsigned char *maglumat=(const unsigned char*)&poçta_gutusy_maglumat[5];unsigned 합=0;
    for(unsigned 순번=0;순번<6;순번++){salgy[순번]=maglumat[순번];합|=maglumat[순번];}return 합&&!(salgy[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(진동수));
    기계저장기(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    기계저장기(범용입출력 + 4) = (기계저장기(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    기계저장기(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. näsazlyk_baha 시 config.txt의 48MHz를 사용한다.
    poçta_gutusy_maglumat[0] = 36; poçta_gutusy_maglumat[1] = 0; poçta_gutusy_maglumat[2] = 0x38002; poçta_gutusy_maglumat[3] = 12;
    poçta_gutusy_maglumat[4] = 0; poçta_gutusy_maglumat[5] = 2; poçta_gutusy_maglumat[6] = 48000000; poçta_gutusy_maglumat[7] = 0; poçta_gutusy_maglumat[8] = 0;
    int 시계정상 = poçta_gutusy();
    uint32_t 속도 = 시계정상 && poçta_gutusy_maglumat[6] >= 1843200 ? poçta_gutusy_maglumat[6] : 48000000;
    poçta_gutusy_maglumat[0]=32; poçta_gutusy_maglumat[1]=0; poçta_gutusy_maglumat[2]=0x10005; poçta_gutusy_maglumat[3]=8; poçta_gutusy_maglumat[4]=0;
    poçta_gutusy_maglumat[5]=poçta_gutusy_maglumat[6]=poçta_gutusy_maglumat[7]=0;
    if (poçta_gutusy() && poçta_gutusy_maglumat[4]==0x80000008u) 팔기억킬로바이트=poçta_gutusy_maglumat[6]/1024;
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
kompýuter_Söz 보드파일전송(kompýuter_Söz iş) { return (uint32_t)ftp_control((int)iş); }
kompýuter_Söz 보드망상태(kompýuter_Söz girizmeklik_baha, kompýuter_Söz indeks) { return 망상태읽기(girizmeklik_baha, indeks); }
kompýuter_Söz 보드망설정(kompýuter_Söz iş, kompýuter_Söz salgy, kompýuter_Söz örtük_baha, kompýuter_Söz şlýuz_baha) { return (uint32_t)düz_Tor(iş, salgy, örtük_baha, şlýuz_baha); }
kompýuter_Söz 보드응답보내기(kompýuter_Söz salgy, kompýuter_Söz tertip_baha) { return (uint32_t)응답시험시작(salgy, tertip_baha); }
kompýuter_Söz 보드응답읽기(kompýuter_Söz girizmeklik_baha) { return (uint32_t)응답시험읽기(girizmeklik_baha); }
kompýuter_Söz 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned indeks=0; indeks<32; indeks++) ýap_Tor(indeks);
    for (unsigned indeks=0; indeks<4; indeks++) 보드사용자제어(32+indeks);
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

kompýuter_Söz 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 현재 크기를 읽는다. */
    const uint32_t talap_baha[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(talap_baha)/4; 순번++) poçta_gutusy_maglumat[순번] = talap_baha[순번];
    if (poçta_gutusy() && poçta_gutusy_maglumat[4] == 0x80000008u &&
        poçta_gutusy_maglumat[5] >= 640 && poçta_gutusy_maglumat[5] <= 1920 &&
        poçta_gutusy_maglumat[6] >= 480 && poçta_gutusy_maglumat[6] <= 1080) {
        요청너비 = poçta_gutusy_maglumat[5]; 요청높이 = poçta_gutusy_maglumat[6];
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
    for (size_t 순번 = 0; 순번 < sizeof(요청)/4; 순번++) poçta_gutusy_maglumat[순번] = 요청[순번];
    // 위 메시지의 hakyky_maglumat 길이를 사용: 태그 추가 시 dowamlylyk_baha 불일치를 방지한다.
    poçta_gutusy_maglumat[0] = sizeof(요청);
    if (!poçta_gutusy()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 응답길이[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (poçta_gutusy_maglumat[응답들[순번]] != (0x80000000u | 응답길이[순번])) return 0;
    uint32_t Fon_baha = poçta_gutusy_maglumat[28] & 0x3fffffffu;
    uint32_t Ululyk = poçta_gutusy_maglumat[29];
    uint32_t 받은너비 = poçta_gutusy_maglumat[5], 받은높이 = poçta_gutusy_maglumat[6], 받은줄간격 = poçta_gutusy_maglumat[33];
    if (poçta_gutusy_maglumat[15] != 32 || poçta_gutusy_maglumat[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        poçta_gutusy_maglumat[10] < 받은너비 || poçta_gutusy_maglumat[11] < 받은높이 || poçta_gutusy_maglumat[23] || poçta_gutusy_maglumat[24] ||
        !Fon_baha || Fon_baha < 0x1000000 || (Fon_baha & 3) || 받은줄간격 < 받은너비 * 4 || (받은줄간격 & 3) ||
        (uint64_t)받은줄간격 * 받은높이 > Ululyk || (uint64_t)Fon_baha + Ululyk > 0x40000000u)
        return 0;
    보드그림준비((volatile uint32_t *)(uintptr_t)Fon_baha, 받은너비, 받은높이, 받은줄간격);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 akym_baha. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } Kontekst;
static Kontekst 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int 실행중[3] = {1, 0, 0};
static int 현재작업;
extern void Kontekst_calşyr(Kontekst *, Kontekst *);
extern void 자바작업(int32_t);
kompýuter_Söz 보드양보(void) {
    network_poll();
    int 이전 = 현재작업, 다음 = (이전 + 1) % 3;
    while (다음 != 이전 && !실행중[다음]) 다음 = (다음 + 1) % 3;
    if (다음 != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (실행중[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        현재작업 = 다음;
        Kontekst_calşyr(&작업문맥들[이전], &작업문맥들[다음]);
    }
    return 0;
}
static void tabşyryk_başlangyç(void) {
    자바작업(현재작업);
    실행중[현재작업] = 0;
    보드양보();
    커널중단("finished task resumed");
}
kompýuter_Söz 보드작업만들기(kompýuter_Söz tanaýjy_baha) {
    if (tanaýjy_baha < 1 || tanaýjy_baha > 2 || 실행중[tanaýjy_baha]) return (uint32_t)-1;
    memset(&작업문맥들[tanaýjy_baha], 0, sizeof(Kontekst));
    *(uint64_t *)쌓임공간들[tanaýjy_baha - 1] = 0x6b6f726f7373746bull;
    작업문맥들[tanaýjy_baha].저장값[11] = (uintptr_t)tabşyryk_başlangyç;
    작업문맥들[tanaýjy_baha].저장값[12] = (uintptr_t)(쌓임공간들[tanaýjy_baha - 1] + sizeof(쌓임공간들[0]));
    실행중[tanaýjy_baha] = 1;
    return 0;
}
kompýuter_Söz 보드작업상태(kompýuter_Söz tanaýjy_baha) { return tanaýjy_baha < 3 ? 실행중[tanaýjy_baha] : (uint32_t)-1; }
extern kompýuter_Söz 미리번역기억조회(kompýuter_Söz);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
kompýuter_Söz 보드체계조회(kompýuter_Söz girizmeklik_baha, kompýuter_Söz indeks) {
    if (girizmeklik_baha==0) return 팔기억킬로바이트;
    if (girizmeklik_baha==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (girizmeklik_baha==2 || girizmeklik_baha==3) return 미리번역기억조회(girizmeklik_baha==3);
    if (girizmeklik_baha==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (girizmeklik_baha==5) return 80*1024; /* ýerine_ýetir_buýruk 공간 16 MiB + 네 세션 보관 공간. */
    if (girizmeklik_baha>=20) return 사용자상태읽기(girizmeklik_baha-20, indeks);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[현재작업]; }
