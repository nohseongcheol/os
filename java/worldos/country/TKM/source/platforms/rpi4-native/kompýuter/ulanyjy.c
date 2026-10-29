#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 ýerine_ýetir_buýruk kompýuter dereje_baha. Faýl maglumat/정책은 기존 AOT Java 커널에 위임한다.
#include "ulanyjy.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../Tor_Desse/Tor_Desse.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define 기계저장기(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_paýlaýjy 0xff841000ul
#define IRQ_CPU_interfeýs 0xff842000ul
#define sahypanyň_ölçegi 4096ul
#define 접근표시 (1ul << 10)
#define 권한실행금지 (1ul << 53)
#define 사용자실행금지 (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | 접근표시)
#define ýadro_sahypa (3ul | 보통기억 | 권한실행금지 | 사용자실행금지)
#define ulanyjy_okalýan_ýazylýan (3ul | 보통기억 | (1ul << 6) | 권한실행금지 | 사용자실행금지)
#define ulanyjy_diňe_okalýan (3ul | 보통기억 | (3ul << 6) | 권한실행금지 | 사용자실행금지)
#define 사용자읽고실행 (3ul | 보통기억 | (3ul << 6) | 권한실행금지)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t 보드화소(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t 보드터미널(uintptr_t);
extern int 터미널대기(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int ulanyjy_CV(ulanyjy_kadr *,void *);
extern void 사용자실수보관(void *);
extern int ulanyjy_giriz(uintptr_t girizmeklik_utuk, uintptr_t Desse_Ammar, uintptr_t 전달값);
extern void 사용자복귀(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t 뿌리주소[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t sahypa_Sanaw[사용자쪽수] __attribute__((aligned(4096)));
static uint8_t rugsatlar_Sanaw[사용자쪽수];
static int işjeň, faýl_Sanaw[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned faýl_ryçag){return faýl_ryçag<40?자바전문닫기(faýl_ryçag):자바흐름닫기(faýl_ryçag);}
static uint64_t 진동수, 마감시각;
static uintptr_t 동적기억끝;
// ýadro_baha 셸이 준비한 UTF-8 인수. EL0에는 synp_baha 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,interaktiw,리눅스규약,faýl_Sanaw[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char argument_ARRAY[8][256],rugsatlar_Sanaw[사용자쪽수];
    uintptr_t 동적기억공간; ulanyjy_kadr 실행틀;
    unsigned char 실수저장상태[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int eýe_obýekt,interaktiw;
static uint32_t ulanyjynyň_belgisi[4], 사용자시작시각[4], 사용자누적시각[4], 사용자실행시각[4], 다음사용자번호=10;
static unsigned char ulanyjy_buýruk_at[4][288];
uint32_t 사용자상태읽기(unsigned girizmeklik_baha, unsigned indeks) {
    unsigned 자리=indeks&3;
    int ýagdaý_baha=(işjeň && eýe_obýekt==(int)자리) ? 1 : 저장값[자리].멈춤상태 ? 2 : 0;
    if (girizmeklik_baha==0) return ýagdaý_baha;
    if (!ýagdaý_baha) return 0;
    if (girizmeklik_baha==1) return ulanyjynyň_belgisi[자리];
    if (girizmeklik_baha==2) {
        unsigned char *쪽들=ýagdaý_baha==1?rugsatlar_Sanaw:저장값[자리].rugsatlar_Sanaw;
        unsigned 쪽수=0; for (unsigned 순번=0; 순번<사용자쪽수; 순번++) if(쪽들[순번]) 쪽수++;
        return 쪽수*4;
    }
    if (girizmeklik_baha==3) return (uint32_t)보드밀리초()-사용자시작시각[자리];
    if (girizmeklik_baha==4) return 사용자누적시각[자리]+(ýagdaý_baha==1?(uint32_t)보드밀리초()-사용자실행시각[자리]:0);
    if (girizmeklik_baha==5) return indeks/4<sizeof(ulanyjy_buýruk_at[0])?ulanyjy_buýruk_at[자리][indeks/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t 항목수) {
    if (işjeň || 항목수 > 8) return (uint32_t)-22;
    전달인수개수 = 항목수;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t 색인, uintptr_t 현재위치, uintptr_t baýt_maglumat) {
    if (işjeň || 색인 >= 전달인수개수 || 현재위치 >= 255 || 현재위치 != 전달인수길이[색인] || !baýt_maglumat || baýt_maglumat > 255)
        return (uint32_t)-22;
    전달인수[색인][현재위치] = baýt_maglumat;
    전달인수길이[색인] = 현재위치 + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t sagat_baha(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void 시간제한멈춤(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    기계저장기(IRQ_paýlaýjy + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void 시간제한시작(void) {
    uint64_t 간격 = 진동수 * 2, mümkinçilik_ber = 1;
    마감시각 = sagat_baha() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(mümkinçilik_ber) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned maglumat_bökde = 0; maglumat_bökde < 4; maglumat_bökde++) {
        뿌리주소[maglumat_bökde] = (uintptr_t)가운데[maglumat_bökde] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t salgy = ((uintptr_t)maglumat_bökde << 30) | ((uintptr_t)순번 << 21);
            가운데[maglumat_bökde][순번] = salgy | 1 | 접근표시 | 사용자실행금지;
            if (salgy >= 0xfc000000ul) 가운데[maglumat_bökde][순번] |= 권한실행금지; // Device-nGnRnE
            else 가운데[maglumat_bökde][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned 둘째값 = 0; 둘째값 < 사용자쪽수 / 512; 둘째값++)
        가운데[0][(사용자바탕 >> 21) + 둘째값] = (uintptr_t)(sahypa_Sanaw + 둘째값 * 512) | 3;
    for (unsigned 순번 = 0; 순번 < 사용자쪽수; 순번++) sahypa_Sanaw[순번] = (사용자바탕 + 순번 * sahypanyň_ölçegi) | ýadro_sahypa;
    uint64_t 기억속성저장값 = 0x4400, salgy_Terjime_dolandyryş = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(기억속성저장값), "r"(salgy_Terjime_dolandyryş), "r"((uintptr_t)뿌리주소) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t 실수저장상태 = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(실수저장상태) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(진동수));
    시간제한멈춤();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 girizmeklik_utuk_baha 때만 Rugsat_ber_baha.
    기계저장기(IRQ_paýlaýjy) = 0;
    기계저장기(IRQ_paýlaýjy + 0x180) = 0xffffffff;
    기계저장기(IRQ_paýlaýjy + 0x80) = 0xffffffff;
    기계저장기(IRQ_paýlaýjy + 0x280) = 1u << 30;
    기계저장기(IRQ_paýlaýjy + 0x41c) = 0x80808080;
    기계저장기(IRQ_paýlaýjy + 0x100) = 1u << 30;
    기계저장기(IRQ_CPU_interfeýs + 4) = 0xff;
    기계저장기(IRQ_CPU_interfeýs + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 수 있다.
    int Gorag = (기계저장기(IRQ_paýlaýjy + 4) & (1u << 10)) != 0;
    기계저장기(IRQ_paýlaýjy) = Gorag ? 1 : 3;
    기계저장기(IRQ_CPU_interfeýs) = Gorag ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t ýaz_kategoriýa, kompýuter_ýaz; uint32_t 판번호;
    uint64_t girizmeklik_utuk, programma_At_Süýşüriş, bölüm_At_Süýşüriş; uint32_t 설정비트;
    uint16_t 실행머리크기, programma_At_girizmeklik_ölçegi_üýtget, 프로그램머리개수, bölüm_At_girizmeklik_ölçegi_üýtget, 구역머리개수, bölüm_at_tablisa_indeks;
} 실행파일머리;
typedef struct { uint32_t ýaz_kategoriýa, 설정비트; uint64_t Süýşüriş_baha, salgy, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(ulanyjy_kadr) == 272, "exception assembly layout");
static int 포함된범위(uint64_t Süýşüriş_baha, uint64_t Ululyk, uint64_t tamamla_Süýşüriş) {
    return Süýşüriş_baha <= tamamla_Süýşüriş && Ululyk <= tamamla_Süýşüriş - Süýşüriş_baha;
}
static int 부가정보검사(const unsigned char *자료위치, size_t Ululyk) {
    size_t 현재위치 = 0;
    while (포함된범위(현재위치, 12, Ululyk)) {
        uint32_t 낱말들[3]; memcpy(낱말들, 자료위치 + 현재위치, 12); 현재위치 += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(현재위치, 이름영역크기, Ululyk) || !포함된범위(현재위치 + 이름영역크기, 설명크기, Ululyk)) return 0;
        const unsigned char Ad[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Ad) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Ad); 순번++) if (자료위치[현재위치 + 순번] != Ad[순번]) 일치 = 0;
        uint32_t 판번호 = 0;
        if (일치) memcpy(&판번호, 자료위치 + 현재위치 + 이름영역크기, 4);
        if (일치 && 판번호 == 1) return 1;
        현재위치 += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *maglumat, size_t Ululyk, int 리눅스방식) {
    if (Ululyk < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, maglumat, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.ýaz_kategoriýa != 2 || 실행머리.kompýuter_ýaz != 183 || 실행머리.판번호 != 1 || 실행머리.설정비트 || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.programma_At_girizmeklik_ölçegi_üýtget != sizeof(실행파일구획) || !실행머리.프로그램머리개수 || 실행머리.프로그램머리개수 > 16 ||
        실행머리.programma_At_Süýşüriş < sizeof(실행머리) || !포함된범위(실행머리.programma_At_Süýşüriş, (uint64_t)실행머리.프로그램머리개수 * sizeof(실행파일구획), Ululyk)) return 사용자실행파일오류;
    uint8_t 사용량[(ulanyjy_surat_tamamla - 사용자바탕) / sahypanyň_ölçegi] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.프로그램머리개수; 순번++) {
        실행파일구획 자료위치; memcpy(&자료위치, maglumat + 실행머리.programma_At_Süýşüriş + 순번 * sizeof(자료위치), sizeof(자료위치));
        if (자료위치.ýaz_kategoriýa == 4) {
            if (!포함된범위(자료위치.Süýşüriş_baha, 자료위치.파일영역크기, Ululyk)) return 사용자실행파일오류;
            if (부가정보검사(maglumat + 자료위치.Süýşüriş_baha, 자료위치.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (자료위치.ýaz_kategoriýa == 0 || 자료위치.ýaz_kategoriýa == 6 || (자료위치.ýaz_kategoriýa == 0x6474e551 && !(자료위치.설정비트 & 1))) continue;
        if (자료위치.ýaz_kategoriýa != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!자료위치.기억영역크기) continue;
        if (자료위치.설정비트 & ~7u || !(자료위치.설정비트 & 4) || (자료위치.설정비트 & 3) == 3 || 자료위치.파일영역크기 > 자료위치.기억영역크기 ||
            (자료위치.파일영역크기 && !포함된범위(자료위치.Süýşüriş_baha, 자료위치.파일영역크기, Ululyk)) || 자료위치.salgy < 사용자바탕 ||
            !포함된범위(자료위치.salgy, 자료위치.기억영역크기, ulanyjy_surat_tamamla) ||
            (!리눅스방식 && ((자료위치.salgy & (sahypanyň_ölçegi - 1)) || (자료위치.Süýşüriş_baha & (sahypanyň_ölçegi - 1)) || 자료위치.맞춤 != sahypanyň_ölçegi)) ||
            (리눅스방식 && (((자료위치.salgy ^ 자료위치.Süýşüriş_baha) & (sahypanyň_ölçegi - 1)) || !자료위치.맞춤 ||
                (자료위치.맞춤 & (자료위치.맞춤 - 1)) || 자료위치.맞춤 > 0x200000 || ((자료위치.salgy ^ 자료위치.Süýşüriş_baha) & (자료위치.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (자료위치.salgy - 사용자바탕) / sahypanyň_ölçegi;
        unsigned 항목수 = ((자료위치.salgy & (sahypanyň_ölçegi - 1)) + 자료위치.기억영역크기 + sahypanyň_ölçegi - 1) / sahypanyň_ölçegi;
        for (unsigned sahypa_baha = 첫항목; sahypa_baha < 첫항목 + 항목수; sahypa_baha++) {
            if (사용량[sahypa_baha]) return 사용자실행파일오류;
            사용량[sahypa_baha] = 1;
        }
        if ((자료위치.설정비트 & 1) && 실행머리.girizmeklik_utuk >= 자료위치.salgy && 실행머리.girizmeklik_utuk < 자료위치.salgy + 자료위치.파일영역크기 && !(실행머리.girizmeklik_utuk & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *maglumat, size_t Ululyk) { return 실행파일검사(maglumat, Ululyk, 0); }
static void sahypadaky_ýerleşiş(uintptr_t salgy, uint64_t 설정비트, unsigned rugsatlar) {
    unsigned 색인 = (salgy - 사용자바탕) / sahypanyň_ölçegi;
    sahypa_Sanaw[색인] = salgy | 설정비트;
    rugsatlar_Sanaw[색인] = rugsatlar;
}
static int 사용자범위(uintptr_t salgy, size_t 항목수, int 쓰는중) {
    if (salgy < 사용자바탕 || !포함된범위(salgy, 항목수, ulanyjy_tamamla)) return 0;
    if (!항목수) return 1;
    unsigned 첫항목 = (salgy - 사용자바탕) / sahypanyň_ölçegi, 마지막 = (salgy + 항목수 - 1 - 사용자바탕) / sahypanyň_ölçegi;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(rugsatlar_Sanaw[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int synp_ýol(uintptr_t salgy, char *Ýol) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!사용자범위(salgy, 1, 0)) return -14;
        Ýol[순번] = *(const char *)salgy++;
        if (!Ýol[순번]) return 0;
    }
    return -36;
}
static intptr_t 커널결과(intptr_t 결과) { return 결과 < 0 ? -오류번호 : 결과; }
static int 대응파일기술자(uint64_t faýl_ryçag) { return faýl_ryçag >= 3 && faýl_ryçag < 19 ? faýl_Sanaw[faýl_ryçag - 3] : -1; }
static int 통신끝점소유(uint64_t faýl_ryçag) { return faýl_ryçag >= 32 && faýl_ryçag < 56 && 통신끝점들[faýl_ryçag - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t dowamlylyk_baha, struct pk_sockaddr_in *salgy) {
    if (dowamlylyk_baha != sizeof(*salgy)) return -22;
    if (!사용자범위(가리킴값, dowamlylyk_baha, 0)) return -14;
    memcpy(salgy, (const void *)가리킴값, sizeof(*salgy));
    return salgy->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t dowamlylyk_görkeziji, pk_socklen_t *수용량) {
    if (!사용자범위(dowamlylyk_görkeziji, sizeof(*수용량), 1)) return -14;
    memcpy(수용량, (const void *)dowamlylyk_görkeziji, sizeof(*수용량));
    if (*수용량 > sizeof(struct pk_sockaddr_in)) *수용량 = sizeof(struct pk_sockaddr_in);
    if (*수용량 && !사용자범위(가리킴값, *수용량, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t dowamlylyk_görkeziji, pk_socklen_t 수용량, int salgy, int 접속번호) {
    struct pk_sockaddr_in baha; memset(&baha, 0, sizeof(baha));
    baha.sin_family = AF_INET; baha.sin_port = pk_htons(접속번호); baha.sin_addr.s_addr = pk_htonl(salgy);
    if (수용량) memcpy((void *)가리킴값, &baha, 수용량);
    pk_socklen_t dowamlylyk_baha = sizeof(baha); memcpy((void *)dowamlylyk_görkeziji, &dowamlylyk_baha, sizeof(dowamlylyk_baha));
}
extern uintptr_t 보드통로(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(ulanyjy_kadr *faýl_girizmeklik) {
    uintptr_t 첫째값 = faýl_girizmeklik->저장기값[0], 둘째값 = faýl_girizmeklik->저장기값[1], nyşanyň_kody = faýl_girizmeklik->저장기값[2];
    char Ýol[65];
    int faýl_ryçag, 결과;
    switch (faýl_girizmeklik->저장기값[8]) {
    case 0: return 1; // 자체 ABI 버전
    case 1: // write: görkeziji 전체를 검사한 Yza_baha 출력/Faýl üýtget_baha
        if (nyşanyň_kody > 65536) return -22;
        if (!사용자범위(둘째값, nyşanyň_kody, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=sagat_baha();
            for (size_t 순번 = 0; 순번 < nyşanyň_kody; 순번++) 보드통로(첫째값, ((const unsigned char *)둘째값)[순번]);
            /* 큰 tty를 그린 ýadro_baha 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(interaktiw){
                마감시각+=sagat_baha()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(마감시각) : "memory");
            }
            return nyşanyň_kody;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t 개수=nyşanyň_kody>512?512:nyşanyň_kody;for(size_t 순번=0;순번<개수;순번++)자바전문넣기(순번,((const unsigned char *)둘째값)[순번]);return 자바흐름쓰기(첫째값,개수);
        }
        faýl_ryçag = 대응파일기술자(첫째값); if (faýl_ryçag < 0) return -9;
        return 커널결과(pk_write(faýl_ryçag, (const void *)둘째값, nyşanyň_kody));
    case 2:
        if (nyşanyň_kody > 65536) return -22;
        if (!사용자범위(둘째값, nyşanyň_kody, 1)) return -14;
        if (첫째값 == 0) {
            size_t 개수 = 0;
            while (개수 < nyşanyň_kody) {
                int nyşan_baha_068c2631 = (int32_t)보드글자읽기(); if (nyşan_baha_068c2631 == -2) return 개수; if (nyşan_baha_068c2631 < 0) break;
                ((unsigned char *)둘째값)[개수++] = nyşan_baha_068c2631;
            }
            return 개수 ? (intptr_t)개수 : (nyşanyň_kody ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            결과=자바흐름읽기(첫째값,nyşanyň_kody>512?512:nyşanyň_kody);if(결과>0)for(int 순번=0;순번<결과;순번++)((unsigned char *)둘째값)[순번]=자바전문얻기(순번);return 결과;
        }
        faýl_ryçag = 대응파일기술자(첫째값); if (faýl_ryçag < 0) return -9;
        return 커널결과(pk_read(faýl_ryçag, (void *)둘째값, nyşanyň_kody));
    case 3:
        결과 = synp_ýol(첫째값, Ýol); if (결과) return 결과;
        if (둘째값 > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (faýl_Sanaw[순번] < 0) {
            faýl_ryçag = pk_open(Ýol, (int)둘째값, 0600);
            if (faýl_ryçag < 0) return -오류번호;
            faýl_Sanaw[순번] = faýl_ryçag; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { 결과 = 통신끝점닫기(첫째값); if (!결과) 통신끝점들[첫째값 - 32] = 0; return 결과; }
        faýl_ryçag = 대응파일기술자(첫째값); if (faýl_ryçag < 0) return -9;
        결과 = pk_close(faýl_ryçag); if (!결과) faýl_Sanaw[첫째값 - 3] = -1;
        return 커널결과(결과);
    case 5:
        faýl_ryçag = 대응파일기술자(첫째값); if (faýl_ryçag < 0) return -9;
        if (nyşanyň_kody > 2) return -22;
        return 커널결과(pk_lseek(faýl_ryçag, (int64_t)둘째값, nyşanyň_kody));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 ulanyjy RW/NX 힙, 새로 노출되는 페이지는 0으로 ulanyşa_taýýarla
        if (!첫째값) return 동적기억끝;
        if (첫째값 < ulanyjy_surat_tamamla || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + sahypanyň_ölçegi - 1) & ~(sahypanyň_ölçegi - 1);
        uintptr_t 새쪽들 = (첫째값 + sahypanyň_ölçegi - 1) & ~(sahypanyň_ölçegi - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t 자료위치 = 이전쪽들; 자료위치 < 새쪽들; 자료위치 += sahypanyň_ölçegi) sahypadaky_ýerleşiş(자료위치, ýadro_sahypa, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t 자료위치 = 이전쪽들; 자료위치 < 새쪽들; 자료위치 += sahypanyň_ölçegi) sahypadaky_ýerleşiş(자료위치, ulanyjy_okalýan_ýazylýan, 3);
        } else {
            for (uintptr_t 자료위치 = 새쪽들; 자료위치 < 이전쪽들; 자료위치 += sahypanyň_ölçegi) {
                sahypa_Sanaw[(자료위치 - 사용자바탕) / sahypanyň_ölçegi] = 0; rugsatlar_Sanaw[(자료위치 - 사용자바탕) / sahypanyň_ölçegi] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        faýl_ryçag = 대응파일기술자(첫째값); return faýl_ryçag < 0 ? -9 : 커널결과(pk_size(faýl_ryçag));
    case 10:
        faýl_ryçag = 대응파일기술자(첫째값); return faýl_ryçag < 0 ? -9 : 커널결과(pk_ftruncate(faýl_ryçag, (int64_t)둘째값));
    case 11:
        결과 = synp_ýol(첫째값, Ýol); return 결과 ? 결과 : 커널결과(pk_unlink(Ýol));
    case 12:
        faýl_ryçag = 대응파일기술자(첫째값); return faýl_ryçag < 0 ? -9 : 커널결과(pk_fsync(faýl_ryçag));
    case 13: { // 그래픽 기초 API: ulanyjy 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = faýl_girizmeklik->저장기값[3], 높이값 = faýl_girizmeklik->저장기값[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || 둘째값 > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - 둘째값) return -22;
        for (uintptr_t 세로좌표 = 둘째값; 세로좌표 < 둘째값 + 높이값; 세로좌표++) for (uintptr_t x_koordinatasy = 첫째값; x_koordinatasy < 첫째값 + 너비값; x_koordinatasy++) 보드화소(x_koordinatasy, 세로좌표, nyşanyň_kody);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=개수; args(index,buffer,capacity)=UTF-8 dowamlylyk_baha
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (nyşanyň_kody <= 전달인수길이[첫째값]) return -36;
        if (!사용자범위(둘째값, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)둘째값, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;interaktiw=1;return 보드터미널(13);}
        if(첫째값==2){interaktiw=0;return 0;}
        if(첫째값==3)return 보드터미널(13);
        if(첫째값!=1||!interaktiw)return -22;
        결과=(int32_t)보드글자읽기();
        if(결과==-4096)return 결과;
        시간제한시작();return 결과<0?-11:결과;
    case 17: { // 유한한 협력 대기: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t 끝시각 = sagat_baha() + 진동수 * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (sagat_baha() < 끝시각);
        시간제한시작(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 부모·빈 폴더를 검사한다.
        if (둘째값 > 2) return -22;
        결과 = synp_ýol(첫째값, Ýol); if (결과) return 결과;
        unsigned dowamlylyk_baha = 0; while (Ýol[dowamlylyk_baha]) dowamlylyk_baha++;
        결과 = 자바경로시작(dowamlylyk_baha); if (결과 < 0) return 결과;
        for (unsigned 순번 = 0; 순번 < dowamlylyk_baha; 순번++) 자바경로바이트(순번, (unsigned char)Ýol[순번]);
        return 둘째값 == 0 ? 자바항목종류() : 둘째값 == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int nyşan_baha_068c2631=(int32_t)보드글자읽기();if(nyşan_baha_068c2631==-4096)return nyşan_baha_068c2631;if(nyşan_baha_068c2631>=0)화면누름(eýe_obýekt,nyşan_baha_068c2631);시간제한시작();}
        if(첫째값==3&&nyşanyň_kody){if(!자바셸대화형())return -95;interaktiw=1;보드터미널(300);}
        return 화면호출(eýe_obýekt,첫째값,둘째값,nyşanyň_kody,faýl_girizmeklik->저장기값[3],faýl_girizmeklik->저장기값[4],faýl_girizmeklik->저장기값[5]);
    case 21:
        if(nyşanyň_kody>127)return -22;if(!사용자범위(둘째값,nyşanyň_kody*sizeof(uint32_t),0))return -14;
        return 화면글(eýe_obýekt,첫째값,(const uint32_t *)둘째값,nyşanyň_kody);
    case 22: // 화면 Ululyk talap_baha: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(둘째값==SOCK_STREAM&&(nyşanyň_kody==0||nyşanyň_kody==6))결과=자바흐름만들기();
        else if(둘째값==SOCK_DGRAM&&(nyşanyň_kody==0||nyşanyň_kody==IPPROTO_UDP))결과=자바전문만들기(첫째값,둘째값,nyşanyň_kody);
        else return -93;
        if (결과 >= 32 && 결과 < 56) 통신끝점들[결과 - 32] = 1;
        return 결과;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in salgy;
        결과 = 주소입력(둘째값, nyşanyň_kody, &salgy); if (결과) return 결과;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(salgy.sin_addr.s_addr),pk_htons(salgy.sin_port)):자바전문묶기(첫째값, pk_htonl(salgy.sin_addr.s_addr), pk_htons(salgy.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (faýl_girizmeklik->저장기값[3]) return -95;
        if (nyşanyň_kody > 512) return -90;
        if (nyşanyň_kody && !사용자범위(둘째값, nyşanyň_kody, 0)) return -14;
        struct pk_sockaddr_in salgy;
        결과 = 주소입력(faýl_girizmeklik->저장기값[4], faýl_girizmeklik->저장기값[5], &salgy); if (결과) return 결과;
        for (unsigned 순번 = 0; 순번 < nyşanyň_kody; 순번++) 자바전문넣기(순번, ((const unsigned char *)둘째값)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(salgy.sin_addr.s_addr), pk_htons(salgy.sin_port), nyşanyň_kody);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (faýl_girizmeklik->저장기값[3]) return -95;
        if (nyşanyň_kody > 512) return -90;
        if (nyşanyň_kody && !사용자범위(둘째값, nyşanyň_kody, 1)) return -14;
        pk_socklen_t 수용량 = 0;
        if (faýl_girizmeklik->저장기값[4]) { 결과 = 주소출력검사(faýl_girizmeklik->저장기값[4], faýl_girizmeklik->저장기값[5], &수용량); if (결과) return 결과; }
        결과 = 자바전문받기(첫째값, nyşanyň_kody); if (결과 < 0) return 결과;
        for (int 순번 = 0; 순번 < 결과; 순번++) ((unsigned char *)둘째값)[순번] = 자바전문얻기(순번);
        if (faýl_girizmeklik->저장기값[4]) 주소출력(faýl_girizmeklik->저장기값[4], faýl_girizmeklik->저장기값[5], 수용량, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return 결과;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t 수용량;
        결과 = 주소출력검사(둘째값, nyşanyň_kody, &수용량); if (결과) return 결과;
        주소출력(둘째값,nyşanyň_kody,수용량,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in salgy;
        결과=주소입력(둘째값,nyşanyň_kody,&salgy);if(결과)return 결과;
        return 자바흐름연결(첫째값,pk_htonl(salgy.sin_addr.s_addr),pk_htons(salgy.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,둘째값):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(둘째값||nyşanyň_kody)return -95;결과=자바흐름연결받기(첫째값);if(결과>=40&&결과<56)통신끝점들[결과-32]=1;return 결과;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(ulanyjy_kadr *faýl_girizmeklik) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(faýl_girizmeklik) : 자체체계호출(faýl_girizmeklik);
}
static void 커널돌아가기(ulanyjy_kadr *faýl_girizmeklik, int 결과) {
    시간제한멈춤();
    faýl_girizmeklik->저장기값[0] = (uint64_t)(int64_t)결과;
    faýl_girizmeklik->명령위치 = (uintptr_t)사용자복귀;
    faýl_girizmeklik->상태값 = 0x3c5; // EL1h, DAIF masked
}
int 사용자예외(ulanyjy_kadr *faýl_girizmeklik, unsigned 가로채기) {
    if (!işjeň || (faýl_girizmeklik->상태값 & 15) != 0) return 0;
    if (가로채기) {
        uint32_t 승인값 = 기계저장기(IRQ_CPU_interfeýs + 0xc), tanaýjy_baha = 승인값 & 1023;
        if (tanaýjy_baha == 30) { 커널돌아가기(faýl_girizmeklik, 사용자시간초과); 기계저장기(IRQ_CPU_interfeýs + 0x10) = 승인값; return 1; }
        if (tanaýjy_baha < 1020) 기계저장기(IRQ_CPU_interfeýs + 0x10) = 승인값;
        return 1;
    }
    uint64_t 예외상태; __asm__ volatile("mrs %0, esr_el1" : "=r"(예외상태));
    if (sagat_baha() >= 마감시각) { 커널돌아가기(faýl_girizmeklik, 사용자시간초과); return 1; }
    unsigned 예외분류 = 예외상태 >> 26;
    if (예외분류 == 0x15 && (예외상태 & 0xffff) == 0) {
        if (리눅스규약 ? faýl_girizmeklik->저장기값[8] == 93 || faýl_girizmeklik->저장기값[8] == 94 : faýl_girizmeklik->저장기값[8] == 6) 커널돌아가기(faýl_girizmeklik, (int)(faýl_girizmeklik->저장기값[0] & 255));
        else {
            intptr_t 결과=체계호출(faýl_girizmeklik);
            if(결과==-4096&&interaktiw){
                저장값[eýe_obýekt].실행틀=*faýl_girizmeklik;저장값[eýe_obýekt].실행틀.명령위치-=4;
                사용자실수보관(저장값[eýe_obýekt].실수저장상태);커널돌아가기(faýl_girizmeklik,사용자중단됨);
            }else faýl_girizmeklik->저장기값[0]=(uint64_t)결과;
        }
    } else 커널돌아가기(faýl_girizmeklik, 예외분류 == 0x24 ? ulanyjy_maglumat_säwlik : 예외분류 == 0x20 ? 사용자실행오류 : ulanyjy_nädogry_instruksiýa);
    return 1;
}

// 생성된 const ELF topar_baha: 실행은 반드시 programma_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *maglumat; size_t Ululyk; unsigned 전달값; } programma;
#include "programs.h"
static void *kadr_f57035a1(unsigned 자리){return (void *)(0x04000000ul+자리*(ulanyjy_tamamla-사용자바탕));}
static int Tamamla_programma(int 결과){
    사용자누적시각[eýe_obýekt]+=(uint32_t)보드밀리초()-사용자실행시각[eýe_obýekt];
    시간제한멈춤();işjeň=0;
    if(결과==사용자중단됨){
        저장된작업 *setir_maglumat=&저장값[eýe_obýekt];setir_maglumat->멈춤상태=1;setir_maglumat->interaktiw=interaktiw;setir_maglumat->리눅스규약=리눅스규약;setir_maglumat->동적기억공간=동적기억끝;setir_maglumat->인수개수=전달인수개수;
        memcpy(setir_maglumat->rugsatlar_Sanaw,rugsatlar_Sanaw,sizeof(rugsatlar_Sanaw));memcpy(setir_maglumat->faýl_Sanaw,faýl_Sanaw,sizeof(faýl_Sanaw));memcpy(setir_maglumat->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(setir_maglumat->argument_ARRAY,전달인수,sizeof(전달인수));memcpy(setir_maglumat->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<사용자쪽수;순번++)if(rugsatlar_Sanaw[순번])memcpy((unsigned char *)kadr_f57035a1(eýe_obýekt)+순번*sahypanyň_ölçegi,(void *)(사용자바탕+순번*sahypanyň_ölçegi),sahypanyň_ölçegi);
    }else{
        저장값[eýe_obýekt].멈춤상태=0;화면초기화(eýe_obýekt);
        for(unsigned 순번=0;순번<16;순번++)if(faýl_Sanaw[순번]>=0)pk_close(faýl_Sanaw[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<사용자쪽수;순번++){sahypa_Sanaw[순번]=0;rugsatlar_Sanaw[순번]=0;}변환표맞추기();return 결과;
}
uintptr_t 보드사용자제어(uintptr_t iş){
    unsigned 자리=iş&15;if(자리>=4||işjeň)return (uint32_t)-22;
    저장된작업 *setir_maglumat=&저장값[자리];
    if(iş>=32){if(setir_maglumat->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(setir_maglumat->faýl_Sanaw[순번]>=0)pk_close(setir_maglumat->faýl_Sanaw[순번]);for(unsigned 순번=0;순번<24;순번++)if(setir_maglumat->통신끝점들[순번])통신끝점닫기(순번+32);}setir_maglumat->멈춤상태=0;화면초기화(자리);return 0;}
    if(iş>=16)return setir_maglumat->멈춤상태;
    if(!setir_maglumat->멈춤상태)return (uint32_t)-22;
    eýe_obýekt=자리;interaktiw=setir_maglumat->interaktiw;리눅스규약=setir_maglumat->리눅스규약;동적기억끝=setir_maglumat->동적기억공간;전달인수개수=setir_maglumat->인수개수;
    memcpy(faýl_Sanaw,setir_maglumat->faýl_Sanaw,sizeof(faýl_Sanaw));memcpy(통신끝점들,setir_maglumat->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,setir_maglumat->argument_ARRAY,sizeof(전달인수));memcpy(전달인수길이,setir_maglumat->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<사용자쪽수;순번++)sahypa_Sanaw[순번]=(사용자바탕+순번*sahypanyň_ölçegi)|ýadro_sahypa;변환표맞추기();
    memset((void *)사용자바탕,0,ulanyjy_tamamla-사용자바탕);
    for(unsigned 순번=0;순번<사용자쪽수;순번++)if(setir_maglumat->rugsatlar_Sanaw[순번])memcpy((void *)(사용자바탕+순번*sahypanyň_ölçegi),(unsigned char *)kadr_f57035a1(자리)+순번*sahypanyň_ölçegi,sahypanyň_ölçegi);
    memcpy(rugsatlar_Sanaw,setir_maglumat->rugsatlar_Sanaw,sizeof(rugsatlar_Sanaw));
    for(unsigned 순번=0;순번<사용자쪽수;순번++){unsigned 자료위치=rugsatlar_Sanaw[순번];sahypa_Sanaw[순번]=자료위치?(사용자바탕+순번*sahypanyň_ölçegi)|(자료위치==3?ulanyjy_okalýan_ýazylýan:자료위치==5?사용자읽고실행:ulanyjy_diňe_okalýan):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");işjeň=1;setir_maglumat->멈춤상태=0;시간제한시작();
    사용자실행시각[eýe_obýekt]=보드밀리초();
    return (uint32_t)Tamamla_programma(ulanyjy_CV(&setir_maglumat->실행틀,setir_maglumat->실수저장상태));
}
static int işe_goýber_programma(const unsigned char *maglumat, size_t Ululyk, unsigned 전달값, int 리눅스방식, const char *Ad) {
    if (işjeň) return -16;
    eýe_obýekt=보드터미널(11);if(eýe_obýekt<0||eýe_obýekt>3||저장값[eýe_obýekt].멈춤상태)return -16;interaktiw=0;
    int 유효함 = 실행파일검사(maglumat, Ululyk, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned at_indeks=0;
    while (*Ad && at_indeks<31) ulanyjy_buýruk_at[eýe_obýekt][at_indeks++]=(unsigned char)*Ad++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (at_indeks) ulanyjy_buýruk_at[eýe_obýekt][at_indeks++]=' ';
        for (unsigned 자리=0; 자리<전달인수길이[0]; 자리++) ulanyjy_buýruk_at[eýe_obýekt][at_indeks++]=전달인수[0][자리];
    }
    ulanyjy_buýruk_at[eýe_obýekt][at_indeks]=0; ulanyjynyň_belgisi[eýe_obýekt]=다음사용자번호++;
    if (다음사용자번호>0x7fffffffu) 다음사용자번호=10;
    사용자시작시각[eýe_obýekt]=보드밀리초(); 사용자누적시각[eýe_obýekt]=0;
    for (unsigned 순번 = 0; 순번 < 사용자쪽수; 순번++) sahypa_Sanaw[순번] = (사용자바탕 + 순번 * sahypanyň_ölçegi) | ýadro_sahypa;
    변환표맞추기();
    memset((void *)사용자바탕, 0, ulanyjy_tamamla - 사용자바탕);
    memset(rugsatlar_Sanaw, 0, sizeof(rugsatlar_Sanaw));
    실행파일머리 실행머리; memcpy(&실행머리, maglumat, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.프로그램머리개수; 순번++) {
        실행파일구획 자료위치; memcpy(&자료위치, maglumat + 실행머리.programma_At_Süýşüriş + 순번 * sizeof(자료위치), sizeof(자료위치));
        if (자료위치.ýaz_kategoriýa != 1 || !자료위치.기억영역크기) continue;
        if (자료위치.파일영역크기) memcpy((void *)(uintptr_t)자료위치.salgy, maglumat + 자료위치.Süýşüriş_baha, 자료위치.파일영역크기);
        for (uintptr_t 현재위치 = 자료위치.salgy & ~(sahypanyň_ölçegi - 1); 현재위치 < 자료위치.salgy + 자료위치.기억영역크기; 현재위치 += sahypanyň_ölçegi) {
            rugsatlar_Sanaw[(현재위치 - 사용자바탕) / sahypanyň_ölçegi] = (자료위치.설정비트 & 2) ? 3 : ((자료위치.설정비트 & 1) ? 5 : 1);
        }
    }
    for (uintptr_t 현재위치 = ulanyjy_Desse_salgy; 현재위치 < ulanyjy_tamamla; 현재위치 += sahypanyň_ölçegi) rugsatlar_Sanaw[(현재위치 - 사용자바탕) / sahypanyň_ölçegi] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.girizmeklik_utuk) : ulanyjy_tamamla;
    for (unsigned 순번 = 0; 순번 < 사용자쪽수; 순번++) {
        unsigned rugsatlar = rugsatlar_Sanaw[순번];
        sahypa_Sanaw[순번] = rugsatlar ? (사용자바탕 + 순번 * sahypanyň_ölçegi) | (rugsatlar == 3 ? ulanyjy_okalýan_ýazylýan : rugsatlar == 5 ? 사용자읽고실행 : ulanyjy_diňe_okalýan) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) faýl_Sanaw[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = ulanyjy_surat_tamamla;
    işjeň = 1; 시간제한시작();
    사용자실행시각[eýe_obýekt]=보드밀리초();
    int 결과 = ulanyjy_giriz(실행머리.girizmeklik_utuk, 초기쌓임공간, 전달값);
    return Tamamla_programma(결과);
}
uintptr_t 보드사용자실행(uintptr_t 색인) {
    if (색인 >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Ad=색인==10?"javac":색인==11?"java":색인==12?"python":색인==13?"vi":색인==14?"jar":색인==15?"cc":색인==16?"jaot":"ELF";
    return (uint32_t)işe_goýber_programma(실행항목들[색인].maglumat, 실행항목들[색인].Ululyk, 실행항목들[색인].전달값, 0, Ad);
}
static uintptr_t ýerine_ýetir_faýl(int 리눅스방식) {
    static unsigned char surat[16384];
    if (işjeň || !전달인수개수) return (uint32_t)-22;
    int faýl_ryçag = pk_open((const char *)전달인수[0], diňe_okalýan_baha, 0);
    if (faýl_ryçag < 0) return (uint32_t)-오류번호;
    int Ululyk = pk_size(faýl_ryçag);
    if (Ululyk < 0 || (unsigned)Ululyk > sizeof(surat)) { pk_close(faýl_ryçag); return (uint32_t)-27; }
    int 받은수 = pk_read(faýl_ryçag, surat, Ululyk); pk_close(faýl_ryçag);
    if (받은수 != Ululyk) return (uint32_t)-5;
    return (uint32_t)işe_goýber_programma(surat, Ululyk, 0, 리눅스방식, "");
}
uintptr_t 보드사용자파일(void) { return ýerine_ýetir_faýl(0); }
uintptr_t 보드사용자리눅스파일(void) { return ýerine_ýetir_faýl(1); }
uintptr_t 보드사용자검사(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].maglumat, 잘못된실행항목들[순번].Ululyk) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
