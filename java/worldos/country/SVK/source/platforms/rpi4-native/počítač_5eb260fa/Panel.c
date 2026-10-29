#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "používateľ.h"
#include "../sieť_Vrstvy/sieť_Vrstvy.h"
typedef uintptr_t počítač_Word;
#define počítač_register(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define poštová_schránka_adresa 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Hodiny_COUNT(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t FREQUENCY;
static volatile uint32_t poštová_schránka_údaje[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *údaje_pozícia, int bod_kódu, size_t položka_COUNT) { unsigned char *Ďalej_Posun = údaje_pozícia; while (položka_COUNT--) *Ďalej_Posun++ = bod_kódu; return údaje_pozícia; }
void *memcpy(void *cieľ_údaje, const void *reťazec_údaje, size_t položka_COUNT) { unsigned char *첫째값 = cieľ_údaje; const unsigned char *SECOND_VALUE = reťazec_údaje; while (položka_COUNT--) *첫째값++ = *SECOND_VALUE++; return cieľ_údaje; }

static int poštová_schránka(void) {
    uint32_t požiadavka = (uint32_t)(uintptr_t)poštová_schránka_údaje | 8;
    uint64_t Spustiť_2 = Hodiny_COUNT();
    기억장벽();
    while (počítač_register(poštová_schránka_adresa + 0x38) & 0x80000000u)
        if (Hodiny_COUNT() - Spustiť_2 > FREQUENCY) return 0;
    počítač_register(poštová_schránka_adresa + 0x20) = požiadavka;
    for (;;) {
        if (!(počítač_register(poštová_schránka_adresa + 0x18) & 0x40000000u)) {
            uint32_t odozva = počítač_register(poštová_schránka_adresa);
            if (odozva == požiadavka) { 기억장벽(); return poštová_schránka_údaje[1] == 0x80000000u; }
        }
        if (Hodiny_COUNT() - Spustiť_2 > FREQUENCY) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terminál_Byte(unsigned);
extern int Terminál_čakajúci(void);
extern void Terminál_ukazovateľ(unsigned,int,int),터미널바로가기키(unsigned);
extern void Terminál_vstup_MODE(unsigned);
#include "../vzdialený_VALUE/vzdialený_VALUE.h"
static int Prehľady;
static unsigned 직렬이전글자;
počítač_Word Panel_Prehľady(počítač_Word 사용여부) { Prehľady=사용여부!=0; return 0; }
počítač_Word Panel_Kanál(počítač_Word Kanál, počítač_Word bod_kódu) {
    if(Prehľady && 자바셸출력((int32_t)Kanál,(int32_t)(bod_kódu&255))) return 0;
    Terminál_Byte(bod_kódu&255);
    원격출력(bod_kódu&255);
    if ((bod_kódu&255)==10 && 직렬이전글자!=13) {
        while (počítač_register(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        počítač_register(직렬장치)=13;
    }
    직렬이전글자=bod_kódu&255;
    while (počítač_register(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    počítač_register(직렬장치) = (uint32_t)bod_kódu & 255;
    return 0;
}
počítač_Word 보드글자쓰기(počítač_Word bod_kódu) { return Panel_Kanál(1,bod_kódu); }
počítač_Word 보드원시글자읽기(void) {
    int vzdialený_znak=vzdialený_vstup();if(vzdialený_znak>=0)return vzdialený_znak;
    if (počítač_register(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t VALUE = počítač_register(직렬장치);
    if (VALUE & 0xf00) { počítač_register(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return VALUE & 255;
}
počítač_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char paket_údaje[6];
    if(Terminál_čakajúci())return (uint32_t)-4096;
    if(Prehľady){int32_t bod_kódu=자바셸입력();if(bod_kódu!=-3)return (uint32_t)bod_kódu;}
    for(;;){
        int bod_kódu=(int32_t)보드원시글자읽기();if(bod_kódu<0)return (uint32_t)bod_kódu;
        if(!꾸러미안쪽){if(bod_kódu!=30)return bod_kódu;꾸러미안쪽=1;사용량=0;continue;}
        paket_údaje[사용량++]=bod_kódu;if(사용량<6)continue;꾸러미안쪽=0;
        if(paket_údaje[0]==1)Terminál_ukazovateľ(paket_údaje[1],paket_údaje[2]+paket_údaje[3]*256,paket_údaje[4]+paket_údaje[5]*256);
        if(paket_údaje[0]==2)터미널바로가기키(paket_údaje[1]);
        if(paket_údaje[0]==3)Terminál_vstup_MODE(paket_údaje[1]);
        if(Terminál_čakajúci())return (uint32_t)-4096;
    }
}
počítač_Word 보드밀리초(void) { return (uint32_t)(Hodiny_COUNT() / (FREQUENCY / 1000)); }
počítač_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *reťazec_údaje) { while (*reťazec_údaje) 보드글자쓰기((unsigned char)*reťazec_údaje++); }
static void 직렬열여섯진출력(počítač_Word položka_COUNT) { const char *열여섯진숫자 = "0123456789abcdef"; for (int reťazec_údaje = 60; reťazec_údaje >= 0; reťazec_údaje -= 4) 보드글자쓰기(열여섯진숫자[(položka_COUNT >> reťazec_údaje) & 15]); }
počítač_Word Panel_Stop(počítač_Word Stav_VALUE) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(Stav_VALUE); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); Panel_Stop(1); __builtin_unreachable(); }
void Panel_výnimka(počítač_Word výnimka_Stav, počítač_Word príkaz_pozícia, počítač_Word neplatné_adresa) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(výnimka_Stav);
    직렬글출력(" PC="); 직렬열여섯진출력(príkaz_pozícia); 직렬글출력(" FAR="); 직렬열여섯진출력(neplatné_adresa);
    Panel_Stop(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    poštová_schránka_údaje[0]=32;poštová_schránka_údaje[1]=0;poštová_schránka_údaje[2]=0x10004;poštová_schránka_údaje[3]=8;poštová_schránka_údaje[4]=0;
    poštová_schránka_údaje[5]=poštová_schránka_údaje[6]=poštová_schránka_údaje[7]=0;
    return poštová_schránka()&&poštová_schránka_údaje[4]==0x80000008u&&(poštová_schránka_údaje[5]||poštová_schránka_údaje[6]);
}
int Panel_absolútna_adresa(unsigned char *adresa) {
    poštová_schránka_údaje[0]=32;poštová_schránka_údaje[1]=0;poštová_schránka_údaje[2]=0x10003;poštová_schránka_údaje[3]=8;poštová_schránka_údaje[4]=0;
    poštová_schránka_údaje[5]=poštová_schránka_údaje[6]=poštová_schránka_údaje[7]=0;
    if(!poštová_schránka()||(poštová_schránka_údaje[4]&0x80000000u)==0||(poštová_schránka_údaje[4]&0xffff)!=6)return 0;
    const unsigned char *údaje=(const unsigned char*)&poštová_schránka_údaje[5];unsigned SUM_VALUE=0;
    for(unsigned 순번=0;순번<6;순번++){adresa[순번]=údaje[순번];SUM_VALUE|=údaje[순번];}return SUM_VALUE&&!(adresa[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    počítač_register(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    počítač_register(범용입출력 + 4) = (počítač_register(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    počítač_register(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. zlyhanie_VALUE 시 config.txt의 48MHz를 사용한다.
    poštová_schránka_údaje[0] = 36; poštová_schránka_údaje[1] = 0; poštová_schránka_údaje[2] = 0x38002; poštová_schránka_údaje[3] = 12;
    poštová_schránka_údaje[4] = 0; poštová_schránka_údaje[5] = 2; poštová_schránka_údaje[6] = 48000000; poštová_schránka_údaje[7] = 0; poštová_schránka_údaje[8] = 0;
    int 시계정상 = poštová_schránka();
    uint32_t 속도 = 시계정상 && poštová_schránka_údaje[6] >= 1843200 ? poštová_schránka_údaje[6] : 48000000;
    poštová_schránka_údaje[0]=32; poštová_schránka_údaje[1]=0; poštová_schránka_údaje[2]=0x10005; poštová_schránka_údaje[3]=8; poštová_schránka_údaje[4]=0;
    poštová_schránka_údaje[5]=poštová_schránka_údaje[6]=poštová_schránka_údaje[7]=0;
    if (poštová_schránka() && poštová_schránka_údaje[4]==0x80000008u) 팔기억킬로바이트=poštová_schránka_údaje[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    počítač_register(직렬장치 + 0x44) = 0x7ff;
    počítač_register(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    počítač_register(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    počítač_register(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    počítač_register(직렬장치 + 0x38) = 0;
    počítač_register(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
počítač_Word Panel_FTP(počítač_Word Akcia) { return (uint32_t)ftp_control((int)Akcia); }
počítač_Word Panel_sieť_stav(počítač_Word položka_VALUE, počítač_Word INDEX) { return 망상태읽기(položka_VALUE, INDEX); }
počítač_Word Panel_sieť_Nastavenia(počítač_Word Akcia, počítač_Word adresa, počítač_Word maska_VALUE, počítač_Word brána_VALUE) { return (uint32_t)konfigurovať_sieť(Akcia, adresa, maska_VALUE, brána_VALUE); }
počítač_Word Panel_odoslať_odpoveď(počítač_Word adresa, počítač_Word poradie_VALUE) { return (uint32_t)START_odpoveď_test(adresa, poradie_VALUE); }
počítač_Word 보드응답읽기(počítač_Word položka_VALUE) { return (uint32_t)응답시험읽기(položka_VALUE); }
počítač_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEX=0; INDEX<32; INDEX++) Zavrieť_sieť(INDEX);
    for (unsigned INDEX=0; INDEX<4; INDEX++) Panel_používateľský_ovládací_prvok(32+INDEX);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (počítač_register(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    počítač_register(0xfe100020ul)=0x5a000000u | (počítač_register(0xfe100020ul)&~0xfffu) | 0x555;
    počítač_register(0xfe100024ul)=0x5a000000u | 10;
    počítač_register(0xfe10001cul)=0x5a000000u | (počítač_register(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

počítač_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 v_termíne_splatnosti_položka 크기를 읽는다. */
    const uint32_t dotaz_VALUE[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(dotaz_VALUE)/4; 순번++) poštová_schránka_údaje[순번] = dotaz_VALUE[순번];
    if (poštová_schránka() && poštová_schránka_údaje[4] == 0x80000008u &&
        poštová_schránka_údaje[5] >= 640 && poštová_schránka_údaje[5] <= 1920 &&
        poštová_schránka_údaje[6] >= 480 && poštová_schránka_údaje[6] <= 1080) {
        요청너비 = poštová_schránka_údaje[5]; 요청높이 = poštová_schránka_údaje[6];
    }
    const uint32_t požiadavka[] = {
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
    for (size_t 순번 = 0; 순번 < sizeof(požiadavka)/4; 순번++) poštová_schránka_údaje[순번] = požiadavka[순번];
    // 위 메시지의 skutočný_údaje 길이를 používať_VALUE: 태그 Pripojiť_položka 시 dĺžka_VALUE 불일치를 방지한다.
    poštová_schránka_údaje[0] = sizeof(požiadavka);
    if (!poštová_schránka()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned odpoveď_dĺžka[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (poštová_schránka_údaje[응답들[순번]] != (0x80000000u | odpoveď_dĺžka[순번])) return 0;
    uint32_t tapeta_VALUE = poštová_schránka_údaje[28] & 0x3fffffffu;
    uint32_t Veľkosť = poštová_schránka_údaje[29];
    uint32_t 받은너비 = poštová_schránka_údaje[5], RECEIVED_výška = poštová_schránka_údaje[6], RECEIVED_Riadkovanie = poštová_schránka_údaje[33];
    if (poštová_schránka_údaje[15] != 32 || poštová_schránka_údaje[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || RECEIVED_výška < 480 || RECEIVED_výška > 1080 ||
        poštová_schránka_údaje[10] < 받은너비 || poštová_schránka_údaje[11] < RECEIVED_výška || poštová_schránka_údaje[23] || poštová_schránka_údaje[24] ||
        !tapeta_VALUE || tapeta_VALUE < 0x1000000 || (tapeta_VALUE & 3) || RECEIVED_Riadkovanie < 받은너비 * 4 || (RECEIVED_Riadkovanie & 3) ||
        (uint64_t)RECEIVED_Riadkovanie * RECEIVED_výška > Veľkosť || (uint64_t)tapeta_VALUE + Veľkosť > 0x40000000u)
        return 0;
    Panel_Pripraviť_kresba((volatile uint32_t *)(uintptr_t)tapeta_VALUE, 받은너비, RECEIVED_výška, RECEIVED_Riadkovanie);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 vlákno_VALUE. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } 작업문맥;
static 작업문맥 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int Informačné_systémy_Beh[3] = {1, 0, 0};
static int v_termíne_splatnosti_úloha;
extern void prepnutie_kontextu(작업문맥 *, 작업문맥 *);
extern void 자바작업(int32_t);
počítač_Word Panel_YIELD(void) {
    network_poll();
    int 이전 = v_termíne_splatnosti_úloha, Ďalej_položka = (이전 + 1) % 3;
    while (Ďalej_položka != 이전 && !Informačné_systémy_Beh[Ďalej_položka]) Ďalej_položka = (Ďalej_položka + 1) % 3;
    if (Ďalej_položka != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (Informačné_systémy_Beh[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        v_termíne_splatnosti_úloha = Ďalej_položka;
        prepnutie_kontextu(&작업문맥들[이전], &작업문맥들[Ďalej_položka]);
    }
    return 0;
}
static void úloha_spustenie(void) {
    자바작업(v_termíne_splatnosti_úloha);
    Informačné_systémy_Beh[v_termíne_splatnosti_úloha] = 0;
    Panel_YIELD();
    커널중단("finished task resumed");
}
počítač_Word Panel_úloha_Create(počítač_Word identifikátor_VALUE) {
    if (identifikátor_VALUE < 1 || identifikátor_VALUE > 2 || Informačné_systémy_Beh[identifikátor_VALUE]) return (uint32_t)-1;
    memset(&작업문맥들[identifikátor_VALUE], 0, sizeof(작업문맥));
    *(uint64_t *)쌓임공간들[identifikátor_VALUE - 1] = 0x6b6f726f7373746bull;
    작업문맥들[identifikátor_VALUE].저장값[11] = (uintptr_t)úloha_spustenie;
    작업문맥들[identifikátor_VALUE].저장값[12] = (uintptr_t)(쌓임공간들[identifikátor_VALUE - 1] + sizeof(쌓임공간들[0]));
    Informačné_systémy_Beh[identifikátor_VALUE] = 1;
    return 0;
}
počítač_Word Panel_úloha_Stav(počítač_Word identifikátor_VALUE) { return identifikátor_VALUE < 3 ? Informačné_systémy_Beh[identifikátor_VALUE] : (uint32_t)-1; }
extern počítač_Word 미리번역기억조회(počítač_Word);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
počítač_Word Panel_dotaz_systém(počítač_Word položka_VALUE, počítač_Word INDEX) {
    if (položka_VALUE==0) return 팔기억킬로바이트;
    if (položka_VALUE==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (položka_VALUE==2 || položka_VALUE==3) return 미리번역기억조회(položka_VALUE==3);
    if (položka_VALUE==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (položka_VALUE==5) return 80*1024; /* Vykonať_príkaz adresa_oblasť 16 MiB + 네 세션 보관 adresa_oblasť. */
    if (položka_VALUE>=20) return 사용자상태읽기(položka_VALUE-20, INDEX);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[v_termíne_splatnosti_úloha]; }
