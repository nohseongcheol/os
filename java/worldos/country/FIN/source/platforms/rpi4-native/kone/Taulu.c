#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "käyttäjätila.h"
#include "../verkko_Pino/verkko_Pino.h"
typedef uintptr_t kone_Word;
#define kone_rekisteri(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define postilaatikko_OSOITE 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Kello_LASKE(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t TAAJUUS;
static volatile uint32_t postilaatikko_data[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *data_toimi, int merkkikoodi, size_t kohde_LASKE) { unsigned char *Seuraava_SIIRTYMÄ = data_toimi; while (kohde_LASKE--) *Seuraava_SIIRTYMÄ++ = merkkikoodi; return data_toimi; }
void *memcpy(void *kohde_data, const void *merkkijono_data, size_t kohde_LASKE) { unsigned char *첫째값 = kohde_data; const unsigned char *SEKUNNIT_ARVO = merkkijono_data; while (kohde_LASKE--) *첫째값++ = *SEKUNNIT_ARVO++; return kohde_data; }

static int postilaatikko(void) {
    uint32_t pyyntö = (uint32_t)(uintptr_t)postilaatikko_data | 8;
    uint64_t Suorita_2 = Kello_LASKE();
    기억장벽();
    while (kone_rekisteri(postilaatikko_OSOITE + 0x38) & 0x80000000u)
        if (Kello_LASKE() - Suorita_2 > TAAJUUS) return 0;
    kone_rekisteri(postilaatikko_OSOITE + 0x20) = pyyntö;
    for (;;) {
        if (!(kone_rekisteri(postilaatikko_OSOITE + 0x18) & 0x40000000u)) {
            uint32_t palaute = kone_rekisteri(postilaatikko_OSOITE);
            if (palaute == pyyntö) { 기억장벽(); return postilaatikko_data[1] == 0x80000000u; }
        }
        if (Kello_LASKE() - Suorita_2 > TAAJUUS) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Pääte_tavu(unsigned);
extern int Pääte_Odottaa(void);
extern void Pääte_osoitin(unsigned,int,int),터미널바로가기키(unsigned);
extern void Pääte_syöte_tila(unsigned);
#include "../etä_ARVO/etä_ARVO.h"
static int Viestivirrat;
static unsigned 직렬이전글자;
kone_Word Taulu_Viestivirrat(kone_Word 사용여부) { Viestivirrat=사용여부!=0; return 0; }
kone_Word Taulu_Media(kone_Word Media, kone_Word merkkikoodi) {
    if(Viestivirrat && 자바셸출력((int32_t)Media,(int32_t)(merkkikoodi&255))) return 0;
    Pääte_tavu(merkkikoodi&255);
    etä_tulos(merkkikoodi&255);
    if ((merkkikoodi&255)==10 && 직렬이전글자!=13) {
        while (kone_rekisteri(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        kone_rekisteri(직렬장치)=13;
    }
    직렬이전글자=merkkikoodi&255;
    while (kone_rekisteri(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    kone_rekisteri(직렬장치) = (uint32_t)merkkikoodi & 255;
    return 0;
}
kone_Word 보드글자쓰기(kone_Word merkkikoodi) { return Taulu_Media(1,merkkikoodi); }
kone_Word 보드원시글자읽기(void) {
    int etä_merkki=etä_syöte();if(etä_merkki>=0)return etä_merkki;
    if (kone_rekisteri(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t ARVO = kone_rekisteri(직렬장치);
    if (ARVO & 0xf00) { kone_rekisteri(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return ARVO & 255;
}
kone_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char paketti_data[6];
    if(Pääte_Odottaa())return (uint32_t)-4096;
    if(Viestivirrat){int32_t merkkikoodi=자바셸입력();if(merkkikoodi!=-3)return (uint32_t)merkkikoodi;}
    for(;;){
        int merkkikoodi=(int32_t)보드원시글자읽기();if(merkkikoodi<0)return (uint32_t)merkkikoodi;
        if(!꾸러미안쪽){if(merkkikoodi!=30)return merkkikoodi;꾸러미안쪽=1;사용량=0;continue;}
        paketti_data[사용량++]=merkkikoodi;if(사용량<6)continue;꾸러미안쪽=0;
        if(paketti_data[0]==1)Pääte_osoitin(paketti_data[1],paketti_data[2]+paketti_data[3]*256,paketti_data[4]+paketti_data[5]*256);
        if(paketti_data[0]==2)터미널바로가기키(paketti_data[1]);
        if(paketti_data[0]==3)Pääte_syöte_tila(paketti_data[1]);
        if(Pääte_Odottaa())return (uint32_t)-4096;
    }
}
kone_Word 보드밀리초(void) { return (uint32_t)(Kello_LASKE() / (TAAJUUS / 1000)); }
kone_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *merkkijono_data) { while (*merkkijono_data) 보드글자쓰기((unsigned char)*merkkijono_data++); }
static void 직렬열여섯진출력(kone_Word kohde_LASKE) { const char *열여섯진숫자 = "0123456789abcdef"; for (int merkkijono_data = 60; merkkijono_data >= 0; merkkijono_data -= 4) 보드글자쓰기(열여섯진숫자[(kohde_LASKE >> merkkijono_data) & 15]); }
kone_Word Taulu_Seis(kone_Word Tila_ARVO) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(Tila_ARVO); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); Taulu_Seis(1); __builtin_unreachable(); }
void Taulu_poikkeus(kone_Word poikkeus_Tila, kone_Word komento_toimi, kone_Word pätemätön_OSOITE) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(poikkeus_Tila);
    직렬글출력(" PC="); 직렬열여섯진출력(komento_toimi); 직렬글출력(" FAR="); 직렬열여섯진출력(pätemätön_OSOITE);
    Taulu_Seis(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    postilaatikko_data[0]=32;postilaatikko_data[1]=0;postilaatikko_data[2]=0x10004;postilaatikko_data[3]=8;postilaatikko_data[4]=0;
    postilaatikko_data[5]=postilaatikko_data[6]=postilaatikko_data[7]=0;
    return postilaatikko()&&postilaatikko_data[4]==0x80000008u&&(postilaatikko_data[5]||postilaatikko_data[6]);
}
int Taulu_absoluuttinen_osoite(unsigned char *OSOITE) {
    postilaatikko_data[0]=32;postilaatikko_data[1]=0;postilaatikko_data[2]=0x10003;postilaatikko_data[3]=8;postilaatikko_data[4]=0;
    postilaatikko_data[5]=postilaatikko_data[6]=postilaatikko_data[7]=0;
    if(!postilaatikko()||(postilaatikko_data[4]&0x80000000u)==0||(postilaatikko_data[4]&0xffff)!=6)return 0;
    const unsigned char *data=(const unsigned char*)&postilaatikko_data[5];unsigned SUM_ARVO=0;
    for(unsigned 순번=0;순번<6;순번++){OSOITE[순번]=data[순번];SUM_ARVO|=data[순번];}return SUM_ARVO&&!(OSOITE[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(TAAJUUS));
    kone_rekisteri(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    kone_rekisteri(범용입출력 + 4) = (kone_rekisteri(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    kone_rekisteri(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. virhe_ARVO 시 config.txt의 48MHz를 사용한다.
    postilaatikko_data[0] = 36; postilaatikko_data[1] = 0; postilaatikko_data[2] = 0x38002; postilaatikko_data[3] = 12;
    postilaatikko_data[4] = 0; postilaatikko_data[5] = 2; postilaatikko_data[6] = 48000000; postilaatikko_data[7] = 0; postilaatikko_data[8] = 0;
    int 시계정상 = postilaatikko();
    uint32_t 속도 = 시계정상 && postilaatikko_data[6] >= 1843200 ? postilaatikko_data[6] : 48000000;
    postilaatikko_data[0]=32; postilaatikko_data[1]=0; postilaatikko_data[2]=0x10005; postilaatikko_data[3]=8; postilaatikko_data[4]=0;
    postilaatikko_data[5]=postilaatikko_data[6]=postilaatikko_data[7]=0;
    if (postilaatikko() && postilaatikko_data[4]==0x80000008u) 팔기억킬로바이트=postilaatikko_data[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    kone_rekisteri(직렬장치 + 0x44) = 0x7ff;
    kone_rekisteri(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    kone_rekisteri(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    kone_rekisteri(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    kone_rekisteri(직렬장치 + 0x38) = 0;
    kone_rekisteri(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
kone_Word Taulu_FTP(kone_Word Toiminto) { return (uint32_t)ftp_control((int)Toiminto); }
kone_Word Taulu_verkko_tila(kone_Word merkintä_ARVO_962f286b, kone_Word INDEKSI) { return lukea_verkko_tila(merkintä_ARVO_962f286b, INDEKSI); }
kone_Word Taulu_verkko_Asetukset(kone_Word Toiminto, kone_Word OSOITE, kone_Word peite_ARVO, kone_Word yhdyskäytävä_ARVO) { return (uint32_t)määrittää_verkko(Toiminto, OSOITE, peite_ARVO, yhdyskäytävä_ARVO); }
kone_Word Taulu_lähettää_vastaus(kone_Word OSOITE, kone_Word tilata_ARVO) { return (uint32_t)alku_vastaus_testi(OSOITE, tilata_ARVO); }
kone_Word Taulu_lukea_vastaus(kone_Word merkintä_ARVO_962f286b) { return (uint32_t)lukea_vastaus_testi(merkintä_ARVO_962f286b); }
kone_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEKSI=0; INDEKSI<32; INDEKSI++) Sulje_verkko(INDEKSI);
    for (unsigned INDEKSI=0; INDEKSI<4; INDEKSI++) Taulu_käyttäjän_ohjausobjekti(32+INDEKSI);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (kone_rekisteri(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    kone_rekisteri(0xfe100020ul)=0x5a000000u | (kone_rekisteri(0xfe100020ul)&~0xfffu) | 0x555;
    kone_rekisteri(0xfe100024ul)=0x5a000000u | 10;
    kone_rekisteri(0xfe10001cul)=0x5a000000u | (kone_rekisteri(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

kone_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 nykyinen_kohde 크기를 읽는다. */
    const uint32_t kysely_ARVO[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(kysely_ARVO)/4; 순번++) postilaatikko_data[순번] = kysely_ARVO[순번];
    if (postilaatikko() && postilaatikko_data[4] == 0x80000008u &&
        postilaatikko_data[5] >= 640 && postilaatikko_data[5] <= 1920 &&
        postilaatikko_data[6] >= 480 && postilaatikko_data[6] <= 1080) {
        요청너비 = postilaatikko_data[5]; 요청높이 = postilaatikko_data[6];
    }
    const uint32_t pyyntö[] = {
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
    for (size_t 순번 = 0; 순번 < sizeof(pyyntö)/4; 순번++) postilaatikko_data[순번] = pyyntö[순번];
    // 위 메시지의 todellinen_data 길이를 käyttö_ARVO: 태그 liitä_merkintä 시 kesto_ARVO 불일치를 방지한다.
    postilaatikko_data[0] = sizeof(pyyntö);
    if (!postilaatikko()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned vastaus_kesto[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (postilaatikko_data[응답들[순번]] != (0x80000000u | vastaus_kesto[순번])) return 0;
    uint32_t Tausta_ARVO = postilaatikko_data[28] & 0x3fffffffu;
    uint32_t Koko = postilaatikko_data[29];
    uint32_t 받은너비 = postilaatikko_data[5], 받은높이 = postilaatikko_data[6], SAATU_HINTA_riviväli = postilaatikko_data[33];
    if (postilaatikko_data[15] != 32 || postilaatikko_data[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        postilaatikko_data[10] < 받은너비 || postilaatikko_data[11] < 받은높이 || postilaatikko_data[23] || postilaatikko_data[24] ||
        !Tausta_ARVO || Tausta_ARVO < 0x1000000 || (Tausta_ARVO & 3) || SAATU_HINTA_riviväli < 받은너비 * 4 || (SAATU_HINTA_riviväli & 3) ||
        (uint64_t)SAATU_HINTA_riviväli * 받은높이 > Koko || (uint64_t)Tausta_ARVO + Koko > 0x40000000u)
        return 0;
    Taulu_Valmistele_piirustus((volatile uint32_t *)(uintptr_t)Tausta_ARVO, 받은너비, 받은높이, SAATU_HINTA_riviväli);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 säie_ARVO. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } konteksti;
static konteksti 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int tietojärjestelmät_Juoksu[3] = {1, 0, 0};
static int nykyinen_tehtävä;
extern void kontekstin_vaihto(konteksti *, konteksti *);
extern void 자바작업(int32_t);
kone_Word Taulu_TUOTTO(void) {
    network_poll();
    int Edellinen_kohde = nykyinen_tehtävä, Seuraava_kohde = (Edellinen_kohde + 1) % 3;
    while (Seuraava_kohde != Edellinen_kohde && !tietojärjestelmät_Juoksu[Seuraava_kohde]) Seuraava_kohde = (Seuraava_kohde + 1) % 3;
    if (Seuraava_kohde != Edellinen_kohde) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (tietojärjestelmät_Juoksu[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        nykyinen_tehtävä = Seuraava_kohde;
        kontekstin_vaihto(&작업문맥들[Edellinen_kohde], &작업문맥들[Seuraava_kohde]);
    }
    return 0;
}
static void tehtävä_käynnistys(void) {
    자바작업(nykyinen_tehtävä);
    tietojärjestelmät_Juoksu[nykyinen_tehtävä] = 0;
    Taulu_TUOTTO();
    커널중단("finished task resumed");
}
kone_Word Taulu_tehtävä_Luo(kone_Word tunniste_ARVO) {
    if (tunniste_ARVO < 1 || tunniste_ARVO > 2 || tietojärjestelmät_Juoksu[tunniste_ARVO]) return (uint32_t)-1;
    memset(&작업문맥들[tunniste_ARVO], 0, sizeof(konteksti));
    *(uint64_t *)쌓임공간들[tunniste_ARVO - 1] = 0x6b6f726f7373746bull;
    작업문맥들[tunniste_ARVO].저장값[11] = (uintptr_t)tehtävä_käynnistys;
    작업문맥들[tunniste_ARVO].저장값[12] = (uintptr_t)(쌓임공간들[tunniste_ARVO - 1] + sizeof(쌓임공간들[0]));
    tietojärjestelmät_Juoksu[tunniste_ARVO] = 1;
    return 0;
}
kone_Word Taulu_tehtävä_Tila(kone_Word tunniste_ARVO) { return tunniste_ARVO < 3 ? tietojärjestelmät_Juoksu[tunniste_ARVO] : (uint32_t)-1; }
extern kone_Word AOT_Muisti_HAKU(kone_Word);
extern uint32_t lukea_käyttäjä_Tila(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
kone_Word Taulu_kysely_Järjestelmä(kone_Word merkintä_ARVO_962f286b, kone_Word INDEKSI) {
    if (merkintä_ARVO_962f286b==0) return 팔기억킬로바이트;
    if (merkintä_ARVO_962f286b==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (merkintä_ARVO_962f286b==2 || merkintä_ARVO_962f286b==3) return AOT_Muisti_HAKU(merkintä_ARVO_962f286b==3);
    if (merkintä_ARVO_962f286b==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (merkintä_ARVO_962f286b==5) return 80*1024; /* Suorita_komento OSOITE_alue 16 MiB + 네 세션 보관 OSOITE_alue. */
    if (merkintä_ARVO_962f286b>=20) return lukea_käyttäjä_Tila(merkintä_ARVO_962f286b-20, INDEKSI);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[nykyinen_tehtävä]; }
