#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "umsebenzisi.h"
#include "../Inethiwekhi_fumba/Inethiwekhi_fumba.h"
typedef uintptr_t umatshini_Igama;
#define umatshini_bhalisa(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define ibhokisi_yeposi_idilesi 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t 시계세기(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t 진동수;
static volatile uint32_t ibhokisi_yeposi_iingcombolo[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *자료위치, int ikhowudi_yekharakhtha, size_t 개수) { unsigned char *다음위치 = 자료위치; while (개수--) *다음위치++ = ikhowudi_yekharakhtha; return 자료위치; }
void *memcpy(void *indawo_ekuyiwa_kuyo_iingcombolo, const void *uluhlu_lweekharektha_iingcombolo, size_t 개수) { unsigned char *첫째값 = indawo_ekuyiwa_kuyo_iingcombolo; const unsigned char *둘째값 = uluhlu_lweekharektha_iingcombolo; while (개수--) *첫째값++ = *둘째값++; return indawo_ekuyiwa_kuyo_iingcombolo; }

static int ibhokisi_yeposi(void) {
    uint32_t 요청 = (uint32_t)(uintptr_t)ibhokisi_yeposi_iingcombolo | 8;
    uint64_t Phumeza = 시계세기();
    기억장벽();
    while (umatshini_bhalisa(ibhokisi_yeposi_idilesi + 0x38) & 0x80000000u)
        if (시계세기() - Phumeza > 진동수) return 0;
    umatshini_bhalisa(ibhokisi_yeposi_idilesi + 0x20) = 요청;
    for (;;) {
        if (!(umatshini_bhalisa(ibhokisi_yeposi_idilesi + 0x18) & 0x40000000u)) {
            uint32_t phendula = umatshini_bhalisa(ibhokisi_yeposi_idilesi);
            if (phendula == 요청) { 기억장벽(); return ibhokisi_yeposi_iingcombolo[1] == 0x80000000u; }
        }
        if (시계세기() - Phumeza > 진동수) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void 터미널바이트(unsigned);
extern int 터미널대기(void);
extern void 터미널가리킴(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../kude_ixabiso/kude_ixabiso.h"
static int 흐름목록;
static unsigned 직렬이전글자;
umatshini_Igama 보드흐름설정(umatshini_Igama 사용여부) { 흐름목록=사용여부!=0; return 0; }
umatshini_Igama 보드통로(umatshini_Igama ijelo, umatshini_Igama ikhowudi_yekharakhtha) {
    if(흐름목록 && 자바셸출력((int32_t)ijelo,(int32_t)(ikhowudi_yekharakhtha&255))) return 0;
    터미널바이트(ikhowudi_yekharakhtha&255);
    원격출력(ikhowudi_yekharakhtha&255);
    if ((ikhowudi_yekharakhtha&255)==10 && 직렬이전글자!=13) {
        while (umatshini_bhalisa(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        umatshini_bhalisa(직렬장치)=13;
    }
    직렬이전글자=ikhowudi_yekharakhtha&255;
    while (umatshini_bhalisa(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    umatshini_bhalisa(직렬장치) = (uint32_t)ikhowudi_yekharakhtha & 255;
    return 0;
}
umatshini_Igama 보드글자쓰기(umatshini_Igama ikhowudi_yekharakhtha) { return 보드통로(1,ikhowudi_yekharakhtha); }
umatshini_Igama 보드원시글자읽기(void) {
    int kude_ikharakhtha=원격입력();if(kude_ikharakhtha>=0)return kude_ikharakhtha;
    if (umatshini_bhalisa(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t ixabiso = umatshini_bhalisa(직렬장치);
    if (ixabiso & 0xf00) { umatshini_bhalisa(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return ixabiso & 255;
}
umatshini_Igama 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char ipakethe_iingcombolo[6];
    if(터미널대기())return (uint32_t)-4096;
    if(흐름목록){int32_t ikhowudi_yekharakhtha=자바셸입력();if(ikhowudi_yekharakhtha!=-3)return (uint32_t)ikhowudi_yekharakhtha;}
    for(;;){
        int ikhowudi_yekharakhtha=(int32_t)보드원시글자읽기();if(ikhowudi_yekharakhtha<0)return (uint32_t)ikhowudi_yekharakhtha;
        if(!꾸러미안쪽){if(ikhowudi_yekharakhtha!=30)return ikhowudi_yekharakhtha;꾸러미안쪽=1;사용량=0;continue;}
        ipakethe_iingcombolo[사용량++]=ikhowudi_yekharakhtha;if(사용량<6)continue;꾸러미안쪽=0;
        if(ipakethe_iingcombolo[0]==1)터미널가리킴(ipakethe_iingcombolo[1],ipakethe_iingcombolo[2]+ipakethe_iingcombolo[3]*256,ipakethe_iingcombolo[4]+ipakethe_iingcombolo[5]*256);
        if(ipakethe_iingcombolo[0]==2)터미널바로가기키(ipakethe_iingcombolo[1]);
        if(ipakethe_iingcombolo[0]==3)터미널입력방식(ipakethe_iingcombolo[1]);
        if(터미널대기())return (uint32_t)-4096;
    }
}
umatshini_Igama 보드밀리초(void) { return (uint32_t)(시계세기() / (진동수 / 1000)); }
umatshini_Igama 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *uluhlu_lweekharektha_iingcombolo) { while (*uluhlu_lweekharektha_iingcombolo) 보드글자쓰기((unsigned char)*uluhlu_lweekharektha_iingcombolo++); }
static void 직렬열여섯진출력(umatshini_Igama 개수) { const char *열여섯진숫자 = "0123456789abcdef"; for (int uluhlu_lweekharektha_iingcombolo = 60; uluhlu_lweekharektha_iingcombolo >= 0; uluhlu_lweekharektha_iingcombolo -= 4) 보드글자쓰기(열여섯진숫자[(개수 >> uluhlu_lweekharektha_iingcombolo) & 15]); }
umatshini_Igama 보드멈추기(umatshini_Igama imo_ixabiso) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(imo_ixabiso); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); 보드멈추기(1); __builtin_unreachable(); }
void 보드예외(umatshini_Igama 예외상태, umatshini_Igama 명령위치, umatshini_Igama ayisebenzi_idilesi) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(예외상태);
    직렬글출력(" PC="); 직렬열여섯진출력(명령위치); 직렬글출력(" FAR="); 직렬열여섯진출력(ayisebenzi_idilesi);
    보드멈추기(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    ibhokisi_yeposi_iingcombolo[0]=32;ibhokisi_yeposi_iingcombolo[1]=0;ibhokisi_yeposi_iingcombolo[2]=0x10004;ibhokisi_yeposi_iingcombolo[3]=8;ibhokisi_yeposi_iingcombolo[4]=0;
    ibhokisi_yeposi_iingcombolo[5]=ibhokisi_yeposi_iingcombolo[6]=ibhokisi_yeposi_iingcombolo[7]=0;
    return ibhokisi_yeposi()&&ibhokisi_yeposi_iingcombolo[4]==0x80000008u&&(ibhokisi_yeposi_iingcombolo[5]||ibhokisi_yeposi_iingcombolo[6]);
}
int 보드기계주소(unsigned char *idilesi) {
    ibhokisi_yeposi_iingcombolo[0]=32;ibhokisi_yeposi_iingcombolo[1]=0;ibhokisi_yeposi_iingcombolo[2]=0x10003;ibhokisi_yeposi_iingcombolo[3]=8;ibhokisi_yeposi_iingcombolo[4]=0;
    ibhokisi_yeposi_iingcombolo[5]=ibhokisi_yeposi_iingcombolo[6]=ibhokisi_yeposi_iingcombolo[7]=0;
    if(!ibhokisi_yeposi()||(ibhokisi_yeposi_iingcombolo[4]&0x80000000u)==0||(ibhokisi_yeposi_iingcombolo[4]&0xffff)!=6)return 0;
    const unsigned char *iingcombolo=(const unsigned char*)&ibhokisi_yeposi_iingcombolo[5];unsigned 합=0;
    for(unsigned 순번=0;순번<6;순번++){idilesi[순번]=iingcombolo[순번];합|=iingcombolo[순번];}return 합&&!(idilesi[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(진동수));
    umatshini_bhalisa(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    umatshini_bhalisa(범용입출력 + 4) = (umatshini_bhalisa(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    umatshini_bhalisa(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. ukungaphumeleli_ixabiso 시 config.txt의 48MHz를 사용한다.
    ibhokisi_yeposi_iingcombolo[0] = 36; ibhokisi_yeposi_iingcombolo[1] = 0; ibhokisi_yeposi_iingcombolo[2] = 0x38002; ibhokisi_yeposi_iingcombolo[3] = 12;
    ibhokisi_yeposi_iingcombolo[4] = 0; ibhokisi_yeposi_iingcombolo[5] = 2; ibhokisi_yeposi_iingcombolo[6] = 48000000; ibhokisi_yeposi_iingcombolo[7] = 0; ibhokisi_yeposi_iingcombolo[8] = 0;
    int 시계정상 = ibhokisi_yeposi();
    uint32_t 속도 = 시계정상 && ibhokisi_yeposi_iingcombolo[6] >= 1843200 ? ibhokisi_yeposi_iingcombolo[6] : 48000000;
    ibhokisi_yeposi_iingcombolo[0]=32; ibhokisi_yeposi_iingcombolo[1]=0; ibhokisi_yeposi_iingcombolo[2]=0x10005; ibhokisi_yeposi_iingcombolo[3]=8; ibhokisi_yeposi_iingcombolo[4]=0;
    ibhokisi_yeposi_iingcombolo[5]=ibhokisi_yeposi_iingcombolo[6]=ibhokisi_yeposi_iingcombolo[7]=0;
    if (ibhokisi_yeposi() && ibhokisi_yeposi_iingcombolo[4]==0x80000008u) 팔기억킬로바이트=ibhokisi_yeposi_iingcombolo[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    umatshini_bhalisa(직렬장치 + 0x44) = 0x7ff;
    umatshini_bhalisa(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    umatshini_bhalisa(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    umatshini_bhalisa(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    umatshini_bhalisa(직렬장치 + 0x38) = 0;
    umatshini_bhalisa(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
umatshini_Igama 보드파일전송(umatshini_Igama Intshukumo) { return (uint32_t)ftp_control((int)Intshukumo); }
umatshini_Igama 보드망상태(umatshini_Igama ufako_nkcukacha_ixabiso, umatshini_Igama indeksa) { return 망상태읽기(ufako_nkcukacha_ixabiso, indeksa); }
umatshini_Igama 보드망설정(umatshini_Igama Intshukumo, umatshini_Igama idilesi, umatshini_Igama imaskhi_ixabiso, umatshini_Igama isango_lekhompyutha_ixabiso) { return (uint32_t)lungiselela_Inethiwekhi(Intshukumo, idilesi, imaskhi_ixabiso, isango_lekhompyutha_ixabiso); }
umatshini_Igama 보드응답보내기(umatshini_Igama idilesi, umatshini_Igama ulandelelwano_ixabiso) { return (uint32_t)응답시험시작(idilesi, ulandelelwano_ixabiso); }
umatshini_Igama 보드응답읽기(umatshini_Igama ufako_nkcukacha_ixabiso) { return (uint32_t)응답시험읽기(ufako_nkcukacha_ixabiso); }
umatshini_Igama 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned indeksa=0; indeksa<32; indeksa++) vala_Inethiwekhi(indeksa);
    for (unsigned indeksa=0; indeksa<4; indeksa++) 보드사용자제어(32+indeksa);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (umatshini_bhalisa(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    umatshini_bhalisa(0xfe100020ul)=0x5a000000u | (umatshini_bhalisa(0xfe100020ul)&~0xfffu) | 0x555;
    umatshini_bhalisa(0xfe100024ul)=0x5a000000u | 10;
    umatshini_bhalisa(0xfe10001cul)=0x5a000000u | (umatshini_bhalisa(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

umatshini_Igama 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 현재 크기를 읽는다. */
    const uint32_t umbuzo_ixabiso[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(umbuzo_ixabiso)/4; 순번++) ibhokisi_yeposi_iingcombolo[순번] = umbuzo_ixabiso[순번];
    if (ibhokisi_yeposi() && ibhokisi_yeposi_iingcombolo[4] == 0x80000008u &&
        ibhokisi_yeposi_iingcombolo[5] >= 640 && ibhokisi_yeposi_iingcombolo[5] <= 1920 &&
        ibhokisi_yeposi_iingcombolo[6] >= 480 && ibhokisi_yeposi_iingcombolo[6] <= 1080) {
        요청너비 = ibhokisi_yeposi_iingcombolo[5]; 요청높이 = ibhokisi_yeposi_iingcombolo[6];
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
    for (size_t 순번 = 0; 순번 < sizeof(요청)/4; 순번++) ibhokisi_yeposi_iingcombolo[순번] = 요청[순번];
    // 위 메시지의 eyona_yenzekileyo_iingcombolo 길이를 사용: 태그 추가 시 ubude_ixabiso 불일치를 방지한다.
    ibhokisi_yeposi_iingcombolo[0] = sizeof(요청);
    if (!ibhokisi_yeposi()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 응답길이[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (ibhokisi_yeposi_iingcombolo[응답들[순번]] != (0x80000000u | 응답길이[순번])) return 0;
    uint32_t Ngasemva_ixabiso = ibhokisi_yeposi_iingcombolo[28] & 0x3fffffffu;
    uint32_t Ubukhulu = ibhokisi_yeposi_iingcombolo[29];
    uint32_t 받은너비 = ibhokisi_yeposi_iingcombolo[5], 받은높이 = ibhokisi_yeposi_iingcombolo[6], 받은줄간격 = ibhokisi_yeposi_iingcombolo[33];
    if (ibhokisi_yeposi_iingcombolo[15] != 32 || ibhokisi_yeposi_iingcombolo[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        ibhokisi_yeposi_iingcombolo[10] < 받은너비 || ibhokisi_yeposi_iingcombolo[11] < 받은높이 || ibhokisi_yeposi_iingcombolo[23] || ibhokisi_yeposi_iingcombolo[24] ||
        !Ngasemva_ixabiso || Ngasemva_ixabiso < 0x1000000 || (Ngasemva_ixabiso & 3) || 받은줄간격 < 받은너비 * 4 || (받은줄간격 & 3) ||
        (uint64_t)받은줄간격 * 받은높이 > Ubukhulu || (uint64_t)Ngasemva_ixabiso + Ubukhulu > 0x40000000u)
        return 0;
    보드그림준비((volatile uint32_t *)(uintptr_t)Ngasemva_ixabiso, 받은너비, 받은높이, 받은줄간격);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 ithredi_ixabiso. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } umxholo;
static umxholo 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int 실행중[3] = {1, 0, 0};
static int 현재작업;
extern void umxholo_tshintshela(umxholo *, umxholo *);
extern void 자바작업(int32_t);
umatshini_Igama 보드양보(void) {
    network_poll();
    int 이전 = 현재작업, 다음 = (이전 + 1) % 3;
    while (다음 != 이전 && !실행중[다음]) 다음 = (다음 + 1) % 3;
    if (다음 != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (실행중[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        현재작업 = 다음;
        umxholo_tshintshela(&작업문맥들[이전], &작업문맥들[다음]);
    }
    return 0;
}
static void umsebenzi_ukuvula(void) {
    자바작업(현재작업);
    실행중[현재작업] = 0;
    보드양보();
    커널중단("finished task resumed");
}
umatshini_Igama 보드작업만들기(umatshini_Igama isalathisi_ixabiso) {
    if (isalathisi_ixabiso < 1 || isalathisi_ixabiso > 2 || 실행중[isalathisi_ixabiso]) return (uint32_t)-1;
    memset(&작업문맥들[isalathisi_ixabiso], 0, sizeof(umxholo));
    *(uint64_t *)쌓임공간들[isalathisi_ixabiso - 1] = 0x6b6f726f7373746bull;
    작업문맥들[isalathisi_ixabiso].저장값[11] = (uintptr_t)umsebenzi_ukuvula;
    작업문맥들[isalathisi_ixabiso].저장값[12] = (uintptr_t)(쌓임공간들[isalathisi_ixabiso - 1] + sizeof(쌓임공간들[0]));
    실행중[isalathisi_ixabiso] = 1;
    return 0;
}
umatshini_Igama 보드작업상태(umatshini_Igama isalathisi_ixabiso) { return isalathisi_ixabiso < 3 ? 실행중[isalathisi_ixabiso] : (uint32_t)-1; }
extern umatshini_Igama 미리번역기억조회(umatshini_Igama);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
umatshini_Igama 보드체계조회(umatshini_Igama ufako_nkcukacha_ixabiso, umatshini_Igama indeksa) {
    if (ufako_nkcukacha_ixabiso==0) return 팔기억킬로바이트;
    if (ufako_nkcukacha_ixabiso==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (ufako_nkcukacha_ixabiso==2 || ufako_nkcukacha_ixabiso==3) return 미리번역기억조회(ufako_nkcukacha_ixabiso==3);
    if (ufako_nkcukacha_ixabiso==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (ufako_nkcukacha_ixabiso==5) return 80*1024; /* ukwenza_umyalelo 공간 16 MiB + 네 세션 보관 공간. */
    if (ufako_nkcukacha_ixabiso>=20) return 사용자상태읽기(ufako_nkcukacha_ixabiso-20, indeksa);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[현재작업]; }
