#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 Utfør_kommando maskin lag_VALUE. Fil data/정책은 기존 AOT Java 커널에 위임한다.
#include "brukar.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../Nettverk_Stabel/Nettverk_Stabel.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define maskin_registrere(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_distributør 0xff841000ul
#define IRQ_CPU_grensesnitt 0xff842000ul
#define sidestorleik 4096ul
#define 접근표시 (1ul << 10)
#define nei_Utfør_løyve (1ul << 53)
#define brukar_nei_Utfør (1ul << 54)
#define normal_Minne ((1ul << 2) | (3ul << 8) | 접근표시)
#define kjerne_side (3ul | normal_Minne | nei_Utfør_løyve | brukar_nei_Utfør)
#define brukar_lese_og_skrivetilgang (3ul | normal_Minne | (1ul << 6) | nei_Utfør_løyve | brukar_nei_Utfør)
#define brukar_skriveverna (3ul | normal_Minne | (3ul << 6) | nei_Utfør_løyve | brukar_nei_Utfør)
#define 사용자읽고실행 (3ul | normal_Minne | (3ul << 6) | nei_Utfør_løyve)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t Tavle_piksel(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t Tavle_Terminal(uintptr_t);
extern int Terminal_ventande(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int brukar_CV(brukar_rute *,void *);
extern void 사용자실수보관(void *);
extern int brukar_skrive_inn(uintptr_t oppføring_p, uintptr_t Stabel_Lagring, uintptr_t 전달값);
extern void brukar_levere_tilbake(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t rot_ADDRESS[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t side_Liste[brukar_side_COUNT] __attribute__((aligned(4096)));
static uint8_t løyve_Liste[brukar_side_COUNT];
static int aktiv, fil_Liste[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned fil_handtak){return fil_handtak<40?자바전문닫기(fil_handtak):자바흐름닫기(fil_handtak);}
static uint64_t FREQUENCY, 마감시각;
static uintptr_t 동적기억끝;
// kjerne_VALUE 셸이 준비한 UTF-8 Argument. EL0에는 kopiere_VALUE 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,interaktiv,리눅스규약,fil_Liste[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char argument_ARRAY[8][256],løyve_Liste[brukar_side_COUNT];
    uintptr_t 동적기억공간; brukar_rute 실행틀;
    unsigned char 실수저장상태[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int eigar_objekt,interaktiv;
static uint32_t brukarnummer[4], brukar_START_TIME[4], 사용자누적시각[4], 사용자실행시각[4], Neste_brukarnummer=10;
static unsigned char brukar_kommando_namn[4][288];
uint32_t 사용자상태읽기(unsigned oppføring_VALUE, unsigned INDEX) {
    unsigned plassere_INDEX=INDEX&3;
    int status_VALUE=(aktiv && eigar_objekt==(int)plassere_INDEX) ? 1 : 저장값[plassere_INDEX].멈춤상태 ? 2 : 0;
    if (oppføring_VALUE==0) return status_VALUE;
    if (!status_VALUE) return 0;
    if (oppføring_VALUE==1) return brukarnummer[plassere_INDEX];
    if (oppføring_VALUE==2) {
        unsigned char *쪽들=status_VALUE==1?løyve_Liste:저장값[plassere_INDEX].løyve_Liste;
        unsigned side_COUNT=0; for (unsigned 순번=0; 순번<brukar_side_COUNT; 순번++) if(쪽들[순번]) side_COUNT++;
        return side_COUNT*4;
    }
    if (oppføring_VALUE==3) return (uint32_t)보드밀리초()-brukar_START_TIME[plassere_INDEX];
    if (oppføring_VALUE==4) return 사용자누적시각[plassere_INDEX]+(status_VALUE==1?(uint32_t)보드밀리초()-사용자실행시각[plassere_INDEX]:0);
    if (oppføring_VALUE==5) return INDEX/4<sizeof(brukar_kommando_namn[0])?brukar_kommando_namn[plassere_INDEX][INDEX/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t oppføring_COUNT) {
    if (aktiv || oppføring_COUNT > 8) return (uint32_t)-22;
    전달인수개수 = oppføring_COUNT;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t LOOKUP_INDEX, uintptr_t betalt_plassere, uintptr_t byte_data) {
    if (aktiv || LOOKUP_INDEX >= 전달인수개수 || betalt_plassere >= 255 || betalt_plassere != 전달인수길이[LOOKUP_INDEX] || !byte_data || byte_data > 255)
        return (uint32_t)-22;
    전달인수[LOOKUP_INDEX][betalt_plassere] = byte_data;
    전달인수길이[LOOKUP_INDEX] = betalt_plassere + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Klokke_VALUE(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Stopp_TIMEOUT(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    maskin_registrere(IRQ_distributør + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void START_TIMEOUT(void) {
    uint64_t 간격 = FREQUENCY * 2, slå_på = 1;
    마감시각 = Klokke_VALUE() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(slå_på) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned data_Blokker = 0; data_Blokker < 4; data_Blokker++) {
        rot_ADDRESS[data_Blokker] = (uintptr_t)가운데[data_Blokker] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t ADDRESS = ((uintptr_t)data_Blokker << 30) | ((uintptr_t)순번 << 21);
            가운데[data_Blokker][순번] = ADDRESS | 1 | 접근표시 | brukar_nei_Utfør;
            if (ADDRESS >= 0xfc000000ul) 가운데[data_Blokker][순번] |= nei_Utfør_løyve; // Device-nGnRnE
            else 가운데[data_Blokker][순번] |= normal_Minne; // Normal, non-cacheable
        }
    }
    for (unsigned SECOND_VALUE = 0; SECOND_VALUE < brukar_side_COUNT / 512; SECOND_VALUE++)
        가운데[0][(brukar_BASE >> 21) + SECOND_VALUE] = (uintptr_t)(side_Liste + SECOND_VALUE * 512) | 3;
    for (unsigned 순번 = 0; 순번 < brukar_side_COUNT; 순번++) side_Liste[순번] = (brukar_BASE + 순번 * sidestorleik) | kjerne_side;
    uint64_t Minne_attributt_registrere = 0x4400, ADDRESS_Omsetjing_styring = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Minne_attributt_registrere), "r"(ADDRESS_Omsetjing_styring), "r"((uintptr_t)rot_ADDRESS) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t 실수저장상태 = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(실수저장상태) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    Stopp_TIMEOUT();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 oppføring_p_VALUE 때만 Tillat_VALUE.
    maskin_registrere(IRQ_distributør) = 0;
    maskin_registrere(IRQ_distributør + 0x180) = 0xffffffff;
    maskin_registrere(IRQ_distributør + 0x80) = 0xffffffff;
    maskin_registrere(IRQ_distributør + 0x280) = 1u << 30;
    maskin_registrere(IRQ_distributør + 0x41c) = 0x80808080;
    maskin_registrere(IRQ_distributør + 0x100) = 1u << 30;
    maskin_registrere(IRQ_CPU_grensesnitt + 4) = 0xff;
    maskin_registrere(IRQ_CPU_grensesnitt + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 informasjonsteknologi_normal 확인할 수 있다.
    int Tryggleik = (maskin_registrere(IRQ_distributør + 4) & (1u << 10)) != 0;
    maskin_registrere(IRQ_distributør) = Tryggleik ? 1 : 3;
    maskin_registrere(IRQ_CPU_grensesnitt) = Tryggleik ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t TYPE_kategori, maskin_TYPE; uint32_t 판번호;
    uint64_t oppføring_p, app_hode_OFFSET, del_hode_OFFSET; uint32_t 설정비트;
    uint16_t 실행머리크기, app_hode_oppføring_endre_storleik, app_hode_COUNT, del_hode_oppføring_endre_storleik, del_hode_COUNT, del_namn_tabell_INDEX;
} 실행파일머리;
typedef struct { uint32_t TYPE_kategori, 설정비트; uint64_t OFFSET_VALUE, ADDRESS, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(brukar_rute) == 272, "exception assembly layout");
static int 포함된범위(uint64_t OFFSET_VALUE, uint64_t Storleik, uint64_t avslutte_OFFSET) {
    return OFFSET_VALUE <= avslutte_OFFSET && Storleik <= avslutte_OFFSET - OFFSET_VALUE;
}
static int 부가정보검사(const unsigned char *data_plassere, size_t Storleik) {
    size_t betalt_plassere = 0;
    while (포함된범위(betalt_plassere, 12, Storleik)) {
        uint32_t 낱말들[3]; memcpy(낱말들, data_plassere + betalt_plassere, 12); betalt_plassere += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(betalt_plassere, 이름영역크기, Storleik) || !포함된범위(betalt_plassere + 이름영역크기, 설명크기, Storleik)) return 0;
        const unsigned char Namn[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Namn) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Namn); 순번++) if (data_plassere[betalt_plassere + 순번] != Namn[순번]) 일치 = 0;
        uint32_t 판번호 = 0;
        if (일치) memcpy(&판번호, data_plassere + betalt_plassere + 이름영역크기, 4);
        if (일치 && 판번호 == 1) return 1;
        betalt_plassere += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *data, size_t Storleik, int 리눅스방식) {
    if (Storleik < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, data, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.TYPE_kategori != 2 || 실행머리.maskin_TYPE != 183 || 실행머리.판번호 != 1 || 실행머리.설정비트 || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.app_hode_oppføring_endre_storleik != sizeof(실행파일구획) || !실행머리.app_hode_COUNT || 실행머리.app_hode_COUNT > 16 ||
        실행머리.app_hode_OFFSET < sizeof(실행머리) || !포함된범위(실행머리.app_hode_OFFSET, (uint64_t)실행머리.app_hode_COUNT * sizeof(실행파일구획), Storleik)) return 사용자실행파일오류;
    uint8_t 사용량[(brukar_IMAGE_avslutte - brukar_BASE) / sidestorleik] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.app_hode_COUNT; 순번++) {
        실행파일구획 data_plassere; memcpy(&data_plassere, data + 실행머리.app_hode_OFFSET + 순번 * sizeof(data_plassere), sizeof(data_plassere));
        if (data_plassere.TYPE_kategori == 4) {
            if (!포함된범위(data_plassere.OFFSET_VALUE, data_plassere.파일영역크기, Storleik)) return 사용자실행파일오류;
            if (부가정보검사(data + data_plassere.OFFSET_VALUE, data_plassere.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (data_plassere.TYPE_kategori == 0 || data_plassere.TYPE_kategori == 6 || (data_plassere.TYPE_kategori == 0x6474e551 && !(data_plassere.설정비트 & 1))) continue;
        if (data_plassere.TYPE_kategori != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!data_plassere.기억영역크기) continue;
        if (data_plassere.설정비트 & ~7u || !(data_plassere.설정비트 & 4) || (data_plassere.설정비트 & 3) == 3 || data_plassere.파일영역크기 > data_plassere.기억영역크기 ||
            (data_plassere.파일영역크기 && !포함된범위(data_plassere.OFFSET_VALUE, data_plassere.파일영역크기, Storleik)) || data_plassere.ADDRESS < brukar_BASE ||
            !포함된범위(data_plassere.ADDRESS, data_plassere.기억영역크기, brukar_IMAGE_avslutte) ||
            (!리눅스방식 && ((data_plassere.ADDRESS & (sidestorleik - 1)) || (data_plassere.OFFSET_VALUE & (sidestorleik - 1)) || data_plassere.맞춤 != sidestorleik)) ||
            (리눅스방식 && (((data_plassere.ADDRESS ^ data_plassere.OFFSET_VALUE) & (sidestorleik - 1)) || !data_plassere.맞춤 ||
                (data_plassere.맞춤 & (data_plassere.맞춤 - 1)) || data_plassere.맞춤 > 0x200000 || ((data_plassere.ADDRESS ^ data_plassere.OFFSET_VALUE) & (data_plassere.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (data_plassere.ADDRESS - brukar_BASE) / sidestorleik;
        unsigned oppføring_COUNT = ((data_plassere.ADDRESS & (sidestorleik - 1)) + data_plassere.기억영역크기 + sidestorleik - 1) / sidestorleik;
        for (unsigned side_VALUE = 첫항목; side_VALUE < 첫항목 + oppføring_COUNT; side_VALUE++) {
            if (사용량[side_VALUE]) return 사용자실행파일오류;
            사용량[side_VALUE] = 1;
        }
        if ((data_plassere.설정비트 & 1) && 실행머리.oppføring_p >= data_plassere.ADDRESS && 실행머리.oppføring_p < data_plassere.ADDRESS + data_plassere.파일영역크기 && !(실행머리.oppføring_p & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *data, size_t Storleik) { return 실행파일검사(data, Storleik, 0); }
static void sideoppsett(uintptr_t ADDRESS, uint64_t 설정비트, unsigned løyve) {
    unsigned LOOKUP_INDEX = (ADDRESS - brukar_BASE) / sidestorleik;
    side_Liste[LOOKUP_INDEX] = ADDRESS | 설정비트;
    løyve_Liste[LOOKUP_INDEX] = løyve;
}
static int 사용자범위(uintptr_t ADDRESS, size_t oppføring_COUNT, int 쓰는중) {
    if (ADDRESS < brukar_BASE || !포함된범위(ADDRESS, oppføring_COUNT, brukar_avslutte)) return 0;
    if (!oppføring_COUNT) return 1;
    unsigned 첫항목 = (ADDRESS - brukar_BASE) / sidestorleik, 마지막 = (ADDRESS + oppføring_COUNT - 1 - brukar_BASE) / sidestorleik;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(løyve_Liste[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int kopiere_bane(uintptr_t ADDRESS, char *STIGE) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!사용자범위(ADDRESS, 1, 0)) return -14;
        STIGE[순번] = *(const char *)ADDRESS++;
        if (!STIGE[순번]) return 0;
    }
    return -36;
}
static intptr_t kjerne_forretningsmål(intptr_t forretningsmål) { return forretningsmål < 0 ? -feilnummer : forretningsmål; }
static int 대응파일기술자(uint64_t fil_handtak) { return fil_handtak >= 3 && fil_handtak < 19 ? fil_Liste[fil_handtak - 3] : -1; }
static int 통신끝점소유(uint64_t fil_handtak) { return fil_handtak >= 32 && fil_handtak < 56 && 통신끝점들[fil_handtak - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t lengd_VALUE, struct pk_sockaddr_in *ADDRESS) {
    if (lengd_VALUE != sizeof(*ADDRESS)) return -22;
    if (!사용자범위(가리킴값, lengd_VALUE, 0)) return -14;
    memcpy(ADDRESS, (const void *)가리킴값, sizeof(*ADDRESS));
    return ADDRESS->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t lengd_peikar, pk_socklen_t *수용량) {
    if (!사용자범위(lengd_peikar, sizeof(*수용량), 1)) return -14;
    memcpy(수용량, (const void *)lengd_peikar, sizeof(*수용량));
    if (*수용량 > sizeof(struct pk_sockaddr_in)) *수용량 = sizeof(struct pk_sockaddr_in);
    if (*수용량 && !사용자범위(가리킴값, *수용량, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t lengd_peikar, pk_socklen_t 수용량, int ADDRESS, int portnummer) {
    struct pk_sockaddr_in VALUE; memset(&VALUE, 0, sizeof(VALUE));
    VALUE.sin_family = AF_INET; VALUE.sin_port = pk_htons(portnummer); VALUE.sin_addr.s_addr = pk_htonl(ADDRESS);
    if (수용량) memcpy((void *)가리킴값, &VALUE, 수용량);
    pk_socklen_t lengd_VALUE = sizeof(VALUE); memcpy((void *)lengd_peikar, &lengd_VALUE, sizeof(lengd_VALUE));
}
extern uintptr_t Tavle_kanal(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(brukar_rute *fil_oppføring) {
    uintptr_t 첫째값 = fil_oppføring->registrere_data[0], SECOND_VALUE = fil_oppføring->registrere_data[1], teiknkode = fil_oppføring->registrere_data[2];
    char STIGE[65];
    int fil_handtak, forretningsmål;
    switch (fil_oppføring->registrere_data[8]) {
    case 0: return 1; // 자체 ABI 버전
    case 1: // write: peikar 전체를 검사한 TILBAKE_VALUE Utdata/Fil endre_VALUE
        if (teiknkode > 65536) return -22;
        if (!사용자범위(SECOND_VALUE, teiknkode, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=Klokke_VALUE();
            for (size_t 순번 = 0; 순번 < teiknkode; 순번++) Tavle_kanal(첫째값, ((const unsigned char *)SECOND_VALUE)[순번]);
            /* 큰 tty를 그린 kjerne_VALUE 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(interaktiv){
                마감시각+=Klokke_VALUE()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(마감시각) : "memory");
            }
            return teiknkode;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t vare_COUNT=teiknkode>512?512:teiknkode;for(size_t 순번=0;순번<vare_COUNT;순번++)자바전문넣기(순번,((const unsigned char *)SECOND_VALUE)[순번]);return 자바흐름쓰기(첫째값,vare_COUNT);
        }
        fil_handtak = 대응파일기술자(첫째값); if (fil_handtak < 0) return -9;
        return kjerne_forretningsmål(pk_write(fil_handtak, (const void *)SECOND_VALUE, teiknkode));
    case 2:
        if (teiknkode > 65536) return -22;
        if (!사용자범위(SECOND_VALUE, teiknkode, 1)) return -14;
        if (첫째값 == 0) {
            size_t vare_COUNT = 0;
            while (vare_COUNT < teiknkode) {
                int teikn_VALUE = (int32_t)보드글자읽기(); if (teikn_VALUE == -2) return vare_COUNT; if (teikn_VALUE < 0) break;
                ((unsigned char *)SECOND_VALUE)[vare_COUNT++] = teikn_VALUE;
            }
            return vare_COUNT ? (intptr_t)vare_COUNT : (teiknkode ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            forretningsmål=자바흐름읽기(첫째값,teiknkode>512?512:teiknkode);if(forretningsmål>0)for(int 순번=0;순번<forretningsmål;순번++)((unsigned char *)SECOND_VALUE)[순번]=자바전문얻기(순번);return forretningsmål;
        }
        fil_handtak = 대응파일기술자(첫째값); if (fil_handtak < 0) return -9;
        return kjerne_forretningsmål(pk_read(fil_handtak, (void *)SECOND_VALUE, teiknkode));
    case 3:
        forretningsmål = kopiere_bane(첫째값, STIGE); if (forretningsmål) return forretningsmål;
        if (SECOND_VALUE > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (fil_Liste[순번] < 0) {
            fil_handtak = pk_open(STIGE, (int)SECOND_VALUE, 0600);
            if (fil_handtak < 0) return -feilnummer;
            fil_Liste[순번] = fil_handtak; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { forretningsmål = 통신끝점닫기(첫째값); if (!forretningsmål) 통신끝점들[첫째값 - 32] = 0; return forretningsmål; }
        fil_handtak = 대응파일기술자(첫째값); if (fil_handtak < 0) return -9;
        forretningsmål = pk_close(fil_handtak); if (!forretningsmål) fil_Liste[첫째값 - 3] = -1;
        return kjerne_forretningsmål(forretningsmål);
    case 5:
        fil_handtak = 대응파일기술자(첫째값); if (fil_handtak < 0) return -9;
        if (teiknkode > 2) return -22;
        return kjerne_forretningsmål(pk_lseek(fil_handtak, (int64_t)SECOND_VALUE, teiknkode));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 brukar RW/NX 힙, 새로 노출되는 페이지는 0으로 starte
        if (!첫째값) return 동적기억끝;
        if (첫째값 < brukar_IMAGE_avslutte || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + sidestorleik - 1) & ~(sidestorleik - 1);
        uintptr_t 새쪽들 = (첫째값 + sidestorleik - 1) & ~(sidestorleik - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t data_plassere = 이전쪽들; data_plassere < 새쪽들; data_plassere += sidestorleik) sideoppsett(data_plassere, kjerne_side, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t data_plassere = 이전쪽들; data_plassere < 새쪽들; data_plassere += sidestorleik) sideoppsett(data_plassere, brukar_lese_og_skrivetilgang, 3);
        } else {
            for (uintptr_t data_plassere = 새쪽들; data_plassere < 이전쪽들; data_plassere += sidestorleik) {
                side_Liste[(data_plassere - brukar_BASE) / sidestorleik] = 0; løyve_Liste[(data_plassere - brukar_BASE) / sidestorleik] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        fil_handtak = 대응파일기술자(첫째값); return fil_handtak < 0 ? -9 : kjerne_forretningsmål(pk_size(fil_handtak));
    case 10:
        fil_handtak = 대응파일기술자(첫째값); return fil_handtak < 0 ? -9 : kjerne_forretningsmål(pk_ftruncate(fil_handtak, (int64_t)SECOND_VALUE));
    case 11:
        forretningsmål = kopiere_bane(첫째값, STIGE); return forretningsmål ? forretningsmål : kjerne_forretningsmål(pk_unlink(STIGE));
    case 12:
        fil_handtak = 대응파일기술자(첫째값); return fil_handtak < 0 ? -9 : kjerne_forretningsmål(pk_fsync(fil_handtak));
    case 13: { // 그래픽 기초 API: brukar 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = fil_oppføring->registrere_data[3], 높이값 = fil_oppføring->registrere_data[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SECOND_VALUE > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - SECOND_VALUE) return -22;
        for (uintptr_t Y_koordinat = SECOND_VALUE; Y_koordinat < SECOND_VALUE + 높이값; Y_koordinat++) for (uintptr_t x_koordinat = 첫째값; x_koordinat < 첫째값 + 너비값; x_koordinat++) Tavle_piksel(x_koordinat, Y_koordinat, teiknkode);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=vare_COUNT; args(index,buffer,capacity)=UTF-8 lengd_VALUE
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (teiknkode <= 전달인수길이[첫째값]) return -36;
        if (!사용자범위(SECOND_VALUE, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SECOND_VALUE, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;interaktiv=1;return Tavle_Terminal(13);}
        if(첫째값==2){interaktiv=0;return 0;}
        if(첫째값==3)return Tavle_Terminal(13);
        if(첫째값!=1||!interaktiv)return -22;
        forretningsmål=(int32_t)보드글자읽기();
        if(forretningsmål==-4096)return forretningsmål;
        START_TIMEOUT();return forretningsmål<0?-11:forretningsmål;
    case 17: { // 유한한 협력 vent_VALUE: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t avslutte_TIME = Klokke_VALUE() + FREQUENCY * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Klokke_VALUE() < avslutte_TIME);
        START_TIMEOUT(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 forelder_VALUE·빈 폴더를 검사한다.
        if (SECOND_VALUE > 2) return -22;
        forretningsmål = kopiere_bane(첫째값, STIGE); if (forretningsmål) return forretningsmål;
        unsigned lengd_VALUE = 0; while (STIGE[lengd_VALUE]) lengd_VALUE++;
        forretningsmål = 자바경로시작(lengd_VALUE); if (forretningsmål < 0) return forretningsmål;
        for (unsigned 순번 = 0; 순번 < lengd_VALUE; 순번++) 자바경로바이트(순번, (unsigned char)STIGE[순번]);
        return SECOND_VALUE == 0 ? 자바항목종류() : SECOND_VALUE == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int teikn_VALUE=(int32_t)보드글자읽기();if(teikn_VALUE==-4096)return teikn_VALUE;if(teikn_VALUE>=0)화면누름(eigar_objekt,teikn_VALUE);START_TIMEOUT();}
        if(첫째값==3&&teiknkode){if(!자바셸대화형())return -95;interaktiv=1;Tavle_Terminal(300);}
        return 화면호출(eigar_objekt,첫째값,SECOND_VALUE,teiknkode,fil_oppføring->registrere_data[3],fil_oppføring->registrere_data[4],fil_oppføring->registrere_data[5]);
    case 21:
        if(teiknkode>127)return -22;if(!사용자범위(SECOND_VALUE,teiknkode*sizeof(uint32_t),0))return -14;
        return 화면글(eigar_objekt,첫째값,(const uint32_t *)SECOND_VALUE,teiknkode);
    case 22: // 화면 Storleik spørjing_VALUE: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SECOND_VALUE==SOCK_STREAM&&(teiknkode==0||teiknkode==6))forretningsmål=자바흐름만들기();
        else if(SECOND_VALUE==SOCK_DGRAM&&(teiknkode==0||teiknkode==IPPROTO_UDP))forretningsmål=자바전문만들기(첫째값,SECOND_VALUE,teiknkode);
        else return -93;
        if (forretningsmål >= 32 && forretningsmål < 56) 통신끝점들[forretningsmål - 32] = 1;
        return forretningsmål;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in ADDRESS;
        forretningsmål = 주소입력(SECOND_VALUE, teiknkode, &ADDRESS); if (forretningsmål) return forretningsmål;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(ADDRESS.sin_addr.s_addr),pk_htons(ADDRESS.sin_port)):자바전문묶기(첫째값, pk_htonl(ADDRESS.sin_addr.s_addr), pk_htons(ADDRESS.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (fil_oppføring->registrere_data[3]) return -95;
        if (teiknkode > 512) return -90;
        if (teiknkode && !사용자범위(SECOND_VALUE, teiknkode, 0)) return -14;
        struct pk_sockaddr_in ADDRESS;
        forretningsmål = 주소입력(fil_oppføring->registrere_data[4], fil_oppføring->registrere_data[5], &ADDRESS); if (forretningsmål) return forretningsmål;
        for (unsigned 순번 = 0; 순번 < teiknkode; 순번++) 자바전문넣기(순번, ((const unsigned char *)SECOND_VALUE)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(ADDRESS.sin_addr.s_addr), pk_htons(ADDRESS.sin_port), teiknkode);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (fil_oppføring->registrere_data[3]) return -95;
        if (teiknkode > 512) return -90;
        if (teiknkode && !사용자범위(SECOND_VALUE, teiknkode, 1)) return -14;
        pk_socklen_t 수용량 = 0;
        if (fil_oppføring->registrere_data[4]) { forretningsmål = 주소출력검사(fil_oppføring->registrere_data[4], fil_oppføring->registrere_data[5], &수용량); if (forretningsmål) return forretningsmål; }
        forretningsmål = 자바전문받기(첫째값, teiknkode); if (forretningsmål < 0) return forretningsmål;
        for (int 순번 = 0; 순번 < forretningsmål; 순번++) ((unsigned char *)SECOND_VALUE)[순번] = 자바전문얻기(순번);
        if (fil_oppføring->registrere_data[4]) 주소출력(fil_oppføring->registrere_data[4], fil_oppføring->registrere_data[5], 수용량, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return forretningsmål;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t 수용량;
        forretningsmål = 주소출력검사(SECOND_VALUE, teiknkode, &수용량); if (forretningsmål) return forretningsmål;
        주소출력(SECOND_VALUE,teiknkode,수용량,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in ADDRESS;
        forretningsmål=주소입력(SECOND_VALUE,teiknkode,&ADDRESS);if(forretningsmål)return forretningsmål;
        return 자바흐름연결(첫째값,pk_htonl(ADDRESS.sin_addr.s_addr),pk_htons(ADDRESS.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,SECOND_VALUE):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(SECOND_VALUE||teiknkode)return -95;forretningsmål=자바흐름연결받기(첫째값);if(forretningsmål>=40&&forretningsmål<56)통신끝점들[forretningsmål-32]=1;return forretningsmål;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(brukar_rute *fil_oppføring) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(fil_oppføring) : 자체체계호출(fil_oppføring);
}
static void levere_tilbake_kjerne(brukar_rute *fil_oppføring, int forretningsmål) {
    Stopp_TIMEOUT();
    fil_oppføring->registrere_data[0] = (uint64_t)(int64_t)forretningsmål;
    fil_oppføring->kommando_plassere = (uintptr_t)brukar_levere_tilbake;
    fil_oppføring->status_CODE = 0x3c5; // EL1h, DAIF masked
}
int brukar_unntak(brukar_rute *fil_oppføring, unsigned INTERCEPT) {
    if (!aktiv || (fil_oppføring->status_CODE & 15) != 0) return 0;
    if (INTERCEPT) {
        uint32_t 승인값 = maskin_registrere(IRQ_CPU_grensesnitt + 0xc), identifikator_VALUE = 승인값 & 1023;
        if (identifikator_VALUE == 30) { levere_tilbake_kjerne(fil_oppføring, brukar_TIMEOUT); maskin_registrere(IRQ_CPU_grensesnitt + 0x10) = 승인값; return 1; }
        if (identifikator_VALUE < 1020) maskin_registrere(IRQ_CPU_grensesnitt + 0x10) = 승인값;
        return 1;
    }
    uint64_t unntak_status; __asm__ volatile("mrs %0, esr_el1" : "=r"(unntak_status));
    if (Klokke_VALUE() >= 마감시각) { levere_tilbake_kjerne(fil_oppføring, brukar_TIMEOUT); return 1; }
    unsigned unntak_kategori = unntak_status >> 26;
    if (unntak_kategori == 0x15 && (unntak_status & 0xffff) == 0) {
        if (리눅스규약 ? fil_oppføring->registrere_data[8] == 93 || fil_oppføring->registrere_data[8] == 94 : fil_oppføring->registrere_data[8] == 6) levere_tilbake_kjerne(fil_oppføring, (int)(fil_oppføring->registrere_data[0] & 255));
        else {
            intptr_t forretningsmål=체계호출(fil_oppføring);
            if(forretningsmål==-4096&&interaktiv){
                저장값[eigar_objekt].실행틀=*fil_oppføring;저장값[eigar_objekt].실행틀.kommando_plassere-=4;
                사용자실수보관(저장값[eigar_objekt].실수저장상태);levere_tilbake_kjerne(fil_oppføring,사용자중단됨);
            }else fil_oppføring->registrere_data[0]=(uint64_t)forretningsmål;
        }
    } else levere_tilbake_kjerne(fil_oppføring, unntak_kategori == 0x24 ? brukar_data_feil : unntak_kategori == 0x20 ? 사용자실행오류 : brukar_ugyldig_instruksjon);
    return 1;
}

// 생성된 const ELF gruppe_VALUE: 실행은 반드시 app_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *data; size_t Storleik; unsigned 전달값; } app;
#include "programs.h"
static void *skuggekopi(unsigned plassere_INDEX){return (void *)(0x04000000ul+plassere_INDEX*(brukar_avslutte-brukar_BASE));}
static int Ferdig_app(int forretningsmål){
    사용자누적시각[eigar_objekt]+=(uint32_t)보드밀리초()-사용자실행시각[eigar_objekt];
    Stopp_TIMEOUT();aktiv=0;
    if(forretningsmål==사용자중단됨){
        저장된작업 *streng_data=&저장값[eigar_objekt];streng_data->멈춤상태=1;streng_data->interaktiv=interaktiv;streng_data->리눅스규약=리눅스규약;streng_data->동적기억공간=동적기억끝;streng_data->인수개수=전달인수개수;
        memcpy(streng_data->løyve_Liste,løyve_Liste,sizeof(løyve_Liste));memcpy(streng_data->fil_Liste,fil_Liste,sizeof(fil_Liste));memcpy(streng_data->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(streng_data->argument_ARRAY,전달인수,sizeof(전달인수));memcpy(streng_data->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<brukar_side_COUNT;순번++)if(løyve_Liste[순번])memcpy((unsigned char *)skuggekopi(eigar_objekt)+순번*sidestorleik,(void *)(brukar_BASE+순번*sidestorleik),sidestorleik);
    }else{
        저장값[eigar_objekt].멈춤상태=0;화면초기화(eigar_objekt);
        for(unsigned 순번=0;순번<16;순번++)if(fil_Liste[순번]>=0)pk_close(fil_Liste[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<brukar_side_COUNT;순번++){side_Liste[순번]=0;løyve_Liste[순번]=0;}변환표맞추기();return forretningsmål;
}
uintptr_t Tavle_brukarkontroll(uintptr_t Handling){
    unsigned plassere_INDEX=Handling&15;if(plassere_INDEX>=4||aktiv)return (uint32_t)-22;
    저장된작업 *streng_data=&저장값[plassere_INDEX];
    if(Handling>=32){if(streng_data->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(streng_data->fil_Liste[순번]>=0)pk_close(streng_data->fil_Liste[순번]);for(unsigned 순번=0;순번<24;순번++)if(streng_data->통신끝점들[순번])통신끝점닫기(순번+32);}streng_data->멈춤상태=0;화면초기화(plassere_INDEX);return 0;}
    if(Handling>=16)return streng_data->멈춤상태;
    if(!streng_data->멈춤상태)return (uint32_t)-22;
    eigar_objekt=plassere_INDEX;interaktiv=streng_data->interaktiv;리눅스규약=streng_data->리눅스규약;동적기억끝=streng_data->동적기억공간;전달인수개수=streng_data->인수개수;
    memcpy(fil_Liste,streng_data->fil_Liste,sizeof(fil_Liste));memcpy(통신끝점들,streng_data->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,streng_data->argument_ARRAY,sizeof(전달인수));memcpy(전달인수길이,streng_data->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<brukar_side_COUNT;순번++)side_Liste[순번]=(brukar_BASE+순번*sidestorleik)|kjerne_side;변환표맞추기();
    memset((void *)brukar_BASE,0,brukar_avslutte-brukar_BASE);
    for(unsigned 순번=0;순번<brukar_side_COUNT;순번++)if(streng_data->løyve_Liste[순번])memcpy((void *)(brukar_BASE+순번*sidestorleik),(unsigned char *)skuggekopi(plassere_INDEX)+순번*sidestorleik,sidestorleik);
    memcpy(løyve_Liste,streng_data->løyve_Liste,sizeof(løyve_Liste));
    for(unsigned 순번=0;순번<brukar_side_COUNT;순번++){unsigned data_plassere=løyve_Liste[순번];side_Liste[순번]=data_plassere?(brukar_BASE+순번*sidestorleik)|(data_plassere==3?brukar_lese_og_skrivetilgang:data_plassere==5?사용자읽고실행:brukar_skriveverna):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");aktiv=1;streng_data->멈춤상태=0;START_TIMEOUT();
    사용자실행시각[eigar_objekt]=보드밀리초();
    return (uint32_t)Ferdig_app(brukar_CV(&streng_data->실행틀,streng_data->실수저장상태));
}
static int køyre_app(const unsigned char *data, size_t Storleik, unsigned 전달값, int 리눅스방식, const char *Namn) {
    if (aktiv) return -16;
    eigar_objekt=Tavle_Terminal(11);if(eigar_objekt<0||eigar_objekt>3||저장값[eigar_objekt].멈춤상태)return -16;interaktiv=0;
    int 유효함 = 실행파일검사(data, Storleik, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned namn_INDEX=0;
    while (*Namn && namn_INDEX<31) brukar_kommando_namn[eigar_objekt][namn_INDEX++]=(unsigned char)*Namn++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (namn_INDEX) brukar_kommando_namn[eigar_objekt][namn_INDEX++]=' ';
        for (unsigned plassere_INDEX=0; plassere_INDEX<전달인수길이[0]; plassere_INDEX++) brukar_kommando_namn[eigar_objekt][namn_INDEX++]=전달인수[0][plassere_INDEX];
    }
    brukar_kommando_namn[eigar_objekt][namn_INDEX]=0; brukarnummer[eigar_objekt]=Neste_brukarnummer++;
    if (Neste_brukarnummer>0x7fffffffu) Neste_brukarnummer=10;
    brukar_START_TIME[eigar_objekt]=보드밀리초(); 사용자누적시각[eigar_objekt]=0;
    for (unsigned 순번 = 0; 순번 < brukar_side_COUNT; 순번++) side_Liste[순번] = (brukar_BASE + 순번 * sidestorleik) | kjerne_side;
    변환표맞추기();
    memset((void *)brukar_BASE, 0, brukar_avslutte - brukar_BASE);
    memset(løyve_Liste, 0, sizeof(løyve_Liste));
    실행파일머리 실행머리; memcpy(&실행머리, data, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.app_hode_COUNT; 순번++) {
        실행파일구획 data_plassere; memcpy(&data_plassere, data + 실행머리.app_hode_OFFSET + 순번 * sizeof(data_plassere), sizeof(data_plassere));
        if (data_plassere.TYPE_kategori != 1 || !data_plassere.기억영역크기) continue;
        if (data_plassere.파일영역크기) memcpy((void *)(uintptr_t)data_plassere.ADDRESS, data + data_plassere.OFFSET_VALUE, data_plassere.파일영역크기);
        for (uintptr_t betalt_plassere = data_plassere.ADDRESS & ~(sidestorleik - 1); betalt_plassere < data_plassere.ADDRESS + data_plassere.기억영역크기; betalt_plassere += sidestorleik) {
            løyve_Liste[(betalt_plassere - brukar_BASE) / sidestorleik] = (data_plassere.설정비트 & 2) ? 3 : ((data_plassere.설정비트 & 1) ? 5 : 1);
        }
    }
    for (uintptr_t betalt_plassere = brukar_Stabel_ADDRESS; betalt_plassere < brukar_avslutte; betalt_plassere += sidestorleik) løyve_Liste[(betalt_plassere - brukar_BASE) / sidestorleik] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.oppføring_p) : brukar_avslutte;
    for (unsigned 순번 = 0; 순번 < brukar_side_COUNT; 순번++) {
        unsigned løyve = løyve_Liste[순번];
        side_Liste[순번] = løyve ? (brukar_BASE + 순번 * sidestorleik) | (løyve == 3 ? brukar_lese_og_skrivetilgang : løyve == 5 ? 사용자읽고실행 : brukar_skriveverna) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) fil_Liste[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = brukar_IMAGE_avslutte;
    aktiv = 1; START_TIMEOUT();
    사용자실행시각[eigar_objekt]=보드밀리초();
    int forretningsmål = brukar_skrive_inn(실행머리.oppføring_p, 초기쌓임공간, 전달값);
    return Ferdig_app(forretningsmål);
}
uintptr_t Tavle_brukar_køyre(uintptr_t LOOKUP_INDEX) {
    if (LOOKUP_INDEX >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Namn=LOOKUP_INDEX==10?"javac":LOOKUP_INDEX==11?"java":LOOKUP_INDEX==12?"python":LOOKUP_INDEX==13?"vi":LOOKUP_INDEX==14?"jar":LOOKUP_INDEX==15?"cc":LOOKUP_INDEX==16?"jaot":"ELF";
    return (uint32_t)køyre_app(실행항목들[LOOKUP_INDEX].data, 실행항목들[LOOKUP_INDEX].Storleik, 실행항목들[LOOKUP_INDEX].전달값, 0, Namn);
}
static uintptr_t Utfør_fil(int 리눅스방식) {
    static unsigned char IMAGE[16384];
    if (aktiv || !전달인수개수) return (uint32_t)-22;
    int fil_handtak = pk_open((const char *)전달인수[0], skriveverna_VALUE, 0);
    if (fil_handtak < 0) return (uint32_t)-feilnummer;
    int Storleik = pk_size(fil_handtak);
    if (Storleik < 0 || (unsigned)Storleik > sizeof(IMAGE)) { pk_close(fil_handtak); return (uint32_t)-27; }
    int RECEIVED_COUNT = pk_read(fil_handtak, IMAGE, Storleik); pk_close(fil_handtak);
    if (RECEIVED_COUNT != Storleik) return (uint32_t)-5;
    return (uint32_t)køyre_app(IMAGE, Storleik, 0, 리눅스방식, "");
}
uintptr_t Tavle_brukar_fil(void) { return Utfør_fil(0); }
uintptr_t 보드사용자리눅스파일(void) { return Utfør_fil(1); }
uintptr_t Tavle_brukar_bekrefte(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].data, 잘못된실행항목들[순번].Storleik) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
