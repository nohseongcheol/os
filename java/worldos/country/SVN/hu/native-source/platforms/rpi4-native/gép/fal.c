#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "felhasználó.h"
#include "../hálózat_Sor/hálózat_Sor.h"
typedef uintptr_t gép_szó;
#define gép_jegyzék(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define postaláda_CÍM 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Óra_DARAB(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t GYAKORISÁG;
static volatile uint32_t postaláda_adat[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *adat_pozíció, int kódpont, size_t cikk_DARAB) { unsigned char *Tovább_Ofszet = adat_pozíció; while (cikk_DARAB--) *Tovább_Ofszet++ = kódpont; return adat_pozíció; }
void *memcpy(void *cél_adat, const void *sztring_adat, size_t cikk_DARAB) { unsigned char *첫째값 = cél_adat; const unsigned char *MPERC_ÉRTÉK = sztring_adat; while (cikk_DARAB--) *첫째값++ = *MPERC_ÉRTÉK++; return cél_adat; }

static int postaláda(void) {
    uint32_t kérés = (uint32_t)(uintptr_t)postaláda_adat | 8;
    uint64_t Futtatás = Óra_DARAB();
    기억장벽();
    while (gép_jegyzék(postaláda_CÍM + 0x38) & 0x80000000u)
        if (Óra_DARAB() - Futtatás > GYAKORISÁG) return 0;
    gép_jegyzék(postaláda_CÍM + 0x20) = kérés;
    for (;;) {
        if (!(gép_jegyzék(postaláda_CÍM + 0x18) & 0x40000000u)) {
            uint32_t válasz = gép_jegyzék(postaláda_CÍM);
            if (válasz == kérés) { 기억장벽(); return postaláda_adat[1] == 0x80000000u; }
        }
        if (Óra_DARAB() - Futtatás > GYAKORISÁG) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terminál_bájt(unsigned);
extern int Terminál_Függő(void);
extern void Terminál_mutató(unsigned,int,int),터미널바로가기키(unsigned);
extern void Terminál_bevitel_mód(unsigned);
#include "../távoli_ÉRTÉK/távoli_ÉRTÉK.h"
static int adatfolyamok;
static unsigned 직렬이전글자;
gép_szó fal_adatfolyamok(gép_szó 사용여부) { adatfolyamok=사용여부!=0; return 0; }
gép_szó fal_Csatorna(gép_szó Csatorna, gép_szó kódpont) {
    if(adatfolyamok && 자바셸출력((int32_t)Csatorna,(int32_t)(kódpont&255))) return 0;
    Terminál_bájt(kódpont&255);
    távoli_kimenet(kódpont&255);
    if ((kódpont&255)==10 && 직렬이전글자!=13) {
        while (gép_jegyzék(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        gép_jegyzék(직렬장치)=13;
    }
    직렬이전글자=kódpont&255;
    while (gép_jegyzék(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    gép_jegyzék(직렬장치) = (uint32_t)kódpont & 255;
    return 0;
}
gép_szó 보드글자쓰기(gép_szó kódpont) { return fal_Csatorna(1,kódpont); }
gép_szó 보드원시글자읽기(void) {
    int távoli_karakter=távoli_bevitel();if(távoli_karakter>=0)return távoli_karakter;
    if (gép_jegyzék(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t ÉRTÉK = gép_jegyzék(직렬장치);
    if (ÉRTÉK & 0xf00) { gép_jegyzék(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return ÉRTÉK & 255;
}
gép_szó 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char csomag_adat[6];
    if(Terminál_Függő())return (uint32_t)-4096;
    if(adatfolyamok){int32_t kódpont=자바셸입력();if(kódpont!=-3)return (uint32_t)kódpont;}
    for(;;){
        int kódpont=(int32_t)보드원시글자읽기();if(kódpont<0)return (uint32_t)kódpont;
        if(!꾸러미안쪽){if(kódpont!=30)return kódpont;꾸러미안쪽=1;사용량=0;continue;}
        csomag_adat[사용량++]=kódpont;if(사용량<6)continue;꾸러미안쪽=0;
        if(csomag_adat[0]==1)Terminál_mutató(csomag_adat[1],csomag_adat[2]+csomag_adat[3]*256,csomag_adat[4]+csomag_adat[5]*256);
        if(csomag_adat[0]==2)터미널바로가기키(csomag_adat[1]);
        if(csomag_adat[0]==3)Terminál_bevitel_mód(csomag_adat[1]);
        if(Terminál_Függő())return (uint32_t)-4096;
    }
}
gép_szó 보드밀리초(void) { return (uint32_t)(Óra_DARAB() / (GYAKORISÁG / 1000)); }
gép_szó 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *sztring_adat) { while (*sztring_adat) 보드글자쓰기((unsigned char)*sztring_adat++); }
static void 직렬열여섯진출력(gép_szó cikk_DARAB) { const char *열여섯진숫자 = "0123456789abcdef"; for (int sztring_adat = 60; sztring_adat >= 0; sztring_adat -= 4) 보드글자쓰기(열여섯진숫자[(cikk_DARAB >> sztring_adat) & 15]); }
gép_szó fal_Állj(gép_szó Állapot_ÉRTÉK) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(Állapot_ÉRTÉK); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); fal_Állj(1); __builtin_unreachable(); }
void fal_kivétel(gép_szó kivétel_Állapot, gép_szó parancs_pozíció, gép_szó alaptalan_CÍM) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(kivétel_Állapot);
    직렬글출력(" PC="); 직렬열여섯진출력(parancs_pozíció); 직렬글출력(" FAR="); 직렬열여섯진출력(alaptalan_CÍM);
    fal_Állj(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    postaláda_adat[0]=32;postaláda_adat[1]=0;postaláda_adat[2]=0x10004;postaláda_adat[3]=8;postaláda_adat[4]=0;
    postaláda_adat[5]=postaláda_adat[6]=postaláda_adat[7]=0;
    return postaláda()&&postaláda_adat[4]==0x80000008u&&(postaláda_adat[5]||postaláda_adat[6]);
}
int fal_valódi_cím(unsigned char *CÍM) {
    postaláda_adat[0]=32;postaláda_adat[1]=0;postaláda_adat[2]=0x10003;postaláda_adat[3]=8;postaláda_adat[4]=0;
    postaláda_adat[5]=postaláda_adat[6]=postaláda_adat[7]=0;
    if(!postaláda()||(postaláda_adat[4]&0x80000000u)==0||(postaláda_adat[4]&0xffff)!=6)return 0;
    const unsigned char *adat=(const unsigned char*)&postaláda_adat[5];unsigned SUM_ÉRTÉK=0;
    for(unsigned 순번=0;순번<6;순번++){CÍM[순번]=adat[순번];SUM_ÉRTÉK|=adat[순번];}return SUM_ÉRTÉK&&!(CÍM[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(GYAKORISÁG));
    gép_jegyzék(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    gép_jegyzék(범용입출력 + 4) = (gép_jegyzék(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    gép_jegyzék(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. hiba_ÉRTÉK 시 config.txt의 48MHz를 사용한다.
    postaláda_adat[0] = 36; postaláda_adat[1] = 0; postaláda_adat[2] = 0x38002; postaláda_adat[3] = 12;
    postaláda_adat[4] = 0; postaláda_adat[5] = 2; postaláda_adat[6] = 48000000; postaláda_adat[7] = 0; postaláda_adat[8] = 0;
    int Óra_kifogástalan = postaláda();
    uint32_t 속도 = Óra_kifogástalan && postaláda_adat[6] >= 1843200 ? postaláda_adat[6] : 48000000;
    postaláda_adat[0]=32; postaláda_adat[1]=0; postaláda_adat[2]=0x10005; postaláda_adat[3]=8; postaláda_adat[4]=0;
    postaláda_adat[5]=postaláda_adat[6]=postaláda_adat[7]=0;
    if (postaláda() && postaláda_adat[4]==0x80000008u) 팔기억킬로바이트=postaláda_adat[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    gép_jegyzék(직렬장치 + 0x44) = 0x7ff;
    gép_jegyzék(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    gép_jegyzék(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    gép_jegyzék(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    gép_jegyzék(직렬장치 + 0x38) = 0;
    gép_jegyzék(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
gép_szó fal_FTP(gép_szó Művelet) { return (uint32_t)ftp_control((int)Művelet); }
gép_szó fal_hálózat_állapot(gép_szó bejegyzés_ÉRTÉK, gép_szó INDEX) { return 망상태읽기(bejegyzés_ÉRTÉK, INDEX); }
gép_szó fal_hálózat_Gépház(gép_szó Művelet, gép_szó CÍM, gép_szó maszk_ÉRTÉK, gép_szó átjáró_ÉRTÉK) { return (uint32_t)망설정하기(Művelet, CÍM, maszk_ÉRTÉK, átjáró_ÉRTÉK); }
gép_szó fal_küld_válasz(gép_szó CÍM, gép_szó rendel_ÉRTÉK) { return (uint32_t)START_válasz_teszt(CÍM, rendel_ÉRTÉK); }
gép_szó 보드응답읽기(gép_szó bejegyzés_ÉRTÉK) { return (uint32_t)응답시험읽기(bejegyzés_ÉRTÉK); }
gép_szó 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEX=0; INDEX<32; INDEX++) bezár_hálózat(INDEX);
    for (unsigned INDEX=0; INDEX<4; INDEX++) fal_egyéni_vezérlőelem(32+INDEX);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (gép_jegyzék(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    gép_jegyzék(0xfe100020ul)=0x5a000000u | (gép_jegyzék(0xfe100020ul)&~0xfffu) | 0x555;
    gép_jegyzék(0xfe100024ul)=0x5a000000u | 10;
    gép_jegyzék(0xfe10001cul)=0x5a000000u | (gép_jegyzék(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

gép_szó 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 aktuális_cikk 크기를 읽는다. */
    const uint32_t lekérdez_ÉRTÉK[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(lekérdez_ÉRTÉK)/4; 순번++) postaláda_adat[순번] = lekérdez_ÉRTÉK[순번];
    if (postaláda() && postaláda_adat[4] == 0x80000008u &&
        postaláda_adat[5] >= 640 && postaláda_adat[5] <= 1920 &&
        postaláda_adat[6] >= 480 && postaláda_adat[6] <= 1080) {
        요청너비 = postaláda_adat[5]; 요청높이 = postaláda_adat[6];
    }
    const uint32_t kérés[] = {
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
    for (size_t 순번 = 0; 순번 < sizeof(kérés)/4; 순번++) postaláda_adat[순번] = kérés[순번];
    // 위 메시지의 tényleges_adat 길이를 használ_ÉRTÉK: 태그 hozzáfűz_bejegyzés 시 hossz_ÉRTÉK 불일치를 방지한다.
    postaláda_adat[0] = sizeof(kérés);
    if (!postaláda()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned válasz_hossz[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (postaláda_adat[응답들[순번]] != (0x80000000u | válasz_hossz[순번])) return 0;
    uint32_t Háttér_ÉRTÉK = postaláda_adat[28] & 0x3fffffffu;
    uint32_t Méret = postaláda_adat[29];
    uint32_t 받은너비 = postaláda_adat[5], 받은높이 = postaláda_adat[6], KAPOTT_sorköz = postaláda_adat[33];
    if (postaláda_adat[15] != 32 || postaláda_adat[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        postaláda_adat[10] < 받은너비 || postaláda_adat[11] < 받은높이 || postaláda_adat[23] || postaláda_adat[24] ||
        !Háttér_ÉRTÉK || Háttér_ÉRTÉK < 0x1000000 || (Háttér_ÉRTÉK & 3) || KAPOTT_sorköz < 받은너비 * 4 || (KAPOTT_sorköz & 3) ||
        (uint64_t)KAPOTT_sorköz * 받은높이 > Méret || (uint64_t)Háttér_ÉRTÉK + Méret > 0x40000000u)
        return 0;
    fal_Előkészítés_rajz((volatile uint32_t *)(uintptr_t)Háttér_ÉRTÉK, 받은너비, 받은높이, KAPOTT_sorköz);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 szál_ÉRTÉK. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } környezet;
static környezet 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int informatikai_részleg_Futás[3] = {1, 0, 0};
static int aktuális_teendő;
extern void kontextusváltás(környezet *, környezet *);
extern void 자바작업(int32_t);
gép_szó fal_HOZAM(void) {
    network_poll();
    int Előző_cikk = aktuális_teendő, Tovább_cikk = (Előző_cikk + 1) % 3;
    while (Tovább_cikk != Előző_cikk && !informatikai_részleg_Futás[Tovább_cikk]) Tovább_cikk = (Tovább_cikk + 1) % 3;
    if (Tovább_cikk != Előző_cikk) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (informatikai_részleg_Futás[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        aktuális_teendő = Tovább_cikk;
        kontextusváltás(&작업문맥들[Előző_cikk], &작업문맥들[Tovább_cikk]);
    }
    return 0;
}
static void teendő_rendszerindítás(void) {
    자바작업(aktuális_teendő);
    informatikai_részleg_Futás[aktuális_teendő] = 0;
    fal_HOZAM();
    커널중단("finished task resumed");
}
gép_szó fal_teendő_készít(gép_szó azonosító_ÉRTÉK) {
    if (azonosító_ÉRTÉK < 1 || azonosító_ÉRTÉK > 2 || informatikai_részleg_Futás[azonosító_ÉRTÉK]) return (uint32_t)-1;
    memset(&작업문맥들[azonosító_ÉRTÉK], 0, sizeof(környezet));
    *(uint64_t *)쌓임공간들[azonosító_ÉRTÉK - 1] = 0x6b6f726f7373746bull;
    작업문맥들[azonosító_ÉRTÉK].저장값[11] = (uintptr_t)teendő_rendszerindítás;
    작업문맥들[azonosító_ÉRTÉK].저장값[12] = (uintptr_t)(쌓임공간들[azonosító_ÉRTÉK - 1] + sizeof(쌓임공간들[0]));
    informatikai_részleg_Futás[azonosító_ÉRTÉK] = 1;
    return 0;
}
gép_szó fal_teendő_Állapot(gép_szó azonosító_ÉRTÉK) { return azonosító_ÉRTÉK < 3 ? informatikai_részleg_Futás[azonosító_ÉRTÉK] : (uint32_t)-1; }
extern gép_szó AOT_Memória_KERES(gép_szó);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
gép_szó fal_lekérdez_Rendszer(gép_szó bejegyzés_ÉRTÉK, gép_szó INDEX) {
    if (bejegyzés_ÉRTÉK==0) return 팔기억킬로바이트;
    if (bejegyzés_ÉRTÉK==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (bejegyzés_ÉRTÉK==2 || bejegyzés_ÉRTÉK==3) return AOT_Memória_KERES(bejegyzés_ÉRTÉK==3);
    if (bejegyzés_ÉRTÉK==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (bejegyzés_ÉRTÉK==5) return 80*1024; /* végrehajt_parancs CÍM_régió 16 MiB + 네 세션 보관 CÍM_régió. */
    if (bejegyzés_ÉRTÉK>=20) return 사용자상태읽기(bejegyzés_ÉRTÉK-20, INDEX);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[aktuális_teendő]; }
