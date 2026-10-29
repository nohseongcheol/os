#include "../명명/기계연결이름.h"
#include "skärmbild_info.h"
// EL0 köra_kommando dator nivå_värde. filnamn data/정책은 기존 AOT Java 커널에 위임한다.
#include "användarutrymme.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../nätverk_Stack/nätverk_Stack.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define dator_register(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_distributör 0xff841000ul
#define IRQ_CPU_gränssnitt 0xff842000ul
#define sidstorlek 4096ul
#define ansluta_markör (1ul << 10)
#define nej_köra_behörighet (1ul << 53)
#define användare_nej_köra (1ul << 54)
#define normal_Minne ((1ul << 2) | (3ul << 8) | ansluta_markör)
#define kärna_page (3ul | normal_Minne | nej_köra_behörighet | användare_nej_köra)
#define användare_läsa_skriva (3ul | normal_Minne | (1ul << 6) | nej_köra_behörighet | användare_nej_köra)
#define användare_skrivskyddad (3ul | normal_Minne | (3ul << 6) | nej_köra_behörighet | användare_nej_köra)
#define användare_läsa_köra (3ul | normal_Minne | (3ul << 6) | nej_köra_behörighet)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t Tavla_bildpunkt(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t Tavla_Terminal(uintptr_t);
extern int Terminal_väntar(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),skärmbild_SMS(int,int,const uint32_t *,unsigned);
extern void starta_skärmbild(int),skärmbild_tryck(int,unsigned);
extern int användare_CV(användare_ram *,void *);
extern void 사용자실수보관(void *);
extern int användare_ange(uintptr_t startpunkt, uintptr_t stackminne, uintptr_t 전달값);
extern void användare_Retur(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t rot_ADRESS[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t page_ange[användare_page_ANTAL] __attribute__((aligned(4096)));
static uint8_t Behörigheter_ange[användare_page_ANTAL];
static int Aktiv, fillista[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int Stäng_socket_deltagare(unsigned filreferens){return filreferens<40?자바전문닫기(filreferens):자바흐름닫기(filreferens);}
static uint64_t FREKVENS, måldatum_tid;
static uintptr_t heap_avsluta;
// kärna_värde 셸이 준비한 UTF-8 argument. EL0에는 kopia_värde 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int pausad_status,interaktiv,리눅스규약,fillista[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char argument_MATRIS[8][256],Behörigheter_ange[användare_page_ANTAL];
    uintptr_t dynamiskt_minne; användare_ram körning_ram;
    unsigned char flyttal_status[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int ägare_objekt,interaktiv;
static uint32_t användarnummer[4], användare_START_tid[4], 사용자누적시각[4], användare_körning_tid[4], Nästa_användarnummer=10;
static unsigned char användare_kommando_namn[4][288];
uint32_t läsa_användare_status(unsigned post_värde, unsigned INDEX) {
    unsigned positionsindex=INDEX&3;
    int status_värde=(Aktiv && ägare_objekt==(int)positionsindex) ? 1 : 저장값[positionsindex].pausad_status ? 2 : 0;
    if (post_värde==0) return status_värde;
    if (!status_värde) return 0;
    if (post_värde==1) return användarnummer[positionsindex];
    if (post_värde==2) {
        unsigned char *쪽들=status_värde==1?Behörigheter_ange:저장값[positionsindex].Behörigheter_ange;
        unsigned page_ANTAL=0; for (unsigned 순번=0; 순번<användare_page_ANTAL; 순번++) if(쪽들[순번]) page_ANTAL++;
        return page_ANTAL*4;
    }
    if (post_värde==3) return (uint32_t)보드밀리초()-användare_START_tid[positionsindex];
    if (post_värde==4) return 사용자누적시각[positionsindex]+(status_värde==1?(uint32_t)보드밀리초()-användare_körning_tid[positionsindex]:0);
    if (post_värde==5) return INDEX/4<sizeof(användare_kommando_namn[0])?användare_kommando_namn[positionsindex][INDEX/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t post_ANTAL) {
    if (Aktiv || post_ANTAL > 8) return (uint32_t)-22;
    전달인수개수 = post_ANTAL;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t LETAUPP_INDEX, uintptr_t aktuellt_placera, uintptr_t byte_data) {
    if (Aktiv || LETAUPP_INDEX >= 전달인수개수 || aktuellt_placera >= 255 || aktuellt_placera != 전달인수길이[LETAUPP_INDEX] || !byte_data || byte_data > 255)
        return (uint32_t)-22;
    전달인수[LETAUPP_INDEX][aktuellt_placera] = byte_data;
    전달인수길이[LETAUPP_INDEX] = aktuellt_placera + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Klocka_värde(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Stopp_TIMEOUT(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    dator_register(IRQ_distributör + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void START_TIMEOUT(void) {
    uint64_t 간격 = FREKVENS * 2, aktivera = 1;
    måldatum_tid = Klocka_värde() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(aktivera) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned datablock = 0; datablock < 4; datablock++) {
        rot_ADRESS[datablock] = (uintptr_t)가운데[datablock] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t Adress = ((uintptr_t)datablock << 30) | ((uintptr_t)순번 << 21);
            가운데[datablock][순번] = Adress | 1 | ansluta_markör | användare_nej_köra;
            if (Adress >= 0xfc000000ul) 가운데[datablock][순번] |= nej_köra_behörighet; // Device-nGnRnE
            else 가운데[datablock][순번] |= normal_Minne; // Normal, non-cacheable
        }
    }
    for (unsigned SEKUND_värde = 0; SEKUND_värde < användare_page_ANTAL / 512; SEKUND_värde++)
        가운데[0][(användare_BAS >> 21) + SEKUND_värde] = (uintptr_t)(page_ange + SEKUND_värde * 512) | 3;
    for (unsigned 순번 = 0; 순번 < användare_page_ANTAL; 순번++) page_ange[순번] = (användare_BAS + 순번 * sidstorlek) | kärna_page;
    uint64_t Minne_attribut_register = 0x4400, ADRESS_Översättning_kontroll = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Minne_attribut_register), "r"(ADRESS_Översättning_kontroll), "r"((uintptr_t)rot_ADRESS) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t flyttal_status = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(flyttal_status) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREKVENS));
    Stopp_TIMEOUT();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 startpunkt_värde 때만 Tillåt_värde.
    dator_register(IRQ_distributör) = 0;
    dator_register(IRQ_distributör + 0x180) = 0xffffffff;
    dator_register(IRQ_distributör + 0x80) = 0xffffffff;
    dator_register(IRQ_distributör + 0x280) = 1u << 30;
    dator_register(IRQ_distributör + 0x41c) = 0x80808080;
    dator_register(IRQ_distributör + 0x100) = 1u << 30;
    dator_register(IRQ_CPU_gränssnitt + 4) = 0xff;
    dator_register(IRQ_CPU_gränssnitt + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 informationsteknik_normal 확인할 nummer 있다.
    int Säkerhet = (dator_register(IRQ_distributör + 4) & (1u << 10)) != 0;
    dator_register(IRQ_distributör) = Säkerhet ? 1 : 3;
    dator_register(IRQ_CPU_gränssnitt) = Säkerhet ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t Typ_område, dator_Typ; uint32_t versionsnummer;
    uint64_t startpunkt, app_huvud_FÖRSKJUTNING, avsnittsrubrik_FÖRSKJUTNING; uint32_t konfiguration_BITS;
    uint16_t körbar_fil_huvud_storlek, app_huvud_post_storlek, app_huvud_ANTAL, avsnittsrubrik_post_storlek, avsnittsrubrik_ANTAL, avsnitt_namn_tabell_INDEX;
} 실행파일머리;
typedef struct { uint32_t Typ_område, konfiguration_BITS; uint64_t FÖRSKJUTNING_värde, Adress, 물리주소, 파일영역크기, 기억영역크기, justera_gräns; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(användare_ram) == 272, "exception assembly layout");
static int 포함된범위(uint64_t FÖRSKJUTNING_värde, uint64_t Storlek, uint64_t avsluta_FÖRSKJUTNING) {
    return FÖRSKJUTNING_värde <= avsluta_FÖRSKJUTNING && Storlek <= avsluta_FÖRSKJUTNING - FÖRSKJUTNING_värde;
}
static int 부가정보검사(const unsigned char *data_placera, size_t Storlek) {
    size_t aktuellt_placera = 0;
    while (포함된범위(aktuellt_placera, 12, Storlek)) {
        uint32_t 낱말들[3]; memcpy(낱말들, data_placera + aktuellt_placera, 12); aktuellt_placera += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(aktuellt_placera, 이름영역크기, Storlek) || !포함된범위(aktuellt_placera + 이름영역크기, 설명크기, Storlek)) return 0;
        const unsigned char Namn[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Namn) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Namn); 순번++) if (data_placera[aktuellt_placera + 순번] != Namn[순번]) 일치 = 0;
        uint32_t versionsnummer = 0;
        if (일치) memcpy(&versionsnummer, data_placera + aktuellt_placera + 이름영역크기, 4);
        if (일치 && versionsnummer == 1) return 1;
        aktuellt_placera += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *data, size_t Storlek, int 리눅스방식) {
    if (Storlek < sizeof(실행파일머리)) return användare_körbar_fil_fel;
    실행파일머리 körbar_fil_huvud; memcpy(&körbar_fil_huvud, data, sizeof(körbar_fil_huvud));
    if (körbar_fil_huvud.형식식별[0] != 127 || körbar_fil_huvud.형식식별[1] != 'E' || körbar_fil_huvud.형식식별[2] != 'L' || körbar_fil_huvud.형식식별[3] != 'F' ||
        körbar_fil_huvud.형식식별[4] != 2 || körbar_fil_huvud.형식식별[5] != 1 || körbar_fil_huvud.형식식별[6] != 1 || (körbar_fil_huvud.형식식별[7] != 0 && (!리눅스방식 || körbar_fil_huvud.형식식별[7] != 3)) ||
        körbar_fil_huvud.Typ_område != 2 || körbar_fil_huvud.dator_Typ != 183 || körbar_fil_huvud.versionsnummer != 1 || körbar_fil_huvud.konfiguration_BITS || körbar_fil_huvud.körbar_fil_huvud_storlek != sizeof(körbar_fil_huvud) ||
        körbar_fil_huvud.app_huvud_post_storlek != sizeof(실행파일구획) || !körbar_fil_huvud.app_huvud_ANTAL || körbar_fil_huvud.app_huvud_ANTAL > 16 ||
        körbar_fil_huvud.app_huvud_FÖRSKJUTNING < sizeof(körbar_fil_huvud) || !포함된범위(körbar_fil_huvud.app_huvud_FÖRSKJUTNING, (uint64_t)körbar_fil_huvud.app_huvud_ANTAL * sizeof(실행파일구획), Storlek)) return användare_körbar_fil_fel;
    uint8_t 사용량[(användare_BILD_avsluta - användare_BAS) / sidstorlek] = {0};
    int giltig_startpunkt = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < körbar_fil_huvud.app_huvud_ANTAL; 순번++) {
        실행파일구획 data_placera; memcpy(&data_placera, data + körbar_fil_huvud.app_huvud_FÖRSKJUTNING + 순번 * sizeof(data_placera), sizeof(data_placera));
        if (data_placera.Typ_område == 4) {
            if (!포함된범위(data_placera.FÖRSKJUTNING_värde, data_placera.파일영역크기, Storlek)) return användare_körbar_fil_fel;
            if (부가정보검사(data + data_placera.FÖRSKJUTNING_värde, data_placera.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (data_placera.Typ_område == 0 || data_placera.Typ_område == 6 || (data_placera.Typ_område == 0x6474e551 && !(data_placera.konfiguration_BITS & 1))) continue;
        if (data_placera.Typ_område != 1) return användare_körbar_fil_fel; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!data_placera.기억영역크기) continue;
        if (data_placera.konfiguration_BITS & ~7u || !(data_placera.konfiguration_BITS & 4) || (data_placera.konfiguration_BITS & 3) == 3 || data_placera.파일영역크기 > data_placera.기억영역크기 ||
            (data_placera.파일영역크기 && !포함된범위(data_placera.FÖRSKJUTNING_värde, data_placera.파일영역크기, Storlek)) || data_placera.Adress < användare_BAS ||
            !포함된범위(data_placera.Adress, data_placera.기억영역크기, användare_BILD_avsluta) ||
            (!리눅스방식 && ((data_placera.Adress & (sidstorlek - 1)) || (data_placera.FÖRSKJUTNING_värde & (sidstorlek - 1)) || data_placera.justera_gräns != sidstorlek)) ||
            (리눅스방식 && (((data_placera.Adress ^ data_placera.FÖRSKJUTNING_värde) & (sidstorlek - 1)) || !data_placera.justera_gräns ||
                (data_placera.justera_gräns & (data_placera.justera_gräns - 1)) || data_placera.justera_gräns > 0x200000 || ((data_placera.Adress ^ data_placera.FÖRSKJUTNING_värde) & (data_placera.justera_gräns - 1))))) return användare_körbar_fil_fel;
        unsigned 첫항목 = (data_placera.Adress - användare_BAS) / sidstorlek;
        unsigned post_ANTAL = ((data_placera.Adress & (sidstorlek - 1)) + data_placera.기억영역크기 + sidstorlek - 1) / sidstorlek;
        for (unsigned page_värde = 첫항목; page_värde < 첫항목 + post_ANTAL; page_värde++) {
            if (사용량[page_värde]) return användare_körbar_fil_fel;
            사용량[page_värde] = 1;
        }
        if ((data_placera.konfiguration_BITS & 1) && körbar_fil_huvud.startpunkt >= data_placera.Adress && körbar_fil_huvud.startpunkt < data_placera.Adress + data_placera.파일영역크기 && !(körbar_fil_huvud.startpunkt & 3)) giltig_startpunkt = 1;
        적재구획++;
    }
    return giltig_startpunkt && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : användare_körbar_fil_fel;
}
int 사용자실행파일검사(const unsigned char *data, size_t Storlek) { return 실행파일검사(data, Storlek, 0); }
static void sidlayout(uintptr_t Adress, uint64_t konfiguration_BITS, unsigned behörigheter) {
    unsigned LETAUPP_INDEX = (Adress - användare_BAS) / sidstorlek;
    page_ange[LETAUPP_INDEX] = Adress | konfiguration_BITS;
    Behörigheter_ange[LETAUPP_INDEX] = behörigheter;
}
static int användare_område(uintptr_t Adress, size_t post_ANTAL, int 쓰는중) {
    if (Adress < användare_BAS || !포함된범위(Adress, post_ANTAL, användare_avsluta)) return 0;
    if (!post_ANTAL) return 1;
    unsigned 첫항목 = (Adress - användare_BAS) / sidstorlek, 마지막 = (Adress + post_ANTAL - 1 - användare_BAS) / sidstorlek;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(Behörigheter_ange[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int kopia_väg(uintptr_t Adress, char *sökväg_2) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!användare_område(Adress, 1, 0)) return -14;
        sökväg_2[순번] = *(const char *)Adress++;
        if (!sökväg_2[순번]) return 0;
    }
    return -36;
}
static intptr_t kärna_KR(intptr_t RESULTAT) { return RESULTAT < 0 ? -felnummer : RESULTAT; }
static int 대응파일기술자(uint64_t filreferens) { return filreferens >= 3 && filreferens < 19 ? fillista[filreferens - 3] : -1; }
static int socket_deltagare_ägare(uint64_t filreferens) { return filreferens >= 32 && filreferens < 56 && 통신끝점들[filreferens - 32]; }
static int ADRESS_indata(uintptr_t 가리킴값, size_t längd_värde, struct pk_sockaddr_in *Adress) {
    if (längd_värde != sizeof(*Adress)) return -22;
    if (!användare_område(가리킴값, längd_värde, 0)) return -14;
    memcpy(Adress, (const void *)가리킴값, sizeof(*Adress));
    return Adress->sin_family == AF_INET ? 0 : -97;
}
static int ADRESS_utleverans_check(uintptr_t 가리킴값, uintptr_t längd_markör, pk_socklen_t *buffra_kapacitet) {
    if (!användare_område(längd_markör, sizeof(*buffra_kapacitet), 1)) return -14;
    memcpy(buffra_kapacitet, (const void *)längd_markör, sizeof(*buffra_kapacitet));
    if (*buffra_kapacitet > sizeof(struct pk_sockaddr_in)) *buffra_kapacitet = sizeof(struct pk_sockaddr_in);
    if (*buffra_kapacitet && !användare_område(가리킴값, *buffra_kapacitet, 1)) return -14;
    return 0;
}
static void ADRESS_utleverans(uintptr_t 가리킴값, uintptr_t längd_markör, pk_socklen_t buffra_kapacitet, int Adress, int portnummer) {
    struct pk_sockaddr_in värde; memset(&värde, 0, sizeof(värde));
    värde.sin_family = AF_INET; värde.sin_port = pk_htons(portnummer); värde.sin_addr.s_addr = pk_htonl(Adress);
    if (buffra_kapacitet) memcpy((void *)가리킴값, &värde, buffra_kapacitet);
    pk_socklen_t längd_värde = sizeof(värde); memcpy((void *)längd_markör, &längd_värde, sizeof(längd_värde));
}
extern uintptr_t Tavla_Kanal(uintptr_t, uintptr_t);
static intptr_t ursprunglig_System_ring(användare_ram *fil_post) {
    uintptr_t 첫째값 = fil_post->register_data[0], SEKUND_värde = fil_post->register_data[1], kodpunkt = fil_post->register_data[2];
    char sökväg_2[65];
    int filreferens, RESULTAT;
    switch (fil_post->register_data[8]) {
    case 0: return 1; // eget ABI 버전
    case 1: // write: markör 전체를 검사한 BACK_värde utmatningsposition/filnamn ändra_värde
        if (kodpunkt > 65536) return -22;
        if (!användare_område(SEKUND_värde, kodpunkt, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t START_utleverans=Klocka_värde();
            for (size_t 순번 = 0; 순번 < kodpunkt; 순번++) Tavla_Kanal(첫째값, ((const unsigned char *)SEKUND_värde)[순번]);
            /* 큰 tty를 그린 kärna_värde 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(interaktiv){
                måldatum_tid+=Klocka_värde()-START_utleverans;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(måldatum_tid) : "memory");
            }
            return kodpunkt;
        }
        if(첫째값>=40&&socket_deltagare_ägare(첫째값)){
            size_t objekt_ANTAL=kodpunkt>512?512:kodpunkt;for(size_t 순번=0;순번<objekt_ANTAL;순번++)자바전문넣기(순번,((const unsigned char *)SEKUND_värde)[순번]);return 자바흐름쓰기(첫째값,objekt_ANTAL);
        }
        filreferens = 대응파일기술자(첫째값); if (filreferens < 0) return -9;
        return kärna_KR(pk_write(filreferens, (const void *)SEKUND_värde, kodpunkt));
    case 2:
        if (kodpunkt > 65536) return -22;
        if (!användare_område(SEKUND_värde, kodpunkt, 1)) return -14;
        if (첫째값 == 0) {
            size_t objekt_ANTAL = 0;
            while (objekt_ANTAL < kodpunkt) {
                int tecken_värde = (int32_t)보드글자읽기(); if (tecken_värde == -2) return objekt_ANTAL; if (tecken_värde < 0) break;
                ((unsigned char *)SEKUND_värde)[objekt_ANTAL++] = tecken_värde;
            }
            return objekt_ANTAL ? (intptr_t)objekt_ANTAL : (kodpunkt ? -11 : 0);
        }
        if(첫째값>=40&&socket_deltagare_ägare(첫째값)){
            RESULTAT=자바흐름읽기(첫째값,kodpunkt>512?512:kodpunkt);if(RESULTAT>0)for(int 순번=0;순번<RESULTAT;순번++)((unsigned char *)SEKUND_värde)[순번]=자바전문얻기(순번);return RESULTAT;
        }
        filreferens = 대응파일기술자(첫째값); if (filreferens < 0) return -9;
        return kärna_KR(pk_read(filreferens, (void *)SEKUND_värde, kodpunkt));
    case 3:
        RESULTAT = kopia_väg(첫째값, sökväg_2); if (RESULTAT) return RESULTAT;
        if (SEKUND_värde > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (fillista[순번] < 0) {
            filreferens = pk_open(sökväg_2, (int)SEKUND_värde, 0600);
            if (filreferens < 0) return -felnummer;
            fillista[순번] = filreferens; return 순번 + 3;
        }
        return -24;
    case 4:
        if (socket_deltagare_ägare(첫째값)) { RESULTAT = Stäng_socket_deltagare(첫째값); if (!RESULTAT) 통신끝점들[첫째값 - 32] = 0; return RESULTAT; }
        filreferens = 대응파일기술자(첫째값); if (filreferens < 0) return -9;
        RESULTAT = pk_close(filreferens); if (!RESULTAT) fillista[첫째값 - 3] = -1;
        return kärna_KR(RESULTAT);
    case 5:
        filreferens = 대응파일기술자(첫째값); if (filreferens < 0) return -9;
        if (kodpunkt > 2) return -22;
        return kärna_KR(pk_lseek(filreferens, (int64_t)SEKUND_värde, kodpunkt));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 användarutrymme RW/NX heap_värde, 새로 노출되는 페이지는 0으로 starta
        if (!첫째값) return heap_avsluta;
        if (첫째값 < användare_BILD_avsluta || 첫째값 > användare_heap_avsluta) return -12;
        uintptr_t 이전쪽들 = (heap_avsluta + sidstorlek - 1) & ~(sidstorlek - 1);
        uintptr_t 새쪽들 = (첫째값 + sidstorlek - 1) & ~(sidstorlek - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t data_placera = 이전쪽들; data_placera < 새쪽들; data_placera += sidstorlek) sidlayout(data_placera, kärna_page, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t data_placera = 이전쪽들; data_placera < 새쪽들; data_placera += sidstorlek) sidlayout(data_placera, användare_läsa_skriva, 3);
        } else {
            for (uintptr_t data_placera = 새쪽들; data_placera < 이전쪽들; data_placera += sidstorlek) {
                page_ange[(data_placera - användare_BAS) / sidstorlek] = 0; Behörigheter_ange[(data_placera - användare_BAS) / sidstorlek] = 0;
            }
        }
        heap_avsluta = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        filreferens = 대응파일기술자(첫째값); return filreferens < 0 ? -9 : kärna_KR(pk_size(filreferens));
    case 10:
        filreferens = 대응파일기술자(첫째값); return filreferens < 0 ? -9 : kärna_KR(pk_ftruncate(filreferens, (int64_t)SEKUND_värde));
    case 11:
        RESULTAT = kopia_väg(첫째값, sökväg_2); return RESULTAT ? RESULTAT : kärna_KR(pk_unlink(sökväg_2));
    case 12:
        filreferens = 대응파일기술자(첫째값); return filreferens < 0 ? -9 : kärna_KR(pk_fsync(filreferens));
    case 13: { // 그래픽 기초 API: användarutrymme 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = fil_post->register_data[3], 높이값 = fil_post->register_data[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), skärmbild_längd = 보드화면높이();
        if (첫째값 > 화면폭 || SEKUND_värde > skärmbild_längd || 너비값 > 화면폭 - 첫째값 || 높이값 > skärmbild_längd - SEKUND_värde) return -22;
        for (uintptr_t Y_koordinat = SEKUND_värde; Y_koordinat < SEKUND_värde + 높이값; Y_koordinat++) for (uintptr_t x_koordinat = 첫째값; x_koordinat < 첫째값 + 너비값; x_koordinat++) Tavla_bildpunkt(x_koordinat, Y_koordinat, kodpunkt);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=objekt_ANTAL; args(index,buffer,capacity)=UTF-8 längd_värde
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (kodpunkt <= 전달인수길이[첫째값]) return -36;
        if (!användare_område(SEKUND_värde, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SEKUND_värde, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;interaktiv=1;return Tavla_Terminal(13);}
        if(첫째값==2){interaktiv=0;return 0;}
        if(첫째값==3)return Tavla_Terminal(13);
        if(첫째값!=1||!interaktiv)return -22;
        RESULTAT=(int32_t)보드글자읽기();
        if(RESULTAT==-4096)return RESULTAT;
        START_TIMEOUT();return RESULTAT<0?-11:RESULTAT;
    case 17: { // 유한한 협력 vänta_värde: kommunikation 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t avsluta_tid = Klocka_värde() + FREKVENS * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Klocka_värde() < avsluta_tid);
        START_TIMEOUT(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 överordnad_värde·빈 폴더를 검사한다.
        if (SEKUND_värde > 2) return -22;
        RESULTAT = kopia_väg(첫째값, sökväg_2); if (RESULTAT) return RESULTAT;
        unsigned längd_värde = 0; while (sökväg_2[längd_värde]) längd_värde++;
        RESULTAT = 자바경로시작(längd_värde); if (RESULTAT < 0) return RESULTAT;
        for (unsigned 순번 = 0; 순번 < längd_värde; 순번++) 자바경로바이트(순번, (unsigned char)sökväg_2[순번]);
        return SEKUND_värde == 0 ? 자바항목종류() : SEKUND_värde == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int tecken_värde=(int32_t)보드글자읽기();if(tecken_värde==-4096)return tecken_värde;if(tecken_värde>=0)skärmbild_tryck(ägare_objekt,tecken_värde);START_TIMEOUT();}
        if(첫째값==3&&kodpunkt){if(!자바셸대화형())return -95;interaktiv=1;Tavla_Terminal(300);}
        return 화면호출(ägare_objekt,첫째값,SEKUND_värde,kodpunkt,fil_post->register_data[3],fil_post->register_data[4],fil_post->register_data[5]);
    case 21:
        if(kodpunkt>127)return -22;if(!användare_område(SEKUND_värde,kodpunkt*sizeof(uint32_t),0))return -14;
        return skärmbild_SMS(ägare_objekt,첫째값,(const uint32_t *)SEKUND_värde,kodpunkt);
    case 22: // skärmbild Storlek fråga_värde: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SEKUND_värde==SOCK_STREAM&&(kodpunkt==0||kodpunkt==6))RESULTAT=자바흐름만들기();
        else if(SEKUND_värde==SOCK_DGRAM&&(kodpunkt==0||kodpunkt==IPPROTO_UDP))RESULTAT=자바전문만들기(첫째값,SEKUND_värde,kodpunkt);
        else return -93;
        if (RESULTAT >= 32 && RESULTAT < 56) 통신끝점들[RESULTAT - 32] = 1;
        return RESULTAT;
    case 33: {
        if (!socket_deltagare_ägare(첫째값)) return -9;
        struct pk_sockaddr_in Adress;
        RESULTAT = ADRESS_indata(SEKUND_värde, kodpunkt, &Adress); if (RESULTAT) return RESULTAT;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(Adress.sin_addr.s_addr),pk_htons(Adress.sin_port)):자바전문묶기(첫째값, pk_htonl(Adress.sin_addr.s_addr), pk_htons(Adress.sin_port));
    }
    case 34: {
        if (!socket_deltagare_ägare(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (fil_post->register_data[3]) return -95;
        if (kodpunkt > 512) return -90;
        if (kodpunkt && !användare_område(SEKUND_värde, kodpunkt, 0)) return -14;
        struct pk_sockaddr_in Adress;
        RESULTAT = ADRESS_indata(fil_post->register_data[4], fil_post->register_data[5], &Adress); if (RESULTAT) return RESULTAT;
        for (unsigned 순번 = 0; 순번 < kodpunkt; 순번++) 자바전문넣기(순번, ((const unsigned char *)SEKUND_värde)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(Adress.sin_addr.s_addr), pk_htons(Adress.sin_port), kodpunkt);
    }
    case 35: {
        if (!socket_deltagare_ägare(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (fil_post->register_data[3]) return -95;
        if (kodpunkt > 512) return -90;
        if (kodpunkt && !användare_område(SEKUND_värde, kodpunkt, 1)) return -14;
        pk_socklen_t buffra_kapacitet = 0;
        if (fil_post->register_data[4]) { RESULTAT = ADRESS_utleverans_check(fil_post->register_data[4], fil_post->register_data[5], &buffra_kapacitet); if (RESULTAT) return RESULTAT; }
        RESULTAT = 자바전문받기(첫째값, kodpunkt); if (RESULTAT < 0) return RESULTAT;
        for (int 순번 = 0; 순번 < RESULTAT; 순번++) ((unsigned char *)SEKUND_värde)[순번] = 자바전문얻기(순번);
        if (fil_post->register_data[4]) ADRESS_utleverans(fil_post->register_data[4], fil_post->register_data[5], buffra_kapacitet, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return RESULTAT;
    }
    case 36: {
        if (!socket_deltagare_ägare(첫째값)) return -9;
        pk_socklen_t buffra_kapacitet;
        RESULTAT = ADRESS_utleverans_check(SEKUND_värde, kodpunkt, &buffra_kapacitet); if (RESULTAT) return RESULTAT;
        ADRESS_utleverans(SEKUND_värde,kodpunkt,buffra_kapacitet,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!socket_deltagare_ägare(첫째값))return -9;struct pk_sockaddr_in Adress;
        RESULTAT=ADRESS_indata(SEKUND_värde,kodpunkt,&Adress);if(RESULTAT)return RESULTAT;
        return 자바흐름연결(첫째값,pk_htonl(Adress.sin_addr.s_addr),pk_htons(Adress.sin_port));
    }
    case 38: return 첫째값>=40&&socket_deltagare_ägare(첫째값)?자바흐름듣기(첫째값,SEKUND_värde):-9;
    case 39:
        if(첫째값<40||!socket_deltagare_ägare(첫째값))return -9;
        if(SEKUND_värde||kodpunkt)return -95;RESULTAT=자바흐름연결받기(첫째값);if(RESULTAT>=40&&RESULTAT<56)통신끝점들[RESULTAT-32]=1;return RESULTAT;
    case 40: return 첫째값>=40&&socket_deltagare_ägare(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t systemanrop(användare_ram *fil_post) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(fil_post) : ursprunglig_System_ring(fil_post);
}
static void Retur_kärna(användare_ram *fil_post, int RESULTAT) {
    Stopp_TIMEOUT();
    fil_post->register_data[0] = (uint64_t)(int64_t)RESULTAT;
    fil_post->kommando_placera = (uintptr_t)användare_Retur;
    fil_post->kod_för_tillstånd = 0x3c5; // EL1h, DAIF masked
}
int undantagsfel_för_användare(användare_ram *fil_post, unsigned SKÄRNINGSPUNKT) {
    if (!Aktiv || (fil_post->kod_för_tillstånd & 15) != 0) return 0;
    if (SKÄRNINGSPUNKT) {
        uint32_t bekräftelse_värde = dator_register(IRQ_CPU_gränssnitt + 0xc), identifierare_värde = bekräftelse_värde & 1023;
        if (identifierare_värde == 30) { Retur_kärna(fil_post, användare_TIMEOUT); dator_register(IRQ_CPU_gränssnitt + 0x10) = bekräftelse_värde; return 1; }
        if (identifierare_värde < 1020) dator_register(IRQ_CPU_gränssnitt + 0x10) = bekräftelse_värde;
        return 1;
    }
    uint64_t fel_status; __asm__ volatile("mrs %0, esr_el1" : "=r"(fel_status));
    if (Klocka_värde() >= måldatum_tid) { Retur_kärna(fil_post, användare_TIMEOUT); return 1; }
    unsigned fel_område = fel_status >> 26;
    if (fel_område == 0x15 && (fel_status & 0xffff) == 0) {
        if (리눅스규약 ? fil_post->register_data[8] == 93 || fil_post->register_data[8] == 94 : fil_post->register_data[8] == 6) Retur_kärna(fil_post, (int)(fil_post->register_data[0] & 255));
        else {
            intptr_t RESULTAT=systemanrop(fil_post);
            if(RESULTAT==-4096&&interaktiv){
                저장값[ägare_objekt].körning_ram=*fil_post;저장값[ägare_objekt].körning_ram.kommando_placera-=4;
                사용자실수보관(저장값[ägare_objekt].flyttal_status);Retur_kärna(fil_post,사용자중단됨);
            }else fil_post->register_data[0]=(uint64_t)RESULTAT;
        }
    } else Retur_kärna(fil_post, fel_område == 0x24 ? användare_data_fel : fel_område == 0x20 ? användare_körning_fel : användare_ogiltig_instruktion);
    return 1;
}

// 생성된 const ELF grupp_värde: 실행은 반드시 app_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *data; size_t Storlek; unsigned 전달값; } app;
#include "programs.h"
static void *stillbild(unsigned positionsindex){return (void *)(0x04000000ul+positionsindex*(användare_avsluta-användare_BAS));}
static int slut_app(int RESULTAT){
    사용자누적시각[ägare_objekt]+=(uint32_t)보드밀리초()-användare_körning_tid[ägare_objekt];
    Stopp_TIMEOUT();Aktiv=0;
    if(RESULTAT==사용자중단됨){
        저장된작업 *sträng_data=&저장값[ägare_objekt];sträng_data->pausad_status=1;sträng_data->interaktiv=interaktiv;sträng_data->리눅스규약=리눅스규약;sträng_data->dynamiskt_minne=heap_avsluta;sträng_data->인수개수=전달인수개수;
        memcpy(sträng_data->Behörigheter_ange,Behörigheter_ange,sizeof(Behörigheter_ange));memcpy(sträng_data->fillista,fillista,sizeof(fillista));memcpy(sträng_data->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(sträng_data->argument_MATRIS,전달인수,sizeof(전달인수));memcpy(sträng_data->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<användare_page_ANTAL;순번++)if(Behörigheter_ange[순번])memcpy((unsigned char *)stillbild(ägare_objekt)+순번*sidstorlek,(void *)(användare_BAS+순번*sidstorlek),sidstorlek);
    }else{
        저장값[ägare_objekt].pausad_status=0;starta_skärmbild(ägare_objekt);
        for(unsigned 순번=0;순번<16;순번++)if(fillista[순번]>=0)pk_close(fillista[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])Stäng_socket_deltagare(순번+32);
    }
    for(unsigned 순번=0;순번<användare_page_ANTAL;순번++){page_ange[순번]=0;Behörigheter_ange[순번]=0;}변환표맞추기();return RESULTAT;
}
uintptr_t Tavla_användarkontroll(uintptr_t Åtgärd){
    unsigned positionsindex=Åtgärd&15;if(positionsindex>=4||Aktiv)return (uint32_t)-22;
    저장된작업 *sträng_data=&저장값[positionsindex];
    if(Åtgärd>=32){if(sträng_data->pausad_status){for(unsigned 순번=0;순번<16;순번++)if(sträng_data->fillista[순번]>=0)pk_close(sträng_data->fillista[순번]);for(unsigned 순번=0;순번<24;순번++)if(sträng_data->통신끝점들[순번])Stäng_socket_deltagare(순번+32);}sträng_data->pausad_status=0;starta_skärmbild(positionsindex);return 0;}
    if(Åtgärd>=16)return sträng_data->pausad_status;
    if(!sträng_data->pausad_status)return (uint32_t)-22;
    ägare_objekt=positionsindex;interaktiv=sträng_data->interaktiv;리눅스규약=sträng_data->리눅스규약;heap_avsluta=sträng_data->dynamiskt_minne;전달인수개수=sträng_data->인수개수;
    memcpy(fillista,sträng_data->fillista,sizeof(fillista));memcpy(통신끝점들,sträng_data->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,sträng_data->argument_MATRIS,sizeof(전달인수));memcpy(전달인수길이,sträng_data->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<användare_page_ANTAL;순번++)page_ange[순번]=(användare_BAS+순번*sidstorlek)|kärna_page;변환표맞추기();
    memset((void *)användare_BAS,0,användare_avsluta-användare_BAS);
    for(unsigned 순번=0;순번<användare_page_ANTAL;순번++)if(sträng_data->Behörigheter_ange[순번])memcpy((void *)(användare_BAS+순번*sidstorlek),(unsigned char *)stillbild(positionsindex)+순번*sidstorlek,sidstorlek);
    memcpy(Behörigheter_ange,sträng_data->Behörigheter_ange,sizeof(Behörigheter_ange));
    for(unsigned 순번=0;순번<användare_page_ANTAL;순번++){unsigned data_placera=Behörigheter_ange[순번];page_ange[순번]=data_placera?(användare_BAS+순번*sidstorlek)|(data_placera==3?användare_läsa_skriva:data_placera==5?användare_läsa_köra:användare_skrivskyddad):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");Aktiv=1;sträng_data->pausad_status=0;START_TIMEOUT();
    användare_körning_tid[ägare_objekt]=보드밀리초();
    return (uint32_t)slut_app(användare_CV(&sträng_data->körning_ram,sträng_data->flyttal_status));
}
static int köra_app(const unsigned char *data, size_t Storlek, unsigned 전달값, int 리눅스방식, const char *Namn) {
    if (Aktiv) return -16;
    ägare_objekt=Tavla_Terminal(11);if(ägare_objekt<0||ägare_objekt>3||저장값[ägare_objekt].pausad_status)return -16;interaktiv=0;
    int giltig = 실행파일검사(data, Storlek, 리눅스방식); if (giltig) return giltig;
    리눅스규약 = 리눅스방식;
    unsigned namn_INDEX=0;
    while (*Namn && namn_INDEX<31) användare_kommando_namn[ägare_objekt][namn_INDEX++]=(unsigned char)*Namn++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (namn_INDEX) användare_kommando_namn[ägare_objekt][namn_INDEX++]=' ';
        for (unsigned positionsindex=0; positionsindex<전달인수길이[0]; positionsindex++) användare_kommando_namn[ägare_objekt][namn_INDEX++]=전달인수[0][positionsindex];
    }
    användare_kommando_namn[ägare_objekt][namn_INDEX]=0; användarnummer[ägare_objekt]=Nästa_användarnummer++;
    if (Nästa_användarnummer>0x7fffffffu) Nästa_användarnummer=10;
    användare_START_tid[ägare_objekt]=보드밀리초(); 사용자누적시각[ägare_objekt]=0;
    for (unsigned 순번 = 0; 순번 < användare_page_ANTAL; 순번++) page_ange[순번] = (användare_BAS + 순번 * sidstorlek) | kärna_page;
    변환표맞추기();
    memset((void *)användare_BAS, 0, användare_avsluta - användare_BAS);
    memset(Behörigheter_ange, 0, sizeof(Behörigheter_ange));
    실행파일머리 körbar_fil_huvud; memcpy(&körbar_fil_huvud, data, sizeof(körbar_fil_huvud));
    for (unsigned 순번 = 0; 순번 < körbar_fil_huvud.app_huvud_ANTAL; 순번++) {
        실행파일구획 data_placera; memcpy(&data_placera, data + körbar_fil_huvud.app_huvud_FÖRSKJUTNING + 순번 * sizeof(data_placera), sizeof(data_placera));
        if (data_placera.Typ_område != 1 || !data_placera.기억영역크기) continue;
        if (data_placera.파일영역크기) memcpy((void *)(uintptr_t)data_placera.Adress, data + data_placera.FÖRSKJUTNING_värde, data_placera.파일영역크기);
        for (uintptr_t aktuellt_placera = data_placera.Adress & ~(sidstorlek - 1); aktuellt_placera < data_placera.Adress + data_placera.기억영역크기; aktuellt_placera += sidstorlek) {
            Behörigheter_ange[(aktuellt_placera - användare_BAS) / sidstorlek] = (data_placera.konfiguration_BITS & 2) ? 3 : ((data_placera.konfiguration_BITS & 1) ? 5 : 1);
        }
    }
    for (uintptr_t aktuellt_placera = användare_Stack_ADRESS; aktuellt_placera < användare_avsluta; aktuellt_placera += sidstorlek) Behörigheter_ange[(aktuellt_placera - användare_BAS) / sidstorlek] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(körbar_fil_huvud.startpunkt) : användare_avsluta;
    for (unsigned 순번 = 0; 순번 < användare_page_ANTAL; 순번++) {
        unsigned behörigheter = Behörigheter_ange[순번];
        page_ange[순번] = behörigheter ? (användare_BAS + 순번 * sidstorlek) | (behörigheter == 3 ? användare_läsa_skriva : behörigheter == 5 ? användare_läsa_köra : användare_skrivskyddad) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) fillista[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    heap_avsluta = användare_BILD_avsluta;
    Aktiv = 1; START_TIMEOUT();
    användare_körning_tid[ägare_objekt]=보드밀리초();
    int RESULTAT = användare_ange(körbar_fil_huvud.startpunkt, 초기쌓임공간, 전달값);
    return slut_app(RESULTAT);
}
uintptr_t Tavla_användare_köra(uintptr_t LETAUPP_INDEX) {
    if (LETAUPP_INDEX >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Namn=LETAUPP_INDEX==10?"javac":LETAUPP_INDEX==11?"java":LETAUPP_INDEX==12?"python":LETAUPP_INDEX==13?"vi":LETAUPP_INDEX==14?"jar":LETAUPP_INDEX==15?"cc":LETAUPP_INDEX==16?"jaot":"ELF";
    return (uint32_t)köra_app(실행항목들[LETAUPP_INDEX].data, 실행항목들[LETAUPP_INDEX].Storlek, 실행항목들[LETAUPP_INDEX].전달값, 0, Namn);
}
static uintptr_t köra_fil(int 리눅스방식) {
    static unsigned char BILD[16384];
    if (Aktiv || !전달인수개수) return (uint32_t)-22;
    int filreferens = pk_open((const char *)전달인수[0], skrivskyddad_värde, 0);
    if (filreferens < 0) return (uint32_t)-felnummer;
    int Storlek = pk_size(filreferens);
    if (Storlek < 0 || (unsigned)Storlek > sizeof(BILD)) { pk_close(filreferens); return (uint32_t)-27; }
    int BELOPP_ANTAL = pk_read(filreferens, BILD, Storlek); pk_close(filreferens);
    if (BELOPP_ANTAL != Storlek) return (uint32_t)-5;
    return (uint32_t)köra_app(BILD, Storlek, 0, 리눅스방식, "");
}
uintptr_t Tavla_användare_fil(void) { return köra_fil(0); }
uintptr_t 보드사용자리눅스파일(void) { return köra_fil(1); }
uintptr_t Tavla_användare_validera(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].data, 잘못된실행항목들[순번].Storlek) != användare_körbar_fil_fel) return 순번 + 1;
    return 0;
}
