#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "Mai_anfani_da_kwamfuta.h"
#include "../Hanyar_sadarwa_tara/Hanyar_sadarwa_tara.h"
typedef uintptr_t na_ura_mai_kwakwalwa_Microsoft_Word;
#define 기계저장기(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define akwatinsako_imel 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t 시계세기(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t 진동수;
static volatile uint32_t akwatinsako_Tarin_bayani[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *자료위치, int Lambar_sirrin_harafi, size_t 개수) { unsigned char *다음위치 = 자료위치; while (개수--) *다음위치++ = Lambar_sirrin_harafi; return 자료위치; }
void *memcpy(void *Zangon_ƙarshe_Tarin_bayani, const void *Zare_Tarin_bayani, size_t 개수) { unsigned char *첫째값 = Zangon_ƙarshe_Tarin_bayani; const unsigned char *둘째값 = Zare_Tarin_bayani; while (개수--) *첫째값++ = *둘째값++; return Zangon_ƙarshe_Tarin_bayani; }

static int akwatinsako(void) {
    uint32_t 요청 = (uint32_t)(uintptr_t)akwatinsako_Tarin_bayani | 8;
    uint64_t Tafiyar_da = 시계세기();
    기억장벽();
    while (기계저장기(akwatinsako_imel + 0x38) & 0x80000000u)
        if (시계세기() - Tafiyar_da > 진동수) return 0;
    기계저장기(akwatinsako_imel + 0x20) = 요청;
    for (;;) {
        if (!(기계저장기(akwatinsako_imel + 0x18) & 0x40000000u)) {
            uint32_t mayar_da_martani = 기계저장기(akwatinsako_imel);
            if (mayar_da_martani == 요청) { 기억장벽(); return akwatinsako_Tarin_bayani[1] == 0x80000000u; }
        }
        if (시계세기() - Tafiyar_da > 진동수) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void 터미널바이트(unsigned);
extern int 터미널대기(void);
extern void 터미널가리킴(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../na_nesa_Daraja/na_nesa_Daraja.h"
static int 흐름목록;
static unsigned 직렬이전글자;
na_ura_mai_kwakwalwa_Microsoft_Word 보드흐름설정(na_ura_mai_kwakwalwa_Microsoft_Word 사용여부) { 흐름목록=사용여부!=0; return 0; }
na_ura_mai_kwakwalwa_Microsoft_Word 보드통로(na_ura_mai_kwakwalwa_Microsoft_Word tasha, na_ura_mai_kwakwalwa_Microsoft_Word Lambar_sirrin_harafi) {
    if(흐름목록 && 자바셸출력((int32_t)tasha,(int32_t)(Lambar_sirrin_harafi&255))) return 0;
    터미널바이트(Lambar_sirrin_harafi&255);
    원격출력(Lambar_sirrin_harafi&255);
    if ((Lambar_sirrin_harafi&255)==10 && 직렬이전글자!=13) {
        while (기계저장기(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        기계저장기(직렬장치)=13;
    }
    직렬이전글자=Lambar_sirrin_harafi&255;
    while (기계저장기(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    기계저장기(직렬장치) = (uint32_t)Lambar_sirrin_harafi & 255;
    return 0;
}
na_ura_mai_kwakwalwa_Microsoft_Word 보드글자쓰기(na_ura_mai_kwakwalwa_Microsoft_Word Lambar_sirrin_harafi) { return 보드통로(1,Lambar_sirrin_harafi); }
na_ura_mai_kwakwalwa_Microsoft_Word 보드원시글자읽기(void) {
    int na_nesa_Harafi=원격입력();if(na_nesa_Harafi>=0)return na_nesa_Harafi;
    if (기계저장기(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t Daraja = 기계저장기(직렬장치);
    if (Daraja & 0xf00) { 기계저장기(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return Daraja & 255;
}
na_ura_mai_kwakwalwa_Microsoft_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char makunshi_Tarin_bayani[6];
    if(터미널대기())return (uint32_t)-4096;
    if(흐름목록){int32_t Lambar_sirrin_harafi=자바셸입력();if(Lambar_sirrin_harafi!=-3)return (uint32_t)Lambar_sirrin_harafi;}
    for(;;){
        int Lambar_sirrin_harafi=(int32_t)보드원시글자읽기();if(Lambar_sirrin_harafi<0)return (uint32_t)Lambar_sirrin_harafi;
        if(!꾸러미안쪽){if(Lambar_sirrin_harafi!=30)return Lambar_sirrin_harafi;꾸러미안쪽=1;사용량=0;continue;}
        makunshi_Tarin_bayani[사용량++]=Lambar_sirrin_harafi;if(사용량<6)continue;꾸러미안쪽=0;
        if(makunshi_Tarin_bayani[0]==1)터미널가리킴(makunshi_Tarin_bayani[1],makunshi_Tarin_bayani[2]+makunshi_Tarin_bayani[3]*256,makunshi_Tarin_bayani[4]+makunshi_Tarin_bayani[5]*256);
        if(makunshi_Tarin_bayani[0]==2)터미널바로가기키(makunshi_Tarin_bayani[1]);
        if(makunshi_Tarin_bayani[0]==3)터미널입력방식(makunshi_Tarin_bayani[1]);
        if(터미널대기())return (uint32_t)-4096;
    }
}
na_ura_mai_kwakwalwa_Microsoft_Word 보드밀리초(void) { return (uint32_t)(시계세기() / (진동수 / 1000)); }
na_ura_mai_kwakwalwa_Microsoft_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *Zare_Tarin_bayani) { while (*Zare_Tarin_bayani) 보드글자쓰기((unsigned char)*Zare_Tarin_bayani++); }
static void 직렬열여섯진출력(na_ura_mai_kwakwalwa_Microsoft_Word 개수) { const char *열여섯진숫자 = "0123456789abcdef"; for (int Zare_Tarin_bayani = 60; Zare_Tarin_bayani >= 0; Zare_Tarin_bayani -= 4) 보드글자쓰기(열여섯진숫자[(개수 >> Zare_Tarin_bayani) & 15]); }
na_ura_mai_kwakwalwa_Microsoft_Word 보드멈추기(na_ura_mai_kwakwalwa_Microsoft_Word Matsayi_Daraja) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(Matsayi_Daraja); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); 보드멈추기(1); __builtin_unreachable(); }
void 보드예외(na_ura_mai_kwakwalwa_Microsoft_Word banbanchi_Matsayi, na_ura_mai_kwakwalwa_Microsoft_Word 명령위치, na_ura_mai_kwakwalwa_Microsoft_Word mara_ƙarfi_imel) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(banbanchi_Matsayi);
    직렬글출력(" PC="); 직렬열여섯진출력(명령위치); 직렬글출력(" FAR="); 직렬열여섯진출력(mara_ƙarfi_imel);
    보드멈추기(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    akwatinsako_Tarin_bayani[0]=32;akwatinsako_Tarin_bayani[1]=0;akwatinsako_Tarin_bayani[2]=0x10004;akwatinsako_Tarin_bayani[3]=8;akwatinsako_Tarin_bayani[4]=0;
    akwatinsako_Tarin_bayani[5]=akwatinsako_Tarin_bayani[6]=akwatinsako_Tarin_bayani[7]=0;
    return akwatinsako()&&akwatinsako_Tarin_bayani[4]==0x80000008u&&(akwatinsako_Tarin_bayani[5]||akwatinsako_Tarin_bayani[6]);
}
int 보드기계주소(unsigned char *imel) {
    akwatinsako_Tarin_bayani[0]=32;akwatinsako_Tarin_bayani[1]=0;akwatinsako_Tarin_bayani[2]=0x10003;akwatinsako_Tarin_bayani[3]=8;akwatinsako_Tarin_bayani[4]=0;
    akwatinsako_Tarin_bayani[5]=akwatinsako_Tarin_bayani[6]=akwatinsako_Tarin_bayani[7]=0;
    if(!akwatinsako()||(akwatinsako_Tarin_bayani[4]&0x80000000u)==0||(akwatinsako_Tarin_bayani[4]&0xffff)!=6)return 0;
    const unsigned char *Tarin_bayani=(const unsigned char*)&akwatinsako_Tarin_bayani[5];unsigned 합=0;
    for(unsigned 순번=0;순번<6;순번++){imel[순번]=Tarin_bayani[순번];합|=Tarin_bayani[순번];}return 합&&!(imel[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(진동수));
    기계저장기(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    기계저장기(범용입출력 + 4) = (기계저장기(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    기계저장기(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. Kasa_aiki_Daraja 시 config.txt의 48MHz를 사용한다.
    akwatinsako_Tarin_bayani[0] = 36; akwatinsako_Tarin_bayani[1] = 0; akwatinsako_Tarin_bayani[2] = 0x38002; akwatinsako_Tarin_bayani[3] = 12;
    akwatinsako_Tarin_bayani[4] = 0; akwatinsako_Tarin_bayani[5] = 2; akwatinsako_Tarin_bayani[6] = 48000000; akwatinsako_Tarin_bayani[7] = 0; akwatinsako_Tarin_bayani[8] = 0;
    int 시계정상 = akwatinsako();
    uint32_t 속도 = 시계정상 && akwatinsako_Tarin_bayani[6] >= 1843200 ? akwatinsako_Tarin_bayani[6] : 48000000;
    akwatinsako_Tarin_bayani[0]=32; akwatinsako_Tarin_bayani[1]=0; akwatinsako_Tarin_bayani[2]=0x10005; akwatinsako_Tarin_bayani[3]=8; akwatinsako_Tarin_bayani[4]=0;
    akwatinsako_Tarin_bayani[5]=akwatinsako_Tarin_bayani[6]=akwatinsako_Tarin_bayani[7]=0;
    if (akwatinsako() && akwatinsako_Tarin_bayani[4]==0x80000008u) 팔기억킬로바이트=akwatinsako_Tarin_bayani[6]/1024;
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
na_ura_mai_kwakwalwa_Microsoft_Word 보드파일전송(na_ura_mai_kwakwalwa_Microsoft_Word Aiki) { return (uint32_t)ftp_control((int)Aiki); }
na_ura_mai_kwakwalwa_Microsoft_Word 보드망상태(na_ura_mai_kwakwalwa_Microsoft_Word Mashigar_bayanai_Daraja, na_ura_mai_kwakwalwa_Microsoft_Word Indes) { return 망상태읽기(Mashigar_bayanai_Daraja, Indes); }
na_ura_mai_kwakwalwa_Microsoft_Word 보드망설정(na_ura_mai_kwakwalwa_Microsoft_Word Aiki, na_ura_mai_kwakwalwa_Microsoft_Word imel, na_ura_mai_kwakwalwa_Microsoft_Word Burtu_Daraja, na_ura_mai_kwakwalwa_Microsoft_Word Mashiga_Daraja) { return (uint32_t)hada_kayan_Hanyar_sadarwa(Aiki, imel, Burtu_Daraja, Mashiga_Daraja); }
na_ura_mai_kwakwalwa_Microsoft_Word 보드응답보내기(na_ura_mai_kwakwalwa_Microsoft_Word imel, na_ura_mai_kwakwalwa_Microsoft_Word Hanyar_jejjerawa_Daraja) { return (uint32_t)응답시험시작(imel, Hanyar_jejjerawa_Daraja); }
na_ura_mai_kwakwalwa_Microsoft_Word 보드응답읽기(na_ura_mai_kwakwalwa_Microsoft_Word Mashigar_bayanai_Daraja) { return (uint32_t)응답시험읽기(Mashigar_bayanai_Daraja); }
na_ura_mai_kwakwalwa_Microsoft_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned Indes=0; Indes<32; Indes++) Rufe_Hanyar_sadarwa(Indes);
    for (unsigned Indes=0; Indes<4; Indes++) 보드사용자제어(32+Indes);
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

na_ura_mai_kwakwalwa_Microsoft_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 현재 크기를 읽는다. */
    const uint32_t Matantanci_Daraja[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(Matantanci_Daraja)/4; 순번++) akwatinsako_Tarin_bayani[순번] = Matantanci_Daraja[순번];
    if (akwatinsako() && akwatinsako_Tarin_bayani[4] == 0x80000008u &&
        akwatinsako_Tarin_bayani[5] >= 640 && akwatinsako_Tarin_bayani[5] <= 1920 &&
        akwatinsako_Tarin_bayani[6] >= 480 && akwatinsako_Tarin_bayani[6] <= 1080) {
        요청너비 = akwatinsako_Tarin_bayani[5]; 요청높이 = akwatinsako_Tarin_bayani[6];
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
    for (size_t 순번 = 0; 순번 < sizeof(요청)/4; 순번++) akwatinsako_Tarin_bayani[순번] = 요청[순번];
    // 위 메시지의 Na_hakika_Tarin_bayani 길이를 사용: 태그 추가 시 Tsawo_Daraja 불일치를 방지한다.
    akwatinsako_Tarin_bayani[0] = sizeof(요청);
    if (!akwatinsako()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 응답길이[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (akwatinsako_Tarin_bayani[응답들[순번]] != (0x80000000u | 응답길이[순번])) return 0;
    uint32_t Bi_bango_Daraja = akwatinsako_Tarin_bayani[28] & 0x3fffffffu;
    uint32_t Girma = akwatinsako_Tarin_bayani[29];
    uint32_t 받은너비 = akwatinsako_Tarin_bayani[5], 받은높이 = akwatinsako_Tarin_bayani[6], 받은줄간격 = akwatinsako_Tarin_bayani[33];
    if (akwatinsako_Tarin_bayani[15] != 32 || akwatinsako_Tarin_bayani[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        akwatinsako_Tarin_bayani[10] < 받은너비 || akwatinsako_Tarin_bayani[11] < 받은높이 || akwatinsako_Tarin_bayani[23] || akwatinsako_Tarin_bayani[24] ||
        !Bi_bango_Daraja || Bi_bango_Daraja < 0x1000000 || (Bi_bango_Daraja & 3) || 받은줄간격 < 받은너비 * 4 || (받은줄간격 & 3) ||
        (uint64_t)받은줄간격 * 받은높이 > Girma || (uint64_t)Bi_bango_Daraja + Girma > 0x40000000u)
        return 0;
    보드그림준비((volatile uint32_t *)(uintptr_t)Bi_bango_Daraja, 받은너비, 받은높이, 받은줄간격);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 hira_Daraja. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } Kwaryar_rubutu;
static Kwaryar_rubutu 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int kimiyar_bayanai_Gudu[3] = {1, 0, 0};
static int 현재작업;
extern void Kwaryar_rubutu_Sauya(Kwaryar_rubutu *, Kwaryar_rubutu *);
extern void 자바작업(int32_t);
na_ura_mai_kwakwalwa_Microsoft_Word 보드양보(void) {
    network_poll();
    int 이전 = 현재작업, 다음 = (이전 + 1) % 3;
    while (다음 != 이전 && !kimiyar_bayanai_Gudu[다음]) 다음 = (다음 + 1) % 3;
    if (다음 != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (kimiyar_bayanai_Gudu[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        현재작업 = 다음;
        Kwaryar_rubutu_Sauya(&작업문맥들[이전], &작업문맥들[다음]);
    }
    return 0;
}
static void aiki_Matakan_kunna_kwamfuta(void) {
    자바작업(현재작업);
    kimiyar_bayanai_Gudu[현재작업] = 0;
    보드양보();
    커널중단("finished task resumed");
}
na_ura_mai_kwakwalwa_Microsoft_Word 보드작업만들기(na_ura_mai_kwakwalwa_Microsoft_Word mai_ganewa_Daraja) {
    if (mai_ganewa_Daraja < 1 || mai_ganewa_Daraja > 2 || kimiyar_bayanai_Gudu[mai_ganewa_Daraja]) return (uint32_t)-1;
    memset(&작업문맥들[mai_ganewa_Daraja], 0, sizeof(Kwaryar_rubutu));
    *(uint64_t *)쌓임공간들[mai_ganewa_Daraja - 1] = 0x6b6f726f7373746bull;
    작업문맥들[mai_ganewa_Daraja].저장값[11] = (uintptr_t)aiki_Matakan_kunna_kwamfuta;
    작업문맥들[mai_ganewa_Daraja].저장값[12] = (uintptr_t)(쌓임공간들[mai_ganewa_Daraja - 1] + sizeof(쌓임공간들[0]));
    kimiyar_bayanai_Gudu[mai_ganewa_Daraja] = 1;
    return 0;
}
na_ura_mai_kwakwalwa_Microsoft_Word 보드작업상태(na_ura_mai_kwakwalwa_Microsoft_Word mai_ganewa_Daraja) { return mai_ganewa_Daraja < 3 ? kimiyar_bayanai_Gudu[mai_ganewa_Daraja] : (uint32_t)-1; }
extern na_ura_mai_kwakwalwa_Microsoft_Word 미리번역기억조회(na_ura_mai_kwakwalwa_Microsoft_Word);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
na_ura_mai_kwakwalwa_Microsoft_Word 보드체계조회(na_ura_mai_kwakwalwa_Microsoft_Word Mashigar_bayanai_Daraja, na_ura_mai_kwakwalwa_Microsoft_Word Indes) {
    if (Mashigar_bayanai_Daraja==0) return 팔기억킬로바이트;
    if (Mashigar_bayanai_Daraja==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (Mashigar_bayanai_Daraja==2 || Mashigar_bayanai_Daraja==3) return 미리번역기억조회(Mashigar_bayanai_Daraja==3);
    if (Mashigar_bayanai_Daraja==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (Mashigar_bayanai_Daraja==5) return 80*1024; /* gudanar_Umarni 공간 16 MiB + 네 세션 보관 공간. */
    if (Mashigar_bayanai_Daraja>=20) return 사용자상태읽기(Mashigar_bayanai_Daraja-20, Indes);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[현재작업]; }
