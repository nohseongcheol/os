#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "mtumiaji.h"
#include "../Mtandao_Mpororo/Mtandao_Mpororo.h"
typedef uintptr_t mashine_Neno;
#define mashine_sajili(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define kikasha_barua_anwani 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t 시계세기(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t 진동수;
static volatile uint32_t kikasha_barua_data[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *자료위치, int msimbo_wa_kibambo, size_t 개수) { unsigned char *다음위치 = 자료위치; while (개수--) *다음위치++ = msimbo_wa_kibambo; return 자료위치; }
void *memcpy(void *fikio_data, const void *tungo_data, size_t 개수) { unsigned char *첫째값 = fikio_data; const unsigned char *둘째값 = tungo_data; while (개수--) *첫째값++ = *둘째값++; return fikio_data; }

static int kikasha_barua(void) {
    uint32_t 요청 = (uint32_t)(uintptr_t)kikasha_barua_data | 8;
    uint64_t endesha = 시계세기();
    기억장벽();
    while (mashine_sajili(kikasha_barua_anwani + 0x38) & 0x80000000u)
        if (시계세기() - endesha > 진동수) return 0;
    mashine_sajili(kikasha_barua_anwani + 0x20) = 요청;
    for (;;) {
        if (!(mashine_sajili(kikasha_barua_anwani + 0x18) & 0x40000000u)) {
            uint32_t jibu = mashine_sajili(kikasha_barua_anwani);
            if (jibu == 요청) { 기억장벽(); return kikasha_barua_data[1] == 0x80000000u; }
        }
        if (시계세기() - endesha > 진동수) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void 터미널바이트(unsigned);
extern int 터미널대기(void);
extern void 터미널가리킴(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../kwa_mbali_thamani/kwa_mbali_thamani.h"
static int 흐름목록;
static unsigned 직렬이전글자;
mashine_Neno 보드흐름설정(mashine_Neno 사용여부) { 흐름목록=사용여부!=0; return 0; }
mashine_Neno 보드통로(mashine_Neno mkondo, mashine_Neno msimbo_wa_kibambo) {
    if(흐름목록 && 자바셸출력((int32_t)mkondo,(int32_t)(msimbo_wa_kibambo&255))) return 0;
    터미널바이트(msimbo_wa_kibambo&255);
    원격출력(msimbo_wa_kibambo&255);
    if ((msimbo_wa_kibambo&255)==10 && 직렬이전글자!=13) {
        while (mashine_sajili(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        mashine_sajili(직렬장치)=13;
    }
    직렬이전글자=msimbo_wa_kibambo&255;
    while (mashine_sajili(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    mashine_sajili(직렬장치) = (uint32_t)msimbo_wa_kibambo & 255;
    return 0;
}
mashine_Neno 보드글자쓰기(mashine_Neno msimbo_wa_kibambo) { return 보드통로(1,msimbo_wa_kibambo); }
mashine_Neno 보드원시글자읽기(void) {
    int kwa_mbali_kibambo=원격입력();if(kwa_mbali_kibambo>=0)return kwa_mbali_kibambo;
    if (mashine_sajili(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t thamani = mashine_sajili(직렬장치);
    if (thamani & 0xf00) { mashine_sajili(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return thamani & 255;
}
mashine_Neno 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char pakiti_data[6];
    if(터미널대기())return (uint32_t)-4096;
    if(흐름목록){int32_t msimbo_wa_kibambo=자바셸입력();if(msimbo_wa_kibambo!=-3)return (uint32_t)msimbo_wa_kibambo;}
    for(;;){
        int msimbo_wa_kibambo=(int32_t)보드원시글자읽기();if(msimbo_wa_kibambo<0)return (uint32_t)msimbo_wa_kibambo;
        if(!꾸러미안쪽){if(msimbo_wa_kibambo!=30)return msimbo_wa_kibambo;꾸러미안쪽=1;사용량=0;continue;}
        pakiti_data[사용량++]=msimbo_wa_kibambo;if(사용량<6)continue;꾸러미안쪽=0;
        if(pakiti_data[0]==1)터미널가리킴(pakiti_data[1],pakiti_data[2]+pakiti_data[3]*256,pakiti_data[4]+pakiti_data[5]*256);
        if(pakiti_data[0]==2)터미널바로가기키(pakiti_data[1]);
        if(pakiti_data[0]==3)터미널입력방식(pakiti_data[1]);
        if(터미널대기())return (uint32_t)-4096;
    }
}
mashine_Neno 보드밀리초(void) { return (uint32_t)(시계세기() / (진동수 / 1000)); }
mashine_Neno 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *tungo_data) { while (*tungo_data) 보드글자쓰기((unsigned char)*tungo_data++); }
static void 직렬열여섯진출력(mashine_Neno 개수) { const char *열여섯진숫자 = "0123456789abcdef"; for (int tungo_data = 60; tungo_data >= 0; tungo_data -= 4) 보드글자쓰기(열여섯진숫자[(개수 >> tungo_data) & 15]); }
mashine_Neno 보드멈추기(mashine_Neno hali_thamani) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(hali_thamani); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); 보드멈추기(1); __builtin_unreachable(); }
void 보드예외(mashine_Neno vighairi_hali, mashine_Neno 명령위치, mashine_Neno batili_anwani) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(vighairi_hali);
    직렬글출력(" PC="); 직렬열여섯진출력(명령위치); 직렬글출력(" FAR="); 직렬열여섯진출력(batili_anwani);
    보드멈추기(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    kikasha_barua_data[0]=32;kikasha_barua_data[1]=0;kikasha_barua_data[2]=0x10004;kikasha_barua_data[3]=8;kikasha_barua_data[4]=0;
    kikasha_barua_data[5]=kikasha_barua_data[6]=kikasha_barua_data[7]=0;
    return kikasha_barua()&&kikasha_barua_data[4]==0x80000008u&&(kikasha_barua_data[5]||kikasha_barua_data[6]);
}
int 보드기계주소(unsigned char *anwani) {
    kikasha_barua_data[0]=32;kikasha_barua_data[1]=0;kikasha_barua_data[2]=0x10003;kikasha_barua_data[3]=8;kikasha_barua_data[4]=0;
    kikasha_barua_data[5]=kikasha_barua_data[6]=kikasha_barua_data[7]=0;
    if(!kikasha_barua()||(kikasha_barua_data[4]&0x80000000u)==0||(kikasha_barua_data[4]&0xffff)!=6)return 0;
    const unsigned char *data=(const unsigned char*)&kikasha_barua_data[5];unsigned 합=0;
    for(unsigned 순번=0;순번<6;순번++){anwani[순번]=data[순번];합|=data[순번];}return 합&&!(anwani[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(진동수));
    mashine_sajili(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    mashine_sajili(범용입출력 + 4) = (mashine_sajili(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    mashine_sajili(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. kushindwa_thamani 시 config.txt의 48MHz를 사용한다.
    kikasha_barua_data[0] = 36; kikasha_barua_data[1] = 0; kikasha_barua_data[2] = 0x38002; kikasha_barua_data[3] = 12;
    kikasha_barua_data[4] = 0; kikasha_barua_data[5] = 2; kikasha_barua_data[6] = 48000000; kikasha_barua_data[7] = 0; kikasha_barua_data[8] = 0;
    int 시계정상 = kikasha_barua();
    uint32_t 속도 = 시계정상 && kikasha_barua_data[6] >= 1843200 ? kikasha_barua_data[6] : 48000000;
    kikasha_barua_data[0]=32; kikasha_barua_data[1]=0; kikasha_barua_data[2]=0x10005; kikasha_barua_data[3]=8; kikasha_barua_data[4]=0;
    kikasha_barua_data[5]=kikasha_barua_data[6]=kikasha_barua_data[7]=0;
    if (kikasha_barua() && kikasha_barua_data[4]==0x80000008u) 팔기억킬로바이트=kikasha_barua_data[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    mashine_sajili(직렬장치 + 0x44) = 0x7ff;
    mashine_sajili(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    mashine_sajili(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    mashine_sajili(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    mashine_sajili(직렬장치 + 0x38) = 0;
    mashine_sajili(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
mashine_Neno 보드파일전송(mashine_Neno Kitendo) { return (uint32_t)ftp_control((int)Kitendo); }
mashine_Neno 보드망상태(mashine_Neno ingizo_thamani, mashine_Neno kielezo) { return 망상태읽기(ingizo_thamani, kielezo); }
mashine_Neno 보드망설정(mashine_Neno Kitendo, mashine_Neno anwani, mashine_Neno barakoa_thamani, mashine_Neno kichanganishi_mtandao_thamani) { return (uint32_t)sanidi_Mtandao(Kitendo, anwani, barakoa_thamani, kichanganishi_mtandao_thamani); }
mashine_Neno 보드응답보내기(mashine_Neno anwani, mashine_Neno mpangilio_thamani) { return (uint32_t)응답시험시작(anwani, mpangilio_thamani); }
mashine_Neno 보드응답읽기(mashine_Neno ingizo_thamani) { return (uint32_t)응답시험읽기(ingizo_thamani); }
mashine_Neno 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned kielezo=0; kielezo<32; kielezo++) funga_Mtandao(kielezo);
    for (unsigned kielezo=0; kielezo<4; kielezo++) 보드사용자제어(32+kielezo);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (mashine_sajili(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    mashine_sajili(0xfe100020ul)=0x5a000000u | (mashine_sajili(0xfe100020ul)&~0xfffu) | 0x555;
    mashine_sajili(0xfe100024ul)=0x5a000000u | 10;
    mashine_sajili(0xfe10001cul)=0x5a000000u | (mashine_sajili(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

mashine_Neno 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 현재 크기를 읽는다. */
    const uint32_t uliza_thamani[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(uliza_thamani)/4; 순번++) kikasha_barua_data[순번] = uliza_thamani[순번];
    if (kikasha_barua() && kikasha_barua_data[4] == 0x80000008u &&
        kikasha_barua_data[5] >= 640 && kikasha_barua_data[5] <= 1920 &&
        kikasha_barua_data[6] >= 480 && kikasha_barua_data[6] <= 1080) {
        요청너비 = kikasha_barua_data[5]; 요청높이 = kikasha_barua_data[6];
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
    for (size_t 순번 = 0; 순번 < sizeof(요청)/4; 순번++) kikasha_barua_data[순번] = 요청[순번];
    // 위 메시지의 halisi_data 길이를 사용: 태그 추가 시 urefu_thamani 불일치를 방지한다.
    kikasha_barua_data[0] = sizeof(요청);
    if (!kikasha_barua()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 응답길이[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (kikasha_barua_data[응답들[순번]] != (0x80000000u | 응답길이[순번])) return 0;
    uint32_t nyuma_thamani = kikasha_barua_data[28] & 0x3fffffffu;
    uint32_t panga_ukubwa = kikasha_barua_data[29];
    uint32_t 받은너비 = kikasha_barua_data[5], 받은높이 = kikasha_barua_data[6], 받은줄간격 = kikasha_barua_data[33];
    if (kikasha_barua_data[15] != 32 || kikasha_barua_data[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        kikasha_barua_data[10] < 받은너비 || kikasha_barua_data[11] < 받은높이 || kikasha_barua_data[23] || kikasha_barua_data[24] ||
        !nyuma_thamani || nyuma_thamani < 0x1000000 || (nyuma_thamani & 3) || 받은줄간격 < 받은너비 * 4 || (받은줄간격 & 3) ||
        (uint64_t)받은줄간격 * 받은높이 > panga_ukubwa || (uint64_t)nyuma_thamani + panga_ukubwa > 0x40000000u)
        return 0;
    보드그림준비((volatile uint32_t *)(uintptr_t)nyuma_thamani, 받은너비, 받은높이, 받은줄간격);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 mtungo_thamani. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } Muktadha;
static Muktadha 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int teknolojia_ya_maelezo_Kukimbia[3] = {1, 0, 0};
static int 현재작업;
extern void Muktadha_badili(Muktadha *, Muktadha *);
extern void 자바작업(int32_t);
mashine_Neno 보드양보(void) {
    network_poll();
    int 이전 = 현재작업, 다음 = (이전 + 1) % 3;
    while (다음 != 이전 && !teknolojia_ya_maelezo_Kukimbia[다음]) 다음 = (다음 + 1) % 3;
    if (다음 != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (teknolojia_ya_maelezo_Kukimbia[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        현재작업 = 다음;
        Muktadha_badili(&작업문맥들[이전], &작업문맥들[다음]);
    }
    return 0;
}
static void kazi_uwashaji(void) {
    자바작업(현재작업);
    teknolojia_ya_maelezo_Kukimbia[현재작업] = 0;
    보드양보();
    커널중단("finished task resumed");
}
mashine_Neno 보드작업만들기(mashine_Neno kitambulishi_thamani) {
    if (kitambulishi_thamani < 1 || kitambulishi_thamani > 2 || teknolojia_ya_maelezo_Kukimbia[kitambulishi_thamani]) return (uint32_t)-1;
    memset(&작업문맥들[kitambulishi_thamani], 0, sizeof(Muktadha));
    *(uint64_t *)쌓임공간들[kitambulishi_thamani - 1] = 0x6b6f726f7373746bull;
    작업문맥들[kitambulishi_thamani].저장값[11] = (uintptr_t)kazi_uwashaji;
    작업문맥들[kitambulishi_thamani].저장값[12] = (uintptr_t)(쌓임공간들[kitambulishi_thamani - 1] + sizeof(쌓임공간들[0]));
    teknolojia_ya_maelezo_Kukimbia[kitambulishi_thamani] = 1;
    return 0;
}
mashine_Neno 보드작업상태(mashine_Neno kitambulishi_thamani) { return kitambulishi_thamani < 3 ? teknolojia_ya_maelezo_Kukimbia[kitambulishi_thamani] : (uint32_t)-1; }
extern mashine_Neno 미리번역기억조회(mashine_Neno);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
mashine_Neno 보드체계조회(mashine_Neno ingizo_thamani, mashine_Neno kielezo) {
    if (ingizo_thamani==0) return 팔기억킬로바이트;
    if (ingizo_thamani==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (ingizo_thamani==2 || ingizo_thamani==3) return 미리번역기억조회(ingizo_thamani==3);
    if (ingizo_thamani==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (ingizo_thamani==5) return 80*1024; /* tekeleza_amri 공간 16 MiB + 네 세션 보관 공간. */
    if (ingizo_thamani>=20) return 사용자상태읽기(ingizo_thamani-20, kielezo);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[현재작업]; }
