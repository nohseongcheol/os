#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 Mag_execute_utos machine patong_VALUE. file data/정책은 기존 AOT Java 커널에 위임한다.
#include "gumagamit.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../Network_Stack/Network_Stack.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define machine_magrehistro(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_distributor 0xff841000ul
#define IRQ_CPU_interface 0xff842000ul
#define laki_ng_pahina 4096ul
#define 접근표시 (1ul << 10)
#define hindi_Mag_execute_pahintulot (1ul << 53)
#define gumagamit_hindi_Mag_execute (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | 접근표시)
#define kernel_page (3ul | 보통기억 | hindi_Mag_execute_pahintulot | gumagamit_hindi_Mag_execute)
#define gumagamit_nababasa_nasusulatan (3ul | 보통기억 | (1ul << 6) | hindi_Mag_execute_pahintulot | gumagamit_hindi_Mag_execute)
#define gumagamit_mababasa_lamang (3ul | 보통기억 | (3ul << 6) | hindi_Mag_execute_pahintulot | gumagamit_hindi_Mag_execute)
#define 사용자읽고실행 (3ul | 보통기억 | (3ul << 6) | hindi_Mag_execute_pahintulot)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t board_pel(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t board_Terminal(uintptr_t);
extern int Terminal_pending(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int gumagamit_CV(gumagamit_frame *,void *);
extern void 사용자실수보관(void *);
extern int gumagamit_magpasok(uintptr_t pagpasok_point, uintptr_t Stack_Storage, uintptr_t 전달값);
extern void 사용자복귀(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t root_email[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t page_list[gumagamit_page_COUNT] __attribute__((aligned(4096)));
static uint8_t Mga_Pahintulot_list[gumagamit_page_COUNT];
static int Aktibo, file_list[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned file_hawakán){return file_hawakán<40?자바전문닫기(file_hawakán):자바흐름닫기(file_hawakán);}
static uint64_t FREQUENCY, 마감시각;
static uintptr_t 동적기억끝;
// kernel_VALUE 셸이 준비한 UTF-8 인수. EL0에는 gumawa_ng_kopya_VALUE 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,tumutugon_interactive,리눅스규약,file_list[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char argumento_ARRAY[8][256],Mga_Pahintulot_list[gumagamit_page_COUNT];
    uintptr_t 동적기억공간; gumagamit_frame 실행틀;
    unsigned char 실수저장상태[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int may_ari_bagay,tumutugon_interactive;
static uint32_t user_number[4], gumagamit_Start_TIME[4], 사용자누적시각[4], 사용자실행시각[4], Susunod_user_number=10;
static unsigned char gumagamit_utos_pangalan[4][288];
uint32_t 사용자상태읽기(unsigned pagpasok_VALUE, unsigned INDEX) {
    unsigned posisyon_INDEX=INDEX&3;
    int katayuan_VALUE=(Aktibo && may_ari_bagay==(int)posisyon_INDEX) ? 1 : 저장값[posisyon_INDEX].멈춤상태 ? 2 : 0;
    if (pagpasok_VALUE==0) return katayuan_VALUE;
    if (!katayuan_VALUE) return 0;
    if (pagpasok_VALUE==1) return user_number[posisyon_INDEX];
    if (pagpasok_VALUE==2) {
        unsigned char *쪽들=katayuan_VALUE==1?Mga_Pahintulot_list:저장값[posisyon_INDEX].Mga_Pahintulot_list;
        unsigned page_COUNT=0; for (unsigned 순번=0; 순번<gumagamit_page_COUNT; 순번++) if(쪽들[순번]) page_COUNT++;
        return page_COUNT*4;
    }
    if (pagpasok_VALUE==3) return (uint32_t)보드밀리초()-gumagamit_Start_TIME[posisyon_INDEX];
    if (pagpasok_VALUE==4) return 사용자누적시각[posisyon_INDEX]+(katayuan_VALUE==1?(uint32_t)보드밀리초()-사용자실행시각[posisyon_INDEX]:0);
    if (pagpasok_VALUE==5) return INDEX/4<sizeof(gumagamit_utos_pangalan[0])?gumagamit_utos_pangalan[posisyon_INDEX][INDEX/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t pagpasok_COUNT) {
    if (Aktibo || pagpasok_COUNT > 8) return (uint32_t)-22;
    전달인수개수 = pagpasok_COUNT;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t LOOKUP_INDEX, uintptr_t 현재위치, uintptr_t byte_data) {
    if (Aktibo || LOOKUP_INDEX >= 전달인수개수 || 현재위치 >= 255 || 현재위치 != 전달인수길이[LOOKUP_INDEX] || !byte_data || byte_data > 255)
        return (uint32_t)-22;
    전달인수[LOOKUP_INDEX][현재위치] = byte_data;
    전달인수길이[LOOKUP_INDEX] = 현재위치 + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Orasan_VALUE(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Hinto_TIMEOUT(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    machine_magrehistro(IRQ_distributor + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void Start_TIMEOUT(void) {
    uint64_t 간격 = FREQUENCY * 2, i_on = 1;
    마감시각 = Orasan_VALUE() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(i_on) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned data_i_block = 0; data_i_block < 4; data_i_block++) {
        root_email[data_i_block] = (uintptr_t)가운데[data_i_block] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t email = ((uintptr_t)data_i_block << 30) | ((uintptr_t)순번 << 21);
            가운데[data_i_block][순번] = email | 1 | 접근표시 | gumagamit_hindi_Mag_execute;
            if (email >= 0xfc000000ul) 가운데[data_i_block][순번] |= hindi_Mag_execute_pahintulot; // Device-nGnRnE
            else 가운데[data_i_block][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned SECOND_VALUE = 0; SECOND_VALUE < gumagamit_page_COUNT / 512; SECOND_VALUE++)
        가운데[0][(gumagamit_BASE >> 21) + SECOND_VALUE] = (uintptr_t)(page_list + SECOND_VALUE * 512) | 3;
    for (unsigned 순번 = 0; 순번 < gumagamit_page_COUNT; 순번++) page_list[순번] = (gumagamit_BASE + 순번 * laki_ng_pahina) | kernel_page;
    uint64_t Memory_katangian_magrehistro = 0x4400, email_Translation_control = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Memory_katangian_magrehistro), "r"(email_Translation_control), "r"((uintptr_t)root_email) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t 실수저장상태 = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(실수저장상태) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    Hinto_TIMEOUT();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 pagpasok_point_VALUE 때만 payagan_VALUE.
    machine_magrehistro(IRQ_distributor) = 0;
    machine_magrehistro(IRQ_distributor + 0x180) = 0xffffffff;
    machine_magrehistro(IRQ_distributor + 0x80) = 0xffffffff;
    machine_magrehistro(IRQ_distributor + 0x280) = 1u << 30;
    machine_magrehistro(IRQ_distributor + 0x41c) = 0x80808080;
    machine_magrehistro(IRQ_distributor + 0x100) = 1u << 30;
    machine_magrehistro(IRQ_CPU_interface + 4) = 0xff;
    machine_magrehistro(IRQ_CPU_interface + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 수 있다.
    int Seguridad = (machine_magrehistro(IRQ_distributor + 4) & (1u << 10)) != 0;
    machine_magrehistro(IRQ_distributor) = Seguridad ? 1 : 3;
    machine_magrehistro(IRQ_CPU_interface) = Seguridad ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t TYPE_kategorya, machine_TYPE; uint32_t 판번호;
    uint64_t pagpasok_point, app_Header_OFFSET, seksiyon_Header_OFFSET; uint32_t kompigurasyon_Background_Intelligent_Transfer_Service;
    uint16_t 실행머리크기, app_Header_pagpasok_sukat, app_Header_COUNT, seksiyon_Header_pagpasok_sukat, seksiyon_Header_COUNT, seksiyon_pangalan_talahanayan_INDEX;
} 실행파일머리;
typedef struct { uint32_t TYPE_kategorya, kompigurasyon_Background_Intelligent_Transfer_Service; uint64_t OFFSET_VALUE, email, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(gumagamit_frame) == 272, "exception assembly layout");
static int 포함된범위(uint64_t OFFSET_VALUE, uint64_t sukat_82232621, uint64_t tapusin_OFFSET) {
    return OFFSET_VALUE <= tapusin_OFFSET && sukat_82232621 <= tapusin_OFFSET - OFFSET_VALUE;
}
static int 부가정보검사(const unsigned char *data_posisyon, size_t sukat_82232621) {
    size_t 현재위치 = 0;
    while (포함된범위(현재위치, 12, sukat_82232621)) {
        uint32_t 낱말들[3]; memcpy(낱말들, data_posisyon + 현재위치, 12); 현재위치 += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(현재위치, 이름영역크기, sukat_82232621) || !포함된범위(현재위치 + 이름영역크기, 설명크기, sukat_82232621)) return 0;
        const unsigned char pangalan[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(pangalan) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(pangalan); 순번++) if (data_posisyon[현재위치 + 순번] != pangalan[순번]) 일치 = 0;
        uint32_t 판번호 = 0;
        if (일치) memcpy(&판번호, data_posisyon + 현재위치 + 이름영역크기, 4);
        if (일치 && 판번호 == 1) return 1;
        현재위치 += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *data, size_t sukat_82232621, int 리눅스방식) {
    if (sukat_82232621 < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, data, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.TYPE_kategorya != 2 || 실행머리.machine_TYPE != 183 || 실행머리.판번호 != 1 || 실행머리.kompigurasyon_Background_Intelligent_Transfer_Service || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.app_Header_pagpasok_sukat != sizeof(실행파일구획) || !실행머리.app_Header_COUNT || 실행머리.app_Header_COUNT > 16 ||
        실행머리.app_Header_OFFSET < sizeof(실행머리) || !포함된범위(실행머리.app_Header_OFFSET, (uint64_t)실행머리.app_Header_COUNT * sizeof(실행파일구획), sukat_82232621)) return 사용자실행파일오류;
    uint8_t 사용량[(gumagamit_IMAGE_tapusin - gumagamit_BASE) / laki_ng_pahina] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.app_Header_COUNT; 순번++) {
        실행파일구획 data_posisyon; memcpy(&data_posisyon, data + 실행머리.app_Header_OFFSET + 순번 * sizeof(data_posisyon), sizeof(data_posisyon));
        if (data_posisyon.TYPE_kategorya == 4) {
            if (!포함된범위(data_posisyon.OFFSET_VALUE, data_posisyon.파일영역크기, sukat_82232621)) return 사용자실행파일오류;
            if (부가정보검사(data + data_posisyon.OFFSET_VALUE, data_posisyon.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (data_posisyon.TYPE_kategorya == 0 || data_posisyon.TYPE_kategorya == 6 || (data_posisyon.TYPE_kategorya == 0x6474e551 && !(data_posisyon.kompigurasyon_Background_Intelligent_Transfer_Service & 1))) continue;
        if (data_posisyon.TYPE_kategorya != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!data_posisyon.기억영역크기) continue;
        if (data_posisyon.kompigurasyon_Background_Intelligent_Transfer_Service & ~7u || !(data_posisyon.kompigurasyon_Background_Intelligent_Transfer_Service & 4) || (data_posisyon.kompigurasyon_Background_Intelligent_Transfer_Service & 3) == 3 || data_posisyon.파일영역크기 > data_posisyon.기억영역크기 ||
            (data_posisyon.파일영역크기 && !포함된범위(data_posisyon.OFFSET_VALUE, data_posisyon.파일영역크기, sukat_82232621)) || data_posisyon.email < gumagamit_BASE ||
            !포함된범위(data_posisyon.email, data_posisyon.기억영역크기, gumagamit_IMAGE_tapusin) ||
            (!리눅스방식 && ((data_posisyon.email & (laki_ng_pahina - 1)) || (data_posisyon.OFFSET_VALUE & (laki_ng_pahina - 1)) || data_posisyon.맞춤 != laki_ng_pahina)) ||
            (리눅스방식 && (((data_posisyon.email ^ data_posisyon.OFFSET_VALUE) & (laki_ng_pahina - 1)) || !data_posisyon.맞춤 ||
                (data_posisyon.맞춤 & (data_posisyon.맞춤 - 1)) || data_posisyon.맞춤 > 0x200000 || ((data_posisyon.email ^ data_posisyon.OFFSET_VALUE) & (data_posisyon.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (data_posisyon.email - gumagamit_BASE) / laki_ng_pahina;
        unsigned pagpasok_COUNT = ((data_posisyon.email & (laki_ng_pahina - 1)) + data_posisyon.기억영역크기 + laki_ng_pahina - 1) / laki_ng_pahina;
        for (unsigned page_VALUE = 첫항목; page_VALUE < 첫항목 + pagpasok_COUNT; page_VALUE++) {
            if (사용량[page_VALUE]) return 사용자실행파일오류;
            사용량[page_VALUE] = 1;
        }
        if ((data_posisyon.kompigurasyon_Background_Intelligent_Transfer_Service & 1) && 실행머리.pagpasok_point >= data_posisyon.email && 실행머리.pagpasok_point < data_posisyon.email + data_posisyon.파일영역크기 && !(실행머리.pagpasok_point & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *data, size_t sukat_82232621) { return 실행파일검사(data, sukat_82232621, 0); }
static void pagkakalatag_sa_pahina(uintptr_t email, uint64_t kompigurasyon_Background_Intelligent_Transfer_Service, unsigned mga_pahintulot) {
    unsigned LOOKUP_INDEX = (email - gumagamit_BASE) / laki_ng_pahina;
    page_list[LOOKUP_INDEX] = email | kompigurasyon_Background_Intelligent_Transfer_Service;
    Mga_Pahintulot_list[LOOKUP_INDEX] = mga_pahintulot;
}
static int 사용자범위(uintptr_t email, size_t pagpasok_COUNT, int 쓰는중) {
    if (email < gumagamit_BASE || !포함된범위(email, pagpasok_COUNT, gumagamit_tapusin)) return 0;
    if (!pagpasok_COUNT) return 1;
    unsigned 첫항목 = (email - gumagamit_BASE) / laki_ng_pahina, 마지막 = (email + pagpasok_COUNT - 1 - gumagamit_BASE) / laki_ng_pahina;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(Mga_Pahintulot_list[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int gumawa_ng_kopya_path(uintptr_t email, char *path) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!사용자범위(email, 1, 0)) return -14;
        path[순번] = *(const char *)email++;
        if (!path[순번]) return 0;
    }
    return -36;
}
static intptr_t kernel_sukat(intptr_t sukat) { return sukat < 0 ? -오류번호 : sukat; }
static int 대응파일기술자(uint64_t file_hawakán) { return file_hawakán >= 3 && file_hawakán < 19 ? file_list[file_hawakán - 3] : -1; }
static int 통신끝점소유(uint64_t file_hawakán) { return file_hawakán >= 32 && file_hawakán < 56 && 통신끝점들[file_hawakán - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t haba_VALUE, struct pk_sockaddr_in *email) {
    if (haba_VALUE != sizeof(*email)) return -22;
    if (!사용자범위(가리킴값, haba_VALUE, 0)) return -14;
    memcpy(email, (const void *)가리킴값, sizeof(*email));
    return email->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t haba_pointer, pk_socklen_t *수용량) {
    if (!사용자범위(haba_pointer, sizeof(*수용량), 1)) return -14;
    memcpy(수용량, (const void *)haba_pointer, sizeof(*수용량));
    if (*수용량 > sizeof(struct pk_sockaddr_in)) *수용량 = sizeof(struct pk_sockaddr_in);
    if (*수용량 && !사용자범위(가리킴값, *수용량, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t haba_pointer, pk_socklen_t 수용량, int email, int numero_ng_port) {
    struct pk_sockaddr_in VALUE; memset(&VALUE, 0, sizeof(VALUE));
    VALUE.sin_family = AF_INET; VALUE.sin_port = pk_htons(numero_ng_port); VALUE.sin_addr.s_addr = pk_htonl(email);
    if (수용량) memcpy((void *)가리킴값, &VALUE, 수용량);
    pk_socklen_t haba_VALUE = sizeof(VALUE); memcpy((void *)haba_pointer, &haba_VALUE, sizeof(haba_VALUE));
}
extern uintptr_t board_channel(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(gumagamit_frame *file_pagpasok) {
    uintptr_t 첫째값 = file_pagpasok->magrehistro_data[0], SECOND_VALUE = file_pagpasok->magrehistro_data[1], character_code = file_pagpasok->magrehistro_data[2];
    char path[65];
    int file_hawakán, sukat;
    switch (file_pagpasok->magrehistro_data[8]) {
    case 0: return 1; // 자체 ABI 버전
    case 1: // write: pointer 전체를 검사한 Bumalik_VALUE 출력/file baguhin_VALUE
        if (character_code > 65536) return -22;
        if (!사용자범위(SECOND_VALUE, character_code, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=Orasan_VALUE();
            for (size_t 순번 = 0; 순번 < character_code; 순번++) board_channel(첫째값, ((const unsigned char *)SECOND_VALUE)[순번]);
            /* 큰 tty를 그린 kernel_VALUE 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(tumutugon_interactive){
                마감시각+=Orasan_VALUE()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(마감시각) : "memory");
            }
            return character_code;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t item_COUNT=character_code>512?512:character_code;for(size_t 순번=0;순번<item_COUNT;순번++)자바전문넣기(순번,((const unsigned char *)SECOND_VALUE)[순번]);return 자바흐름쓰기(첫째값,item_COUNT);
        }
        file_hawakán = 대응파일기술자(첫째값); if (file_hawakán < 0) return -9;
        return kernel_sukat(pk_write(file_hawakán, (const void *)SECOND_VALUE, character_code));
    case 2:
        if (character_code > 65536) return -22;
        if (!사용자범위(SECOND_VALUE, character_code, 1)) return -14;
        if (첫째값 == 0) {
            size_t item_COUNT = 0;
            while (item_COUNT < character_code) {
                int karakter_VALUE = (int32_t)보드글자읽기(); if (karakter_VALUE == -2) return item_COUNT; if (karakter_VALUE < 0) break;
                ((unsigned char *)SECOND_VALUE)[item_COUNT++] = karakter_VALUE;
            }
            return item_COUNT ? (intptr_t)item_COUNT : (character_code ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            sukat=자바흐름읽기(첫째값,character_code>512?512:character_code);if(sukat>0)for(int 순번=0;순번<sukat;순번++)((unsigned char *)SECOND_VALUE)[순번]=자바전문얻기(순번);return sukat;
        }
        file_hawakán = 대응파일기술자(첫째값); if (file_hawakán < 0) return -9;
        return kernel_sukat(pk_read(file_hawakán, (void *)SECOND_VALUE, character_code));
    case 3:
        sukat = gumawa_ng_kopya_path(첫째값, path); if (sukat) return sukat;
        if (SECOND_VALUE > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (file_list[순번] < 0) {
            file_hawakán = pk_open(path, (int)SECOND_VALUE, 0600);
            if (file_hawakán < 0) return -오류번호;
            file_list[순번] = file_hawakán; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { sukat = 통신끝점닫기(첫째값); if (!sukat) 통신끝점들[첫째값 - 32] = 0; return sukat; }
        file_hawakán = 대응파일기술자(첫째값); if (file_hawakán < 0) return -9;
        sukat = pk_close(file_hawakán); if (!sukat) file_list[첫째값 - 3] = -1;
        return kernel_sukat(sukat);
    case 5:
        file_hawakán = 대응파일기술자(첫째값); if (file_hawakán < 0) return -9;
        if (character_code > 2) return -22;
        return kernel_sukat(pk_lseek(file_hawakán, (int64_t)SECOND_VALUE, character_code));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 gumagamit RW/NX 힙, 새로 노출되는 페이지는 0으로 magsimula
        if (!첫째값) return 동적기억끝;
        if (첫째값 < gumagamit_IMAGE_tapusin || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + laki_ng_pahina - 1) & ~(laki_ng_pahina - 1);
        uintptr_t 새쪽들 = (첫째값 + laki_ng_pahina - 1) & ~(laki_ng_pahina - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t data_posisyon = 이전쪽들; data_posisyon < 새쪽들; data_posisyon += laki_ng_pahina) pagkakalatag_sa_pahina(data_posisyon, kernel_page, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t data_posisyon = 이전쪽들; data_posisyon < 새쪽들; data_posisyon += laki_ng_pahina) pagkakalatag_sa_pahina(data_posisyon, gumagamit_nababasa_nasusulatan, 3);
        } else {
            for (uintptr_t data_posisyon = 새쪽들; data_posisyon < 이전쪽들; data_posisyon += laki_ng_pahina) {
                page_list[(data_posisyon - gumagamit_BASE) / laki_ng_pahina] = 0; Mga_Pahintulot_list[(data_posisyon - gumagamit_BASE) / laki_ng_pahina] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        file_hawakán = 대응파일기술자(첫째값); return file_hawakán < 0 ? -9 : kernel_sukat(pk_size(file_hawakán));
    case 10:
        file_hawakán = 대응파일기술자(첫째값); return file_hawakán < 0 ? -9 : kernel_sukat(pk_ftruncate(file_hawakán, (int64_t)SECOND_VALUE));
    case 11:
        sukat = gumawa_ng_kopya_path(첫째값, path); return sukat ? sukat : kernel_sukat(pk_unlink(path));
    case 12:
        file_hawakán = 대응파일기술자(첫째값); return file_hawakán < 0 ? -9 : kernel_sukat(pk_fsync(file_hawakán));
    case 13: { // 그래픽 기초 API: gumagamit 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = file_pagpasok->magrehistro_data[3], 높이값 = file_pagpasok->magrehistro_data[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SECOND_VALUE > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - SECOND_VALUE) return -22;
        for (uintptr_t Y_button_coordinate = SECOND_VALUE; Y_button_coordinate < SECOND_VALUE + 높이값; Y_button_coordinate++) for (uintptr_t x_coordinate = 첫째값; x_coordinate < 첫째값 + 너비값; x_coordinate++) board_pel(x_coordinate, Y_button_coordinate, character_code);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=item_COUNT; args(index,buffer,capacity)=UTF-8 haba_VALUE
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (character_code <= 전달인수길이[첫째값]) return -36;
        if (!사용자범위(SECOND_VALUE, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SECOND_VALUE, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;tumutugon_interactive=1;return board_Terminal(13);}
        if(첫째값==2){tumutugon_interactive=0;return 0;}
        if(첫째값==3)return board_Terminal(13);
        if(첫째값!=1||!tumutugon_interactive)return -22;
        sukat=(int32_t)보드글자읽기();
        if(sukat==-4096)return sukat;
        Start_TIMEOUT();return sukat<0?-11:sukat;
    case 17: { // 유한한 협력 maghintay_VALUE: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t tapusin_TIME = Orasan_VALUE() + FREQUENCY * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Orasan_VALUE() < tapusin_TIME);
        Start_TIMEOUT(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 부모·빈 폴더를 검사한다.
        if (SECOND_VALUE > 2) return -22;
        sukat = gumawa_ng_kopya_path(첫째값, path); if (sukat) return sukat;
        unsigned haba_VALUE = 0; while (path[haba_VALUE]) haba_VALUE++;
        sukat = 자바경로시작(haba_VALUE); if (sukat < 0) return sukat;
        for (unsigned 순번 = 0; 순번 < haba_VALUE; 순번++) 자바경로바이트(순번, (unsigned char)path[순번]);
        return SECOND_VALUE == 0 ? 자바항목종류() : SECOND_VALUE == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int karakter_VALUE=(int32_t)보드글자읽기();if(karakter_VALUE==-4096)return karakter_VALUE;if(karakter_VALUE>=0)화면누름(may_ari_bagay,karakter_VALUE);Start_TIMEOUT();}
        if(첫째값==3&&character_code){if(!자바셸대화형())return -95;tumutugon_interactive=1;board_Terminal(300);}
        return 화면호출(may_ari_bagay,첫째값,SECOND_VALUE,character_code,file_pagpasok->magrehistro_data[3],file_pagpasok->magrehistro_data[4],file_pagpasok->magrehistro_data[5]);
    case 21:
        if(character_code>127)return -22;if(!사용자범위(SECOND_VALUE,character_code*sizeof(uint32_t),0))return -14;
        return 화면글(may_ari_bagay,첫째값,(const uint32_t *)SECOND_VALUE,character_code);
    case 22: // 화면 sukat_82232621 query_VALUE: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SECOND_VALUE==SOCK_STREAM&&(character_code==0||character_code==6))sukat=자바흐름만들기();
        else if(SECOND_VALUE==SOCK_DGRAM&&(character_code==0||character_code==IPPROTO_UDP))sukat=자바전문만들기(첫째값,SECOND_VALUE,character_code);
        else return -93;
        if (sukat >= 32 && sukat < 56) 통신끝점들[sukat - 32] = 1;
        return sukat;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in email;
        sukat = 주소입력(SECOND_VALUE, character_code, &email); if (sukat) return sukat;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(email.sin_addr.s_addr),pk_htons(email.sin_port)):자바전문묶기(첫째값, pk_htonl(email.sin_addr.s_addr), pk_htons(email.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (file_pagpasok->magrehistro_data[3]) return -95;
        if (character_code > 512) return -90;
        if (character_code && !사용자범위(SECOND_VALUE, character_code, 0)) return -14;
        struct pk_sockaddr_in email;
        sukat = 주소입력(file_pagpasok->magrehistro_data[4], file_pagpasok->magrehistro_data[5], &email); if (sukat) return sukat;
        for (unsigned 순번 = 0; 순번 < character_code; 순번++) 자바전문넣기(순번, ((const unsigned char *)SECOND_VALUE)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(email.sin_addr.s_addr), pk_htons(email.sin_port), character_code);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (file_pagpasok->magrehistro_data[3]) return -95;
        if (character_code > 512) return -90;
        if (character_code && !사용자범위(SECOND_VALUE, character_code, 1)) return -14;
        pk_socklen_t 수용량 = 0;
        if (file_pagpasok->magrehistro_data[4]) { sukat = 주소출력검사(file_pagpasok->magrehistro_data[4], file_pagpasok->magrehistro_data[5], &수용량); if (sukat) return sukat; }
        sukat = 자바전문받기(첫째값, character_code); if (sukat < 0) return sukat;
        for (int 순번 = 0; 순번 < sukat; 순번++) ((unsigned char *)SECOND_VALUE)[순번] = 자바전문얻기(순번);
        if (file_pagpasok->magrehistro_data[4]) 주소출력(file_pagpasok->magrehistro_data[4], file_pagpasok->magrehistro_data[5], 수용량, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return sukat;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t 수용량;
        sukat = 주소출력검사(SECOND_VALUE, character_code, &수용량); if (sukat) return sukat;
        주소출력(SECOND_VALUE,character_code,수용량,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in email;
        sukat=주소입력(SECOND_VALUE,character_code,&email);if(sukat)return sukat;
        return 자바흐름연결(첫째값,pk_htonl(email.sin_addr.s_addr),pk_htons(email.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,SECOND_VALUE):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(SECOND_VALUE||character_code)return -95;sukat=자바흐름연결받기(첫째값);if(sukat>=40&&sukat<56)통신끝점들[sukat-32]=1;return sukat;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(gumagamit_frame *file_pagpasok) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(file_pagpasok) : 자체체계호출(file_pagpasok);
}
static void 커널돌아가기(gumagamit_frame *file_pagpasok, int sukat) {
    Hinto_TIMEOUT();
    file_pagpasok->magrehistro_data[0] = (uint64_t)(int64_t)sukat;
    file_pagpasok->utos_posisyon = (uintptr_t)사용자복귀;
    file_pagpasok->katayuan_CODE = 0x3c5; // EL1h, DAIF masked
}
int gumagamit_pagbubukod(gumagamit_frame *file_pagpasok, unsigned INTERCEPT) {
    if (!Aktibo || (file_pagpasok->katayuan_CODE & 15) != 0) return 0;
    if (INTERCEPT) {
        uint32_t 승인값 = machine_magrehistro(IRQ_CPU_interface + 0xc), tagakilala_VALUE = 승인값 & 1023;
        if (tagakilala_VALUE == 30) { 커널돌아가기(file_pagpasok, gumagamit_TIMEOUT); machine_magrehistro(IRQ_CPU_interface + 0x10) = 승인값; return 1; }
        if (tagakilala_VALUE < 1020) machine_magrehistro(IRQ_CPU_interface + 0x10) = 승인값;
        return 1;
    }
    uint64_t pagbubukod_katayuan; __asm__ volatile("mrs %0, esr_el1" : "=r"(pagbubukod_katayuan));
    if (Orasan_VALUE() >= 마감시각) { 커널돌아가기(file_pagpasok, gumagamit_TIMEOUT); return 1; }
    unsigned pagbubukod_kategorya = pagbubukod_katayuan >> 26;
    if (pagbubukod_kategorya == 0x15 && (pagbubukod_katayuan & 0xffff) == 0) {
        if (리눅스규약 ? file_pagpasok->magrehistro_data[8] == 93 || file_pagpasok->magrehistro_data[8] == 94 : file_pagpasok->magrehistro_data[8] == 6) 커널돌아가기(file_pagpasok, (int)(file_pagpasok->magrehistro_data[0] & 255));
        else {
            intptr_t sukat=체계호출(file_pagpasok);
            if(sukat==-4096&&tumutugon_interactive){
                저장값[may_ari_bagay].실행틀=*file_pagpasok;저장값[may_ari_bagay].실행틀.utos_posisyon-=4;
                사용자실수보관(저장값[may_ari_bagay].실수저장상태);커널돌아가기(file_pagpasok,사용자중단됨);
            }else file_pagpasok->magrehistro_data[0]=(uint64_t)sukat;
        }
    } else 커널돌아가기(file_pagpasok, pagbubukod_kategorya == 0x24 ? gumagamit_data_error : pagbubukod_kategorya == 0x20 ? 사용자실행오류 : gumagamit_hindi_tama_instruksiyon);
    return 1;
}

// 생성된 const ELF Grupo_VALUE: 실행은 반드시 app_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *data; size_t sukat_82232621; unsigned 전달값; } app;
#include "programs.h"
static void *snapshot(unsigned posisyon_INDEX){return (void *)(0x04000000ul+posisyon_INDEX*(gumagamit_tapusin-gumagamit_BASE));}
static int Tapos_Na_app(int sukat){
    사용자누적시각[may_ari_bagay]+=(uint32_t)보드밀리초()-사용자실행시각[may_ari_bagay];
    Hinto_TIMEOUT();Aktibo=0;
    if(sukat==사용자중단됨){
        저장된작업 *string_data=&저장값[may_ari_bagay];string_data->멈춤상태=1;string_data->tumutugon_interactive=tumutugon_interactive;string_data->리눅스규약=리눅스규약;string_data->동적기억공간=동적기억끝;string_data->인수개수=전달인수개수;
        memcpy(string_data->Mga_Pahintulot_list,Mga_Pahintulot_list,sizeof(Mga_Pahintulot_list));memcpy(string_data->file_list,file_list,sizeof(file_list));memcpy(string_data->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(string_data->argumento_ARRAY,전달인수,sizeof(전달인수));memcpy(string_data->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<gumagamit_page_COUNT;순번++)if(Mga_Pahintulot_list[순번])memcpy((unsigned char *)snapshot(may_ari_bagay)+순번*laki_ng_pahina,(void *)(gumagamit_BASE+순번*laki_ng_pahina),laki_ng_pahina);
    }else{
        저장값[may_ari_bagay].멈춤상태=0;화면초기화(may_ari_bagay);
        for(unsigned 순번=0;순번<16;순번++)if(file_list[순번]>=0)pk_close(file_list[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<gumagamit_page_COUNT;순번++){page_list[순번]=0;Mga_Pahintulot_list[순번]=0;}변환표맞추기();return sukat;
}
uintptr_t board_user_control(uintptr_t aksyon){
    unsigned posisyon_INDEX=aksyon&15;if(posisyon_INDEX>=4||Aktibo)return (uint32_t)-22;
    저장된작업 *string_data=&저장값[posisyon_INDEX];
    if(aksyon>=32){if(string_data->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(string_data->file_list[순번]>=0)pk_close(string_data->file_list[순번]);for(unsigned 순번=0;순번<24;순번++)if(string_data->통신끝점들[순번])통신끝점닫기(순번+32);}string_data->멈춤상태=0;화면초기화(posisyon_INDEX);return 0;}
    if(aksyon>=16)return string_data->멈춤상태;
    if(!string_data->멈춤상태)return (uint32_t)-22;
    may_ari_bagay=posisyon_INDEX;tumutugon_interactive=string_data->tumutugon_interactive;리눅스규약=string_data->리눅스규약;동적기억끝=string_data->동적기억공간;전달인수개수=string_data->인수개수;
    memcpy(file_list,string_data->file_list,sizeof(file_list));memcpy(통신끝점들,string_data->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,string_data->argumento_ARRAY,sizeof(전달인수));memcpy(전달인수길이,string_data->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<gumagamit_page_COUNT;순번++)page_list[순번]=(gumagamit_BASE+순번*laki_ng_pahina)|kernel_page;변환표맞추기();
    memset((void *)gumagamit_BASE,0,gumagamit_tapusin-gumagamit_BASE);
    for(unsigned 순번=0;순번<gumagamit_page_COUNT;순번++)if(string_data->Mga_Pahintulot_list[순번])memcpy((void *)(gumagamit_BASE+순번*laki_ng_pahina),(unsigned char *)snapshot(posisyon_INDEX)+순번*laki_ng_pahina,laki_ng_pahina);
    memcpy(Mga_Pahintulot_list,string_data->Mga_Pahintulot_list,sizeof(Mga_Pahintulot_list));
    for(unsigned 순번=0;순번<gumagamit_page_COUNT;순번++){unsigned data_posisyon=Mga_Pahintulot_list[순번];page_list[순번]=data_posisyon?(gumagamit_BASE+순번*laki_ng_pahina)|(data_posisyon==3?gumagamit_nababasa_nasusulatan:data_posisyon==5?사용자읽고실행:gumagamit_mababasa_lamang):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");Aktibo=1;string_data->멈춤상태=0;Start_TIMEOUT();
    사용자실행시각[may_ari_bagay]=보드밀리초();
    return (uint32_t)Tapos_Na_app(gumagamit_CV(&string_data->실행틀,string_data->실수저장상태));
}
static int run_app(const unsigned char *data, size_t sukat_82232621, unsigned 전달값, int 리눅스방식, const char *pangalan) {
    if (Aktibo) return -16;
    may_ari_bagay=board_Terminal(11);if(may_ari_bagay<0||may_ari_bagay>3||저장값[may_ari_bagay].멈춤상태)return -16;tumutugon_interactive=0;
    int 유효함 = 실행파일검사(data, sukat_82232621, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned pangalan_INDEX=0;
    while (*pangalan && pangalan_INDEX<31) gumagamit_utos_pangalan[may_ari_bagay][pangalan_INDEX++]=(unsigned char)*pangalan++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (pangalan_INDEX) gumagamit_utos_pangalan[may_ari_bagay][pangalan_INDEX++]=' ';
        for (unsigned posisyon_INDEX=0; posisyon_INDEX<전달인수길이[0]; posisyon_INDEX++) gumagamit_utos_pangalan[may_ari_bagay][pangalan_INDEX++]=전달인수[0][posisyon_INDEX];
    }
    gumagamit_utos_pangalan[may_ari_bagay][pangalan_INDEX]=0; user_number[may_ari_bagay]=Susunod_user_number++;
    if (Susunod_user_number>0x7fffffffu) Susunod_user_number=10;
    gumagamit_Start_TIME[may_ari_bagay]=보드밀리초(); 사용자누적시각[may_ari_bagay]=0;
    for (unsigned 순번 = 0; 순번 < gumagamit_page_COUNT; 순번++) page_list[순번] = (gumagamit_BASE + 순번 * laki_ng_pahina) | kernel_page;
    변환표맞추기();
    memset((void *)gumagamit_BASE, 0, gumagamit_tapusin - gumagamit_BASE);
    memset(Mga_Pahintulot_list, 0, sizeof(Mga_Pahintulot_list));
    실행파일머리 실행머리; memcpy(&실행머리, data, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.app_Header_COUNT; 순번++) {
        실행파일구획 data_posisyon; memcpy(&data_posisyon, data + 실행머리.app_Header_OFFSET + 순번 * sizeof(data_posisyon), sizeof(data_posisyon));
        if (data_posisyon.TYPE_kategorya != 1 || !data_posisyon.기억영역크기) continue;
        if (data_posisyon.파일영역크기) memcpy((void *)(uintptr_t)data_posisyon.email, data + data_posisyon.OFFSET_VALUE, data_posisyon.파일영역크기);
        for (uintptr_t 현재위치 = data_posisyon.email & ~(laki_ng_pahina - 1); 현재위치 < data_posisyon.email + data_posisyon.기억영역크기; 현재위치 += laki_ng_pahina) {
            Mga_Pahintulot_list[(현재위치 - gumagamit_BASE) / laki_ng_pahina] = (data_posisyon.kompigurasyon_Background_Intelligent_Transfer_Service & 2) ? 3 : ((data_posisyon.kompigurasyon_Background_Intelligent_Transfer_Service & 1) ? 5 : 1);
        }
    }
    for (uintptr_t 현재위치 = gumagamit_Stack_email; 현재위치 < gumagamit_tapusin; 현재위치 += laki_ng_pahina) Mga_Pahintulot_list[(현재위치 - gumagamit_BASE) / laki_ng_pahina] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.pagpasok_point) : gumagamit_tapusin;
    for (unsigned 순번 = 0; 순번 < gumagamit_page_COUNT; 순번++) {
        unsigned mga_pahintulot = Mga_Pahintulot_list[순번];
        page_list[순번] = mga_pahintulot ? (gumagamit_BASE + 순번 * laki_ng_pahina) | (mga_pahintulot == 3 ? gumagamit_nababasa_nasusulatan : mga_pahintulot == 5 ? 사용자읽고실행 : gumagamit_mababasa_lamang) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) file_list[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = gumagamit_IMAGE_tapusin;
    Aktibo = 1; Start_TIMEOUT();
    사용자실행시각[may_ari_bagay]=보드밀리초();
    int sukat = gumagamit_magpasok(실행머리.pagpasok_point, 초기쌓임공간, 전달값);
    return Tapos_Na_app(sukat);
}
uintptr_t board_gumagamit_run(uintptr_t LOOKUP_INDEX) {
    if (LOOKUP_INDEX >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *pangalan=LOOKUP_INDEX==10?"javac":LOOKUP_INDEX==11?"java":LOOKUP_INDEX==12?"python":LOOKUP_INDEX==13?"vi":LOOKUP_INDEX==14?"jar":LOOKUP_INDEX==15?"cc":LOOKUP_INDEX==16?"jaot":"ELF";
    return (uint32_t)run_app(실행항목들[LOOKUP_INDEX].data, 실행항목들[LOOKUP_INDEX].sukat_82232621, 실행항목들[LOOKUP_INDEX].전달값, 0, pangalan);
}
static uintptr_t Mag_execute_file(int 리눅스방식) {
    static unsigned char IMAGE[16384];
    if (Aktibo || !전달인수개수) return (uint32_t)-22;
    int file_hawakán = pk_open((const char *)전달인수[0], mababasa_lamang_VALUE, 0);
    if (file_hawakán < 0) return (uint32_t)-오류번호;
    int sukat_82232621 = pk_size(file_hawakán);
    if (sukat_82232621 < 0 || (unsigned)sukat_82232621 > sizeof(IMAGE)) { pk_close(file_hawakán); return (uint32_t)-27; }
    int RECEIVED_COUNT = pk_read(file_hawakán, IMAGE, sukat_82232621); pk_close(file_hawakán);
    if (RECEIVED_COUNT != sukat_82232621) return (uint32_t)-5;
    return (uint32_t)run_app(IMAGE, sukat_82232621, 0, 리눅스방식, "");
}
uintptr_t board_gumagamit_file(void) { return Mag_execute_file(0); }
uintptr_t 보드사용자리눅스파일(void) { return Mag_execute_file(1); }
uintptr_t board_gumagamit_patunayan(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].data, 잘못된실행항목들[순번].sukat_82232621) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
