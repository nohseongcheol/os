#include "../명명/기계연결이름.h"
#include "skærmbillede_info.h"
#include <stdint.h>
#include <stddef.h>
#include "bruger.h"
#include "../netværk_Stak/netværk_Stak.h"
typedef uintptr_t maskine_Ord;
#define maskine_register(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define postkasse_mail 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Ur_TÆL(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t FREKVENS;
static volatile uint32_t postkasse_data[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *data_placere, int tegnkode, size_t vare_TÆL) { unsigned char *Næste_FORSKYDNING = data_placere; while (vare_TÆL--) *Næste_FORSKYDNING++ = tegnkode; return data_placere; }
void *memcpy(void *destination_data, const void *streng_data, size_t vare_TÆL) { unsigned char *첫째값 = destination_data; const unsigned char *SEKUND_VÆRDI = streng_data; while (vare_TÆL--) *첫째값++ = *SEKUND_VÆRDI++; return destination_data; }

static int postkasse(void) {
    uint32_t anmodning = (uint32_t)(uintptr_t)postkasse_data | 8;
    uint64_t Kør_2 = Ur_TÆL();
    기억장벽();
    while (maskine_register(postkasse_mail + 0x38) & 0x80000000u)
        if (Ur_TÆL() - Kør_2 > FREKVENS) return 0;
    maskine_register(postkasse_mail + 0x20) = anmodning;
    for (;;) {
        if (!(maskine_register(postkasse_mail + 0x18) & 0x40000000u)) {
            uint32_t svar = maskine_register(postkasse_mail);
            if (svar == anmodning) { 기억장벽(); return postkasse_data[1] == 0x80000000u; }
        }
        if (Ur_TÆL() - Kør_2 > FREKVENS) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terminal_byte(unsigned);
extern int Terminal_Afventer(void);
extern void Terminal_markør(unsigned,int,int),터미널바로가기키(unsigned);
extern void Terminal_input_HYPPIGST(unsigned);
#include "../fjern_VÆRDI/fjern_VÆRDI.h"
static int Strømme;
static unsigned 직렬이전글자;
maskine_Ord Tavle_Strømme(maskine_Ord 사용여부) { Strømme=사용여부!=0; return 0; }
maskine_Ord Tavle_Kanal(maskine_Ord Kanal, maskine_Ord tegnkode) {
    if(Strømme && 자바셸출력((int32_t)Kanal,(int32_t)(tegnkode&255))) return 0;
    Terminal_byte(tegnkode&255);
    fjern_produktoutput(tegnkode&255);
    if ((tegnkode&255)==10 && 직렬이전글자!=13) {
        while (maskine_register(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        maskine_register(직렬장치)=13;
    }
    직렬이전글자=tegnkode&255;
    while (maskine_register(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    maskine_register(직렬장치) = (uint32_t)tegnkode & 255;
    return 0;
}
maskine_Ord 보드글자쓰기(maskine_Ord tegnkode) { return Tavle_Kanal(1,tegnkode); }
maskine_Ord 보드원시글자읽기(void) {
    int fjern_tegn=fjern_input();if(fjern_tegn>=0)return fjern_tegn;
    if (maskine_register(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t VÆRDI = maskine_register(직렬장치);
    if (VÆRDI & 0xf00) { maskine_register(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return VÆRDI & 255;
}
maskine_Ord 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char pakke_data[6];
    if(Terminal_Afventer())return (uint32_t)-4096;
    if(Strømme){int32_t tegnkode=자바셸입력();if(tegnkode!=-3)return (uint32_t)tegnkode;}
    for(;;){
        int tegnkode=(int32_t)보드원시글자읽기();if(tegnkode<0)return (uint32_t)tegnkode;
        if(!꾸러미안쪽){if(tegnkode!=30)return tegnkode;꾸러미안쪽=1;사용량=0;continue;}
        pakke_data[사용량++]=tegnkode;if(사용량<6)continue;꾸러미안쪽=0;
        if(pakke_data[0]==1)Terminal_markør(pakke_data[1],pakke_data[2]+pakke_data[3]*256,pakke_data[4]+pakke_data[5]*256);
        if(pakke_data[0]==2)터미널바로가기키(pakke_data[1]);
        if(pakke_data[0]==3)Terminal_input_HYPPIGST(pakke_data[1]);
        if(Terminal_Afventer())return (uint32_t)-4096;
    }
}
maskine_Ord 보드밀리초(void) { return (uint32_t)(Ur_TÆL() / (FREKVENS / 1000)); }
maskine_Ord 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *streng_data) { while (*streng_data) 보드글자쓰기((unsigned char)*streng_data++); }
static void 직렬열여섯진출력(maskine_Ord vare_TÆL) { const char *열여섯진숫자 = "0123456789abcdef"; for (int streng_data = 60; streng_data >= 0; streng_data -= 4) 보드글자쓰기(열여섯진숫자[(vare_TÆL >> streng_data) & 15]); }
maskine_Ord Tavle_Stop(maskine_Ord status_VÆRDI) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(status_VÆRDI); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); Tavle_Stop(1); __builtin_unreachable(); }
void Tavle_undtagelse(maskine_Ord undtagelse_status, maskine_Ord kommando_placere, maskine_Ord ugyldig_mail) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(undtagelse_status);
    직렬글출력(" PC="); 직렬열여섯진출력(kommando_placere); 직렬글출력(" FAR="); 직렬열여섯진출력(ugyldig_mail);
    Tavle_Stop(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    postkasse_data[0]=32;postkasse_data[1]=0;postkasse_data[2]=0x10004;postkasse_data[3]=8;postkasse_data[4]=0;
    postkasse_data[5]=postkasse_data[6]=postkasse_data[7]=0;
    return postkasse()&&postkasse_data[4]==0x80000008u&&(postkasse_data[5]||postkasse_data[6]);
}
int Tavle_absolut_adresse(unsigned char *mail) {
    postkasse_data[0]=32;postkasse_data[1]=0;postkasse_data[2]=0x10003;postkasse_data[3]=8;postkasse_data[4]=0;
    postkasse_data[5]=postkasse_data[6]=postkasse_data[7]=0;
    if(!postkasse()||(postkasse_data[4]&0x80000000u)==0||(postkasse_data[4]&0xffff)!=6)return 0;
    const unsigned char *data=(const unsigned char*)&postkasse_data[5];unsigned SUM_VÆRDI=0;
    for(unsigned 순번=0;순번<6;순번++){mail[순번]=data[순번];SUM_VÆRDI|=data[순번];}return SUM_VÆRDI&&!(mail[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREKVENS));
    maskine_register(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    maskine_register(범용입출력 + 4) = (maskine_register(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    maskine_register(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. fejl_VÆRDI 시 config.txt의 48MHz를 사용한다.
    postkasse_data[0] = 36; postkasse_data[1] = 0; postkasse_data[2] = 0x38002; postkasse_data[3] = 12;
    postkasse_data[4] = 0; postkasse_data[5] = 2; postkasse_data[6] = 48000000; postkasse_data[7] = 0; postkasse_data[8] = 0;
    int 시계정상 = postkasse();
    uint32_t 속도 = 시계정상 && postkasse_data[6] >= 1843200 ? postkasse_data[6] : 48000000;
    postkasse_data[0]=32; postkasse_data[1]=0; postkasse_data[2]=0x10005; postkasse_data[3]=8; postkasse_data[4]=0;
    postkasse_data[5]=postkasse_data[6]=postkasse_data[7]=0;
    if (postkasse() && postkasse_data[4]==0x80000008u) 팔기억킬로바이트=postkasse_data[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    maskine_register(직렬장치 + 0x44) = 0x7ff;
    maskine_register(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    maskine_register(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    maskine_register(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    maskine_register(직렬장치 + 0x38) = 0;
    maskine_register(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
maskine_Ord Tavle_FTP(maskine_Ord Handling) { return (uint32_t)ftp_control((int)Handling); }
maskine_Ord Tavle_netværk_status(maskine_Ord post_VÆRDI_962f286b, maskine_Ord INDEKS) { return 망상태읽기(post_VÆRDI_962f286b, INDEKS); }
maskine_Ord Tavle_netværk_Indstillinger(maskine_Ord Handling, maskine_Ord mail, maskine_Ord maske_VÆRDI, maskine_Ord gateway_VÆRDI) { return (uint32_t)konfigurere_netværk(Handling, mail, maske_VÆRDI, gateway_VÆRDI); }
maskine_Ord Tavle_maile_svar(maskine_Ord mail, maskine_Ord ordre_VÆRDI) { return (uint32_t)START_svar_test(mail, ordre_VÆRDI); }
maskine_Ord 보드응답읽기(maskine_Ord post_VÆRDI_962f286b) { return (uint32_t)응답시험읽기(post_VÆRDI_962f286b); }
maskine_Ord 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEKS=0; INDEKS<32; INDEKS++) Luk_netværk(INDEKS);
    for (unsigned INDEKS=0; INDEKS<4; INDEKS++) Tavle_brugerkontrolelement(32+INDEKS);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (maskine_register(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    maskine_register(0xfe100020ul)=0x5a000000u | (maskine_register(0xfe100020ul)&~0xfffu) | 0x555;
    maskine_register(0xfe100024ul)=0x5a000000u | 10;
    maskine_register(0xfe10001cul)=0x5a000000u | (maskine_register(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

maskine_Ord 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 aktuel_vare 크기를 읽는다. */
    const uint32_t forespørge_VÆRDI[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(forespørge_VÆRDI)/4; 순번++) postkasse_data[순번] = forespørge_VÆRDI[순번];
    if (postkasse() && postkasse_data[4] == 0x80000008u &&
        postkasse_data[5] >= 640 && postkasse_data[5] <= 1920 &&
        postkasse_data[6] >= 480 && postkasse_data[6] <= 1080) {
        요청너비 = postkasse_data[5]; 요청높이 = postkasse_data[6];
    }
    const uint32_t anmodning[] = {
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
    for (size_t 순번 = 0; 순번 < sizeof(anmodning)/4; 순번++) postkasse_data[순번] = anmodning[순번];
    // 위 메시지의 faktisk_data 길이를 brug_VÆRDI: 태그 tilføj_post 시 varighed_VÆRDI 불일치를 방지한다.
    postkasse_data[0] = sizeof(anmodning);
    if (!postkasse()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned svar_varighed[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (postkasse_data[응답들[순번]] != (0x80000000u | svar_varighed[순번])) return 0;
    uint32_t Baggrund_VÆRDI = postkasse_data[28] & 0x3fffffffu;
    uint32_t Størrelse = postkasse_data[29];
    uint32_t 받은너비 = postkasse_data[5], 받은높이 = postkasse_data[6], MODTAGET_VED_UDLØB_skydning = postkasse_data[33];
    if (postkasse_data[15] != 32 || postkasse_data[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        postkasse_data[10] < 받은너비 || postkasse_data[11] < 받은높이 || postkasse_data[23] || postkasse_data[24] ||
        !Baggrund_VÆRDI || Baggrund_VÆRDI < 0x1000000 || (Baggrund_VÆRDI & 3) || MODTAGET_VED_UDLØB_skydning < 받은너비 * 4 || (MODTAGET_VED_UDLØB_skydning & 3) ||
        (uint64_t)MODTAGET_VED_UDLØB_skydning * 받은높이 > Størrelse || (uint64_t)Baggrund_VÆRDI + Størrelse > 0x40000000u)
        return 0;
    Tavle_Tilrettelæg_tegning((volatile uint32_t *)(uintptr_t)Baggrund_VÆRDI, 받은너비, 받은높이, MODTAGET_VED_UDLØB_skydning);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 tråd_VÆRDI. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } kontekst;
static kontekst 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int it_Løb[3] = {1, 0, 0};
static int aktuel_job;
extern void kontekstskift(kontekst *, kontekst *);
extern void 자바작업(int32_t);
maskine_Ord Tavle_AFKAST(void) {
    network_poll();
    int Forrige_vare = aktuel_job, Næste_vare = (Forrige_vare + 1) % 3;
    while (Næste_vare != Forrige_vare && !it_Løb[Næste_vare]) Næste_vare = (Næste_vare + 1) % 3;
    if (Næste_vare != Forrige_vare) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (it_Løb[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        aktuel_job = Næste_vare;
        kontekstskift(&작업문맥들[Forrige_vare], &작업문맥들[Næste_vare]);
    }
    return 0;
}
static void job_IPL(void) {
    자바작업(aktuel_job);
    it_Løb[aktuel_job] = 0;
    Tavle_AFKAST();
    커널중단("finished task resumed");
}
maskine_Ord Tavle_job_åbne(maskine_Ord identifikator_VÆRDI) {
    if (identifikator_VÆRDI < 1 || identifikator_VÆRDI > 2 || it_Løb[identifikator_VÆRDI]) return (uint32_t)-1;
    memset(&작업문맥들[identifikator_VÆRDI], 0, sizeof(kontekst));
    *(uint64_t *)쌓임공간들[identifikator_VÆRDI - 1] = 0x6b6f726f7373746bull;
    작업문맥들[identifikator_VÆRDI].저장값[11] = (uintptr_t)job_IPL;
    작업문맥들[identifikator_VÆRDI].저장값[12] = (uintptr_t)(쌓임공간들[identifikator_VÆRDI - 1] + sizeof(쌓임공간들[0]));
    it_Løb[identifikator_VÆRDI] = 1;
    return 0;
}
maskine_Ord Tavle_job_status(maskine_Ord identifikator_VÆRDI) { return identifikator_VÆRDI < 3 ? it_Løb[identifikator_VÆRDI] : (uint32_t)-1; }
extern maskine_Ord AOT_Hukommelse_Opslag(maskine_Ord);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
maskine_Ord Tavle_forespørge_System(maskine_Ord post_VÆRDI_962f286b, maskine_Ord INDEKS) {
    if (post_VÆRDI_962f286b==0) return 팔기억킬로바이트;
    if (post_VÆRDI_962f286b==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (post_VÆRDI_962f286b==2 || post_VÆRDI_962f286b==3) return AOT_Hukommelse_Opslag(post_VÆRDI_962f286b==3);
    if (post_VÆRDI_962f286b==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (post_VÆRDI_962f286b==5) return 80*1024; /* Udfør_kommando mail_område 16 MiB + 네 세션 보관 mail_område. */
    if (post_VÆRDI_962f286b>=20) return 사용자상태읽기(post_VÆRDI_962f286b-20, INDEKS);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[aktuel_job]; }
