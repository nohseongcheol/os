#include "../명명/기계연결이름.h"
#include "skjermbilde_info.h"
// EL0 Utfør_kommando maskin lag_VERDI. Fil data/정책은 기존 AOT Java 커널에 위임한다.
#include "bruker.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../nettverk_stakk/nettverk_stakk.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define maskin_register(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_distributør 0xff841000ul
#define IRQ_CPU_grensesnitt 0xff842000ul
#define sidestørrelse 4096ul
#define tilgang_tusj (1ul << 10)
#define nei_Utfør_tillatelse (1ul << 53)
#define bruker_nei_Utfør (1ul << 54)
#define normal_Minne ((1ul << 2) | (3ul << 8) | tilgang_tusj)
#define kjerne_page (3ul | normal_Minne | nei_Utfør_tillatelse | bruker_nei_Utfør)
#define bruker_lese_og_skrive (3ul | normal_Minne | (1ul << 6) | nei_Utfør_tillatelse | bruker_nei_Utfør)
#define bruker_skrivebeskyttet (3ul | normal_Minne | (3ul << 6) | nei_Utfør_tillatelse | bruker_nei_Utfør)
#define 사용자읽고실행 (3ul | normal_Minne | (3ul << 6) | nei_Utfør_tillatelse)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t Tavle_piksel(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t Tavle_Terminal(uintptr_t);
extern int Terminal_Venter(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),skjermbilde_SMS(int,int,const uint32_t *,unsigned);
extern void starte_skjermbilde(int),화면누름(int,unsigned);
extern int bruker_CV(bruker_bilde *,void *);
extern void 사용자실수보관(void *);
extern int bruker_angi(uintptr_t inngangspunkt, uintptr_t stakk_lager, uintptr_t 전달값);
extern void bruker_return(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t rot_e_post[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t page_Liste[bruker_page_ANTALL] __attribute__((aligned(4096)));
static uint8_t tillatelse_Liste[bruker_page_ANTALL];
static int Aktiv, filliste[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int Lukk_socket_deltaker(unsigned Fil_håndtak){return Fil_håndtak<40?자바전문닫기(Fil_håndtak):자바흐름닫기(Fil_håndtak);}
static uint64_t FREKVENS, tidsfrist_TID;
static uintptr_t heap_avslutte_en_samtale;
// kjerne_VERDI 셸이 준비한 UTF-8 Argumenter. EL0에는 kopiere_VERDI 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,interaktiv,리눅스규약,filliste[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char argument_MATRISE[8][256],tillatelse_Liste[bruker_page_ANTALL];
    uintptr_t heap_lager; bruker_bilde kjøring_bilde;
    unsigned char flyttall_status[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int eier_objekt,interaktiv;
static uint32_t brukernummer[4], bruker_START_TID[4], 사용자누적시각[4], bruker_kjøring_TID[4], Neste_brukernummer=10;
static unsigned char bruker_kommando_navn[4][288];
uint32_t 사용자상태읽기(unsigned oppføring_VERDI, unsigned INDEKS) {
    unsigned posisjonsindeks=INDEKS&3;
    int status_VERDI=(Aktiv && eier_objekt==(int)posisjonsindeks) ? 1 : 저장값[posisjonsindeks].멈춤상태 ? 2 : 0;
    if (oppføring_VERDI==0) return status_VERDI;
    if (!status_VERDI) return 0;
    if (oppføring_VERDI==1) return brukernummer[posisjonsindeks];
    if (oppføring_VERDI==2) {
        unsigned char *쪽들=status_VERDI==1?tillatelse_Liste:저장값[posisjonsindeks].tillatelse_Liste;
        unsigned page_ANTALL=0; for (unsigned 순번=0; 순번<bruker_page_ANTALL; 순번++) if(쪽들[순번]) page_ANTALL++;
        return page_ANTALL*4;
    }
    if (oppføring_VERDI==3) return (uint32_t)보드밀리초()-bruker_START_TID[posisjonsindeks];
    if (oppføring_VERDI==4) return 사용자누적시각[posisjonsindeks]+(status_VERDI==1?(uint32_t)보드밀리초()-bruker_kjøring_TID[posisjonsindeks]:0);
    if (oppføring_VERDI==5) return INDEKS/4<sizeof(bruker_kommando_navn[0])?bruker_kommando_navn[posisjonsindeks][INDEKS/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t oppføring_ANTALL) {
    if (Aktiv || oppføring_ANTALL > 8) return (uint32_t)-22;
    전달인수개수 = oppføring_ANTALL;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t Oppslag_INDEKS, uintptr_t betalt_plassere, uintptr_t byte_data) {
    if (Aktiv || Oppslag_INDEKS >= 전달인수개수 || betalt_plassere >= 255 || betalt_plassere != 전달인수길이[Oppslag_INDEKS] || !byte_data || byte_data > 255)
        return (uint32_t)-22;
    전달인수[Oppslag_INDEKS][betalt_plassere] = byte_data;
    전달인수길이[Oppslag_INDEKS] = betalt_plassere + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Klokke_VERDI(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Stopp_TIMEOUT(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    maskin_register(IRQ_distributør + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void START_TIMEOUT(void) {
    uint64_t 간격 = FREKVENS * 2, aktivere = 1;
    tidsfrist_TID = Klokke_VERDI() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(aktivere) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned data_blokk = 0; data_blokk < 4; data_blokk++) {
        rot_e_post[data_blokk] = (uintptr_t)가운데[data_blokk] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t e_post = ((uintptr_t)data_blokk << 30) | ((uintptr_t)순번 << 21);
            가운데[data_blokk][순번] = e_post | 1 | tilgang_tusj | bruker_nei_Utfør;
            if (e_post >= 0xfc000000ul) 가운데[data_blokk][순번] |= nei_Utfør_tillatelse; // Device-nGnRnE
            else 가운데[data_blokk][순번] |= normal_Minne; // Normal, non-cacheable
        }
    }
    for (unsigned SEKUND_VERDI = 0; SEKUND_VERDI < bruker_page_ANTALL / 512; SEKUND_VERDI++)
        가운데[0][(bruker_grunnlag >> 21) + SEKUND_VERDI] = (uintptr_t)(page_Liste + SEKUND_VERDI * 512) | 3;
    for (unsigned 순번 = 0; 순번 < bruker_page_ANTALL; 순번++) page_Liste[순번] = (bruker_grunnlag + 순번 * sidestørrelse) | kjerne_page;
    uint64_t Minne_attributt_register = 0x4400, e_post_Oversettelse_kontroll = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Minne_attributt_register), "r"(e_post_Oversettelse_kontroll), "r"((uintptr_t)rot_e_post) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t flyttall_status = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(flyttall_status) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREKVENS));
    Stopp_TIMEOUT();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 inngangspunkt_VERDI 때만 Tillat_VERDI.
    maskin_register(IRQ_distributør) = 0;
    maskin_register(IRQ_distributør + 0x180) = 0xffffffff;
    maskin_register(IRQ_distributør + 0x80) = 0xffffffff;
    maskin_register(IRQ_distributør + 0x280) = 1u << 30;
    maskin_register(IRQ_distributør + 0x41c) = 0x80808080;
    maskin_register(IRQ_distributør + 0x100) = 1u << 30;
    maskin_register(IRQ_CPU_grensesnitt + 4) = 0xff;
    maskin_register(IRQ_CPU_grensesnitt + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 informasjonssystemer_normal 확인할 nummer 있다.
    int Sikkerhet = (maskin_register(IRQ_distributør + 4) & (1u << 10)) != 0;
    maskin_register(IRQ_distributør) = Sikkerhet ? 1 : 3;
    maskin_register(IRQ_CPU_grensesnitt) = Sikkerhet ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t Type_område, maskin_Type; uint32_t versjonsnummer;
    uint64_t inngangspunkt, app_Topptekst_FORSKYVNING, deloverskrift_FORSKYVNING; uint32_t konfigurasjon_BITS;
    uint16_t kjørbar_fil_Topptekst_skalere, app_Topptekst_oppføring_skalere, app_Topptekst_ANTALL, deloverskrift_oppføring_skalere, deloverskrift_ANTALL, inndeling_navn_tabell_INDEKS;
} 실행파일머리;
typedef struct { uint32_t Type_område, konfigurasjon_BITS; uint64_t FORSKYVNING_VERDI, e_post, 물리주소, 파일영역크기, 기억영역크기, justere_grense; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(bruker_bilde) == 272, "exception assembly layout");
static int 포함된범위(uint64_t FORSKYVNING_VERDI, uint64_t Størrelse, uint64_t avslutte_en_samtale_FORSKYVNING) {
    return FORSKYVNING_VERDI <= avslutte_en_samtale_FORSKYVNING && Størrelse <= avslutte_en_samtale_FORSKYVNING - FORSKYVNING_VERDI;
}
static int 부가정보검사(const unsigned char *data_plassere, size_t Størrelse) {
    size_t betalt_plassere = 0;
    while (포함된범위(betalt_plassere, 12, Størrelse)) {
        uint32_t 낱말들[3]; memcpy(낱말들, data_plassere + betalt_plassere, 12); betalt_plassere += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(betalt_plassere, 이름영역크기, Størrelse) || !포함된범위(betalt_plassere + 이름영역크기, 설명크기, Størrelse)) return 0;
        const unsigned char Navn[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Navn) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Navn); 순번++) if (data_plassere[betalt_plassere + 순번] != Navn[순번]) 일치 = 0;
        uint32_t versjonsnummer = 0;
        if (일치) memcpy(&versjonsnummer, data_plassere + betalt_plassere + 이름영역크기, 4);
        if (일치 && versjonsnummer == 1) return 1;
        betalt_plassere += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *data, size_t Størrelse, int 리눅스방식) {
    if (Størrelse < sizeof(실행파일머리)) return bruker_kjørbar_fil_feil;
    실행파일머리 kjørbar_fil_Topptekst; memcpy(&kjørbar_fil_Topptekst, data, sizeof(kjørbar_fil_Topptekst));
    if (kjørbar_fil_Topptekst.형식식별[0] != 127 || kjørbar_fil_Topptekst.형식식별[1] != 'E' || kjørbar_fil_Topptekst.형식식별[2] != 'L' || kjørbar_fil_Topptekst.형식식별[3] != 'F' ||
        kjørbar_fil_Topptekst.형식식별[4] != 2 || kjørbar_fil_Topptekst.형식식별[5] != 1 || kjørbar_fil_Topptekst.형식식별[6] != 1 || (kjørbar_fil_Topptekst.형식식별[7] != 0 && (!리눅스방식 || kjørbar_fil_Topptekst.형식식별[7] != 3)) ||
        kjørbar_fil_Topptekst.Type_område != 2 || kjørbar_fil_Topptekst.maskin_Type != 183 || kjørbar_fil_Topptekst.versjonsnummer != 1 || kjørbar_fil_Topptekst.konfigurasjon_BITS || kjørbar_fil_Topptekst.kjørbar_fil_Topptekst_skalere != sizeof(kjørbar_fil_Topptekst) ||
        kjørbar_fil_Topptekst.app_Topptekst_oppføring_skalere != sizeof(실행파일구획) || !kjørbar_fil_Topptekst.app_Topptekst_ANTALL || kjørbar_fil_Topptekst.app_Topptekst_ANTALL > 16 ||
        kjørbar_fil_Topptekst.app_Topptekst_FORSKYVNING < sizeof(kjørbar_fil_Topptekst) || !포함된범위(kjørbar_fil_Topptekst.app_Topptekst_FORSKYVNING, (uint64_t)kjørbar_fil_Topptekst.app_Topptekst_ANTALL * sizeof(실행파일구획), Størrelse)) return bruker_kjørbar_fil_feil;
    uint8_t 사용량[(bruker_BILDE_avslutte_en_samtale - bruker_grunnlag) / sidestørrelse] = {0};
    int gyldig_inngangspunkt = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < kjørbar_fil_Topptekst.app_Topptekst_ANTALL; 순번++) {
        실행파일구획 data_plassere; memcpy(&data_plassere, data + kjørbar_fil_Topptekst.app_Topptekst_FORSKYVNING + 순번 * sizeof(data_plassere), sizeof(data_plassere));
        if (data_plassere.Type_område == 4) {
            if (!포함된범위(data_plassere.FORSKYVNING_VERDI, data_plassere.파일영역크기, Størrelse)) return bruker_kjørbar_fil_feil;
            if (부가정보검사(data + data_plassere.FORSKYVNING_VERDI, data_plassere.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (data_plassere.Type_område == 0 || data_plassere.Type_område == 6 || (data_plassere.Type_område == 0x6474e551 && !(data_plassere.konfigurasjon_BITS & 1))) continue;
        if (data_plassere.Type_område != 1) return bruker_kjørbar_fil_feil; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!data_plassere.기억영역크기) continue;
        if (data_plassere.konfigurasjon_BITS & ~7u || !(data_plassere.konfigurasjon_BITS & 4) || (data_plassere.konfigurasjon_BITS & 3) == 3 || data_plassere.파일영역크기 > data_plassere.기억영역크기 ||
            (data_plassere.파일영역크기 && !포함된범위(data_plassere.FORSKYVNING_VERDI, data_plassere.파일영역크기, Størrelse)) || data_plassere.e_post < bruker_grunnlag ||
            !포함된범위(data_plassere.e_post, data_plassere.기억영역크기, bruker_BILDE_avslutte_en_samtale) ||
            (!리눅스방식 && ((data_plassere.e_post & (sidestørrelse - 1)) || (data_plassere.FORSKYVNING_VERDI & (sidestørrelse - 1)) || data_plassere.justere_grense != sidestørrelse)) ||
            (리눅스방식 && (((data_plassere.e_post ^ data_plassere.FORSKYVNING_VERDI) & (sidestørrelse - 1)) || !data_plassere.justere_grense ||
                (data_plassere.justere_grense & (data_plassere.justere_grense - 1)) || data_plassere.justere_grense > 0x200000 || ((data_plassere.e_post ^ data_plassere.FORSKYVNING_VERDI) & (data_plassere.justere_grense - 1))))) return bruker_kjørbar_fil_feil;
        unsigned 첫항목 = (data_plassere.e_post - bruker_grunnlag) / sidestørrelse;
        unsigned oppføring_ANTALL = ((data_plassere.e_post & (sidestørrelse - 1)) + data_plassere.기억영역크기 + sidestørrelse - 1) / sidestørrelse;
        for (unsigned page_VERDI = 첫항목; page_VERDI < 첫항목 + oppføring_ANTALL; page_VERDI++) {
            if (사용량[page_VERDI]) return bruker_kjørbar_fil_feil;
            사용량[page_VERDI] = 1;
        }
        if ((data_plassere.konfigurasjon_BITS & 1) && kjørbar_fil_Topptekst.inngangspunkt >= data_plassere.e_post && kjørbar_fil_Topptekst.inngangspunkt < data_plassere.e_post + data_plassere.파일영역크기 && !(kjørbar_fil_Topptekst.inngangspunkt & 3)) gyldig_inngangspunkt = 1;
        적재구획++;
    }
    return gyldig_inngangspunkt && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : bruker_kjørbar_fil_feil;
}
int 사용자실행파일검사(const unsigned char *data, size_t Størrelse) { return 실행파일검사(data, Størrelse, 0); }
static void sideoppsett(uintptr_t e_post, uint64_t konfigurasjon_BITS, unsigned tillatelse) {
    unsigned Oppslag_INDEKS = (e_post - bruker_grunnlag) / sidestørrelse;
    page_Liste[Oppslag_INDEKS] = e_post | konfigurasjon_BITS;
    tillatelse_Liste[Oppslag_INDEKS] = tillatelse;
}
static int bruker_område(uintptr_t e_post, size_t oppføring_ANTALL, int 쓰는중) {
    if (e_post < bruker_grunnlag || !포함된범위(e_post, oppføring_ANTALL, bruker_avslutte_en_samtale)) return 0;
    if (!oppføring_ANTALL) return 1;
    unsigned 첫항목 = (e_post - bruker_grunnlag) / sidestørrelse, 마지막 = (e_post + oppføring_ANTALL - 1 - bruker_grunnlag) / sidestørrelse;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(tillatelse_Liste[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int kopiere_bane(uintptr_t e_post, char *Sti) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!bruker_område(e_post, 1, 0)) return -14;
        Sti[순번] = *(const char *)e_post++;
        if (!Sti[순번]) return 0;
    }
    return -36;
}
static intptr_t kjerne_KR(intptr_t KR) { return KR < 0 ? -feilnummer : KR; }
static int 대응파일기술자(uint64_t Fil_håndtak) { return Fil_håndtak >= 3 && Fil_håndtak < 19 ? filliste[Fil_håndtak - 3] : -1; }
static int socket_deltaker_eier(uint64_t Fil_håndtak) { return Fil_håndtak >= 32 && Fil_håndtak < 56 && 통신끝점들[Fil_håndtak - 32]; }
static int e_post_inndata(uintptr_t 가리킴값, size_t lengde_VERDI, struct pk_sockaddr_in *e_post) {
    if (lengde_VERDI != sizeof(*e_post)) return -22;
    if (!bruker_område(가리킴값, lengde_VERDI, 0)) return -14;
    memcpy(e_post, (const void *)가리킴값, sizeof(*e_post));
    return e_post->sin_family == AF_INET ? 0 : -97;
}
static int e_post_produksjon_sjekk(uintptr_t 가리킴값, uintptr_t lengde_peker, pk_socklen_t *bufre_kapasitet) {
    if (!bruker_område(lengde_peker, sizeof(*bufre_kapasitet), 1)) return -14;
    memcpy(bufre_kapasitet, (const void *)lengde_peker, sizeof(*bufre_kapasitet));
    if (*bufre_kapasitet > sizeof(struct pk_sockaddr_in)) *bufre_kapasitet = sizeof(struct pk_sockaddr_in);
    if (*bufre_kapasitet && !bruker_område(가리킴값, *bufre_kapasitet, 1)) return -14;
    return 0;
}
static void e_post_produksjon(uintptr_t 가리킴값, uintptr_t lengde_peker, pk_socklen_t bufre_kapasitet, int e_post, int portnummer) {
    struct pk_sockaddr_in VERDI; memset(&VERDI, 0, sizeof(VERDI));
    VERDI.sin_family = AF_INET; VERDI.sin_port = pk_htons(portnummer); VERDI.sin_addr.s_addr = pk_htonl(e_post);
    if (bufre_kapasitet) memcpy((void *)가리킴값, &VERDI, bufre_kapasitet);
    pk_socklen_t lengde_VERDI = sizeof(VERDI); memcpy((void *)lengde_peker, &lengde_VERDI, sizeof(lengde_VERDI));
}
extern uintptr_t Tavle_Kanal(uintptr_t, uintptr_t);
static intptr_t opprinnelig_System_Ring(bruker_bilde *Fil_oppføring) {
    uintptr_t 첫째값 = Fil_oppføring->register_data[0], SEKUND_VERDI = Fil_oppføring->register_data[1], tegnkode = Fil_oppføring->register_data[2];
    char Sti[65];
    int Fil_håndtak, KR;
    switch (Fil_oppføring->register_data[8]) {
    case 0: return 1; // eget ABI 버전
    case 1: // write: peker 전체를 검사한 TILBAKE_VERDI Utgang/Fil endre_VERDI
        if (tegnkode > 65536) return -22;
        if (!bruker_område(SEKUND_VERDI, tegnkode, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t START_produksjon=Klokke_VERDI();
            for (size_t 순번 = 0; 순번 < tegnkode; 순번++) Tavle_Kanal(첫째값, ((const unsigned char *)SEKUND_VERDI)[순번]);
            /* 큰 tty를 그린 kjerne_VERDI 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(interaktiv){
                tidsfrist_TID+=Klokke_VERDI()-START_produksjon;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(tidsfrist_TID) : "memory");
            }
            return tegnkode;
        }
        if(첫째값>=40&&socket_deltaker_eier(첫째값)){
            size_t vare_ANTALL=tegnkode>512?512:tegnkode;for(size_t 순번=0;순번<vare_ANTALL;순번++)자바전문넣기(순번,((const unsigned char *)SEKUND_VERDI)[순번]);return 자바흐름쓰기(첫째값,vare_ANTALL);
        }
        Fil_håndtak = 대응파일기술자(첫째값); if (Fil_håndtak < 0) return -9;
        return kjerne_KR(pk_write(Fil_håndtak, (const void *)SEKUND_VERDI, tegnkode));
    case 2:
        if (tegnkode > 65536) return -22;
        if (!bruker_område(SEKUND_VERDI, tegnkode, 1)) return -14;
        if (첫째값 == 0) {
            size_t vare_ANTALL = 0;
            while (vare_ANTALL < tegnkode) {
                int tegn_VERDI = (int32_t)보드글자읽기(); if (tegn_VERDI == -2) return vare_ANTALL; if (tegn_VERDI < 0) break;
                ((unsigned char *)SEKUND_VERDI)[vare_ANTALL++] = tegn_VERDI;
            }
            return vare_ANTALL ? (intptr_t)vare_ANTALL : (tegnkode ? -11 : 0);
        }
        if(첫째값>=40&&socket_deltaker_eier(첫째값)){
            KR=자바흐름읽기(첫째값,tegnkode>512?512:tegnkode);if(KR>0)for(int 순번=0;순번<KR;순번++)((unsigned char *)SEKUND_VERDI)[순번]=자바전문얻기(순번);return KR;
        }
        Fil_håndtak = 대응파일기술자(첫째값); if (Fil_håndtak < 0) return -9;
        return kjerne_KR(pk_read(Fil_håndtak, (void *)SEKUND_VERDI, tegnkode));
    case 3:
        KR = kopiere_bane(첫째값, Sti); if (KR) return KR;
        if (SEKUND_VERDI > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (filliste[순번] < 0) {
            Fil_håndtak = pk_open(Sti, (int)SEKUND_VERDI, 0600);
            if (Fil_håndtak < 0) return -feilnummer;
            filliste[순번] = Fil_håndtak; return 순번 + 3;
        }
        return -24;
    case 4:
        if (socket_deltaker_eier(첫째값)) { KR = Lukk_socket_deltaker(첫째값); if (!KR) 통신끝점들[첫째값 - 32] = 0; return KR; }
        Fil_håndtak = 대응파일기술자(첫째값); if (Fil_håndtak < 0) return -9;
        KR = pk_close(Fil_håndtak); if (!KR) filliste[첫째값 - 3] = -1;
        return kjerne_KR(KR);
    case 5:
        Fil_håndtak = 대응파일기술자(첫째값); if (Fil_håndtak < 0) return -9;
        if (tegnkode > 2) return -22;
        return kjerne_KR(pk_lseek(Fil_håndtak, (int64_t)SEKUND_VERDI, tegnkode));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 bruker RW/NX heap_VERDI, 새로 노출되는 페이지는 0으로 starte
        if (!첫째값) return heap_avslutte_en_samtale;
        if (첫째값 < bruker_BILDE_avslutte_en_samtale || 첫째값 > bruker_heap_avslutte_en_samtale) return -12;
        uintptr_t 이전쪽들 = (heap_avslutte_en_samtale + sidestørrelse - 1) & ~(sidestørrelse - 1);
        uintptr_t 새쪽들 = (첫째값 + sidestørrelse - 1) & ~(sidestørrelse - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t data_plassere = 이전쪽들; data_plassere < 새쪽들; data_plassere += sidestørrelse) sideoppsett(data_plassere, kjerne_page, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t data_plassere = 이전쪽들; data_plassere < 새쪽들; data_plassere += sidestørrelse) sideoppsett(data_plassere, bruker_lese_og_skrive, 3);
        } else {
            for (uintptr_t data_plassere = 새쪽들; data_plassere < 이전쪽들; data_plassere += sidestørrelse) {
                page_Liste[(data_plassere - bruker_grunnlag) / sidestørrelse] = 0; tillatelse_Liste[(data_plassere - bruker_grunnlag) / sidestørrelse] = 0;
            }
        }
        heap_avslutte_en_samtale = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        Fil_håndtak = 대응파일기술자(첫째값); return Fil_håndtak < 0 ? -9 : kjerne_KR(pk_size(Fil_håndtak));
    case 10:
        Fil_håndtak = 대응파일기술자(첫째값); return Fil_håndtak < 0 ? -9 : kjerne_KR(pk_ftruncate(Fil_håndtak, (int64_t)SEKUND_VERDI));
    case 11:
        KR = kopiere_bane(첫째값, Sti); return KR ? KR : kjerne_KR(pk_unlink(Sti));
    case 12:
        Fil_håndtak = 대응파일기술자(첫째값); return Fil_håndtak < 0 ? -9 : kjerne_KR(pk_fsync(Fil_håndtak));
    case 13: { // 그래픽 기초 API: bruker 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = Fil_oppføring->register_data[3], 높이값 = Fil_oppføring->register_data[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), skjermbilde_lengde = 보드화면높이();
        if (첫째값 > 화면폭 || SEKUND_VERDI > skjermbilde_lengde || 너비값 > 화면폭 - 첫째값 || 높이값 > skjermbilde_lengde - SEKUND_VERDI) return -22;
        for (uintptr_t Y_koordinat = SEKUND_VERDI; Y_koordinat < SEKUND_VERDI + 높이값; Y_koordinat++) for (uintptr_t x_koordinat = 첫째값; x_koordinat < 첫째값 + 너비값; x_koordinat++) Tavle_piksel(x_koordinat, Y_koordinat, tegnkode);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=vare_ANTALL; args(index,buffer,capacity)=UTF-8 lengde_VERDI
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (tegnkode <= 전달인수길이[첫째값]) return -36;
        if (!bruker_område(SEKUND_VERDI, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SEKUND_VERDI, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;interaktiv=1;return Tavle_Terminal(13);}
        if(첫째값==2){interaktiv=0;return 0;}
        if(첫째값==3)return Tavle_Terminal(13);
        if(첫째값!=1||!interaktiv)return -22;
        KR=(int32_t)보드글자읽기();
        if(KR==-4096)return KR;
        START_TIMEOUT();return KR<0?-11:KR;
    case 17: { // 유한한 협력 vent_VERDI: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t avslutte_en_samtale_TID = Klokke_VERDI() + FREKVENS * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Klokke_VERDI() < avslutte_en_samtale_TID);
        START_TIMEOUT(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 overordnet_VERDI_881a8172·빈 폴더를 검사한다.
        if (SEKUND_VERDI > 2) return -22;
        KR = kopiere_bane(첫째값, Sti); if (KR) return KR;
        unsigned lengde_VERDI = 0; while (Sti[lengde_VERDI]) lengde_VERDI++;
        KR = 자바경로시작(lengde_VERDI); if (KR < 0) return KR;
        for (unsigned 순번 = 0; 순번 < lengde_VERDI; 순번++) 자바경로바이트(순번, (unsigned char)Sti[순번]);
        return SEKUND_VERDI == 0 ? 자바항목종류() : SEKUND_VERDI == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int tegn_VERDI=(int32_t)보드글자읽기();if(tegn_VERDI==-4096)return tegn_VERDI;if(tegn_VERDI>=0)화면누름(eier_objekt,tegn_VERDI);START_TIMEOUT();}
        if(첫째값==3&&tegnkode){if(!자바셸대화형())return -95;interaktiv=1;Tavle_Terminal(300);}
        return 화면호출(eier_objekt,첫째값,SEKUND_VERDI,tegnkode,Fil_oppføring->register_data[3],Fil_oppføring->register_data[4],Fil_oppføring->register_data[5]);
    case 21:
        if(tegnkode>127)return -22;if(!bruker_område(SEKUND_VERDI,tegnkode*sizeof(uint32_t),0))return -14;
        return skjermbilde_SMS(eier_objekt,첫째값,(const uint32_t *)SEKUND_VERDI,tegnkode);
    case 22: // skjermbilde Størrelse spørre_VERDI: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SEKUND_VERDI==SOCK_STREAM&&(tegnkode==0||tegnkode==6))KR=자바흐름만들기();
        else if(SEKUND_VERDI==SOCK_DGRAM&&(tegnkode==0||tegnkode==IPPROTO_UDP))KR=자바전문만들기(첫째값,SEKUND_VERDI,tegnkode);
        else return -93;
        if (KR >= 32 && KR < 56) 통신끝점들[KR - 32] = 1;
        return KR;
    case 33: {
        if (!socket_deltaker_eier(첫째값)) return -9;
        struct pk_sockaddr_in e_post;
        KR = e_post_inndata(SEKUND_VERDI, tegnkode, &e_post); if (KR) return KR;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(e_post.sin_addr.s_addr),pk_htons(e_post.sin_port)):자바전문묶기(첫째값, pk_htonl(e_post.sin_addr.s_addr), pk_htons(e_post.sin_port));
    }
    case 34: {
        if (!socket_deltaker_eier(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Fil_oppføring->register_data[3]) return -95;
        if (tegnkode > 512) return -90;
        if (tegnkode && !bruker_område(SEKUND_VERDI, tegnkode, 0)) return -14;
        struct pk_sockaddr_in e_post;
        KR = e_post_inndata(Fil_oppføring->register_data[4], Fil_oppføring->register_data[5], &e_post); if (KR) return KR;
        for (unsigned 순번 = 0; 순번 < tegnkode; 순번++) 자바전문넣기(순번, ((const unsigned char *)SEKUND_VERDI)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(e_post.sin_addr.s_addr), pk_htons(e_post.sin_port), tegnkode);
    }
    case 35: {
        if (!socket_deltaker_eier(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Fil_oppføring->register_data[3]) return -95;
        if (tegnkode > 512) return -90;
        if (tegnkode && !bruker_område(SEKUND_VERDI, tegnkode, 1)) return -14;
        pk_socklen_t bufre_kapasitet = 0;
        if (Fil_oppføring->register_data[4]) { KR = e_post_produksjon_sjekk(Fil_oppføring->register_data[4], Fil_oppføring->register_data[5], &bufre_kapasitet); if (KR) return KR; }
        KR = 자바전문받기(첫째값, tegnkode); if (KR < 0) return KR;
        for (int 순번 = 0; 순번 < KR; 순번++) ((unsigned char *)SEKUND_VERDI)[순번] = 자바전문얻기(순번);
        if (Fil_oppføring->register_data[4]) e_post_produksjon(Fil_oppføring->register_data[4], Fil_oppføring->register_data[5], bufre_kapasitet, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return KR;
    }
    case 36: {
        if (!socket_deltaker_eier(첫째값)) return -9;
        pk_socklen_t bufre_kapasitet;
        KR = e_post_produksjon_sjekk(SEKUND_VERDI, tegnkode, &bufre_kapasitet); if (KR) return KR;
        e_post_produksjon(SEKUND_VERDI,tegnkode,bufre_kapasitet,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!socket_deltaker_eier(첫째값))return -9;struct pk_sockaddr_in e_post;
        KR=e_post_inndata(SEKUND_VERDI,tegnkode,&e_post);if(KR)return KR;
        return 자바흐름연결(첫째값,pk_htonl(e_post.sin_addr.s_addr),pk_htons(e_post.sin_port));
    }
    case 38: return 첫째값>=40&&socket_deltaker_eier(첫째값)?자바흐름듣기(첫째값,SEKUND_VERDI):-9;
    case 39:
        if(첫째값<40||!socket_deltaker_eier(첫째값))return -9;
        if(SEKUND_VERDI||tegnkode)return -95;KR=자바흐름연결받기(첫째값);if(KR>=40&&KR<56)통신끝점들[KR-32]=1;return KR;
    case 40: return 첫째값>=40&&socket_deltaker_eier(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(bruker_bilde *Fil_oppføring) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(Fil_oppføring) : opprinnelig_System_Ring(Fil_oppføring);
}
static void return_kjerne(bruker_bilde *Fil_oppføring, int KR) {
    Stopp_TIMEOUT();
    Fil_oppføring->register_data[0] = (uint64_t)(int64_t)KR;
    Fil_oppføring->kommando_plassere = (uintptr_t)bruker_return;
    Fil_oppføring->status_KODE = 0x3c5; // EL1h, DAIF masked
}
int bruker_unntak(bruker_bilde *Fil_oppføring, unsigned SKJÆRINGSPUNKT) {
    if (!Aktiv || (Fil_oppføring->status_KODE & 15) != 0) return 0;
    if (SKJÆRINGSPUNKT) {
        uint32_t bekreftelse_VERDI = maskin_register(IRQ_CPU_grensesnitt + 0xc), identifikator_VERDI = bekreftelse_VERDI & 1023;
        if (identifikator_VERDI == 30) { return_kjerne(Fil_oppføring, bruker_TIMEOUT); maskin_register(IRQ_CPU_grensesnitt + 0x10) = bekreftelse_VERDI; return 1; }
        if (identifikator_VERDI < 1020) maskin_register(IRQ_CPU_grensesnitt + 0x10) = bekreftelse_VERDI;
        return 1;
    }
    uint64_t unntak_status; __asm__ volatile("mrs %0, esr_el1" : "=r"(unntak_status));
    if (Klokke_VERDI() >= tidsfrist_TID) { return_kjerne(Fil_oppføring, bruker_TIMEOUT); return 1; }
    unsigned unntak_område = unntak_status >> 26;
    if (unntak_område == 0x15 && (unntak_status & 0xffff) == 0) {
        if (리눅스규약 ? Fil_oppføring->register_data[8] == 93 || Fil_oppføring->register_data[8] == 94 : Fil_oppføring->register_data[8] == 6) return_kjerne(Fil_oppføring, (int)(Fil_oppføring->register_data[0] & 255));
        else {
            intptr_t KR=체계호출(Fil_oppføring);
            if(KR==-4096&&interaktiv){
                저장값[eier_objekt].kjøring_bilde=*Fil_oppføring;저장값[eier_objekt].kjøring_bilde.kommando_plassere-=4;
                사용자실수보관(저장값[eier_objekt].flyttall_status);return_kjerne(Fil_oppføring,사용자중단됨);
            }else Fil_oppføring->register_data[0]=(uint64_t)KR;
        }
    } else return_kjerne(Fil_oppføring, unntak_område == 0x24 ? bruker_data_feil : unntak_område == 0x20 ? bruker_kjøring_feil : 사용자잘못된명령);
    return 1;
}

// 생성된 const ELF gruppe_VERDI: 실행은 반드시 app_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *data; size_t Størrelse; unsigned 전달값; } app;
#include "programs.h"
static void *skyggekopi(unsigned posisjonsindeks){return (void *)(0x04000000ul+posisjonsindeks*(bruker_avslutte_en_samtale-bruker_grunnlag));}
static int slutt_app(int KR){
    사용자누적시각[eier_objekt]+=(uint32_t)보드밀리초()-bruker_kjøring_TID[eier_objekt];
    Stopp_TIMEOUT();Aktiv=0;
    if(KR==사용자중단됨){
        저장된작업 *streng_data=&저장값[eier_objekt];streng_data->멈춤상태=1;streng_data->interaktiv=interaktiv;streng_data->리눅스규약=리눅스규약;streng_data->heap_lager=heap_avslutte_en_samtale;streng_data->인수개수=전달인수개수;
        memcpy(streng_data->tillatelse_Liste,tillatelse_Liste,sizeof(tillatelse_Liste));memcpy(streng_data->filliste,filliste,sizeof(filliste));memcpy(streng_data->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(streng_data->argument_MATRISE,전달인수,sizeof(전달인수));memcpy(streng_data->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<bruker_page_ANTALL;순번++)if(tillatelse_Liste[순번])memcpy((unsigned char *)skyggekopi(eier_objekt)+순번*sidestørrelse,(void *)(bruker_grunnlag+순번*sidestørrelse),sidestørrelse);
    }else{
        저장값[eier_objekt].멈춤상태=0;starte_skjermbilde(eier_objekt);
        for(unsigned 순번=0;순번<16;순번++)if(filliste[순번]>=0)pk_close(filliste[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])Lukk_socket_deltaker(순번+32);
    }
    for(unsigned 순번=0;순번<bruker_page_ANTALL;순번++){page_Liste[순번]=0;tillatelse_Liste[순번]=0;}변환표맞추기();return KR;
}
uintptr_t Tavle_brukerkontroll(uintptr_t Handling){
    unsigned posisjonsindeks=Handling&15;if(posisjonsindeks>=4||Aktiv)return (uint32_t)-22;
    저장된작업 *streng_data=&저장값[posisjonsindeks];
    if(Handling>=32){if(streng_data->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(streng_data->filliste[순번]>=0)pk_close(streng_data->filliste[순번]);for(unsigned 순번=0;순번<24;순번++)if(streng_data->통신끝점들[순번])Lukk_socket_deltaker(순번+32);}streng_data->멈춤상태=0;starte_skjermbilde(posisjonsindeks);return 0;}
    if(Handling>=16)return streng_data->멈춤상태;
    if(!streng_data->멈춤상태)return (uint32_t)-22;
    eier_objekt=posisjonsindeks;interaktiv=streng_data->interaktiv;리눅스규약=streng_data->리눅스규약;heap_avslutte_en_samtale=streng_data->heap_lager;전달인수개수=streng_data->인수개수;
    memcpy(filliste,streng_data->filliste,sizeof(filliste));memcpy(통신끝점들,streng_data->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,streng_data->argument_MATRISE,sizeof(전달인수));memcpy(전달인수길이,streng_data->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<bruker_page_ANTALL;순번++)page_Liste[순번]=(bruker_grunnlag+순번*sidestørrelse)|kjerne_page;변환표맞추기();
    memset((void *)bruker_grunnlag,0,bruker_avslutte_en_samtale-bruker_grunnlag);
    for(unsigned 순번=0;순번<bruker_page_ANTALL;순번++)if(streng_data->tillatelse_Liste[순번])memcpy((void *)(bruker_grunnlag+순번*sidestørrelse),(unsigned char *)skyggekopi(posisjonsindeks)+순번*sidestørrelse,sidestørrelse);
    memcpy(tillatelse_Liste,streng_data->tillatelse_Liste,sizeof(tillatelse_Liste));
    for(unsigned 순번=0;순번<bruker_page_ANTALL;순번++){unsigned data_plassere=tillatelse_Liste[순번];page_Liste[순번]=data_plassere?(bruker_grunnlag+순번*sidestørrelse)|(data_plassere==3?bruker_lese_og_skrive:data_plassere==5?사용자읽고실행:bruker_skrivebeskyttet):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");Aktiv=1;streng_data->멈춤상태=0;START_TIMEOUT();
    bruker_kjøring_TID[eier_objekt]=보드밀리초();
    return (uint32_t)slutt_app(bruker_CV(&streng_data->kjøring_bilde,streng_data->flyttall_status));
}
static int kjøre_app(const unsigned char *data, size_t Størrelse, unsigned 전달값, int 리눅스방식, const char *Navn) {
    if (Aktiv) return -16;
    eier_objekt=Tavle_Terminal(11);if(eier_objekt<0||eier_objekt>3||저장값[eier_objekt].멈춤상태)return -16;interaktiv=0;
    int gyldig = 실행파일검사(data, Størrelse, 리눅스방식); if (gyldig) return gyldig;
    리눅스규약 = 리눅스방식;
    unsigned navn_INDEKS=0;
    while (*Navn && navn_INDEKS<31) bruker_kommando_navn[eier_objekt][navn_INDEKS++]=(unsigned char)*Navn++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (navn_INDEKS) bruker_kommando_navn[eier_objekt][navn_INDEKS++]=' ';
        for (unsigned posisjonsindeks=0; posisjonsindeks<전달인수길이[0]; posisjonsindeks++) bruker_kommando_navn[eier_objekt][navn_INDEKS++]=전달인수[0][posisjonsindeks];
    }
    bruker_kommando_navn[eier_objekt][navn_INDEKS]=0; brukernummer[eier_objekt]=Neste_brukernummer++;
    if (Neste_brukernummer>0x7fffffffu) Neste_brukernummer=10;
    bruker_START_TID[eier_objekt]=보드밀리초(); 사용자누적시각[eier_objekt]=0;
    for (unsigned 순번 = 0; 순번 < bruker_page_ANTALL; 순번++) page_Liste[순번] = (bruker_grunnlag + 순번 * sidestørrelse) | kjerne_page;
    변환표맞추기();
    memset((void *)bruker_grunnlag, 0, bruker_avslutte_en_samtale - bruker_grunnlag);
    memset(tillatelse_Liste, 0, sizeof(tillatelse_Liste));
    실행파일머리 kjørbar_fil_Topptekst; memcpy(&kjørbar_fil_Topptekst, data, sizeof(kjørbar_fil_Topptekst));
    for (unsigned 순번 = 0; 순번 < kjørbar_fil_Topptekst.app_Topptekst_ANTALL; 순번++) {
        실행파일구획 data_plassere; memcpy(&data_plassere, data + kjørbar_fil_Topptekst.app_Topptekst_FORSKYVNING + 순번 * sizeof(data_plassere), sizeof(data_plassere));
        if (data_plassere.Type_område != 1 || !data_plassere.기억영역크기) continue;
        if (data_plassere.파일영역크기) memcpy((void *)(uintptr_t)data_plassere.e_post, data + data_plassere.FORSKYVNING_VERDI, data_plassere.파일영역크기);
        for (uintptr_t betalt_plassere = data_plassere.e_post & ~(sidestørrelse - 1); betalt_plassere < data_plassere.e_post + data_plassere.기억영역크기; betalt_plassere += sidestørrelse) {
            tillatelse_Liste[(betalt_plassere - bruker_grunnlag) / sidestørrelse] = (data_plassere.konfigurasjon_BITS & 2) ? 3 : ((data_plassere.konfigurasjon_BITS & 1) ? 5 : 1);
        }
    }
    for (uintptr_t betalt_plassere = bruker_stakk_e_post; betalt_plassere < bruker_avslutte_en_samtale; betalt_plassere += sidestørrelse) tillatelse_Liste[(betalt_plassere - bruker_grunnlag) / sidestørrelse] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(kjørbar_fil_Topptekst.inngangspunkt) : bruker_avslutte_en_samtale;
    for (unsigned 순번 = 0; 순번 < bruker_page_ANTALL; 순번++) {
        unsigned tillatelse = tillatelse_Liste[순번];
        page_Liste[순번] = tillatelse ? (bruker_grunnlag + 순번 * sidestørrelse) | (tillatelse == 3 ? bruker_lese_og_skrive : tillatelse == 5 ? 사용자읽고실행 : bruker_skrivebeskyttet) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) filliste[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    heap_avslutte_en_samtale = bruker_BILDE_avslutte_en_samtale;
    Aktiv = 1; START_TIMEOUT();
    bruker_kjøring_TID[eier_objekt]=보드밀리초();
    int KR = bruker_angi(kjørbar_fil_Topptekst.inngangspunkt, 초기쌓임공간, 전달값);
    return slutt_app(KR);
}
uintptr_t Tavle_bruker_kjøre(uintptr_t Oppslag_INDEKS) {
    if (Oppslag_INDEKS >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Navn=Oppslag_INDEKS==10?"javac":Oppslag_INDEKS==11?"java":Oppslag_INDEKS==12?"python":Oppslag_INDEKS==13?"vi":Oppslag_INDEKS==14?"jar":Oppslag_INDEKS==15?"cc":Oppslag_INDEKS==16?"jaot":"ELF";
    return (uint32_t)kjøre_app(실행항목들[Oppslag_INDEKS].data, 실행항목들[Oppslag_INDEKS].Størrelse, 실행항목들[Oppslag_INDEKS].전달값, 0, Navn);
}
static uintptr_t Utfør_Fil(int 리눅스방식) {
    static unsigned char BILDE[16384];
    if (Aktiv || !전달인수개수) return (uint32_t)-22;
    int Fil_håndtak = pk_open((const char *)전달인수[0], skrivebeskyttet_VERDI, 0);
    if (Fil_håndtak < 0) return (uint32_t)-feilnummer;
    int Størrelse = pk_size(Fil_håndtak);
    if (Størrelse < 0 || (unsigned)Størrelse > sizeof(BILDE)) { pk_close(Fil_håndtak); return (uint32_t)-27; }
    int MOTTATT_AVKAST_ANTALL = pk_read(Fil_håndtak, BILDE, Størrelse); pk_close(Fil_håndtak);
    if (MOTTATT_AVKAST_ANTALL != Størrelse) return (uint32_t)-5;
    return (uint32_t)kjøre_app(BILDE, Størrelse, 0, 리눅스방식, "");
}
uintptr_t Tavle_bruker_Fil(void) { return Utfør_Fil(0); }
uintptr_t 보드사용자리눅스파일(void) { return Utfør_Fil(1); }
uintptr_t Tavle_bruker_bekrefte(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].data, 잘못된실행항목들[순번].Størrelse) != bruker_kjørbar_fil_feil) return 순번 + 1;
    return 0;
}
