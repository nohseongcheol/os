#include "../명명/기계연결이름.h"
#include "skærmbillede_info.h"
// EL0 Udfør_kommando maskine lag_VÆRDI. Fil data/정책은 기존 AOT Java 커널에 위임한다.
#include "bruger.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../netværk_Stak/netværk_Stak.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define maskine_register(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_distributør 0xff841000ul
#define IRQ_CPU_grænseflade 0xff842000ul
#define sidestørrelse 4096ul
#define åbne_mærke (1ul << 10)
#define nej_Udfør_rettighed (1ul << 53)
#define bruger_nej_Udfør (1ul << 54)
#define normal_Hukommelse ((1ul << 2) | (3ul << 8) | åbne_mærke)
#define kerne_side (3ul | normal_Hukommelse | nej_Udfør_rettighed | bruger_nej_Udfør)
#define bruger_læse_skrive (3ul | normal_Hukommelse | (1ul << 6) | nej_Udfør_rettighed | bruger_nej_Udfør)
#define bruger_skrivebeskyttet (3ul | normal_Hukommelse | (3ul << 6) | nej_Udfør_rettighed | bruger_nej_Udfør)
#define 사용자읽고실행 (3ul | normal_Hukommelse | (3ul << 6) | nej_Udfør_rettighed)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t Tavle_pixel(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t Tavle_Terminal(uintptr_t);
extern int Terminal_Afventer(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),skærmbillede_sms(int,int,const uint32_t *,unsigned);
extern void starte_skærmbillede(int),화면누름(int,unsigned);
extern int bruger_CV(bruger_ramme *,void *);
extern void 사용자실수보관(void *);
extern int bruger_angive(uintptr_t indgangspunkt, uintptr_t Stak_Lager, uintptr_t 전달값);
extern void bruger_returnere(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t rod_mail[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t side_Liste[bruger_side_TÆL] __attribute__((aligned(4096)));
static uint8_t Tilladelser_Liste[bruger_side_TÆL];
static int Aktiv, filliste[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int Luk_socket_slutpunkt(unsigned fil_handle){return fil_handle<40?자바전문닫기(fil_handle):자바흐름닫기(fil_handle);}
static uint64_t FREKVENS, deadline_TID;
static uintptr_t heap_afslutte_et_opkald;
// kerne_VÆRDI 셸이 준비한 UTF-8 Argumenter. EL0에는 kopiere_VÆRDI 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,interaktiv,리눅스규약,filliste[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char argument_MATRIX[8][256],Tilladelser_Liste[bruger_side_TÆL];
    uintptr_t heap_Lager; bruger_ramme udførelse_ramme;
    unsigned char flydende_tal_status[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int ejer_objekt,interaktiv;
static uint32_t brugernummer[4], bruger_START_TID[4], 사용자누적시각[4], bruger_udførelse_TID[4], Næste_brugernummer=10;
static unsigned char bruger_kommando_navn[4][288];
uint32_t 사용자상태읽기(unsigned post_VÆRDI_962f286b, unsigned INDEKS) {
    unsigned positionsindeks=INDEKS&3;
    int status_VÆRDI=(Aktiv && ejer_objekt==(int)positionsindeks) ? 1 : 저장값[positionsindeks].멈춤상태 ? 2 : 0;
    if (post_VÆRDI_962f286b==0) return status_VÆRDI;
    if (!status_VÆRDI) return 0;
    if (post_VÆRDI_962f286b==1) return brugernummer[positionsindeks];
    if (post_VÆRDI_962f286b==2) {
        unsigned char *쪽들=status_VÆRDI==1?Tilladelser_Liste:저장값[positionsindeks].Tilladelser_Liste;
        unsigned side_TÆL=0; for (unsigned 순번=0; 순번<bruger_side_TÆL; 순번++) if(쪽들[순번]) side_TÆL++;
        return side_TÆL*4;
    }
    if (post_VÆRDI_962f286b==3) return (uint32_t)보드밀리초()-bruger_START_TID[positionsindeks];
    if (post_VÆRDI_962f286b==4) return 사용자누적시각[positionsindeks]+(status_VÆRDI==1?(uint32_t)보드밀리초()-bruger_udførelse_TID[positionsindeks]:0);
    if (post_VÆRDI_962f286b==5) return INDEKS/4<sizeof(bruger_kommando_navn[0])?bruger_kommando_navn[positionsindeks][INDEKS/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t post_TÆL_8f7753a1) {
    if (Aktiv || post_TÆL_8f7753a1 > 8) return (uint32_t)-22;
    전달인수개수 = post_TÆL_8f7753a1;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t Opslag_INDEKS, uintptr_t aktuel_placere, uintptr_t byte_data) {
    if (Aktiv || Opslag_INDEKS >= 전달인수개수 || aktuel_placere >= 255 || aktuel_placere != 전달인수길이[Opslag_INDEKS] || !byte_data || byte_data > 255)
        return (uint32_t)-22;
    전달인수[Opslag_INDEKS][aktuel_placere] = byte_data;
    전달인수길이[Opslag_INDEKS] = aktuel_placere + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Ur_VÆRDI(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Stop_TIMEOUT(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    maskine_register(IRQ_distributør + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void START_TIMEOUT(void) {
    uint64_t 간격 = FREKVENS * 2, slå_til = 1;
    deadline_TID = Ur_VÆRDI() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(slå_til) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned datablok = 0; datablok < 4; datablok++) {
        rod_mail[datablok] = (uintptr_t)가운데[datablok] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t mail = ((uintptr_t)datablok << 30) | ((uintptr_t)순번 << 21);
            가운데[datablok][순번] = mail | 1 | åbne_mærke | bruger_nej_Udfør;
            if (mail >= 0xfc000000ul) 가운데[datablok][순번] |= nej_Udfør_rettighed; // Device-nGnRnE
            else 가운데[datablok][순번] |= normal_Hukommelse; // Normal, non-cacheable
        }
    }
    for (unsigned SEKUND_VÆRDI = 0; SEKUND_VÆRDI < bruger_side_TÆL / 512; SEKUND_VÆRDI++)
        가운데[0][(bruger_BASIS >> 21) + SEKUND_VÆRDI] = (uintptr_t)(side_Liste + SEKUND_VÆRDI * 512) | 3;
    for (unsigned 순번 = 0; 순번 < bruger_side_TÆL; 순번++) side_Liste[순번] = (bruger_BASIS + 순번 * sidestørrelse) | kerne_side;
    uint64_t Hukommelse_attribut_register = 0x4400, mail_Oversættelse_kontrol = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Hukommelse_attribut_register), "r"(mail_Oversættelse_kontrol), "r"((uintptr_t)rod_mail) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t flydende_tal_status = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(flydende_tal_status) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREKVENS));
    Stop_TIMEOUT();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 indgangspunkt_VÆRDI 때만 Tillad_VÆRDI.
    maskine_register(IRQ_distributør) = 0;
    maskine_register(IRQ_distributør + 0x180) = 0xffffffff;
    maskine_register(IRQ_distributør + 0x80) = 0xffffffff;
    maskine_register(IRQ_distributør + 0x280) = 1u << 30;
    maskine_register(IRQ_distributør + 0x41c) = 0x80808080;
    maskine_register(IRQ_distributør + 0x100) = 1u << 30;
    maskine_register(IRQ_CPU_grænseflade + 4) = 0xff;
    maskine_register(IRQ_CPU_grænseflade + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 it_normal 확인할 tal 있다.
    int Sikkerhed = (maskine_register(IRQ_distributør + 4) & (1u << 10)) != 0;
    maskine_register(IRQ_distributør) = Sikkerhed ? 1 : 3;
    maskine_register(IRQ_CPU_grænseflade) = Sikkerhed ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t Type_område, maskine_Type; uint32_t versionsnummer;
    uint64_t indgangspunkt, app_Header_FORSKYDNING, sektionsoverskrift_FORSKYDNING; uint32_t konfiguration_BITS;
    uint16_t eksekverbar_fil_Header_tilpasse_størrelse, app_Header_post_tilpasse_størrelse, app_Header_TÆL, sektionsoverskrift_post_tilpasse_størrelse, sektionsoverskrift_TÆL, sektion_navn_tabel_INDEKS;
} 실행파일머리;
typedef struct { uint32_t Type_område, konfiguration_BITS; uint64_t FORSKYDNING_VÆRDI, mail, 물리주소, 파일영역크기, 기억영역크기, justere_grænse; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(bruger_ramme) == 272, "exception assembly layout");
static int 포함된범위(uint64_t FORSKYDNING_VÆRDI, uint64_t Størrelse, uint64_t afslutte_et_opkald_FORSKYDNING) {
    return FORSKYDNING_VÆRDI <= afslutte_et_opkald_FORSKYDNING && Størrelse <= afslutte_et_opkald_FORSKYDNING - FORSKYDNING_VÆRDI;
}
static int 부가정보검사(const unsigned char *data_placere, size_t Størrelse) {
    size_t aktuel_placere = 0;
    while (포함된범위(aktuel_placere, 12, Størrelse)) {
        uint32_t 낱말들[3]; memcpy(낱말들, data_placere + aktuel_placere, 12); aktuel_placere += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(aktuel_placere, 이름영역크기, Størrelse) || !포함된범위(aktuel_placere + 이름영역크기, 설명크기, Størrelse)) return 0;
        const unsigned char Navn[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Navn) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Navn); 순번++) if (data_placere[aktuel_placere + 순번] != Navn[순번]) 일치 = 0;
        uint32_t versionsnummer = 0;
        if (일치) memcpy(&versionsnummer, data_placere + aktuel_placere + 이름영역크기, 4);
        if (일치 && versionsnummer == 1) return 1;
        aktuel_placere += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *data, size_t Størrelse, int 리눅스방식) {
    if (Størrelse < sizeof(실행파일머리)) return bruger_eksekverbar_fil_fejl;
    실행파일머리 eksekverbar_fil_Header; memcpy(&eksekverbar_fil_Header, data, sizeof(eksekverbar_fil_Header));
    if (eksekverbar_fil_Header.형식식별[0] != 127 || eksekverbar_fil_Header.형식식별[1] != 'E' || eksekverbar_fil_Header.형식식별[2] != 'L' || eksekverbar_fil_Header.형식식별[3] != 'F' ||
        eksekverbar_fil_Header.형식식별[4] != 2 || eksekverbar_fil_Header.형식식별[5] != 1 || eksekverbar_fil_Header.형식식별[6] != 1 || (eksekverbar_fil_Header.형식식별[7] != 0 && (!리눅스방식 || eksekverbar_fil_Header.형식식별[7] != 3)) ||
        eksekverbar_fil_Header.Type_område != 2 || eksekverbar_fil_Header.maskine_Type != 183 || eksekverbar_fil_Header.versionsnummer != 1 || eksekverbar_fil_Header.konfiguration_BITS || eksekverbar_fil_Header.eksekverbar_fil_Header_tilpasse_størrelse != sizeof(eksekverbar_fil_Header) ||
        eksekverbar_fil_Header.app_Header_post_tilpasse_størrelse != sizeof(실행파일구획) || !eksekverbar_fil_Header.app_Header_TÆL || eksekverbar_fil_Header.app_Header_TÆL > 16 ||
        eksekverbar_fil_Header.app_Header_FORSKYDNING < sizeof(eksekverbar_fil_Header) || !포함된범위(eksekverbar_fil_Header.app_Header_FORSKYDNING, (uint64_t)eksekverbar_fil_Header.app_Header_TÆL * sizeof(실행파일구획), Størrelse)) return bruger_eksekverbar_fil_fejl;
    uint8_t 사용량[(bruger_Image_afslutte_et_opkald - bruger_BASIS) / sidestørrelse] = {0};
    int gyldig_indgangspunkt = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < eksekverbar_fil_Header.app_Header_TÆL; 순번++) {
        실행파일구획 data_placere; memcpy(&data_placere, data + eksekverbar_fil_Header.app_Header_FORSKYDNING + 순번 * sizeof(data_placere), sizeof(data_placere));
        if (data_placere.Type_område == 4) {
            if (!포함된범위(data_placere.FORSKYDNING_VÆRDI, data_placere.파일영역크기, Størrelse)) return bruger_eksekverbar_fil_fejl;
            if (부가정보검사(data + data_placere.FORSKYDNING_VÆRDI, data_placere.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (data_placere.Type_område == 0 || data_placere.Type_område == 6 || (data_placere.Type_område == 0x6474e551 && !(data_placere.konfiguration_BITS & 1))) continue;
        if (data_placere.Type_område != 1) return bruger_eksekverbar_fil_fejl; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!data_placere.기억영역크기) continue;
        if (data_placere.konfiguration_BITS & ~7u || !(data_placere.konfiguration_BITS & 4) || (data_placere.konfiguration_BITS & 3) == 3 || data_placere.파일영역크기 > data_placere.기억영역크기 ||
            (data_placere.파일영역크기 && !포함된범위(data_placere.FORSKYDNING_VÆRDI, data_placere.파일영역크기, Størrelse)) || data_placere.mail < bruger_BASIS ||
            !포함된범위(data_placere.mail, data_placere.기억영역크기, bruger_Image_afslutte_et_opkald) ||
            (!리눅스방식 && ((data_placere.mail & (sidestørrelse - 1)) || (data_placere.FORSKYDNING_VÆRDI & (sidestørrelse - 1)) || data_placere.justere_grænse != sidestørrelse)) ||
            (리눅스방식 && (((data_placere.mail ^ data_placere.FORSKYDNING_VÆRDI) & (sidestørrelse - 1)) || !data_placere.justere_grænse ||
                (data_placere.justere_grænse & (data_placere.justere_grænse - 1)) || data_placere.justere_grænse > 0x200000 || ((data_placere.mail ^ data_placere.FORSKYDNING_VÆRDI) & (data_placere.justere_grænse - 1))))) return bruger_eksekverbar_fil_fejl;
        unsigned 첫항목 = (data_placere.mail - bruger_BASIS) / sidestørrelse;
        unsigned post_TÆL_8f7753a1 = ((data_placere.mail & (sidestørrelse - 1)) + data_placere.기억영역크기 + sidestørrelse - 1) / sidestørrelse;
        for (unsigned side_VÆRDI = 첫항목; side_VÆRDI < 첫항목 + post_TÆL_8f7753a1; side_VÆRDI++) {
            if (사용량[side_VÆRDI]) return bruger_eksekverbar_fil_fejl;
            사용량[side_VÆRDI] = 1;
        }
        if ((data_placere.konfiguration_BITS & 1) && eksekverbar_fil_Header.indgangspunkt >= data_placere.mail && eksekverbar_fil_Header.indgangspunkt < data_placere.mail + data_placere.파일영역크기 && !(eksekverbar_fil_Header.indgangspunkt & 3)) gyldig_indgangspunkt = 1;
        적재구획++;
    }
    return gyldig_indgangspunkt && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : bruger_eksekverbar_fil_fejl;
}
int 사용자실행파일검사(const unsigned char *data, size_t Størrelse) { return 실행파일검사(data, Størrelse, 0); }
static void sidelayout(uintptr_t mail, uint64_t konfiguration_BITS, unsigned tilladelser) {
    unsigned Opslag_INDEKS = (mail - bruger_BASIS) / sidestørrelse;
    side_Liste[Opslag_INDEKS] = mail | konfiguration_BITS;
    Tilladelser_Liste[Opslag_INDEKS] = tilladelser;
}
static int bruger_område(uintptr_t mail, size_t post_TÆL_8f7753a1, int 쓰는중) {
    if (mail < bruger_BASIS || !포함된범위(mail, post_TÆL_8f7753a1, bruger_afslutte_et_opkald)) return 0;
    if (!post_TÆL_8f7753a1) return 1;
    unsigned 첫항목 = (mail - bruger_BASIS) / sidestørrelse, 마지막 = (mail + post_TÆL_8f7753a1 - 1 - bruger_BASIS) / sidestørrelse;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(Tilladelser_Liste[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int kopiere_sti(uintptr_t mail, char *Sti) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!bruger_område(mail, 1, 0)) return -14;
        Sti[순번] = *(const char *)mail++;
        if (!Sti[순번]) return 0;
    }
    return -36;
}
static intptr_t kerne_KR(intptr_t KR) { return KR < 0 ? -fejlnummer : KR; }
static int 대응파일기술자(uint64_t fil_handle) { return fil_handle >= 3 && fil_handle < 19 ? filliste[fil_handle - 3] : -1; }
static int socket_slutpunkt_ejer(uint64_t fil_handle) { return fil_handle >= 32 && fil_handle < 56 && 통신끝점들[fil_handle - 32]; }
static int mail_input(uintptr_t 가리킴값, size_t varighed_VÆRDI, struct pk_sockaddr_in *mail) {
    if (varighed_VÆRDI != sizeof(*mail)) return -22;
    if (!bruger_område(가리킴값, varighed_VÆRDI, 0)) return -14;
    memcpy(mail, (const void *)가리킴값, sizeof(*mail));
    return mail->sin_family == AF_INET ? 0 : -97;
}
static int mail_produktoutput_check(uintptr_t 가리킴값, uintptr_t varighed_markør, pk_socklen_t *buffer_kapacitet) {
    if (!bruger_område(varighed_markør, sizeof(*buffer_kapacitet), 1)) return -14;
    memcpy(buffer_kapacitet, (const void *)varighed_markør, sizeof(*buffer_kapacitet));
    if (*buffer_kapacitet > sizeof(struct pk_sockaddr_in)) *buffer_kapacitet = sizeof(struct pk_sockaddr_in);
    if (*buffer_kapacitet && !bruger_område(가리킴값, *buffer_kapacitet, 1)) return -14;
    return 0;
}
static void mail_produktoutput(uintptr_t 가리킴값, uintptr_t varighed_markør, pk_socklen_t buffer_kapacitet, int mail, int portnummer) {
    struct pk_sockaddr_in VÆRDI; memset(&VÆRDI, 0, sizeof(VÆRDI));
    VÆRDI.sin_family = AF_INET; VÆRDI.sin_port = pk_htons(portnummer); VÆRDI.sin_addr.s_addr = pk_htonl(mail);
    if (buffer_kapacitet) memcpy((void *)가리킴값, &VÆRDI, buffer_kapacitet);
    pk_socklen_t varighed_VÆRDI = sizeof(VÆRDI); memcpy((void *)varighed_markør, &varighed_VÆRDI, sizeof(varighed_VÆRDI));
}
extern uintptr_t Tavle_Kanal(uintptr_t, uintptr_t);
static intptr_t oprindelig_System_KALD(bruger_ramme *fil_post) {
    uintptr_t 첫째값 = fil_post->register_data[0], SEKUND_VÆRDI = fil_post->register_data[1], tegnkode = fil_post->register_data[2];
    char Sti[65];
    int fil_handle, KR;
    switch (fil_post->register_data[8]) {
    case 0: return 1; // eget ABI 버전
    case 1: // write: markør 전체를 검사한 BACK_VÆRDI Udgang/Fil ændre_VÆRDI
        if (tegnkode > 65536) return -22;
        if (!bruger_område(SEKUND_VÆRDI, tegnkode, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t START_produktoutput=Ur_VÆRDI();
            for (size_t 순번 = 0; 순번 < tegnkode; 순번++) Tavle_Kanal(첫째값, ((const unsigned char *)SEKUND_VÆRDI)[순번]);
            /* 큰 tty를 그린 kerne_VÆRDI 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(interaktiv){
                deadline_TID+=Ur_VÆRDI()-START_produktoutput;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(deadline_TID) : "memory");
            }
            return tegnkode;
        }
        if(첫째값>=40&&socket_slutpunkt_ejer(첫째값)){
            size_t vare_TÆL=tegnkode>512?512:tegnkode;for(size_t 순번=0;순번<vare_TÆL;순번++)자바전문넣기(순번,((const unsigned char *)SEKUND_VÆRDI)[순번]);return 자바흐름쓰기(첫째값,vare_TÆL);
        }
        fil_handle = 대응파일기술자(첫째값); if (fil_handle < 0) return -9;
        return kerne_KR(pk_write(fil_handle, (const void *)SEKUND_VÆRDI, tegnkode));
    case 2:
        if (tegnkode > 65536) return -22;
        if (!bruger_område(SEKUND_VÆRDI, tegnkode, 1)) return -14;
        if (첫째값 == 0) {
            size_t vare_TÆL = 0;
            while (vare_TÆL < tegnkode) {
                int tegn_VÆRDI = (int32_t)보드글자읽기(); if (tegn_VÆRDI == -2) return vare_TÆL; if (tegn_VÆRDI < 0) break;
                ((unsigned char *)SEKUND_VÆRDI)[vare_TÆL++] = tegn_VÆRDI;
            }
            return vare_TÆL ? (intptr_t)vare_TÆL : (tegnkode ? -11 : 0);
        }
        if(첫째값>=40&&socket_slutpunkt_ejer(첫째값)){
            KR=자바흐름읽기(첫째값,tegnkode>512?512:tegnkode);if(KR>0)for(int 순번=0;순번<KR;순번++)((unsigned char *)SEKUND_VÆRDI)[순번]=자바전문얻기(순번);return KR;
        }
        fil_handle = 대응파일기술자(첫째값); if (fil_handle < 0) return -9;
        return kerne_KR(pk_read(fil_handle, (void *)SEKUND_VÆRDI, tegnkode));
    case 3:
        KR = kopiere_sti(첫째값, Sti); if (KR) return KR;
        if (SEKUND_VÆRDI > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (filliste[순번] < 0) {
            fil_handle = pk_open(Sti, (int)SEKUND_VÆRDI, 0600);
            if (fil_handle < 0) return -fejlnummer;
            filliste[순번] = fil_handle; return 순번 + 3;
        }
        return -24;
    case 4:
        if (socket_slutpunkt_ejer(첫째값)) { KR = Luk_socket_slutpunkt(첫째값); if (!KR) 통신끝점들[첫째값 - 32] = 0; return KR; }
        fil_handle = 대응파일기술자(첫째값); if (fil_handle < 0) return -9;
        KR = pk_close(fil_handle); if (!KR) filliste[첫째값 - 3] = -1;
        return kerne_KR(KR);
    case 5:
        fil_handle = 대응파일기술자(첫째값); if (fil_handle < 0) return -9;
        if (tegnkode > 2) return -22;
        return kerne_KR(pk_lseek(fil_handle, (int64_t)SEKUND_VÆRDI, tegnkode));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 bruger RW/NX heap_VÆRDI, 새로 노출되는 페이지는 0으로 starte
        if (!첫째값) return heap_afslutte_et_opkald;
        if (첫째값 < bruger_Image_afslutte_et_opkald || 첫째값 > bruger_heap_afslutte_et_opkald) return -12;
        uintptr_t 이전쪽들 = (heap_afslutte_et_opkald + sidestørrelse - 1) & ~(sidestørrelse - 1);
        uintptr_t 새쪽들 = (첫째값 + sidestørrelse - 1) & ~(sidestørrelse - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t data_placere = 이전쪽들; data_placere < 새쪽들; data_placere += sidestørrelse) sidelayout(data_placere, kerne_side, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t data_placere = 이전쪽들; data_placere < 새쪽들; data_placere += sidestørrelse) sidelayout(data_placere, bruger_læse_skrive, 3);
        } else {
            for (uintptr_t data_placere = 새쪽들; data_placere < 이전쪽들; data_placere += sidestørrelse) {
                side_Liste[(data_placere - bruger_BASIS) / sidestørrelse] = 0; Tilladelser_Liste[(data_placere - bruger_BASIS) / sidestørrelse] = 0;
            }
        }
        heap_afslutte_et_opkald = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        fil_handle = 대응파일기술자(첫째값); return fil_handle < 0 ? -9 : kerne_KR(pk_size(fil_handle));
    case 10:
        fil_handle = 대응파일기술자(첫째값); return fil_handle < 0 ? -9 : kerne_KR(pk_ftruncate(fil_handle, (int64_t)SEKUND_VÆRDI));
    case 11:
        KR = kopiere_sti(첫째값, Sti); return KR ? KR : kerne_KR(pk_unlink(Sti));
    case 12:
        fil_handle = 대응파일기술자(첫째값); return fil_handle < 0 ? -9 : kerne_KR(pk_fsync(fil_handle));
    case 13: { // 그래픽 기초 API: bruger 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = fil_post->register_data[3], 높이값 = fil_post->register_data[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), skærmbillede_varighed = 보드화면높이();
        if (첫째값 > 화면폭 || SEKUND_VÆRDI > skærmbillede_varighed || 너비값 > 화면폭 - 첫째값 || 높이값 > skærmbillede_varighed - SEKUND_VÆRDI) return -22;
        for (uintptr_t Y_koordinat = SEKUND_VÆRDI; Y_koordinat < SEKUND_VÆRDI + 높이값; Y_koordinat++) for (uintptr_t X_koordinat = 첫째값; X_koordinat < 첫째값 + 너비값; X_koordinat++) Tavle_pixel(X_koordinat, Y_koordinat, tegnkode);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=vare_TÆL; args(index,buffer,capacity)=UTF-8 varighed_VÆRDI
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (tegnkode <= 전달인수길이[첫째값]) return -36;
        if (!bruger_område(SEKUND_VÆRDI, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SEKUND_VÆRDI, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;interaktiv=1;return Tavle_Terminal(13);}
        if(첫째값==2){interaktiv=0;return 0;}
        if(첫째값==3)return Tavle_Terminal(13);
        if(첫째값!=1||!interaktiv)return -22;
        KR=(int32_t)보드글자읽기();
        if(KR==-4096)return KR;
        START_TIMEOUT();return KR<0?-11:KR;
    case 17: { // 유한한 협력 vent_VÆRDI: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t afslutte_et_opkald_TID = Ur_VÆRDI() + FREKVENS * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Ur_VÆRDI() < afslutte_et_opkald_TID);
        START_TIMEOUT(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 overordnet_VÆRDI·빈 폴더를 검사한다.
        if (SEKUND_VÆRDI > 2) return -22;
        KR = kopiere_sti(첫째값, Sti); if (KR) return KR;
        unsigned varighed_VÆRDI = 0; while (Sti[varighed_VÆRDI]) varighed_VÆRDI++;
        KR = 자바경로시작(varighed_VÆRDI); if (KR < 0) return KR;
        for (unsigned 순번 = 0; 순번 < varighed_VÆRDI; 순번++) 자바경로바이트(순번, (unsigned char)Sti[순번]);
        return SEKUND_VÆRDI == 0 ? 자바항목종류() : SEKUND_VÆRDI == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int tegn_VÆRDI=(int32_t)보드글자읽기();if(tegn_VÆRDI==-4096)return tegn_VÆRDI;if(tegn_VÆRDI>=0)화면누름(ejer_objekt,tegn_VÆRDI);START_TIMEOUT();}
        if(첫째값==3&&tegnkode){if(!자바셸대화형())return -95;interaktiv=1;Tavle_Terminal(300);}
        return 화면호출(ejer_objekt,첫째값,SEKUND_VÆRDI,tegnkode,fil_post->register_data[3],fil_post->register_data[4],fil_post->register_data[5]);
    case 21:
        if(tegnkode>127)return -22;if(!bruger_område(SEKUND_VÆRDI,tegnkode*sizeof(uint32_t),0))return -14;
        return skærmbillede_sms(ejer_objekt,첫째값,(const uint32_t *)SEKUND_VÆRDI,tegnkode);
    case 22: // skærmbillede Størrelse forespørge_VÆRDI: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SEKUND_VÆRDI==SOCK_STREAM&&(tegnkode==0||tegnkode==6))KR=자바흐름만들기();
        else if(SEKUND_VÆRDI==SOCK_DGRAM&&(tegnkode==0||tegnkode==IPPROTO_UDP))KR=자바전문만들기(첫째값,SEKUND_VÆRDI,tegnkode);
        else return -93;
        if (KR >= 32 && KR < 56) 통신끝점들[KR - 32] = 1;
        return KR;
    case 33: {
        if (!socket_slutpunkt_ejer(첫째값)) return -9;
        struct pk_sockaddr_in mail;
        KR = mail_input(SEKUND_VÆRDI, tegnkode, &mail); if (KR) return KR;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(mail.sin_addr.s_addr),pk_htons(mail.sin_port)):자바전문묶기(첫째값, pk_htonl(mail.sin_addr.s_addr), pk_htons(mail.sin_port));
    }
    case 34: {
        if (!socket_slutpunkt_ejer(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (fil_post->register_data[3]) return -95;
        if (tegnkode > 512) return -90;
        if (tegnkode && !bruger_område(SEKUND_VÆRDI, tegnkode, 0)) return -14;
        struct pk_sockaddr_in mail;
        KR = mail_input(fil_post->register_data[4], fil_post->register_data[5], &mail); if (KR) return KR;
        for (unsigned 순번 = 0; 순번 < tegnkode; 순번++) 자바전문넣기(순번, ((const unsigned char *)SEKUND_VÆRDI)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(mail.sin_addr.s_addr), pk_htons(mail.sin_port), tegnkode);
    }
    case 35: {
        if (!socket_slutpunkt_ejer(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (fil_post->register_data[3]) return -95;
        if (tegnkode > 512) return -90;
        if (tegnkode && !bruger_område(SEKUND_VÆRDI, tegnkode, 1)) return -14;
        pk_socklen_t buffer_kapacitet = 0;
        if (fil_post->register_data[4]) { KR = mail_produktoutput_check(fil_post->register_data[4], fil_post->register_data[5], &buffer_kapacitet); if (KR) return KR; }
        KR = 자바전문받기(첫째값, tegnkode); if (KR < 0) return KR;
        for (int 순번 = 0; 순번 < KR; 순번++) ((unsigned char *)SEKUND_VÆRDI)[순번] = 자바전문얻기(순번);
        if (fil_post->register_data[4]) mail_produktoutput(fil_post->register_data[4], fil_post->register_data[5], buffer_kapacitet, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return KR;
    }
    case 36: {
        if (!socket_slutpunkt_ejer(첫째값)) return -9;
        pk_socklen_t buffer_kapacitet;
        KR = mail_produktoutput_check(SEKUND_VÆRDI, tegnkode, &buffer_kapacitet); if (KR) return KR;
        mail_produktoutput(SEKUND_VÆRDI,tegnkode,buffer_kapacitet,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!socket_slutpunkt_ejer(첫째값))return -9;struct pk_sockaddr_in mail;
        KR=mail_input(SEKUND_VÆRDI,tegnkode,&mail);if(KR)return KR;
        return 자바흐름연결(첫째값,pk_htonl(mail.sin_addr.s_addr),pk_htons(mail.sin_port));
    }
    case 38: return 첫째값>=40&&socket_slutpunkt_ejer(첫째값)?자바흐름듣기(첫째값,SEKUND_VÆRDI):-9;
    case 39:
        if(첫째값<40||!socket_slutpunkt_ejer(첫째값))return -9;
        if(SEKUND_VÆRDI||tegnkode)return -95;KR=자바흐름연결받기(첫째값);if(KR>=40&&KR<56)통신끝점들[KR-32]=1;return KR;
    case 40: return 첫째값>=40&&socket_slutpunkt_ejer(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(bruger_ramme *fil_post) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(fil_post) : oprindelig_System_KALD(fil_post);
}
static void returnere_kerne(bruger_ramme *fil_post, int KR) {
    Stop_TIMEOUT();
    fil_post->register_data[0] = (uint64_t)(int64_t)KR;
    fil_post->kommando_placere = (uintptr_t)bruger_returnere;
    fil_post->status_KODE = 0x3c5; // EL1h, DAIF masked
}
int brugerundtagelse(bruger_ramme *fil_post, unsigned SKÆRING) {
    if (!Aktiv || (fil_post->status_KODE & 15) != 0) return 0;
    if (SKÆRING) {
        uint32_t anerkendelse_VÆRDI = maskine_register(IRQ_CPU_grænseflade + 0xc), identifikator_VÆRDI = anerkendelse_VÆRDI & 1023;
        if (identifikator_VÆRDI == 30) { returnere_kerne(fil_post, bruger_TIMEOUT); maskine_register(IRQ_CPU_grænseflade + 0x10) = anerkendelse_VÆRDI; return 1; }
        if (identifikator_VÆRDI < 1020) maskine_register(IRQ_CPU_grænseflade + 0x10) = anerkendelse_VÆRDI;
        return 1;
    }
    uint64_t undtagelse_status; __asm__ volatile("mrs %0, esr_el1" : "=r"(undtagelse_status));
    if (Ur_VÆRDI() >= deadline_TID) { returnere_kerne(fil_post, bruger_TIMEOUT); return 1; }
    unsigned undtagelse_område = undtagelse_status >> 26;
    if (undtagelse_område == 0x15 && (undtagelse_status & 0xffff) == 0) {
        if (리눅스규약 ? fil_post->register_data[8] == 93 || fil_post->register_data[8] == 94 : fil_post->register_data[8] == 6) returnere_kerne(fil_post, (int)(fil_post->register_data[0] & 255));
        else {
            intptr_t KR=체계호출(fil_post);
            if(KR==-4096&&interaktiv){
                저장값[ejer_objekt].udførelse_ramme=*fil_post;저장값[ejer_objekt].udførelse_ramme.kommando_placere-=4;
                사용자실수보관(저장값[ejer_objekt].flydende_tal_status);returnere_kerne(fil_post,사용자중단됨);
            }else fil_post->register_data[0]=(uint64_t)KR;
        }
    } else returnere_kerne(fil_post, undtagelse_område == 0x24 ? bruger_data_fejl : undtagelse_område == 0x20 ? bruger_udførelse_fejl : 사용자잘못된명령);
    return 1;
}

// 생성된 const ELF gruppe_VÆRDI: 실행은 반드시 app_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *data; size_t Størrelse; unsigned 전달값; } app;
#include "programs.h"
static void *billede(unsigned positionsindeks){return (void *)(0x04000000ul+positionsindeks*(bruger_afslutte_et_opkald-bruger_BASIS));}
static int Udfør_app(int KR){
    사용자누적시각[ejer_objekt]+=(uint32_t)보드밀리초()-bruger_udførelse_TID[ejer_objekt];
    Stop_TIMEOUT();Aktiv=0;
    if(KR==사용자중단됨){
        저장된작업 *streng_data=&저장값[ejer_objekt];streng_data->멈춤상태=1;streng_data->interaktiv=interaktiv;streng_data->리눅스규약=리눅스규약;streng_data->heap_Lager=heap_afslutte_et_opkald;streng_data->인수개수=전달인수개수;
        memcpy(streng_data->Tilladelser_Liste,Tilladelser_Liste,sizeof(Tilladelser_Liste));memcpy(streng_data->filliste,filliste,sizeof(filliste));memcpy(streng_data->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(streng_data->argument_MATRIX,전달인수,sizeof(전달인수));memcpy(streng_data->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<bruger_side_TÆL;순번++)if(Tilladelser_Liste[순번])memcpy((unsigned char *)billede(ejer_objekt)+순번*sidestørrelse,(void *)(bruger_BASIS+순번*sidestørrelse),sidestørrelse);
    }else{
        저장값[ejer_objekt].멈춤상태=0;starte_skærmbillede(ejer_objekt);
        for(unsigned 순번=0;순번<16;순번++)if(filliste[순번]>=0)pk_close(filliste[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])Luk_socket_slutpunkt(순번+32);
    }
    for(unsigned 순번=0;순번<bruger_side_TÆL;순번++){side_Liste[순번]=0;Tilladelser_Liste[순번]=0;}변환표맞추기();return KR;
}
uintptr_t Tavle_brugerkontrolelement(uintptr_t Handling){
    unsigned positionsindeks=Handling&15;if(positionsindeks>=4||Aktiv)return (uint32_t)-22;
    저장된작업 *streng_data=&저장값[positionsindeks];
    if(Handling>=32){if(streng_data->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(streng_data->filliste[순번]>=0)pk_close(streng_data->filliste[순번]);for(unsigned 순번=0;순번<24;순번++)if(streng_data->통신끝점들[순번])Luk_socket_slutpunkt(순번+32);}streng_data->멈춤상태=0;starte_skærmbillede(positionsindeks);return 0;}
    if(Handling>=16)return streng_data->멈춤상태;
    if(!streng_data->멈춤상태)return (uint32_t)-22;
    ejer_objekt=positionsindeks;interaktiv=streng_data->interaktiv;리눅스규약=streng_data->리눅스규약;heap_afslutte_et_opkald=streng_data->heap_Lager;전달인수개수=streng_data->인수개수;
    memcpy(filliste,streng_data->filliste,sizeof(filliste));memcpy(통신끝점들,streng_data->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,streng_data->argument_MATRIX,sizeof(전달인수));memcpy(전달인수길이,streng_data->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<bruger_side_TÆL;순번++)side_Liste[순번]=(bruger_BASIS+순번*sidestørrelse)|kerne_side;변환표맞추기();
    memset((void *)bruger_BASIS,0,bruger_afslutte_et_opkald-bruger_BASIS);
    for(unsigned 순번=0;순번<bruger_side_TÆL;순번++)if(streng_data->Tilladelser_Liste[순번])memcpy((void *)(bruger_BASIS+순번*sidestørrelse),(unsigned char *)billede(positionsindeks)+순번*sidestørrelse,sidestørrelse);
    memcpy(Tilladelser_Liste,streng_data->Tilladelser_Liste,sizeof(Tilladelser_Liste));
    for(unsigned 순번=0;순번<bruger_side_TÆL;순번++){unsigned data_placere=Tilladelser_Liste[순번];side_Liste[순번]=data_placere?(bruger_BASIS+순번*sidestørrelse)|(data_placere==3?bruger_læse_skrive:data_placere==5?사용자읽고실행:bruger_skrivebeskyttet):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");Aktiv=1;streng_data->멈춤상태=0;START_TIMEOUT();
    bruger_udførelse_TID[ejer_objekt]=보드밀리초();
    return (uint32_t)Udfør_app(bruger_CV(&streng_data->udførelse_ramme,streng_data->flydende_tal_status));
}
static int køre_app(const unsigned char *data, size_t Størrelse, unsigned 전달값, int 리눅스방식, const char *Navn) {
    if (Aktiv) return -16;
    ejer_objekt=Tavle_Terminal(11);if(ejer_objekt<0||ejer_objekt>3||저장값[ejer_objekt].멈춤상태)return -16;interaktiv=0;
    int gyldig = 실행파일검사(data, Størrelse, 리눅스방식); if (gyldig) return gyldig;
    리눅스규약 = 리눅스방식;
    unsigned navn_INDEKS=0;
    while (*Navn && navn_INDEKS<31) bruger_kommando_navn[ejer_objekt][navn_INDEKS++]=(unsigned char)*Navn++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (navn_INDEKS) bruger_kommando_navn[ejer_objekt][navn_INDEKS++]=' ';
        for (unsigned positionsindeks=0; positionsindeks<전달인수길이[0]; positionsindeks++) bruger_kommando_navn[ejer_objekt][navn_INDEKS++]=전달인수[0][positionsindeks];
    }
    bruger_kommando_navn[ejer_objekt][navn_INDEKS]=0; brugernummer[ejer_objekt]=Næste_brugernummer++;
    if (Næste_brugernummer>0x7fffffffu) Næste_brugernummer=10;
    bruger_START_TID[ejer_objekt]=보드밀리초(); 사용자누적시각[ejer_objekt]=0;
    for (unsigned 순번 = 0; 순번 < bruger_side_TÆL; 순번++) side_Liste[순번] = (bruger_BASIS + 순번 * sidestørrelse) | kerne_side;
    변환표맞추기();
    memset((void *)bruger_BASIS, 0, bruger_afslutte_et_opkald - bruger_BASIS);
    memset(Tilladelser_Liste, 0, sizeof(Tilladelser_Liste));
    실행파일머리 eksekverbar_fil_Header; memcpy(&eksekverbar_fil_Header, data, sizeof(eksekverbar_fil_Header));
    for (unsigned 순번 = 0; 순번 < eksekverbar_fil_Header.app_Header_TÆL; 순번++) {
        실행파일구획 data_placere; memcpy(&data_placere, data + eksekverbar_fil_Header.app_Header_FORSKYDNING + 순번 * sizeof(data_placere), sizeof(data_placere));
        if (data_placere.Type_område != 1 || !data_placere.기억영역크기) continue;
        if (data_placere.파일영역크기) memcpy((void *)(uintptr_t)data_placere.mail, data + data_placere.FORSKYDNING_VÆRDI, data_placere.파일영역크기);
        for (uintptr_t aktuel_placere = data_placere.mail & ~(sidestørrelse - 1); aktuel_placere < data_placere.mail + data_placere.기억영역크기; aktuel_placere += sidestørrelse) {
            Tilladelser_Liste[(aktuel_placere - bruger_BASIS) / sidestørrelse] = (data_placere.konfiguration_BITS & 2) ? 3 : ((data_placere.konfiguration_BITS & 1) ? 5 : 1);
        }
    }
    for (uintptr_t aktuel_placere = bruger_Stak_mail; aktuel_placere < bruger_afslutte_et_opkald; aktuel_placere += sidestørrelse) Tilladelser_Liste[(aktuel_placere - bruger_BASIS) / sidestørrelse] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(eksekverbar_fil_Header.indgangspunkt) : bruger_afslutte_et_opkald;
    for (unsigned 순번 = 0; 순번 < bruger_side_TÆL; 순번++) {
        unsigned tilladelser = Tilladelser_Liste[순번];
        side_Liste[순번] = tilladelser ? (bruger_BASIS + 순번 * sidestørrelse) | (tilladelser == 3 ? bruger_læse_skrive : tilladelser == 5 ? 사용자읽고실행 : bruger_skrivebeskyttet) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) filliste[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    heap_afslutte_et_opkald = bruger_Image_afslutte_et_opkald;
    Aktiv = 1; START_TIMEOUT();
    bruger_udførelse_TID[ejer_objekt]=보드밀리초();
    int KR = bruger_angive(eksekverbar_fil_Header.indgangspunkt, 초기쌓임공간, 전달값);
    return Udfør_app(KR);
}
uintptr_t Tavle_bruger_køre(uintptr_t Opslag_INDEKS) {
    if (Opslag_INDEKS >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Navn=Opslag_INDEKS==10?"javac":Opslag_INDEKS==11?"java":Opslag_INDEKS==12?"python":Opslag_INDEKS==13?"vi":Opslag_INDEKS==14?"jar":Opslag_INDEKS==15?"cc":Opslag_INDEKS==16?"jaot":"ELF";
    return (uint32_t)køre_app(실행항목들[Opslag_INDEKS].data, 실행항목들[Opslag_INDEKS].Størrelse, 실행항목들[Opslag_INDEKS].전달값, 0, Navn);
}
static uintptr_t Udfør_fil(int 리눅스방식) {
    static unsigned char Image[16384];
    if (Aktiv || !전달인수개수) return (uint32_t)-22;
    int fil_handle = pk_open((const char *)전달인수[0], skrivebeskyttet_VÆRDI, 0);
    if (fil_handle < 0) return (uint32_t)-fejlnummer;
    int Størrelse = pk_size(fil_handle);
    if (Størrelse < 0 || (unsigned)Størrelse > sizeof(Image)) { pk_close(fil_handle); return (uint32_t)-27; }
    int MODTAGET_VED_UDLØB_TÆL = pk_read(fil_handle, Image, Størrelse); pk_close(fil_handle);
    if (MODTAGET_VED_UDLØB_TÆL != Størrelse) return (uint32_t)-5;
    return (uint32_t)køre_app(Image, Størrelse, 0, 리눅스방식, "");
}
uintptr_t Tavle_bruger_fil(void) { return Udfør_fil(0); }
uintptr_t 보드사용자리눅스파일(void) { return Udfør_fil(1); }
uintptr_t Tavle_bruger_bekræfte(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].data, 잘못된실행항목들[순번].Størrelse) != bruger_eksekverbar_fil_fejl) return 순번 + 1;
    return 0;
}
