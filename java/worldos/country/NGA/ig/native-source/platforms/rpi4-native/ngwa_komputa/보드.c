#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "òjìàrụ.h"
#include "../Netwọọkụ_ikpo/Netwọọkụ_ikpo.h"
typedef uintptr_t ngwa_komputa_Mkpụrụokwu;
#define 기계저장기(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define ìgbeozī_àdreèsì 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t 시계세기(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t 진동수;
static volatile uint32_t ìgbeozī_datà[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *자료위치, int koòdù_nkeakàrà, size_t 개수) { unsigned char *다음위치 = 자료위치; while (개수--) *다음위치++ = koòdù_nkeakàrà; return 자료위치; }
void *memcpy(void *ebemwèga_datà, const void *ùsòròokwū_datà, size_t 개수) { unsigned char *첫째값 = ebemwèga_datà; const unsigned char *둘째값 = ùsòròokwū_datà; while (개수--) *첫째값++ = *둘째값++; return ebemwèga_datà; }

static int ìgbeozī(void) {
    uint32_t 요청 = (uint32_t)(uintptr_t)ìgbeozī_datà | 8;
    uint64_t Bido = 시계세기();
    기억장벽();
    while (기계저장기(ìgbeozī_àdreèsì + 0x38) & 0x80000000u)
        if (시계세기() - Bido > 진동수) return 0;
    기계저장기(ìgbeozī_àdreèsì + 0x20) = 요청;
    for (;;) {
        if (!(기계저장기(ìgbeozī_àdreèsì + 0x18) & 0x40000000u)) {
            uint32_t nzaghachi = 기계저장기(ìgbeozī_àdreèsì);
            if (nzaghachi == 요청) { 기억장벽(); return ìgbeozī_datà[1] == 0x80000000u; }
        }
        if (시계세기() - Bido > 진동수) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void 터미널바이트(unsigned);
extern int 터미널대기(void);
extern void 터미널가리킴(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../ebe_dị̀anyā_valuu/ebe_dị̀anyā_valuu.h"
static int 흐름목록;
static unsigned 직렬이전글자;
ngwa_komputa_Mkpụrụokwu 보드흐름설정(ngwa_komputa_Mkpụrụokwu 사용여부) { 흐름목록=사용여부!=0; return 0; }
ngwa_komputa_Mkpụrụokwu 보드통로(ngwa_komputa_Mkpụrụokwu ọwa, ngwa_komputa_Mkpụrụokwu koòdù_nkeakàrà) {
    if(흐름목록 && 자바셸출력((int32_t)ọwa,(int32_t)(koòdù_nkeakàrà&255))) return 0;
    터미널바이트(koòdù_nkeakàrà&255);
    원격출력(koòdù_nkeakàrà&255);
    if ((koòdù_nkeakàrà&255)==10 && 직렬이전글자!=13) {
        while (기계저장기(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        기계저장기(직렬장치)=13;
    }
    직렬이전글자=koòdù_nkeakàrà&255;
    while (기계저장기(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    기계저장기(직렬장치) = (uint32_t)koòdù_nkeakàrà & 255;
    return 0;
}
ngwa_komputa_Mkpụrụokwu 보드글자쓰기(ngwa_komputa_Mkpụrụokwu koòdù_nkeakàrà) { return 보드통로(1,koòdù_nkeakàrà); }
ngwa_komputa_Mkpụrụokwu 보드원시글자읽기(void) {
    int ebe_dị̀anyā_mkpụrụedemede=원격입력();if(ebe_dị̀anyā_mkpụrụedemede>=0)return ebe_dị̀anyā_mkpụrụedemede;
    if (기계저장기(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t valuu = 기계저장기(직렬장치);
    if (valuu & 0xf00) { 기계저장기(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return valuu & 255;
}
ngwa_komputa_Mkpụrụokwu 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char ngwùgwù_datà[6];
    if(터미널대기())return (uint32_t)-4096;
    if(흐름목록){int32_t koòdù_nkeakàrà=자바셸입력();if(koòdù_nkeakàrà!=-3)return (uint32_t)koòdù_nkeakàrà;}
    for(;;){
        int koòdù_nkeakàrà=(int32_t)보드원시글자읽기();if(koòdù_nkeakàrà<0)return (uint32_t)koòdù_nkeakàrà;
        if(!꾸러미안쪽){if(koòdù_nkeakàrà!=30)return koòdù_nkeakàrà;꾸러미안쪽=1;사용량=0;continue;}
        ngwùgwù_datà[사용량++]=koòdù_nkeakàrà;if(사용량<6)continue;꾸러미안쪽=0;
        if(ngwùgwù_datà[0]==1)터미널가리킴(ngwùgwù_datà[1],ngwùgwù_datà[2]+ngwùgwù_datà[3]*256,ngwùgwù_datà[4]+ngwùgwù_datà[5]*256);
        if(ngwùgwù_datà[0]==2)터미널바로가기키(ngwùgwù_datà[1]);
        if(ngwùgwù_datà[0]==3)터미널입력방식(ngwùgwù_datà[1]);
        if(터미널대기())return (uint32_t)-4096;
    }
}
ngwa_komputa_Mkpụrụokwu 보드밀리초(void) { return (uint32_t)(시계세기() / (진동수 / 1000)); }
ngwa_komputa_Mkpụrụokwu 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *ùsòròokwū_datà) { while (*ùsòròokwū_datà) 보드글자쓰기((unsigned char)*ùsòròokwū_datà++); }
static void 직렬열여섯진출력(ngwa_komputa_Mkpụrụokwu 개수) { const char *열여섯진숫자 = "0123456789abcdef"; for (int ùsòròokwū_datà = 60; ùsòròokwū_datà >= 0; ùsòròokwū_datà -= 4) 보드글자쓰기(열여섯진숫자[(개수 >> ùsòròokwū_datà) & 15]); }
ngwa_komputa_Mkpụrụokwu 보드멈추기(ngwa_komputa_Mkpụrụokwu ọnọdụ_valuu) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(ọnọdụ_valuu); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); 보드멈추기(1); __builtin_unreachable(); }
void 보드예외(ngwa_komputa_Mkpụrụokwu 예외상태, ngwa_komputa_Mkpụrụokwu 명령위치, ngwa_komputa_Mkpụrụokwu abànihe_àdreèsì) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(예외상태);
    직렬글출력(" PC="); 직렬열여섯진출력(명령위치); 직렬글출력(" FAR="); 직렬열여섯진출력(abànihe_àdreèsì);
    보드멈추기(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    ìgbeozī_datà[0]=32;ìgbeozī_datà[1]=0;ìgbeozī_datà[2]=0x10004;ìgbeozī_datà[3]=8;ìgbeozī_datà[4]=0;
    ìgbeozī_datà[5]=ìgbeozī_datà[6]=ìgbeozī_datà[7]=0;
    return ìgbeozī()&&ìgbeozī_datà[4]==0x80000008u&&(ìgbeozī_datà[5]||ìgbeozī_datà[6]);
}
int 보드기계주소(unsigned char *àdreèsì) {
    ìgbeozī_datà[0]=32;ìgbeozī_datà[1]=0;ìgbeozī_datà[2]=0x10003;ìgbeozī_datà[3]=8;ìgbeozī_datà[4]=0;
    ìgbeozī_datà[5]=ìgbeozī_datà[6]=ìgbeozī_datà[7]=0;
    if(!ìgbeozī()||(ìgbeozī_datà[4]&0x80000000u)==0||(ìgbeozī_datà[4]&0xffff)!=6)return 0;
    const unsigned char *datà=(const unsigned char*)&ìgbeozī_datà[5];unsigned 합=0;
    for(unsigned 순번=0;순번<6;순번++){àdreèsì[순번]=datà[순번];합|=datà[순번];}return 합&&!(àdreèsì[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(진동수));
    기계저장기(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    기계저장기(범용입출력 + 4) = (기계저장기(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    기계저장기(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. ọdịdà_valuu 시 config.txt의 48MHz를 사용한다.
    ìgbeozī_datà[0] = 36; ìgbeozī_datà[1] = 0; ìgbeozī_datà[2] = 0x38002; ìgbeozī_datà[3] = 12;
    ìgbeozī_datà[4] = 0; ìgbeozī_datà[5] = 2; ìgbeozī_datà[6] = 48000000; ìgbeozī_datà[7] = 0; ìgbeozī_datà[8] = 0;
    int 시계정상 = ìgbeozī();
    uint32_t 속도 = 시계정상 && ìgbeozī_datà[6] >= 1843200 ? ìgbeozī_datà[6] : 48000000;
    ìgbeozī_datà[0]=32; ìgbeozī_datà[1]=0; ìgbeozī_datà[2]=0x10005; ìgbeozī_datà[3]=8; ìgbeozī_datà[4]=0;
    ìgbeozī_datà[5]=ìgbeozī_datà[6]=ìgbeozī_datà[7]=0;
    if (ìgbeozī() && ìgbeozī_datà[4]==0x80000008u) 팔기억킬로바이트=ìgbeozī_datà[6]/1024;
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
ngwa_komputa_Mkpụrụokwu 보드파일전송(ngwa_komputa_Mkpụrụokwu mmèm) { return (uint32_t)ftp_control((int)mmèm); }
ngwa_komputa_Mkpụrụokwu 보드망상태(ngwa_komputa_Mkpụrụokwu ndebà_valuu, ngwa_komputa_Mkpụrụokwu indèks) { return 망상태읽기(ndebà_valuu, indèks); }
ngwa_komputa_Mkpụrụokwu 보드망설정(ngwa_komputa_Mkpụrụokwu mmèm, ngwa_komputa_Mkpụrụokwu àdreèsì, ngwa_komputa_Mkpụrụokwu mkpù_valuu, ngwa_komputa_Mkpụrụokwu ụzọmbànye_valuu) { return (uint32_t)hàkọọ_ngwaāhụ_kọmputa_Netwọọkụ(mmèm, àdreèsì, mkpù_valuu, ụzọmbànye_valuu); }
ngwa_komputa_Mkpụrụokwu 보드응답보내기(ngwa_komputa_Mkpụrụokwu àdreèsì, ngwa_komputa_Mkpụrụokwu ùsòrò_valuu) { return (uint32_t)응답시험시작(àdreèsì, ùsòrò_valuu); }
ngwa_komputa_Mkpụrụokwu 보드응답읽기(ngwa_komputa_Mkpụrụokwu ndebà_valuu) { return (uint32_t)응답시험읽기(ndebà_valuu); }
ngwa_komputa_Mkpụrụokwu 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned indèks=0; indèks<32; indèks++) mmechi_Netwọọkụ(indèks);
    for (unsigned indèks=0; indèks<4; indèks++) 보드사용자제어(32+indèks);
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

ngwa_komputa_Mkpụrụokwu 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 현재 크기를 읽는다. */
    const uint32_t mgbaajụjụ_valuu[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(mgbaajụjụ_valuu)/4; 순번++) ìgbeozī_datà[순번] = mgbaajụjụ_valuu[순번];
    if (ìgbeozī() && ìgbeozī_datà[4] == 0x80000008u &&
        ìgbeozī_datà[5] >= 640 && ìgbeozī_datà[5] <= 1920 &&
        ìgbeozī_datà[6] >= 480 && ìgbeozī_datà[6] <= 1080) {
        요청너비 = ìgbeozī_datà[5]; 요청높이 = ìgbeozī_datà[6];
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
    for (size_t 순번 = 0; 순번 < sizeof(요청)/4; 순번++) ìgbeozī_datà[순번] = 요청[순번];
    // 위 메시지의 ǹdịnezie_datà 길이를 사용: 태그 추가 시 ogologo_valuu 불일치를 방지한다.
    ìgbeozī_datà[0] = sizeof(요청);
    if (!ìgbeozī()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 응답길이[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (ìgbeozī_datà[응답들[순번]] != (0x80000000u | 응답길이[순번])) return 0;
    uint32_t Bakgraụnd_valuu = ìgbeozī_datà[28] & 0x3fffffffu;
    uint32_t Ụhara = ìgbeozī_datà[29];
    uint32_t 받은너비 = ìgbeozī_datà[5], 받은높이 = ìgbeozī_datà[6], 받은줄간격 = ìgbeozī_datà[33];
    if (ìgbeozī_datà[15] != 32 || ìgbeozī_datà[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        ìgbeozī_datà[10] < 받은너비 || ìgbeozī_datà[11] < 받은높이 || ìgbeozī_datà[23] || ìgbeozī_datà[24] ||
        !Bakgraụnd_valuu || Bakgraụnd_valuu < 0x1000000 || (Bakgraụnd_valuu & 3) || 받은줄간격 < 받은너비 * 4 || (받은줄간격 & 3) ||
        (uint64_t)받은줄간격 * 받은높이 > Ụhara || (uint64_t)Bakgraụnd_valuu + Ụhara > 0x40000000u)
        return 0;
    보드그림준비((volatile uint32_t *)(uintptr_t)Bakgraụnd_valuu, 받은너비, 받은높이, 받은줄간격);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 treèd_valuu. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } Ọnọdụ;
static Ọnọdụ 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int 실행중[3] = {1, 0, 0};
static int 현재작업;
extern void Ọnọdụ_ngbanwụ(Ọnọdụ *, Ọnọdụ *);
extern void 자바작업(int32_t);
ngwa_komputa_Mkpụrụokwu 보드양보(void) {
    network_poll();
    int 이전 = 현재작업, 다음 = (이전 + 1) % 3;
    while (다음 != 이전 && !실행중[다음]) 다음 = (다음 + 1) % 3;
    if (다음 != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (실행중[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        현재작업 = 다음;
        Ọnọdụ_ngbanwụ(&작업문맥들[이전], &작업문맥들[다음]);
    }
    return 0;
}
static void ọrụ_mbido(void) {
    자바작업(현재작업);
    실행중[현재작업] = 0;
    보드양보();
    커널중단("finished task resumed");
}
ngwa_komputa_Mkpụrụokwu 보드작업만들기(ngwa_komputa_Mkpụrụokwu ihe_nkọwapụta_valuu) {
    if (ihe_nkọwapụta_valuu < 1 || ihe_nkọwapụta_valuu > 2 || 실행중[ihe_nkọwapụta_valuu]) return (uint32_t)-1;
    memset(&작업문맥들[ihe_nkọwapụta_valuu], 0, sizeof(Ọnọdụ));
    *(uint64_t *)쌓임공간들[ihe_nkọwapụta_valuu - 1] = 0x6b6f726f7373746bull;
    작업문맥들[ihe_nkọwapụta_valuu].저장값[11] = (uintptr_t)ọrụ_mbido;
    작업문맥들[ihe_nkọwapụta_valuu].저장값[12] = (uintptr_t)(쌓임공간들[ihe_nkọwapụta_valuu - 1] + sizeof(쌓임공간들[0]));
    실행중[ihe_nkọwapụta_valuu] = 1;
    return 0;
}
ngwa_komputa_Mkpụrụokwu 보드작업상태(ngwa_komputa_Mkpụrụokwu ihe_nkọwapụta_valuu) { return ihe_nkọwapụta_valuu < 3 ? 실행중[ihe_nkọwapụta_valuu] : (uint32_t)-1; }
extern ngwa_komputa_Mkpụrụokwu 미리번역기억조회(ngwa_komputa_Mkpụrụokwu);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
ngwa_komputa_Mkpụrụokwu 보드체계조회(ngwa_komputa_Mkpụrụokwu ndebà_valuu, ngwa_komputa_Mkpụrụokwu indèks) {
    if (ndebà_valuu==0) return 팔기억킬로바이트;
    if (ndebà_valuu==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (ndebà_valuu==2 || ndebà_valuu==3) return 미리번역기억조회(ndebà_valuu==3);
    if (ndebà_valuu==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (ndebà_valuu==5) return 80*1024; /* mee_nnyemiwu 공간 16 MiB + 네 세션 보관 공간. */
    if (ndebà_valuu>=20) return 사용자상태읽기(ndebà_valuu-20, indèks);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[현재작업]; }
