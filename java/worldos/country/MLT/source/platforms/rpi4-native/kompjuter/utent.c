#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 eżegwixxa_kmand kompjuter saff_VALUE. fajl data/정책은 기존 AOT Java 커널에 위임한다.
#include "utent.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../netwerk_Munzell/netwerk_Munzell.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define kompjuter_i_rreġistra(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_distributur 0xff841000ul
#define IRQ_CPU_interface 0xff842000ul
#define daqs_tal_paġna 4096ul
#define 접근표시 (1ul << 10)
#define 권한실행금지 (1ul << 53)
#define 사용자실행금지 (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | 접근표시)
#define kernel_paġna (3ul | 보통기억 | 권한실행금지 | 사용자실행금지)
#define utent_qari_kitba (3ul | 보통기억 | (1ul << 6) | 권한실행금지 | 사용자실행금지)
#define utent_qari_biss (3ul | 보통기억 | (3ul << 6) | 권한실행금지 | 사용자실행금지)
#define 사용자읽고실행 (3ul | 보통기억 | (3ul << 6) | 권한실행금지)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t bord_pel(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t bord_Terminal(uintptr_t);
extern int Terminal_pendenti(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int utent_CV(utent_frejm *,void *);
extern void 사용자실수보관(void *);
extern int utent_daħħal(uintptr_t entrata_punt, uintptr_t Munzell_Ħażna, uintptr_t 전달값);
extern void 사용자복귀(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t għerq_ADDRESS[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t paġna_Lista[utent_paġna_COUNT] __attribute__((aligned(4096)));
static uint8_t permessi_Lista[utent_paġna_COUNT];
static int attiv, fajl_Lista[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned fajl_handle){return fajl_handle<40?자바전문닫기(fajl_handle):자바흐름닫기(fajl_handle);}
static uint64_t FREQUENCY, 마감시각;
static uintptr_t 동적기억끝;
// kernel_VALUE 셸이 준비한 UTF-8 인수. EL0에는 kkopja_VALUE 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,interattiv,리눅스규약,fajl_Lista[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char argument_ARRAY[8][256],permessi_Lista[utent_paġna_COUNT];
    uintptr_t 동적기억공간; utent_frejm 실행틀;
    unsigned char 실수저장상태[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int propjetarju_oġġett,interattiv;
static uint32_t numru_tal_utent[4], utent_Bidu_TIME[4], 사용자누적시각[4], 사용자실행시각[4], Li_Jmiss_numru_tal_utent=10;
static unsigned char utent_kmand_isem[4][288];
uint32_t 사용자상태읽기(unsigned entrata_VALUE, unsigned INDEX) {
    unsigned pożizzjoni_INDEX=INDEX&3;
    int stat_VALUE=(attiv && propjetarju_oġġett==(int)pożizzjoni_INDEX) ? 1 : 저장값[pożizzjoni_INDEX].멈춤상태 ? 2 : 0;
    if (entrata_VALUE==0) return stat_VALUE;
    if (!stat_VALUE) return 0;
    if (entrata_VALUE==1) return numru_tal_utent[pożizzjoni_INDEX];
    if (entrata_VALUE==2) {
        unsigned char *쪽들=stat_VALUE==1?permessi_Lista:저장값[pożizzjoni_INDEX].permessi_Lista;
        unsigned paġna_COUNT=0; for (unsigned 순번=0; 순번<utent_paġna_COUNT; 순번++) if(쪽들[순번]) paġna_COUNT++;
        return paġna_COUNT*4;
    }
    if (entrata_VALUE==3) return (uint32_t)보드밀리초()-utent_Bidu_TIME[pożizzjoni_INDEX];
    if (entrata_VALUE==4) return 사용자누적시각[pożizzjoni_INDEX]+(stat_VALUE==1?(uint32_t)보드밀리초()-사용자실행시각[pożizzjoni_INDEX]:0);
    if (entrata_VALUE==5) return INDEX/4<sizeof(utent_kmand_isem[0])?utent_kmand_isem[pożizzjoni_INDEX][INDEX/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t entrata_COUNT) {
    if (attiv || entrata_COUNT > 8) return (uint32_t)-22;
    전달인수개수 = entrata_COUNT;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t LOOKUP_INDEX, uintptr_t 현재위치, uintptr_t byte_data) {
    if (attiv || LOOKUP_INDEX >= 전달인수개수 || 현재위치 >= 255 || 현재위치 != 전달인수길이[LOOKUP_INDEX] || !byte_data || byte_data > 255)
        return (uint32_t)-22;
    전달인수[LOOKUP_INDEX][현재위치] = byte_data;
    전달인수길이[LOOKUP_INDEX] = 현재위치 + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Arloġġ_VALUE(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void waqqaf_TIMEOUT(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    kompjuter_i_rreġistra(IRQ_distributur + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void Bidu_TIMEOUT(void) {
    uint64_t 간격 = FREQUENCY * 2, attiva = 1;
    마감시각 = Arloġġ_VALUE() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(attiva) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned data_imblokka = 0; data_imblokka < 4; data_imblokka++) {
        għerq_ADDRESS[data_imblokka] = (uintptr_t)가운데[data_imblokka] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t ADDRESS = ((uintptr_t)data_imblokka << 30) | ((uintptr_t)순번 << 21);
            가운데[data_imblokka][순번] = ADDRESS | 1 | 접근표시 | 사용자실행금지;
            if (ADDRESS >= 0xfc000000ul) 가운데[data_imblokka][순번] |= 권한실행금지; // Device-nGnRnE
            else 가운데[data_imblokka][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned SECOND_VALUE = 0; SECOND_VALUE < utent_paġna_COUNT / 512; SECOND_VALUE++)
        가운데[0][(utent_BASE >> 21) + SECOND_VALUE] = (uintptr_t)(paġna_Lista + SECOND_VALUE * 512) | 3;
    for (unsigned 순번 = 0; 순번 < utent_paġna_COUNT; 순번++) paġna_Lista[순번] = (utent_BASE + 순번 * daqs_tal_paġna) | kernel_paġna;
    uint64_t Memorja_attribut_i_rreġistra = 0x4400, ADDRESS_Traduzzjoni_kontroll = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Memorja_attribut_i_rreġistra), "r"(ADDRESS_Traduzzjoni_kontroll), "r"((uintptr_t)għerq_ADDRESS) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t 실수저장상태 = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(실수저장상태) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    waqqaf_TIMEOUT();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 entrata_punt_VALUE 때만 ppermetti_VALUE.
    kompjuter_i_rreġistra(IRQ_distributur) = 0;
    kompjuter_i_rreġistra(IRQ_distributur + 0x180) = 0xffffffff;
    kompjuter_i_rreġistra(IRQ_distributur + 0x80) = 0xffffffff;
    kompjuter_i_rreġistra(IRQ_distributur + 0x280) = 1u << 30;
    kompjuter_i_rreġistra(IRQ_distributur + 0x41c) = 0x80808080;
    kompjuter_i_rreġistra(IRQ_distributur + 0x100) = 1u << 30;
    kompjuter_i_rreġistra(IRQ_CPU_interface + 4) = 0xff;
    kompjuter_i_rreġistra(IRQ_CPU_interface + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 수 있다.
    int Sigurtà = (kompjuter_i_rreġistra(IRQ_distributur + 4) & (1u << 10)) != 0;
    kompjuter_i_rreġistra(IRQ_distributur) = Sigurtà ? 1 : 3;
    kompjuter_i_rreġistra(IRQ_CPU_interface) = Sigurtà ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t TYPE_kategorija, kompjuter_TYPE; uint32_t 판번호;
    uint64_t entrata_punt, programm_Intestazzjoni_OFFSET, taqsima_Intestazzjoni_OFFSET; uint32_t 설정비트;
    uint16_t 실행머리크기, programm_Intestazzjoni_entrata_daqqas, programm_Intestazzjoni_COUNT, taqsima_Intestazzjoni_entrata_daqqas, taqsima_Intestazzjoni_COUNT, taqsima_isem_tabella_INDEX;
} 실행파일머리;
typedef struct { uint32_t TYPE_kategorija, 설정비트; uint64_t OFFSET_VALUE, ADDRESS, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(utent_frejm) == 272, "exception assembly layout");
static int 포함된범위(uint64_t OFFSET_VALUE, uint64_t daqqas, uint64_t ttermina_OFFSET) {
    return OFFSET_VALUE <= ttermina_OFFSET && daqqas <= ttermina_OFFSET - OFFSET_VALUE;
}
static int 부가정보검사(const unsigned char *data_pożizzjoni, size_t daqqas) {
    size_t 현재위치 = 0;
    while (포함된범위(현재위치, 12, daqqas)) {
        uint32_t 낱말들[3]; memcpy(낱말들, data_pożizzjoni + 현재위치, 12); 현재위치 += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(현재위치, 이름영역크기, daqqas) || !포함된범위(현재위치 + 이름영역크기, 설명크기, daqqas)) return 0;
        const unsigned char isem[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(isem) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(isem); 순번++) if (data_pożizzjoni[현재위치 + 순번] != isem[순번]) 일치 = 0;
        uint32_t 판번호 = 0;
        if (일치) memcpy(&판번호, data_pożizzjoni + 현재위치 + 이름영역크기, 4);
        if (일치 && 판번호 == 1) return 1;
        현재위치 += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *data, size_t daqqas, int 리눅스방식) {
    if (daqqas < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, data, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.TYPE_kategorija != 2 || 실행머리.kompjuter_TYPE != 183 || 실행머리.판번호 != 1 || 실행머리.설정비트 || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.programm_Intestazzjoni_entrata_daqqas != sizeof(실행파일구획) || !실행머리.programm_Intestazzjoni_COUNT || 실행머리.programm_Intestazzjoni_COUNT > 16 ||
        실행머리.programm_Intestazzjoni_OFFSET < sizeof(실행머리) || !포함된범위(실행머리.programm_Intestazzjoni_OFFSET, (uint64_t)실행머리.programm_Intestazzjoni_COUNT * sizeof(실행파일구획), daqqas)) return 사용자실행파일오류;
    uint8_t 사용량[(utent_IMAGE_ttermina - utent_BASE) / daqs_tal_paġna] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.programm_Intestazzjoni_COUNT; 순번++) {
        실행파일구획 data_pożizzjoni; memcpy(&data_pożizzjoni, data + 실행머리.programm_Intestazzjoni_OFFSET + 순번 * sizeof(data_pożizzjoni), sizeof(data_pożizzjoni));
        if (data_pożizzjoni.TYPE_kategorija == 4) {
            if (!포함된범위(data_pożizzjoni.OFFSET_VALUE, data_pożizzjoni.파일영역크기, daqqas)) return 사용자실행파일오류;
            if (부가정보검사(data + data_pożizzjoni.OFFSET_VALUE, data_pożizzjoni.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (data_pożizzjoni.TYPE_kategorija == 0 || data_pożizzjoni.TYPE_kategorija == 6 || (data_pożizzjoni.TYPE_kategorija == 0x6474e551 && !(data_pożizzjoni.설정비트 & 1))) continue;
        if (data_pożizzjoni.TYPE_kategorija != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!data_pożizzjoni.기억영역크기) continue;
        if (data_pożizzjoni.설정비트 & ~7u || !(data_pożizzjoni.설정비트 & 4) || (data_pożizzjoni.설정비트 & 3) == 3 || data_pożizzjoni.파일영역크기 > data_pożizzjoni.기억영역크기 ||
            (data_pożizzjoni.파일영역크기 && !포함된범위(data_pożizzjoni.OFFSET_VALUE, data_pożizzjoni.파일영역크기, daqqas)) || data_pożizzjoni.ADDRESS < utent_BASE ||
            !포함된범위(data_pożizzjoni.ADDRESS, data_pożizzjoni.기억영역크기, utent_IMAGE_ttermina) ||
            (!리눅스방식 && ((data_pożizzjoni.ADDRESS & (daqs_tal_paġna - 1)) || (data_pożizzjoni.OFFSET_VALUE & (daqs_tal_paġna - 1)) || data_pożizzjoni.맞춤 != daqs_tal_paġna)) ||
            (리눅스방식 && (((data_pożizzjoni.ADDRESS ^ data_pożizzjoni.OFFSET_VALUE) & (daqs_tal_paġna - 1)) || !data_pożizzjoni.맞춤 ||
                (data_pożizzjoni.맞춤 & (data_pożizzjoni.맞춤 - 1)) || data_pożizzjoni.맞춤 > 0x200000 || ((data_pożizzjoni.ADDRESS ^ data_pożizzjoni.OFFSET_VALUE) & (data_pożizzjoni.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (data_pożizzjoni.ADDRESS - utent_BASE) / daqs_tal_paġna;
        unsigned entrata_COUNT = ((data_pożizzjoni.ADDRESS & (daqs_tal_paġna - 1)) + data_pożizzjoni.기억영역크기 + daqs_tal_paġna - 1) / daqs_tal_paġna;
        for (unsigned paġna_VALUE = 첫항목; paġna_VALUE < 첫항목 + entrata_COUNT; paġna_VALUE++) {
            if (사용량[paġna_VALUE]) return 사용자실행파일오류;
            사용량[paġna_VALUE] = 1;
        }
        if ((data_pożizzjoni.설정비트 & 1) && 실행머리.entrata_punt >= data_pożizzjoni.ADDRESS && 실행머리.entrata_punt < data_pożizzjoni.ADDRESS + data_pożizzjoni.파일영역크기 && !(실행머리.entrata_punt & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *data, size_t daqqas) { return 실행파일검사(data, daqqas, 0); }
static void tqassim_tal_paġna(uintptr_t ADDRESS, uint64_t 설정비트, unsigned permessi) {
    unsigned LOOKUP_INDEX = (ADDRESS - utent_BASE) / daqs_tal_paġna;
    paġna_Lista[LOOKUP_INDEX] = ADDRESS | 설정비트;
    permessi_Lista[LOOKUP_INDEX] = permessi;
}
static int 사용자범위(uintptr_t ADDRESS, size_t entrata_COUNT, int 쓰는중) {
    if (ADDRESS < utent_BASE || !포함된범위(ADDRESS, entrata_COUNT, utent_ttermina)) return 0;
    if (!entrata_COUNT) return 1;
    unsigned 첫항목 = (ADDRESS - utent_BASE) / daqs_tal_paġna, 마지막 = (ADDRESS + entrata_COUNT - 1 - utent_BASE) / daqs_tal_paġna;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(permessi_Lista[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int kkopja_mogħdija(uintptr_t ADDRESS, char *mogħdija) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!사용자범위(ADDRESS, 1, 0)) return -14;
        mogħdija[순번] = *(const char *)ADDRESS++;
        if (!mogħdija[순번]) return 0;
    }
    return -36;
}
static intptr_t kernel_miżura(intptr_t miżura) { return miżura < 0 ? -오류번호 : miżura; }
static int 대응파일기술자(uint64_t fajl_handle) { return fajl_handle >= 3 && fajl_handle < 19 ? fajl_Lista[fajl_handle - 3] : -1; }
static int 통신끝점소유(uint64_t fajl_handle) { return fajl_handle >= 32 && fajl_handle < 56 && 통신끝점들[fajl_handle - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t tul_VALUE, struct pk_sockaddr_in *ADDRESS) {
    if (tul_VALUE != sizeof(*ADDRESS)) return -22;
    if (!사용자범위(가리킴값, tul_VALUE, 0)) return -14;
    memcpy(ADDRESS, (const void *)가리킴값, sizeof(*ADDRESS));
    return ADDRESS->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t tul_pointer, pk_socklen_t *수용량) {
    if (!사용자범위(tul_pointer, sizeof(*수용량), 1)) return -14;
    memcpy(수용량, (const void *)tul_pointer, sizeof(*수용량));
    if (*수용량 > sizeof(struct pk_sockaddr_in)) *수용량 = sizeof(struct pk_sockaddr_in);
    if (*수용량 && !사용자범위(가리킴값, *수용량, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t tul_pointer, pk_socklen_t 수용량, int ADDRESS, int 접속번호) {
    struct pk_sockaddr_in VALUE; memset(&VALUE, 0, sizeof(VALUE));
    VALUE.sin_family = AF_INET; VALUE.sin_port = pk_htons(접속번호); VALUE.sin_addr.s_addr = pk_htonl(ADDRESS);
    if (수용량) memcpy((void *)가리킴값, &VALUE, 수용량);
    pk_socklen_t tul_VALUE = sizeof(VALUE); memcpy((void *)tul_pointer, &tul_VALUE, sizeof(tul_VALUE));
}
extern uintptr_t bord_Kanal(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(utent_frejm *fajl_entrata) {
    uintptr_t 첫째값 = fajl_entrata->i_rreġistra_data[0], SECOND_VALUE = fajl_entrata->i_rreġistra_data[1], kodiċi_tal_karattru = fajl_entrata->i_rreġistra_data[2];
    char mogħdija[65];
    int fajl_handle, miżura;
    switch (fajl_entrata->i_rreġistra_data[8]) {
    case 0: return 1; // 자체 ABI 버전
    case 1: // write: pointer 전체를 검사한 Lura_VALUE 출력/fajl bidel_VALUE
        if (kodiċi_tal_karattru > 65536) return -22;
        if (!사용자범위(SECOND_VALUE, kodiċi_tal_karattru, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=Arloġġ_VALUE();
            for (size_t 순번 = 0; 순번 < kodiċi_tal_karattru; 순번++) bord_Kanal(첫째값, ((const unsigned char *)SECOND_VALUE)[순번]);
            /* 큰 tty를 그린 kernel_VALUE 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(interattiv){
                마감시각+=Arloġġ_VALUE()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(마감시각) : "memory");
            }
            return kodiċi_tal_karattru;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t element_COUNT=kodiċi_tal_karattru>512?512:kodiċi_tal_karattru;for(size_t 순번=0;순번<element_COUNT;순번++)자바전문넣기(순번,((const unsigned char *)SECOND_VALUE)[순번]);return 자바흐름쓰기(첫째값,element_COUNT);
        }
        fajl_handle = 대응파일기술자(첫째값); if (fajl_handle < 0) return -9;
        return kernel_miżura(pk_write(fajl_handle, (const void *)SECOND_VALUE, kodiċi_tal_karattru));
    case 2:
        if (kodiċi_tal_karattru > 65536) return -22;
        if (!사용자범위(SECOND_VALUE, kodiċi_tal_karattru, 1)) return -14;
        if (첫째값 == 0) {
            size_t element_COUNT = 0;
            while (element_COUNT < kodiċi_tal_karattru) {
                int karattru_VALUE = (int32_t)보드글자읽기(); if (karattru_VALUE == -2) return element_COUNT; if (karattru_VALUE < 0) break;
                ((unsigned char *)SECOND_VALUE)[element_COUNT++] = karattru_VALUE;
            }
            return element_COUNT ? (intptr_t)element_COUNT : (kodiċi_tal_karattru ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            miżura=자바흐름읽기(첫째값,kodiċi_tal_karattru>512?512:kodiċi_tal_karattru);if(miżura>0)for(int 순번=0;순번<miżura;순번++)((unsigned char *)SECOND_VALUE)[순번]=자바전문얻기(순번);return miżura;
        }
        fajl_handle = 대응파일기술자(첫째값); if (fajl_handle < 0) return -9;
        return kernel_miżura(pk_read(fajl_handle, (void *)SECOND_VALUE, kodiċi_tal_karattru));
    case 3:
        miżura = kkopja_mogħdija(첫째값, mogħdija); if (miżura) return miżura;
        if (SECOND_VALUE > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (fajl_Lista[순번] < 0) {
            fajl_handle = pk_open(mogħdija, (int)SECOND_VALUE, 0600);
            if (fajl_handle < 0) return -오류번호;
            fajl_Lista[순번] = fajl_handle; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { miżura = 통신끝점닫기(첫째값); if (!miżura) 통신끝점들[첫째값 - 32] = 0; return miżura; }
        fajl_handle = 대응파일기술자(첫째값); if (fajl_handle < 0) return -9;
        miżura = pk_close(fajl_handle); if (!miżura) fajl_Lista[첫째값 - 3] = -1;
        return kernel_miżura(miżura);
    case 5:
        fajl_handle = 대응파일기술자(첫째값); if (fajl_handle < 0) return -9;
        if (kodiċi_tal_karattru > 2) return -22;
        return kernel_miżura(pk_lseek(fajl_handle, (int64_t)SECOND_VALUE, kodiċi_tal_karattru));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 utent RW/NX 힙, 새로 노출되는 페이지는 0으로 inizjala
        if (!첫째값) return 동적기억끝;
        if (첫째값 < utent_IMAGE_ttermina || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + daqs_tal_paġna - 1) & ~(daqs_tal_paġna - 1);
        uintptr_t 새쪽들 = (첫째값 + daqs_tal_paġna - 1) & ~(daqs_tal_paġna - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t data_pożizzjoni = 이전쪽들; data_pożizzjoni < 새쪽들; data_pożizzjoni += daqs_tal_paġna) tqassim_tal_paġna(data_pożizzjoni, kernel_paġna, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t data_pożizzjoni = 이전쪽들; data_pożizzjoni < 새쪽들; data_pożizzjoni += daqs_tal_paġna) tqassim_tal_paġna(data_pożizzjoni, utent_qari_kitba, 3);
        } else {
            for (uintptr_t data_pożizzjoni = 새쪽들; data_pożizzjoni < 이전쪽들; data_pożizzjoni += daqs_tal_paġna) {
                paġna_Lista[(data_pożizzjoni - utent_BASE) / daqs_tal_paġna] = 0; permessi_Lista[(data_pożizzjoni - utent_BASE) / daqs_tal_paġna] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        fajl_handle = 대응파일기술자(첫째값); return fajl_handle < 0 ? -9 : kernel_miżura(pk_size(fajl_handle));
    case 10:
        fajl_handle = 대응파일기술자(첫째값); return fajl_handle < 0 ? -9 : kernel_miżura(pk_ftruncate(fajl_handle, (int64_t)SECOND_VALUE));
    case 11:
        miżura = kkopja_mogħdija(첫째값, mogħdija); return miżura ? miżura : kernel_miżura(pk_unlink(mogħdija));
    case 12:
        fajl_handle = 대응파일기술자(첫째값); return fajl_handle < 0 ? -9 : kernel_miżura(pk_fsync(fajl_handle));
    case 13: { // 그래픽 기초 API: utent 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = fajl_entrata->i_rreġistra_data[3], 높이값 = fajl_entrata->i_rreġistra_data[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SECOND_VALUE > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - SECOND_VALUE) return -22;
        for (uintptr_t 세로좌표 = SECOND_VALUE; 세로좌표 < SECOND_VALUE + 높이값; 세로좌표++) for (uintptr_t koordinat_x = 첫째값; koordinat_x < 첫째값 + 너비값; koordinat_x++) bord_pel(koordinat_x, 세로좌표, kodiċi_tal_karattru);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=element_COUNT; args(index,buffer,capacity)=UTF-8 tul_VALUE
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (kodiċi_tal_karattru <= 전달인수길이[첫째값]) return -36;
        if (!사용자범위(SECOND_VALUE, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SECOND_VALUE, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;interattiv=1;return bord_Terminal(13);}
        if(첫째값==2){interattiv=0;return 0;}
        if(첫째값==3)return bord_Terminal(13);
        if(첫째값!=1||!interattiv)return -22;
        miżura=(int32_t)보드글자읽기();
        if(miżura==-4096)return miżura;
        Bidu_TIMEOUT();return miżura<0?-11:miżura;
    case 17: { // 유한한 협력 대기: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t ttermina_TIME = Arloġġ_VALUE() + FREQUENCY * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Arloġġ_VALUE() < ttermina_TIME);
        Bidu_TIMEOUT(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 부모·빈 폴더를 검사한다.
        if (SECOND_VALUE > 2) return -22;
        miżura = kkopja_mogħdija(첫째값, mogħdija); if (miżura) return miżura;
        unsigned tul_VALUE = 0; while (mogħdija[tul_VALUE]) tul_VALUE++;
        miżura = 자바경로시작(tul_VALUE); if (miżura < 0) return miżura;
        for (unsigned 순번 = 0; 순번 < tul_VALUE; 순번++) 자바경로바이트(순번, (unsigned char)mogħdija[순번]);
        return SECOND_VALUE == 0 ? 자바항목종류() : SECOND_VALUE == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int karattru_VALUE=(int32_t)보드글자읽기();if(karattru_VALUE==-4096)return karattru_VALUE;if(karattru_VALUE>=0)화면누름(propjetarju_oġġett,karattru_VALUE);Bidu_TIMEOUT();}
        if(첫째값==3&&kodiċi_tal_karattru){if(!자바셸대화형())return -95;interattiv=1;bord_Terminal(300);}
        return 화면호출(propjetarju_oġġett,첫째값,SECOND_VALUE,kodiċi_tal_karattru,fajl_entrata->i_rreġistra_data[3],fajl_entrata->i_rreġistra_data[4],fajl_entrata->i_rreġistra_data[5]);
    case 21:
        if(kodiċi_tal_karattru>127)return -22;if(!사용자범위(SECOND_VALUE,kodiċi_tal_karattru*sizeof(uint32_t),0))return -14;
        return 화면글(propjetarju_oġġett,첫째값,(const uint32_t *)SECOND_VALUE,kodiċi_tal_karattru);
    case 22: // 화면 daqqas query_VALUE: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SECOND_VALUE==SOCK_STREAM&&(kodiċi_tal_karattru==0||kodiċi_tal_karattru==6))miżura=자바흐름만들기();
        else if(SECOND_VALUE==SOCK_DGRAM&&(kodiċi_tal_karattru==0||kodiċi_tal_karattru==IPPROTO_UDP))miżura=자바전문만들기(첫째값,SECOND_VALUE,kodiċi_tal_karattru);
        else return -93;
        if (miżura >= 32 && miżura < 56) 통신끝점들[miżura - 32] = 1;
        return miżura;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in ADDRESS;
        miżura = 주소입력(SECOND_VALUE, kodiċi_tal_karattru, &ADDRESS); if (miżura) return miżura;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(ADDRESS.sin_addr.s_addr),pk_htons(ADDRESS.sin_port)):자바전문묶기(첫째값, pk_htonl(ADDRESS.sin_addr.s_addr), pk_htons(ADDRESS.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (fajl_entrata->i_rreġistra_data[3]) return -95;
        if (kodiċi_tal_karattru > 512) return -90;
        if (kodiċi_tal_karattru && !사용자범위(SECOND_VALUE, kodiċi_tal_karattru, 0)) return -14;
        struct pk_sockaddr_in ADDRESS;
        miżura = 주소입력(fajl_entrata->i_rreġistra_data[4], fajl_entrata->i_rreġistra_data[5], &ADDRESS); if (miżura) return miżura;
        for (unsigned 순번 = 0; 순번 < kodiċi_tal_karattru; 순번++) 자바전문넣기(순번, ((const unsigned char *)SECOND_VALUE)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(ADDRESS.sin_addr.s_addr), pk_htons(ADDRESS.sin_port), kodiċi_tal_karattru);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (fajl_entrata->i_rreġistra_data[3]) return -95;
        if (kodiċi_tal_karattru > 512) return -90;
        if (kodiċi_tal_karattru && !사용자범위(SECOND_VALUE, kodiċi_tal_karattru, 1)) return -14;
        pk_socklen_t 수용량 = 0;
        if (fajl_entrata->i_rreġistra_data[4]) { miżura = 주소출력검사(fajl_entrata->i_rreġistra_data[4], fajl_entrata->i_rreġistra_data[5], &수용량); if (miżura) return miżura; }
        miżura = 자바전문받기(첫째값, kodiċi_tal_karattru); if (miżura < 0) return miżura;
        for (int 순번 = 0; 순번 < miżura; 순번++) ((unsigned char *)SECOND_VALUE)[순번] = 자바전문얻기(순번);
        if (fajl_entrata->i_rreġistra_data[4]) 주소출력(fajl_entrata->i_rreġistra_data[4], fajl_entrata->i_rreġistra_data[5], 수용량, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return miżura;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t 수용량;
        miżura = 주소출력검사(SECOND_VALUE, kodiċi_tal_karattru, &수용량); if (miżura) return miżura;
        주소출력(SECOND_VALUE,kodiċi_tal_karattru,수용량,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in ADDRESS;
        miżura=주소입력(SECOND_VALUE,kodiċi_tal_karattru,&ADDRESS);if(miżura)return miżura;
        return 자바흐름연결(첫째값,pk_htonl(ADDRESS.sin_addr.s_addr),pk_htons(ADDRESS.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,SECOND_VALUE):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(SECOND_VALUE||kodiċi_tal_karattru)return -95;miżura=자바흐름연결받기(첫째값);if(miżura>=40&&miżura<56)통신끝점들[miżura-32]=1;return miżura;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(utent_frejm *fajl_entrata) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(fajl_entrata) : 자체체계호출(fajl_entrata);
}
static void 커널돌아가기(utent_frejm *fajl_entrata, int miżura) {
    waqqaf_TIMEOUT();
    fajl_entrata->i_rreġistra_data[0] = (uint64_t)(int64_t)miżura;
    fajl_entrata->kmand_pożizzjoni = (uintptr_t)사용자복귀;
    fajl_entrata->stat_CODE = 0x3c5; // EL1h, DAIF masked
}
int 사용자예외(utent_frejm *fajl_entrata, unsigned INTERCEPT) {
    if (!attiv || (fajl_entrata->stat_CODE & 15) != 0) return 0;
    if (INTERCEPT) {
        uint32_t 승인값 = kompjuter_i_rreġistra(IRQ_CPU_interface + 0xc), identifikatur_VALUE = 승인값 & 1023;
        if (identifikatur_VALUE == 30) { 커널돌아가기(fajl_entrata, utent_TIMEOUT); kompjuter_i_rreġistra(IRQ_CPU_interface + 0x10) = 승인값; return 1; }
        if (identifikatur_VALUE < 1020) kompjuter_i_rreġistra(IRQ_CPU_interface + 0x10) = 승인값;
        return 1;
    }
    uint64_t 예외상태; __asm__ volatile("mrs %0, esr_el1" : "=r"(예외상태));
    if (Arloġġ_VALUE() >= 마감시각) { 커널돌아가기(fajl_entrata, utent_TIMEOUT); return 1; }
    unsigned 예외분류 = 예외상태 >> 26;
    if (예외분류 == 0x15 && (예외상태 & 0xffff) == 0) {
        if (리눅스규약 ? fajl_entrata->i_rreġistra_data[8] == 93 || fajl_entrata->i_rreġistra_data[8] == 94 : fajl_entrata->i_rreġistra_data[8] == 6) 커널돌아가기(fajl_entrata, (int)(fajl_entrata->i_rreġistra_data[0] & 255));
        else {
            intptr_t miżura=체계호출(fajl_entrata);
            if(miżura==-4096&&interattiv){
                저장값[propjetarju_oġġett].실행틀=*fajl_entrata;저장값[propjetarju_oġġett].실행틀.kmand_pożizzjoni-=4;
                사용자실수보관(저장값[propjetarju_oġġett].실수저장상태);커널돌아가기(fajl_entrata,사용자중단됨);
            }else fajl_entrata->i_rreġistra_data[0]=(uint64_t)miżura;
        }
    } else 커널돌아가기(fajl_entrata, 예외분류 == 0x24 ? utent_data_żball : 예외분류 == 0x20 ? 사용자실행오류 : utent_invalidu_istruzzjoni);
    return 1;
}

// 생성된 const ELF grupp_VALUE: 실행은 반드시 programm_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *data; size_t daqqas; unsigned 전달값; } programm;
#include "programs.h"
static void *kopja_dell(unsigned pożizzjoni_INDEX){return (void *)(0x04000000ul+pożizzjoni_INDEX*(utent_ttermina-utent_BASE));}
static int Tmiem_programm(int miżura){
    사용자누적시각[propjetarju_oġġett]+=(uint32_t)보드밀리초()-사용자실행시각[propjetarju_oġġett];
    waqqaf_TIMEOUT();attiv=0;
    if(miżura==사용자중단됨){
        저장된작업 *string_data=&저장값[propjetarju_oġġett];string_data->멈춤상태=1;string_data->interattiv=interattiv;string_data->리눅스규약=리눅스규약;string_data->동적기억공간=동적기억끝;string_data->인수개수=전달인수개수;
        memcpy(string_data->permessi_Lista,permessi_Lista,sizeof(permessi_Lista));memcpy(string_data->fajl_Lista,fajl_Lista,sizeof(fajl_Lista));memcpy(string_data->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(string_data->argument_ARRAY,전달인수,sizeof(전달인수));memcpy(string_data->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<utent_paġna_COUNT;순번++)if(permessi_Lista[순번])memcpy((unsigned char *)kopja_dell(propjetarju_oġġett)+순번*daqs_tal_paġna,(void *)(utent_BASE+순번*daqs_tal_paġna),daqs_tal_paġna);
    }else{
        저장값[propjetarju_oġġett].멈춤상태=0;화면초기화(propjetarju_oġġett);
        for(unsigned 순번=0;순번<16;순번++)if(fajl_Lista[순번]>=0)pk_close(fajl_Lista[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<utent_paġna_COUNT;순번++){paġna_Lista[순번]=0;permessi_Lista[순번]=0;}변환표맞추기();return miżura;
}
uintptr_t bord_kontroll_tal_utent(uintptr_t azzjoni){
    unsigned pożizzjoni_INDEX=azzjoni&15;if(pożizzjoni_INDEX>=4||attiv)return (uint32_t)-22;
    저장된작업 *string_data=&저장값[pożizzjoni_INDEX];
    if(azzjoni>=32){if(string_data->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(string_data->fajl_Lista[순번]>=0)pk_close(string_data->fajl_Lista[순번]);for(unsigned 순번=0;순번<24;순번++)if(string_data->통신끝점들[순번])통신끝점닫기(순번+32);}string_data->멈춤상태=0;화면초기화(pożizzjoni_INDEX);return 0;}
    if(azzjoni>=16)return string_data->멈춤상태;
    if(!string_data->멈춤상태)return (uint32_t)-22;
    propjetarju_oġġett=pożizzjoni_INDEX;interattiv=string_data->interattiv;리눅스규약=string_data->리눅스규약;동적기억끝=string_data->동적기억공간;전달인수개수=string_data->인수개수;
    memcpy(fajl_Lista,string_data->fajl_Lista,sizeof(fajl_Lista));memcpy(통신끝점들,string_data->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,string_data->argument_ARRAY,sizeof(전달인수));memcpy(전달인수길이,string_data->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<utent_paġna_COUNT;순번++)paġna_Lista[순번]=(utent_BASE+순번*daqs_tal_paġna)|kernel_paġna;변환표맞추기();
    memset((void *)utent_BASE,0,utent_ttermina-utent_BASE);
    for(unsigned 순번=0;순번<utent_paġna_COUNT;순번++)if(string_data->permessi_Lista[순번])memcpy((void *)(utent_BASE+순번*daqs_tal_paġna),(unsigned char *)kopja_dell(pożizzjoni_INDEX)+순번*daqs_tal_paġna,daqs_tal_paġna);
    memcpy(permessi_Lista,string_data->permessi_Lista,sizeof(permessi_Lista));
    for(unsigned 순번=0;순번<utent_paġna_COUNT;순번++){unsigned data_pożizzjoni=permessi_Lista[순번];paġna_Lista[순번]=data_pożizzjoni?(utent_BASE+순번*daqs_tal_paġna)|(data_pożizzjoni==3?utent_qari_kitba:data_pożizzjoni==5?사용자읽고실행:utent_qari_biss):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");attiv=1;string_data->멈춤상태=0;Bidu_TIMEOUT();
    사용자실행시각[propjetarju_oġġett]=보드밀리초();
    return (uint32_t)Tmiem_programm(utent_CV(&string_data->실행틀,string_data->실수저장상태));
}
static int serje_programm(const unsigned char *data, size_t daqqas, unsigned 전달값, int 리눅스방식, const char *isem) {
    if (attiv) return -16;
    propjetarju_oġġett=bord_Terminal(11);if(propjetarju_oġġett<0||propjetarju_oġġett>3||저장값[propjetarju_oġġett].멈춤상태)return -16;interattiv=0;
    int 유효함 = 실행파일검사(data, daqqas, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned isem_INDEX=0;
    while (*isem && isem_INDEX<31) utent_kmand_isem[propjetarju_oġġett][isem_INDEX++]=(unsigned char)*isem++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (isem_INDEX) utent_kmand_isem[propjetarju_oġġett][isem_INDEX++]=' ';
        for (unsigned pożizzjoni_INDEX=0; pożizzjoni_INDEX<전달인수길이[0]; pożizzjoni_INDEX++) utent_kmand_isem[propjetarju_oġġett][isem_INDEX++]=전달인수[0][pożizzjoni_INDEX];
    }
    utent_kmand_isem[propjetarju_oġġett][isem_INDEX]=0; numru_tal_utent[propjetarju_oġġett]=Li_Jmiss_numru_tal_utent++;
    if (Li_Jmiss_numru_tal_utent>0x7fffffffu) Li_Jmiss_numru_tal_utent=10;
    utent_Bidu_TIME[propjetarju_oġġett]=보드밀리초(); 사용자누적시각[propjetarju_oġġett]=0;
    for (unsigned 순번 = 0; 순번 < utent_paġna_COUNT; 순번++) paġna_Lista[순번] = (utent_BASE + 순번 * daqs_tal_paġna) | kernel_paġna;
    변환표맞추기();
    memset((void *)utent_BASE, 0, utent_ttermina - utent_BASE);
    memset(permessi_Lista, 0, sizeof(permessi_Lista));
    실행파일머리 실행머리; memcpy(&실행머리, data, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.programm_Intestazzjoni_COUNT; 순번++) {
        실행파일구획 data_pożizzjoni; memcpy(&data_pożizzjoni, data + 실행머리.programm_Intestazzjoni_OFFSET + 순번 * sizeof(data_pożizzjoni), sizeof(data_pożizzjoni));
        if (data_pożizzjoni.TYPE_kategorija != 1 || !data_pożizzjoni.기억영역크기) continue;
        if (data_pożizzjoni.파일영역크기) memcpy((void *)(uintptr_t)data_pożizzjoni.ADDRESS, data + data_pożizzjoni.OFFSET_VALUE, data_pożizzjoni.파일영역크기);
        for (uintptr_t 현재위치 = data_pożizzjoni.ADDRESS & ~(daqs_tal_paġna - 1); 현재위치 < data_pożizzjoni.ADDRESS + data_pożizzjoni.기억영역크기; 현재위치 += daqs_tal_paġna) {
            permessi_Lista[(현재위치 - utent_BASE) / daqs_tal_paġna] = (data_pożizzjoni.설정비트 & 2) ? 3 : ((data_pożizzjoni.설정비트 & 1) ? 5 : 1);
        }
    }
    for (uintptr_t 현재위치 = utent_Munzell_ADDRESS; 현재위치 < utent_ttermina; 현재위치 += daqs_tal_paġna) permessi_Lista[(현재위치 - utent_BASE) / daqs_tal_paġna] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.entrata_punt) : utent_ttermina;
    for (unsigned 순번 = 0; 순번 < utent_paġna_COUNT; 순번++) {
        unsigned permessi = permessi_Lista[순번];
        paġna_Lista[순번] = permessi ? (utent_BASE + 순번 * daqs_tal_paġna) | (permessi == 3 ? utent_qari_kitba : permessi == 5 ? 사용자읽고실행 : utent_qari_biss) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) fajl_Lista[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = utent_IMAGE_ttermina;
    attiv = 1; Bidu_TIMEOUT();
    사용자실행시각[propjetarju_oġġett]=보드밀리초();
    int miżura = utent_daħħal(실행머리.entrata_punt, 초기쌓임공간, 전달값);
    return Tmiem_programm(miżura);
}
uintptr_t bord_utent_serje(uintptr_t LOOKUP_INDEX) {
    if (LOOKUP_INDEX >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *isem=LOOKUP_INDEX==10?"javac":LOOKUP_INDEX==11?"java":LOOKUP_INDEX==12?"python":LOOKUP_INDEX==13?"vi":LOOKUP_INDEX==14?"jar":LOOKUP_INDEX==15?"cc":LOOKUP_INDEX==16?"jaot":"ELF";
    return (uint32_t)serje_programm(실행항목들[LOOKUP_INDEX].data, 실행항목들[LOOKUP_INDEX].daqqas, 실행항목들[LOOKUP_INDEX].전달값, 0, isem);
}
static uintptr_t eżegwixxa_fajl(int 리눅스방식) {
    static unsigned char IMAGE[16384];
    if (attiv || !전달인수개수) return (uint32_t)-22;
    int fajl_handle = pk_open((const char *)전달인수[0], qari_biss_VALUE, 0);
    if (fajl_handle < 0) return (uint32_t)-오류번호;
    int daqqas = pk_size(fajl_handle);
    if (daqqas < 0 || (unsigned)daqqas > sizeof(IMAGE)) { pk_close(fajl_handle); return (uint32_t)-27; }
    int RECEIVED_COUNT = pk_read(fajl_handle, IMAGE, daqqas); pk_close(fajl_handle);
    if (RECEIVED_COUNT != daqqas) return (uint32_t)-5;
    return (uint32_t)serje_programm(IMAGE, daqqas, 0, 리눅스방식, "");
}
uintptr_t bord_utent_fajl(void) { return eżegwixxa_fajl(0); }
uintptr_t 보드사용자리눅스파일(void) { return eżegwixxa_fajl(1); }
uintptr_t bord_utent_vvalida(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].data, 잘못된실행항목들[순번].daqqas) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
