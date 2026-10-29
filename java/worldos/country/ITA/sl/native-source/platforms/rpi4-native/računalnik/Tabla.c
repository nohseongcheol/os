#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "uporabnik.h"
#include "../mreža_Sklad/mreža_Sklad.h"
typedef uintptr_t računalnik_Word;
#define računalnik_register(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define nabiralnik_naslov 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Ura_COUNT(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t FREQUENCY;
static volatile uint32_t nabiralnik_podatki[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *podatki_položaj, int koda_znaka, size_t element_COUNT) { unsigned char *Naprej_odmik = podatki_položaj; while (element_COUNT--) *Naprej_odmik++ = koda_znaka; return podatki_položaj; }
void *memcpy(void *cilj_podatki, const void *niz_podatki, size_t element_COUNT) { unsigned char *첫째값 = cilj_podatki; const unsigned char *SECOND_VALUE = niz_podatki; while (element_COUNT--) *첫째값++ = *SECOND_VALUE++; return cilj_podatki; }

static int nabiralnik(void) {
    uint32_t zahteva = (uint32_t)(uintptr_t)nabiralnik_podatki | 8;
    uint64_t Zaženi = Ura_COUNT();
    기억장벽();
    while (računalnik_register(nabiralnik_naslov + 0x38) & 0x80000000u)
        if (Ura_COUNT() - Zaženi > FREQUENCY) return 0;
    računalnik_register(nabiralnik_naslov + 0x20) = zahteva;
    for (;;) {
        if (!(računalnik_register(nabiralnik_naslov + 0x18) & 0x40000000u)) {
            uint32_t odgovor = računalnik_register(nabiralnik_naslov);
            if (odgovor == zahteva) { 기억장벽(); return nabiralnik_podatki[1] == 0x80000000u; }
        }
        if (Ura_COUNT() - Zaženi > FREQUENCY) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terminal_bajt(unsigned);
extern int Terminal_čakajoče(void);
extern void Terminal_kazalec(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../oddaljen_VALUE/oddaljen_VALUE.h"
static int Tokovi;
static unsigned 직렬이전글자;
računalnik_Word Tabla_Tokovi(računalnik_Word 사용여부) { Tokovi=사용여부!=0; return 0; }
računalnik_Word Tabla_Kanal(računalnik_Word Kanal, računalnik_Word koda_znaka) {
    if(Tokovi && 자바셸출력((int32_t)Kanal,(int32_t)(koda_znaka&255))) return 0;
    Terminal_bajt(koda_znaka&255);
    원격출력(koda_znaka&255);
    if ((koda_znaka&255)==10 && 직렬이전글자!=13) {
        while (računalnik_register(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        računalnik_register(직렬장치)=13;
    }
    직렬이전글자=koda_znaka&255;
    while (računalnik_register(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    računalnik_register(직렬장치) = (uint32_t)koda_znaka & 255;
    return 0;
}
računalnik_Word 보드글자쓰기(računalnik_Word koda_znaka) { return Tabla_Kanal(1,koda_znaka); }
računalnik_Word 보드원시글자읽기(void) {
    int oddaljen_znak=원격입력();if(oddaljen_znak>=0)return oddaljen_znak;
    if (računalnik_register(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t VALUE = računalnik_register(직렬장치);
    if (VALUE & 0xf00) { računalnik_register(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return VALUE & 255;
}
računalnik_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char paket_podatki[6];
    if(Terminal_čakajoče())return (uint32_t)-4096;
    if(Tokovi){int32_t koda_znaka=자바셸입력();if(koda_znaka!=-3)return (uint32_t)koda_znaka;}
    for(;;){
        int koda_znaka=(int32_t)보드원시글자읽기();if(koda_znaka<0)return (uint32_t)koda_znaka;
        if(!꾸러미안쪽){if(koda_znaka!=30)return koda_znaka;꾸러미안쪽=1;사용량=0;continue;}
        paket_podatki[사용량++]=koda_znaka;if(사용량<6)continue;꾸러미안쪽=0;
        if(paket_podatki[0]==1)Terminal_kazalec(paket_podatki[1],paket_podatki[2]+paket_podatki[3]*256,paket_podatki[4]+paket_podatki[5]*256);
        if(paket_podatki[0]==2)터미널바로가기키(paket_podatki[1]);
        if(paket_podatki[0]==3)터미널입력방식(paket_podatki[1]);
        if(Terminal_čakajoče())return (uint32_t)-4096;
    }
}
računalnik_Word 보드밀리초(void) { return (uint32_t)(Ura_COUNT() / (FREQUENCY / 1000)); }
računalnik_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *niz_podatki) { while (*niz_podatki) 보드글자쓰기((unsigned char)*niz_podatki++); }
static void 직렬열여섯진출력(računalnik_Word element_COUNT) { const char *열여섯진숫자 = "0123456789abcdef"; for (int niz_podatki = 60; niz_podatki >= 0; niz_podatki -= 4) 보드글자쓰기(열여섯진숫자[(element_COUNT >> niz_podatki) & 15]); }
računalnik_Word Tabla_Stop(računalnik_Word stanje_VALUE) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(stanje_VALUE); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); Tabla_Stop(1); __builtin_unreachable(); }
void Tabla_izjema(računalnik_Word izjema_stanje, računalnik_Word ukaz_položaj, računalnik_Word neveljaven_naslov) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(izjema_stanje);
    직렬글출력(" PC="); 직렬열여섯진출력(ukaz_položaj); 직렬글출력(" FAR="); 직렬열여섯진출력(neveljaven_naslov);
    Tabla_Stop(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    nabiralnik_podatki[0]=32;nabiralnik_podatki[1]=0;nabiralnik_podatki[2]=0x10004;nabiralnik_podatki[3]=8;nabiralnik_podatki[4]=0;
    nabiralnik_podatki[5]=nabiralnik_podatki[6]=nabiralnik_podatki[7]=0;
    return nabiralnik()&&nabiralnik_podatki[4]==0x80000008u&&(nabiralnik_podatki[5]||nabiralnik_podatki[6]);
}
int Tabla_absolutni_naslov(unsigned char *naslov) {
    nabiralnik_podatki[0]=32;nabiralnik_podatki[1]=0;nabiralnik_podatki[2]=0x10003;nabiralnik_podatki[3]=8;nabiralnik_podatki[4]=0;
    nabiralnik_podatki[5]=nabiralnik_podatki[6]=nabiralnik_podatki[7]=0;
    if(!nabiralnik()||(nabiralnik_podatki[4]&0x80000000u)==0||(nabiralnik_podatki[4]&0xffff)!=6)return 0;
    const unsigned char *podatki=(const unsigned char*)&nabiralnik_podatki[5];unsigned SUM_VALUE=0;
    for(unsigned 순번=0;순번<6;순번++){naslov[순번]=podatki[순번];SUM_VALUE|=podatki[순번];}return SUM_VALUE&&!(naslov[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    računalnik_register(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    računalnik_register(범용입출력 + 4) = (računalnik_register(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    računalnik_register(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. napaka_VALUE 시 config.txt의 48MHz를 사용한다.
    nabiralnik_podatki[0] = 36; nabiralnik_podatki[1] = 0; nabiralnik_podatki[2] = 0x38002; nabiralnik_podatki[3] = 12;
    nabiralnik_podatki[4] = 0; nabiralnik_podatki[5] = 2; nabiralnik_podatki[6] = 48000000; nabiralnik_podatki[7] = 0; nabiralnik_podatki[8] = 0;
    int 시계정상 = nabiralnik();
    uint32_t 속도 = 시계정상 && nabiralnik_podatki[6] >= 1843200 ? nabiralnik_podatki[6] : 48000000;
    nabiralnik_podatki[0]=32; nabiralnik_podatki[1]=0; nabiralnik_podatki[2]=0x10005; nabiralnik_podatki[3]=8; nabiralnik_podatki[4]=0;
    nabiralnik_podatki[5]=nabiralnik_podatki[6]=nabiralnik_podatki[7]=0;
    if (nabiralnik() && nabiralnik_podatki[4]==0x80000008u) 팔기억킬로바이트=nabiralnik_podatki[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    računalnik_register(직렬장치 + 0x44) = 0x7ff;
    računalnik_register(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    računalnik_register(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    računalnik_register(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    računalnik_register(직렬장치 + 0x38) = 0;
    računalnik_register(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
računalnik_Word Tabla_FTP(računalnik_Word Dejanje) { return (uint32_t)ftp_control((int)Dejanje); }
računalnik_Word Tabla_mreža_stanje(računalnik_Word vnos_VALUE, računalnik_Word INDEX) { return 망상태읽기(vnos_VALUE, INDEX); }
računalnik_Word Tabla_mreža_Nastavitve(računalnik_Word Dejanje, računalnik_Word naslov, računalnik_Word maska_VALUE, računalnik_Word prehod_VALUE) { return (uint32_t)konfigurirati_mreža(Dejanje, naslov, maska_VALUE, prehod_VALUE); }
računalnik_Word Tabla_poslati_odziv(računalnik_Word naslov, računalnik_Word naročilo_VALUE) { return (uint32_t)Start_odziv_preskusiti(naslov, naročilo_VALUE); }
računalnik_Word 보드응답읽기(računalnik_Word vnos_VALUE) { return (uint32_t)응답시험읽기(vnos_VALUE); }
računalnik_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEX=0; INDEX<32; INDEX++) Zapri_mreža(INDEX);
    for (unsigned INDEX=0; INDEX<4; INDEX++) Tabla_uporabniški_kontrolnik(32+INDEX);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (računalnik_register(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    računalnik_register(0xfe100020ul)=0x5a000000u | (računalnik_register(0xfe100020ul)&~0xfffu) | 0x555;
    računalnik_register(0xfe100024ul)=0x5a000000u | 10;
    računalnik_register(0xfe10001cul)=0x5a000000u | (računalnik_register(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

računalnik_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 sprotno_element 크기를 읽는다. */
    const uint32_t poizvedba_VALUE[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(poizvedba_VALUE)/4; 순번++) nabiralnik_podatki[순번] = poizvedba_VALUE[순번];
    if (nabiralnik() && nabiralnik_podatki[4] == 0x80000008u &&
        nabiralnik_podatki[5] >= 640 && nabiralnik_podatki[5] <= 1920 &&
        nabiralnik_podatki[6] >= 480 && nabiralnik_podatki[6] <= 1080) {
        요청너비 = nabiralnik_podatki[5]; 요청높이 = nabiralnik_podatki[6];
    }
    const uint32_t zahteva[] = {
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
    for (size_t 순번 = 0; 순번 < sizeof(zahteva)/4; 순번++) nabiralnik_podatki[순번] = zahteva[순번];
    // 위 메시지의 dejanski_podatki 길이를 uporaba_VALUE: 태그 dodati_vnos 시 길이 불일치를 방지한다.
    nabiralnik_podatki[0] = sizeof(zahteva);
    if (!nabiralnik()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 응답길이[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (nabiralnik_podatki[응답들[순번]] != (0x80000000u | 응답길이[순번])) return 0;
    uint32_t Ozadje_VALUE = nabiralnik_podatki[28] & 0x3fffffffu;
    uint32_t Velikost = nabiralnik_podatki[29];
    uint32_t 받은너비 = nabiralnik_podatki[5], RECEIVED_višina = nabiralnik_podatki[6], RECEIVED_razmik_vrstic = nabiralnik_podatki[33];
    if (nabiralnik_podatki[15] != 32 || nabiralnik_podatki[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || RECEIVED_višina < 480 || RECEIVED_višina > 1080 ||
        nabiralnik_podatki[10] < 받은너비 || nabiralnik_podatki[11] < RECEIVED_višina || nabiralnik_podatki[23] || nabiralnik_podatki[24] ||
        !Ozadje_VALUE || Ozadje_VALUE < 0x1000000 || (Ozadje_VALUE & 3) || RECEIVED_razmik_vrstic < 받은너비 * 4 || (RECEIVED_razmik_vrstic & 3) ||
        (uint64_t)RECEIVED_razmik_vrstic * RECEIVED_višina > Velikost || (uint64_t)Ozadje_VALUE + Velikost > 0x40000000u)
        return 0;
    Tabla_Pripravi_risba((volatile uint32_t *)(uintptr_t)Ozadje_VALUE, 받은너비, RECEIVED_višina, RECEIVED_razmik_vrstic);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 nit_VALUE. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } 작업문맥;
static 작업문맥 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int informacijska_tehnologija_Tek[3] = {1, 0, 0};
static int sprotno_opravek;
extern void zamenjava_vsebine(작업문맥 *, 작업문맥 *);
extern void 자바작업(int32_t);
računalnik_Word Tabla_YIELD(void) {
    network_poll();
    int 이전 = sprotno_opravek, Naprej_element = (이전 + 1) % 3;
    while (Naprej_element != 이전 && !informacijska_tehnologija_Tek[Naprej_element]) Naprej_element = (Naprej_element + 1) % 3;
    if (Naprej_element != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (informacijska_tehnologija_Tek[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        sprotno_opravek = Naprej_element;
        zamenjava_vsebine(&작업문맥들[이전], &작업문맥들[Naprej_element]);
    }
    return 0;
}
static void opravek_zagnati(void) {
    자바작업(sprotno_opravek);
    informacijska_tehnologija_Tek[sprotno_opravek] = 0;
    Tabla_YIELD();
    커널중단("finished task resumed");
}
računalnik_Word Tabla_opravek_Ustvari(računalnik_Word identifikator_VALUE) {
    if (identifikator_VALUE < 1 || identifikator_VALUE > 2 || informacijska_tehnologija_Tek[identifikator_VALUE]) return (uint32_t)-1;
    memset(&작업문맥들[identifikator_VALUE], 0, sizeof(작업문맥));
    *(uint64_t *)쌓임공간들[identifikator_VALUE - 1] = 0x6b6f726f7373746bull;
    작업문맥들[identifikator_VALUE].저장값[11] = (uintptr_t)opravek_zagnati;
    작업문맥들[identifikator_VALUE].저장값[12] = (uintptr_t)(쌓임공간들[identifikator_VALUE - 1] + sizeof(쌓임공간들[0]));
    informacijska_tehnologija_Tek[identifikator_VALUE] = 1;
    return 0;
}
računalnik_Word Tabla_opravek_stanje(računalnik_Word identifikator_VALUE) { return identifikator_VALUE < 3 ? informacijska_tehnologija_Tek[identifikator_VALUE] : (uint32_t)-1; }
extern računalnik_Word 미리번역기억조회(računalnik_Word);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
računalnik_Word Tabla_poizvedba_sistem(računalnik_Word vnos_VALUE, računalnik_Word INDEX) {
    if (vnos_VALUE==0) return 팔기억킬로바이트;
    if (vnos_VALUE==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (vnos_VALUE==2 || vnos_VALUE==3) return 미리번역기억조회(vnos_VALUE==3);
    if (vnos_VALUE==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (vnos_VALUE==5) return 80*1024; /* Izvedi_ukaz naslov_območje 16 MiB + 네 세션 보관 naslov_območje. */
    if (vnos_VALUE>=20) return 사용자상태읽기(vnos_VALUE-20, INDEX);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[sprotno_opravek]; }
