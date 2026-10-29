#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 Izpildīt_komanda mašīna slānis_VALUE. Fails dati/정책은 기존 AOT Java 커널에 위임한다.
#include "lietotājs.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../tīkls_kopa/tīkls_kopa.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define mašīna_reģistrs(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_izplatītājs 0xff841000ul
#define IRQ_centrālais_procesors_interfeiss 0xff842000ul
#define lappuses_izmēri 4096ul
#define piekļūt_marķieris (1ul << 10)
#define nē_Izpildīt_atļauja (1ul << 53)
#define lietotājs_nē_Izpildīt (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | piekļūt_marķieris)
#define kodols_lapa (3ul | 보통기억 | nē_Izpildīt_atļauja | lietotājs_nē_Izpildīt)
#define 사용자읽고쓰기 (3ul | 보통기억 | (1ul << 6) | nē_Izpildīt_atļauja | lietotājs_nē_Izpildīt)
#define lietotājs_tikai_lasāms (3ul | 보통기억 | (3ul << 6) | nē_Izpildīt_atļauja | lietotājs_nē_Izpildīt)
#define 사용자읽고실행 (3ul | 보통기억 | (3ul << 6) | nē_Izpildīt_atļauja)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t Panelis_attēla_elements(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t Panelis_Terminālis(uintptr_t);
extern int Terminālis_gaida(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int lietotājs_CV(lietotājs_kadrs *,void *);
extern void 사용자실수보관(void *);
extern int lietotājs_ievadīt(uintptr_t ieejas_punkts, uintptr_t kopa_Krātuve, uintptr_t 전달값);
extern void lietotājs_atdot(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t sakne_adrese[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t lapa_Saraksts[lietotājs_lapa_COUNT] __attribute__((aligned(4096)));
static uint8_t Atļaujas_Saraksts[lietotājs_lapa_COUNT];
static int Aktīvs, Fails_Saraksts[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned Fails_turis){return Fails_turis<40?자바전문닫기(Fails_turis):자바흐름닫기(Fails_turis);}
static uint64_t FREQUENCY, izpildes_termiņš_TIME;
static uintptr_t kaudze_beigt_zvanu;
// kodols_VALUE 셸이 준비한 UTF-8 Parametri. EL0에는 kopēt_VALUE 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,대화형,리눅스규약,Fails_Saraksts[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char arg_ARRAY[8][256],Atļaujas_Saraksts[lietotājs_lapa_COUNT];
    uintptr_t kaudze_Krātuve; lietotājs_kadrs 실행틀;
    unsigned char peldošs_p_Statuss[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int īpašnieks_objekts,대화형;
static uint32_t lietotāja_numurs[4], lietotājs_Sākt_TIME[4], 사용자누적시각[4], 사용자실행시각[4], Tālāk_lietotāja_numurs=10;
static unsigned char lietotājs_komanda_nosaukums[4][288];
uint32_t 사용자상태읽기(unsigned ievade_VALUE, unsigned INDEX) {
    unsigned pozīcijas_indekss=INDEX&3;
    int Statuss_VALUE=(Aktīvs && īpašnieks_objekts==(int)pozīcijas_indekss) ? 1 : 저장값[pozīcijas_indekss].멈춤상태 ? 2 : 0;
    if (ievade_VALUE==0) return Statuss_VALUE;
    if (!Statuss_VALUE) return 0;
    if (ievade_VALUE==1) return lietotāja_numurs[pozīcijas_indekss];
    if (ievade_VALUE==2) {
        unsigned char *쪽들=Statuss_VALUE==1?Atļaujas_Saraksts:저장값[pozīcijas_indekss].Atļaujas_Saraksts;
        unsigned lapa_COUNT=0; for (unsigned 순번=0; 순번<lietotājs_lapa_COUNT; 순번++) if(쪽들[순번]) lapa_COUNT++;
        return lapa_COUNT*4;
    }
    if (ievade_VALUE==3) return (uint32_t)보드밀리초()-lietotājs_Sākt_TIME[pozīcijas_indekss];
    if (ievade_VALUE==4) return 사용자누적시각[pozīcijas_indekss]+(Statuss_VALUE==1?(uint32_t)보드밀리초()-사용자실행시각[pozīcijas_indekss]:0);
    if (ievade_VALUE==5) return INDEX/4<sizeof(lietotājs_komanda_nosaukums[0])?lietotājs_komanda_nosaukums[pozīcijas_indekss][INDEX/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t ievade_COUNT) {
    if (Aktīvs || ievade_COUNT > 8) return (uint32_t)-22;
    전달인수개수 = ievade_COUNT;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t LOOKUP_INDEX, uintptr_t pašreizējais_amats, uintptr_t byte_dati) {
    if (Aktīvs || LOOKUP_INDEX >= 전달인수개수 || pašreizējais_amats >= 255 || pašreizējais_amats != 전달인수길이[LOOKUP_INDEX] || !byte_dati || byte_dati > 255)
        return (uint32_t)-22;
    전달인수[LOOKUP_INDEX][pašreizējais_amats] = byte_dati;
    전달인수길이[LOOKUP_INDEX] = pašreizējais_amats + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Pulkstenis_VALUE(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Stop_NOILGUMS(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    mašīna_reģistrs(IRQ_izplatītājs + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void Sākt_NOILGUMS(void) {
    uint64_t 간격 = FREQUENCY * 2, ieslēgt = 1;
    izpildes_termiņš_TIME = Pulkstenis_VALUE() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(ieslēgt) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned datu_bloks = 0; datu_bloks < 4; datu_bloks++) {
        sakne_adrese[datu_bloks] = (uintptr_t)가운데[datu_bloks] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t adrese = ((uintptr_t)datu_bloks << 30) | ((uintptr_t)순번 << 21);
            가운데[datu_bloks][순번] = adrese | 1 | piekļūt_marķieris | lietotājs_nē_Izpildīt;
            if (adrese >= 0xfc000000ul) 가운데[datu_bloks][순번] |= nē_Izpildīt_atļauja; // Device-nGnRnE
            else 가운데[datu_bloks][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned SECOND_VALUE = 0; SECOND_VALUE < lietotājs_lapa_COUNT / 512; SECOND_VALUE++)
        가운데[0][(lietotājs_BASE >> 21) + SECOND_VALUE] = (uintptr_t)(lapa_Saraksts + SECOND_VALUE * 512) | 3;
    for (unsigned 순번 = 0; 순번 < lietotājs_lapa_COUNT; 순번++) lapa_Saraksts[순번] = (lietotājs_BASE + 순번 * lappuses_izmēri) | kodols_lapa;
    uint64_t atmiņa_atribūts_reģistrs = 0x4400, adrese_Tulkošana_vadība = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(atmiņa_atribūts_reģistrs), "r"(adrese_Tulkošana_vadība), "r"((uintptr_t)sakne_adrese) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t peldošs_p_Statuss = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(peldošs_p_Statuss) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    Stop_NOILGUMS();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 ieejas_punkts_VALUE 때만 Atļaut_VALUE.
    mašīna_reģistrs(IRQ_izplatītājs) = 0;
    mašīna_reģistrs(IRQ_izplatītājs + 0x180) = 0xffffffff;
    mašīna_reģistrs(IRQ_izplatītājs + 0x80) = 0xffffffff;
    mašīna_reģistrs(IRQ_izplatītājs + 0x280) = 1u << 30;
    mašīna_reģistrs(IRQ_izplatītājs + 0x41c) = 0x80808080;
    mašīna_reģistrs(IRQ_izplatītājs + 0x100) = 1u << 30;
    mašīna_reģistrs(IRQ_centrālais_procesors_interfeiss + 4) = 0xff;
    mašīna_reģistrs(IRQ_centrālais_procesors_interfeiss + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 numurs 있다.
    int Drošība = (mašīna_reģistrs(IRQ_izplatītājs + 4) & (1u << 10)) != 0;
    mašīna_reģistrs(IRQ_izplatītājs) = Drošība ? 1 : 3;
    mašīna_reģistrs(IRQ_centrālais_procesors_interfeiss) = Drošība ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t TYPE_joma, mašīna_TYPE; uint32_t versijas_numurs;
    uint64_t ieejas_punkts, programma_galvene_Nobīde, sadaļas_galvene_Nobīde; uint32_t konfigurācija_Background_Intelligent_Transfer_Service;
    uint16_t izpildāms_fails_galvene_mainīt_izmērus, programma_galvene_ievade_mainīt_izmērus, programma_galvene_COUNT, sadaļas_galvene_ievade_mainīt_izmērus, sadaļas_galvene_COUNT, sadaļa_nosaukums_tabula_INDEX;
} 실행파일머리;
typedef struct { uint32_t TYPE_joma, konfigurācija_Background_Intelligent_Transfer_Service; uint64_t Nobīde_VALUE, adrese, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(lietotājs_kadrs) == 272, "exception assembly layout");
static int 포함된범위(uint64_t Nobīde_VALUE, uint64_t Izmērs, uint64_t beigt_zvanu_Nobīde) {
    return Nobīde_VALUE <= beigt_zvanu_Nobīde && Izmērs <= beigt_zvanu_Nobīde - Nobīde_VALUE;
}
static int 부가정보검사(const unsigned char *dati_amats, size_t Izmērs) {
    size_t pašreizējais_amats = 0;
    while (포함된범위(pašreizējais_amats, 12, Izmērs)) {
        uint32_t 낱말들[3]; memcpy(낱말들, dati_amats + pašreizējais_amats, 12); pašreizējais_amats += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(pašreizējais_amats, 이름영역크기, Izmērs) || !포함된범위(pašreizējais_amats + 이름영역크기, 설명크기, Izmērs)) return 0;
        const unsigned char Nosaukums[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Nosaukums) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Nosaukums); 순번++) if (dati_amats[pašreizējais_amats + 순번] != Nosaukums[순번]) 일치 = 0;
        uint32_t versijas_numurs = 0;
        if (일치) memcpy(&versijas_numurs, dati_amats + pašreizējais_amats + 이름영역크기, 4);
        if (일치 && versijas_numurs == 1) return 1;
        pašreizējais_amats += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *dati, size_t Izmērs, int 리눅스방식) {
    if (Izmērs < sizeof(실행파일머리)) return lietotājs_izpildāms_fails_kļūda;
    실행파일머리 izpildāms_fails_galvene; memcpy(&izpildāms_fails_galvene, dati, sizeof(izpildāms_fails_galvene));
    if (izpildāms_fails_galvene.형식식별[0] != 127 || izpildāms_fails_galvene.형식식별[1] != 'E' || izpildāms_fails_galvene.형식식별[2] != 'L' || izpildāms_fails_galvene.형식식별[3] != 'F' ||
        izpildāms_fails_galvene.형식식별[4] != 2 || izpildāms_fails_galvene.형식식별[5] != 1 || izpildāms_fails_galvene.형식식별[6] != 1 || (izpildāms_fails_galvene.형식식별[7] != 0 && (!리눅스방식 || izpildāms_fails_galvene.형식식별[7] != 3)) ||
        izpildāms_fails_galvene.TYPE_joma != 2 || izpildāms_fails_galvene.mašīna_TYPE != 183 || izpildāms_fails_galvene.versijas_numurs != 1 || izpildāms_fails_galvene.konfigurācija_Background_Intelligent_Transfer_Service || izpildāms_fails_galvene.izpildāms_fails_galvene_mainīt_izmērus != sizeof(izpildāms_fails_galvene) ||
        izpildāms_fails_galvene.programma_galvene_ievade_mainīt_izmērus != sizeof(실행파일구획) || !izpildāms_fails_galvene.programma_galvene_COUNT || izpildāms_fails_galvene.programma_galvene_COUNT > 16 ||
        izpildāms_fails_galvene.programma_galvene_Nobīde < sizeof(izpildāms_fails_galvene) || !포함된범위(izpildāms_fails_galvene.programma_galvene_Nobīde, (uint64_t)izpildāms_fails_galvene.programma_galvene_COUNT * sizeof(실행파일구획), Izmērs)) return lietotājs_izpildāms_fails_kļūda;
    uint8_t 사용량[(lietotājs_IMAGE_beigt_zvanu - lietotājs_BASE) / lappuses_izmēri] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < izpildāms_fails_galvene.programma_galvene_COUNT; 순번++) {
        실행파일구획 dati_amats; memcpy(&dati_amats, dati + izpildāms_fails_galvene.programma_galvene_Nobīde + 순번 * sizeof(dati_amats), sizeof(dati_amats));
        if (dati_amats.TYPE_joma == 4) {
            if (!포함된범위(dati_amats.Nobīde_VALUE, dati_amats.파일영역크기, Izmērs)) return lietotājs_izpildāms_fails_kļūda;
            if (부가정보검사(dati + dati_amats.Nobīde_VALUE, dati_amats.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (dati_amats.TYPE_joma == 0 || dati_amats.TYPE_joma == 6 || (dati_amats.TYPE_joma == 0x6474e551 && !(dati_amats.konfigurācija_Background_Intelligent_Transfer_Service & 1))) continue;
        if (dati_amats.TYPE_joma != 1) return lietotājs_izpildāms_fails_kļūda; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!dati_amats.기억영역크기) continue;
        if (dati_amats.konfigurācija_Background_Intelligent_Transfer_Service & ~7u || !(dati_amats.konfigurācija_Background_Intelligent_Transfer_Service & 4) || (dati_amats.konfigurācija_Background_Intelligent_Transfer_Service & 3) == 3 || dati_amats.파일영역크기 > dati_amats.기억영역크기 ||
            (dati_amats.파일영역크기 && !포함된범위(dati_amats.Nobīde_VALUE, dati_amats.파일영역크기, Izmērs)) || dati_amats.adrese < lietotājs_BASE ||
            !포함된범위(dati_amats.adrese, dati_amats.기억영역크기, lietotājs_IMAGE_beigt_zvanu) ||
            (!리눅스방식 && ((dati_amats.adrese & (lappuses_izmēri - 1)) || (dati_amats.Nobīde_VALUE & (lappuses_izmēri - 1)) || dati_amats.맞춤 != lappuses_izmēri)) ||
            (리눅스방식 && (((dati_amats.adrese ^ dati_amats.Nobīde_VALUE) & (lappuses_izmēri - 1)) || !dati_amats.맞춤 ||
                (dati_amats.맞춤 & (dati_amats.맞춤 - 1)) || dati_amats.맞춤 > 0x200000 || ((dati_amats.adrese ^ dati_amats.Nobīde_VALUE) & (dati_amats.맞춤 - 1))))) return lietotājs_izpildāms_fails_kļūda;
        unsigned 첫항목 = (dati_amats.adrese - lietotājs_BASE) / lappuses_izmēri;
        unsigned ievade_COUNT = ((dati_amats.adrese & (lappuses_izmēri - 1)) + dati_amats.기억영역크기 + lappuses_izmēri - 1) / lappuses_izmēri;
        for (unsigned lapa_VALUE = 첫항목; lapa_VALUE < 첫항목 + ievade_COUNT; lapa_VALUE++) {
            if (사용량[lapa_VALUE]) return lietotājs_izpildāms_fails_kļūda;
            사용량[lapa_VALUE] = 1;
        }
        if ((dati_amats.konfigurācija_Background_Intelligent_Transfer_Service & 1) && izpildāms_fails_galvene.ieejas_punkts >= dati_amats.adrese && izpildāms_fails_galvene.ieejas_punkts < dati_amats.adrese + dati_amats.파일영역크기 && !(izpildāms_fails_galvene.ieejas_punkts & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : lietotājs_izpildāms_fails_kļūda;
}
int 사용자실행파일검사(const unsigned char *dati, size_t Izmērs) { return 실행파일검사(dati, Izmērs, 0); }
static void lappuses_izkārtojums(uintptr_t adrese, uint64_t konfigurācija_Background_Intelligent_Transfer_Service, unsigned atļaujas) {
    unsigned LOOKUP_INDEX = (adrese - lietotājs_BASE) / lappuses_izmēri;
    lapa_Saraksts[LOOKUP_INDEX] = adrese | konfigurācija_Background_Intelligent_Transfer_Service;
    Atļaujas_Saraksts[LOOKUP_INDEX] = atļaujas;
}
static int lietotājs_diapazons(uintptr_t adrese, size_t ievade_COUNT, int 쓰는중) {
    if (adrese < lietotājs_BASE || !포함된범위(adrese, ievade_COUNT, lietotājs_beigt_zvanu)) return 0;
    if (!ievade_COUNT) return 1;
    unsigned 첫항목 = (adrese - lietotājs_BASE) / lappuses_izmēri, 마지막 = (adrese + ievade_COUNT - 1 - lietotājs_BASE) / lappuses_izmēri;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(Atļaujas_Saraksts[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int kopēt_ceļš(uintptr_t adrese, char *CEĻŠ) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!lietotājs_diapazons(adrese, 1, 0)) return -14;
        CEĻŠ[순번] = *(const char *)adrese++;
        if (!CEĻŠ[순번]) return 0;
    }
    return -36;
}
static intptr_t kodols_mērs(intptr_t mērs) { return mērs < 0 ? -kļūdas_numurs : mērs; }
static int 대응파일기술자(uint64_t Fails_turis) { return Fails_turis >= 3 && Fails_turis < 19 ? Fails_Saraksts[Fails_turis - 3] : -1; }
static int 통신끝점소유(uint64_t Fails_turis) { return Fails_turis >= 32 && Fails_turis < 56 && 통신끝점들[Fails_turis - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t 길이, struct pk_sockaddr_in *adrese) {
    if (길이 != sizeof(*adrese)) return -22;
    if (!lietotājs_diapazons(가리킴값, 길이, 0)) return -14;
    memcpy(adrese, (const void *)가리킴값, sizeof(*adrese));
    return adrese->sin_family == AF_INET ? 0 : -97;
}
static int adrese_ražojums_čeks(uintptr_t 가리킴값, uintptr_t 길이포인터, pk_socklen_t *buferis_noslodze) {
    if (!lietotājs_diapazons(길이포인터, sizeof(*buferis_noslodze), 1)) return -14;
    memcpy(buferis_noslodze, (const void *)길이포인터, sizeof(*buferis_noslodze));
    if (*buferis_noslodze > sizeof(struct pk_sockaddr_in)) *buferis_noslodze = sizeof(struct pk_sockaddr_in);
    if (*buferis_noslodze && !lietotājs_diapazons(가리킴값, *buferis_noslodze, 1)) return -14;
    return 0;
}
static void adrese_ražojums(uintptr_t 가리킴값, uintptr_t 길이포인터, pk_socklen_t buferis_noslodze, int adrese, int porta_numurs) {
    struct pk_sockaddr_in VALUE; memset(&VALUE, 0, sizeof(VALUE));
    VALUE.sin_family = AF_INET; VALUE.sin_port = pk_htons(porta_numurs); VALUE.sin_addr.s_addr = pk_htonl(adrese);
    if (buferis_noslodze) memcpy((void *)가리킴값, &VALUE, buferis_noslodze);
    pk_socklen_t 길이 = sizeof(VALUE); memcpy((void *)길이포인터, &길이, sizeof(길이));
}
extern uintptr_t Panelis_Kanāls(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(lietotājs_kadrs *Fails_ievade) {
    uintptr_t 첫째값 = Fails_ievade->reģistrs_dati[0], SECOND_VALUE = Fails_ievade->reģistrs_dati[1], koda_punkts = Fails_ievade->reģistrs_dati[2];
    char CEĻŠ[65];
    int Fails_turis, mērs;
    switch (Fails_ievade->reģistrs_dati[8]) {
    case 0: return 1; // savs ABI 버전
    case 1: // write: rādītājs 전체를 검사한 ATPAKAĻ_VALUE Izvade/Fails mainīt_VALUE
        if (koda_punkts > 65536) return -22;
        if (!lietotājs_diapazons(SECOND_VALUE, koda_punkts, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t Sākt_ražojums=Pulkstenis_VALUE();
            for (size_t 순번 = 0; 순번 < koda_punkts; 순번++) Panelis_Kanāls(첫째값, ((const unsigned char *)SECOND_VALUE)[순번]);
            /* 큰 tty를 그린 kodols_VALUE 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(대화형){
                izpildes_termiņš_TIME+=Pulkstenis_VALUE()-Sākt_ražojums;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(izpildes_termiņš_TIME) : "memory");
            }
            return koda_punkts;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t krājums_COUNT=koda_punkts>512?512:koda_punkts;for(size_t 순번=0;순번<krājums_COUNT;순번++)자바전문넣기(순번,((const unsigned char *)SECOND_VALUE)[순번]);return 자바흐름쓰기(첫째값,krājums_COUNT);
        }
        Fails_turis = 대응파일기술자(첫째값); if (Fails_turis < 0) return -9;
        return kodols_mērs(pk_write(Fails_turis, (const void *)SECOND_VALUE, koda_punkts));
    case 2:
        if (koda_punkts > 65536) return -22;
        if (!lietotājs_diapazons(SECOND_VALUE, koda_punkts, 1)) return -14;
        if (첫째값 == 0) {
            size_t krājums_COUNT = 0;
            while (krājums_COUNT < koda_punkts) {
                int rakstzīme_VALUE = (int32_t)보드글자읽기(); if (rakstzīme_VALUE == -2) return krājums_COUNT; if (rakstzīme_VALUE < 0) break;
                ((unsigned char *)SECOND_VALUE)[krājums_COUNT++] = rakstzīme_VALUE;
            }
            return krājums_COUNT ? (intptr_t)krājums_COUNT : (koda_punkts ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            mērs=자바흐름읽기(첫째값,koda_punkts>512?512:koda_punkts);if(mērs>0)for(int 순번=0;순번<mērs;순번++)((unsigned char *)SECOND_VALUE)[순번]=자바전문얻기(순번);return mērs;
        }
        Fails_turis = 대응파일기술자(첫째값); if (Fails_turis < 0) return -9;
        return kodols_mērs(pk_read(Fails_turis, (void *)SECOND_VALUE, koda_punkts));
    case 3:
        mērs = kopēt_ceļš(첫째값, CEĻŠ); if (mērs) return mērs;
        if (SECOND_VALUE > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (Fails_Saraksts[순번] < 0) {
            Fails_turis = pk_open(CEĻŠ, (int)SECOND_VALUE, 0600);
            if (Fails_turis < 0) return -kļūdas_numurs;
            Fails_Saraksts[순번] = Fails_turis; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { mērs = 통신끝점닫기(첫째값); if (!mērs) 통신끝점들[첫째값 - 32] = 0; return mērs; }
        Fails_turis = 대응파일기술자(첫째값); if (Fails_turis < 0) return -9;
        mērs = pk_close(Fails_turis); if (!mērs) Fails_Saraksts[첫째값 - 3] = -1;
        return kodols_mērs(mērs);
    case 5:
        Fails_turis = 대응파일기술자(첫째값); if (Fails_turis < 0) return -9;
        if (koda_punkts > 2) return -22;
        return kodols_mērs(pk_lseek(Fails_turis, (int64_t)SECOND_VALUE, koda_punkts));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 lietotājs RW/NX kaudze_VALUE, 새로 노출되는 페이지는 0으로 초기화
        if (!첫째값) return kaudze_beigt_zvanu;
        if (첫째값 < lietotājs_IMAGE_beigt_zvanu || 첫째값 > lietotājs_kaudze_beigt_zvanu) return -12;
        uintptr_t 이전쪽들 = (kaudze_beigt_zvanu + lappuses_izmēri - 1) & ~(lappuses_izmēri - 1);
        uintptr_t 새쪽들 = (첫째값 + lappuses_izmēri - 1) & ~(lappuses_izmēri - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t dati_amats = 이전쪽들; dati_amats < 새쪽들; dati_amats += lappuses_izmēri) lappuses_izkārtojums(dati_amats, kodols_lapa, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t dati_amats = 이전쪽들; dati_amats < 새쪽들; dati_amats += lappuses_izmēri) lappuses_izkārtojums(dati_amats, 사용자읽고쓰기, 3);
        } else {
            for (uintptr_t dati_amats = 새쪽들; dati_amats < 이전쪽들; dati_amats += lappuses_izmēri) {
                lapa_Saraksts[(dati_amats - lietotājs_BASE) / lappuses_izmēri] = 0; Atļaujas_Saraksts[(dati_amats - lietotājs_BASE) / lappuses_izmēri] = 0;
            }
        }
        kaudze_beigt_zvanu = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        Fails_turis = 대응파일기술자(첫째값); return Fails_turis < 0 ? -9 : kodols_mērs(pk_size(Fails_turis));
    case 10:
        Fails_turis = 대응파일기술자(첫째값); return Fails_turis < 0 ? -9 : kodols_mērs(pk_ftruncate(Fails_turis, (int64_t)SECOND_VALUE));
    case 11:
        mērs = kopēt_ceļš(첫째값, CEĻŠ); return mērs ? mērs : kodols_mērs(pk_unlink(CEĻŠ));
    case 12:
        Fails_turis = 대응파일기술자(첫째값); return Fails_turis < 0 ? -9 : kodols_mērs(pk_fsync(Fails_turis));
    case 13: { // 그래픽 기초 API: lietotājs 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = Fails_ievade->reģistrs_dati[3], 높이값 = Fails_ievade->reģistrs_dati[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SECOND_VALUE > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - SECOND_VALUE) return -22;
        for (uintptr_t 세로좌표 = SECOND_VALUE; 세로좌표 < SECOND_VALUE + 높이값; 세로좌표++) for (uintptr_t x_koordināta = 첫째값; x_koordināta < 첫째값 + 너비값; x_koordināta++) Panelis_attēla_elements(x_koordināta, 세로좌표, koda_punkts);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=krājums_COUNT; args(index,buffer,capacity)=UTF-8 길이
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (koda_punkts <= 전달인수길이[첫째값]) return -36;
        if (!lietotājs_diapazons(SECOND_VALUE, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SECOND_VALUE, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;대화형=1;return Panelis_Terminālis(13);}
        if(첫째값==2){대화형=0;return 0;}
        if(첫째값==3)return Panelis_Terminālis(13);
        if(첫째값!=1||!대화형)return -22;
        mērs=(int32_t)보드글자읽기();
        if(mērs==-4096)return mērs;
        Sākt_NOILGUMS();return mērs<0?-11:mērs;
    case 17: { // 유한한 협력 pagaidi_VALUE: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t beigt_zvanu_TIME = Pulkstenis_VALUE() + FREQUENCY * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Pulkstenis_VALUE() < beigt_zvanu_TIME);
        Sākt_NOILGUMS(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 vecākobjekts_VALUE·빈 폴더를 검사한다.
        if (SECOND_VALUE > 2) return -22;
        mērs = kopēt_ceļš(첫째값, CEĻŠ); if (mērs) return mērs;
        unsigned 길이 = 0; while (CEĻŠ[길이]) 길이++;
        mērs = 자바경로시작(길이); if (mērs < 0) return mērs;
        for (unsigned 순번 = 0; 순번 < 길이; 순번++) 자바경로바이트(순번, (unsigned char)CEĻŠ[순번]);
        return SECOND_VALUE == 0 ? 자바항목종류() : SECOND_VALUE == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int rakstzīme_VALUE=(int32_t)보드글자읽기();if(rakstzīme_VALUE==-4096)return rakstzīme_VALUE;if(rakstzīme_VALUE>=0)화면누름(īpašnieks_objekts,rakstzīme_VALUE);Sākt_NOILGUMS();}
        if(첫째값==3&&koda_punkts){if(!자바셸대화형())return -95;대화형=1;Panelis_Terminālis(300);}
        return 화면호출(īpašnieks_objekts,첫째값,SECOND_VALUE,koda_punkts,Fails_ievade->reģistrs_dati[3],Fails_ievade->reģistrs_dati[4],Fails_ievade->reģistrs_dati[5]);
    case 21:
        if(koda_punkts>127)return -22;if(!lietotājs_diapazons(SECOND_VALUE,koda_punkts*sizeof(uint32_t),0))return -14;
        return 화면글(īpašnieks_objekts,첫째값,(const uint32_t *)SECOND_VALUE,koda_punkts);
    case 22: // 화면 Izmērs vaicāt_VALUE: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SECOND_VALUE==SOCK_STREAM&&(koda_punkts==0||koda_punkts==6))mērs=자바흐름만들기();
        else if(SECOND_VALUE==SOCK_DGRAM&&(koda_punkts==0||koda_punkts==IPPROTO_UDP))mērs=자바전문만들기(첫째값,SECOND_VALUE,koda_punkts);
        else return -93;
        if (mērs >= 32 && mērs < 56) 통신끝점들[mērs - 32] = 1;
        return mērs;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in adrese;
        mērs = 주소입력(SECOND_VALUE, koda_punkts, &adrese); if (mērs) return mērs;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(adrese.sin_addr.s_addr),pk_htons(adrese.sin_port)):자바전문묶기(첫째값, pk_htonl(adrese.sin_addr.s_addr), pk_htons(adrese.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Fails_ievade->reģistrs_dati[3]) return -95;
        if (koda_punkts > 512) return -90;
        if (koda_punkts && !lietotājs_diapazons(SECOND_VALUE, koda_punkts, 0)) return -14;
        struct pk_sockaddr_in adrese;
        mērs = 주소입력(Fails_ievade->reģistrs_dati[4], Fails_ievade->reģistrs_dati[5], &adrese); if (mērs) return mērs;
        for (unsigned 순번 = 0; 순번 < koda_punkts; 순번++) 자바전문넣기(순번, ((const unsigned char *)SECOND_VALUE)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(adrese.sin_addr.s_addr), pk_htons(adrese.sin_port), koda_punkts);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Fails_ievade->reģistrs_dati[3]) return -95;
        if (koda_punkts > 512) return -90;
        if (koda_punkts && !lietotājs_diapazons(SECOND_VALUE, koda_punkts, 1)) return -14;
        pk_socklen_t buferis_noslodze = 0;
        if (Fails_ievade->reģistrs_dati[4]) { mērs = adrese_ražojums_čeks(Fails_ievade->reģistrs_dati[4], Fails_ievade->reģistrs_dati[5], &buferis_noslodze); if (mērs) return mērs; }
        mērs = 자바전문받기(첫째값, koda_punkts); if (mērs < 0) return mērs;
        for (int 순번 = 0; 순번 < mērs; 순번++) ((unsigned char *)SECOND_VALUE)[순번] = 자바전문얻기(순번);
        if (Fails_ievade->reģistrs_dati[4]) adrese_ražojums(Fails_ievade->reģistrs_dati[4], Fails_ievade->reģistrs_dati[5], buferis_noslodze, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return mērs;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t buferis_noslodze;
        mērs = adrese_ražojums_čeks(SECOND_VALUE, koda_punkts, &buferis_noslodze); if (mērs) return mērs;
        adrese_ražojums(SECOND_VALUE,koda_punkts,buferis_noslodze,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in adrese;
        mērs=주소입력(SECOND_VALUE,koda_punkts,&adrese);if(mērs)return mērs;
        return 자바흐름연결(첫째값,pk_htonl(adrese.sin_addr.s_addr),pk_htons(adrese.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,SECOND_VALUE):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(SECOND_VALUE||koda_punkts)return -95;mērs=자바흐름연결받기(첫째값);if(mērs>=40&&mērs<56)통신끝점들[mērs-32]=1;return mērs;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(lietotājs_kadrs *Fails_ievade) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(Fails_ievade) : 자체체계호출(Fails_ievade);
}
static void atdot_kodols(lietotājs_kadrs *Fails_ievade, int mērs) {
    Stop_NOILGUMS();
    Fails_ievade->reģistrs_dati[0] = (uint64_t)(int64_t)mērs;
    Fails_ievade->komanda_amats = (uintptr_t)lietotājs_atdot;
    Fails_ievade->Statuss_CODE = 0x3c5; // EL1h, DAIF masked
}
int lietotāja_izņēmums(lietotājs_kadrs *Fails_ievade, unsigned INTERCEPT) {
    if (!Aktīvs || (Fails_ievade->Statuss_CODE & 15) != 0) return 0;
    if (INTERCEPT) {
        uint32_t apliecinājums_VALUE = mašīna_reģistrs(IRQ_centrālais_procesors_interfeiss + 0xc), identifikators_VALUE = apliecinājums_VALUE & 1023;
        if (identifikators_VALUE == 30) { atdot_kodols(Fails_ievade, lietotājs_NOILGUMS); mašīna_reģistrs(IRQ_centrālais_procesors_interfeiss + 0x10) = apliecinājums_VALUE; return 1; }
        if (identifikators_VALUE < 1020) mašīna_reģistrs(IRQ_centrālais_procesors_interfeiss + 0x10) = apliecinājums_VALUE;
        return 1;
    }
    uint64_t izņēmums_Statuss; __asm__ volatile("mrs %0, esr_el1" : "=r"(izņēmums_Statuss));
    if (Pulkstenis_VALUE() >= izpildes_termiņš_TIME) { atdot_kodols(Fails_ievade, lietotājs_NOILGUMS); return 1; }
    unsigned izņēmums_joma = izņēmums_Statuss >> 26;
    if (izņēmums_joma == 0x15 && (izņēmums_Statuss & 0xffff) == 0) {
        if (리눅스규약 ? Fails_ievade->reģistrs_dati[8] == 93 || Fails_ievade->reģistrs_dati[8] == 94 : Fails_ievade->reģistrs_dati[8] == 6) atdot_kodols(Fails_ievade, (int)(Fails_ievade->reģistrs_dati[0] & 255));
        else {
            intptr_t mērs=체계호출(Fails_ievade);
            if(mērs==-4096&&대화형){
                저장값[īpašnieks_objekts].실행틀=*Fails_ievade;저장값[īpašnieks_objekts].실행틀.komanda_amats-=4;
                사용자실수보관(저장값[īpašnieks_objekts].peldošs_p_Statuss);atdot_kodols(Fails_ievade,사용자중단됨);
            }else Fails_ievade->reģistrs_dati[0]=(uint64_t)mērs;
        }
    } else atdot_kodols(Fails_ievade, izņēmums_joma == 0x24 ? lietotājs_dati_kļūda : izņēmums_joma == 0x20 ? 사용자실행오류 : 사용자잘못된명령);
    return 1;
}

// 생성된 const ELF Grupa_VALUE: 실행은 반드시 programma_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *dati; size_t Izmērs; unsigned 전달값; } programma;
#include "programs.h"
static void *ēnkopija(unsigned pozīcijas_indekss){return (void *)(0x04000000ul+pozīcijas_indekss*(lietotājs_beigt_zvanu-lietotājs_BASE));}
static int beigas_programma(int mērs){
    사용자누적시각[īpašnieks_objekts]+=(uint32_t)보드밀리초()-사용자실행시각[īpašnieks_objekts];
    Stop_NOILGUMS();Aktīvs=0;
    if(mērs==사용자중단됨){
        저장된작업 *virkne_dati=&저장값[īpašnieks_objekts];virkne_dati->멈춤상태=1;virkne_dati->대화형=대화형;virkne_dati->리눅스규약=리눅스규약;virkne_dati->kaudze_Krātuve=kaudze_beigt_zvanu;virkne_dati->인수개수=전달인수개수;
        memcpy(virkne_dati->Atļaujas_Saraksts,Atļaujas_Saraksts,sizeof(Atļaujas_Saraksts));memcpy(virkne_dati->Fails_Saraksts,Fails_Saraksts,sizeof(Fails_Saraksts));memcpy(virkne_dati->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(virkne_dati->arg_ARRAY,전달인수,sizeof(전달인수));memcpy(virkne_dati->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<lietotājs_lapa_COUNT;순번++)if(Atļaujas_Saraksts[순번])memcpy((unsigned char *)ēnkopija(īpašnieks_objekts)+순번*lappuses_izmēri,(void *)(lietotājs_BASE+순번*lappuses_izmēri),lappuses_izmēri);
    }else{
        저장값[īpašnieks_objekts].멈춤상태=0;화면초기화(īpašnieks_objekts);
        for(unsigned 순번=0;순번<16;순번++)if(Fails_Saraksts[순번]>=0)pk_close(Fails_Saraksts[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<lietotājs_lapa_COUNT;순번++){lapa_Saraksts[순번]=0;Atļaujas_Saraksts[순번]=0;}변환표맞추기();return mērs;
}
uintptr_t Panelis_lietotāja_vadīkla(uintptr_t Darbība){
    unsigned pozīcijas_indekss=Darbība&15;if(pozīcijas_indekss>=4||Aktīvs)return (uint32_t)-22;
    저장된작업 *virkne_dati=&저장값[pozīcijas_indekss];
    if(Darbība>=32){if(virkne_dati->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(virkne_dati->Fails_Saraksts[순번]>=0)pk_close(virkne_dati->Fails_Saraksts[순번]);for(unsigned 순번=0;순번<24;순번++)if(virkne_dati->통신끝점들[순번])통신끝점닫기(순번+32);}virkne_dati->멈춤상태=0;화면초기화(pozīcijas_indekss);return 0;}
    if(Darbība>=16)return virkne_dati->멈춤상태;
    if(!virkne_dati->멈춤상태)return (uint32_t)-22;
    īpašnieks_objekts=pozīcijas_indekss;대화형=virkne_dati->대화형;리눅스규약=virkne_dati->리눅스규약;kaudze_beigt_zvanu=virkne_dati->kaudze_Krātuve;전달인수개수=virkne_dati->인수개수;
    memcpy(Fails_Saraksts,virkne_dati->Fails_Saraksts,sizeof(Fails_Saraksts));memcpy(통신끝점들,virkne_dati->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,virkne_dati->arg_ARRAY,sizeof(전달인수));memcpy(전달인수길이,virkne_dati->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<lietotājs_lapa_COUNT;순번++)lapa_Saraksts[순번]=(lietotājs_BASE+순번*lappuses_izmēri)|kodols_lapa;변환표맞추기();
    memset((void *)lietotājs_BASE,0,lietotājs_beigt_zvanu-lietotājs_BASE);
    for(unsigned 순번=0;순번<lietotājs_lapa_COUNT;순번++)if(virkne_dati->Atļaujas_Saraksts[순번])memcpy((void *)(lietotājs_BASE+순번*lappuses_izmēri),(unsigned char *)ēnkopija(pozīcijas_indekss)+순번*lappuses_izmēri,lappuses_izmēri);
    memcpy(Atļaujas_Saraksts,virkne_dati->Atļaujas_Saraksts,sizeof(Atļaujas_Saraksts));
    for(unsigned 순번=0;순번<lietotājs_lapa_COUNT;순번++){unsigned dati_amats=Atļaujas_Saraksts[순번];lapa_Saraksts[순번]=dati_amats?(lietotājs_BASE+순번*lappuses_izmēri)|(dati_amats==3?사용자읽고쓰기:dati_amats==5?사용자읽고실행:lietotājs_tikai_lasāms):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");Aktīvs=1;virkne_dati->멈춤상태=0;Sākt_NOILGUMS();
    사용자실행시각[īpašnieks_objekts]=보드밀리초();
    return (uint32_t)beigas_programma(lietotājs_CV(&virkne_dati->실행틀,virkne_dati->peldošs_p_Statuss));
}
static int virkne_programma(const unsigned char *dati, size_t Izmērs, unsigned 전달값, int 리눅스방식, const char *Nosaukums) {
    if (Aktīvs) return -16;
    īpašnieks_objekts=Panelis_Terminālis(11);if(īpašnieks_objekts<0||īpašnieks_objekts>3||저장값[īpašnieks_objekts].멈춤상태)return -16;대화형=0;
    int 유효함 = 실행파일검사(dati, Izmērs, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned nosaukums_INDEX=0;
    while (*Nosaukums && nosaukums_INDEX<31) lietotājs_komanda_nosaukums[īpašnieks_objekts][nosaukums_INDEX++]=(unsigned char)*Nosaukums++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (nosaukums_INDEX) lietotājs_komanda_nosaukums[īpašnieks_objekts][nosaukums_INDEX++]=' ';
        for (unsigned pozīcijas_indekss=0; pozīcijas_indekss<전달인수길이[0]; pozīcijas_indekss++) lietotājs_komanda_nosaukums[īpašnieks_objekts][nosaukums_INDEX++]=전달인수[0][pozīcijas_indekss];
    }
    lietotājs_komanda_nosaukums[īpašnieks_objekts][nosaukums_INDEX]=0; lietotāja_numurs[īpašnieks_objekts]=Tālāk_lietotāja_numurs++;
    if (Tālāk_lietotāja_numurs>0x7fffffffu) Tālāk_lietotāja_numurs=10;
    lietotājs_Sākt_TIME[īpašnieks_objekts]=보드밀리초(); 사용자누적시각[īpašnieks_objekts]=0;
    for (unsigned 순번 = 0; 순번 < lietotājs_lapa_COUNT; 순번++) lapa_Saraksts[순번] = (lietotājs_BASE + 순번 * lappuses_izmēri) | kodols_lapa;
    변환표맞추기();
    memset((void *)lietotājs_BASE, 0, lietotājs_beigt_zvanu - lietotājs_BASE);
    memset(Atļaujas_Saraksts, 0, sizeof(Atļaujas_Saraksts));
    실행파일머리 izpildāms_fails_galvene; memcpy(&izpildāms_fails_galvene, dati, sizeof(izpildāms_fails_galvene));
    for (unsigned 순번 = 0; 순번 < izpildāms_fails_galvene.programma_galvene_COUNT; 순번++) {
        실행파일구획 dati_amats; memcpy(&dati_amats, dati + izpildāms_fails_galvene.programma_galvene_Nobīde + 순번 * sizeof(dati_amats), sizeof(dati_amats));
        if (dati_amats.TYPE_joma != 1 || !dati_amats.기억영역크기) continue;
        if (dati_amats.파일영역크기) memcpy((void *)(uintptr_t)dati_amats.adrese, dati + dati_amats.Nobīde_VALUE, dati_amats.파일영역크기);
        for (uintptr_t pašreizējais_amats = dati_amats.adrese & ~(lappuses_izmēri - 1); pašreizējais_amats < dati_amats.adrese + dati_amats.기억영역크기; pašreizējais_amats += lappuses_izmēri) {
            Atļaujas_Saraksts[(pašreizējais_amats - lietotājs_BASE) / lappuses_izmēri] = (dati_amats.konfigurācija_Background_Intelligent_Transfer_Service & 2) ? 3 : ((dati_amats.konfigurācija_Background_Intelligent_Transfer_Service & 1) ? 5 : 1);
        }
    }
    for (uintptr_t pašreizējais_amats = lietotājs_kopa_adrese; pašreizējais_amats < lietotājs_beigt_zvanu; pašreizējais_amats += lappuses_izmēri) Atļaujas_Saraksts[(pašreizējais_amats - lietotājs_BASE) / lappuses_izmēri] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(izpildāms_fails_galvene.ieejas_punkts) : lietotājs_beigt_zvanu;
    for (unsigned 순번 = 0; 순번 < lietotājs_lapa_COUNT; 순번++) {
        unsigned atļaujas = Atļaujas_Saraksts[순번];
        lapa_Saraksts[순번] = atļaujas ? (lietotājs_BASE + 순번 * lappuses_izmēri) | (atļaujas == 3 ? 사용자읽고쓰기 : atļaujas == 5 ? 사용자읽고실행 : lietotājs_tikai_lasāms) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) Fails_Saraksts[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    kaudze_beigt_zvanu = lietotājs_IMAGE_beigt_zvanu;
    Aktīvs = 1; Sākt_NOILGUMS();
    사용자실행시각[īpašnieks_objekts]=보드밀리초();
    int mērs = lietotājs_ievadīt(izpildāms_fails_galvene.ieejas_punkts, 초기쌓임공간, 전달값);
    return beigas_programma(mērs);
}
uintptr_t Panelis_lietotājs_virkne(uintptr_t LOOKUP_INDEX) {
    if (LOOKUP_INDEX >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Nosaukums=LOOKUP_INDEX==10?"javac":LOOKUP_INDEX==11?"java":LOOKUP_INDEX==12?"python":LOOKUP_INDEX==13?"vi":LOOKUP_INDEX==14?"jar":LOOKUP_INDEX==15?"cc":LOOKUP_INDEX==16?"jaot":"ELF";
    return (uint32_t)virkne_programma(실행항목들[LOOKUP_INDEX].dati, 실행항목들[LOOKUP_INDEX].Izmērs, 실행항목들[LOOKUP_INDEX].전달값, 0, Nosaukums);
}
static uintptr_t Izpildīt_Fails(int 리눅스방식) {
    static unsigned char IMAGE[16384];
    if (Aktīvs || !전달인수개수) return (uint32_t)-22;
    int Fails_turis = pk_open((const char *)전달인수[0], tikai_lasāms_VALUE, 0);
    if (Fails_turis < 0) return (uint32_t)-kļūdas_numurs;
    int Izmērs = pk_size(Fails_turis);
    if (Izmērs < 0 || (unsigned)Izmērs > sizeof(IMAGE)) { pk_close(Fails_turis); return (uint32_t)-27; }
    int RECEIVED_COUNT = pk_read(Fails_turis, IMAGE, Izmērs); pk_close(Fails_turis);
    if (RECEIVED_COUNT != Izmērs) return (uint32_t)-5;
    return (uint32_t)virkne_programma(IMAGE, Izmērs, 0, 리눅스방식, "");
}
uintptr_t Panelis_lietotājs_Fails(void) { return Izpildīt_Fails(0); }
uintptr_t 보드사용자리눅스파일(void) { return Izpildīt_Fails(1); }
uintptr_t Panelis_lietotājs_validēt(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].dati, 잘못된실행항목들[순번].Izmērs) != lietotājs_izpildāms_fails_kļūda) return 순번 + 1;
    return 0;
}
