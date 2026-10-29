#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "ukoresha.h"
#include "../Urusobemiyoboro_Ikirundo/Urusobemiyoboro_Ikirundo.h"
typedef uintptr_t imashini_Ijambo;
#define 기계저장기(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define agasanduku_k_amabaruwa_aderesi 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t 시계세기(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t 진동수;
static volatile uint32_t agasanduku_k_amabaruwa_amakurushingiro[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *자료위치, int 문자값, size_t 개수) { unsigned char *다음위치 = 자료위치; while (개수--) *다음위치++ = 문자값; return 자료위치; }
void *memcpy(void *aho_ijya_amakurushingiro, const void *igicenteruro_amakurushingiro, size_t 개수) { unsigned char *첫째값 = aho_ijya_amakurushingiro; const unsigned char *둘째값 = igicenteruro_amakurushingiro; while (개수--) *첫째값++ = *둘째값++; return aho_ijya_amakurushingiro; }

static int agasanduku_k_amabaruwa(void) {
    uint32_t 요청 = (uint32_t)(uintptr_t)agasanduku_k_amabaruwa_amakurushingiro | 8;
    uint64_t ihuriro = 시계세기();
    기억장벽();
    while (기계저장기(agasanduku_k_amabaruwa_aderesi + 0x38) & 0x80000000u)
        if (시계세기() - ihuriro > 진동수) return 0;
    기계저장기(agasanduku_k_amabaruwa_aderesi + 0x20) = 요청;
    for (;;) {
        if (!(기계저장기(agasanduku_k_amabaruwa_aderesi + 0x18) & 0x40000000u)) {
            uint32_t gusubiza = 기계저장기(agasanduku_k_amabaruwa_aderesi);
            if (gusubiza == 요청) { 기억장벽(); return agasanduku_k_amabaruwa_amakurushingiro[1] == 0x80000000u; }
        }
        if (시계세기() - ihuriro > 진동수) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void 터미널바이트(unsigned);
extern int 터미널대기(void);
extern void 터미널가리킴(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../kure_agaciro/kure_agaciro.h"
static int 흐름목록;
static unsigned 직렬이전글자;
imashini_Ijambo 보드흐름설정(imashini_Ijambo 사용여부) { 흐름목록=사용여부!=0; return 0; }
imashini_Ijambo 보드통로(imashini_Ijambo umurongo_c1b5826f, imashini_Ijambo 문자값) {
    if(흐름목록 && 자바셸출력((int32_t)umurongo_c1b5826f,(int32_t)(문자값&255))) return 0;
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
imashini_Ijambo 보드글자쓰기(imashini_Ijambo 문자값) { return 보드통로(1,문자값); }
imashini_Ijambo 보드원시글자읽기(void) {
    int kure_inyuguti=원격입력();if(kure_inyuguti>=0)return kure_inyuguti;
    if (기계저장기(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t agaciro = 기계저장기(직렬장치);
    if (agaciro & 0xf00) { 기계저장기(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return agaciro & 255;
}
imashini_Ijambo 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char ipaki_amakurushingiro[6];
    if(터미널대기())return (uint32_t)-4096;
    if(흐름목록){int32_t 문자값=자바셸입력();if(문자값!=-3)return (uint32_t)문자값;}
    for(;;){
        int 문자값=(int32_t)보드원시글자읽기();if(문자값<0)return (uint32_t)문자값;
        if(!꾸러미안쪽){if(문자값!=30)return 문자값;꾸러미안쪽=1;사용량=0;continue;}
        ipaki_amakurushingiro[사용량++]=문자값;if(사용량<6)continue;꾸러미안쪽=0;
        if(ipaki_amakurushingiro[0]==1)터미널가리킴(ipaki_amakurushingiro[1],ipaki_amakurushingiro[2]+ipaki_amakurushingiro[3]*256,ipaki_amakurushingiro[4]+ipaki_amakurushingiro[5]*256);
        if(ipaki_amakurushingiro[0]==2)터미널바로가기키(ipaki_amakurushingiro[1]);
        if(ipaki_amakurushingiro[0]==3)터미널입력방식(ipaki_amakurushingiro[1]);
        if(터미널대기())return (uint32_t)-4096;
    }
}
imashini_Ijambo 보드밀리초(void) { return (uint32_t)(시계세기() / (진동수 / 1000)); }
imashini_Ijambo 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *igicenteruro_amakurushingiro) { while (*igicenteruro_amakurushingiro) 보드글자쓰기((unsigned char)*igicenteruro_amakurushingiro++); }
static void 직렬열여섯진출력(imashini_Ijambo 개수) { const char *열여섯진숫자 = "0123456789abcdef"; for (int igicenteruro_amakurushingiro = 60; igicenteruro_amakurushingiro >= 0; igicenteruro_amakurushingiro -= 4) 보드글자쓰기(열여섯진숫자[(개수 >> igicenteruro_amakurushingiro) & 15]); }
imashini_Ijambo 보드멈추기(imashini_Ijambo imimerere_agaciro) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(imimerere_agaciro); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); 보드멈추기(1); __builtin_unreachable(); }
void 보드예외(imashini_Ijambo 예외상태, imashini_Ijambo 명령위치, imashini_Ijambo kitemewe_aderesi) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(예외상태);
    직렬글출력(" PC="); 직렬열여섯진출력(명령위치); 직렬글출력(" FAR="); 직렬열여섯진출력(kitemewe_aderesi);
    보드멈추기(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    agasanduku_k_amabaruwa_amakurushingiro[0]=32;agasanduku_k_amabaruwa_amakurushingiro[1]=0;agasanduku_k_amabaruwa_amakurushingiro[2]=0x10004;agasanduku_k_amabaruwa_amakurushingiro[3]=8;agasanduku_k_amabaruwa_amakurushingiro[4]=0;
    agasanduku_k_amabaruwa_amakurushingiro[5]=agasanduku_k_amabaruwa_amakurushingiro[6]=agasanduku_k_amabaruwa_amakurushingiro[7]=0;
    return agasanduku_k_amabaruwa()&&agasanduku_k_amabaruwa_amakurushingiro[4]==0x80000008u&&(agasanduku_k_amabaruwa_amakurushingiro[5]||agasanduku_k_amabaruwa_amakurushingiro[6]);
}
int 보드기계주소(unsigned char *aderesi) {
    agasanduku_k_amabaruwa_amakurushingiro[0]=32;agasanduku_k_amabaruwa_amakurushingiro[1]=0;agasanduku_k_amabaruwa_amakurushingiro[2]=0x10003;agasanduku_k_amabaruwa_amakurushingiro[3]=8;agasanduku_k_amabaruwa_amakurushingiro[4]=0;
    agasanduku_k_amabaruwa_amakurushingiro[5]=agasanduku_k_amabaruwa_amakurushingiro[6]=agasanduku_k_amabaruwa_amakurushingiro[7]=0;
    if(!agasanduku_k_amabaruwa()||(agasanduku_k_amabaruwa_amakurushingiro[4]&0x80000000u)==0||(agasanduku_k_amabaruwa_amakurushingiro[4]&0xffff)!=6)return 0;
    const unsigned char *amakurushingiro=(const unsigned char*)&agasanduku_k_amabaruwa_amakurushingiro[5];unsigned 합=0;
    for(unsigned 순번=0;순번<6;순번++){aderesi[순번]=amakurushingiro[순번];합|=amakurushingiro[순번];}return 합&&!(aderesi[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(진동수));
    기계저장기(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    기계저장기(범용입출력 + 4) = (기계저장기(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    기계저장기(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. kudakora_agaciro 시 config.txt의 48MHz를 사용한다.
    agasanduku_k_amabaruwa_amakurushingiro[0] = 36; agasanduku_k_amabaruwa_amakurushingiro[1] = 0; agasanduku_k_amabaruwa_amakurushingiro[2] = 0x38002; agasanduku_k_amabaruwa_amakurushingiro[3] = 12;
    agasanduku_k_amabaruwa_amakurushingiro[4] = 0; agasanduku_k_amabaruwa_amakurushingiro[5] = 2; agasanduku_k_amabaruwa_amakurushingiro[6] = 48000000; agasanduku_k_amabaruwa_amakurushingiro[7] = 0; agasanduku_k_amabaruwa_amakurushingiro[8] = 0;
    int 시계정상 = agasanduku_k_amabaruwa();
    uint32_t 속도 = 시계정상 && agasanduku_k_amabaruwa_amakurushingiro[6] >= 1843200 ? agasanduku_k_amabaruwa_amakurushingiro[6] : 48000000;
    agasanduku_k_amabaruwa_amakurushingiro[0]=32; agasanduku_k_amabaruwa_amakurushingiro[1]=0; agasanduku_k_amabaruwa_amakurushingiro[2]=0x10005; agasanduku_k_amabaruwa_amakurushingiro[3]=8; agasanduku_k_amabaruwa_amakurushingiro[4]=0;
    agasanduku_k_amabaruwa_amakurushingiro[5]=agasanduku_k_amabaruwa_amakurushingiro[6]=agasanduku_k_amabaruwa_amakurushingiro[7]=0;
    if (agasanduku_k_amabaruwa() && agasanduku_k_amabaruwa_amakurushingiro[4]==0x80000008u) 팔기억킬로바이트=agasanduku_k_amabaruwa_amakurushingiro[6]/1024;
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
imashini_Ijambo 보드파일전송(imashini_Ijambo Igikorwa) { return (uint32_t)ftp_control((int)Igikorwa); }
imashini_Ijambo 보드망상태(imashini_Ijambo icyinjizwa_agaciro, imashini_Ijambo umugerekashakiro) { return 망상태읽기(icyinjizwa_agaciro, umugerekashakiro); }
imashini_Ijambo 보드망설정(imashini_Ijambo Igikorwa, imashini_Ijambo aderesi, imashini_Ijambo masiki_agaciro, imashini_Ijambo muhuzaporotokore_agaciro) { return (uint32_t)kuboneza_Urusobemiyoboro(Igikorwa, aderesi, masiki_agaciro, muhuzaporotokore_agaciro); }
imashini_Ijambo 보드응답보내기(imashini_Ijambo aderesi, imashini_Ijambo umujyo_agaciro) { return (uint32_t)응답시험시작(aderesi, umujyo_agaciro); }
imashini_Ijambo 보드응답읽기(imashini_Ijambo icyinjizwa_agaciro) { return (uint32_t)응답시험읽기(icyinjizwa_agaciro); }
imashini_Ijambo 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned umugerekashakiro=0; umugerekashakiro<32; umugerekashakiro++) gufunga_Urusobemiyoboro(umugerekashakiro);
    for (unsigned umugerekashakiro=0; umugerekashakiro<4; umugerekashakiro++) 보드사용자제어(32+umugerekashakiro);
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

imashini_Ijambo 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 현재 크기를 읽는다. */
    const uint32_t isaba_agaciro[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(isaba_agaciro)/4; 순번++) agasanduku_k_amabaruwa_amakurushingiro[순번] = isaba_agaciro[순번];
    if (agasanduku_k_amabaruwa() && agasanduku_k_amabaruwa_amakurushingiro[4] == 0x80000008u &&
        agasanduku_k_amabaruwa_amakurushingiro[5] >= 640 && agasanduku_k_amabaruwa_amakurushingiro[5] <= 1920 &&
        agasanduku_k_amabaruwa_amakurushingiro[6] >= 480 && agasanduku_k_amabaruwa_amakurushingiro[6] <= 1080) {
        요청너비 = agasanduku_k_amabaruwa_amakurushingiro[5]; 요청높이 = agasanduku_k_amabaruwa_amakurushingiro[6];
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
    for (size_t 순번 = 0; 순번 < sizeof(요청)/4; 순번++) agasanduku_k_amabaruwa_amakurushingiro[순번] = 요청[순번];
    // 위 메시지의 nyakuri_amakurushingiro 길이를 사용: 태그 추가 시 uburebure_agaciro 불일치를 방지한다.
    agasanduku_k_amabaruwa_amakurushingiro[0] = sizeof(요청);
    if (!agasanduku_k_amabaruwa()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 응답길이[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (agasanduku_k_amabaruwa_amakurushingiro[응답들[순번]] != (0x80000000u | 응답길이[순번])) return 0;
    uint32_t Imbuganyuma_agaciro = agasanduku_k_amabaruwa_amakurushingiro[28] & 0x3fffffffu;
    uint32_t Ingano = agasanduku_k_amabaruwa_amakurushingiro[29];
    uint32_t 받은너비 = agasanduku_k_amabaruwa_amakurushingiro[5], 받은높이 = agasanduku_k_amabaruwa_amakurushingiro[6], 받은줄간격 = agasanduku_k_amabaruwa_amakurushingiro[33];
    if (agasanduku_k_amabaruwa_amakurushingiro[15] != 32 || agasanduku_k_amabaruwa_amakurushingiro[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        agasanduku_k_amabaruwa_amakurushingiro[10] < 받은너비 || agasanduku_k_amabaruwa_amakurushingiro[11] < 받은높이 || agasanduku_k_amabaruwa_amakurushingiro[23] || agasanduku_k_amabaruwa_amakurushingiro[24] ||
        !Imbuganyuma_agaciro || Imbuganyuma_agaciro < 0x1000000 || (Imbuganyuma_agaciro & 3) || 받은줄간격 < 받은너비 * 4 || (받은줄간격 & 3) ||
        (uint64_t)받은줄간격 * 받은높이 > Ingano || (uint64_t)Imbuganyuma_agaciro + Ingano > 0x40000000u)
        return 0;
    보드그림준비((volatile uint32_t *)(uintptr_t)Imbuganyuma_agaciro, 받은너비, 받은높이, 받은줄간격);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 mugenaporogaramu_agaciro. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } Imikoreshereze;
static Imikoreshereze 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int 실행중[3] = {1, 0, 0};
static int 현재작업;
extern void Imikoreshereze_guhinduranya(Imikoreshereze *, Imikoreshereze *);
extern void 자바작업(int32_t);
imashini_Ijambo 보드양보(void) {
    network_poll();
    int 이전 = 현재작업, 다음 = (이전 + 1) % 3;
    while (다음 != 이전 && !실행중[다음]) 다음 = (다음 + 1) % 3;
    if (다음 != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (실행중[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        현재작업 = 다음;
        Imikoreshereze_guhinduranya(&작업문맥들[이전], &작업문맥들[다음]);
    }
    return 0;
}
static void umukoro_iyatsa(void) {
    자바작업(현재작업);
    실행중[현재작업] = 0;
    보드양보();
    커널중단("finished task resumed");
}
imashini_Ijambo 보드작업만들기(imashini_Ijambo indanga_agaciro) {
    if (indanga_agaciro < 1 || indanga_agaciro > 2 || 실행중[indanga_agaciro]) return (uint32_t)-1;
    memset(&작업문맥들[indanga_agaciro], 0, sizeof(Imikoreshereze));
    *(uint64_t *)쌓임공간들[indanga_agaciro - 1] = 0x6b6f726f7373746bull;
    작업문맥들[indanga_agaciro].저장값[11] = (uintptr_t)umukoro_iyatsa;
    작업문맥들[indanga_agaciro].저장값[12] = (uintptr_t)(쌓임공간들[indanga_agaciro - 1] + sizeof(쌓임공간들[0]));
    실행중[indanga_agaciro] = 1;
    return 0;
}
imashini_Ijambo 보드작업상태(imashini_Ijambo indanga_agaciro) { return indanga_agaciro < 3 ? 실행중[indanga_agaciro] : (uint32_t)-1; }
extern imashini_Ijambo 미리번역기억조회(imashini_Ijambo);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
imashini_Ijambo 보드체계조회(imashini_Ijambo icyinjizwa_agaciro, imashini_Ijambo umugerekashakiro) {
    if (icyinjizwa_agaciro==0) return 팔기억킬로바이트;
    if (icyinjizwa_agaciro==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (icyinjizwa_agaciro==2 || icyinjizwa_agaciro==3) return 미리번역기억조회(icyinjizwa_agaciro==3);
    if (icyinjizwa_agaciro==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (icyinjizwa_agaciro==5) return 80*1024; /* gukora_ibwiriza 공간 16 MiB + 네 세션 보관 공간. */
    if (icyinjizwa_agaciro>=20) return 사용자상태읽기(icyinjizwa_agaciro-20, umugerekashakiro);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[현재작업]; }
