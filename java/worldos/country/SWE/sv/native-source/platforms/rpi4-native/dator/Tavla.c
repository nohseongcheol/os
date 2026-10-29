#include "../명명/기계연결이름.h"
#include "skärmbild_info.h"
#include <stdint.h>
#include <stddef.h>
#include "användarutrymme.h"
#include "../nätverk_Stack/nätverk_Stack.h"
typedef uintptr_t dator_Ord;
#define dator_register(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define postlåda_ADRESS 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Klocka_ANTAL(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t FREKVENS;
static volatile uint32_t postlåda_data[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *data_placera, int kodpunkt, size_t objekt_ANTAL) { unsigned char *Nästa_FÖRSKJUTNING = data_placera; while (objekt_ANTAL--) *Nästa_FÖRSKJUTNING++ = kodpunkt; return data_placera; }
void *memcpy(void *mål_data, const void *sträng_data, size_t objekt_ANTAL) { unsigned char *첫째값 = mål_data; const unsigned char *SEKUND_värde = sträng_data; while (objekt_ANTAL--) *첫째값++ = *SEKUND_värde++; return mål_data; }

static int postlåda(void) {
    uint32_t begäran = (uint32_t)(uintptr_t)postlåda_data | 8;
    uint64_t Kör = Klocka_ANTAL();
    기억장벽();
    while (dator_register(postlåda_ADRESS + 0x38) & 0x80000000u)
        if (Klocka_ANTAL() - Kör > FREKVENS) return 0;
    dator_register(postlåda_ADRESS + 0x20) = begäran;
    for (;;) {
        if (!(dator_register(postlåda_ADRESS + 0x18) & 0x40000000u)) {
            uint32_t svara = dator_register(postlåda_ADRESS);
            if (svara == begäran) { 기억장벽(); return postlåda_data[1] == 0x80000000u; }
        }
        if (Klocka_ANTAL() - Kör > FREKVENS) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terminal_byte(unsigned);
extern int Terminal_väntar(void);
extern void Terminal_markör(unsigned,int,int),터미널바로가기키(unsigned);
extern void Terminal_indata_läge(unsigned);
#include "../fjärr_värde/fjärr_värde.h"
static int Flöden;
static unsigned 직렬이전글자;
dator_Ord Tavla_Flöden(dator_Ord 사용여부) { Flöden=사용여부!=0; return 0; }
dator_Ord Tavla_Kanal(dator_Ord Kanal, dator_Ord kodpunkt) {
    if(Flöden && 자바셸출력((int32_t)Kanal,(int32_t)(kodpunkt&255))) return 0;
    Terminal_byte(kodpunkt&255);
    fjärr_utleverans(kodpunkt&255);
    if ((kodpunkt&255)==10 && 직렬이전글자!=13) {
        while (dator_register(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        dator_register(직렬장치)=13;
    }
    직렬이전글자=kodpunkt&255;
    while (dator_register(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    dator_register(직렬장치) = (uint32_t)kodpunkt & 255;
    return 0;
}
dator_Ord 보드글자쓰기(dator_Ord kodpunkt) { return Tavla_Kanal(1,kodpunkt); }
dator_Ord 보드원시글자읽기(void) {
    int fjärr_tecken=fjärr_indata();if(fjärr_tecken>=0)return fjärr_tecken;
    if (dator_register(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t värde = dator_register(직렬장치);
    if (värde & 0xf00) { dator_register(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return värde & 255;
}
dator_Ord 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char paket_data[6];
    if(Terminal_väntar())return (uint32_t)-4096;
    if(Flöden){int32_t kodpunkt=자바셸입력();if(kodpunkt!=-3)return (uint32_t)kodpunkt;}
    for(;;){
        int kodpunkt=(int32_t)보드원시글자읽기();if(kodpunkt<0)return (uint32_t)kodpunkt;
        if(!꾸러미안쪽){if(kodpunkt!=30)return kodpunkt;꾸러미안쪽=1;사용량=0;continue;}
        paket_data[사용량++]=kodpunkt;if(사용량<6)continue;꾸러미안쪽=0;
        if(paket_data[0]==1)Terminal_markör(paket_data[1],paket_data[2]+paket_data[3]*256,paket_data[4]+paket_data[5]*256);
        if(paket_data[0]==2)터미널바로가기키(paket_data[1]);
        if(paket_data[0]==3)Terminal_indata_läge(paket_data[1]);
        if(Terminal_väntar())return (uint32_t)-4096;
    }
}
dator_Ord 보드밀리초(void) { return (uint32_t)(Klocka_ANTAL() / (FREKVENS / 1000)); }
dator_Ord 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *sträng_data) { while (*sträng_data) 보드글자쓰기((unsigned char)*sträng_data++); }
static void 직렬열여섯진출력(dator_Ord objekt_ANTAL) { const char *열여섯진숫자 = "0123456789abcdef"; for (int sträng_data = 60; sträng_data >= 0; sträng_data -= 4) 보드글자쓰기(열여섯진숫자[(objekt_ANTAL >> sträng_data) & 15]); }
dator_Ord Tavla_Stopp(dator_Ord status_värde) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(status_värde); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); Tavla_Stopp(1); __builtin_unreachable(); }
void Tavla_fel(dator_Ord fel_status, dator_Ord kommando_placera, dator_Ord ogiltig_ADRESS) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(fel_status);
    직렬글출력(" PC="); 직렬열여섯진출력(kommando_placera); 직렬글출력(" FAR="); 직렬열여섯진출력(ogiltig_ADRESS);
    Tavla_Stopp(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    postlåda_data[0]=32;postlåda_data[1]=0;postlåda_data[2]=0x10004;postlåda_data[3]=8;postlåda_data[4]=0;
    postlåda_data[5]=postlåda_data[6]=postlåda_data[7]=0;
    return postlåda()&&postlåda_data[4]==0x80000008u&&(postlåda_data[5]||postlåda_data[6]);
}
int Tavla_absolut_adress(unsigned char *Adress) {
    postlåda_data[0]=32;postlåda_data[1]=0;postlåda_data[2]=0x10003;postlåda_data[3]=8;postlåda_data[4]=0;
    postlåda_data[5]=postlåda_data[6]=postlåda_data[7]=0;
    if(!postlåda()||(postlåda_data[4]&0x80000000u)==0||(postlåda_data[4]&0xffff)!=6)return 0;
    const unsigned char *data=(const unsigned char*)&postlåda_data[5];unsigned SUM_värde=0;
    for(unsigned 순번=0;순번<6;순번++){Adress[순번]=data[순번];SUM_värde|=data[순번];}return SUM_värde&&!(Adress[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREKVENS));
    dator_register(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    dator_register(범용입출력 + 4) = (dator_register(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    dator_register(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. fel_värde 시 config.txt의 48MHz를 사용한다.
    postlåda_data[0] = 36; postlåda_data[1] = 0; postlåda_data[2] = 0x38002; postlåda_data[3] = 12;
    postlåda_data[4] = 0; postlåda_data[5] = 2; postlåda_data[6] = 48000000; postlåda_data[7] = 0; postlåda_data[8] = 0;
    int Klocka_felfri = postlåda();
    uint32_t 속도 = Klocka_felfri && postlåda_data[6] >= 1843200 ? postlåda_data[6] : 48000000;
    postlåda_data[0]=32; postlåda_data[1]=0; postlåda_data[2]=0x10005; postlåda_data[3]=8; postlåda_data[4]=0;
    postlåda_data[5]=postlåda_data[6]=postlåda_data[7]=0;
    if (postlåda() && postlåda_data[4]==0x80000008u) 팔기억킬로바이트=postlåda_data[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    dator_register(직렬장치 + 0x44) = 0x7ff;
    dator_register(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    dator_register(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    dator_register(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    dator_register(직렬장치 + 0x38) = 0;
    dator_register(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
dator_Ord Tavla_FTP(dator_Ord Åtgärd) { return (uint32_t)ftp_control((int)Åtgärd); }
dator_Ord Tavla_nätverk_status(dator_Ord post_värde, dator_Ord INDEX) { return läsa_nätverk_status(post_värde, INDEX); }
dator_Ord Tavla_nätverk_Inställningar(dator_Ord Åtgärd, dator_Ord Adress, dator_Ord mask_värde, dator_Ord gateway_värde) { return (uint32_t)konfigurera_nätverk(Åtgärd, Adress, mask_värde, gateway_värde); }
dator_Ord Tavla_skicka_svar(dator_Ord Adress, dator_Ord order_värde) { return (uint32_t)START_svar_test(Adress, order_värde); }
dator_Ord Tavla_läsa_svar(dator_Ord post_värde) { return (uint32_t)läsa_svar_test(post_värde); }
dator_Ord 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEX=0; INDEX<32; INDEX++) Stäng_nätverk(INDEX);
    for (unsigned INDEX=0; INDEX<4; INDEX++) Tavla_användarkontroll(32+INDEX);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (dator_register(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    dator_register(0xfe100020ul)=0x5a000000u | (dator_register(0xfe100020ul)&~0xfffu) | 0x555;
    dator_register(0xfe100024ul)=0x5a000000u | 10;
    dator_register(0xfe10001cul)=0x5a000000u | (dator_register(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

dator_Ord 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 aktuellt_objekt 크기를 읽는다. */
    const uint32_t fråga_värde[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(fråga_värde)/4; 순번++) postlåda_data[순번] = fråga_värde[순번];
    if (postlåda() && postlåda_data[4] == 0x80000008u &&
        postlåda_data[5] >= 640 && postlåda_data[5] <= 1920 &&
        postlåda_data[6] >= 480 && postlåda_data[6] <= 1080) {
        요청너비 = postlåda_data[5]; 요청높이 = postlåda_data[6];
    }
    const uint32_t begäran[] = {
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
    for (size_t 순번 = 0; 순번 < sizeof(begäran)/4; 순번++) postlåda_data[순번] = begäran[순번];
    // 위 메시지의 verklig_data 길이를 använda_värde: 태그 Lägga_till_post 시 längd_värde 불일치를 방지한다.
    postlåda_data[0] = sizeof(begäran);
    if (!postlåda()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned svar_längd[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (postlåda_data[응답들[순번]] != (0x80000000u | svar_längd[순번])) return 0;
    uint32_t Bakgrund_värde = postlåda_data[28] & 0x3fffffffu;
    uint32_t Storlek = postlåda_data[29];
    uint32_t 받은너비 = postlåda_data[5], 받은높이 = postlåda_data[6], BELOPP_avstånd = postlåda_data[33];
    if (postlåda_data[15] != 32 || postlåda_data[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        postlåda_data[10] < 받은너비 || postlåda_data[11] < 받은높이 || postlåda_data[23] || postlåda_data[24] ||
        !Bakgrund_värde || Bakgrund_värde < 0x1000000 || (Bakgrund_värde & 3) || BELOPP_avstånd < 받은너비 * 4 || (BELOPP_avstånd & 3) ||
        (uint64_t)BELOPP_avstånd * 받은높이 > Storlek || (uint64_t)Bakgrund_värde + Storlek > 0x40000000u)
        return 0;
    Tavla_Förbereda_ritning((volatile uint32_t *)(uintptr_t)Bakgrund_värde, 받은너비, 받은높이, BELOPP_avstånd);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 tråd_värde. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } sammanhang;
static sammanhang 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int informationsteknik_Löpning[3] = {1, 0, 0};
static int aktuellt_uppgift;
extern void kontextbyte(sammanhang *, sammanhang *);
extern void 자바작업(int32_t);
dator_Ord Tavla_NOMAVK(void) {
    network_poll();
    int Föregående_objekt = aktuellt_uppgift, Nästa_objekt = (Föregående_objekt + 1) % 3;
    while (Nästa_objekt != Föregående_objekt && !informationsteknik_Löpning[Nästa_objekt]) Nästa_objekt = (Nästa_objekt + 1) % 3;
    if (Nästa_objekt != Föregående_objekt) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (informationsteknik_Löpning[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        aktuellt_uppgift = Nästa_objekt;
        kontextbyte(&작업문맥들[Föregående_objekt], &작업문맥들[Nästa_objekt]);
    }
    return 0;
}
static void uppgift_start(void) {
    자바작업(aktuellt_uppgift);
    informationsteknik_Löpning[aktuellt_uppgift] = 0;
    Tavla_NOMAVK();
    커널중단("finished task resumed");
}
dator_Ord Tavla_uppgift_Skapa(dator_Ord identifierare_värde) {
    if (identifierare_värde < 1 || identifierare_värde > 2 || informationsteknik_Löpning[identifierare_värde]) return (uint32_t)-1;
    memset(&작업문맥들[identifierare_värde], 0, sizeof(sammanhang));
    *(uint64_t *)쌓임공간들[identifierare_värde - 1] = 0x6b6f726f7373746bull;
    작업문맥들[identifierare_värde].저장값[11] = (uintptr_t)uppgift_start;
    작업문맥들[identifierare_värde].저장값[12] = (uintptr_t)(쌓임공간들[identifierare_värde - 1] + sizeof(쌓임공간들[0]));
    informationsteknik_Löpning[identifierare_värde] = 1;
    return 0;
}
dator_Ord Tavla_uppgift_status(dator_Ord identifierare_värde) { return identifierare_värde < 3 ? informationsteknik_Löpning[identifierare_värde] : (uint32_t)-1; }
extern dator_Ord AOT_Minne_LETAUPP(dator_Ord);
extern uint32_t läsa_användare_status(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
dator_Ord Tavla_fråga_System(dator_Ord post_värde, dator_Ord INDEX) {
    if (post_värde==0) return 팔기억킬로바이트;
    if (post_värde==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (post_värde==2 || post_värde==3) return AOT_Minne_LETAUPP(post_värde==3);
    if (post_värde==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (post_värde==5) return 80*1024; /* köra_kommando ADRESS_område 16 MiB + 네 세션 보관 ADRESS_område. */
    if (post_värde>=20) return läsa_användare_status(post_värde-20, INDEX);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[aktuellt_uppgift]; }
