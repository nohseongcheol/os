#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "mošomiši.h"
#include "../Netweke_kgoboko/Netweke_kgoboko.h"
typedef uintptr_t motšhene_Thalokontšu;
#define motšhene_ngwadiša(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define lepokisana_la_e_meile_atrese 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t 시계세기(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t 진동수;
static volatile uint32_t lepokisana_la_e_meile_data[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *자료위치, int khouto_ya_tlhaka, size_t 개수) { unsigned char *다음위치 = 자료위치; while (개수--) *다음위치++ = khouto_ya_tlhaka; return 자료위치; }
void *memcpy(void *boyo_data, const void *molokoloko_data, size_t 개수) { unsigned char *첫째값 = boyo_data; const unsigned char *둘째값 = molokoloko_data; while (개수--) *첫째값++ = *둘째값++; return boyo_data; }

static int lepokisana_la_e_meile(void) {
    uint32_t 요청 = (uint32_t)(uintptr_t)lepokisana_la_e_meile_data | 8;
    uint64_t Diriša = 시계세기();
    기억장벽();
    while (motšhene_ngwadiša(lepokisana_la_e_meile_atrese + 0x38) & 0x80000000u)
        if (시계세기() - Diriša > 진동수) return 0;
    motšhene_ngwadiša(lepokisana_la_e_meile_atrese + 0x20) = 요청;
    for (;;) {
        if (!(motšhene_ngwadiša(lepokisana_la_e_meile_atrese + 0x18) & 0x40000000u)) {
            uint32_t fetola = motšhene_ngwadiša(lepokisana_la_e_meile_atrese);
            if (fetola == 요청) { 기억장벽(); return lepokisana_la_e_meile_data[1] == 0x80000000u; }
        }
        if (시계세기() - Diriša > 진동수) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void 터미널바이트(unsigned);
extern int 터미널대기(void);
extern void 터미널가리킴(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../ya_kgole_boleng/ya_kgole_boleng.h"
static int 흐름목록;
static unsigned 직렬이전글자;
motšhene_Thalokontšu 보드흐름설정(motšhene_Thalokontšu 사용여부) { 흐름목록=사용여부!=0; return 0; }
motšhene_Thalokontšu 보드통로(motšhene_Thalokontšu mokero, motšhene_Thalokontšu khouto_ya_tlhaka) {
    if(흐름목록 && 자바셸출력((int32_t)mokero,(int32_t)(khouto_ya_tlhaka&255))) return 0;
    터미널바이트(khouto_ya_tlhaka&255);
    원격출력(khouto_ya_tlhaka&255);
    if ((khouto_ya_tlhaka&255)==10 && 직렬이전글자!=13) {
        while (motšhene_ngwadiša(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        motšhene_ngwadiša(직렬장치)=13;
    }
    직렬이전글자=khouto_ya_tlhaka&255;
    while (motšhene_ngwadiša(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    motšhene_ngwadiša(직렬장치) = (uint32_t)khouto_ya_tlhaka & 255;
    return 0;
}
motšhene_Thalokontšu 보드글자쓰기(motšhene_Thalokontšu khouto_ya_tlhaka) { return 보드통로(1,khouto_ya_tlhaka); }
motšhene_Thalokontšu 보드원시글자읽기(void) {
    int ya_kgole_tlhaka=원격입력();if(ya_kgole_tlhaka>=0)return ya_kgole_tlhaka;
    if (motšhene_ngwadiša(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t boleng = motšhene_ngwadiša(직렬장치);
    if (boleng & 0xf00) { motšhene_ngwadiša(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return boleng & 255;
}
motšhene_Thalokontšu 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char sephuthelwana_data[6];
    if(터미널대기())return (uint32_t)-4096;
    if(흐름목록){int32_t khouto_ya_tlhaka=자바셸입력();if(khouto_ya_tlhaka!=-3)return (uint32_t)khouto_ya_tlhaka;}
    for(;;){
        int khouto_ya_tlhaka=(int32_t)보드원시글자읽기();if(khouto_ya_tlhaka<0)return (uint32_t)khouto_ya_tlhaka;
        if(!꾸러미안쪽){if(khouto_ya_tlhaka!=30)return khouto_ya_tlhaka;꾸러미안쪽=1;사용량=0;continue;}
        sephuthelwana_data[사용량++]=khouto_ya_tlhaka;if(사용량<6)continue;꾸러미안쪽=0;
        if(sephuthelwana_data[0]==1)터미널가리킴(sephuthelwana_data[1],sephuthelwana_data[2]+sephuthelwana_data[3]*256,sephuthelwana_data[4]+sephuthelwana_data[5]*256);
        if(sephuthelwana_data[0]==2)터미널바로가기키(sephuthelwana_data[1]);
        if(sephuthelwana_data[0]==3)터미널입력방식(sephuthelwana_data[1]);
        if(터미널대기())return (uint32_t)-4096;
    }
}
motšhene_Thalokontšu 보드밀리초(void) { return (uint32_t)(시계세기() / (진동수 / 1000)); }
motšhene_Thalokontšu 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *molokoloko_data) { while (*molokoloko_data) 보드글자쓰기((unsigned char)*molokoloko_data++); }
static void 직렬열여섯진출력(motšhene_Thalokontšu 개수) { const char *열여섯진숫자 = "0123456789abcdef"; for (int molokoloko_data = 60; molokoloko_data >= 0; molokoloko_data -= 4) 보드글자쓰기(열여섯진숫자[(개수 >> molokoloko_data) & 15]); }
motšhene_Thalokontšu 보드멈추기(motšhene_Thalokontšu boemo_boleng) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(boemo_boleng); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); 보드멈추기(1); __builtin_unreachable(); }
void 보드예외(motšhene_Thalokontšu 예외상태, motšhene_Thalokontšu 명령위치, motšhene_Thalokontšu ye_e_phošagetšego_atrese) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(예외상태);
    직렬글출력(" PC="); 직렬열여섯진출력(명령위치); 직렬글출력(" FAR="); 직렬열여섯진출력(ye_e_phošagetšego_atrese);
    보드멈추기(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    lepokisana_la_e_meile_data[0]=32;lepokisana_la_e_meile_data[1]=0;lepokisana_la_e_meile_data[2]=0x10004;lepokisana_la_e_meile_data[3]=8;lepokisana_la_e_meile_data[4]=0;
    lepokisana_la_e_meile_data[5]=lepokisana_la_e_meile_data[6]=lepokisana_la_e_meile_data[7]=0;
    return lepokisana_la_e_meile()&&lepokisana_la_e_meile_data[4]==0x80000008u&&(lepokisana_la_e_meile_data[5]||lepokisana_la_e_meile_data[6]);
}
int 보드기계주소(unsigned char *atrese) {
    lepokisana_la_e_meile_data[0]=32;lepokisana_la_e_meile_data[1]=0;lepokisana_la_e_meile_data[2]=0x10003;lepokisana_la_e_meile_data[3]=8;lepokisana_la_e_meile_data[4]=0;
    lepokisana_la_e_meile_data[5]=lepokisana_la_e_meile_data[6]=lepokisana_la_e_meile_data[7]=0;
    if(!lepokisana_la_e_meile()||(lepokisana_la_e_meile_data[4]&0x80000000u)==0||(lepokisana_la_e_meile_data[4]&0xffff)!=6)return 0;
    const unsigned char *data=(const unsigned char*)&lepokisana_la_e_meile_data[5];unsigned 합=0;
    for(unsigned 순번=0;순번<6;순번++){atrese[순번]=data[순번];합|=data[순번];}return 합&&!(atrese[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(진동수));
    motšhene_ngwadiša(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    motšhene_ngwadiša(범용입출력 + 4) = (motšhene_ngwadiša(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    motšhene_ngwadiša(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. go_palelwa_boleng 시 config.txt의 48MHz를 사용한다.
    lepokisana_la_e_meile_data[0] = 36; lepokisana_la_e_meile_data[1] = 0; lepokisana_la_e_meile_data[2] = 0x38002; lepokisana_la_e_meile_data[3] = 12;
    lepokisana_la_e_meile_data[4] = 0; lepokisana_la_e_meile_data[5] = 2; lepokisana_la_e_meile_data[6] = 48000000; lepokisana_la_e_meile_data[7] = 0; lepokisana_la_e_meile_data[8] = 0;
    int 시계정상 = lepokisana_la_e_meile();
    uint32_t 속도 = 시계정상 && lepokisana_la_e_meile_data[6] >= 1843200 ? lepokisana_la_e_meile_data[6] : 48000000;
    lepokisana_la_e_meile_data[0]=32; lepokisana_la_e_meile_data[1]=0; lepokisana_la_e_meile_data[2]=0x10005; lepokisana_la_e_meile_data[3]=8; lepokisana_la_e_meile_data[4]=0;
    lepokisana_la_e_meile_data[5]=lepokisana_la_e_meile_data[6]=lepokisana_la_e_meile_data[7]=0;
    if (lepokisana_la_e_meile() && lepokisana_la_e_meile_data[4]==0x80000008u) 팔기억킬로바이트=lepokisana_la_e_meile_data[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    motšhene_ngwadiša(직렬장치 + 0x44) = 0x7ff;
    motšhene_ngwadiša(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    motšhene_ngwadiša(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    motšhene_ngwadiša(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    motšhene_ngwadiša(직렬장치 + 0x38) = 0;
    motšhene_ngwadiša(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
motšhene_Thalokontšu 보드파일전송(motšhene_Thalokontšu Mogato) { return (uint32_t)ftp_control((int)Mogato); }
motšhene_Thalokontšu 보드망상태(motšhene_Thalokontšu go_tsenya_tshedimošo_boleng, motšhene_Thalokontšu lokela) { return 망상태읽기(go_tsenya_tshedimošo_boleng, lokela); }
motšhene_Thalokontšu 보드망설정(motšhene_Thalokontšu Mogato, motšhene_Thalokontšu atrese, motšhene_Thalokontšu maseke_boleng, motšhene_Thalokontšu tsela_ya_netweke_boleng) { return (uint32_t)lomaganya_Netweke(Mogato, atrese, maseke_boleng, tsela_ya_netweke_boleng); }
motšhene_Thalokontšu 보드응답보내기(motšhene_Thalokontšu atrese, motšhene_Thalokontšu thulaganyo_boleng) { return (uint32_t)응답시험시작(atrese, thulaganyo_boleng); }
motšhene_Thalokontšu 보드응답읽기(motšhene_Thalokontšu go_tsenya_tshedimošo_boleng) { return (uint32_t)응답시험읽기(go_tsenya_tshedimošo_boleng); }
motšhene_Thalokontšu 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned lokela=0; lokela<32; lokela++) tswalela_Netweke(lokela);
    for (unsigned lokela=0; lokela<4; lokela++) 보드사용자제어(32+lokela);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (motšhene_ngwadiša(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    motšhene_ngwadiša(0xfe100020ul)=0x5a000000u | (motšhene_ngwadiša(0xfe100020ul)&~0xfffu) | 0x555;
    motšhene_ngwadiša(0xfe100024ul)=0x5a000000u | 10;
    motšhene_ngwadiša(0xfe10001cul)=0x5a000000u | (motšhene_ngwadiša(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

motšhene_Thalokontšu 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 현재 크기를 읽는다. */
    const uint32_t kwiri_boleng[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(kwiri_boleng)/4; 순번++) lepokisana_la_e_meile_data[순번] = kwiri_boleng[순번];
    if (lepokisana_la_e_meile() && lepokisana_la_e_meile_data[4] == 0x80000008u &&
        lepokisana_la_e_meile_data[5] >= 640 && lepokisana_la_e_meile_data[5] <= 1920 &&
        lepokisana_la_e_meile_data[6] >= 480 && lepokisana_la_e_meile_data[6] <= 1080) {
        요청너비 = lepokisana_la_e_meile_data[5]; 요청높이 = lepokisana_la_e_meile_data[6];
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
    for (size_t 순번 = 0; 순번 < sizeof(요청)/4; 순번++) lepokisana_la_e_meile_data[순번] = 요청[순번];
    // 위 메시지의 kgonthe_data 길이를 사용: 태그 추가 시 botelele_boleng 불일치를 방지한다.
    lepokisana_la_e_meile_data[0] = sizeof(요청);
    if (!lepokisana_la_e_meile()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 응답길이[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (lepokisana_la_e_meile_data[응답들[순번]] != (0x80000000u | 응답길이[순번])) return 0;
    uint32_t Bokamorago_boleng = lepokisana_la_e_meile_data[28] & 0x3fffffffu;
    uint32_t Bogolo = lepokisana_la_e_meile_data[29];
    uint32_t 받은너비 = lepokisana_la_e_meile_data[5], 받은높이 = lepokisana_la_e_meile_data[6], 받은줄간격 = lepokisana_la_e_meile_data[33];
    if (lepokisana_la_e_meile_data[15] != 32 || lepokisana_la_e_meile_data[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        lepokisana_la_e_meile_data[10] < 받은너비 || lepokisana_la_e_meile_data[11] < 받은높이 || lepokisana_la_e_meile_data[23] || lepokisana_la_e_meile_data[24] ||
        !Bokamorago_boleng || Bokamorago_boleng < 0x1000000 || (Bokamorago_boleng & 3) || 받은줄간격 < 받은너비 * 4 || (받은줄간격 & 3) ||
        (uint64_t)받은줄간격 * 받은높이 > Bogolo || (uint64_t)Bokamorago_boleng + Bogolo > 0x40000000u)
        return 0;
    보드그림준비((volatile uint32_t *)(uintptr_t)Bokamorago_boleng, 받은너비, 받은높이, 받은줄간격);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 threte_boleng. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } Kamano;
static Kamano 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int 실행중[3] = {1, 0, 0};
static int 현재작업;
extern void Kamano_fetogela(Kamano *, Kamano *);
extern void 자바작업(int32_t);
motšhene_Thalokontšu 보드양보(void) {
    network_poll();
    int 이전 = 현재작업, 다음 = (이전 + 1) % 3;
    while (다음 != 이전 && !실행중[다음]) 다음 = (다음 + 1) % 3;
    if (다음 != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (실행중[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        현재작업 = 다음;
        Kamano_fetogela(&작업문맥들[이전], &작업문맥들[다음]);
    }
    return 0;
}
static void mošomo_bula(void) {
    자바작업(현재작업);
    실행중[현재작업] = 0;
    보드양보();
    커널중단("finished task resumed");
}
motšhene_Thalokontšu 보드작업만들기(motšhene_Thalokontšu sešupi_boleng) {
    if (sešupi_boleng < 1 || sešupi_boleng > 2 || 실행중[sešupi_boleng]) return (uint32_t)-1;
    memset(&작업문맥들[sešupi_boleng], 0, sizeof(Kamano));
    *(uint64_t *)쌓임공간들[sešupi_boleng - 1] = 0x6b6f726f7373746bull;
    작업문맥들[sešupi_boleng].저장값[11] = (uintptr_t)mošomo_bula;
    작업문맥들[sešupi_boleng].저장값[12] = (uintptr_t)(쌓임공간들[sešupi_boleng - 1] + sizeof(쌓임공간들[0]));
    실행중[sešupi_boleng] = 1;
    return 0;
}
motšhene_Thalokontšu 보드작업상태(motšhene_Thalokontšu sešupi_boleng) { return sešupi_boleng < 3 ? 실행중[sešupi_boleng] : (uint32_t)-1; }
extern motšhene_Thalokontšu 미리번역기억조회(motšhene_Thalokontšu);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
motšhene_Thalokontšu 보드체계조회(motšhene_Thalokontšu go_tsenya_tshedimošo_boleng, motšhene_Thalokontšu lokela) {
    if (go_tsenya_tshedimošo_boleng==0) return 팔기억킬로바이트;
    if (go_tsenya_tshedimošo_boleng==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (go_tsenya_tshedimošo_boleng==2 || go_tsenya_tshedimošo_boleng==3) return 미리번역기억조회(go_tsenya_tshedimošo_boleng==3);
    if (go_tsenya_tshedimošo_boleng==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (go_tsenya_tshedimošo_boleng==5) return 80*1024; /* phethagatša_taelo 공간 16 MiB + 네 세션 보관 공간. */
    if (go_tsenya_tshedimošo_boleng>=20) return 사용자상태읽기(go_tsenya_tshedimošo_boleng-20, lokela);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[현재작업]; }
