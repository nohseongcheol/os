#include "../명명/기계연결이름.h"
#include "skjermbilde_info.h"
#include <stdint.h>
#include <stddef.h>
#include "bruker.h"
#include "../nettverk_stakk/nettverk_stakk.h"
typedef uintptr_t maskin_ord;
#define maskin_register(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define innboks_e_post 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Klokke_ANTALL(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t FREKVENS;
static volatile uint32_t innboks_data[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *data_plassere, int tegnkode, size_t vare_ANTALL) { unsigned char *Neste_FORSKYVNING = data_plassere; while (vare_ANTALL--) *Neste_FORSKYVNING++ = tegnkode; return data_plassere; }
void *memcpy(void *mål_data, const void *streng_data, size_t vare_ANTALL) { unsigned char *첫째값 = mål_data; const unsigned char *SEKUND_VERDI = streng_data; while (vare_ANTALL--) *첫째값++ = *SEKUND_VERDI++; return mål_data; }

static int innboks(void) {
    uint32_t forespørsel = (uint32_t)(uintptr_t)innboks_data | 8;
    uint64_t Kjør_2 = Klokke_ANTALL();
    기억장벽();
    while (maskin_register(innboks_e_post + 0x38) & 0x80000000u)
        if (Klokke_ANTALL() - Kjør_2 > FREKVENS) return 0;
    maskin_register(innboks_e_post + 0x20) = forespørsel;
    for (;;) {
        if (!(maskin_register(innboks_e_post + 0x18) & 0x40000000u)) {
            uint32_t svar = maskin_register(innboks_e_post);
            if (svar == forespørsel) { 기억장벽(); return innboks_data[1] == 0x80000000u; }
        }
        if (Klokke_ANTALL() - Kjør_2 > FREKVENS) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terminal_byte(unsigned);
extern int Terminal_Venter(void);
extern void Terminal_peker(unsigned,int,int),터미널바로가기키(unsigned);
extern void Terminal_inndata_MODUS(unsigned);
#include "../ekstern_VERDI_28edcfa1/ekstern_VERDI_28edcfa1.h"
static int Strømmer;
static unsigned 직렬이전글자;
maskin_ord Tavle_Strømmer(maskin_ord 사용여부) { Strømmer=사용여부!=0; return 0; }
maskin_ord Tavle_Kanal(maskin_ord Kanal, maskin_ord tegnkode) {
    if(Strømmer && 자바셸출력((int32_t)Kanal,(int32_t)(tegnkode&255))) return 0;
    Terminal_byte(tegnkode&255);
    ekstern_produksjon(tegnkode&255);
    if ((tegnkode&255)==10 && 직렬이전글자!=13) {
        while (maskin_register(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        maskin_register(직렬장치)=13;
    }
    직렬이전글자=tegnkode&255;
    while (maskin_register(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    maskin_register(직렬장치) = (uint32_t)tegnkode & 255;
    return 0;
}
maskin_ord 보드글자쓰기(maskin_ord tegnkode) { return Tavle_Kanal(1,tegnkode); }
maskin_ord 보드원시글자읽기(void) {
    int ekstern_tegn=ekstern_inndata();if(ekstern_tegn>=0)return ekstern_tegn;
    if (maskin_register(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t VERDI = maskin_register(직렬장치);
    if (VERDI & 0xf00) { maskin_register(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return VERDI & 255;
}
maskin_ord 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char pakke_data[6];
    if(Terminal_Venter())return (uint32_t)-4096;
    if(Strømmer){int32_t tegnkode=자바셸입력();if(tegnkode!=-3)return (uint32_t)tegnkode;}
    for(;;){
        int tegnkode=(int32_t)보드원시글자읽기();if(tegnkode<0)return (uint32_t)tegnkode;
        if(!꾸러미안쪽){if(tegnkode!=30)return tegnkode;꾸러미안쪽=1;사용량=0;continue;}
        pakke_data[사용량++]=tegnkode;if(사용량<6)continue;꾸러미안쪽=0;
        if(pakke_data[0]==1)Terminal_peker(pakke_data[1],pakke_data[2]+pakke_data[3]*256,pakke_data[4]+pakke_data[5]*256);
        if(pakke_data[0]==2)터미널바로가기키(pakke_data[1]);
        if(pakke_data[0]==3)Terminal_inndata_MODUS(pakke_data[1]);
        if(Terminal_Venter())return (uint32_t)-4096;
    }
}
maskin_ord 보드밀리초(void) { return (uint32_t)(Klokke_ANTALL() / (FREKVENS / 1000)); }
maskin_ord 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *streng_data) { while (*streng_data) 보드글자쓰기((unsigned char)*streng_data++); }
static void 직렬열여섯진출력(maskin_ord vare_ANTALL) { const char *열여섯진숫자 = "0123456789abcdef"; for (int streng_data = 60; streng_data >= 0; streng_data -= 4) 보드글자쓰기(열여섯진숫자[(vare_ANTALL >> streng_data) & 15]); }
maskin_ord Tavle_Stopp(maskin_ord status_VERDI) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(status_VERDI); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); Tavle_Stopp(1); __builtin_unreachable(); }
void Tavle_unntak(maskin_ord unntak_status, maskin_ord kommando_plassere, maskin_ord ugyldig_e_post) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(unntak_status);
    직렬글출력(" PC="); 직렬열여섯진출력(kommando_plassere); 직렬글출력(" FAR="); 직렬열여섯진출력(ugyldig_e_post);
    Tavle_Stopp(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    innboks_data[0]=32;innboks_data[1]=0;innboks_data[2]=0x10004;innboks_data[3]=8;innboks_data[4]=0;
    innboks_data[5]=innboks_data[6]=innboks_data[7]=0;
    return innboks()&&innboks_data[4]==0x80000008u&&(innboks_data[5]||innboks_data[6]);
}
int Tavle_absolutt_adresse(unsigned char *e_post) {
    innboks_data[0]=32;innboks_data[1]=0;innboks_data[2]=0x10003;innboks_data[3]=8;innboks_data[4]=0;
    innboks_data[5]=innboks_data[6]=innboks_data[7]=0;
    if(!innboks()||(innboks_data[4]&0x80000000u)==0||(innboks_data[4]&0xffff)!=6)return 0;
    const unsigned char *data=(const unsigned char*)&innboks_data[5];unsigned SUMMER_VERDI=0;
    for(unsigned 순번=0;순번<6;순번++){e_post[순번]=data[순번];SUMMER_VERDI|=data[순번];}return SUMMER_VERDI&&!(e_post[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREKVENS));
    maskin_register(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    maskin_register(범용입출력 + 4) = (maskin_register(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    maskin_register(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. feil_VERDI 시 config.txt의 48MHz를 사용한다.
    innboks_data[0] = 36; innboks_data[1] = 0; innboks_data[2] = 0x38002; innboks_data[3] = 12;
    innboks_data[4] = 0; innboks_data[5] = 2; innboks_data[6] = 48000000; innboks_data[7] = 0; innboks_data[8] = 0;
    int 시계정상 = innboks();
    uint32_t 속도 = 시계정상 && innboks_data[6] >= 1843200 ? innboks_data[6] : 48000000;
    innboks_data[0]=32; innboks_data[1]=0; innboks_data[2]=0x10005; innboks_data[3]=8; innboks_data[4]=0;
    innboks_data[5]=innboks_data[6]=innboks_data[7]=0;
    if (innboks() && innboks_data[4]==0x80000008u) 팔기억킬로바이트=innboks_data[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    maskin_register(직렬장치 + 0x44) = 0x7ff;
    maskin_register(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    maskin_register(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    maskin_register(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    maskin_register(직렬장치 + 0x38) = 0;
    maskin_register(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
maskin_ord Tavle_FTP(maskin_ord Handling) { return (uint32_t)ftp_control((int)Handling); }
maskin_ord Tavle_nettverk_status(maskin_ord oppføring_VERDI, maskin_ord INDEKS) { return 망상태읽기(oppføring_VERDI, INDEKS); }
maskin_ord Tavle_nettverk_Innstillinger(maskin_ord Handling, maskin_ord e_post, maskin_ord maske_VERDI, maskin_ord gateway_VERDI) { return (uint32_t)konfigurere_nettverk(Handling, e_post, maske_VERDI, gateway_VERDI); }
maskin_ord Tavle_sende_svar(maskin_ord e_post, maskin_ord ordre_VERDI) { return (uint32_t)START_svar_test(e_post, ordre_VERDI); }
maskin_ord 보드응답읽기(maskin_ord oppføring_VERDI) { return (uint32_t)응답시험읽기(oppføring_VERDI); }
maskin_ord 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEKS=0; INDEKS<32; INDEKS++) Lukk_nettverk(INDEKS);
    for (unsigned INDEKS=0; INDEKS<4; INDEKS++) Tavle_brukerkontroll(32+INDEKS);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (maskin_register(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    maskin_register(0xfe100020ul)=0x5a000000u | (maskin_register(0xfe100020ul)&~0xfffu) | 0x555;
    maskin_register(0xfe100024ul)=0x5a000000u | 10;
    maskin_register(0xfe10001cul)=0x5a000000u | (maskin_register(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

maskin_ord 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 betalt_vare 크기를 읽는다. */
    const uint32_t spørre_VERDI[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(spørre_VERDI)/4; 순번++) innboks_data[순번] = spørre_VERDI[순번];
    if (innboks() && innboks_data[4] == 0x80000008u &&
        innboks_data[5] >= 640 && innboks_data[5] <= 1920 &&
        innboks_data[6] >= 480 && innboks_data[6] <= 1080) {
        요청너비 = innboks_data[5]; 요청높이 = innboks_data[6];
    }
    const uint32_t forespørsel[] = {
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
    for (size_t 순번 = 0; 순번 < sizeof(forespørsel)/4; 순번++) innboks_data[순번] = forespørsel[순번];
    // 위 메시지의 faktisk_data 길이를 bruk_VERDI: 태그 Tilføye_oppføring 시 lengde_VERDI 불일치를 방지한다.
    innboks_data[0] = sizeof(forespørsel);
    if (!innboks()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned svar_lengde[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (innboks_data[응답들[순번]] != (0x80000000u | svar_lengde[순번])) return 0;
    uint32_t bakgrunn_VERDI = innboks_data[28] & 0x3fffffffu;
    uint32_t Størrelse = innboks_data[29];
    uint32_t 받은너비 = innboks_data[5], 받은높이 = innboks_data[6], MOTTATT_AVKAST_linjeavstand = innboks_data[33];
    if (innboks_data[15] != 32 || innboks_data[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        innboks_data[10] < 받은너비 || innboks_data[11] < 받은높이 || innboks_data[23] || innboks_data[24] ||
        !bakgrunn_VERDI || bakgrunn_VERDI < 0x1000000 || (bakgrunn_VERDI & 3) || MOTTATT_AVKAST_linjeavstand < 받은너비 * 4 || (MOTTATT_AVKAST_linjeavstand & 3) ||
        (uint64_t)MOTTATT_AVKAST_linjeavstand * 받은높이 > Størrelse || (uint64_t)bakgrunn_VERDI + Størrelse > 0x40000000u)
        return 0;
    Tavle_Forbered_tegning((volatile uint32_t *)(uintptr_t)bakgrunn_VERDI, 받은너비, 받은높이, MOTTATT_AVKAST_linjeavstand);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 tråd_VERDI. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } kontekst;
static kontekst 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int informasjonssystemer_Løper[3] = {1, 0, 0};
static int betalt_oppgave;
extern void kontekst_bytt(kontekst *, kontekst *);
extern void 자바작업(int32_t);
maskin_ord Tavle_AVKAST(void) {
    network_poll();
    int Forrige_vare = betalt_oppgave, Neste_vare = (Forrige_vare + 1) % 3;
    while (Neste_vare != Forrige_vare && !informasjonssystemer_Løper[Neste_vare]) Neste_vare = (Neste_vare + 1) % 3;
    if (Neste_vare != Forrige_vare) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (informasjonssystemer_Løper[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        betalt_oppgave = Neste_vare;
        kontekst_bytt(&작업문맥들[Forrige_vare], &작업문맥들[Neste_vare]);
    }
    return 0;
}
static void oppgave_oppstart(void) {
    자바작업(betalt_oppgave);
    informasjonssystemer_Løper[betalt_oppgave] = 0;
    Tavle_AVKAST();
    커널중단("finished task resumed");
}
maskin_ord Tavle_oppgave_åpne(maskin_ord identifikator_VERDI) {
    if (identifikator_VERDI < 1 || identifikator_VERDI > 2 || informasjonssystemer_Løper[identifikator_VERDI]) return (uint32_t)-1;
    memset(&작업문맥들[identifikator_VERDI], 0, sizeof(kontekst));
    *(uint64_t *)쌓임공간들[identifikator_VERDI - 1] = 0x6b6f726f7373746bull;
    작업문맥들[identifikator_VERDI].저장값[11] = (uintptr_t)oppgave_oppstart;
    작업문맥들[identifikator_VERDI].저장값[12] = (uintptr_t)(쌓임공간들[identifikator_VERDI - 1] + sizeof(쌓임공간들[0]));
    informasjonssystemer_Løper[identifikator_VERDI] = 1;
    return 0;
}
maskin_ord Tavle_oppgave_status(maskin_ord identifikator_VERDI) { return identifikator_VERDI < 3 ? informasjonssystemer_Løper[identifikator_VERDI] : (uint32_t)-1; }
extern maskin_ord applikasjonsobjekttre_Minne_Oppslag(maskin_ord);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
maskin_ord Tavle_spørre_System(maskin_ord oppføring_VERDI, maskin_ord INDEKS) {
    if (oppføring_VERDI==0) return 팔기억킬로바이트;
    if (oppføring_VERDI==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (oppføring_VERDI==2 || oppføring_VERDI==3) return applikasjonsobjekttre_Minne_Oppslag(oppføring_VERDI==3);
    if (oppføring_VERDI==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (oppføring_VERDI==5) return 80*1024; /* Utfør_kommando e_post_område 16 MiB + 네 세션 보관 e_post_område. */
    if (oppføring_VERDI>=20) return 사용자상태읽기(oppføring_VERDI-20, INDEKS);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[betalt_oppgave]; }
