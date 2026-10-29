#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "korisnik.h"
#include "../Mreža_stek/Mreža_stek.h"
typedef uintptr_t računar_Word;
#define računar_registar(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define poštansko_sanduče_adresa 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Sat_COUNT(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t FREQUENCY;
static volatile uint32_t poštansko_sanduče_podaci[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *podaci_pozicija, int kôd_znaka, size_t stavka_COUNT) { unsigned char *Dalje_Pomak = podaci_pozicija; while (stavka_COUNT--) *Dalje_Pomak++ = kôd_znaka; return podaci_pozicija; }
void *memcpy(void *odredište_podaci, const void *niska_podaci, size_t stavka_COUNT) { unsigned char *첫째값 = odredište_podaci; const unsigned char *SECOND_VALUE = niska_podaci; while (stavka_COUNT--) *첫째값++ = *SECOND_VALUE++; return odredište_podaci; }

static int poštansko_sanduče(void) {
    uint32_t zahtev = (uint32_t)(uintptr_t)poštansko_sanduče_podaci | 8;
    uint64_t koristiti = Sat_COUNT();
    기억장벽();
    while (računar_registar(poštansko_sanduče_adresa + 0x38) & 0x80000000u)
        if (Sat_COUNT() - koristiti > FREQUENCY) return 0;
    računar_registar(poštansko_sanduče_adresa + 0x20) = zahtev;
    for (;;) {
        if (!(računar_registar(poštansko_sanduče_adresa + 0x18) & 0x40000000u)) {
            uint32_t odgovor = računar_registar(poštansko_sanduče_adresa);
            if (odgovor == zahtev) { 기억장벽(); return poštansko_sanduče_podaci[1] == 0x80000000u; }
        }
        if (Sat_COUNT() - koristiti > FREQUENCY) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terminal_bajt(unsigned);
extern int Terminal_na_čekanju(void);
extern void Terminal_pokazivač(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../udaljen_VALUE/udaljen_VALUE.h"
static int Tokovi;
static unsigned 직렬이전글자;
računar_Word Tabla_Tokovi(računar_Word 사용여부) { Tokovi=사용여부!=0; return 0; }
računar_Word Tabla_Kanal(računar_Word Kanal, računar_Word kôd_znaka) {
    if(Tokovi && 자바셸출력((int32_t)Kanal,(int32_t)(kôd_znaka&255))) return 0;
    Terminal_bajt(kôd_znaka&255);
    원격출력(kôd_znaka&255);
    if ((kôd_znaka&255)==10 && 직렬이전글자!=13) {
        while (računar_registar(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        računar_registar(직렬장치)=13;
    }
    직렬이전글자=kôd_znaka&255;
    while (računar_registar(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    računar_registar(직렬장치) = (uint32_t)kôd_znaka & 255;
    return 0;
}
računar_Word 보드글자쓰기(računar_Word kôd_znaka) { return Tabla_Kanal(1,kôd_znaka); }
računar_Word 보드원시글자읽기(void) {
    int udaljen_znak=원격입력();if(udaljen_znak>=0)return udaljen_znak;
    if (računar_registar(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t VALUE = računar_registar(직렬장치);
    if (VALUE & 0xf00) { računar_registar(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return VALUE & 255;
}
računar_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char paket_podaci[6];
    if(Terminal_na_čekanju())return (uint32_t)-4096;
    if(Tokovi){int32_t kôd_znaka=자바셸입력();if(kôd_znaka!=-3)return (uint32_t)kôd_znaka;}
    for(;;){
        int kôd_znaka=(int32_t)보드원시글자읽기();if(kôd_znaka<0)return (uint32_t)kôd_znaka;
        if(!꾸러미안쪽){if(kôd_znaka!=30)return kôd_znaka;꾸러미안쪽=1;사용량=0;continue;}
        paket_podaci[사용량++]=kôd_znaka;if(사용량<6)continue;꾸러미안쪽=0;
        if(paket_podaci[0]==1)Terminal_pokazivač(paket_podaci[1],paket_podaci[2]+paket_podaci[3]*256,paket_podaci[4]+paket_podaci[5]*256);
        if(paket_podaci[0]==2)터미널바로가기키(paket_podaci[1]);
        if(paket_podaci[0]==3)터미널입력방식(paket_podaci[1]);
        if(Terminal_na_čekanju())return (uint32_t)-4096;
    }
}
računar_Word 보드밀리초(void) { return (uint32_t)(Sat_COUNT() / (FREQUENCY / 1000)); }
računar_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *niska_podaci) { while (*niska_podaci) 보드글자쓰기((unsigned char)*niska_podaci++); }
static void 직렬열여섯진출력(računar_Word stavka_COUNT) { const char *열여섯진숫자 = "0123456789abcdef"; for (int niska_podaci = 60; niska_podaci >= 0; niska_podaci -= 4) 보드글자쓰기(열여섯진숫자[(stavka_COUNT >> niska_podaci) & 15]); }
računar_Word Tabla_Stani(računar_Word Status_VALUE) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(Status_VALUE); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); Tabla_Stani(1); __builtin_unreachable(); }
void Tabla_izuzetak(računar_Word izuzetak_Status, računar_Word komanda_pozicija, računar_Word nevažeći_adresa) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(izuzetak_Status);
    직렬글출력(" PC="); 직렬열여섯진출력(komanda_pozicija); 직렬글출력(" FAR="); 직렬열여섯진출력(nevažeći_adresa);
    Tabla_Stani(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    poštansko_sanduče_podaci[0]=32;poštansko_sanduče_podaci[1]=0;poštansko_sanduče_podaci[2]=0x10004;poštansko_sanduče_podaci[3]=8;poštansko_sanduče_podaci[4]=0;
    poštansko_sanduče_podaci[5]=poštansko_sanduče_podaci[6]=poštansko_sanduče_podaci[7]=0;
    return poštansko_sanduče()&&poštansko_sanduče_podaci[4]==0x80000008u&&(poštansko_sanduče_podaci[5]||poštansko_sanduče_podaci[6]);
}
int Tabla_apsolutna_adresa(unsigned char *adresa) {
    poštansko_sanduče_podaci[0]=32;poštansko_sanduče_podaci[1]=0;poštansko_sanduče_podaci[2]=0x10003;poštansko_sanduče_podaci[3]=8;poštansko_sanduče_podaci[4]=0;
    poštansko_sanduče_podaci[5]=poštansko_sanduče_podaci[6]=poštansko_sanduče_podaci[7]=0;
    if(!poštansko_sanduče()||(poštansko_sanduče_podaci[4]&0x80000000u)==0||(poštansko_sanduče_podaci[4]&0xffff)!=6)return 0;
    const unsigned char *podaci=(const unsigned char*)&poštansko_sanduče_podaci[5];unsigned SUM_VALUE=0;
    for(unsigned 순번=0;순번<6;순번++){adresa[순번]=podaci[순번];SUM_VALUE|=podaci[순번];}return SUM_VALUE&&!(adresa[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    računar_registar(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    računar_registar(범용입출력 + 4) = (računar_registar(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    računar_registar(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. otkazivanje_VALUE 시 config.txt의 48MHz를 사용한다.
    poštansko_sanduče_podaci[0] = 36; poštansko_sanduče_podaci[1] = 0; poštansko_sanduče_podaci[2] = 0x38002; poštansko_sanduče_podaci[3] = 12;
    poštansko_sanduče_podaci[4] = 0; poštansko_sanduče_podaci[5] = 2; poštansko_sanduče_podaci[6] = 48000000; poštansko_sanduče_podaci[7] = 0; poštansko_sanduče_podaci[8] = 0;
    int 시계정상 = poštansko_sanduče();
    uint32_t 속도 = 시계정상 && poštansko_sanduče_podaci[6] >= 1843200 ? poštansko_sanduče_podaci[6] : 48000000;
    poštansko_sanduče_podaci[0]=32; poštansko_sanduče_podaci[1]=0; poštansko_sanduče_podaci[2]=0x10005; poštansko_sanduče_podaci[3]=8; poštansko_sanduče_podaci[4]=0;
    poštansko_sanduče_podaci[5]=poštansko_sanduče_podaci[6]=poštansko_sanduče_podaci[7]=0;
    if (poštansko_sanduče() && poštansko_sanduče_podaci[4]==0x80000008u) 팔기억킬로바이트=poštansko_sanduče_podaci[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    računar_registar(직렬장치 + 0x44) = 0x7ff;
    računar_registar(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    računar_registar(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    računar_registar(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    računar_registar(직렬장치 + 0x38) = 0;
    računar_registar(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
računar_Word Tabla_FTP(računar_Word radnja) { return (uint32_t)ftp_control((int)radnja); }
računar_Word Tabla_Mreža_status(računar_Word stavka_VALUE, računar_Word INDEX) { return 망상태읽기(stavka_VALUE, INDEX); }
računar_Word Tabla_Mreža_Postavke(računar_Word radnja, računar_Word adresa, računar_Word maska_VALUE, računar_Word mrežni_prolaz_VALUE) { return (uint32_t)konfigurisati_Mreža(radnja, adresa, maska_VALUE, mrežni_prolaz_VALUE); }
računar_Word Tabla_poslati_odgovor(računar_Word adresa, računar_Word poručiti_VALUE) { return (uint32_t)응답시험시작(adresa, poručiti_VALUE); }
računar_Word 보드응답읽기(računar_Word stavka_VALUE) { return (uint32_t)응답시험읽기(stavka_VALUE); }
računar_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEX=0; INDEX<32; INDEX++) Zatvori_Mreža(INDEX);
    for (unsigned INDEX=0; INDEX<4; INDEX++) Tabla_korisnička_kontrola(32+INDEX);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (računar_registar(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    računar_registar(0xfe100020ul)=0x5a000000u | (računar_registar(0xfe100020ul)&~0xfffu) | 0x555;
    računar_registar(0xfe100024ul)=0x5a000000u | 10;
    računar_registar(0xfe10001cul)=0x5a000000u | (računar_registar(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

računar_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 aktuelno_stavka 크기를 읽는다. */
    const uint32_t upit_VALUE[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(upit_VALUE)/4; 순번++) poštansko_sanduče_podaci[순번] = upit_VALUE[순번];
    if (poštansko_sanduče() && poštansko_sanduče_podaci[4] == 0x80000008u &&
        poštansko_sanduče_podaci[5] >= 640 && poštansko_sanduče_podaci[5] <= 1920 &&
        poštansko_sanduče_podaci[6] >= 480 && poštansko_sanduče_podaci[6] <= 1080) {
        요청너비 = poštansko_sanduče_podaci[5]; 요청높이 = poštansko_sanduče_podaci[6];
    }
    const uint32_t zahtev[] = {
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
    for (size_t 순번 = 0; 순번 < sizeof(zahtev)/4; 순번++) poštansko_sanduče_podaci[순번] = zahtev[순번];
    // 위 메시지의 stvarni_podaci 길이를 koristiti_VALUE: 태그 dodati_stavka 시 길이 불일치를 방지한다.
    poštansko_sanduče_podaci[0] = sizeof(zahtev);
    if (!poštansko_sanduče()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 응답길이[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (poštansko_sanduče_podaci[응답들[순번]] != (0x80000000u | 응답길이[순번])) return 0;
    uint32_t poster_VALUE = poštansko_sanduče_podaci[28] & 0x3fffffffu;
    uint32_t promeniti_veličinu = poštansko_sanduče_podaci[29];
    uint32_t 받은너비 = poštansko_sanduče_podaci[5], 받은높이 = poštansko_sanduče_podaci[6], RECEIVED_prored = poštansko_sanduče_podaci[33];
    if (poštansko_sanduče_podaci[15] != 32 || poštansko_sanduče_podaci[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        poštansko_sanduče_podaci[10] < 받은너비 || poštansko_sanduče_podaci[11] < 받은높이 || poštansko_sanduče_podaci[23] || poštansko_sanduče_podaci[24] ||
        !poster_VALUE || poster_VALUE < 0x1000000 || (poster_VALUE & 3) || RECEIVED_prored < 받은너비 * 4 || (RECEIVED_prored & 3) ||
        (uint64_t)RECEIVED_prored * 받은높이 > promeniti_veličinu || (uint64_t)poster_VALUE + promeniti_veličinu > 0x40000000u)
        return 0;
    Tabla_Pripremi_crtež((volatile uint32_t *)(uintptr_t)poster_VALUE, 받은너비, 받은높이, RECEIVED_prored);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 nit_VALUE. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } 작업문맥;
static 작업문맥 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int informatičko_odeljenje_Trčanje[3] = {1, 0, 0};
static int aktuelno_obaveza;
extern void promena_konteksta(작업문맥 *, 작업문맥 *);
extern void 자바작업(int32_t);
računar_Word Tabla_YIELD(void) {
    network_poll();
    int 이전 = aktuelno_obaveza, Dalje_stavka = (이전 + 1) % 3;
    while (Dalje_stavka != 이전 && !informatičko_odeljenje_Trčanje[Dalje_stavka]) Dalje_stavka = (Dalje_stavka + 1) % 3;
    if (Dalje_stavka != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (informatičko_odeljenje_Trčanje[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        aktuelno_obaveza = Dalje_stavka;
        promena_konteksta(&작업문맥들[이전], &작업문맥들[Dalje_stavka]);
    }
    return 0;
}
static void 작업첫시작(void) {
    자바작업(aktuelno_obaveza);
    informatičko_odeljenje_Trčanje[aktuelno_obaveza] = 0;
    Tabla_YIELD();
    커널중단("finished task resumed");
}
računar_Word Tabla_obaveza_Create(računar_Word identifikator_VALUE) {
    if (identifikator_VALUE < 1 || identifikator_VALUE > 2 || informatičko_odeljenje_Trčanje[identifikator_VALUE]) return (uint32_t)-1;
    memset(&작업문맥들[identifikator_VALUE], 0, sizeof(작업문맥));
    *(uint64_t *)쌓임공간들[identifikator_VALUE - 1] = 0x6b6f726f7373746bull;
    작업문맥들[identifikator_VALUE].저장값[11] = (uintptr_t)작업첫시작;
    작업문맥들[identifikator_VALUE].저장값[12] = (uintptr_t)(쌓임공간들[identifikator_VALUE - 1] + sizeof(쌓임공간들[0]));
    informatičko_odeljenje_Trčanje[identifikator_VALUE] = 1;
    return 0;
}
računar_Word Tabla_obaveza_Status(računar_Word identifikator_VALUE) { return identifikator_VALUE < 3 ? informatičko_odeljenje_Trčanje[identifikator_VALUE] : (uint32_t)-1; }
extern računar_Word 미리번역기억조회(računar_Word);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
računar_Word Tabla_upit_sistem(računar_Word stavka_VALUE, računar_Word INDEX) {
    if (stavka_VALUE==0) return 팔기억킬로바이트;
    if (stavka_VALUE==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (stavka_VALUE==2 || stavka_VALUE==3) return 미리번역기억조회(stavka_VALUE==3);
    if (stavka_VALUE==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (stavka_VALUE==5) return 80*1024; /* Izvrši_komanda adresa_oblast 16 MiB + 네 세션 보관 adresa_oblast. */
    if (stavka_VALUE>=20) return 사용자상태읽기(stavka_VALUE-20, INDEX);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[aktuelno_obaveza]; }
