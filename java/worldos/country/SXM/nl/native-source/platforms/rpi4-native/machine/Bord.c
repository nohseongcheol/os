#include "../명명/기계연결이름.h"
#include "scherm_info.h"
#include <stdint.h>
#include <stddef.h>
#include "gebruikersruimte.h"
#include "../net_stack/net_stack.h"
typedef uintptr_t machine_Word;
#define machine_register(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define postvak_ADRES 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Klok_AANTAL(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t INTERVAL;
static volatile uint32_t postvak_gegevens[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *gegevens_functie, int codepoint, size_t item_AANTAL) { unsigned char *Volgende_VERSCHUIVING = gegevens_functie; while (item_AANTAL--) *Volgende_VERSCHUIVING++ = codepoint; return gegevens_functie; }
void *memcpy(void *doel_gegevens, const void *tekenreeks_gegevens, size_t item_AANTAL) { unsigned char *첫째값 = doel_gegevens; const unsigned char *SECONDE_WAARDE = tekenreeks_gegevens; while (item_AANTAL--) *첫째값++ = *SECONDE_WAARDE++; return doel_gegevens; }

static int postvak(void) {
    uint32_t aanvraag = (uint32_t)(uintptr_t)postvak_gegevens | 8;
    uint64_t starten = Klok_AANTAL();
    기억장벽();
    while (machine_register(postvak_ADRES + 0x38) & 0x80000000u)
        if (Klok_AANTAL() - starten > INTERVAL) return 0;
    machine_register(postvak_ADRES + 0x20) = aanvraag;
    for (;;) {
        if (!(machine_register(postvak_ADRES + 0x18) & 0x40000000u)) {
            uint32_t reactie = machine_register(postvak_ADRES);
            if (reactie == aanvraag) { 기억장벽(); return postvak_gegevens[1] == 0x80000000u; }
        }
        if (Klok_AANTAL() - starten > INTERVAL) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terminal_byte(unsigned);
extern int Terminal_In_behandeling(void);
extern void Terminal_wijzer(unsigned,int,int),터미널바로가기키(unsigned);
extern void Terminal_invoer_MODUS(unsigned);
#include "../extern_WAARDE_28edcfa1/extern_WAARDE_28edcfa1.h"
static int Streams;
static unsigned 직렬이전글자;
machine_Word Bord_Streams(machine_Word 사용여부) { Streams=사용여부!=0; return 0; }
machine_Word Bord_Kanaal(machine_Word Kanaal, machine_Word codepoint) {
    if(Streams && 자바셸출력((int32_t)Kanaal,(int32_t)(codepoint&255))) return 0;
    Terminal_byte(codepoint&255);
    extern_uitvoer(codepoint&255);
    if ((codepoint&255)==10 && 직렬이전글자!=13) {
        while (machine_register(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        machine_register(직렬장치)=13;
    }
    직렬이전글자=codepoint&255;
    while (machine_register(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    machine_register(직렬장치) = (uint32_t)codepoint & 255;
    return 0;
}
machine_Word 보드글자쓰기(machine_Word codepoint) { return Bord_Kanaal(1,codepoint); }
machine_Word 보드원시글자읽기(void) {
    int extern_teken=extern_invoer();if(extern_teken>=0)return extern_teken;
    if (machine_register(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t WAARDE = machine_register(직렬장치);
    if (WAARDE & 0xf00) { machine_register(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return WAARDE & 255;
}
machine_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char pakket_gegevens[6];
    if(Terminal_In_behandeling())return (uint32_t)-4096;
    if(Streams){int32_t codepoint=자바셸입력();if(codepoint!=-3)return (uint32_t)codepoint;}
    for(;;){
        int codepoint=(int32_t)보드원시글자읽기();if(codepoint<0)return (uint32_t)codepoint;
        if(!꾸러미안쪽){if(codepoint!=30)return codepoint;꾸러미안쪽=1;사용량=0;continue;}
        pakket_gegevens[사용량++]=codepoint;if(사용량<6)continue;꾸러미안쪽=0;
        if(pakket_gegevens[0]==1)Terminal_wijzer(pakket_gegevens[1],pakket_gegevens[2]+pakket_gegevens[3]*256,pakket_gegevens[4]+pakket_gegevens[5]*256);
        if(pakket_gegevens[0]==2)터미널바로가기키(pakket_gegevens[1]);
        if(pakket_gegevens[0]==3)Terminal_invoer_MODUS(pakket_gegevens[1]);
        if(Terminal_In_behandeling())return (uint32_t)-4096;
    }
}
machine_Word 보드밀리초(void) { return (uint32_t)(Klok_AANTAL() / (INTERVAL / 1000)); }
machine_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *tekenreeks_gegevens) { while (*tekenreeks_gegevens) 보드글자쓰기((unsigned char)*tekenreeks_gegevens++); }
static void 직렬열여섯진출력(machine_Word item_AANTAL) { const char *열여섯진숫자 = "0123456789abcdef"; for (int tekenreeks_gegevens = 60; tekenreeks_gegevens >= 0; tekenreeks_gegevens -= 4) 보드글자쓰기(열여섯진숫자[(item_AANTAL >> tekenreeks_gegevens) & 15]); }
machine_Word Bord_Stop(machine_Word Status_WAARDE) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(Status_WAARDE); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); Bord_Stop(1); __builtin_unreachable(); }
void Bord_uitzondering(machine_Word uitzondering_Status, machine_Word opdracht_functie, machine_Word nietig_ADRES) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(uitzondering_Status);
    직렬글출력(" PC="); 직렬열여섯진출력(opdracht_functie); 직렬글출력(" FAR="); 직렬열여섯진출력(nietig_ADRES);
    Bord_Stop(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    postvak_gegevens[0]=32;postvak_gegevens[1]=0;postvak_gegevens[2]=0x10004;postvak_gegevens[3]=8;postvak_gegevens[4]=0;
    postvak_gegevens[5]=postvak_gegevens[6]=postvak_gegevens[7]=0;
    return postvak()&&postvak_gegevens[4]==0x80000008u&&(postvak_gegevens[5]||postvak_gegevens[6]);
}
int Bord_absoluut_adres(unsigned char *ADRES) {
    postvak_gegevens[0]=32;postvak_gegevens[1]=0;postvak_gegevens[2]=0x10003;postvak_gegevens[3]=8;postvak_gegevens[4]=0;
    postvak_gegevens[5]=postvak_gegevens[6]=postvak_gegevens[7]=0;
    if(!postvak()||(postvak_gegevens[4]&0x80000000u)==0||(postvak_gegevens[4]&0xffff)!=6)return 0;
    const unsigned char *gegevens=(const unsigned char*)&postvak_gegevens[5];unsigned SOM_WAARDE=0;
    for(unsigned 순번=0;순번<6;순번++){ADRES[순번]=gegevens[순번];SOM_WAARDE|=gegevens[순번];}return SOM_WAARDE&&!(ADRES[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(INTERVAL));
    machine_register(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    machine_register(범용입출력 + 4) = (machine_register(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    machine_register(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. fout_WAARDE 시 config.txt의 48MHz를 사용한다.
    postvak_gegevens[0] = 36; postvak_gegevens[1] = 0; postvak_gegevens[2] = 0x38002; postvak_gegevens[3] = 12;
    postvak_gegevens[4] = 0; postvak_gegevens[5] = 2; postvak_gegevens[6] = 48000000; postvak_gegevens[7] = 0; postvak_gegevens[8] = 0;
    int Klok_in_orde = postvak();
    uint32_t 속도 = Klok_in_orde && postvak_gegevens[6] >= 1843200 ? postvak_gegevens[6] : 48000000;
    postvak_gegevens[0]=32; postvak_gegevens[1]=0; postvak_gegevens[2]=0x10005; postvak_gegevens[3]=8; postvak_gegevens[4]=0;
    postvak_gegevens[5]=postvak_gegevens[6]=postvak_gegevens[7]=0;
    if (postvak() && postvak_gegevens[4]==0x80000008u) 팔기억킬로바이트=postvak_gegevens[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    machine_register(직렬장치 + 0x44) = 0x7ff;
    machine_register(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    machine_register(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    machine_register(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    machine_register(직렬장치 + 0x38) = 0;
    machine_register(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
machine_Word Bord_FTP(machine_Word Actie) { return (uint32_t)ftp_control((int)Actie); }
machine_Word Bord_net_status(machine_Word invoer_WAARDE_962f286b, machine_Word INDEX) { return 망상태읽기(invoer_WAARDE_962f286b, INDEX); }
machine_Word Bord_net_Instellingen(machine_Word Actie, machine_Word ADRES, machine_Word masker_WAARDE, machine_Word gateway_WAARDE) { return (uint32_t)configureren_net(Actie, ADRES, masker_WAARDE, gateway_WAARDE); }
machine_Word Bord_e_mailen_reactie(machine_Word ADRES, machine_Word order_WAARDE) { return (uint32_t)START_reactie_test(ADRES, order_WAARDE); }
machine_Word 보드응답읽기(machine_Word invoer_WAARDE_962f286b) { return (uint32_t)응답시험읽기(invoer_WAARDE_962f286b); }
machine_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEX=0; INDEX<32; INDEX++) Sluiten_net(INDEX);
    for (unsigned INDEX=0; INDEX<4; INDEX++) Bord_gebruikersbesturingselement(32+INDEX);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (machine_register(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    machine_register(0xfe100020ul)=0x5a000000u | (machine_register(0xfe100020ul)&~0xfffu) | 0x555;
    machine_register(0xfe100024ul)=0x5a000000u | 10;
    machine_register(0xfe10001cul)=0x5a000000u | (machine_register(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

machine_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 actueel_item 크기를 읽는다. */
    const uint32_t query_WAARDE[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, aangevraagd_hoogte = 480;
    for (size_t 순번 = 0; 순번 < sizeof(query_WAARDE)/4; 순번++) postvak_gegevens[순번] = query_WAARDE[순번];
    if (postvak() && postvak_gegevens[4] == 0x80000008u &&
        postvak_gegevens[5] >= 640 && postvak_gegevens[5] <= 1920 &&
        postvak_gegevens[6] >= 480 && postvak_gegevens[6] <= 1080) {
        요청너비 = postvak_gegevens[5]; aangevraagd_hoogte = postvak_gegevens[6];
    }
    const uint32_t aanvraag[] = {
        35 * 4, 0,
        0x48003, 8, 0, 요청너비, aangevraagd_hoogte,
        0x48004, 8, 0, 요청너비, aangevraagd_hoogte,
        0x48005, 4, 0, 32,
        0x48006, 4, 0, 1,
        0x48009, 8, 0, 0, 0,
        0x40001, 8, 0, 4096, 0,
        0x40008, 4, 0, 0,
        0
    };
    for (size_t 순번 = 0; 순번 < sizeof(aanvraag)/4; 순번++) postvak_gegevens[순번] = aanvraag[순번];
    // 위 메시지의 werkelijk_gegevens 길이를 gebruik_WAARDE: 태그 toevoegen_invoer 시 tijdsduur_WAARDE 불일치를 방지한다.
    postvak_gegevens[0] = sizeof(aanvraag);
    if (!postvak()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned reactie_tijdsduur[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (postvak_gegevens[응답들[순번]] != (0x80000000u | reactie_tijdsduur[순번])) return 0;
    uint32_t Achtergrond_WAARDE = postvak_gegevens[28] & 0x3fffffffu;
    uint32_t Grootte = postvak_gegevens[29];
    uint32_t 받은너비 = postvak_gegevens[5], OPBRENGST_hoogte = postvak_gegevens[6], OPBRENGST_interlinie = postvak_gegevens[33];
    if (postvak_gegevens[15] != 32 || postvak_gegevens[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || OPBRENGST_hoogte < 480 || OPBRENGST_hoogte > 1080 ||
        postvak_gegevens[10] < 받은너비 || postvak_gegevens[11] < OPBRENGST_hoogte || postvak_gegevens[23] || postvak_gegevens[24] ||
        !Achtergrond_WAARDE || Achtergrond_WAARDE < 0x1000000 || (Achtergrond_WAARDE & 3) || OPBRENGST_interlinie < 받은너비 * 4 || (OPBRENGST_interlinie & 3) ||
        (uint64_t)OPBRENGST_interlinie * OPBRENGST_hoogte > Grootte || (uint64_t)Achtergrond_WAARDE + Grootte > 0x40000000u)
        return 0;
    Bord_Bereid_voor_tekening((volatile uint32_t *)(uintptr_t)Achtergrond_WAARDE, 받은너비, OPBRENGST_hoogte, OPBRENGST_interlinie);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 thread_WAARDE. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } context;
static context 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int informatie_Hardlopen[3] = {1, 0, 0};
static int actueel_taak;
extern void contextomschakeling(context *, context *);
extern void 자바작업(int32_t);
machine_Word Bord_RENDEMENT(void) {
    network_poll();
    int Vorige_item = actueel_taak, Volgende_item = (Vorige_item + 1) % 3;
    while (Volgende_item != Vorige_item && !informatie_Hardlopen[Volgende_item]) Volgende_item = (Volgende_item + 1) % 3;
    if (Volgende_item != Vorige_item) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (informatie_Hardlopen[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        actueel_taak = Volgende_item;
        contextomschakeling(&작업문맥들[Vorige_item], &작업문맥들[Volgende_item]);
    }
    return 0;
}
static void taak_bootstrap(void) {
    자바작업(actueel_taak);
    informatie_Hardlopen[actueel_taak] = 0;
    Bord_RENDEMENT();
    커널중단("finished task resumed");
}
machine_Word Bord_taak_maken(machine_Word id_WAARDE) {
    if (id_WAARDE < 1 || id_WAARDE > 2 || informatie_Hardlopen[id_WAARDE]) return (uint32_t)-1;
    memset(&작업문맥들[id_WAARDE], 0, sizeof(context));
    *(uint64_t *)쌓임공간들[id_WAARDE - 1] = 0x6b6f726f7373746bull;
    작업문맥들[id_WAARDE].저장값[11] = (uintptr_t)taak_bootstrap;
    작업문맥들[id_WAARDE].저장값[12] = (uintptr_t)(쌓임공간들[id_WAARDE - 1] + sizeof(쌓임공간들[0]));
    informatie_Hardlopen[id_WAARDE] = 1;
    return 0;
}
machine_Word Bord_taak_Status(machine_Word id_WAARDE) { return id_WAARDE < 3 ? informatie_Hardlopen[id_WAARDE] : (uint32_t)-1; }
extern machine_Word AOT_Geheugen_ZOEKEN(machine_Word);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
machine_Word Bord_query_Systeem(machine_Word invoer_WAARDE_962f286b, machine_Word INDEX) {
    if (invoer_WAARDE_962f286b==0) return 팔기억킬로바이트;
    if (invoer_WAARDE_962f286b==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (invoer_WAARDE_962f286b==2 || invoer_WAARDE_962f286b==3) return AOT_Geheugen_ZOEKEN(invoer_WAARDE_962f286b==3);
    if (invoer_WAARDE_962f286b==4) return 화면준비됨 ? (보드화면너비()*Bord_scherm_hoogte()*4+1023)/1024 : 0;
    if (invoer_WAARDE_962f286b==5) return 80*1024; /* Uitvoeren_opdracht ADRES_regio 16 MiB + 네 세션 보관 ADRES_regio. */
    if (invoer_WAARDE_962f286b>=20) return 사용자상태읽기(invoer_WAARDE_962f286b-20, INDEX);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[actueel_taak]; }
