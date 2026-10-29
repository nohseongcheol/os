#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "kiy_jariñoo_internet.h"
#include "../mbaal_Tegalo/mbaal_Tegalo.h"
typedef uintptr_t masin_Word;
#define masin_bindu(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define boyetu_bataaxal_dëkkuwaay 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t 시계세기(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t 진동수;
static volatile uint32_t boyetu_bataaxal_mbir[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *자료위치, int kotu_araf, size_t 개수) { unsigned char *다음위치 = 자료위치; while (개수--) *다음위치++ = kotu_araf; return 자료위치; }
void *memcpy(void *jëmmukaay_mbir, const void *araf_yu_bennoo_mbir, size_t 개수) { unsigned char *첫째값 = jëmmukaay_mbir; const unsigned char *둘째값 = araf_yu_bennoo_mbir; while (개수--) *첫째값++ = *둘째값++; return jëmmukaay_mbir; }

static int boyetu_bataaxal(void) {
    uint32_t 요청 = (uint32_t)(uintptr_t)boyetu_bataaxal_mbir | 8;
    uint64_t daw = 시계세기();
    기억장벽();
    while (masin_bindu(boyetu_bataaxal_dëkkuwaay + 0x38) & 0x80000000u)
        if (시계세기() - daw > 진동수) return 0;
    masin_bindu(boyetu_bataaxal_dëkkuwaay + 0x20) = 요청;
    for (;;) {
        if (!(masin_bindu(boyetu_bataaxal_dëkkuwaay + 0x18) & 0x40000000u)) {
            uint32_t tontu = masin_bindu(boyetu_bataaxal_dëkkuwaay);
            if (tontu == 요청) { 기억장벽(); return boyetu_bataaxal_mbir[1] == 0x80000000u; }
        }
        if (시계세기() - daw > 진동수) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void 터미널바이트(unsigned);
extern int 터미널대기(void);
extern void 터미널가리킴(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../lu_soree_xëyma/lu_soree_xëyma.h"
static int 흐름목록;
static unsigned 직렬이전글자;
masin_Word 보드흐름설정(masin_Word 사용여부) { 흐름목록=사용여부!=0; return 0; }
masin_Word 보드통로(masin_Word Yoon, masin_Word kotu_araf) {
    if(흐름목록 && 자바셸출력((int32_t)Yoon,(int32_t)(kotu_araf&255))) return 0;
    터미널바이트(kotu_araf&255);
    원격출력(kotu_araf&255);
    if ((kotu_araf&255)==10 && 직렬이전글자!=13) {
        while (masin_bindu(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        masin_bindu(직렬장치)=13;
    }
    직렬이전글자=kotu_araf&255;
    while (masin_bindu(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    masin_bindu(직렬장치) = (uint32_t)kotu_araf & 255;
    return 0;
}
masin_Word 보드글자쓰기(masin_Word kotu_araf) { return 보드통로(1,kotu_araf); }
masin_Word 보드원시글자읽기(void) {
    int lu_soree_Araf=원격입력();if(lu_soree_Araf>=0)return lu_soree_Araf;
    if (masin_bindu(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t xëyma = masin_bindu(직렬장치);
    if (xëyma & 0xf00) { masin_bindu(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return xëyma & 255;
}
masin_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char 꾸러미자료[6];
    if(터미널대기())return (uint32_t)-4096;
    if(흐름목록){int32_t kotu_araf=자바셸입력();if(kotu_araf!=-3)return (uint32_t)kotu_araf;}
    for(;;){
        int kotu_araf=(int32_t)보드원시글자읽기();if(kotu_araf<0)return (uint32_t)kotu_araf;
        if(!꾸러미안쪽){if(kotu_araf!=30)return kotu_araf;꾸러미안쪽=1;사용량=0;continue;}
        꾸러미자료[사용량++]=kotu_araf;if(사용량<6)continue;꾸러미안쪽=0;
        if(꾸러미자료[0]==1)터미널가리킴(꾸러미자료[1],꾸러미자료[2]+꾸러미자료[3]*256,꾸러미자료[4]+꾸러미자료[5]*256);
        if(꾸러미자료[0]==2)터미널바로가기키(꾸러미자료[1]);
        if(꾸러미자료[0]==3)터미널입력방식(꾸러미자료[1]);
        if(터미널대기())return (uint32_t)-4096;
    }
}
masin_Word 보드밀리초(void) { return (uint32_t)(시계세기() / (진동수 / 1000)); }
masin_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *araf_yu_bennoo_mbir) { while (*araf_yu_bennoo_mbir) 보드글자쓰기((unsigned char)*araf_yu_bennoo_mbir++); }
static void 직렬열여섯진출력(masin_Word 개수) { const char *열여섯진숫자 = "0123456789abcdef"; for (int araf_yu_bennoo_mbir = 60; araf_yu_bennoo_mbir >= 0; araf_yu_bennoo_mbir -= 4) 보드글자쓰기(열여섯진숫자[(개수 >> araf_yu_bennoo_mbir) & 15]); }
masin_Word 보드멈추기(masin_Word nekkin_xëyma) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(nekkin_xëyma); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); 보드멈추기(1); __builtin_unreachable(); }
void 보드예외(masin_Word 예외상태, masin_Word 명령위치, masin_Word baaxul_dëkkuwaay) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(예외상태);
    직렬글출력(" PC="); 직렬열여섯진출력(명령위치); 직렬글출력(" FAR="); 직렬열여섯진출력(baaxul_dëkkuwaay);
    보드멈추기(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    boyetu_bataaxal_mbir[0]=32;boyetu_bataaxal_mbir[1]=0;boyetu_bataaxal_mbir[2]=0x10004;boyetu_bataaxal_mbir[3]=8;boyetu_bataaxal_mbir[4]=0;
    boyetu_bataaxal_mbir[5]=boyetu_bataaxal_mbir[6]=boyetu_bataaxal_mbir[7]=0;
    return boyetu_bataaxal()&&boyetu_bataaxal_mbir[4]==0x80000008u&&(boyetu_bataaxal_mbir[5]||boyetu_bataaxal_mbir[6]);
}
int 보드기계주소(unsigned char *dëkkuwaay) {
    boyetu_bataaxal_mbir[0]=32;boyetu_bataaxal_mbir[1]=0;boyetu_bataaxal_mbir[2]=0x10003;boyetu_bataaxal_mbir[3]=8;boyetu_bataaxal_mbir[4]=0;
    boyetu_bataaxal_mbir[5]=boyetu_bataaxal_mbir[6]=boyetu_bataaxal_mbir[7]=0;
    if(!boyetu_bataaxal()||(boyetu_bataaxal_mbir[4]&0x80000000u)==0||(boyetu_bataaxal_mbir[4]&0xffff)!=6)return 0;
    const unsigned char *mbir=(const unsigned char*)&boyetu_bataaxal_mbir[5];unsigned 합=0;
    for(unsigned 순번=0;순번<6;순번++){dëkkuwaay[순번]=mbir[순번];합|=mbir[순번];}return 합&&!(dëkkuwaay[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(진동수));
    masin_bindu(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    masin_bindu(범용입출력 + 4) = (masin_bindu(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    masin_bindu(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. foo_xëyma 시 config.txt의 48MHz를 사용한다.
    boyetu_bataaxal_mbir[0] = 36; boyetu_bataaxal_mbir[1] = 0; boyetu_bataaxal_mbir[2] = 0x38002; boyetu_bataaxal_mbir[3] = 12;
    boyetu_bataaxal_mbir[4] = 0; boyetu_bataaxal_mbir[5] = 2; boyetu_bataaxal_mbir[6] = 48000000; boyetu_bataaxal_mbir[7] = 0; boyetu_bataaxal_mbir[8] = 0;
    int 시계정상 = boyetu_bataaxal();
    uint32_t 속도 = 시계정상 && boyetu_bataaxal_mbir[6] >= 1843200 ? boyetu_bataaxal_mbir[6] : 48000000;
    boyetu_bataaxal_mbir[0]=32; boyetu_bataaxal_mbir[1]=0; boyetu_bataaxal_mbir[2]=0x10005; boyetu_bataaxal_mbir[3]=8; boyetu_bataaxal_mbir[4]=0;
    boyetu_bataaxal_mbir[5]=boyetu_bataaxal_mbir[6]=boyetu_bataaxal_mbir[7]=0;
    if (boyetu_bataaxal() && boyetu_bataaxal_mbir[4]==0x80000008u) 팔기억킬로바이트=boyetu_bataaxal_mbir[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    masin_bindu(직렬장치 + 0x44) = 0x7ff;
    masin_bindu(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    masin_bindu(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    masin_bindu(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    masin_bindu(직렬장치 + 0x38) = 0;
    masin_bindu(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
masin_Word 보드파일전송(masin_Word jëf) { return (uint32_t)ftp_control((int)jëf); }
masin_Word 보드망상태(masin_Word dugal_xabaar_xëyma, masin_Word àlluwa_tur) { return 망상태읽기(dugal_xabaar_xëyma, àlluwa_tur); }
masin_Word 보드망설정(masin_Word jëf, masin_Word dëkkuwaay, masin_Word muuraay_xëyma, masin_Word bunt_xëyma) { return (uint32_t)Jokkale_ak_ab_ordinateur_mbaal(jëf, dëkkuwaay, muuraay_xëyma, bunt_xëyma); }
masin_Word 보드응답보내기(masin_Word dëkkuwaay, masin_Word toftale_xëyma) { return (uint32_t)응답시험시작(dëkkuwaay, toftale_xëyma); }
masin_Word 보드응답읽기(masin_Word dugal_xabaar_xëyma) { return (uint32_t)응답시험읽기(dugal_xabaar_xëyma); }
masin_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned àlluwa_tur=0; àlluwa_tur<32; àlluwa_tur++) Tej_mbaal(àlluwa_tur);
    for (unsigned àlluwa_tur=0; àlluwa_tur<4; àlluwa_tur++) 보드사용자제어(32+àlluwa_tur);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (masin_bindu(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    masin_bindu(0xfe100020ul)=0x5a000000u | (masin_bindu(0xfe100020ul)&~0xfffu) | 0x555;
    masin_bindu(0xfe100024ul)=0x5a000000u | 10;
    masin_bindu(0xfe10001cul)=0x5a000000u | (masin_bindu(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

masin_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 현재 크기를 읽는다. */
    const uint32_t laaj_xëyma[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(laaj_xëyma)/4; 순번++) boyetu_bataaxal_mbir[순번] = laaj_xëyma[순번];
    if (boyetu_bataaxal() && boyetu_bataaxal_mbir[4] == 0x80000008u &&
        boyetu_bataaxal_mbir[5] >= 640 && boyetu_bataaxal_mbir[5] <= 1920 &&
        boyetu_bataaxal_mbir[6] >= 480 && boyetu_bataaxal_mbir[6] <= 1080) {
        요청너비 = boyetu_bataaxal_mbir[5]; 요청높이 = boyetu_bataaxal_mbir[6];
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
    for (size_t 순번 = 0; 순번 < sizeof(요청)/4; 순번++) boyetu_bataaxal_mbir[순번] = 요청[순번];
    // 위 메시지의 liteew_mbir 길이를 사용: 태그 추가 시 diir_xëyma 불일치를 방지한다.
    boyetu_bataaxal_mbir[0] = sizeof(요청);
    if (!boyetu_bataaxal()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 응답길이[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (boyetu_bataaxal_mbir[응답들[순번]] != (0x80000000u | 응답길이[순번])) return 0;
    uint32_t Njiitlay_xëyma = boyetu_bataaxal_mbir[28] & 0x3fffffffu;
    uint32_t tolluwaay = boyetu_bataaxal_mbir[29];
    uint32_t 받은너비 = boyetu_bataaxal_mbir[5], 받은높이 = boyetu_bataaxal_mbir[6], 받은줄간격 = boyetu_bataaxal_mbir[33];
    if (boyetu_bataaxal_mbir[15] != 32 || boyetu_bataaxal_mbir[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        boyetu_bataaxal_mbir[10] < 받은너비 || boyetu_bataaxal_mbir[11] < 받은높이 || boyetu_bataaxal_mbir[23] || boyetu_bataaxal_mbir[24] ||
        !Njiitlay_xëyma || Njiitlay_xëyma < 0x1000000 || (Njiitlay_xëyma & 3) || 받은줄간격 < 받은너비 * 4 || (받은줄간격 & 3) ||
        (uint64_t)받은줄간격 * 받은높이 > tolluwaay || (uint64_t)Njiitlay_xëyma + tolluwaay > 0x40000000u)
        return 0;
    보드그림준비((volatile uint32_t *)(uintptr_t)Njiitlay_xëyma, 받은너비, 받은높이, 받은줄간격);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 buumug_jokkale_xëyma. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } péete;
static péete 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int 실행중[3] = {1, 0, 0};
static int 현재작업;
extern void péete_jalantu(péete *, péete *);
extern void 자바작업(int32_t);
masin_Word 보드양보(void) {
    network_poll();
    int 이전 = 현재작업, 다음 = (이전 + 1) % 3;
    while (다음 != 이전 && !실행중[다음]) 다음 = (다음 + 1) % 3;
    if (다음 != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (실행중[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        현재작업 = 다음;
        péete_jalantu(&작업문맥들[이전], &작업문맥들[다음]);
    }
    return 0;
}
static void ligeey_buuraat(void) {
    자바작업(현재작업);
    실행중[현재작업] = 0;
    보드양보();
    커널중단("finished task resumed");
}
masin_Word 보드작업만들기(masin_Word raññeekaay_xëyma) {
    if (raññeekaay_xëyma < 1 || raññeekaay_xëyma > 2 || 실행중[raññeekaay_xëyma]) return (uint32_t)-1;
    memset(&작업문맥들[raññeekaay_xëyma], 0, sizeof(péete));
    *(uint64_t *)쌓임공간들[raññeekaay_xëyma - 1] = 0x6b6f726f7373746bull;
    작업문맥들[raññeekaay_xëyma].저장값[11] = (uintptr_t)ligeey_buuraat;
    작업문맥들[raññeekaay_xëyma].저장값[12] = (uintptr_t)(쌓임공간들[raññeekaay_xëyma - 1] + sizeof(쌓임공간들[0]));
    실행중[raññeekaay_xëyma] = 1;
    return 0;
}
masin_Word 보드작업상태(masin_Word raññeekaay_xëyma) { return raññeekaay_xëyma < 3 ? 실행중[raññeekaay_xëyma] : (uint32_t)-1; }
extern masin_Word 미리번역기억조회(masin_Word);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
masin_Word 보드체계조회(masin_Word dugal_xabaar_xëyma, masin_Word àlluwa_tur) {
    if (dugal_xabaar_xëyma==0) return 팔기억킬로바이트;
    if (dugal_xabaar_xëyma==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (dugal_xabaar_xëyma==2 || dugal_xabaar_xëyma==3) return 미리번역기억조회(dugal_xabaar_xëyma==3);
    if (dugal_xabaar_xëyma==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (dugal_xabaar_xëyma==5) return 80*1024; /* def_ndigel 공간 16 MiB + 네 세션 보관 공간. */
    if (dugal_xabaar_xëyma>=20) return 사용자상태읽기(dugal_xabaar_xëyma-20, àlluwa_tur);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[현재작업]; }
