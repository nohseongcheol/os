#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "aṣàmúlò.h"
#include "../Alásopọ̀_kójọ/Alásopọ̀_kójọ.h"
typedef uintptr_t maṣíìnì_Ọ̀rọ̀;
#define maṣíìnì_forúkọsílẹ̀(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define àpótì_méèlì_àdírẹ́ẹ̀sì 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t 시계세기(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t 진동수;
static volatile uint32_t àpótì_méèlì_détà[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *자료위치, int kóòdù_ẹyọ_ọ̀rọ̀, size_t 개수) { unsigned char *다음위치 = 자료위치; while (개수--) *다음위치++ = kóòdù_ẹyọ_ọ̀rọ̀; return 자료위치; }
void *memcpy(void *èbúté_détà, const void *fọ́nrán_détà, size_t 개수) { unsigned char *첫째값 = èbúté_détà; const unsigned char *둘째값 = fọ́nrán_détà; while (개수--) *첫째값++ = *둘째값++; return èbúté_détà; }

static int àpótì_méèlì(void) {
    uint32_t 요청 = (uint32_t)(uintptr_t)àpótì_méèlì_détà | 8;
    uint64_t Rọ́ọ̀nù = 시계세기();
    기억장벽();
    while (maṣíìnì_forúkọsílẹ̀(àpótì_méèlì_àdírẹ́ẹ̀sì + 0x38) & 0x80000000u)
        if (시계세기() - Rọ́ọ̀nù > 진동수) return 0;
    maṣíìnì_forúkọsílẹ̀(àpótì_méèlì_àdírẹ́ẹ̀sì + 0x20) = 요청;
    for (;;) {
        if (!(maṣíìnì_forúkọsílẹ̀(àpótì_méèlì_àdírẹ́ẹ̀sì + 0x18) & 0x40000000u)) {
            uint32_t Fèsì = maṣíìnì_forúkọsílẹ̀(àpótì_méèlì_àdírẹ́ẹ̀sì);
            if (Fèsì == 요청) { 기억장벽(); return àpótì_méèlì_détà[1] == 0x80000000u; }
        }
        if (시계세기() - Rọ́ọ̀nù > 진동수) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void 터미널바이트(unsigned);
extern int 터미널대기(void);
extern void 터미널가리킴(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../Ìjìnnà_iye/Ìjìnnà_iye.h"
static int 흐름목록;
static unsigned 직렬이전글자;
maṣíìnì_Ọ̀rọ̀ 보드흐름설정(maṣíìnì_Ọ̀rọ̀ 사용여부) { 흐름목록=사용여부!=0; return 0; }
maṣíìnì_Ọ̀rọ̀ 보드통로(maṣíìnì_Ọ̀rọ̀ òpónà, maṣíìnì_Ọ̀rọ̀ kóòdù_ẹyọ_ọ̀rọ̀) {
    if(흐름목록 && 자바셸출력((int32_t)òpónà,(int32_t)(kóòdù_ẹyọ_ọ̀rọ̀&255))) return 0;
    터미널바이트(kóòdù_ẹyọ_ọ̀rọ̀&255);
    원격출력(kóòdù_ẹyọ_ọ̀rọ̀&255);
    if ((kóòdù_ẹyọ_ọ̀rọ̀&255)==10 && 직렬이전글자!=13) {
        while (maṣíìnì_forúkọsílẹ̀(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        maṣíìnì_forúkọsílẹ̀(직렬장치)=13;
    }
    직렬이전글자=kóòdù_ẹyọ_ọ̀rọ̀&255;
    while (maṣíìnì_forúkọsílẹ̀(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    maṣíìnì_forúkọsílẹ̀(직렬장치) = (uint32_t)kóòdù_ẹyọ_ọ̀rọ̀ & 255;
    return 0;
}
maṣíìnì_Ọ̀rọ̀ 보드글자쓰기(maṣíìnì_Ọ̀rọ̀ kóòdù_ẹyọ_ọ̀rọ̀) { return 보드통로(1,kóòdù_ẹyọ_ọ̀rọ̀); }
maṣíìnì_Ọ̀rọ̀ 보드원시글자읽기(void) {
    int Ìjìnnà_ẹyọ_ọ̀rọ̀=원격입력();if(Ìjìnnà_ẹyọ_ọ̀rọ̀>=0)return Ìjìnnà_ẹyọ_ọ̀rọ̀;
    if (maṣíìnì_forúkọsílẹ̀(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t iye = maṣíìnì_forúkọsílẹ̀(직렬장치);
    if (iye & 0xf00) { maṣíìnì_forúkọsílẹ̀(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return iye & 255;
}
maṣíìnì_Ọ̀rọ̀ 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char 꾸러미자료[6];
    if(터미널대기())return (uint32_t)-4096;
    if(흐름목록){int32_t kóòdù_ẹyọ_ọ̀rọ̀=자바셸입력();if(kóòdù_ẹyọ_ọ̀rọ̀!=-3)return (uint32_t)kóòdù_ẹyọ_ọ̀rọ̀;}
    for(;;){
        int kóòdù_ẹyọ_ọ̀rọ̀=(int32_t)보드원시글자읽기();if(kóòdù_ẹyọ_ọ̀rọ̀<0)return (uint32_t)kóòdù_ẹyọ_ọ̀rọ̀;
        if(!꾸러미안쪽){if(kóòdù_ẹyọ_ọ̀rọ̀!=30)return kóòdù_ẹyọ_ọ̀rọ̀;꾸러미안쪽=1;사용량=0;continue;}
        꾸러미자료[사용량++]=kóòdù_ẹyọ_ọ̀rọ̀;if(사용량<6)continue;꾸러미안쪽=0;
        if(꾸러미자료[0]==1)터미널가리킴(꾸러미자료[1],꾸러미자료[2]+꾸러미자료[3]*256,꾸러미자료[4]+꾸러미자료[5]*256);
        if(꾸러미자료[0]==2)터미널바로가기키(꾸러미자료[1]);
        if(꾸러미자료[0]==3)터미널입력방식(꾸러미자료[1]);
        if(터미널대기())return (uint32_t)-4096;
    }
}
maṣíìnì_Ọ̀rọ̀ 보드밀리초(void) { return (uint32_t)(시계세기() / (진동수 / 1000)); }
maṣíìnì_Ọ̀rọ̀ 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *fọ́nrán_détà) { while (*fọ́nrán_détà) 보드글자쓰기((unsigned char)*fọ́nrán_détà++); }
static void 직렬열여섯진출력(maṣíìnì_Ọ̀rọ̀ 개수) { const char *열여섯진숫자 = "0123456789abcdef"; for (int fọ́nrán_détà = 60; fọ́nrán_détà >= 0; fọ́nrán_détà -= 4) 보드글자쓰기(열여섯진숫자[(개수 >> fọ́nrán_détà) & 15]); }
maṣíìnì_Ọ̀rọ̀ 보드멈추기(maṣíìnì_Ọ̀rọ̀ ipò_iye) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(ipò_iye); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); 보드멈추기(1); __builtin_unreachable(); }
void 보드예외(maṣíìnì_Ọ̀rọ̀ 예외상태, maṣíìnì_Ọ̀rọ̀ 명령위치, maṣíìnì_Ọ̀rọ̀ aláìbẹgbẹmu_àdírẹ́ẹ̀sì) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(예외상태);
    직렬글출력(" PC="); 직렬열여섯진출력(명령위치); 직렬글출력(" FAR="); 직렬열여섯진출력(aláìbẹgbẹmu_àdírẹ́ẹ̀sì);
    보드멈추기(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    àpótì_méèlì_détà[0]=32;àpótì_méèlì_détà[1]=0;àpótì_méèlì_détà[2]=0x10004;àpótì_méèlì_détà[3]=8;àpótì_méèlì_détà[4]=0;
    àpótì_méèlì_détà[5]=àpótì_méèlì_détà[6]=àpótì_méèlì_détà[7]=0;
    return àpótì_méèlì()&&àpótì_méèlì_détà[4]==0x80000008u&&(àpótì_méèlì_détà[5]||àpótì_méèlì_détà[6]);
}
int 보드기계주소(unsigned char *àdírẹ́ẹ̀sì) {
    àpótì_méèlì_détà[0]=32;àpótì_méèlì_détà[1]=0;àpótì_méèlì_détà[2]=0x10003;àpótì_méèlì_détà[3]=8;àpótì_méèlì_détà[4]=0;
    àpótì_méèlì_détà[5]=àpótì_méèlì_détà[6]=àpótì_méèlì_détà[7]=0;
    if(!àpótì_méèlì()||(àpótì_méèlì_détà[4]&0x80000000u)==0||(àpótì_méèlì_détà[4]&0xffff)!=6)return 0;
    const unsigned char *détà=(const unsigned char*)&àpótì_méèlì_détà[5];unsigned 합=0;
    for(unsigned 순번=0;순번<6;순번++){àdírẹ́ẹ̀sì[순번]=détà[순번];합|=détà[순번];}return 합&&!(àdírẹ́ẹ̀sì[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(진동수));
    maṣíìnì_forúkọsílẹ̀(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    maṣíìnì_forúkọsílẹ̀(범용입출력 + 4) = (maṣíìnì_forúkọsílẹ̀(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    maṣíìnì_forúkọsílẹ̀(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. ìkùnà_iye 시 config.txt의 48MHz를 사용한다.
    àpótì_méèlì_détà[0] = 36; àpótì_méèlì_détà[1] = 0; àpótì_méèlì_détà[2] = 0x38002; àpótì_méèlì_détà[3] = 12;
    àpótì_méèlì_détà[4] = 0; àpótì_méèlì_détà[5] = 2; àpótì_méèlì_détà[6] = 48000000; àpótì_méèlì_détà[7] = 0; àpótì_méèlì_détà[8] = 0;
    int 시계정상 = àpótì_méèlì();
    uint32_t 속도 = 시계정상 && àpótì_méèlì_détà[6] >= 1843200 ? àpótì_méèlì_détà[6] : 48000000;
    àpótì_méèlì_détà[0]=32; àpótì_méèlì_détà[1]=0; àpótì_méèlì_détà[2]=0x10005; àpótì_méèlì_détà[3]=8; àpótì_méèlì_détà[4]=0;
    àpótì_méèlì_détà[5]=àpótì_méèlì_détà[6]=àpótì_méèlì_détà[7]=0;
    if (àpótì_méèlì() && àpótì_méèlì_détà[4]==0x80000008u) 팔기억킬로바이트=àpótì_méèlì_détà[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    maṣíìnì_forúkọsílẹ̀(직렬장치 + 0x44) = 0x7ff;
    maṣíìnì_forúkọsílẹ̀(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    maṣíìnì_forúkọsílẹ̀(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    maṣíìnì_forúkọsílẹ̀(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    maṣíìnì_forúkọsílẹ̀(직렬장치 + 0x38) = 0;
    maṣíìnì_forúkọsílẹ̀(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
maṣíìnì_Ọ̀rọ̀ 보드파일전송(maṣíìnì_Ọ̀rọ̀ ìṣe) { return (uint32_t)ftp_control((int)ìṣe); }
maṣíìnì_Ọ̀rọ̀ 보드망상태(maṣíìnì_Ọ̀rọ̀ ìgbéwọlé_iye, maṣíìnì_Ọ̀rọ̀ wá_atọ̀ka_àkóónú) { return 망상태읽기(ìgbéwọlé_iye, wá_atọ̀ka_àkóónú); }
maṣíìnì_Ọ̀rọ̀ 보드망설정(maṣíìnì_Ọ̀rọ̀ ìṣe, maṣíìnì_Ọ̀rọ̀ àdírẹ́ẹ̀sì, maṣíìnì_Ọ̀rọ̀ asẹ́_iye_iye, maṣíìnì_Ọ̀rọ̀ ẹnu_odi_iye) { return (uint32_t)ṣàtòpọ̀_Alásopọ̀(ìṣe, àdírẹ́ẹ̀sì, asẹ́_iye_iye, ẹnu_odi_iye); }
maṣíìnì_Ọ̀rọ̀ 보드응답보내기(maṣíìnì_Ọ̀rọ̀ àdírẹ́ẹ̀sì, maṣíìnì_Ọ̀rọ̀ ìtodátà_iye) { return (uint32_t)응답시험시작(àdírẹ́ẹ̀sì, ìtodátà_iye); }
maṣíìnì_Ọ̀rọ̀ 보드응답읽기(maṣíìnì_Ọ̀rọ̀ ìgbéwọlé_iye) { return (uint32_t)응답시험읽기(ìgbéwọlé_iye); }
maṣíìnì_Ọ̀rọ̀ 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned wá_atọ̀ka_àkóónú=0; wá_atọ̀ka_àkóónú<32; wá_atọ̀ka_àkóónú++) pa_dé_Alásopọ̀(wá_atọ̀ka_àkóónú);
    for (unsigned wá_atọ̀ka_àkóónú=0; wá_atọ̀ka_àkóónú<4; wá_atọ̀ka_àkóónú++) 보드사용자제어(32+wá_atọ̀ka_àkóónú);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (maṣíìnì_forúkọsílẹ̀(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    maṣíìnì_forúkọsílẹ̀(0xfe100020ul)=0x5a000000u | (maṣíìnì_forúkọsílẹ̀(0xfe100020ul)&~0xfffu) | 0x555;
    maṣíìnì_forúkọsílẹ̀(0xfe100024ul)=0x5a000000u | 10;
    maṣíìnì_forúkọsílẹ̀(0xfe10001cul)=0x5a000000u | (maṣíìnì_forúkọsílẹ̀(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

maṣíìnì_Ọ̀rọ̀ 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 현재 크기를 읽는다. */
    const uint32_t aṣèbéèré_iye[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(aṣèbéèré_iye)/4; 순번++) àpótì_méèlì_détà[순번] = aṣèbéèré_iye[순번];
    if (àpótì_méèlì() && àpótì_méèlì_détà[4] == 0x80000008u &&
        àpótì_méèlì_détà[5] >= 640 && àpótì_méèlì_détà[5] <= 1920 &&
        àpótì_méèlì_détà[6] >= 480 && àpótì_méèlì_détà[6] <= 1080) {
        요청너비 = àpótì_méèlì_détà[5]; 요청높이 = àpótì_méèlì_détà[6];
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
    for (size_t 순번 = 0; 순번 < sizeof(요청)/4; 순번++) àpótì_méèlì_détà[순번] = 요청[순번];
    // 위 메시지의 gangan_détà 길이를 사용: 태그 추가 시 gígùn_iye 불일치를 방지한다.
    àpótì_méèlì_détà[0] = sizeof(요청);
    if (!àpótì_méèlì()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 응답길이[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (àpótì_méèlì_détà[응답들[순번]] != (0x80000000u | 응답길이[순번])) return 0;
    uint32_t Àgbétẹ́lẹ̀_iye = àpótì_méèlì_détà[28] & 0x3fffffffu;
    uint32_t Ìwọ̀n = àpótì_méèlì_détà[29];
    uint32_t 받은너비 = àpótì_méèlì_détà[5], 받은높이 = àpótì_méèlì_détà[6], 받은줄간격 = àpótì_méèlì_détà[33];
    if (àpótì_méèlì_détà[15] != 32 || àpótì_méèlì_détà[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        àpótì_méèlì_détà[10] < 받은너비 || àpótì_méèlì_détà[11] < 받은높이 || àpótì_méèlì_détà[23] || àpótì_méèlì_détà[24] ||
        !Àgbétẹ́lẹ̀_iye || Àgbétẹ́lẹ̀_iye < 0x1000000 || (Àgbétẹ́lẹ̀_iye & 3) || 받은줄간격 < 받은너비 * 4 || (받은줄간격 & 3) ||
        (uint64_t)받은줄간격 * 받은높이 > Ìwọ̀n || (uint64_t)Àgbétẹ́lẹ̀_iye + Ìwọ̀n > 0x40000000u)
        return 0;
    보드그림준비((volatile uint32_t *)(uintptr_t)Àgbétẹ́lẹ̀_iye, 받은너비, 받은높이, 받은줄간격);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 èròjà_atẹ̀lélànà_iye. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } Ìṣètò_kíkà;
static Ìṣètò_kíkà 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int 실행중[3] = {1, 0, 0};
static int 현재작업;
extern void Ìṣètò_kíkà_ṣèpapòdà(Ìṣètò_kíkà *, Ìṣètò_kíkà *);
extern void 자바작업(int32_t);
maṣíìnì_Ọ̀rọ̀ 보드양보(void) {
    network_poll();
    int 이전 = 현재작업, 다음 = (이전 + 1) % 3;
    while (다음 != 이전 && !실행중[다음]) 다음 = (다음 + 1) % 3;
    if (다음 != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (실행중[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        현재작업 = 다음;
        Ìṣètò_kíkà_ṣèpapòdà(&작업문맥들[이전], &작업문맥들[다음]);
    }
    return 0;
}
static void iṣẹ́_ìbẹ̀rẹ̀(void) {
    자바작업(현재작업);
    실행중[현재작업] = 0;
    보드양보();
    커널중단("finished task resumed");
}
maṣíìnì_Ọ̀rọ̀ 보드작업만들기(maṣíìnì_Ọ̀rọ̀ Àfidámọ̀_iye) {
    if (Àfidámọ̀_iye < 1 || Àfidámọ̀_iye > 2 || 실행중[Àfidámọ̀_iye]) return (uint32_t)-1;
    memset(&작업문맥들[Àfidámọ̀_iye], 0, sizeof(Ìṣètò_kíkà));
    *(uint64_t *)쌓임공간들[Àfidámọ̀_iye - 1] = 0x6b6f726f7373746bull;
    작업문맥들[Àfidámọ̀_iye].저장값[11] = (uintptr_t)iṣẹ́_ìbẹ̀rẹ̀;
    작업문맥들[Àfidámọ̀_iye].저장값[12] = (uintptr_t)(쌓임공간들[Àfidámọ̀_iye - 1] + sizeof(쌓임공간들[0]));
    실행중[Àfidámọ̀_iye] = 1;
    return 0;
}
maṣíìnì_Ọ̀rọ̀ 보드작업상태(maṣíìnì_Ọ̀rọ̀ Àfidámọ̀_iye) { return Àfidámọ̀_iye < 3 ? 실행중[Àfidámọ̀_iye] : (uint32_t)-1; }
extern maṣíìnì_Ọ̀rọ̀ 미리번역기억조회(maṣíìnì_Ọ̀rọ̀);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
maṣíìnì_Ọ̀rọ̀ 보드체계조회(maṣíìnì_Ọ̀rọ̀ ìgbéwọlé_iye, maṣíìnì_Ọ̀rọ̀ wá_atọ̀ka_àkóónú) {
    if (ìgbéwọlé_iye==0) return 팔기억킬로바이트;
    if (ìgbéwọlé_iye==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (ìgbéwọlé_iye==2 || ìgbéwọlé_iye==3) return 미리번역기억조회(ìgbéwọlé_iye==3);
    if (ìgbéwọlé_iye==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (ìgbéwọlé_iye==5) return 80*1024; /* ṣiṣẹ́_àṣẹ 공간 16 MiB + 네 세션 보관 공간. */
    if (ìgbéwọlé_iye>=20) return 사용자상태읽기(ìgbéwọlé_iye-20, wá_atọ̀ka_àkóónú);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[현재작업]; }
