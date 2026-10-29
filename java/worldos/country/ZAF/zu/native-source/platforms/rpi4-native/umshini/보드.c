#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "umsebenzisi.h"
#include "../iNethiwekhi_Isitaki/iNethiwekhi_Isitaki.h"
typedef uintptr_t umshini_Amagama;
#define umshini_bhalisa(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define ibhokisi_leposi_ikheli 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t 시계세기(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t 진동수;
static volatile uint32_t ibhokisi_leposi_imininingwane[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *자료위치, int ikhodi_yohlamvu, size_t 개수) { unsigned char *다음위치 = 자료위치; while (개수--) *다음위치++ = ikhodi_yohlamvu; return 자료위치; }
void *memcpy(void *isikhumulo_imininingwane, const void *uchunge_imininingwane, size_t 개수) { unsigned char *첫째값 = isikhumulo_imininingwane; const unsigned char *둘째값 = uchunge_imininingwane; while (개수--) *첫째값++ = *둘째값++; return isikhumulo_imininingwane; }

static int ibhokisi_leposi(void) {
    uint32_t 요청 = (uint32_t)(uintptr_t)ibhokisi_leposi_imininingwane | 8;
    uint64_t Sebenzisa = 시계세기();
    기억장벽();
    while (umshini_bhalisa(ibhokisi_leposi_ikheli + 0x38) & 0x80000000u)
        if (시계세기() - Sebenzisa > 진동수) return 0;
    umshini_bhalisa(ibhokisi_leposi_ikheli + 0x20) = 요청;
    for (;;) {
        if (!(umshini_bhalisa(ibhokisi_leposi_ikheli + 0x18) & 0x40000000u)) {
            uint32_t phendula = umshini_bhalisa(ibhokisi_leposi_ikheli);
            if (phendula == 요청) { 기억장벽(); return ibhokisi_leposi_imininingwane[1] == 0x80000000u; }
        }
        if (시계세기() - Sebenzisa > 진동수) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void 터미널바이트(unsigned);
extern int 터미널대기(void);
extern void 터미널가리킴(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../kude_inani/kude_inani.h"
static int 흐름목록;
static unsigned 직렬이전글자;
umshini_Amagama 보드흐름설정(umshini_Amagama 사용여부) { 흐름목록=사용여부!=0; return 0; }
umshini_Amagama 보드통로(umshini_Amagama umgudu, umshini_Amagama ikhodi_yohlamvu) {
    if(흐름목록 && 자바셸출력((int32_t)umgudu,(int32_t)(ikhodi_yohlamvu&255))) return 0;
    터미널바이트(ikhodi_yohlamvu&255);
    원격출력(ikhodi_yohlamvu&255);
    if ((ikhodi_yohlamvu&255)==10 && 직렬이전글자!=13) {
        while (umshini_bhalisa(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        umshini_bhalisa(직렬장치)=13;
    }
    직렬이전글자=ikhodi_yohlamvu&255;
    while (umshini_bhalisa(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    umshini_bhalisa(직렬장치) = (uint32_t)ikhodi_yohlamvu & 255;
    return 0;
}
umshini_Amagama 보드글자쓰기(umshini_Amagama ikhodi_yohlamvu) { return 보드통로(1,ikhodi_yohlamvu); }
umshini_Amagama 보드원시글자읽기(void) {
    int kude_uhlamvusimo=원격입력();if(kude_uhlamvusimo>=0)return kude_uhlamvusimo;
    if (umshini_bhalisa(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t inani = umshini_bhalisa(직렬장치);
    if (inani & 0xf00) { umshini_bhalisa(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return inani & 255;
}
umshini_Amagama 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char iphakethe_imininingwane[6];
    if(터미널대기())return (uint32_t)-4096;
    if(흐름목록){int32_t ikhodi_yohlamvu=자바셸입력();if(ikhodi_yohlamvu!=-3)return (uint32_t)ikhodi_yohlamvu;}
    for(;;){
        int ikhodi_yohlamvu=(int32_t)보드원시글자읽기();if(ikhodi_yohlamvu<0)return (uint32_t)ikhodi_yohlamvu;
        if(!꾸러미안쪽){if(ikhodi_yohlamvu!=30)return ikhodi_yohlamvu;꾸러미안쪽=1;사용량=0;continue;}
        iphakethe_imininingwane[사용량++]=ikhodi_yohlamvu;if(사용량<6)continue;꾸러미안쪽=0;
        if(iphakethe_imininingwane[0]==1)터미널가리킴(iphakethe_imininingwane[1],iphakethe_imininingwane[2]+iphakethe_imininingwane[3]*256,iphakethe_imininingwane[4]+iphakethe_imininingwane[5]*256);
        if(iphakethe_imininingwane[0]==2)터미널바로가기키(iphakethe_imininingwane[1]);
        if(iphakethe_imininingwane[0]==3)터미널입력방식(iphakethe_imininingwane[1]);
        if(터미널대기())return (uint32_t)-4096;
    }
}
umshini_Amagama 보드밀리초(void) { return (uint32_t)(시계세기() / (진동수 / 1000)); }
umshini_Amagama 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *uchunge_imininingwane) { while (*uchunge_imininingwane) 보드글자쓰기((unsigned char)*uchunge_imininingwane++); }
static void 직렬열여섯진출력(umshini_Amagama 개수) { const char *열여섯진숫자 = "0123456789abcdef"; for (int uchunge_imininingwane = 60; uchunge_imininingwane >= 0; uchunge_imininingwane -= 4) 보드글자쓰기(열여섯진숫자[(개수 >> uchunge_imininingwane) & 15]); }
umshini_Amagama 보드멈추기(umshini_Amagama isimo_inani) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(isimo_inani); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); 보드멈추기(1); __builtin_unreachable(); }
void 보드예외(umshini_Amagama 예외상태, umshini_Amagama 명령위치, umshini_Amagama akusikho_ikheli) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(예외상태);
    직렬글출력(" PC="); 직렬열여섯진출력(명령위치); 직렬글출력(" FAR="); 직렬열여섯진출력(akusikho_ikheli);
    보드멈추기(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    ibhokisi_leposi_imininingwane[0]=32;ibhokisi_leposi_imininingwane[1]=0;ibhokisi_leposi_imininingwane[2]=0x10004;ibhokisi_leposi_imininingwane[3]=8;ibhokisi_leposi_imininingwane[4]=0;
    ibhokisi_leposi_imininingwane[5]=ibhokisi_leposi_imininingwane[6]=ibhokisi_leposi_imininingwane[7]=0;
    return ibhokisi_leposi()&&ibhokisi_leposi_imininingwane[4]==0x80000008u&&(ibhokisi_leposi_imininingwane[5]||ibhokisi_leposi_imininingwane[6]);
}
int 보드기계주소(unsigned char *ikheli) {
    ibhokisi_leposi_imininingwane[0]=32;ibhokisi_leposi_imininingwane[1]=0;ibhokisi_leposi_imininingwane[2]=0x10003;ibhokisi_leposi_imininingwane[3]=8;ibhokisi_leposi_imininingwane[4]=0;
    ibhokisi_leposi_imininingwane[5]=ibhokisi_leposi_imininingwane[6]=ibhokisi_leposi_imininingwane[7]=0;
    if(!ibhokisi_leposi()||(ibhokisi_leposi_imininingwane[4]&0x80000000u)==0||(ibhokisi_leposi_imininingwane[4]&0xffff)!=6)return 0;
    const unsigned char *imininingwane=(const unsigned char*)&ibhokisi_leposi_imininingwane[5];unsigned 합=0;
    for(unsigned 순번=0;순번<6;순번++){ikheli[순번]=imininingwane[순번];합|=imininingwane[순번];}return 합&&!(ikheli[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(진동수));
    umshini_bhalisa(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    umshini_bhalisa(범용입출력 + 4) = (umshini_bhalisa(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    umshini_bhalisa(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. ukwehluleka_inani 시 config.txt의 48MHz를 사용한다.
    ibhokisi_leposi_imininingwane[0] = 36; ibhokisi_leposi_imininingwane[1] = 0; ibhokisi_leposi_imininingwane[2] = 0x38002; ibhokisi_leposi_imininingwane[3] = 12;
    ibhokisi_leposi_imininingwane[4] = 0; ibhokisi_leposi_imininingwane[5] = 2; ibhokisi_leposi_imininingwane[6] = 48000000; ibhokisi_leposi_imininingwane[7] = 0; ibhokisi_leposi_imininingwane[8] = 0;
    int 시계정상 = ibhokisi_leposi();
    uint32_t 속도 = 시계정상 && ibhokisi_leposi_imininingwane[6] >= 1843200 ? ibhokisi_leposi_imininingwane[6] : 48000000;
    ibhokisi_leposi_imininingwane[0]=32; ibhokisi_leposi_imininingwane[1]=0; ibhokisi_leposi_imininingwane[2]=0x10005; ibhokisi_leposi_imininingwane[3]=8; ibhokisi_leposi_imininingwane[4]=0;
    ibhokisi_leposi_imininingwane[5]=ibhokisi_leposi_imininingwane[6]=ibhokisi_leposi_imininingwane[7]=0;
    if (ibhokisi_leposi() && ibhokisi_leposi_imininingwane[4]==0x80000008u) 팔기억킬로바이트=ibhokisi_leposi_imininingwane[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    umshini_bhalisa(직렬장치 + 0x44) = 0x7ff;
    umshini_bhalisa(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    umshini_bhalisa(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    umshini_bhalisa(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    umshini_bhalisa(직렬장치 + 0x38) = 0;
    umshini_bhalisa(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
umshini_Amagama 보드파일전송(umshini_Amagama Isenzo) { return (uint32_t)ftp_control((int)Isenzo); }
umshini_Amagama 보드망상태(umshini_Amagama okufakwayo_inani, umshini_Amagama thola_inkomba) { return 망상태읽기(okufakwayo_inani, thola_inkomba); }
umshini_Amagama 보드망설정(umshini_Amagama Isenzo, umshini_Amagama ikheli, umshini_Amagama insitha_inani, umshini_Amagama isango_inani) { return (uint32_t)misa_iNethiwekhi(Isenzo, ikheli, insitha_inani, isango_inani); }
umshini_Amagama 보드응답보내기(umshini_Amagama ikheli, umshini_Amagama ukuhleleka_inani) { return (uint32_t)응답시험시작(ikheli, ukuhleleka_inani); }
umshini_Amagama 보드응답읽기(umshini_Amagama okufakwayo_inani) { return (uint32_t)응답시험읽기(okufakwayo_inani); }
umshini_Amagama 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned thola_inkomba=0; thola_inkomba<32; thola_inkomba++) vala_iNethiwekhi(thola_inkomba);
    for (unsigned thola_inkomba=0; thola_inkomba<4; thola_inkomba++) 보드사용자제어(32+thola_inkomba);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (umshini_bhalisa(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    umshini_bhalisa(0xfe100020ul)=0x5a000000u | (umshini_bhalisa(0xfe100020ul)&~0xfffu) | 0x555;
    umshini_bhalisa(0xfe100024ul)=0x5a000000u | 10;
    umshini_bhalisa(0xfe10001cul)=0x5a000000u | (umshini_bhalisa(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

umshini_Amagama 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 현재 크기를 읽는다. */
    const uint32_t umbuzo_inani[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(umbuzo_inani)/4; 순번++) ibhokisi_leposi_imininingwane[순번] = umbuzo_inani[순번];
    if (ibhokisi_leposi() && ibhokisi_leposi_imininingwane[4] == 0x80000008u &&
        ibhokisi_leposi_imininingwane[5] >= 640 && ibhokisi_leposi_imininingwane[5] <= 1920 &&
        ibhokisi_leposi_imininingwane[6] >= 480 && ibhokisi_leposi_imininingwane[6] <= 1080) {
        요청너비 = ibhokisi_leposi_imininingwane[5]; 요청높이 = ibhokisi_leposi_imininingwane[6];
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
    for (size_t 순번 = 0; 순번 < sizeof(요청)/4; 순번++) ibhokisi_leposi_imininingwane[순번] = 요청[순번];
    // 위 메시지의 ulwazi_ngokwenzekile_imininingwane 길이를 사용: 태그 추가 시 ubude_inani 불일치를 방지한다.
    ibhokisi_leposi_imininingwane[0] = sizeof(요청);
    if (!ibhokisi_leposi()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 응답길이[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (ibhokisi_leposi_imininingwane[응답들[순번]] != (0x80000000u | 응답길이[순번])) return 0;
    uint32_t ngemuva_inani = ibhokisi_leposi_imininingwane[28] & 0x3fffffffu;
    uint32_t Ubungako = ibhokisi_leposi_imininingwane[29];
    uint32_t 받은너비 = ibhokisi_leposi_imininingwane[5], 받은높이 = ibhokisi_leposi_imininingwane[6], 받은줄간격 = ibhokisi_leposi_imininingwane[33];
    if (ibhokisi_leposi_imininingwane[15] != 32 || ibhokisi_leposi_imininingwane[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        ibhokisi_leposi_imininingwane[10] < 받은너비 || ibhokisi_leposi_imininingwane[11] < 받은높이 || ibhokisi_leposi_imininingwane[23] || ibhokisi_leposi_imininingwane[24] ||
        !ngemuva_inani || ngemuva_inani < 0x1000000 || (ngemuva_inani & 3) || 받은줄간격 < 받은너비 * 4 || (받은줄간격 & 3) ||
        (uint64_t)받은줄간격 * 받은높이 > Ubungako || (uint64_t)ngemuva_inani + Ubungako > 0x40000000u)
        return 0;
    보드그림준비((volatile uint32_t *)(uintptr_t)ngemuva_inani, 받은너비, 받은높이, 받은줄간격);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 uhlu_lwemilayezo_inani. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } Umongo;
static Umongo 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int 실행중[3] = {1, 0, 0};
static int 현재작업;
extern void Umongo_guqulela_kokunye(Umongo *, Umongo *);
extern void 자바작업(int32_t);
umshini_Amagama 보드양보(void) {
    network_poll();
    int 이전 = 현재작업, 다음 = (이전 + 1) % 3;
    while (다음 != 이전 && !실행중[다음]) 다음 = (다음 + 1) % 3;
    if (다음 != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (실행중[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        현재작업 = 다음;
        Umongo_guqulela_kokunye(&작업문맥들[이전], &작업문맥들[다음]);
    }
    return 0;
}
static void umsebenzi_ukuvula(void) {
    자바작업(현재작업);
    실행중[현재작업] = 0;
    보드양보();
    커널중단("finished task resumed");
}
umshini_Amagama 보드작업만들기(umshini_Amagama isivezi_inani) {
    if (isivezi_inani < 1 || isivezi_inani > 2 || 실행중[isivezi_inani]) return (uint32_t)-1;
    memset(&작업문맥들[isivezi_inani], 0, sizeof(Umongo));
    *(uint64_t *)쌓임공간들[isivezi_inani - 1] = 0x6b6f726f7373746bull;
    작업문맥들[isivezi_inani].저장값[11] = (uintptr_t)umsebenzi_ukuvula;
    작업문맥들[isivezi_inani].저장값[12] = (uintptr_t)(쌓임공간들[isivezi_inani - 1] + sizeof(쌓임공간들[0]));
    실행중[isivezi_inani] = 1;
    return 0;
}
umshini_Amagama 보드작업상태(umshini_Amagama isivezi_inani) { return isivezi_inani < 3 ? 실행중[isivezi_inani] : (uint32_t)-1; }
extern umshini_Amagama 미리번역기억조회(umshini_Amagama);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
umshini_Amagama 보드체계조회(umshini_Amagama okufakwayo_inani, umshini_Amagama thola_inkomba) {
    if (okufakwayo_inani==0) return 팔기억킬로바이트;
    if (okufakwayo_inani==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (okufakwayo_inani==2 || okufakwayo_inani==3) return 미리번역기억조회(okufakwayo_inani==3);
    if (okufakwayo_inani==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (okufakwayo_inani==5) return 80*1024; /* yenza_umyalo 공간 16 MiB + 네 세션 보관 공간. */
    if (okufakwayo_inani>=20) return 사용자상태읽기(okufakwayo_inani-20, thola_inkomba);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[현재작업]; }
