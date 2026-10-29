#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "uživatelský_prostor.h"
#include "../síť_Štos/síť_Štos.h"
typedef uintptr_t počítač_Word;
#define počítač_registr(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define poštovní_schránka_ODKAZ 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Hodiny_POČET(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t ČETNOSTI;
static volatile uint32_t poštovní_schránka_data[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *data_pozice, int bod_kódu, size_t zboží_POČET) { unsigned char *Další_POSUN = data_pozice; while (zboží_POČET--) *Další_POSUN++ = bod_kódu; return data_pozice; }
void *memcpy(void *cíl_data, const void *řetězec_data, size_t zboží_POČET) { unsigned char *첫째값 = cíl_data; const unsigned char *SEKUNDA_HODNOTA = řetězec_data; while (zboží_POČET--) *첫째값++ = *SEKUNDA_HODNOTA++; return cíl_data; }

static int poštovní_schránka(void) {
    uint32_t žádost = (uint32_t)(uintptr_t)poštovní_schránka_data | 8;
    uint64_t Spustit_2 = Hodiny_POČET();
    기억장벽();
    while (počítač_registr(poštovní_schránka_ODKAZ + 0x38) & 0x80000000u)
        if (Hodiny_POČET() - Spustit_2 > ČETNOSTI) return 0;
    počítač_registr(poštovní_schránka_ODKAZ + 0x20) = žádost;
    for (;;) {
        if (!(počítač_registr(poštovní_schránka_ODKAZ + 0x18) & 0x40000000u)) {
            uint32_t odezva = počítač_registr(poštovní_schránka_ODKAZ);
            if (odezva == žádost) { 기억장벽(); return poštovní_schránka_data[1] == 0x80000000u; }
        }
        if (Hodiny_POČET() - Spustit_2 > ČETNOSTI) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terminál_bajt(unsigned);
extern int Terminál_probíhá(void);
extern void Terminál_ukazatel(unsigned,int,int),터미널바로가기키(unsigned);
extern void Terminál_vstup_MODE(unsigned);
#include "../vzdálený_HODNOTA/vzdálený_HODNOTA.h"
static int Toky;
static unsigned 직렬이전글자;
počítač_Word Panel_Toky(počítač_Word 사용여부) { Toky=사용여부!=0; return 0; }
počítač_Word Panel_Kanál(počítač_Word Kanál, počítač_Word bod_kódu) {
    if(Toky && 자바셸출력((int32_t)Kanál,(int32_t)(bod_kódu&255))) return 0;
    Terminál_bajt(bod_kódu&255);
    vzdálený_výstup(bod_kódu&255);
    if ((bod_kódu&255)==10 && 직렬이전글자!=13) {
        while (počítač_registr(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        počítač_registr(직렬장치)=13;
    }
    직렬이전글자=bod_kódu&255;
    while (počítač_registr(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    počítač_registr(직렬장치) = (uint32_t)bod_kódu & 255;
    return 0;
}
počítač_Word 보드글자쓰기(počítač_Word bod_kódu) { return Panel_Kanál(1,bod_kódu); }
počítač_Word 보드원시글자읽기(void) {
    int vzdálený_znak=vzdálený_vstup();if(vzdálený_znak>=0)return vzdálený_znak;
    if (počítač_registr(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t HODNOTA = počítač_registr(직렬장치);
    if (HODNOTA & 0xf00) { počítač_registr(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return HODNOTA & 255;
}
počítač_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char paket_data[6];
    if(Terminál_probíhá())return (uint32_t)-4096;
    if(Toky){int32_t bod_kódu=자바셸입력();if(bod_kódu!=-3)return (uint32_t)bod_kódu;}
    for(;;){
        int bod_kódu=(int32_t)보드원시글자읽기();if(bod_kódu<0)return (uint32_t)bod_kódu;
        if(!꾸러미안쪽){if(bod_kódu!=30)return bod_kódu;꾸러미안쪽=1;사용량=0;continue;}
        paket_data[사용량++]=bod_kódu;if(사용량<6)continue;꾸러미안쪽=0;
        if(paket_data[0]==1)Terminál_ukazatel(paket_data[1],paket_data[2]+paket_data[3]*256,paket_data[4]+paket_data[5]*256);
        if(paket_data[0]==2)터미널바로가기키(paket_data[1]);
        if(paket_data[0]==3)Terminál_vstup_MODE(paket_data[1]);
        if(Terminál_probíhá())return (uint32_t)-4096;
    }
}
počítač_Word 보드밀리초(void) { return (uint32_t)(Hodiny_POČET() / (ČETNOSTI / 1000)); }
počítač_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *řetězec_data) { while (*řetězec_data) 보드글자쓰기((unsigned char)*řetězec_data++); }
static void 직렬열여섯진출력(počítač_Word zboží_POČET) { const char *열여섯진숫자 = "0123456789abcdef"; for (int řetězec_data = 60; řetězec_data >= 0; řetězec_data -= 4) 보드글자쓰기(열여섯진숫자[(zboží_POČET >> řetězec_data) & 15]); }
počítač_Word Panel_Stop(počítač_Word Stav_HODNOTA) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(Stav_HODNOTA); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); Panel_Stop(1); __builtin_unreachable(); }
void Panel_výjimka(počítač_Word výjimka_Stav, počítač_Word příkaz_pozice, počítač_Word neplatný_ODKAZ) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(výjimka_Stav);
    직렬글출력(" PC="); 직렬열여섯진출력(příkaz_pozice); 직렬글출력(" FAR="); 직렬열여섯진출력(neplatný_ODKAZ);
    Panel_Stop(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    poštovní_schránka_data[0]=32;poštovní_schránka_data[1]=0;poštovní_schránka_data[2]=0x10004;poštovní_schránka_data[3]=8;poštovní_schránka_data[4]=0;
    poštovní_schránka_data[5]=poštovní_schránka_data[6]=poštovní_schránka_data[7]=0;
    return poštovní_schránka()&&poštovní_schránka_data[4]==0x80000008u&&(poštovní_schránka_data[5]||poštovní_schránka_data[6]);
}
int Panel_absolutní_adresa(unsigned char *Adresa) {
    poštovní_schránka_data[0]=32;poštovní_schránka_data[1]=0;poštovní_schránka_data[2]=0x10003;poštovní_schránka_data[3]=8;poštovní_schránka_data[4]=0;
    poštovní_schránka_data[5]=poštovní_schránka_data[6]=poštovní_schránka_data[7]=0;
    if(!poštovní_schránka()||(poštovní_schránka_data[4]&0x80000000u)==0||(poštovní_schránka_data[4]&0xffff)!=6)return 0;
    const unsigned char *data=(const unsigned char*)&poštovní_schránka_data[5];unsigned SUMA_HODNOTA=0;
    for(unsigned 순번=0;순번<6;순번++){Adresa[순번]=data[순번];SUMA_HODNOTA|=data[순번];}return SUMA_HODNOTA&&!(Adresa[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(ČETNOSTI));
    počítač_registr(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    počítač_registr(범용입출력 + 4) = (počítač_registr(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    počítač_registr(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. selhání_HODNOTA 시 config.txt의 48MHz를 사용한다.
    poštovní_schránka_data[0] = 36; poštovní_schránka_data[1] = 0; poštovní_schránka_data[2] = 0x38002; poštovní_schránka_data[3] = 12;
    poštovní_schránka_data[4] = 0; poštovní_schránka_data[5] = 2; poštovní_schránka_data[6] = 48000000; poštovní_schránka_data[7] = 0; poštovní_schránka_data[8] = 0;
    int Hodiny_v_pořádku = poštovní_schránka();
    uint32_t 속도 = Hodiny_v_pořádku && poštovní_schránka_data[6] >= 1843200 ? poštovní_schránka_data[6] : 48000000;
    poštovní_schránka_data[0]=32; poštovní_schránka_data[1]=0; poštovní_schránka_data[2]=0x10005; poštovní_schránka_data[3]=8; poštovní_schránka_data[4]=0;
    poštovní_schránka_data[5]=poštovní_schránka_data[6]=poštovní_schránka_data[7]=0;
    if (poštovní_schránka() && poštovní_schránka_data[4]==0x80000008u) 팔기억킬로바이트=poštovní_schránka_data[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    počítač_registr(직렬장치 + 0x44) = 0x7ff;
    počítač_registr(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    počítač_registr(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    počítač_registr(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    počítač_registr(직렬장치 + 0x38) = 0;
    počítač_registr(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
počítač_Word Panel_protokol_FTP(počítač_Word Akce) { return (uint32_t)ftp_control((int)Akce); }
počítač_Word Panel_síť_stav(počítač_Word položka_HODNOTA, počítač_Word INDEX) { return 망상태읽기(položka_HODNOTA, INDEX); }
počítač_Word Panel_síť_Nastavení(počítač_Word Akce, počítač_Word Adresa, počítač_Word maska_HODNOTA, počítač_Word brána_HODNOTA) { return (uint32_t)konfigurovat_síť(Akce, Adresa, maska_HODNOTA, brána_HODNOTA); }
počítač_Word Panel_poslat_odpověď(počítač_Word Adresa, počítač_Word pořadí_HODNOTA) { return (uint32_t)START_odpověď_test(Adresa, pořadí_HODNOTA); }
počítač_Word 보드응답읽기(počítač_Word položka_HODNOTA) { return (uint32_t)응답시험읽기(položka_HODNOTA); }
počítač_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEX=0; INDEX<32; INDEX++) Zavřít_síť(INDEX);
    for (unsigned INDEX=0; INDEX<4; INDEX++) Panel_uživatelský_ovládací_prvek(32+INDEX);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (počítač_registr(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    počítač_registr(0xfe100020ul)=0x5a000000u | (počítač_registr(0xfe100020ul)&~0xfffu) | 0x555;
    počítač_registr(0xfe100024ul)=0x5a000000u | 10;
    počítač_registr(0xfe10001cul)=0x5a000000u | (počítač_registr(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

počítač_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 dobrá_zboží 크기를 읽는다. */
    const uint32_t dotaz_HODNOTA[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, vyžádáno_výška = 480;
    for (size_t 순번 = 0; 순번 < sizeof(dotaz_HODNOTA)/4; 순번++) poštovní_schránka_data[순번] = dotaz_HODNOTA[순번];
    if (poštovní_schránka() && poštovní_schránka_data[4] == 0x80000008u &&
        poštovní_schránka_data[5] >= 640 && poštovní_schránka_data[5] <= 1920 &&
        poštovní_schránka_data[6] >= 480 && poštovní_schránka_data[6] <= 1080) {
        요청너비 = poštovní_schránka_data[5]; vyžádáno_výška = poštovní_schránka_data[6];
    }
    const uint32_t žádost[] = {
        35 * 4, 0,
        0x48003, 8, 0, 요청너비, vyžádáno_výška,
        0x48004, 8, 0, 요청너비, vyžádáno_výška,
        0x48005, 4, 0, 32,
        0x48006, 4, 0, 1,
        0x48009, 8, 0, 0, 0,
        0x40001, 8, 0, 4096, 0,
        0x40008, 4, 0, 0,
        0
    };
    for (size_t 순번 = 0; 순번 < sizeof(žádost)/4; 순번++) poštovní_schránka_data[순번] = žádost[순번];
    // 위 메시지의 skutečný_data 길이를 použít_HODNOTA: 태그 Připojit_položka 시 délka_HODNOTA 불일치를 방지한다.
    poštovní_schránka_data[0] = sizeof(žádost);
    if (!poštovní_schránka()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned odpověď_délka[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (poštovní_schránka_data[응답들[순번]] != (0x80000000u | odpověď_délka[순번])) return 0;
    uint32_t Pozadí_HODNOTA = poštovní_schránka_data[28] & 0x3fffffffu;
    uint32_t Velikost = poštovní_schránka_data[29];
    uint32_t 받은너비 = poštovní_schránka_data[5], RECEIVED_výška = poštovní_schránka_data[6], RECEIVED_řádkování = poštovní_schránka_data[33];
    if (poštovní_schránka_data[15] != 32 || poštovní_schránka_data[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || RECEIVED_výška < 480 || RECEIVED_výška > 1080 ||
        poštovní_schránka_data[10] < 받은너비 || poštovní_schránka_data[11] < RECEIVED_výška || poštovní_schránka_data[23] || poštovní_schránka_data[24] ||
        !Pozadí_HODNOTA || Pozadí_HODNOTA < 0x1000000 || (Pozadí_HODNOTA & 3) || RECEIVED_řádkování < 받은너비 * 4 || (RECEIVED_řádkování & 3) ||
        (uint64_t)RECEIVED_řádkování * RECEIVED_výška > Velikost || (uint64_t)Pozadí_HODNOTA + Velikost > 0x40000000u)
        return 0;
    Panel_Připravit_kreslení((volatile uint32_t *)(uintptr_t)Pozadí_HODNOTA, 받은너비, RECEIVED_výška, RECEIVED_řádkování);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 vlákno_HODNOTA. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } kontext;
static kontext 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int informační_systémy_Běh[3] = {1, 0, 0};
static int dobrá_úkol;
extern void přepnutí_kontextu(kontext *, kontext *);
extern void 자바작업(int32_t);
počítač_Word Panel_YIELD(void) {
    network_poll();
    int Předchozí_zboží = dobrá_úkol, Další_zboží = (Předchozí_zboží + 1) % 3;
    while (Další_zboží != Předchozí_zboží && !informační_systémy_Běh[Další_zboží]) Další_zboží = (Další_zboží + 1) % 3;
    if (Další_zboží != Předchozí_zboží) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (informační_systémy_Běh[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        dobrá_úkol = Další_zboží;
        přepnutí_kontextu(&작업문맥들[Předchozí_zboží], &작업문맥들[Další_zboží]);
    }
    return 0;
}
static void úkol_spuštění(void) {
    자바작업(dobrá_úkol);
    informační_systémy_Běh[dobrá_úkol] = 0;
    Panel_YIELD();
    커널중단("finished task resumed");
}
počítač_Word Panel_úkol_Create(počítač_Word identifikátor_HODNOTA) {
    if (identifikátor_HODNOTA < 1 || identifikátor_HODNOTA > 2 || informační_systémy_Běh[identifikátor_HODNOTA]) return (uint32_t)-1;
    memset(&작업문맥들[identifikátor_HODNOTA], 0, sizeof(kontext));
    *(uint64_t *)쌓임공간들[identifikátor_HODNOTA - 1] = 0x6b6f726f7373746bull;
    작업문맥들[identifikátor_HODNOTA].저장값[11] = (uintptr_t)úkol_spuštění;
    작업문맥들[identifikátor_HODNOTA].저장값[12] = (uintptr_t)(쌓임공간들[identifikátor_HODNOTA - 1] + sizeof(쌓임공간들[0]));
    informační_systémy_Běh[identifikátor_HODNOTA] = 1;
    return 0;
}
počítač_Word Panel_úkol_Stav(počítač_Word identifikátor_HODNOTA) { return identifikátor_HODNOTA < 3 ? informační_systémy_Běh[identifikátor_HODNOTA] : (uint32_t)-1; }
extern počítač_Word AOT_Paměť_VYHLEDAT(počítač_Word);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
počítač_Word Panel_dotaz_Systém(počítač_Word položka_HODNOTA, počítač_Word INDEX) {
    if (položka_HODNOTA==0) return 팔기억킬로바이트;
    if (položka_HODNOTA==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (položka_HODNOTA==2 || položka_HODNOTA==3) return AOT_Paměť_VYHLEDAT(položka_HODNOTA==3);
    if (položka_HODNOTA==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (položka_HODNOTA==5) return 80*1024; /* Provést_příkaz ODKAZ_oblast 16 MiB + 네 세션 보관 ODKAZ_oblast. */
    if (položka_HODNOTA>=20) return 사용자상태읽기(položka_HODNOTA-20, INDEX);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[dobrá_úkol]; }
