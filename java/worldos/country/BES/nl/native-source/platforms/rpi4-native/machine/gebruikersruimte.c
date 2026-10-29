#include "../명명/기계연결이름.h"
#include "scherm_info.h"
// EL0 Uitvoeren_opdracht machine laag_WAARDE. bestand gegevens/정책은 기존 AOT Java 커널에 위임한다.
#include "gebruikersruimte.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../net_stack/net_stack.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define machine_register(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_distributor 0xff841000ul
#define IRQ_CPU_interface 0xff842000ul
#define paginaformaat 4096ul
#define toegang_markering (1ul << 10)
#define nee_Uitvoeren_machtiging (1ul << 53)
#define gebruiker_nee_Uitvoeren (1ul << 54)
#define normaal_Geheugen ((1ul << 2) | (3ul << 8) | toegang_markering)
#define kernel_page (3ul | normaal_Geheugen | nee_Uitvoeren_machtiging | gebruiker_nee_Uitvoeren)
#define gebruiker_lezen_schrijven (3ul | normaal_Geheugen | (1ul << 6) | nee_Uitvoeren_machtiging | gebruiker_nee_Uitvoeren)
#define gebruiker_alleen_lezen (3ul | normaal_Geheugen | (3ul << 6) | nee_Uitvoeren_machtiging | gebruiker_nee_Uitvoeren)
#define 사용자읽고실행 (3ul | normaal_Geheugen | (3ul << 6) | nee_Uitvoeren_machtiging)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t Bord_pixel(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t Bord_Terminal(uintptr_t);
extern int Terminal_In_behandeling(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),scherm_sms(int,int,const uint32_t *,unsigned);
extern void initialiseren_scherm(int),화면누름(int,unsigned);
extern int gebruiker_cv(gebruiker_frame *,void *);
extern void 사용자실수보관(void *);
extern int gebruiker_invoeren(uintptr_t beginpunt, uintptr_t stapelgeheugen, uintptr_t 전달값);
extern void gebruiker_Retour(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t wortel_ADRES[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t page_Lijst[gebruiker_page_AANTAL] __attribute__((aligned(4096)));
static uint8_t Machtigingen_Lijst[gebruiker_page_AANTAL];
static int Actief, bestandslijst[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int Sluiten_socket_eindpunt(unsigned bestandsingang){return bestandsingang<40?자바전문닫기(bestandsingang):자바흐름닫기(bestandsingang);}
static uint64_t INTERVAL, deadline_TIJD;
static uintptr_t heap_beëindigen;
// kernel_WAARDE 셸이 준비한 UTF-8 argumenten. EL0에는 kopiëren_WAARDE 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int onderbroken_Status,interactief,리눅스규약,bestandslijst[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char argument_MATRIX[8][256],Machtigingen_Lijst[gebruiker_page_AANTAL];
    uintptr_t dynamisch_geheugen; gebruiker_frame uitvoerbewerking_frame;
    unsigned char drijvende_komma_Status[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int eigenaar_object,interactief;
static uint32_t gebruikersnummer[4], gebruiker_START_TIJD[4], 사용자누적시각[4], gebruiker_uitvoerbewerking_TIJD[4], Volgende_gebruikersnummer=10;
static unsigned char gebruiker_opdracht_naam[4][288];
uint32_t 사용자상태읽기(unsigned invoer_WAARDE_962f286b, unsigned INDEX) {
    unsigned plaatsingsindex=INDEX&3;
    int Status_WAARDE=(Actief && eigenaar_object==(int)plaatsingsindex) ? 1 : 저장값[plaatsingsindex].onderbroken_Status ? 2 : 0;
    if (invoer_WAARDE_962f286b==0) return Status_WAARDE;
    if (!Status_WAARDE) return 0;
    if (invoer_WAARDE_962f286b==1) return gebruikersnummer[plaatsingsindex];
    if (invoer_WAARDE_962f286b==2) {
        unsigned char *쪽들=Status_WAARDE==1?Machtigingen_Lijst:저장값[plaatsingsindex].Machtigingen_Lijst;
        unsigned page_AANTAL=0; for (unsigned 순번=0; 순번<gebruiker_page_AANTAL; 순번++) if(쪽들[순번]) page_AANTAL++;
        return page_AANTAL*4;
    }
    if (invoer_WAARDE_962f286b==3) return (uint32_t)보드밀리초()-gebruiker_START_TIJD[plaatsingsindex];
    if (invoer_WAARDE_962f286b==4) return 사용자누적시각[plaatsingsindex]+(Status_WAARDE==1?(uint32_t)보드밀리초()-gebruiker_uitvoerbewerking_TIJD[plaatsingsindex]:0);
    if (invoer_WAARDE_962f286b==5) return INDEX/4<sizeof(gebruiker_opdracht_naam[0])?gebruiker_opdracht_naam[plaatsingsindex][INDEX/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t invoer_AANTAL_8f7753a1) {
    if (Actief || invoer_AANTAL_8f7753a1 > 8) return (uint32_t)-22;
    전달인수개수 = invoer_AANTAL_8f7753a1;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t ZOEKEN_INDEX, uintptr_t actueel_functie, uintptr_t byte_gegevens) {
    if (Actief || ZOEKEN_INDEX >= 전달인수개수 || actueel_functie >= 255 || actueel_functie != 전달인수길이[ZOEKEN_INDEX] || !byte_gegevens || byte_gegevens > 255)
        return (uint32_t)-22;
    전달인수[ZOEKEN_INDEX][actueel_functie] = byte_gegevens;
    전달인수길이[ZOEKEN_INDEX] = actueel_functie + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Klok_WAARDE(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Stop_TIMEOUT(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    machine_register(IRQ_distributor + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void START_TIMEOUT(void) {
    uint64_t 간격 = INTERVAL * 2, inschakelen = 1;
    deadline_TIJD = Klok_WAARDE() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(inschakelen) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned gegevensblok = 0; gegevensblok < 4; gegevensblok++) {
        wortel_ADRES[gegevensblok] = (uintptr_t)가운데[gegevensblok] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t ADRES = ((uintptr_t)gegevensblok << 30) | ((uintptr_t)순번 << 21);
            가운데[gegevensblok][순번] = ADRES | 1 | toegang_markering | gebruiker_nee_Uitvoeren;
            if (ADRES >= 0xfc000000ul) 가운데[gegevensblok][순번] |= nee_Uitvoeren_machtiging; // Device-nGnRnE
            else 가운데[gegevensblok][순번] |= normaal_Geheugen; // Normal, non-cacheable
        }
    }
    for (unsigned SECONDE_WAARDE = 0; SECONDE_WAARDE < gebruiker_page_AANTAL / 512; SECONDE_WAARDE++)
        가운데[0][(gebruiker_BASIS >> 21) + SECONDE_WAARDE] = (uintptr_t)(page_Lijst + SECONDE_WAARDE * 512) | 3;
    for (unsigned 순번 = 0; 순번 < gebruiker_page_AANTAL; 순번++) page_Lijst[순번] = (gebruiker_BASIS + 순번 * paginaformaat) | kernel_page;
    uint64_t Geheugen_kenmerk_register = 0x4400, ADRES_Vertaling_controle = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Geheugen_kenmerk_register), "r"(ADRES_Vertaling_controle), "r"((uintptr_t)wortel_ADRES) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t drijvende_komma_Status = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(drijvende_komma_Status) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(INTERVAL));
    Stop_TIMEOUT();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 beginpunt_WAARDE 때만 Toestaan_WAARDE.
    machine_register(IRQ_distributor) = 0;
    machine_register(IRQ_distributor + 0x180) = 0xffffffff;
    machine_register(IRQ_distributor + 0x80) = 0xffffffff;
    machine_register(IRQ_distributor + 0x280) = 1u << 30;
    machine_register(IRQ_distributor + 0x41c) = 0x80808080;
    machine_register(IRQ_distributor + 0x100) = 1u << 30;
    machine_register(IRQ_CPU_interface + 4) = 0xff;
    machine_register(IRQ_CPU_interface + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 informatie_normaal 확인할 nummer 있다.
    int Beveiliging = (machine_register(IRQ_distributor + 4) & (1u << 10)) != 0;
    machine_register(IRQ_distributor) = Beveiliging ? 1 : 3;
    machine_register(IRQ_CPU_interface) = Beveiliging ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t TYPE_gebied, machine_TYPE; uint32_t versienummer;
    uint64_t beginpunt, app_header_VERSCHUIVING, sectiekop_VERSCHUIVING; uint32_t configuratie_BITS;
    uint16_t uitvoerbaar_header_formaat_wijzigen, app_header_invoer_formaat_wijzigen, app_header_AANTAL, sectiekop_invoer_formaat_wijzigen, sectiekop_AANTAL, sectie_naam_tabel_INDEX;
} 실행파일머리;
typedef struct { uint32_t TYPE_gebied, configuratie_BITS; uint64_t VERSCHUIVING_WAARDE, ADRES, 물리주소, 파일영역크기, 기억영역크기, uitlijnen_grens; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(gebruiker_frame) == 272, "exception assembly layout");
static int 포함된범위(uint64_t VERSCHUIVING_WAARDE, uint64_t Grootte, uint64_t beëindigen_VERSCHUIVING) {
    return VERSCHUIVING_WAARDE <= beëindigen_VERSCHUIVING && Grootte <= beëindigen_VERSCHUIVING - VERSCHUIVING_WAARDE;
}
static int 부가정보검사(const unsigned char *gegevens_functie, size_t Grootte) {
    size_t actueel_functie = 0;
    while (포함된범위(actueel_functie, 12, Grootte)) {
        uint32_t 낱말들[3]; memcpy(낱말들, gegevens_functie + actueel_functie, 12); actueel_functie += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(actueel_functie, 이름영역크기, Grootte) || !포함된범위(actueel_functie + 이름영역크기, 설명크기, Grootte)) return 0;
        const unsigned char Naam[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Naam) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Naam); 순번++) if (gegevens_functie[actueel_functie + 순번] != Naam[순번]) 일치 = 0;
        uint32_t versienummer = 0;
        if (일치) memcpy(&versienummer, gegevens_functie + actueel_functie + 이름영역크기, 4);
        if (일치 && versienummer == 1) return 1;
        actueel_functie += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *gegevens, size_t Grootte, int 리눅스방식) {
    if (Grootte < sizeof(실행파일머리)) return gebruiker_uitvoerbaar_fout;
    실행파일머리 uitvoerbaar_header; memcpy(&uitvoerbaar_header, gegevens, sizeof(uitvoerbaar_header));
    if (uitvoerbaar_header.형식식별[0] != 127 || uitvoerbaar_header.형식식별[1] != 'E' || uitvoerbaar_header.형식식별[2] != 'L' || uitvoerbaar_header.형식식별[3] != 'F' ||
        uitvoerbaar_header.형식식별[4] != 2 || uitvoerbaar_header.형식식별[5] != 1 || uitvoerbaar_header.형식식별[6] != 1 || (uitvoerbaar_header.형식식별[7] != 0 && (!리눅스방식 || uitvoerbaar_header.형식식별[7] != 3)) ||
        uitvoerbaar_header.TYPE_gebied != 2 || uitvoerbaar_header.machine_TYPE != 183 || uitvoerbaar_header.versienummer != 1 || uitvoerbaar_header.configuratie_BITS || uitvoerbaar_header.uitvoerbaar_header_formaat_wijzigen != sizeof(uitvoerbaar_header) ||
        uitvoerbaar_header.app_header_invoer_formaat_wijzigen != sizeof(실행파일구획) || !uitvoerbaar_header.app_header_AANTAL || uitvoerbaar_header.app_header_AANTAL > 16 ||
        uitvoerbaar_header.app_header_VERSCHUIVING < sizeof(uitvoerbaar_header) || !포함된범위(uitvoerbaar_header.app_header_VERSCHUIVING, (uint64_t)uitvoerbaar_header.app_header_AANTAL * sizeof(실행파일구획), Grootte)) return gebruiker_uitvoerbaar_fout;
    uint8_t 사용량[(gebruiker_kopie_beëindigen - gebruiker_BASIS) / paginaformaat] = {0};
    int geldig_beginpunt = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < uitvoerbaar_header.app_header_AANTAL; 순번++) {
        실행파일구획 gegevens_functie; memcpy(&gegevens_functie, gegevens + uitvoerbaar_header.app_header_VERSCHUIVING + 순번 * sizeof(gegevens_functie), sizeof(gegevens_functie));
        if (gegevens_functie.TYPE_gebied == 4) {
            if (!포함된범위(gegevens_functie.VERSCHUIVING_WAARDE, gegevens_functie.파일영역크기, Grootte)) return gebruiker_uitvoerbaar_fout;
            if (부가정보검사(gegevens + gegevens_functie.VERSCHUIVING_WAARDE, gegevens_functie.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (gegevens_functie.TYPE_gebied == 0 || gegevens_functie.TYPE_gebied == 6 || (gegevens_functie.TYPE_gebied == 0x6474e551 && !(gegevens_functie.configuratie_BITS & 1))) continue;
        if (gegevens_functie.TYPE_gebied != 1) return gebruiker_uitvoerbaar_fout; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!gegevens_functie.기억영역크기) continue;
        if (gegevens_functie.configuratie_BITS & ~7u || !(gegevens_functie.configuratie_BITS & 4) || (gegevens_functie.configuratie_BITS & 3) == 3 || gegevens_functie.파일영역크기 > gegevens_functie.기억영역크기 ||
            (gegevens_functie.파일영역크기 && !포함된범위(gegevens_functie.VERSCHUIVING_WAARDE, gegevens_functie.파일영역크기, Grootte)) || gegevens_functie.ADRES < gebruiker_BASIS ||
            !포함된범위(gegevens_functie.ADRES, gegevens_functie.기억영역크기, gebruiker_kopie_beëindigen) ||
            (!리눅스방식 && ((gegevens_functie.ADRES & (paginaformaat - 1)) || (gegevens_functie.VERSCHUIVING_WAARDE & (paginaformaat - 1)) || gegevens_functie.uitlijnen_grens != paginaformaat)) ||
            (리눅스방식 && (((gegevens_functie.ADRES ^ gegevens_functie.VERSCHUIVING_WAARDE) & (paginaformaat - 1)) || !gegevens_functie.uitlijnen_grens ||
                (gegevens_functie.uitlijnen_grens & (gegevens_functie.uitlijnen_grens - 1)) || gegevens_functie.uitlijnen_grens > 0x200000 || ((gegevens_functie.ADRES ^ gegevens_functie.VERSCHUIVING_WAARDE) & (gegevens_functie.uitlijnen_grens - 1))))) return gebruiker_uitvoerbaar_fout;
        unsigned 첫항목 = (gegevens_functie.ADRES - gebruiker_BASIS) / paginaformaat;
        unsigned invoer_AANTAL_8f7753a1 = ((gegevens_functie.ADRES & (paginaformaat - 1)) + gegevens_functie.기억영역크기 + paginaformaat - 1) / paginaformaat;
        for (unsigned page_WAARDE = 첫항목; page_WAARDE < 첫항목 + invoer_AANTAL_8f7753a1; page_WAARDE++) {
            if (사용량[page_WAARDE]) return gebruiker_uitvoerbaar_fout;
            사용량[page_WAARDE] = 1;
        }
        if ((gegevens_functie.configuratie_BITS & 1) && uitvoerbaar_header.beginpunt >= gegevens_functie.ADRES && uitvoerbaar_header.beginpunt < gegevens_functie.ADRES + gegevens_functie.파일영역크기 && !(uitvoerbaar_header.beginpunt & 3)) geldig_beginpunt = 1;
        적재구획++;
    }
    return geldig_beginpunt && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : gebruiker_uitvoerbaar_fout;
}
int 사용자실행파일검사(const unsigned char *gegevens, size_t Grootte) { return 실행파일검사(gegevens, Grootte, 0); }
static void pagina_indeling(uintptr_t ADRES, uint64_t configuratie_BITS, unsigned machtigingen) {
    unsigned ZOEKEN_INDEX = (ADRES - gebruiker_BASIS) / paginaformaat;
    page_Lijst[ZOEKEN_INDEX] = ADRES | configuratie_BITS;
    Machtigingen_Lijst[ZOEKEN_INDEX] = machtigingen;
}
static int gebruiker_bereik(uintptr_t ADRES, size_t invoer_AANTAL_8f7753a1, int 쓰는중) {
    if (ADRES < gebruiker_BASIS || !포함된범위(ADRES, invoer_AANTAL_8f7753a1, gebruiker_beëindigen)) return 0;
    if (!invoer_AANTAL_8f7753a1) return 1;
    unsigned 첫항목 = (ADRES - gebruiker_BASIS) / paginaformaat, 마지막 = (ADRES + invoer_AANTAL_8f7753a1 - 1 - gebruiker_BASIS) / paginaformaat;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(Machtigingen_Lijst[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int kopiëren_pad(uintptr_t ADRES, char *pad) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!gebruiker_bereik(ADRES, 1, 0)) return -14;
        pad[순번] = *(const char *)ADRES++;
        if (!pad[순번]) return 0;
    }
    return -36;
}
static intptr_t kernel_HR(intptr_t resultaat) { return resultaat < 0 ? -foutnummer : resultaat; }
static int 대응파일기술자(uint64_t bestandsingang) { return bestandsingang >= 3 && bestandsingang < 19 ? bestandslijst[bestandsingang - 3] : -1; }
static int socket_eindpunt_eigenaar(uint64_t bestandsingang) { return bestandsingang >= 32 && bestandsingang < 56 && 통신끝점들[bestandsingang - 32]; }
static int ADRES_invoer(uintptr_t 가리킴값, size_t tijdsduur_WAARDE, struct pk_sockaddr_in *ADRES) {
    if (tijdsduur_WAARDE != sizeof(*ADRES)) return -22;
    if (!gebruiker_bereik(가리킴값, tijdsduur_WAARDE, 0)) return -14;
    memcpy(ADRES, (const void *)가리킴값, sizeof(*ADRES));
    return ADRES->sin_family == AF_INET ? 0 : -97;
}
static int ADRES_uitvoer_cheque(uintptr_t 가리킴값, uintptr_t tijdsduur_wijzer, pk_socklen_t *buffer_capaciteit) {
    if (!gebruiker_bereik(tijdsduur_wijzer, sizeof(*buffer_capaciteit), 1)) return -14;
    memcpy(buffer_capaciteit, (const void *)tijdsduur_wijzer, sizeof(*buffer_capaciteit));
    if (*buffer_capaciteit > sizeof(struct pk_sockaddr_in)) *buffer_capaciteit = sizeof(struct pk_sockaddr_in);
    if (*buffer_capaciteit && !gebruiker_bereik(가리킴값, *buffer_capaciteit, 1)) return -14;
    return 0;
}
static void ADRES_uitvoer(uintptr_t 가리킴값, uintptr_t tijdsduur_wijzer, pk_socklen_t buffer_capaciteit, int ADRES, int poortnummer) {
    struct pk_sockaddr_in WAARDE; memset(&WAARDE, 0, sizeof(WAARDE));
    WAARDE.sin_family = AF_INET; WAARDE.sin_port = pk_htons(poortnummer); WAARDE.sin_addr.s_addr = pk_htonl(ADRES);
    if (buffer_capaciteit) memcpy((void *)가리킴값, &WAARDE, buffer_capaciteit);
    pk_socklen_t tijdsduur_WAARDE = sizeof(WAARDE); memcpy((void *)tijdsduur_wijzer, &tijdsduur_WAARDE, sizeof(tijdsduur_WAARDE));
}
extern uintptr_t Bord_Kanaal(uintptr_t, uintptr_t);
static intptr_t systeemeigen_Systeem_Bellen(gebruiker_frame *Bestand_invoer) {
    uintptr_t 첫째값 = Bestand_invoer->register_gegevens[0], SECONDE_WAARDE = Bestand_invoer->register_gegevens[1], codepoint = Bestand_invoer->register_gegevens[2];
    char pad[65];
    int bestandsingang, resultaat;
    switch (Bestand_invoer->register_gegevens[8]) {
    case 0: return 1; // Eigen ABI 버전
    case 1: // write: wijzer 전체를 검사한 BACK_WAARDE tekstuitvoer/bestand wijzigen_WAARDE
        if (codepoint > 65536) return -22;
        if (!gebruiker_bereik(SECONDE_WAARDE, codepoint, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t START_uitvoer=Klok_WAARDE();
            for (size_t 순번 = 0; 순번 < codepoint; 순번++) Bord_Kanaal(첫째값, ((const unsigned char *)SECONDE_WAARDE)[순번]);
            /* 큰 tty를 그린 kernel_WAARDE 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(interactief){
                deadline_TIJD+=Klok_WAARDE()-START_uitvoer;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(deadline_TIJD) : "memory");
            }
            return codepoint;
        }
        if(첫째값>=40&&socket_eindpunt_eigenaar(첫째값)){
            size_t item_AANTAL=codepoint>512?512:codepoint;for(size_t 순번=0;순번<item_AANTAL;순번++)자바전문넣기(순번,((const unsigned char *)SECONDE_WAARDE)[순번]);return 자바흐름쓰기(첫째값,item_AANTAL);
        }
        bestandsingang = 대응파일기술자(첫째값); if (bestandsingang < 0) return -9;
        return kernel_HR(pk_write(bestandsingang, (const void *)SECONDE_WAARDE, codepoint));
    case 2:
        if (codepoint > 65536) return -22;
        if (!gebruiker_bereik(SECONDE_WAARDE, codepoint, 1)) return -14;
        if (첫째값 == 0) {
            size_t item_AANTAL = 0;
            while (item_AANTAL < codepoint) {
                int teken_WAARDE = (int32_t)보드글자읽기(); if (teken_WAARDE == -2) return item_AANTAL; if (teken_WAARDE < 0) break;
                ((unsigned char *)SECONDE_WAARDE)[item_AANTAL++] = teken_WAARDE;
            }
            return item_AANTAL ? (intptr_t)item_AANTAL : (codepoint ? -11 : 0);
        }
        if(첫째값>=40&&socket_eindpunt_eigenaar(첫째값)){
            resultaat=자바흐름읽기(첫째값,codepoint>512?512:codepoint);if(resultaat>0)for(int 순번=0;순번<resultaat;순번++)((unsigned char *)SECONDE_WAARDE)[순번]=자바전문얻기(순번);return resultaat;
        }
        bestandsingang = 대응파일기술자(첫째값); if (bestandsingang < 0) return -9;
        return kernel_HR(pk_read(bestandsingang, (void *)SECONDE_WAARDE, codepoint));
    case 3:
        resultaat = kopiëren_pad(첫째값, pad); if (resultaat) return resultaat;
        if (SECONDE_WAARDE > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (bestandslijst[순번] < 0) {
            bestandsingang = pk_open(pad, (int)SECONDE_WAARDE, 0600);
            if (bestandsingang < 0) return -foutnummer;
            bestandslijst[순번] = bestandsingang; return 순번 + 3;
        }
        return -24;
    case 4:
        if (socket_eindpunt_eigenaar(첫째값)) { resultaat = Sluiten_socket_eindpunt(첫째값); if (!resultaat) 통신끝점들[첫째값 - 32] = 0; return resultaat; }
        bestandsingang = 대응파일기술자(첫째값); if (bestandsingang < 0) return -9;
        resultaat = pk_close(bestandsingang); if (!resultaat) bestandslijst[첫째값 - 3] = -1;
        return kernel_HR(resultaat);
    case 5:
        bestandsingang = 대응파일기술자(첫째값); if (bestandsingang < 0) return -9;
        if (codepoint > 2) return -22;
        return kernel_HR(pk_lseek(bestandsingang, (int64_t)SECONDE_WAARDE, codepoint));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 gebruikersruimte RW/NX heap_WAARDE, 새로 노출되는 페이지는 0으로 initialiseren
        if (!첫째값) return heap_beëindigen;
        if (첫째값 < gebruiker_kopie_beëindigen || 첫째값 > gebruiker_heap_beëindigen) return -12;
        uintptr_t 이전쪽들 = (heap_beëindigen + paginaformaat - 1) & ~(paginaformaat - 1);
        uintptr_t 새쪽들 = (첫째값 + paginaformaat - 1) & ~(paginaformaat - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t gegevens_functie = 이전쪽들; gegevens_functie < 새쪽들; gegevens_functie += paginaformaat) pagina_indeling(gegevens_functie, kernel_page, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t gegevens_functie = 이전쪽들; gegevens_functie < 새쪽들; gegevens_functie += paginaformaat) pagina_indeling(gegevens_functie, gebruiker_lezen_schrijven, 3);
        } else {
            for (uintptr_t gegevens_functie = 새쪽들; gegevens_functie < 이전쪽들; gegevens_functie += paginaformaat) {
                page_Lijst[(gegevens_functie - gebruiker_BASIS) / paginaformaat] = 0; Machtigingen_Lijst[(gegevens_functie - gebruiker_BASIS) / paginaformaat] = 0;
            }
        }
        heap_beëindigen = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        bestandsingang = 대응파일기술자(첫째값); return bestandsingang < 0 ? -9 : kernel_HR(pk_size(bestandsingang));
    case 10:
        bestandsingang = 대응파일기술자(첫째값); return bestandsingang < 0 ? -9 : kernel_HR(pk_ftruncate(bestandsingang, (int64_t)SECONDE_WAARDE));
    case 11:
        resultaat = kopiëren_pad(첫째값, pad); return resultaat ? resultaat : kernel_HR(pk_unlink(pad));
    case 12:
        bestandsingang = 대응파일기술자(첫째값); return bestandsingang < 0 ? -9 : kernel_HR(pk_fsync(bestandsingang));
    case 13: { // 그래픽 기초 API: gebruikersruimte 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = Bestand_invoer->register_gegevens[3], aangevraagd_hoogte_WAARDE = Bestand_invoer->register_gegevens[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), scherm_tijdsduur = Bord_scherm_hoogte();
        if (첫째값 > 화면폭 || SECONDE_WAARDE > scherm_tijdsduur || 너비값 > 화면폭 - 첫째값 || aangevraagd_hoogte_WAARDE > scherm_tijdsduur - SECONDE_WAARDE) return -22;
        for (uintptr_t Y_coördinaat = SECONDE_WAARDE; Y_coördinaat < SECONDE_WAARDE + aangevraagd_hoogte_WAARDE; Y_coördinaat++) for (uintptr_t x_coördinaat = 첫째값; x_coördinaat < 첫째값 + 너비값; x_coördinaat++) Bord_pixel(x_coördinaat, Y_coördinaat, codepoint);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=item_AANTAL; args(index,buffer,capacity)=UTF-8 tijdsduur_WAARDE
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (codepoint <= 전달인수길이[첫째값]) return -36;
        if (!gebruiker_bereik(SECONDE_WAARDE, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SECONDE_WAARDE, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;interactief=1;return Bord_Terminal(13);}
        if(첫째값==2){interactief=0;return 0;}
        if(첫째값==3)return Bord_Terminal(13);
        if(첫째값!=1||!interactief)return -22;
        resultaat=(int32_t)보드글자읽기();
        if(resultaat==-4096)return resultaat;
        START_TIMEOUT();return resultaat<0?-11:resultaat;
    case 17: { // 유한한 협력 wachten_WAARDE: communicatie 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t beëindigen_TIJD = Klok_WAARDE() + INTERVAL * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Klok_WAARDE() < beëindigen_TIJD);
        START_TIMEOUT(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 bovenliggend_WAARDE·빈 폴더를 검사한다.
        if (SECONDE_WAARDE > 2) return -22;
        resultaat = kopiëren_pad(첫째값, pad); if (resultaat) return resultaat;
        unsigned tijdsduur_WAARDE = 0; while (pad[tijdsduur_WAARDE]) tijdsduur_WAARDE++;
        resultaat = 자바경로시작(tijdsduur_WAARDE); if (resultaat < 0) return resultaat;
        for (unsigned 순번 = 0; 순번 < tijdsduur_WAARDE; 순번++) 자바경로바이트(순번, (unsigned char)pad[순번]);
        return SECONDE_WAARDE == 0 ? 자바항목종류() : SECONDE_WAARDE == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int teken_WAARDE=(int32_t)보드글자읽기();if(teken_WAARDE==-4096)return teken_WAARDE;if(teken_WAARDE>=0)화면누름(eigenaar_object,teken_WAARDE);START_TIMEOUT();}
        if(첫째값==3&&codepoint){if(!자바셸대화형())return -95;interactief=1;Bord_Terminal(300);}
        return 화면호출(eigenaar_object,첫째값,SECONDE_WAARDE,codepoint,Bestand_invoer->register_gegevens[3],Bestand_invoer->register_gegevens[4],Bestand_invoer->register_gegevens[5]);
    case 21:
        if(codepoint>127)return -22;if(!gebruiker_bereik(SECONDE_WAARDE,codepoint*sizeof(uint32_t),0))return -14;
        return scherm_sms(eigenaar_object,첫째값,(const uint32_t *)SECONDE_WAARDE,codepoint);
    case 22: // scherm Grootte query_WAARDE: 0=너비, 1=hoogte_WAARDE. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : Bord_scherm_hoogte();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SECONDE_WAARDE==SOCK_STREAM&&(codepoint==0||codepoint==6))resultaat=자바흐름만들기();
        else if(SECONDE_WAARDE==SOCK_DGRAM&&(codepoint==0||codepoint==IPPROTO_UDP))resultaat=자바전문만들기(첫째값,SECONDE_WAARDE,codepoint);
        else return -93;
        if (resultaat >= 32 && resultaat < 56) 통신끝점들[resultaat - 32] = 1;
        return resultaat;
    case 33: {
        if (!socket_eindpunt_eigenaar(첫째값)) return -9;
        struct pk_sockaddr_in ADRES;
        resultaat = ADRES_invoer(SECONDE_WAARDE, codepoint, &ADRES); if (resultaat) return resultaat;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(ADRES.sin_addr.s_addr),pk_htons(ADRES.sin_port)):자바전문묶기(첫째값, pk_htonl(ADRES.sin_addr.s_addr), pk_htons(ADRES.sin_port));
    }
    case 34: {
        if (!socket_eindpunt_eigenaar(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Bestand_invoer->register_gegevens[3]) return -95;
        if (codepoint > 512) return -90;
        if (codepoint && !gebruiker_bereik(SECONDE_WAARDE, codepoint, 0)) return -14;
        struct pk_sockaddr_in ADRES;
        resultaat = ADRES_invoer(Bestand_invoer->register_gegevens[4], Bestand_invoer->register_gegevens[5], &ADRES); if (resultaat) return resultaat;
        for (unsigned 순번 = 0; 순번 < codepoint; 순번++) 자바전문넣기(순번, ((const unsigned char *)SECONDE_WAARDE)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(ADRES.sin_addr.s_addr), pk_htons(ADRES.sin_port), codepoint);
    }
    case 35: {
        if (!socket_eindpunt_eigenaar(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Bestand_invoer->register_gegevens[3]) return -95;
        if (codepoint > 512) return -90;
        if (codepoint && !gebruiker_bereik(SECONDE_WAARDE, codepoint, 1)) return -14;
        pk_socklen_t buffer_capaciteit = 0;
        if (Bestand_invoer->register_gegevens[4]) { resultaat = ADRES_uitvoer_cheque(Bestand_invoer->register_gegevens[4], Bestand_invoer->register_gegevens[5], &buffer_capaciteit); if (resultaat) return resultaat; }
        resultaat = 자바전문받기(첫째값, codepoint); if (resultaat < 0) return resultaat;
        for (int 순번 = 0; 순번 < resultaat; 순번++) ((unsigned char *)SECONDE_WAARDE)[순번] = 자바전문얻기(순번);
        if (Bestand_invoer->register_gegevens[4]) ADRES_uitvoer(Bestand_invoer->register_gegevens[4], Bestand_invoer->register_gegevens[5], buffer_capaciteit, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return resultaat;
    }
    case 36: {
        if (!socket_eindpunt_eigenaar(첫째값)) return -9;
        pk_socklen_t buffer_capaciteit;
        resultaat = ADRES_uitvoer_cheque(SECONDE_WAARDE, codepoint, &buffer_capaciteit); if (resultaat) return resultaat;
        ADRES_uitvoer(SECONDE_WAARDE,codepoint,buffer_capaciteit,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!socket_eindpunt_eigenaar(첫째값))return -9;struct pk_sockaddr_in ADRES;
        resultaat=ADRES_invoer(SECONDE_WAARDE,codepoint,&ADRES);if(resultaat)return resultaat;
        return 자바흐름연결(첫째값,pk_htonl(ADRES.sin_addr.s_addr),pk_htons(ADRES.sin_port));
    }
    case 38: return 첫째값>=40&&socket_eindpunt_eigenaar(첫째값)?자바흐름듣기(첫째값,SECONDE_WAARDE):-9;
    case 39:
        if(첫째값<40||!socket_eindpunt_eigenaar(첫째값))return -9;
        if(SECONDE_WAARDE||codepoint)return -95;resultaat=자바흐름연결받기(첫째값);if(resultaat>=40&&resultaat<56)통신끝점들[resultaat-32]=1;return resultaat;
    case 40: return 첫째값>=40&&socket_eindpunt_eigenaar(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t systeemaanroep(gebruiker_frame *Bestand_invoer) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(Bestand_invoer) : systeemeigen_Systeem_Bellen(Bestand_invoer);
}
static void Retour_kernel(gebruiker_frame *Bestand_invoer, int resultaat) {
    Stop_TIMEOUT();
    Bestand_invoer->register_gegevens[0] = (uint64_t)(int64_t)resultaat;
    Bestand_invoer->opdracht_functie = (uintptr_t)gebruiker_Retour;
    Bestand_invoer->Status_CODE = 0x3c5; // EL1h, DAIF masked
}
int gebruikersuitzondering(gebruiker_frame *Bestand_invoer, unsigned SNIJPUNT) {
    if (!Actief || (Bestand_invoer->Status_CODE & 15) != 0) return 0;
    if (SNIJPUNT) {
        uint32_t erkenning_WAARDE = machine_register(IRQ_CPU_interface + 0xc), id_WAARDE = erkenning_WAARDE & 1023;
        if (id_WAARDE == 30) { Retour_kernel(Bestand_invoer, gebruiker_TIMEOUT); machine_register(IRQ_CPU_interface + 0x10) = erkenning_WAARDE; return 1; }
        if (id_WAARDE < 1020) machine_register(IRQ_CPU_interface + 0x10) = erkenning_WAARDE;
        return 1;
    }
    uint64_t uitzondering_Status; __asm__ volatile("mrs %0, esr_el1" : "=r"(uitzondering_Status));
    if (Klok_WAARDE() >= deadline_TIJD) { Retour_kernel(Bestand_invoer, gebruiker_TIMEOUT); return 1; }
    unsigned uitzondering_gebied = uitzondering_Status >> 26;
    if (uitzondering_gebied == 0x15 && (uitzondering_Status & 0xffff) == 0) {
        if (리눅스규약 ? Bestand_invoer->register_gegevens[8] == 93 || Bestand_invoer->register_gegevens[8] == 94 : Bestand_invoer->register_gegevens[8] == 6) Retour_kernel(Bestand_invoer, (int)(Bestand_invoer->register_gegevens[0] & 255));
        else {
            intptr_t resultaat=systeemaanroep(Bestand_invoer);
            if(resultaat==-4096&&interactief){
                저장값[eigenaar_object].uitvoerbewerking_frame=*Bestand_invoer;저장값[eigenaar_object].uitvoerbewerking_frame.opdracht_functie-=4;
                사용자실수보관(저장값[eigenaar_object].drijvende_komma_Status);Retour_kernel(Bestand_invoer,사용자중단됨);
            }else Bestand_invoer->register_gegevens[0]=(uint64_t)resultaat;
        }
    } else Retour_kernel(Bestand_invoer, uitzondering_gebied == 0x24 ? gebruiker_gegevens_fout : uitzondering_gebied == 0x20 ? gebruiker_uitvoerbewerking_fout : gebruiker_nietig_instructie);
    return 1;
}

// 생성된 const ELF Groep_WAARDE: 실행은 반드시 app_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *gegevens; size_t Grootte; unsigned 전달값; } app;
#include "programs.h"
static void *snapshot(unsigned plaatsingsindex){return (void *)(0x04000000ul+plaatsingsindex*(gebruiker_beëindigen-gebruiker_BASIS));}
static int Voltooien_app(int resultaat){
    사용자누적시각[eigenaar_object]+=(uint32_t)보드밀리초()-gebruiker_uitvoerbewerking_TIJD[eigenaar_object];
    Stop_TIMEOUT();Actief=0;
    if(resultaat==사용자중단됨){
        저장된작업 *tekenreeks_gegevens=&저장값[eigenaar_object];tekenreeks_gegevens->onderbroken_Status=1;tekenreeks_gegevens->interactief=interactief;tekenreeks_gegevens->리눅스규약=리눅스규약;tekenreeks_gegevens->dynamisch_geheugen=heap_beëindigen;tekenreeks_gegevens->인수개수=전달인수개수;
        memcpy(tekenreeks_gegevens->Machtigingen_Lijst,Machtigingen_Lijst,sizeof(Machtigingen_Lijst));memcpy(tekenreeks_gegevens->bestandslijst,bestandslijst,sizeof(bestandslijst));memcpy(tekenreeks_gegevens->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(tekenreeks_gegevens->argument_MATRIX,전달인수,sizeof(전달인수));memcpy(tekenreeks_gegevens->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<gebruiker_page_AANTAL;순번++)if(Machtigingen_Lijst[순번])memcpy((unsigned char *)snapshot(eigenaar_object)+순번*paginaformaat,(void *)(gebruiker_BASIS+순번*paginaformaat),paginaformaat);
    }else{
        저장값[eigenaar_object].onderbroken_Status=0;initialiseren_scherm(eigenaar_object);
        for(unsigned 순번=0;순번<16;순번++)if(bestandslijst[순번]>=0)pk_close(bestandslijst[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])Sluiten_socket_eindpunt(순번+32);
    }
    for(unsigned 순번=0;순번<gebruiker_page_AANTAL;순번++){page_Lijst[순번]=0;Machtigingen_Lijst[순번]=0;}변환표맞추기();return resultaat;
}
uintptr_t Bord_gebruikersbesturingselement(uintptr_t Actie){
    unsigned plaatsingsindex=Actie&15;if(plaatsingsindex>=4||Actief)return (uint32_t)-22;
    저장된작업 *tekenreeks_gegevens=&저장값[plaatsingsindex];
    if(Actie>=32){if(tekenreeks_gegevens->onderbroken_Status){for(unsigned 순번=0;순번<16;순번++)if(tekenreeks_gegevens->bestandslijst[순번]>=0)pk_close(tekenreeks_gegevens->bestandslijst[순번]);for(unsigned 순번=0;순번<24;순번++)if(tekenreeks_gegevens->통신끝점들[순번])Sluiten_socket_eindpunt(순번+32);}tekenreeks_gegevens->onderbroken_Status=0;initialiseren_scherm(plaatsingsindex);return 0;}
    if(Actie>=16)return tekenreeks_gegevens->onderbroken_Status;
    if(!tekenreeks_gegevens->onderbroken_Status)return (uint32_t)-22;
    eigenaar_object=plaatsingsindex;interactief=tekenreeks_gegevens->interactief;리눅스규약=tekenreeks_gegevens->리눅스규약;heap_beëindigen=tekenreeks_gegevens->dynamisch_geheugen;전달인수개수=tekenreeks_gegevens->인수개수;
    memcpy(bestandslijst,tekenreeks_gegevens->bestandslijst,sizeof(bestandslijst));memcpy(통신끝점들,tekenreeks_gegevens->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,tekenreeks_gegevens->argument_MATRIX,sizeof(전달인수));memcpy(전달인수길이,tekenreeks_gegevens->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<gebruiker_page_AANTAL;순번++)page_Lijst[순번]=(gebruiker_BASIS+순번*paginaformaat)|kernel_page;변환표맞추기();
    memset((void *)gebruiker_BASIS,0,gebruiker_beëindigen-gebruiker_BASIS);
    for(unsigned 순번=0;순번<gebruiker_page_AANTAL;순번++)if(tekenreeks_gegevens->Machtigingen_Lijst[순번])memcpy((void *)(gebruiker_BASIS+순번*paginaformaat),(unsigned char *)snapshot(plaatsingsindex)+순번*paginaformaat,paginaformaat);
    memcpy(Machtigingen_Lijst,tekenreeks_gegevens->Machtigingen_Lijst,sizeof(Machtigingen_Lijst));
    for(unsigned 순번=0;순번<gebruiker_page_AANTAL;순번++){unsigned gegevens_functie=Machtigingen_Lijst[순번];page_Lijst[순번]=gegevens_functie?(gebruiker_BASIS+순번*paginaformaat)|(gegevens_functie==3?gebruiker_lezen_schrijven:gegevens_functie==5?사용자읽고실행:gebruiker_alleen_lezen):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");Actief=1;tekenreeks_gegevens->onderbroken_Status=0;START_TIMEOUT();
    gebruiker_uitvoerbewerking_TIJD[eigenaar_object]=보드밀리초();
    return (uint32_t)Voltooien_app(gebruiker_cv(&tekenreeks_gegevens->uitvoerbewerking_frame,tekenreeks_gegevens->drijvende_komma_Status));
}
static int uitvoeren_app(const unsigned char *gegevens, size_t Grootte, unsigned 전달값, int 리눅스방식, const char *Naam) {
    if (Actief) return -16;
    eigenaar_object=Bord_Terminal(11);if(eigenaar_object<0||eigenaar_object>3||저장값[eigenaar_object].onderbroken_Status)return -16;interactief=0;
    int geldig = 실행파일검사(gegevens, Grootte, 리눅스방식); if (geldig) return geldig;
    리눅스규약 = 리눅스방식;
    unsigned naam_INDEX=0;
    while (*Naam && naam_INDEX<31) gebruiker_opdracht_naam[eigenaar_object][naam_INDEX++]=(unsigned char)*Naam++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (naam_INDEX) gebruiker_opdracht_naam[eigenaar_object][naam_INDEX++]=' ';
        for (unsigned plaatsingsindex=0; plaatsingsindex<전달인수길이[0]; plaatsingsindex++) gebruiker_opdracht_naam[eigenaar_object][naam_INDEX++]=전달인수[0][plaatsingsindex];
    }
    gebruiker_opdracht_naam[eigenaar_object][naam_INDEX]=0; gebruikersnummer[eigenaar_object]=Volgende_gebruikersnummer++;
    if (Volgende_gebruikersnummer>0x7fffffffu) Volgende_gebruikersnummer=10;
    gebruiker_START_TIJD[eigenaar_object]=보드밀리초(); 사용자누적시각[eigenaar_object]=0;
    for (unsigned 순번 = 0; 순번 < gebruiker_page_AANTAL; 순번++) page_Lijst[순번] = (gebruiker_BASIS + 순번 * paginaformaat) | kernel_page;
    변환표맞추기();
    memset((void *)gebruiker_BASIS, 0, gebruiker_beëindigen - gebruiker_BASIS);
    memset(Machtigingen_Lijst, 0, sizeof(Machtigingen_Lijst));
    실행파일머리 uitvoerbaar_header; memcpy(&uitvoerbaar_header, gegevens, sizeof(uitvoerbaar_header));
    for (unsigned 순번 = 0; 순번 < uitvoerbaar_header.app_header_AANTAL; 순번++) {
        실행파일구획 gegevens_functie; memcpy(&gegevens_functie, gegevens + uitvoerbaar_header.app_header_VERSCHUIVING + 순번 * sizeof(gegevens_functie), sizeof(gegevens_functie));
        if (gegevens_functie.TYPE_gebied != 1 || !gegevens_functie.기억영역크기) continue;
        if (gegevens_functie.파일영역크기) memcpy((void *)(uintptr_t)gegevens_functie.ADRES, gegevens + gegevens_functie.VERSCHUIVING_WAARDE, gegevens_functie.파일영역크기);
        for (uintptr_t actueel_functie = gegevens_functie.ADRES & ~(paginaformaat - 1); actueel_functie < gegevens_functie.ADRES + gegevens_functie.기억영역크기; actueel_functie += paginaformaat) {
            Machtigingen_Lijst[(actueel_functie - gebruiker_BASIS) / paginaformaat] = (gegevens_functie.configuratie_BITS & 2) ? 3 : ((gegevens_functie.configuratie_BITS & 1) ? 5 : 1);
        }
    }
    for (uintptr_t actueel_functie = gebruiker_stack_ADRES; actueel_functie < gebruiker_beëindigen; actueel_functie += paginaformaat) Machtigingen_Lijst[(actueel_functie - gebruiker_BASIS) / paginaformaat] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(uitvoerbaar_header.beginpunt) : gebruiker_beëindigen;
    for (unsigned 순번 = 0; 순번 < gebruiker_page_AANTAL; 순번++) {
        unsigned machtigingen = Machtigingen_Lijst[순번];
        page_Lijst[순번] = machtigingen ? (gebruiker_BASIS + 순번 * paginaformaat) | (machtigingen == 3 ? gebruiker_lezen_schrijven : machtigingen == 5 ? 사용자읽고실행 : gebruiker_alleen_lezen) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) bestandslijst[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    heap_beëindigen = gebruiker_kopie_beëindigen;
    Actief = 1; START_TIMEOUT();
    gebruiker_uitvoerbewerking_TIJD[eigenaar_object]=보드밀리초();
    int resultaat = gebruiker_invoeren(uitvoerbaar_header.beginpunt, 초기쌓임공간, 전달값);
    return Voltooien_app(resultaat);
}
uintptr_t Bord_gebruiker_uitvoeren(uintptr_t ZOEKEN_INDEX) {
    if (ZOEKEN_INDEX >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Naam=ZOEKEN_INDEX==10?"javac":ZOEKEN_INDEX==11?"java":ZOEKEN_INDEX==12?"python":ZOEKEN_INDEX==13?"vi":ZOEKEN_INDEX==14?"jar":ZOEKEN_INDEX==15?"cc":ZOEKEN_INDEX==16?"jaot":"ELF";
    return (uint32_t)uitvoeren_app(실행항목들[ZOEKEN_INDEX].gegevens, 실행항목들[ZOEKEN_INDEX].Grootte, 실행항목들[ZOEKEN_INDEX].전달값, 0, Naam);
}
static uintptr_t Uitvoeren_Bestand(int 리눅스방식) {
    static unsigned char kopie[16384];
    if (Actief || !전달인수개수) return (uint32_t)-22;
    int bestandsingang = pk_open((const char *)전달인수[0], alleen_lezen_WAARDE, 0);
    if (bestandsingang < 0) return (uint32_t)-foutnummer;
    int Grootte = pk_size(bestandsingang);
    if (Grootte < 0 || (unsigned)Grootte > sizeof(kopie)) { pk_close(bestandsingang); return (uint32_t)-27; }
    int OPBRENGST_AANTAL = pk_read(bestandsingang, kopie, Grootte); pk_close(bestandsingang);
    if (OPBRENGST_AANTAL != Grootte) return (uint32_t)-5;
    return (uint32_t)uitvoeren_app(kopie, Grootte, 0, 리눅스방식, "");
}
uintptr_t Bord_gebruiker_Bestand(void) { return Uitvoeren_Bestand(0); }
uintptr_t 보드사용자리눅스파일(void) { return Uitvoeren_Bestand(1); }
uintptr_t Bord_gebruiker_valideren(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].gegevens, 잘못된실행항목들[순번].Grootte) != gebruiker_uitvoerbaar_fout) return 순번 + 1;
    return 0;
}
