#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "modirisi.h"
#include "../Neteweke_kokoanyodinepe/Neteweke_kokoanyodinepe.h"
typedef uintptr_t motšhine_Lefoko;
#define motšhine_kwadisa(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define lebokoso_la_imeile_aterese 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t 시계세기(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t 진동수;
static volatile uint32_t lebokoso_la_imeile_tshedimosetso[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *자료위치, int khoutuletshwao, size_t 개수) { unsigned char *다음위치 = 자료위치; while (개수--) *다음위치++ = khoutuletshwao; return 자료위치; }
void *memcpy(void *bogorogelo_tshedimosetso, const void *dikwalwa_tshedimosetso, size_t 개수) { unsigned char *첫째값 = bogorogelo_tshedimosetso; const unsigned char *둘째값 = dikwalwa_tshedimosetso; while (개수--) *첫째값++ = *둘째값++; return bogorogelo_tshedimosetso; }

static int lebokoso_la_imeile(void) {
    uint32_t 요청 = (uint32_t)(uintptr_t)lebokoso_la_imeile_tshedimosetso | 8;
    uint64_t dirisa = 시계세기();
    기억장벽();
    while (motšhine_kwadisa(lebokoso_la_imeile_aterese + 0x38) & 0x80000000u)
        if (시계세기() - dirisa > 진동수) return 0;
    motšhine_kwadisa(lebokoso_la_imeile_aterese + 0x20) = 요청;
    for (;;) {
        if (!(motšhine_kwadisa(lebokoso_la_imeile_aterese + 0x18) & 0x40000000u)) {
            uint32_t araba = motšhine_kwadisa(lebokoso_la_imeile_aterese);
            if (araba == 요청) { 기억장벽(); return lebokoso_la_imeile_tshedimosetso[1] == 0x80000000u; }
        }
        if (시계세기() - dirisa > 진동수) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void 터미널바이트(unsigned);
extern int 터미널대기(void);
extern void 터미널가리킴(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../kgakala_Boleng/kgakala_Boleng.h"
static int 흐름목록;
static unsigned 직렬이전글자;
motšhine_Lefoko 보드흐름설정(motšhine_Lefoko 사용여부) { 흐름목록=사용여부!=0; return 0; }
motšhine_Lefoko 보드통로(motšhine_Lefoko mosele, motšhine_Lefoko khoutuletshwao) {
    if(흐름목록 && 자바셸출력((int32_t)mosele,(int32_t)(khoutuletshwao&255))) return 0;
    터미널바이트(khoutuletshwao&255);
    원격출력(khoutuletshwao&255);
    if ((khoutuletshwao&255)==10 && 직렬이전글자!=13) {
        while (motšhine_kwadisa(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        motšhine_kwadisa(직렬장치)=13;
    }
    직렬이전글자=khoutuletshwao&255;
    while (motšhine_kwadisa(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    motšhine_kwadisa(직렬장치) = (uint32_t)khoutuletshwao & 255;
    return 0;
}
motšhine_Lefoko 보드글자쓰기(motšhine_Lefoko khoutuletshwao) { return 보드통로(1,khoutuletshwao); }
motšhine_Lefoko 보드원시글자읽기(void) {
    int kgakala_Letshwao=원격입력();if(kgakala_Letshwao>=0)return kgakala_Letshwao;
    if (motšhine_kwadisa(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t Boleng = motšhine_kwadisa(직렬장치);
    if (Boleng & 0xf00) { motšhine_kwadisa(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return Boleng & 255;
}
motšhine_Lefoko 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char sephuthelwana_tshedimosetso[6];
    if(터미널대기())return (uint32_t)-4096;
    if(흐름목록){int32_t khoutuletshwao=자바셸입력();if(khoutuletshwao!=-3)return (uint32_t)khoutuletshwao;}
    for(;;){
        int khoutuletshwao=(int32_t)보드원시글자읽기();if(khoutuletshwao<0)return (uint32_t)khoutuletshwao;
        if(!꾸러미안쪽){if(khoutuletshwao!=30)return khoutuletshwao;꾸러미안쪽=1;사용량=0;continue;}
        sephuthelwana_tshedimosetso[사용량++]=khoutuletshwao;if(사용량<6)continue;꾸러미안쪽=0;
        if(sephuthelwana_tshedimosetso[0]==1)터미널가리킴(sephuthelwana_tshedimosetso[1],sephuthelwana_tshedimosetso[2]+sephuthelwana_tshedimosetso[3]*256,sephuthelwana_tshedimosetso[4]+sephuthelwana_tshedimosetso[5]*256);
        if(sephuthelwana_tshedimosetso[0]==2)터미널바로가기키(sephuthelwana_tshedimosetso[1]);
        if(sephuthelwana_tshedimosetso[0]==3)터미널입력방식(sephuthelwana_tshedimosetso[1]);
        if(터미널대기())return (uint32_t)-4096;
    }
}
motšhine_Lefoko 보드밀리초(void) { return (uint32_t)(시계세기() / (진동수 / 1000)); }
motšhine_Lefoko 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *dikwalwa_tshedimosetso) { while (*dikwalwa_tshedimosetso) 보드글자쓰기((unsigned char)*dikwalwa_tshedimosetso++); }
static void 직렬열여섯진출력(motšhine_Lefoko 개수) { const char *열여섯진숫자 = "0123456789abcdef"; for (int dikwalwa_tshedimosetso = 60; dikwalwa_tshedimosetso >= 0; dikwalwa_tshedimosetso -= 4) 보드글자쓰기(열여섯진숫자[(개수 >> dikwalwa_tshedimosetso) & 15]); }
motšhine_Lefoko 보드멈추기(motšhine_Lefoko kemo_Boleng) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(kemo_Boleng); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); 보드멈추기(1); __builtin_unreachable(); }
void 보드예외(motšhine_Lefoko 예외상태, motšhine_Lefoko 명령위치, motšhine_Lefoko Ga_e_a_siama_aterese) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(예외상태);
    직렬글출력(" PC="); 직렬열여섯진출력(명령위치); 직렬글출력(" FAR="); 직렬열여섯진출력(Ga_e_a_siama_aterese);
    보드멈추기(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    lebokoso_la_imeile_tshedimosetso[0]=32;lebokoso_la_imeile_tshedimosetso[1]=0;lebokoso_la_imeile_tshedimosetso[2]=0x10004;lebokoso_la_imeile_tshedimosetso[3]=8;lebokoso_la_imeile_tshedimosetso[4]=0;
    lebokoso_la_imeile_tshedimosetso[5]=lebokoso_la_imeile_tshedimosetso[6]=lebokoso_la_imeile_tshedimosetso[7]=0;
    return lebokoso_la_imeile()&&lebokoso_la_imeile_tshedimosetso[4]==0x80000008u&&(lebokoso_la_imeile_tshedimosetso[5]||lebokoso_la_imeile_tshedimosetso[6]);
}
int 보드기계주소(unsigned char *aterese) {
    lebokoso_la_imeile_tshedimosetso[0]=32;lebokoso_la_imeile_tshedimosetso[1]=0;lebokoso_la_imeile_tshedimosetso[2]=0x10003;lebokoso_la_imeile_tshedimosetso[3]=8;lebokoso_la_imeile_tshedimosetso[4]=0;
    lebokoso_la_imeile_tshedimosetso[5]=lebokoso_la_imeile_tshedimosetso[6]=lebokoso_la_imeile_tshedimosetso[7]=0;
    if(!lebokoso_la_imeile()||(lebokoso_la_imeile_tshedimosetso[4]&0x80000000u)==0||(lebokoso_la_imeile_tshedimosetso[4]&0xffff)!=6)return 0;
    const unsigned char *tshedimosetso=(const unsigned char*)&lebokoso_la_imeile_tshedimosetso[5];unsigned 합=0;
    for(unsigned 순번=0;순번<6;순번++){aterese[순번]=tshedimosetso[순번];합|=tshedimosetso[순번];}return 합&&!(aterese[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(진동수));
    motšhine_kwadisa(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    motšhine_kwadisa(범용입출력 + 4) = (motšhine_kwadisa(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    motšhine_kwadisa(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. palelo_Boleng 시 config.txt의 48MHz를 사용한다.
    lebokoso_la_imeile_tshedimosetso[0] = 36; lebokoso_la_imeile_tshedimosetso[1] = 0; lebokoso_la_imeile_tshedimosetso[2] = 0x38002; lebokoso_la_imeile_tshedimosetso[3] = 12;
    lebokoso_la_imeile_tshedimosetso[4] = 0; lebokoso_la_imeile_tshedimosetso[5] = 2; lebokoso_la_imeile_tshedimosetso[6] = 48000000; lebokoso_la_imeile_tshedimosetso[7] = 0; lebokoso_la_imeile_tshedimosetso[8] = 0;
    int 시계정상 = lebokoso_la_imeile();
    uint32_t 속도 = 시계정상 && lebokoso_la_imeile_tshedimosetso[6] >= 1843200 ? lebokoso_la_imeile_tshedimosetso[6] : 48000000;
    lebokoso_la_imeile_tshedimosetso[0]=32; lebokoso_la_imeile_tshedimosetso[1]=0; lebokoso_la_imeile_tshedimosetso[2]=0x10005; lebokoso_la_imeile_tshedimosetso[3]=8; lebokoso_la_imeile_tshedimosetso[4]=0;
    lebokoso_la_imeile_tshedimosetso[5]=lebokoso_la_imeile_tshedimosetso[6]=lebokoso_la_imeile_tshedimosetso[7]=0;
    if (lebokoso_la_imeile() && lebokoso_la_imeile_tshedimosetso[4]==0x80000008u) 팔기억킬로바이트=lebokoso_la_imeile_tshedimosetso[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    motšhine_kwadisa(직렬장치 + 0x44) = 0x7ff;
    motšhine_kwadisa(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    motšhine_kwadisa(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    motšhine_kwadisa(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    motšhine_kwadisa(직렬장치 + 0x38) = 0;
    motšhine_kwadisa(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
motšhine_Lefoko 보드파일전송(motšhine_Lefoko tiro) { return (uint32_t)ftp_control((int)tiro); }
motšhine_Lefoko 보드망상태(motšhine_Lefoko tsenyo_Boleng, motšhine_Lefoko tshupane) { return 망상태읽기(tsenyo_Boleng, tshupane); }
motšhine_Lefoko 보드망설정(motšhine_Lefoko tiro, motšhine_Lefoko aterese, motšhine_Lefoko mmaseke_Boleng, motšhine_Lefoko kgorotsamaiso_Boleng) { return (uint32_t)Rulaganya_Neteweke(tiro, aterese, mmaseke_Boleng, kgorotsamaiso_Boleng); }
motšhine_Lefoko 보드응답보내기(motšhine_Lefoko aterese, motšhine_Lefoko thulaganyo_Boleng) { return (uint32_t)응답시험시작(aterese, thulaganyo_Boleng); }
motšhine_Lefoko 보드응답읽기(motšhine_Lefoko tsenyo_Boleng) { return (uint32_t)응답시험읽기(tsenyo_Boleng); }
motšhine_Lefoko 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned tshupane=0; tshupane<32; tshupane++) tswala_Neteweke(tshupane);
    for (unsigned tshupane=0; tshupane<4; tshupane++) 보드사용자제어(32+tshupane);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (motšhine_kwadisa(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    motšhine_kwadisa(0xfe100020ul)=0x5a000000u | (motšhine_kwadisa(0xfe100020ul)&~0xfffu) | 0x555;
    motšhine_kwadisa(0xfe100024ul)=0x5a000000u | 10;
    motšhine_kwadisa(0xfe10001cul)=0x5a000000u | (motšhine_kwadisa(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

motšhine_Lefoko 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 ga_jaana_selwana 크기를 읽는다. */
    const uint32_t fenenkolola_Boleng[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(fenenkolola_Boleng)/4; 순번++) lebokoso_la_imeile_tshedimosetso[순번] = fenenkolola_Boleng[순번];
    if (lebokoso_la_imeile() && lebokoso_la_imeile_tshedimosetso[4] == 0x80000008u &&
        lebokoso_la_imeile_tshedimosetso[5] >= 640 && lebokoso_la_imeile_tshedimosetso[5] <= 1920 &&
        lebokoso_la_imeile_tshedimosetso[6] >= 480 && lebokoso_la_imeile_tshedimosetso[6] <= 1080) {
        요청너비 = lebokoso_la_imeile_tshedimosetso[5]; 요청높이 = lebokoso_la_imeile_tshedimosetso[6];
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
    for (size_t 순번 = 0; 순번 < sizeof(요청)/4; 순번++) lebokoso_la_imeile_tshedimosetso[순번] = 요청[순번];
    // 위 메시지의 tota_tshedimosetso 길이를 사용: 태그 추가 시 boleele_Boleng 불일치를 방지한다.
    lebokoso_la_imeile_tshedimosetso[0] = sizeof(요청);
    if (!lebokoso_la_imeile()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 응답길이[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (lebokoso_la_imeile_tshedimosetso[응답들[순번]] != (0x80000000u | 응답길이[순번])) return 0;
    uint32_t Lemorago_Boleng = lebokoso_la_imeile_tshedimosetso[28] & 0x3fffffffu;
    uint32_t lekanya = lebokoso_la_imeile_tshedimosetso[29];
    uint32_t 받은너비 = lebokoso_la_imeile_tshedimosetso[5], 받은높이 = lebokoso_la_imeile_tshedimosetso[6], 받은줄간격 = lebokoso_la_imeile_tshedimosetso[33];
    if (lebokoso_la_imeile_tshedimosetso[15] != 32 || lebokoso_la_imeile_tshedimosetso[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        lebokoso_la_imeile_tshedimosetso[10] < 받은너비 || lebokoso_la_imeile_tshedimosetso[11] < 받은높이 || lebokoso_la_imeile_tshedimosetso[23] || lebokoso_la_imeile_tshedimosetso[24] ||
        !Lemorago_Boleng || Lemorago_Boleng < 0x1000000 || (Lemorago_Boleng & 3) || 받은줄간격 < 받은너비 * 4 || (받은줄간격 & 3) ||
        (uint64_t)받은줄간격 * 받은높이 > lekanya || (uint64_t)Lemorago_Boleng + lekanya > 0x40000000u)
        return 0;
    보드그림준비((volatile uint32_t *)(uintptr_t)Lemorago_Boleng, 받은너비, 받은높이, 받은줄간격);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 tlhale_Boleng. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } bokao;
static bokao 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int 실행중[3] = {1, 0, 0};
static int ga_jaana_Tiro;
extern void bokao_fetola(bokao *, bokao *);
extern void 자바작업(int32_t);
motšhine_Lefoko 보드양보(void) {
    network_poll();
    int 이전 = ga_jaana_Tiro, 다음 = (이전 + 1) % 3;
    while (다음 != 이전 && !실행중[다음]) 다음 = (다음 + 1) % 3;
    if (다음 != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (실행중[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        ga_jaana_Tiro = 다음;
        bokao_fetola(&작업문맥들[이전], &작업문맥들[다음]);
    }
    return 0;
}
static void Tiro_tshimologosešwa(void) {
    자바작업(ga_jaana_Tiro);
    실행중[ga_jaana_Tiro] = 0;
    보드양보();
    커널중단("finished task resumed");
}
motšhine_Lefoko 보드작업만들기(motšhine_Lefoko setlhaodi_Boleng) {
    if (setlhaodi_Boleng < 1 || setlhaodi_Boleng > 2 || 실행중[setlhaodi_Boleng]) return (uint32_t)-1;
    memset(&작업문맥들[setlhaodi_Boleng], 0, sizeof(bokao));
    *(uint64_t *)쌓임공간들[setlhaodi_Boleng - 1] = 0x6b6f726f7373746bull;
    작업문맥들[setlhaodi_Boleng].저장값[11] = (uintptr_t)Tiro_tshimologosešwa;
    작업문맥들[setlhaodi_Boleng].저장값[12] = (uintptr_t)(쌓임공간들[setlhaodi_Boleng - 1] + sizeof(쌓임공간들[0]));
    실행중[setlhaodi_Boleng] = 1;
    return 0;
}
motšhine_Lefoko 보드작업상태(motšhine_Lefoko setlhaodi_Boleng) { return setlhaodi_Boleng < 3 ? 실행중[setlhaodi_Boleng] : (uint32_t)-1; }
extern motšhine_Lefoko 미리번역기억조회(motšhine_Lefoko);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
motšhine_Lefoko 보드체계조회(motšhine_Lefoko tsenyo_Boleng, motšhine_Lefoko tshupane) {
    if (tsenyo_Boleng==0) return 팔기억킬로바이트;
    if (tsenyo_Boleng==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (tsenyo_Boleng==2 || tsenyo_Boleng==3) return 미리번역기억조회(tsenyo_Boleng==3);
    if (tsenyo_Boleng==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (tsenyo_Boleng==5) return 80*1024; /* diragatsa_Taelo 공간 16 MiB + 네 세션 보관 공간. */
    if (tsenyo_Boleng>=20) return 사용자상태읽기(tsenyo_Boleng-20, tshupane);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[ga_jaana_Tiro]; }
