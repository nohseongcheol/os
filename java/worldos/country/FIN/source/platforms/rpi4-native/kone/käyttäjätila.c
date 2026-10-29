#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 Suorita_komento kone kerros_ARVO_e65604ef. tiedoston_nimi data/정책은 기존 AOT Java 커널에 위임한다.
#include "käyttäjätila.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../verkko_Pino/verkko_Pino.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define kone_rekisteri(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_jakelija 0xff841000ul
#define IRQ_suoritin_liittymä 0xff842000ul
#define sivukoko 4096ul
#define pääsy_merkintä (1ul << 10)
#define ei_Suorita_lupa (1ul << 53)
#define käyttäjä_ei_Suorita (1ul << 54)
#define normaali_Muisti ((1ul << 2) | (3ul << 8) | pääsy_merkintä)
#define ydin_page (3ul | normaali_Muisti | ei_Suorita_lupa | käyttäjä_ei_Suorita)
#define käyttäjä_luku_ja_kirjoitus (3ul | normaali_Muisti | (1ul << 6) | ei_Suorita_lupa | käyttäjä_ei_Suorita)
#define käyttäjä_vain_luku (3ul | normaali_Muisti | (3ul << 6) | ei_Suorita_lupa | käyttäjä_ei_Suorita)
#define käyttäjä_lukea_Suorita (3ul | normaali_Muisti | (3ul << 6) | ei_Suorita_lupa)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t Taulu_kuvapiste(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t Taulu_Pääte(uintptr_t);
extern int Pääte_Odottaa(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int käyttäjä_jatka(käyttäjä_kuva *,void *);
extern void 사용자실수보관(void *);
extern int käyttäjä_anna(uintptr_t aloituskohta, uintptr_t pinomuisti, uintptr_t 전달값);
extern void käyttäjä_palauttaa(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t juuri_OSOITE[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t page_luettelo[käyttäjä_page_LASKE] __attribute__((aligned(4096)));
static uint8_t oikeudet_luettelo[käyttäjä_page_LASKE];
static int Aktiivinen, tiedostoluettelo[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int Sulje_vastake_päätepiste(unsigned Tiedosto_kahva){return Tiedosto_kahva<40?자바전문닫기(Tiedosto_kahva):자바흐름닫기(Tiedosto_kahva);}
static uint64_t TAAJUUS, määräaika_AIKA;
static uintptr_t keko_lopettaa_puhelu;
// ydin_ARVO 셸이 준비한 UTF-8 argumentit. EL0에는 kopioida_ARVO 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,vuorovaikutteinen,리눅스규약,tiedostoluettelo[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char argumentti_MATRIISI[8][256],oikeudet_luettelo[käyttäjä_page_LASKE];
    uintptr_t dynaaminen_muisti; käyttäjä_kuva suoritus_kuva;
    unsigned char liukuluku_Tila[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int omistaja_objekti,vuorovaikutteinen;
static uint32_t käyttäjänumero[4], käyttäjä_alku_AIKA[4], 사용자누적시각[4], käyttäjä_suoritus_AIKA[4], Seuraava_käyttäjänumero=10;
static unsigned char käyttäjä_komento_nimi[4][288];
uint32_t lukea_käyttäjä_Tila(unsigned merkintä_ARVO_962f286b, unsigned INDEKSI) {
    unsigned sijainti=INDEKSI&3;
    int Tila_ARVO=(Aktiivinen && omistaja_objekti==(int)sijainti) ? 1 : 저장값[sijainti].멈춤상태 ? 2 : 0;
    if (merkintä_ARVO_962f286b==0) return Tila_ARVO;
    if (!Tila_ARVO) return 0;
    if (merkintä_ARVO_962f286b==1) return käyttäjänumero[sijainti];
    if (merkintä_ARVO_962f286b==2) {
        unsigned char *쪽들=Tila_ARVO==1?oikeudet_luettelo:저장값[sijainti].oikeudet_luettelo;
        unsigned page_LASKE=0; for (unsigned 순번=0; 순번<käyttäjä_page_LASKE; 순번++) if(쪽들[순번]) page_LASKE++;
        return page_LASKE*4;
    }
    if (merkintä_ARVO_962f286b==3) return (uint32_t)보드밀리초()-käyttäjä_alku_AIKA[sijainti];
    if (merkintä_ARVO_962f286b==4) return 사용자누적시각[sijainti]+(Tila_ARVO==1?(uint32_t)보드밀리초()-käyttäjä_suoritus_AIKA[sijainti]:0);
    if (merkintä_ARVO_962f286b==5) return INDEKSI/4<sizeof(käyttäjä_komento_nimi[0])?käyttäjä_komento_nimi[sijainti][INDEKSI/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t merkintä_LASKE) {
    if (Aktiivinen || merkintä_LASKE > 8) return (uint32_t)-22;
    전달인수개수 = merkintä_LASKE;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t HAKU_INDEKSI, uintptr_t nykyinen_toimi, uintptr_t tavu_data) {
    if (Aktiivinen || HAKU_INDEKSI >= 전달인수개수 || nykyinen_toimi >= 255 || nykyinen_toimi != 전달인수길이[HAKU_INDEKSI] || !tavu_data || tavu_data > 255)
        return (uint32_t)-22;
    전달인수[HAKU_INDEKSI][nykyinen_toimi] = tavu_data;
    전달인수길이[HAKU_INDEKSI] = nykyinen_toimi + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Kello_ARVO(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Seis_AIKAKATKAISU(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    kone_rekisteri(IRQ_jakelija + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void alku_AIKAKATKAISU(void) {
    uint64_t 간격 = TAAJUUS * 2, ota_käyttöön = 1;
    määräaika_AIKA = Kello_ARVO() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(ota_käyttöön) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned tietolohko = 0; tietolohko < 4; tietolohko++) {
        juuri_OSOITE[tietolohko] = (uintptr_t)가운데[tietolohko] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t OSOITE = ((uintptr_t)tietolohko << 30) | ((uintptr_t)순번 << 21);
            가운데[tietolohko][순번] = OSOITE | 1 | pääsy_merkintä | käyttäjä_ei_Suorita;
            if (OSOITE >= 0xfc000000ul) 가운데[tietolohko][순번] |= ei_Suorita_lupa; // Device-nGnRnE
            else 가운데[tietolohko][순번] |= normaali_Muisti; // Normal, non-cacheable
        }
    }
    for (unsigned SEKUNNIT_ARVO = 0; SEKUNNIT_ARVO < käyttäjä_page_LASKE / 512; SEKUNNIT_ARVO++)
        가운데[0][(käyttäjä_PERUS >> 21) + SEKUNNIT_ARVO] = (uintptr_t)(page_luettelo + SEKUNNIT_ARVO * 512) | 3;
    for (unsigned 순번 = 0; 순번 < käyttäjä_page_LASKE; 순번++) page_luettelo[순번] = (käyttäjä_PERUS + 순번 * sivukoko) | ydin_page;
    uint64_t Muisti_määrite_rekisteri = 0x4400, OSOITE_Käännös_ohjain = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Muisti_määrite_rekisteri), "r"(OSOITE_Käännös_ohjain), "r"((uintptr_t)juuri_OSOITE) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t liukuluku_Tila = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(liukuluku_Tila) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(TAAJUUS));
    Seis_AIKAKATKAISU();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 aloituskohta_ARVO 때만 Salli_ARVO.
    kone_rekisteri(IRQ_jakelija) = 0;
    kone_rekisteri(IRQ_jakelija + 0x180) = 0xffffffff;
    kone_rekisteri(IRQ_jakelija + 0x80) = 0xffffffff;
    kone_rekisteri(IRQ_jakelija + 0x280) = 1u << 30;
    kone_rekisteri(IRQ_jakelija + 0x41c) = 0x80808080;
    kone_rekisteri(IRQ_jakelija + 0x100) = 1u << 30;
    kone_rekisteri(IRQ_suoritin_liittymä + 4) = 0xff;
    kone_rekisteri(IRQ_suoritin_liittymä + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 tietojärjestelmät_normaali 확인할 numero 있다.
    int suojaus = (kone_rekisteri(IRQ_jakelija + 4) & (1u << 10)) != 0;
    kone_rekisteri(IRQ_jakelija) = suojaus ? 1 : 3;
    kone_rekisteri(IRQ_suoritin_liittymä) = suojaus ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t TYYPPI_alue, kone_TYYPPI; uint32_t versionumero;
    uint64_t aloituskohta, ohjelma_otsikko_SIIRTYMÄ, osan_otsikko_SIIRTYMÄ; uint32_t määritys_Background_Intelligent_Transfer_Service;
    uint16_t suoritettava_tiedosto_otsikko_muuttaa_kokoa, ohjelma_otsikko_merkintä_muuttaa_kokoa, ohjelma_otsikko_LASKE, osan_otsikko_merkintä_muuttaa_kokoa, osan_otsikko_LASKE, osa_nimi_taulukko_INDEKSI;
} 실행파일머리;
typedef struct { uint32_t TYYPPI_alue, määritys_Background_Intelligent_Transfer_Service; uint64_t SIIRTYMÄ_ARVO, OSOITE, 물리주소, 파일영역크기, 기억영역크기, tasaa_rajattu_alue; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(käyttäjä_kuva) == 272, "exception assembly layout");
static int 포함된범위(uint64_t SIIRTYMÄ_ARVO, uint64_t Koko, uint64_t lopettaa_puhelu_SIIRTYMÄ) {
    return SIIRTYMÄ_ARVO <= lopettaa_puhelu_SIIRTYMÄ && Koko <= lopettaa_puhelu_SIIRTYMÄ - SIIRTYMÄ_ARVO;
}
static int 부가정보검사(const unsigned char *data_toimi, size_t Koko) {
    size_t nykyinen_toimi = 0;
    while (포함된범위(nykyinen_toimi, 12, Koko)) {
        uint32_t 낱말들[3]; memcpy(낱말들, data_toimi + nykyinen_toimi, 12); nykyinen_toimi += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(nykyinen_toimi, 이름영역크기, Koko) || !포함된범위(nykyinen_toimi + 이름영역크기, 설명크기, Koko)) return 0;
        const unsigned char Nimi[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Nimi) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Nimi); 순번++) if (data_toimi[nykyinen_toimi + 순번] != Nimi[순번]) 일치 = 0;
        uint32_t versionumero = 0;
        if (일치) memcpy(&versionumero, data_toimi + nykyinen_toimi + 이름영역크기, 4);
        if (일치 && versionumero == 1) return 1;
        nykyinen_toimi += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *data, size_t Koko, int 리눅스방식) {
    if (Koko < sizeof(실행파일머리)) return käyttäjä_suoritettava_tiedosto_virhe;
    실행파일머리 suoritettava_tiedosto_otsikko; memcpy(&suoritettava_tiedosto_otsikko, data, sizeof(suoritettava_tiedosto_otsikko));
    if (suoritettava_tiedosto_otsikko.형식식별[0] != 127 || suoritettava_tiedosto_otsikko.형식식별[1] != 'E' || suoritettava_tiedosto_otsikko.형식식별[2] != 'L' || suoritettava_tiedosto_otsikko.형식식별[3] != 'F' ||
        suoritettava_tiedosto_otsikko.형식식별[4] != 2 || suoritettava_tiedosto_otsikko.형식식별[5] != 1 || suoritettava_tiedosto_otsikko.형식식별[6] != 1 || (suoritettava_tiedosto_otsikko.형식식별[7] != 0 && (!리눅스방식 || suoritettava_tiedosto_otsikko.형식식별[7] != 3)) ||
        suoritettava_tiedosto_otsikko.TYYPPI_alue != 2 || suoritettava_tiedosto_otsikko.kone_TYYPPI != 183 || suoritettava_tiedosto_otsikko.versionumero != 1 || suoritettava_tiedosto_otsikko.määritys_Background_Intelligent_Transfer_Service || suoritettava_tiedosto_otsikko.suoritettava_tiedosto_otsikko_muuttaa_kokoa != sizeof(suoritettava_tiedosto_otsikko) ||
        suoritettava_tiedosto_otsikko.ohjelma_otsikko_merkintä_muuttaa_kokoa != sizeof(실행파일구획) || !suoritettava_tiedosto_otsikko.ohjelma_otsikko_LASKE || suoritettava_tiedosto_otsikko.ohjelma_otsikko_LASKE > 16 ||
        suoritettava_tiedosto_otsikko.ohjelma_otsikko_SIIRTYMÄ < sizeof(suoritettava_tiedosto_otsikko) || !포함된범위(suoritettava_tiedosto_otsikko.ohjelma_otsikko_SIIRTYMÄ, (uint64_t)suoritettava_tiedosto_otsikko.ohjelma_otsikko_LASKE * sizeof(실행파일구획), Koko)) return käyttäjä_suoritettava_tiedosto_virhe;
    uint8_t 사용량[(käyttäjä_KUVA_lopettaa_puhelu - käyttäjä_PERUS) / sivukoko] = {0};
    int kelvollinen_aloituskohta = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < suoritettava_tiedosto_otsikko.ohjelma_otsikko_LASKE; 순번++) {
        실행파일구획 data_toimi; memcpy(&data_toimi, data + suoritettava_tiedosto_otsikko.ohjelma_otsikko_SIIRTYMÄ + 순번 * sizeof(data_toimi), sizeof(data_toimi));
        if (data_toimi.TYYPPI_alue == 4) {
            if (!포함된범위(data_toimi.SIIRTYMÄ_ARVO, data_toimi.파일영역크기, Koko)) return käyttäjä_suoritettava_tiedosto_virhe;
            if (부가정보검사(data + data_toimi.SIIRTYMÄ_ARVO, data_toimi.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (data_toimi.TYYPPI_alue == 0 || data_toimi.TYYPPI_alue == 6 || (data_toimi.TYYPPI_alue == 0x6474e551 && !(data_toimi.määritys_Background_Intelligent_Transfer_Service & 1))) continue;
        if (data_toimi.TYYPPI_alue != 1) return käyttäjä_suoritettava_tiedosto_virhe; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!data_toimi.기억영역크기) continue;
        if (data_toimi.määritys_Background_Intelligent_Transfer_Service & ~7u || !(data_toimi.määritys_Background_Intelligent_Transfer_Service & 4) || (data_toimi.määritys_Background_Intelligent_Transfer_Service & 3) == 3 || data_toimi.파일영역크기 > data_toimi.기억영역크기 ||
            (data_toimi.파일영역크기 && !포함된범위(data_toimi.SIIRTYMÄ_ARVO, data_toimi.파일영역크기, Koko)) || data_toimi.OSOITE < käyttäjä_PERUS ||
            !포함된범위(data_toimi.OSOITE, data_toimi.기억영역크기, käyttäjä_KUVA_lopettaa_puhelu) ||
            (!리눅스방식 && ((data_toimi.OSOITE & (sivukoko - 1)) || (data_toimi.SIIRTYMÄ_ARVO & (sivukoko - 1)) || data_toimi.tasaa_rajattu_alue != sivukoko)) ||
            (리눅스방식 && (((data_toimi.OSOITE ^ data_toimi.SIIRTYMÄ_ARVO) & (sivukoko - 1)) || !data_toimi.tasaa_rajattu_alue ||
                (data_toimi.tasaa_rajattu_alue & (data_toimi.tasaa_rajattu_alue - 1)) || data_toimi.tasaa_rajattu_alue > 0x200000 || ((data_toimi.OSOITE ^ data_toimi.SIIRTYMÄ_ARVO) & (data_toimi.tasaa_rajattu_alue - 1))))) return käyttäjä_suoritettava_tiedosto_virhe;
        unsigned 첫항목 = (data_toimi.OSOITE - käyttäjä_PERUS) / sivukoko;
        unsigned merkintä_LASKE = ((data_toimi.OSOITE & (sivukoko - 1)) + data_toimi.기억영역크기 + sivukoko - 1) / sivukoko;
        for (unsigned page_ARVO = 첫항목; page_ARVO < 첫항목 + merkintä_LASKE; page_ARVO++) {
            if (사용량[page_ARVO]) return käyttäjä_suoritettava_tiedosto_virhe;
            사용량[page_ARVO] = 1;
        }
        if ((data_toimi.määritys_Background_Intelligent_Transfer_Service & 1) && suoritettava_tiedosto_otsikko.aloituskohta >= data_toimi.OSOITE && suoritettava_tiedosto_otsikko.aloituskohta < data_toimi.OSOITE + data_toimi.파일영역크기 && !(suoritettava_tiedosto_otsikko.aloituskohta & 3)) kelvollinen_aloituskohta = 1;
        적재구획++;
    }
    return kelvollinen_aloituskohta && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : käyttäjä_suoritettava_tiedosto_virhe;
}
int 사용자실행파일검사(const unsigned char *data, size_t Koko) { return 실행파일검사(data, Koko, 0); }
static void sivun_asettelu(uintptr_t OSOITE, uint64_t määritys_Background_Intelligent_Transfer_Service, unsigned oikeudet) {
    unsigned HAKU_INDEKSI = (OSOITE - käyttäjä_PERUS) / sivukoko;
    page_luettelo[HAKU_INDEKSI] = OSOITE | määritys_Background_Intelligent_Transfer_Service;
    oikeudet_luettelo[HAKU_INDEKSI] = oikeudet;
}
static int käyttäjä_alue(uintptr_t OSOITE, size_t merkintä_LASKE, int 쓰는중) {
    if (OSOITE < käyttäjä_PERUS || !포함된범위(OSOITE, merkintä_LASKE, käyttäjä_lopettaa_puhelu)) return 0;
    if (!merkintä_LASKE) return 1;
    unsigned 첫항목 = (OSOITE - käyttäjä_PERUS) / sivukoko, 마지막 = (OSOITE + merkintä_LASKE - 1 - käyttäjä_PERUS) / sivukoko;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(oikeudet_luettelo[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int kopioida_polku(uintptr_t OSOITE, char *polku_2) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!käyttäjä_alue(OSOITE, 1, 0)) return -14;
        polku_2[순번] = *(const char *)OSOITE++;
        if (!polku_2[순번]) return 0;
    }
    return -36;
}
static intptr_t ydin_KR(intptr_t TULOS) { return TULOS < 0 ? -virhenumero : TULOS; }
static int 대응파일기술자(uint64_t Tiedosto_kahva) { return Tiedosto_kahva >= 3 && Tiedosto_kahva < 19 ? tiedostoluettelo[Tiedosto_kahva - 3] : -1; }
static int vastake_päätepiste_omistaja(uint64_t Tiedosto_kahva) { return Tiedosto_kahva >= 32 && Tiedosto_kahva < 56 && 통신끝점들[Tiedosto_kahva - 32]; }
static int OSOITE_syöte(uintptr_t 가리킴값, size_t kesto_ARVO, struct pk_sockaddr_in *OSOITE) {
    if (kesto_ARVO != sizeof(*OSOITE)) return -22;
    if (!käyttäjä_alue(가리킴값, kesto_ARVO, 0)) return -14;
    memcpy(OSOITE, (const void *)가리킴값, sizeof(*OSOITE));
    return OSOITE->sin_family == AF_INET ? 0 : -97;
}
static int OSOITE_tulos_sekki(uintptr_t 가리킴값, uintptr_t kesto_osoitin, pk_socklen_t *puskuri_kapasiteetti) {
    if (!käyttäjä_alue(kesto_osoitin, sizeof(*puskuri_kapasiteetti), 1)) return -14;
    memcpy(puskuri_kapasiteetti, (const void *)kesto_osoitin, sizeof(*puskuri_kapasiteetti));
    if (*puskuri_kapasiteetti > sizeof(struct pk_sockaddr_in)) *puskuri_kapasiteetti = sizeof(struct pk_sockaddr_in);
    if (*puskuri_kapasiteetti && !käyttäjä_alue(가리킴값, *puskuri_kapasiteetti, 1)) return -14;
    return 0;
}
static void OSOITE_tulos(uintptr_t 가리킴값, uintptr_t kesto_osoitin, pk_socklen_t puskuri_kapasiteetti, int OSOITE, int portin_numero) {
    struct pk_sockaddr_in ARVO; memset(&ARVO, 0, sizeof(ARVO));
    ARVO.sin_family = AF_INET; ARVO.sin_port = pk_htons(portin_numero); ARVO.sin_addr.s_addr = pk_htonl(OSOITE);
    if (puskuri_kapasiteetti) memcpy((void *)가리킴값, &ARVO, puskuri_kapasiteetti);
    pk_socklen_t kesto_ARVO = sizeof(ARVO); memcpy((void *)kesto_osoitin, &kesto_ARVO, sizeof(kesto_ARVO));
}
extern uintptr_t Taulu_Media(uintptr_t, uintptr_t);
static intptr_t alkuperäinen_Järjestelmä_KUTSU(käyttäjä_kuva *Tiedosto_merkintä) {
    uintptr_t 첫째값 = Tiedosto_merkintä->rekisteri_data[0], SEKUNNIT_ARVO = Tiedosto_merkintä->rekisteri_data[1], merkkikoodi = Tiedosto_merkintä->rekisteri_data[2];
    char polku_2[65];
    int Tiedosto_kahva, TULOS;
    switch (Tiedosto_merkintä->rekisteri_data[8]) {
    case 0: return 1; // oma ABI 버전
    case 1: // write: osoitin 전체를 검사한 BACK_ARVO tulostuspaikka/tiedoston_nimi muuttaa_ARVO
        if (merkkikoodi > 65536) return -22;
        if (!käyttäjä_alue(SEKUNNIT_ARVO, merkkikoodi, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t alku_tulos=Kello_ARVO();
            for (size_t 순번 = 0; 순번 < merkkikoodi; 순번++) Taulu_Media(첫째값, ((const unsigned char *)SEKUNNIT_ARVO)[순번]);
            /* 큰 tty를 그린 ydin_ARVO 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(vuorovaikutteinen){
                määräaika_AIKA+=Kello_ARVO()-alku_tulos;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(määräaika_AIKA) : "memory");
            }
            return merkkikoodi;
        }
        if(첫째값>=40&&vastake_päätepiste_omistaja(첫째값)){
            size_t kohde_LASKE=merkkikoodi>512?512:merkkikoodi;for(size_t 순번=0;순번<kohde_LASKE;순번++)자바전문넣기(순번,((const unsigned char *)SEKUNNIT_ARVO)[순번]);return 자바흐름쓰기(첫째값,kohde_LASKE);
        }
        Tiedosto_kahva = 대응파일기술자(첫째값); if (Tiedosto_kahva < 0) return -9;
        return ydin_KR(pk_write(Tiedosto_kahva, (const void *)SEKUNNIT_ARVO, merkkikoodi));
    case 2:
        if (merkkikoodi > 65536) return -22;
        if (!käyttäjä_alue(SEKUNNIT_ARVO, merkkikoodi, 1)) return -14;
        if (첫째값 == 0) {
            size_t kohde_LASKE = 0;
            while (kohde_LASKE < merkkikoodi) {
                int merkki_ARVO = (int32_t)보드글자읽기(); if (merkki_ARVO == -2) return kohde_LASKE; if (merkki_ARVO < 0) break;
                ((unsigned char *)SEKUNNIT_ARVO)[kohde_LASKE++] = merkki_ARVO;
            }
            return kohde_LASKE ? (intptr_t)kohde_LASKE : (merkkikoodi ? -11 : 0);
        }
        if(첫째값>=40&&vastake_päätepiste_omistaja(첫째값)){
            TULOS=자바흐름읽기(첫째값,merkkikoodi>512?512:merkkikoodi);if(TULOS>0)for(int 순번=0;순번<TULOS;순번++)((unsigned char *)SEKUNNIT_ARVO)[순번]=자바전문얻기(순번);return TULOS;
        }
        Tiedosto_kahva = 대응파일기술자(첫째값); if (Tiedosto_kahva < 0) return -9;
        return ydin_KR(pk_read(Tiedosto_kahva, (void *)SEKUNNIT_ARVO, merkkikoodi));
    case 3:
        TULOS = kopioida_polku(첫째값, polku_2); if (TULOS) return TULOS;
        if (SEKUNNIT_ARVO > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (tiedostoluettelo[순번] < 0) {
            Tiedosto_kahva = pk_open(polku_2, (int)SEKUNNIT_ARVO, 0600);
            if (Tiedosto_kahva < 0) return -virhenumero;
            tiedostoluettelo[순번] = Tiedosto_kahva; return 순번 + 3;
        }
        return -24;
    case 4:
        if (vastake_päätepiste_omistaja(첫째값)) { TULOS = Sulje_vastake_päätepiste(첫째값); if (!TULOS) 통신끝점들[첫째값 - 32] = 0; return TULOS; }
        Tiedosto_kahva = 대응파일기술자(첫째값); if (Tiedosto_kahva < 0) return -9;
        TULOS = pk_close(Tiedosto_kahva); if (!TULOS) tiedostoluettelo[첫째값 - 3] = -1;
        return ydin_KR(TULOS);
    case 5:
        Tiedosto_kahva = 대응파일기술자(첫째값); if (Tiedosto_kahva < 0) return -9;
        if (merkkikoodi > 2) return -22;
        return ydin_KR(pk_lseek(Tiedosto_kahva, (int64_t)SEKUNNIT_ARVO, merkkikoodi));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 käyttäjätila RW/NX keko_ARVO, 새로 노출되는 페이지는 0으로 alustaa
        if (!첫째값) return keko_lopettaa_puhelu;
        if (첫째값 < käyttäjä_KUVA_lopettaa_puhelu || 첫째값 > käyttäjä_keko_lopettaa_puhelu) return -12;
        uintptr_t 이전쪽들 = (keko_lopettaa_puhelu + sivukoko - 1) & ~(sivukoko - 1);
        uintptr_t 새쪽들 = (첫째값 + sivukoko - 1) & ~(sivukoko - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t data_toimi = 이전쪽들; data_toimi < 새쪽들; data_toimi += sivukoko) sivun_asettelu(data_toimi, ydin_page, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t data_toimi = 이전쪽들; data_toimi < 새쪽들; data_toimi += sivukoko) sivun_asettelu(data_toimi, käyttäjä_luku_ja_kirjoitus, 3);
        } else {
            for (uintptr_t data_toimi = 새쪽들; data_toimi < 이전쪽들; data_toimi += sivukoko) {
                page_luettelo[(data_toimi - käyttäjä_PERUS) / sivukoko] = 0; oikeudet_luettelo[(data_toimi - käyttäjä_PERUS) / sivukoko] = 0;
            }
        }
        keko_lopettaa_puhelu = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        Tiedosto_kahva = 대응파일기술자(첫째값); return Tiedosto_kahva < 0 ? -9 : ydin_KR(pk_size(Tiedosto_kahva));
    case 10:
        Tiedosto_kahva = 대응파일기술자(첫째값); return Tiedosto_kahva < 0 ? -9 : ydin_KR(pk_ftruncate(Tiedosto_kahva, (int64_t)SEKUNNIT_ARVO));
    case 11:
        TULOS = kopioida_polku(첫째값, polku_2); return TULOS ? TULOS : ydin_KR(pk_unlink(polku_2));
    case 12:
        Tiedosto_kahva = 대응파일기술자(첫째값); return Tiedosto_kahva < 0 ? -9 : ydin_KR(pk_fsync(Tiedosto_kahva));
    case 13: { // 그래픽 기초 API: käyttäjätila 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = Tiedosto_merkintä->rekisteri_data[3], 높이값 = Tiedosto_merkintä->rekisteri_data[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SEKUNNIT_ARVO > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - SEKUNNIT_ARVO) return -22;
        for (uintptr_t Y_koordinaatti = SEKUNNIT_ARVO; Y_koordinaatti < SEKUNNIT_ARVO + 높이값; Y_koordinaatti++) for (uintptr_t x_koordinaatti = 첫째값; x_koordinaatti < 첫째값 + 너비값; x_koordinaatti++) Taulu_kuvapiste(x_koordinaatti, Y_koordinaatti, merkkikoodi);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=kohde_LASKE; args(index,buffer,capacity)=UTF-8 kesto_ARVO
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (merkkikoodi <= 전달인수길이[첫째값]) return -36;
        if (!käyttäjä_alue(SEKUNNIT_ARVO, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SEKUNNIT_ARVO, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;vuorovaikutteinen=1;return Taulu_Pääte(13);}
        if(첫째값==2){vuorovaikutteinen=0;return 0;}
        if(첫째값==3)return Taulu_Pääte(13);
        if(첫째값!=1||!vuorovaikutteinen)return -22;
        TULOS=(int32_t)보드글자읽기();
        if(TULOS==-4096)return TULOS;
        alku_AIKAKATKAISU();return TULOS<0?-11:TULOS;
    case 17: { // 유한한 협력 odottaa_ARVO: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t lopettaa_puhelu_AIKA = Kello_ARVO() + TAAJUUS * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Kello_ARVO() < lopettaa_puhelu_AIKA);
        alku_AIKAKATKAISU(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 pää_ARVO·빈 폴더를 검사한다.
        if (SEKUNNIT_ARVO > 2) return -22;
        TULOS = kopioida_polku(첫째값, polku_2); if (TULOS) return TULOS;
        unsigned kesto_ARVO = 0; while (polku_2[kesto_ARVO]) kesto_ARVO++;
        TULOS = 자바경로시작(kesto_ARVO); if (TULOS < 0) return TULOS;
        for (unsigned 순번 = 0; 순번 < kesto_ARVO; 순번++) 자바경로바이트(순번, (unsigned char)polku_2[순번]);
        return SEKUNNIT_ARVO == 0 ? 자바항목종류() : SEKUNNIT_ARVO == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int merkki_ARVO=(int32_t)보드글자읽기();if(merkki_ARVO==-4096)return merkki_ARVO;if(merkki_ARVO>=0)화면누름(omistaja_objekti,merkki_ARVO);alku_AIKAKATKAISU();}
        if(첫째값==3&&merkkikoodi){if(!자바셸대화형())return -95;vuorovaikutteinen=1;Taulu_Pääte(300);}
        return 화면호출(omistaja_objekti,첫째값,SEKUNNIT_ARVO,merkkikoodi,Tiedosto_merkintä->rekisteri_data[3],Tiedosto_merkintä->rekisteri_data[4],Tiedosto_merkintä->rekisteri_data[5]);
    case 21:
        if(merkkikoodi>127)return -22;if(!käyttäjä_alue(SEKUNNIT_ARVO,merkkikoodi*sizeof(uint32_t),0))return -14;
        return 화면글(omistaja_objekti,첫째값,(const uint32_t *)SEKUNNIT_ARVO,merkkikoodi);
    case 22: // 화면 Koko kysely_ARVO: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SEKUNNIT_ARVO==SOCK_STREAM&&(merkkikoodi==0||merkkikoodi==6))TULOS=자바흐름만들기();
        else if(SEKUNNIT_ARVO==SOCK_DGRAM&&(merkkikoodi==0||merkkikoodi==IPPROTO_UDP))TULOS=자바전문만들기(첫째값,SEKUNNIT_ARVO,merkkikoodi);
        else return -93;
        if (TULOS >= 32 && TULOS < 56) 통신끝점들[TULOS - 32] = 1;
        return TULOS;
    case 33: {
        if (!vastake_päätepiste_omistaja(첫째값)) return -9;
        struct pk_sockaddr_in OSOITE;
        TULOS = OSOITE_syöte(SEKUNNIT_ARVO, merkkikoodi, &OSOITE); if (TULOS) return TULOS;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(OSOITE.sin_addr.s_addr),pk_htons(OSOITE.sin_port)):자바전문묶기(첫째값, pk_htonl(OSOITE.sin_addr.s_addr), pk_htons(OSOITE.sin_port));
    }
    case 34: {
        if (!vastake_päätepiste_omistaja(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Tiedosto_merkintä->rekisteri_data[3]) return -95;
        if (merkkikoodi > 512) return -90;
        if (merkkikoodi && !käyttäjä_alue(SEKUNNIT_ARVO, merkkikoodi, 0)) return -14;
        struct pk_sockaddr_in OSOITE;
        TULOS = OSOITE_syöte(Tiedosto_merkintä->rekisteri_data[4], Tiedosto_merkintä->rekisteri_data[5], &OSOITE); if (TULOS) return TULOS;
        for (unsigned 순번 = 0; 순번 < merkkikoodi; 순번++) 자바전문넣기(순번, ((const unsigned char *)SEKUNNIT_ARVO)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(OSOITE.sin_addr.s_addr), pk_htons(OSOITE.sin_port), merkkikoodi);
    }
    case 35: {
        if (!vastake_päätepiste_omistaja(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Tiedosto_merkintä->rekisteri_data[3]) return -95;
        if (merkkikoodi > 512) return -90;
        if (merkkikoodi && !käyttäjä_alue(SEKUNNIT_ARVO, merkkikoodi, 1)) return -14;
        pk_socklen_t puskuri_kapasiteetti = 0;
        if (Tiedosto_merkintä->rekisteri_data[4]) { TULOS = OSOITE_tulos_sekki(Tiedosto_merkintä->rekisteri_data[4], Tiedosto_merkintä->rekisteri_data[5], &puskuri_kapasiteetti); if (TULOS) return TULOS; }
        TULOS = 자바전문받기(첫째값, merkkikoodi); if (TULOS < 0) return TULOS;
        for (int 순번 = 0; 순번 < TULOS; 순번++) ((unsigned char *)SEKUNNIT_ARVO)[순번] = 자바전문얻기(순번);
        if (Tiedosto_merkintä->rekisteri_data[4]) OSOITE_tulos(Tiedosto_merkintä->rekisteri_data[4], Tiedosto_merkintä->rekisteri_data[5], puskuri_kapasiteetti, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return TULOS;
    }
    case 36: {
        if (!vastake_päätepiste_omistaja(첫째값)) return -9;
        pk_socklen_t puskuri_kapasiteetti;
        TULOS = OSOITE_tulos_sekki(SEKUNNIT_ARVO, merkkikoodi, &puskuri_kapasiteetti); if (TULOS) return TULOS;
        OSOITE_tulos(SEKUNNIT_ARVO,merkkikoodi,puskuri_kapasiteetti,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!vastake_päätepiste_omistaja(첫째값))return -9;struct pk_sockaddr_in OSOITE;
        TULOS=OSOITE_syöte(SEKUNNIT_ARVO,merkkikoodi,&OSOITE);if(TULOS)return TULOS;
        return 자바흐름연결(첫째값,pk_htonl(OSOITE.sin_addr.s_addr),pk_htons(OSOITE.sin_port));
    }
    case 38: return 첫째값>=40&&vastake_päätepiste_omistaja(첫째값)?자바흐름듣기(첫째값,SEKUNNIT_ARVO):-9;
    case 39:
        if(첫째값<40||!vastake_päätepiste_omistaja(첫째값))return -9;
        if(SEKUNNIT_ARVO||merkkikoodi)return -95;TULOS=자바흐름연결받기(첫째값);if(TULOS>=40&&TULOS<56)통신끝점들[TULOS-32]=1;return TULOS;
    case 40: return 첫째값>=40&&vastake_päätepiste_omistaja(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t järjestelmäkutsu(käyttäjä_kuva *Tiedosto_merkintä) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(Tiedosto_merkintä) : alkuperäinen_Järjestelmä_KUTSU(Tiedosto_merkintä);
}
static void palauttaa_ydin(käyttäjä_kuva *Tiedosto_merkintä, int TULOS) {
    Seis_AIKAKATKAISU();
    Tiedosto_merkintä->rekisteri_data[0] = (uint64_t)(int64_t)TULOS;
    Tiedosto_merkintä->komento_toimi = (uintptr_t)käyttäjä_palauttaa;
    Tiedosto_merkintä->Tila_KOODI = 0x3c5; // EL1h, DAIF masked
}
int käyttäjäpoikkeus(käyttäjä_kuva *Tiedosto_merkintä, unsigned LEIKKAUSPISTE) {
    if (!Aktiivinen || (Tiedosto_merkintä->Tila_KOODI & 15) != 0) return 0;
    if (LEIKKAUSPISTE) {
        uint32_t hyväksyntä_ARVO = kone_rekisteri(IRQ_suoritin_liittymä + 0xc), tunniste_ARVO = hyväksyntä_ARVO & 1023;
        if (tunniste_ARVO == 30) { palauttaa_ydin(Tiedosto_merkintä, käyttäjä_AIKAKATKAISU); kone_rekisteri(IRQ_suoritin_liittymä + 0x10) = hyväksyntä_ARVO; return 1; }
        if (tunniste_ARVO < 1020) kone_rekisteri(IRQ_suoritin_liittymä + 0x10) = hyväksyntä_ARVO;
        return 1;
    }
    uint64_t poikkeus_Tila; __asm__ volatile("mrs %0, esr_el1" : "=r"(poikkeus_Tila));
    if (Kello_ARVO() >= määräaika_AIKA) { palauttaa_ydin(Tiedosto_merkintä, käyttäjä_AIKAKATKAISU); return 1; }
    unsigned poikkeus_alue = poikkeus_Tila >> 26;
    if (poikkeus_alue == 0x15 && (poikkeus_Tila & 0xffff) == 0) {
        if (리눅스규약 ? Tiedosto_merkintä->rekisteri_data[8] == 93 || Tiedosto_merkintä->rekisteri_data[8] == 94 : Tiedosto_merkintä->rekisteri_data[8] == 6) palauttaa_ydin(Tiedosto_merkintä, (int)(Tiedosto_merkintä->rekisteri_data[0] & 255));
        else {
            intptr_t TULOS=järjestelmäkutsu(Tiedosto_merkintä);
            if(TULOS==-4096&&vuorovaikutteinen){
                저장값[omistaja_objekti].suoritus_kuva=*Tiedosto_merkintä;저장값[omistaja_objekti].suoritus_kuva.komento_toimi-=4;
                사용자실수보관(저장값[omistaja_objekti].liukuluku_Tila);palauttaa_ydin(Tiedosto_merkintä,사용자중단됨);
            }else Tiedosto_merkintä->rekisteri_data[0]=(uint64_t)TULOS;
        }
    } else palauttaa_ydin(Tiedosto_merkintä, poikkeus_alue == 0x24 ? käyttäjä_data_virhe : poikkeus_alue == 0x20 ? käyttäjä_suoritus_virhe : käyttäjä_pätemätön_käsky);
    return 1;
}

// 생성된 const ELF Ryhmä_ARVO: 실행은 반드시 ohjelma_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *data; size_t Koko; unsigned 전달값; } ohjelma;
#include "programs.h"
static void *tilannekuva(unsigned sijainti){return (void *)(0x04000000ul+sijainti*(käyttäjä_lopettaa_puhelu-käyttäjä_PERUS));}
static int loppu_ohjelma(int TULOS){
    사용자누적시각[omistaja_objekti]+=(uint32_t)보드밀리초()-käyttäjä_suoritus_AIKA[omistaja_objekti];
    Seis_AIKAKATKAISU();Aktiivinen=0;
    if(TULOS==사용자중단됨){
        저장된작업 *merkkijono_data=&저장값[omistaja_objekti];merkkijono_data->멈춤상태=1;merkkijono_data->vuorovaikutteinen=vuorovaikutteinen;merkkijono_data->리눅스규약=리눅스규약;merkkijono_data->dynaaminen_muisti=keko_lopettaa_puhelu;merkkijono_data->인수개수=전달인수개수;
        memcpy(merkkijono_data->oikeudet_luettelo,oikeudet_luettelo,sizeof(oikeudet_luettelo));memcpy(merkkijono_data->tiedostoluettelo,tiedostoluettelo,sizeof(tiedostoluettelo));memcpy(merkkijono_data->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(merkkijono_data->argumentti_MATRIISI,전달인수,sizeof(전달인수));memcpy(merkkijono_data->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<käyttäjä_page_LASKE;순번++)if(oikeudet_luettelo[순번])memcpy((unsigned char *)tilannekuva(omistaja_objekti)+순번*sivukoko,(void *)(käyttäjä_PERUS+순번*sivukoko),sivukoko);
    }else{
        저장값[omistaja_objekti].멈춤상태=0;화면초기화(omistaja_objekti);
        for(unsigned 순번=0;순번<16;순번++)if(tiedostoluettelo[순번]>=0)pk_close(tiedostoluettelo[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])Sulje_vastake_päätepiste(순번+32);
    }
    for(unsigned 순번=0;순번<käyttäjä_page_LASKE;순번++){page_luettelo[순번]=0;oikeudet_luettelo[순번]=0;}변환표맞추기();return TULOS;
}
uintptr_t Taulu_käyttäjän_ohjausobjekti(uintptr_t Toiminto){
    unsigned sijainti=Toiminto&15;if(sijainti>=4||Aktiivinen)return (uint32_t)-22;
    저장된작업 *merkkijono_data=&저장값[sijainti];
    if(Toiminto>=32){if(merkkijono_data->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(merkkijono_data->tiedostoluettelo[순번]>=0)pk_close(merkkijono_data->tiedostoluettelo[순번]);for(unsigned 순번=0;순번<24;순번++)if(merkkijono_data->통신끝점들[순번])Sulje_vastake_päätepiste(순번+32);}merkkijono_data->멈춤상태=0;화면초기화(sijainti);return 0;}
    if(Toiminto>=16)return merkkijono_data->멈춤상태;
    if(!merkkijono_data->멈춤상태)return (uint32_t)-22;
    omistaja_objekti=sijainti;vuorovaikutteinen=merkkijono_data->vuorovaikutteinen;리눅스규약=merkkijono_data->리눅스규약;keko_lopettaa_puhelu=merkkijono_data->dynaaminen_muisti;전달인수개수=merkkijono_data->인수개수;
    memcpy(tiedostoluettelo,merkkijono_data->tiedostoluettelo,sizeof(tiedostoluettelo));memcpy(통신끝점들,merkkijono_data->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,merkkijono_data->argumentti_MATRIISI,sizeof(전달인수));memcpy(전달인수길이,merkkijono_data->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<käyttäjä_page_LASKE;순번++)page_luettelo[순번]=(käyttäjä_PERUS+순번*sivukoko)|ydin_page;변환표맞추기();
    memset((void *)käyttäjä_PERUS,0,käyttäjä_lopettaa_puhelu-käyttäjä_PERUS);
    for(unsigned 순번=0;순번<käyttäjä_page_LASKE;순번++)if(merkkijono_data->oikeudet_luettelo[순번])memcpy((void *)(käyttäjä_PERUS+순번*sivukoko),(unsigned char *)tilannekuva(sijainti)+순번*sivukoko,sivukoko);
    memcpy(oikeudet_luettelo,merkkijono_data->oikeudet_luettelo,sizeof(oikeudet_luettelo));
    for(unsigned 순번=0;순번<käyttäjä_page_LASKE;순번++){unsigned data_toimi=oikeudet_luettelo[순번];page_luettelo[순번]=data_toimi?(käyttäjä_PERUS+순번*sivukoko)|(data_toimi==3?käyttäjä_luku_ja_kirjoitus:data_toimi==5?käyttäjä_lukea_Suorita:käyttäjä_vain_luku):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");Aktiivinen=1;merkkijono_data->멈춤상태=0;alku_AIKAKATKAISU();
    käyttäjä_suoritus_AIKA[omistaja_objekti]=보드밀리초();
    return (uint32_t)loppu_ohjelma(käyttäjä_jatka(&merkkijono_data->suoritus_kuva,merkkijono_data->liukuluku_Tila));
}
static int suorittaa_ohjelma(const unsigned char *data, size_t Koko, unsigned 전달값, int 리눅스방식, const char *Nimi) {
    if (Aktiivinen) return -16;
    omistaja_objekti=Taulu_Pääte(11);if(omistaja_objekti<0||omistaja_objekti>3||저장값[omistaja_objekti].멈춤상태)return -16;vuorovaikutteinen=0;
    int kelvollinen = 실행파일검사(data, Koko, 리눅스방식); if (kelvollinen) return kelvollinen;
    리눅스규약 = 리눅스방식;
    unsigned nimi_INDEKSI=0;
    while (*Nimi && nimi_INDEKSI<31) käyttäjä_komento_nimi[omistaja_objekti][nimi_INDEKSI++]=(unsigned char)*Nimi++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (nimi_INDEKSI) käyttäjä_komento_nimi[omistaja_objekti][nimi_INDEKSI++]=' ';
        for (unsigned sijainti=0; sijainti<전달인수길이[0]; sijainti++) käyttäjä_komento_nimi[omistaja_objekti][nimi_INDEKSI++]=전달인수[0][sijainti];
    }
    käyttäjä_komento_nimi[omistaja_objekti][nimi_INDEKSI]=0; käyttäjänumero[omistaja_objekti]=Seuraava_käyttäjänumero++;
    if (Seuraava_käyttäjänumero>0x7fffffffu) Seuraava_käyttäjänumero=10;
    käyttäjä_alku_AIKA[omistaja_objekti]=보드밀리초(); 사용자누적시각[omistaja_objekti]=0;
    for (unsigned 순번 = 0; 순번 < käyttäjä_page_LASKE; 순번++) page_luettelo[순번] = (käyttäjä_PERUS + 순번 * sivukoko) | ydin_page;
    변환표맞추기();
    memset((void *)käyttäjä_PERUS, 0, käyttäjä_lopettaa_puhelu - käyttäjä_PERUS);
    memset(oikeudet_luettelo, 0, sizeof(oikeudet_luettelo));
    실행파일머리 suoritettava_tiedosto_otsikko; memcpy(&suoritettava_tiedosto_otsikko, data, sizeof(suoritettava_tiedosto_otsikko));
    for (unsigned 순번 = 0; 순번 < suoritettava_tiedosto_otsikko.ohjelma_otsikko_LASKE; 순번++) {
        실행파일구획 data_toimi; memcpy(&data_toimi, data + suoritettava_tiedosto_otsikko.ohjelma_otsikko_SIIRTYMÄ + 순번 * sizeof(data_toimi), sizeof(data_toimi));
        if (data_toimi.TYYPPI_alue != 1 || !data_toimi.기억영역크기) continue;
        if (data_toimi.파일영역크기) memcpy((void *)(uintptr_t)data_toimi.OSOITE, data + data_toimi.SIIRTYMÄ_ARVO, data_toimi.파일영역크기);
        for (uintptr_t nykyinen_toimi = data_toimi.OSOITE & ~(sivukoko - 1); nykyinen_toimi < data_toimi.OSOITE + data_toimi.기억영역크기; nykyinen_toimi += sivukoko) {
            oikeudet_luettelo[(nykyinen_toimi - käyttäjä_PERUS) / sivukoko] = (data_toimi.määritys_Background_Intelligent_Transfer_Service & 2) ? 3 : ((data_toimi.määritys_Background_Intelligent_Transfer_Service & 1) ? 5 : 1);
        }
    }
    for (uintptr_t nykyinen_toimi = käyttäjä_Pino_OSOITE; nykyinen_toimi < käyttäjä_lopettaa_puhelu; nykyinen_toimi += sivukoko) oikeudet_luettelo[(nykyinen_toimi - käyttäjä_PERUS) / sivukoko] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(suoritettava_tiedosto_otsikko.aloituskohta) : käyttäjä_lopettaa_puhelu;
    for (unsigned 순번 = 0; 순번 < käyttäjä_page_LASKE; 순번++) {
        unsigned oikeudet = oikeudet_luettelo[순번];
        page_luettelo[순번] = oikeudet ? (käyttäjä_PERUS + 순번 * sivukoko) | (oikeudet == 3 ? käyttäjä_luku_ja_kirjoitus : oikeudet == 5 ? käyttäjä_lukea_Suorita : käyttäjä_vain_luku) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) tiedostoluettelo[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    keko_lopettaa_puhelu = käyttäjä_KUVA_lopettaa_puhelu;
    Aktiivinen = 1; alku_AIKAKATKAISU();
    käyttäjä_suoritus_AIKA[omistaja_objekti]=보드밀리초();
    int TULOS = käyttäjä_anna(suoritettava_tiedosto_otsikko.aloituskohta, 초기쌓임공간, 전달값);
    return loppu_ohjelma(TULOS);
}
uintptr_t Taulu_käyttäjä_suorittaa(uintptr_t HAKU_INDEKSI) {
    if (HAKU_INDEKSI >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Nimi=HAKU_INDEKSI==10?"javac":HAKU_INDEKSI==11?"java":HAKU_INDEKSI==12?"python":HAKU_INDEKSI==13?"vi":HAKU_INDEKSI==14?"jar":HAKU_INDEKSI==15?"cc":HAKU_INDEKSI==16?"jaot":"ELF";
    return (uint32_t)suorittaa_ohjelma(실행항목들[HAKU_INDEKSI].data, 실행항목들[HAKU_INDEKSI].Koko, 실행항목들[HAKU_INDEKSI].전달값, 0, Nimi);
}
static uintptr_t Suorita_Tiedosto(int 리눅스방식) {
    static unsigned char KUVA[16384];
    if (Aktiivinen || !전달인수개수) return (uint32_t)-22;
    int Tiedosto_kahva = pk_open((const char *)전달인수[0], vain_luku_ARVO, 0);
    if (Tiedosto_kahva < 0) return (uint32_t)-virhenumero;
    int Koko = pk_size(Tiedosto_kahva);
    if (Koko < 0 || (unsigned)Koko > sizeof(KUVA)) { pk_close(Tiedosto_kahva); return (uint32_t)-27; }
    int SAATU_HINTA_LASKE = pk_read(Tiedosto_kahva, KUVA, Koko); pk_close(Tiedosto_kahva);
    if (SAATU_HINTA_LASKE != Koko) return (uint32_t)-5;
    return (uint32_t)suorittaa_ohjelma(KUVA, Koko, 0, 리눅스방식, "");
}
uintptr_t Taulu_käyttäjä_Tiedosto(void) { return Suorita_Tiedosto(0); }
uintptr_t 보드사용자리눅스파일(void) { return Suorita_Tiedosto(1); }
uintptr_t Taulu_käyttäjä_vahvista(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].data, 잘못된실행항목들[순번].Koko) != käyttäjä_suoritettava_tiedosto_virhe) return 순번 + 1;
    return 0;
}
