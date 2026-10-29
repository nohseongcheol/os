#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "korisnik.h"
#include "../mreža_hrpa/mreža_hrpa.h"
typedef uintptr_t stroj_Word;
#define stroj_registar(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define poštanski_sandučić_adresa 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Sat_COUNT(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t FREQUENCY;
static volatile uint32_t poštanski_sandučić_podaci[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *podaci_položaj, int kodna_točka, size_t artikl_COUNT) { unsigned char *Dalje_pomak = podaci_položaj; while (artikl_COUNT--) *Dalje_pomak++ = kodna_točka; return podaci_položaj; }
void *memcpy(void *odredište_podaci, const void *niz_podaci, size_t artikl_COUNT) { unsigned char *첫째값 = odredište_podaci; const unsigned char *SECOND_VALUE = niz_podaci; while (artikl_COUNT--) *첫째값++ = *SECOND_VALUE++; return odredište_podaci; }

static int poštanski_sandučić(void) {
    uint32_t zahtjev = (uint32_t)(uintptr_t)poštanski_sandučić_podaci | 8;
    uint64_t Pokreni = Sat_COUNT();
    기억장벽();
    while (stroj_registar(poštanski_sandučić_adresa + 0x38) & 0x80000000u)
        if (Sat_COUNT() - Pokreni > FREQUENCY) return 0;
    stroj_registar(poštanski_sandučić_adresa + 0x20) = zahtjev;
    for (;;) {
        if (!(stroj_registar(poštanski_sandučić_adresa + 0x18) & 0x40000000u)) {
            uint32_t odgovor = stroj_registar(poštanski_sandučić_adresa);
            if (odgovor == zahtjev) { 기억장벽(); return poštanski_sandučić_podaci[1] == 0x80000000u; }
        }
        if (Sat_COUNT() - Pokreni > FREQUENCY) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terminal_bajt(unsigned);
extern int Terminal_na_čekanju(void);
extern void Terminal_pokazivač(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../udaljeno_VALUE/udaljeno_VALUE.h"
static int Tokovi;
static unsigned 직렬이전글자;
stroj_Word pano_Tokovi(stroj_Word 사용여부) { Tokovi=사용여부!=0; return 0; }
stroj_Word pano_kanal(stroj_Word kanal, stroj_Word kodna_točka) {
    if(Tokovi && 자바셸출력((int32_t)kanal,(int32_t)(kodna_točka&255))) return 0;
    Terminal_bajt(kodna_točka&255);
    원격출력(kodna_točka&255);
    if ((kodna_točka&255)==10 && 직렬이전글자!=13) {
        while (stroj_registar(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        stroj_registar(직렬장치)=13;
    }
    직렬이전글자=kodna_točka&255;
    while (stroj_registar(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    stroj_registar(직렬장치) = (uint32_t)kodna_točka & 255;
    return 0;
}
stroj_Word 보드글자쓰기(stroj_Word kodna_točka) { return pano_kanal(1,kodna_točka); }
stroj_Word 보드원시글자읽기(void) {
    int udaljeno_znak=원격입력();if(udaljeno_znak>=0)return udaljeno_znak;
    if (stroj_registar(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t VALUE = stroj_registar(직렬장치);
    if (VALUE & 0xf00) { stroj_registar(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return VALUE & 255;
}
stroj_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char paket_podaci[6];
    if(Terminal_na_čekanju())return (uint32_t)-4096;
    if(Tokovi){int32_t kodna_točka=자바셸입력();if(kodna_točka!=-3)return (uint32_t)kodna_točka;}
    for(;;){
        int kodna_točka=(int32_t)보드원시글자읽기();if(kodna_točka<0)return (uint32_t)kodna_točka;
        if(!꾸러미안쪽){if(kodna_točka!=30)return kodna_točka;꾸러미안쪽=1;사용량=0;continue;}
        paket_podaci[사용량++]=kodna_točka;if(사용량<6)continue;꾸러미안쪽=0;
        if(paket_podaci[0]==1)Terminal_pokazivač(paket_podaci[1],paket_podaci[2]+paket_podaci[3]*256,paket_podaci[4]+paket_podaci[5]*256);
        if(paket_podaci[0]==2)터미널바로가기키(paket_podaci[1]);
        if(paket_podaci[0]==3)터미널입력방식(paket_podaci[1]);
        if(Terminal_na_čekanju())return (uint32_t)-4096;
    }
}
stroj_Word 보드밀리초(void) { return (uint32_t)(Sat_COUNT() / (FREQUENCY / 1000)); }
stroj_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *niz_podaci) { while (*niz_podaci) 보드글자쓰기((unsigned char)*niz_podaci++); }
static void 직렬열여섯진출력(stroj_Word artikl_COUNT) { const char *열여섯진숫자 = "0123456789abcdef"; for (int niz_podaci = 60; niz_podaci >= 0; niz_podaci -= 4) 보드글자쓰기(열여섯진숫자[(artikl_COUNT >> niz_podaci) & 15]); }
stroj_Word pano_Stani(stroj_Word Stanje_VALUE) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(Stanje_VALUE); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); pano_Stani(1); __builtin_unreachable(); }
void pano_iznimka(stroj_Word iznimka_Stanje, stroj_Word naredba_položaj, stroj_Word nevaljan_adresa) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(iznimka_Stanje);
    직렬글출력(" PC="); 직렬열여섯진출력(naredba_položaj); 직렬글출력(" FAR="); 직렬열여섯진출력(nevaljan_adresa);
    pano_Stani(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    poštanski_sandučić_podaci[0]=32;poštanski_sandučić_podaci[1]=0;poštanski_sandučić_podaci[2]=0x10004;poštanski_sandučić_podaci[3]=8;poštanski_sandučić_podaci[4]=0;
    poštanski_sandučić_podaci[5]=poštanski_sandučić_podaci[6]=poštanski_sandučić_podaci[7]=0;
    return poštanski_sandučić()&&poštanski_sandučić_podaci[4]==0x80000008u&&(poštanski_sandučić_podaci[5]||poštanski_sandučić_podaci[6]);
}
int pano_apsolutna_adresa(unsigned char *adresa) {
    poštanski_sandučić_podaci[0]=32;poštanski_sandučić_podaci[1]=0;poštanski_sandučić_podaci[2]=0x10003;poštanski_sandučić_podaci[3]=8;poštanski_sandučić_podaci[4]=0;
    poštanski_sandučić_podaci[5]=poštanski_sandučić_podaci[6]=poštanski_sandučić_podaci[7]=0;
    if(!poštanski_sandučić()||(poštanski_sandučić_podaci[4]&0x80000000u)==0||(poštanski_sandučić_podaci[4]&0xffff)!=6)return 0;
    const unsigned char *podaci=(const unsigned char*)&poštanski_sandučić_podaci[5];unsigned SUM_VALUE=0;
    for(unsigned 순번=0;순번<6;순번++){adresa[순번]=podaci[순번];SUM_VALUE|=podaci[순번];}return SUM_VALUE&&!(adresa[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    stroj_registar(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    stroj_registar(범용입출력 + 4) = (stroj_registar(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    stroj_registar(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. kvar_VALUE 시 config.txt의 48MHz를 사용한다.
    poštanski_sandučić_podaci[0] = 36; poštanski_sandučić_podaci[1] = 0; poštanski_sandučić_podaci[2] = 0x38002; poštanski_sandučić_podaci[3] = 12;
    poštanski_sandučić_podaci[4] = 0; poštanski_sandučić_podaci[5] = 2; poštanski_sandučić_podaci[6] = 48000000; poštanski_sandučić_podaci[7] = 0; poštanski_sandučić_podaci[8] = 0;
    int 시계정상 = poštanski_sandučić();
    uint32_t 속도 = 시계정상 && poštanski_sandučić_podaci[6] >= 1843200 ? poštanski_sandučić_podaci[6] : 48000000;
    poštanski_sandučić_podaci[0]=32; poštanski_sandučić_podaci[1]=0; poštanski_sandučić_podaci[2]=0x10005; poštanski_sandučić_podaci[3]=8; poštanski_sandučić_podaci[4]=0;
    poštanski_sandučić_podaci[5]=poštanski_sandučić_podaci[6]=poštanski_sandučić_podaci[7]=0;
    if (poštanski_sandučić() && poštanski_sandučić_podaci[4]==0x80000008u) 팔기억킬로바이트=poštanski_sandučić_podaci[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    stroj_registar(직렬장치 + 0x44) = 0x7ff;
    stroj_registar(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    stroj_registar(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    stroj_registar(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    stroj_registar(직렬장치 + 0x38) = 0;
    stroj_registar(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
stroj_Word pano_FTP(stroj_Word Aktivnost) { return (uint32_t)ftp_control((int)Aktivnost); }
stroj_Word pano_mreža_stanje(stroj_Word unos_VALUE, stroj_Word INDEX) { return 망상태읽기(unos_VALUE, INDEX); }
stroj_Word pano_mreža_Postavke(stroj_Word Aktivnost, stroj_Word adresa, stroj_Word maska_VALUE, stroj_Word pristupnik_VALUE) { return (uint32_t)망설정하기(Aktivnost, adresa, maska_VALUE, pristupnik_VALUE); }
stroj_Word pano_slati_odgovor(stroj_Word adresa, stroj_Word narudžba_VALUE) { return (uint32_t)응답시험시작(adresa, narudžba_VALUE); }
stroj_Word 보드응답읽기(stroj_Word unos_VALUE) { return (uint32_t)응답시험읽기(unos_VALUE); }
stroj_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEX=0; INDEX<32; INDEX++) Zatvori_mreža(INDEX);
    for (unsigned INDEX=0; INDEX<4; INDEX++) pano_korisnička_kontrola(32+INDEX);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (stroj_registar(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    stroj_registar(0xfe100020ul)=0x5a000000u | (stroj_registar(0xfe100020ul)&~0xfffu) | 0x555;
    stroj_registar(0xfe100024ul)=0x5a000000u | 10;
    stroj_registar(0xfe10001cul)=0x5a000000u | (stroj_registar(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

stroj_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 redovno_artikl 크기를 읽는다. */
    const uint32_t upit_VALUE[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(upit_VALUE)/4; 순번++) poštanski_sandučić_podaci[순번] = upit_VALUE[순번];
    if (poštanski_sandučić() && poštanski_sandučić_podaci[4] == 0x80000008u &&
        poštanski_sandučić_podaci[5] >= 640 && poštanski_sandučić_podaci[5] <= 1920 &&
        poštanski_sandučić_podaci[6] >= 480 && poštanski_sandučić_podaci[6] <= 1080) {
        요청너비 = poštanski_sandučić_podaci[5]; 요청높이 = poštanski_sandučić_podaci[6];
    }
    const uint32_t zahtjev[] = {
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
    for (size_t 순번 = 0; 순번 < sizeof(zahtjev)/4; 순번++) poštanski_sandučić_podaci[순번] = zahtjev[순번];
    // 위 메시지의 stvaran_podaci 길이를 uporaba_VALUE: 태그 dodati_unos 시 길이 불일치를 방지한다.
    poštanski_sandučić_podaci[0] = sizeof(zahtjev);
    if (!poštanski_sandučić()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 응답길이[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (poštanski_sandučić_podaci[응답들[순번]] != (0x80000000u | 응답길이[순번])) return 0;
    uint32_t podloga_VALUE = poštanski_sandučić_podaci[28] & 0x3fffffffu;
    uint32_t Veličina = poštanski_sandučić_podaci[29];
    uint32_t 받은너비 = poštanski_sandučić_podaci[5], 받은높이 = poštanski_sandučić_podaci[6], RECEIVED_prored = poštanski_sandučić_podaci[33];
    if (poštanski_sandučić_podaci[15] != 32 || poštanski_sandučić_podaci[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        poštanski_sandučić_podaci[10] < 받은너비 || poštanski_sandučić_podaci[11] < 받은높이 || poštanski_sandučić_podaci[23] || poštanski_sandučić_podaci[24] ||
        !podloga_VALUE || podloga_VALUE < 0x1000000 || (podloga_VALUE & 3) || RECEIVED_prored < 받은너비 * 4 || (RECEIVED_prored & 3) ||
        (uint64_t)RECEIVED_prored * 받은높이 > Veličina || (uint64_t)podloga_VALUE + Veličina > 0x40000000u)
        return 0;
    pano_Pripremi_crtež((volatile uint32_t *)(uintptr_t)podloga_VALUE, 받은너비, 받은높이, RECEIVED_prored);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 nit_VALUE. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } 작업문맥;
static 작업문맥 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int odjel_informacijske_tehnologije_Trčim[3] = {1, 0, 0};
static int redovno_obaveza;
extern void promjena_konteksta(작업문맥 *, 작업문맥 *);
extern void 자바작업(int32_t);
stroj_Word pano_YIELD(void) {
    network_poll();
    int 이전 = redovno_obaveza, Dalje_artikl = (이전 + 1) % 3;
    while (Dalje_artikl != 이전 && !odjel_informacijske_tehnologije_Trčim[Dalje_artikl]) Dalje_artikl = (Dalje_artikl + 1) % 3;
    if (Dalje_artikl != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (odjel_informacijske_tehnologije_Trčim[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        redovno_obaveza = Dalje_artikl;
        promjena_konteksta(&작업문맥들[이전], &작업문맥들[Dalje_artikl]);
    }
    return 0;
}
static void obaveza_pokretanje(void) {
    자바작업(redovno_obaveza);
    odjel_informacijske_tehnologije_Trčim[redovno_obaveza] = 0;
    pano_YIELD();
    커널중단("finished task resumed");
}
stroj_Word pano_obaveza_Create(stroj_Word identifikator_VALUE) {
    if (identifikator_VALUE < 1 || identifikator_VALUE > 2 || odjel_informacijske_tehnologije_Trčim[identifikator_VALUE]) return (uint32_t)-1;
    memset(&작업문맥들[identifikator_VALUE], 0, sizeof(작업문맥));
    *(uint64_t *)쌓임공간들[identifikator_VALUE - 1] = 0x6b6f726f7373746bull;
    작업문맥들[identifikator_VALUE].저장값[11] = (uintptr_t)obaveza_pokretanje;
    작업문맥들[identifikator_VALUE].저장값[12] = (uintptr_t)(쌓임공간들[identifikator_VALUE - 1] + sizeof(쌓임공간들[0]));
    odjel_informacijske_tehnologije_Trčim[identifikator_VALUE] = 1;
    return 0;
}
stroj_Word pano_obaveza_Stanje(stroj_Word identifikator_VALUE) { return identifikator_VALUE < 3 ? odjel_informacijske_tehnologije_Trčim[identifikator_VALUE] : (uint32_t)-1; }
extern stroj_Word 미리번역기억조회(stroj_Word);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
stroj_Word pano_upit_sustav(stroj_Word unos_VALUE, stroj_Word INDEX) {
    if (unos_VALUE==0) return 팔기억킬로바이트;
    if (unos_VALUE==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (unos_VALUE==2 || unos_VALUE==3) return 미리번역기억조회(unos_VALUE==3);
    if (unos_VALUE==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (unos_VALUE==5) return 80*1024; /* Izvrši_naredba adresa_regije 16 MiB + 네 세션 보관 adresa_regije. */
    if (unos_VALUE>=20) return 사용자상태읽기(unos_VALUE-20, INDEX);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[redovno_obaveza]; }
