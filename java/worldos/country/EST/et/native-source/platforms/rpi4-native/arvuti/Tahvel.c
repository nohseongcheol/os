#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "kasutaja.h"
#include "../võrk_Virn/võrk_Virn.h"
typedef uintptr_t arvuti_Word;
#define arvuti_register(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define postkast_ADDRESS 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Kell_COUNT(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t sagedus;
static volatile uint32_t postkast_andmed[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *andmed_ametikoht, int koodipunkt, size_t kaup_COUNT) { unsigned char *Edasi_nihe = andmed_ametikoht; while (kaup_COUNT--) *Edasi_nihe++ = koodipunkt; return andmed_ametikoht; }
void *memcpy(void *sihtkoht_andmed, const void *string_andmed, size_t kaup_COUNT) { unsigned char *첫째값 = sihtkoht_andmed; const unsigned char *SECOND_VALUE = string_andmed; while (kaup_COUNT--) *첫째값++ = *SECOND_VALUE++; return sihtkoht_andmed; }

static int postkast(void) {
    uint32_t päring = (uint32_t)(uintptr_t)postkast_andmed | 8;
    uint64_t Käivita_2 = Kell_COUNT();
    기억장벽();
    while (arvuti_register(postkast_ADDRESS + 0x38) & 0x80000000u)
        if (Kell_COUNT() - Käivita_2 > sagedus) return 0;
    arvuti_register(postkast_ADDRESS + 0x20) = päring;
    for (;;) {
        if (!(arvuti_register(postkast_ADDRESS + 0x18) & 0x40000000u)) {
            uint32_t vastus = arvuti_register(postkast_ADDRESS);
            if (vastus == päring) { 기억장벽(); return postkast_andmed[1] == 0x80000000u; }
        }
        if (Kell_COUNT() - Käivita_2 > sagedus) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void terminal_bait(unsigned);
extern int terminal_ootel(void);
extern void terminal_kursor(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../kauge_VALUE/kauge_VALUE.h"
static int Vood;
static unsigned 직렬이전글자;
arvuti_Word Tahvel_Vood(arvuti_Word 사용여부) { Vood=사용여부!=0; return 0; }
arvuti_Word Tahvel_Kanal(arvuti_Word Kanal, arvuti_Word koodipunkt) {
    if(Vood && 자바셸출력((int32_t)Kanal,(int32_t)(koodipunkt&255))) return 0;
    terminal_bait(koodipunkt&255);
    kauge_toodang(koodipunkt&255);
    if ((koodipunkt&255)==10 && 직렬이전글자!=13) {
        while (arvuti_register(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        arvuti_register(직렬장치)=13;
    }
    직렬이전글자=koodipunkt&255;
    while (arvuti_register(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    arvuti_register(직렬장치) = (uint32_t)koodipunkt & 255;
    return 0;
}
arvuti_Word 보드글자쓰기(arvuti_Word koodipunkt) { return Tahvel_Kanal(1,koodipunkt); }
arvuti_Word 보드원시글자읽기(void) {
    int kauge_märk=원격입력();if(kauge_märk>=0)return kauge_märk;
    if (arvuti_register(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t VALUE = arvuti_register(직렬장치);
    if (VALUE & 0xf00) { arvuti_register(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return VALUE & 255;
}
arvuti_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char pakett_andmed[6];
    if(terminal_ootel())return (uint32_t)-4096;
    if(Vood){int32_t koodipunkt=자바셸입력();if(koodipunkt!=-3)return (uint32_t)koodipunkt;}
    for(;;){
        int koodipunkt=(int32_t)보드원시글자읽기();if(koodipunkt<0)return (uint32_t)koodipunkt;
        if(!꾸러미안쪽){if(koodipunkt!=30)return koodipunkt;꾸러미안쪽=1;사용량=0;continue;}
        pakett_andmed[사용량++]=koodipunkt;if(사용량<6)continue;꾸러미안쪽=0;
        if(pakett_andmed[0]==1)terminal_kursor(pakett_andmed[1],pakett_andmed[2]+pakett_andmed[3]*256,pakett_andmed[4]+pakett_andmed[5]*256);
        if(pakett_andmed[0]==2)터미널바로가기키(pakett_andmed[1]);
        if(pakett_andmed[0]==3)터미널입력방식(pakett_andmed[1]);
        if(terminal_ootel())return (uint32_t)-4096;
    }
}
arvuti_Word 보드밀리초(void) { return (uint32_t)(Kell_COUNT() / (sagedus / 1000)); }
arvuti_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *string_andmed) { while (*string_andmed) 보드글자쓰기((unsigned char)*string_andmed++); }
static void 직렬열여섯진출력(arvuti_Word kaup_COUNT) { const char *열여섯진숫자 = "0123456789abcdef"; for (int string_andmed = 60; string_andmed >= 0; string_andmed -= 4) 보드글자쓰기(열여섯진숫자[(kaup_COUNT >> string_andmed) & 15]); }
arvuti_Word Tahvel_Peata(arvuti_Word Olek_VALUE) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(Olek_VALUE); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); Tahvel_Peata(1); __builtin_unreachable(); }
void Tahvel_erand(arvuti_Word erand_Olek, arvuti_Word käsk_ametikoht, arvuti_Word kehtetu_ADDRESS) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(erand_Olek);
    직렬글출력(" PC="); 직렬열여섯진출력(käsk_ametikoht); 직렬글출력(" FAR="); 직렬열여섯진출력(kehtetu_ADDRESS);
    Tahvel_Peata(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    postkast_andmed[0]=32;postkast_andmed[1]=0;postkast_andmed[2]=0x10004;postkast_andmed[3]=8;postkast_andmed[4]=0;
    postkast_andmed[5]=postkast_andmed[6]=postkast_andmed[7]=0;
    return postkast()&&postkast_andmed[4]==0x80000008u&&(postkast_andmed[5]||postkast_andmed[6]);
}
int Tahvel_absoluutaadress(unsigned char *ADDRESS) {
    postkast_andmed[0]=32;postkast_andmed[1]=0;postkast_andmed[2]=0x10003;postkast_andmed[3]=8;postkast_andmed[4]=0;
    postkast_andmed[5]=postkast_andmed[6]=postkast_andmed[7]=0;
    if(!postkast()||(postkast_andmed[4]&0x80000000u)==0||(postkast_andmed[4]&0xffff)!=6)return 0;
    const unsigned char *andmed=(const unsigned char*)&postkast_andmed[5];unsigned SUM_VALUE=0;
    for(unsigned 순번=0;순번<6;순번++){ADDRESS[순번]=andmed[순번];SUM_VALUE|=andmed[순번];}return SUM_VALUE&&!(ADDRESS[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(sagedus));
    arvuti_register(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    arvuti_register(범용입출력 + 4) = (arvuti_register(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    arvuti_register(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. tõrge_VALUE 시 config.txt의 48MHz를 사용한다.
    postkast_andmed[0] = 36; postkast_andmed[1] = 0; postkast_andmed[2] = 0x38002; postkast_andmed[3] = 12;
    postkast_andmed[4] = 0; postkast_andmed[5] = 2; postkast_andmed[6] = 48000000; postkast_andmed[7] = 0; postkast_andmed[8] = 0;
    int 시계정상 = postkast();
    uint32_t 속도 = 시계정상 && postkast_andmed[6] >= 1843200 ? postkast_andmed[6] : 48000000;
    postkast_andmed[0]=32; postkast_andmed[1]=0; postkast_andmed[2]=0x10005; postkast_andmed[3]=8; postkast_andmed[4]=0;
    postkast_andmed[5]=postkast_andmed[6]=postkast_andmed[7]=0;
    if (postkast() && postkast_andmed[4]==0x80000008u) 팔기억킬로바이트=postkast_andmed[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    arvuti_register(직렬장치 + 0x44) = 0x7ff;
    arvuti_register(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    arvuti_register(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    arvuti_register(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    arvuti_register(직렬장치 + 0x38) = 0;
    arvuti_register(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
arvuti_Word Tahvel_FTP(arvuti_Word Nimi) { return (uint32_t)ftp_control((int)Nimi); }
arvuti_Word Tahvel_võrk_olek(arvuti_Word kirje_VALUE, arvuti_Word INDEX) { return 망상태읽기(kirje_VALUE, INDEX); }
arvuti_Word Tahvel_võrk_Sätted(arvuti_Word Nimi, arvuti_Word ADDRESS, arvuti_Word mask_VALUE, arvuti_Word lüüs_VALUE) { return (uint32_t)konfigureerima_võrk(Nimi, ADDRESS, mask_VALUE, lüüs_VALUE); }
arvuti_Word Tahvel_saatma_vastus(arvuti_Word ADDRESS, arvuti_Word tellimus_VALUE) { return (uint32_t)응답시험시작(ADDRESS, tellimus_VALUE); }
arvuti_Word 보드응답읽기(arvuti_Word kirje_VALUE) { return (uint32_t)응답시험읽기(kirje_VALUE); }
arvuti_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEX=0; INDEX<32; INDEX++) Sule_võrk(INDEX);
    for (unsigned INDEX=0; INDEX<4; INDEX++) Tahvel_kasutusjuhtelement(32+INDEX);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (arvuti_register(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    arvuti_register(0xfe100020ul)=0x5a000000u | (arvuti_register(0xfe100020ul)&~0xfffu) | 0x555;
    arvuti_register(0xfe100024ul)=0x5a000000u | 10;
    arvuti_register(0xfe10001cul)=0x5a000000u | (arvuti_register(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

arvuti_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 tähtaja_piires_kaup 크기를 읽는다. */
    const uint32_t päring_VALUE[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(päring_VALUE)/4; 순번++) postkast_andmed[순번] = päring_VALUE[순번];
    if (postkast() && postkast_andmed[4] == 0x80000008u &&
        postkast_andmed[5] >= 640 && postkast_andmed[5] <= 1920 &&
        postkast_andmed[6] >= 480 && postkast_andmed[6] <= 1080) {
        요청너비 = postkast_andmed[5]; 요청높이 = postkast_andmed[6];
    }
    const uint32_t päring[] = {
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
    for (size_t 순번 = 0; 순번 < sizeof(päring)/4; 순번++) postkast_andmed[순번] = päring[순번];
    // 위 메시지의 tegelik_andmed 길이를 kasutus_VALUE: 태그 Lisa_kirje 시 길이 불일치를 방지한다.
    postkast_andmed[0] = sizeof(päring);
    if (!postkast()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 응답길이[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (postkast_andmed[응답들[순번]] != (0x80000000u | 응답길이[순번])) return 0;
    uint32_t taust_VALUE = postkast_andmed[28] & 0x3fffffffu;
    uint32_t Suurus = postkast_andmed[29];
    uint32_t 받은너비 = postkast_andmed[5], 받은높이 = postkast_andmed[6], RECEIVED_reasamm = postkast_andmed[33];
    if (postkast_andmed[15] != 32 || postkast_andmed[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        postkast_andmed[10] < 받은너비 || postkast_andmed[11] < 받은높이 || postkast_andmed[23] || postkast_andmed[24] ||
        !taust_VALUE || taust_VALUE < 0x1000000 || (taust_VALUE & 3) || RECEIVED_reasamm < 받은너비 * 4 || (RECEIVED_reasamm & 3) ||
        (uint64_t)RECEIVED_reasamm * 받은높이 > Suurus || (uint64_t)taust_VALUE + Suurus > 0x40000000u)
        return 0;
    Tahvel_Ettevalmistamine_joonis((volatile uint32_t *)(uintptr_t)taust_VALUE, 받은너비, 받은높이, RECEIVED_reasamm);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 lõim_VALUE. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } kontekst;
static kontekst 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int infotehnoloogia_Jooksmine[3] = {1, 0, 0};
static int tähtaja_piires_tööüksus;
extern void kontekstilüliti(kontekst *, kontekst *);
extern void 자바작업(int32_t);
arvuti_Word Tahvel_YIELD(void) {
    network_poll();
    int 이전 = tähtaja_piires_tööüksus, Edasi_kaup = (이전 + 1) % 3;
    while (Edasi_kaup != 이전 && !infotehnoloogia_Jooksmine[Edasi_kaup]) Edasi_kaup = (Edasi_kaup + 1) % 3;
    if (Edasi_kaup != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (infotehnoloogia_Jooksmine[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        tähtaja_piires_tööüksus = Edasi_kaup;
        kontekstilüliti(&작업문맥들[이전], &작업문맥들[Edasi_kaup]);
    }
    return 0;
}
static void tööüksus_käivitus(void) {
    자바작업(tähtaja_piires_tööüksus);
    infotehnoloogia_Jooksmine[tähtaja_piires_tööüksus] = 0;
    Tahvel_YIELD();
    커널중단("finished task resumed");
}
arvuti_Word Tahvel_tööüksus_avama(arvuti_Word identifikaator_VALUE) {
    if (identifikaator_VALUE < 1 || identifikaator_VALUE > 2 || infotehnoloogia_Jooksmine[identifikaator_VALUE]) return (uint32_t)-1;
    memset(&작업문맥들[identifikaator_VALUE], 0, sizeof(kontekst));
    *(uint64_t *)쌓임공간들[identifikaator_VALUE - 1] = 0x6b6f726f7373746bull;
    작업문맥들[identifikaator_VALUE].저장값[11] = (uintptr_t)tööüksus_käivitus;
    작업문맥들[identifikaator_VALUE].저장값[12] = (uintptr_t)(쌓임공간들[identifikaator_VALUE - 1] + sizeof(쌓임공간들[0]));
    infotehnoloogia_Jooksmine[identifikaator_VALUE] = 1;
    return 0;
}
arvuti_Word Tahvel_tööüksus_Olek(arvuti_Word identifikaator_VALUE) { return identifikaator_VALUE < 3 ? infotehnoloogia_Jooksmine[identifikaator_VALUE] : (uint32_t)-1; }
extern arvuti_Word AOT_Mälu_LOOKUP(arvuti_Word);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
arvuti_Word Tahvel_päring_süsteem(arvuti_Word kirje_VALUE, arvuti_Word INDEX) {
    if (kirje_VALUE==0) return 팔기억킬로바이트;
    if (kirje_VALUE==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (kirje_VALUE==2 || kirje_VALUE==3) return AOT_Mälu_LOOKUP(kirje_VALUE==3);
    if (kirje_VALUE==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (kirje_VALUE==5) return 80*1024; /* Täida_käsk ADDRESS_regioon 16 MiB + 네 세션 보관 ADDRESS_regioon. */
    if (kirje_VALUE>=20) return 사용자상태읽기(kirje_VALUE-20, INDEX);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[tähtaja_piires_tööüksus]; }
