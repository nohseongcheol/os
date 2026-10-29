#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 ukwenza_umyalelo umatshini ileya_ixabiso. iFayili iingcombolo/정책은 기존 AOT Java 커널에 위임한다.
#include "umsebenzisi.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../Inethiwekhi_fumba/Inethiwekhi_fumba.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define umatshini_bhalisa(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define i_IRQ_umhambisi 0xff841000ul
#define i_IRQ_i_CPU_isinxulumanisi 0xff842000ul
#define ubungakanani_bekhasi 4096ul
#define 접근표시 (1ul << 10)
#define 권한실행금지 (1ul << 53)
#define 사용자실행금지 (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | 접근표시)
#define ikheneli_ikhasi (3ul | 보통기억 | 권한실행금지 | 사용자실행금지)
#define umsebenzisi_funda_bhala (3ul | 보통기억 | (1ul << 6) | 권한실행금지 | 사용자실행금지)
#define umsebenzisi_efundwayo_kuphela (3ul | 보통기억 | (3ul << 6) | 권한실행금지 | 사용자실행금지)
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
extern int umsebenzisi_i_CV(umsebenzisi_ifreyim *,void *);
extern void 사용자실수보관(void *);
extern int umsebenzisi_ngenisa(uintptr_t ufako_nkcukacha_inqaku, uintptr_t fumba_Ugcino, uintptr_t 전달값);
extern void 사용자복귀(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t 뿌리주소[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t ikhasi_uludwe[사용자쪽수] __attribute__((aligned(4096)));
static uint8_t iimvume_uludwe[사용자쪽수];
static int edlamkileyo, ifayile_uludwe[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned ifayile_isibambi){return ifayile_isibambi<40?자바전문닫기(ifayile_isibambi):자바흐름닫기(ifayile_isibambi);}
static uint64_t 진동수, 마감시각;
static uintptr_t 동적기억끝;
// ikheneli_ixabiso 셸이 준비한 UTF-8 인수. EL0에는 kopa_ixabiso 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,esebenzisana_nomsebenzi,리눅스규약,ifayile_uludwe[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char isiniki_myalelo_ULUHLU[8][256],iimvume_uludwe[사용자쪽수];
    uintptr_t 동적기억공간; umsebenzisi_ifreyim 실행틀;
    unsigned char 실수저장상태[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int umnini_into,esebenzisana_nomsebenzi;
static uint32_t inombolo_yomsebenzisi[4], 사용자시작시각[4], 사용자누적시각[4], 사용자실행시각[4], 다음사용자번호=10;
static unsigned char umsebenzisi_umyalelo_igama[4][288];
uint32_t 사용자상태읽기(unsigned ufako_nkcukacha_ixabiso, unsigned indeksa) {
    unsigned 자리=indeksa&3;
    int imo_ixabiso=(edlamkileyo && umnini_into==(int)자리) ? 1 : 저장값[자리].멈춤상태 ? 2 : 0;
    if (ufako_nkcukacha_ixabiso==0) return imo_ixabiso;
    if (!imo_ixabiso) return 0;
    if (ufako_nkcukacha_ixabiso==1) return inombolo_yomsebenzisi[자리];
    if (ufako_nkcukacha_ixabiso==2) {
        unsigned char *쪽들=imo_ixabiso==1?iimvume_uludwe:저장값[자리].iimvume_uludwe;
        unsigned 쪽수=0; for (unsigned 순번=0; 순번<사용자쪽수; 순번++) if(쪽들[순번]) 쪽수++;
        return 쪽수*4;
    }
    if (ufako_nkcukacha_ixabiso==3) return (uint32_t)보드밀리초()-사용자시작시각[자리];
    if (ufako_nkcukacha_ixabiso==4) return 사용자누적시각[자리]+(imo_ixabiso==1?(uint32_t)보드밀리초()-사용자실행시각[자리]:0);
    if (ufako_nkcukacha_ixabiso==5) return indeksa/4<sizeof(umsebenzisi_umyalelo_igama[0])?umsebenzisi_umyalelo_igama[자리][indeksa/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t 항목수) {
    if (edlamkileyo || 항목수 > 8) return (uint32_t)-22;
    전달인수개수 = 항목수;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t 색인, uintptr_t 현재위치, uintptr_t ibhayithi_iingcombolo) {
    if (edlamkileyo || 색인 >= 전달인수개수 || 현재위치 >= 255 || 현재위치 != 전달인수길이[색인] || !ibhayithi_iingcombolo || ibhayithi_iingcombolo > 255)
        return (uint32_t)-22;
    전달인수[색인][현재위치] = ibhayithi_iingcombolo;
    전달인수길이[색인] = 현재위치 + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t iwotshi_ixabiso(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void 시간제한멈춤(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    umatshini_bhalisa(i_IRQ_umhambisi + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void 시간제한시작(void) {
    uint64_t 간격 = 진동수 * 2, ukuvula = 1;
    마감시각 = iwotshi_ixabiso() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(ukuvula) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned iingcombolo_thintela = 0; iingcombolo_thintela < 4; iingcombolo_thintela++) {
        뿌리주소[iingcombolo_thintela] = (uintptr_t)가운데[iingcombolo_thintela] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t idilesi = ((uintptr_t)iingcombolo_thintela << 30) | ((uintptr_t)순번 << 21);
            가운데[iingcombolo_thintela][순번] = idilesi | 1 | 접근표시 | 사용자실행금지;
            if (idilesi >= 0xfc000000ul) 가운데[iingcombolo_thintela][순번] |= 권한실행금지; // Device-nGnRnE
            else 가운데[iingcombolo_thintela][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned 둘째값 = 0; 둘째값 < 사용자쪽수 / 512; 둘째값++)
        가운데[0][(사용자바탕 >> 21) + 둘째값] = (uintptr_t)(ikhasi_uludwe + 둘째값 * 512) | 3;
    for (unsigned 순번 = 0; 순번 < 사용자쪽수; 순번++) ikhasi_uludwe[순번] = (사용자바탕 + 순번 * ubungakanani_bekhasi) | ikheneli_ikhasi;
    uint64_t imemori_uphawu_bhalisa = 0x4400, idilesi_Uguqulelo_magama_isilawuli = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(imemori_uphawu_bhalisa), "r"(idilesi_Uguqulelo_magama_isilawuli), "r"((uintptr_t)뿌리주소) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t 실수저장상태 = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(실수저장상태) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(진동수));
    시간제한멈춤();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 ufako_nkcukacha_inqaku_ixabiso 때만 vumela_ixabiso.
    umatshini_bhalisa(i_IRQ_umhambisi) = 0;
    umatshini_bhalisa(i_IRQ_umhambisi + 0x180) = 0xffffffff;
    umatshini_bhalisa(i_IRQ_umhambisi + 0x80) = 0xffffffff;
    umatshini_bhalisa(i_IRQ_umhambisi + 0x280) = 1u << 30;
    umatshini_bhalisa(i_IRQ_umhambisi + 0x41c) = 0x80808080;
    umatshini_bhalisa(i_IRQ_umhambisi + 0x100) = 1u << 30;
    umatshini_bhalisa(i_IRQ_i_CPU_isinxulumanisi + 4) = 0xff;
    umatshini_bhalisa(i_IRQ_i_CPU_isinxulumanisi + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 수 있다.
    int Ukhuseleko = (umatshini_bhalisa(i_IRQ_umhambisi + 4) & (1u << 10)) != 0;
    umatshini_bhalisa(i_IRQ_umhambisi) = Ukhuseleko ? 1 : 3;
    umatshini_bhalisa(i_IRQ_i_CPU_isinxulumanisi) = Ukhuseleko ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t uhlobo_udidi, umatshini_uhlobo; uint32_t 판번호;
    uint64_t ufako_nkcukacha_inqaku, inkqubo_Iheda_Ukulinganisa, icandelo_Iheda_Ukulinganisa; uint32_t 설정비트;
    uint16_t 실행머리크기, inkqubo_Iheda_ufako_nkcukacha_isayizi, 프로그램머리개수, icandelo_Iheda_ufako_nkcukacha_isayizi, 구역머리개수, icandelo_igama_itheyibhile_indeksa;
} 실행파일머리;
typedef struct { uint32_t uhlobo_udidi, 설정비트; uint64_t Ukulinganisa_ixabiso, idilesi, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(umsebenzisi_ifreyim) == 272, "exception assembly layout");
static int 포함된범위(uint64_t Ukulinganisa_ixabiso, uint64_t Ubukhulu, uint64_t phela_Ukulinganisa) {
    return Ukulinganisa_ixabiso <= phela_Ukulinganisa && Ubukhulu <= phela_Ukulinganisa - Ukulinganisa_ixabiso;
}
static int 부가정보검사(const unsigned char *자료위치, size_t Ubukhulu) {
    size_t 현재위치 = 0;
    while (포함된범위(현재위치, 12, Ubukhulu)) {
        uint32_t 낱말들[3]; memcpy(낱말들, 자료위치 + 현재위치, 12); 현재위치 += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(현재위치, 이름영역크기, Ubukhulu) || !포함된범위(현재위치 + 이름영역크기, 설명크기, Ubukhulu)) return 0;
        const unsigned char Igama[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Igama) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Igama); 순번++) if (자료위치[현재위치 + 순번] != Igama[순번]) 일치 = 0;
        uint32_t 판번호 = 0;
        if (일치) memcpy(&판번호, 자료위치 + 현재위치 + 이름영역크기, 4);
        if (일치 && 판번호 == 1) return 1;
        현재위치 += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *iingcombolo, size_t Ubukhulu, int 리눅스방식) {
    if (Ubukhulu < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, iingcombolo, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.uhlobo_udidi != 2 || 실행머리.umatshini_uhlobo != 183 || 실행머리.판번호 != 1 || 실행머리.설정비트 || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.inkqubo_Iheda_ufako_nkcukacha_isayizi != sizeof(실행파일구획) || !실행머리.프로그램머리개수 || 실행머리.프로그램머리개수 > 16 ||
        실행머리.inkqubo_Iheda_Ukulinganisa < sizeof(실행머리) || !포함된범위(실행머리.inkqubo_Iheda_Ukulinganisa, (uint64_t)실행머리.프로그램머리개수 * sizeof(실행파일구획), Ubukhulu)) return 사용자실행파일오류;
    uint8_t 사용량[(umsebenzisi_umfanekiso_phela - 사용자바탕) / ubungakanani_bekhasi] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.프로그램머리개수; 순번++) {
        실행파일구획 자료위치; memcpy(&자료위치, iingcombolo + 실행머리.inkqubo_Iheda_Ukulinganisa + 순번 * sizeof(자료위치), sizeof(자료위치));
        if (자료위치.uhlobo_udidi == 4) {
            if (!포함된범위(자료위치.Ukulinganisa_ixabiso, 자료위치.파일영역크기, Ubukhulu)) return 사용자실행파일오류;
            if (부가정보검사(iingcombolo + 자료위치.Ukulinganisa_ixabiso, 자료위치.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (자료위치.uhlobo_udidi == 0 || 자료위치.uhlobo_udidi == 6 || (자료위치.uhlobo_udidi == 0x6474e551 && !(자료위치.설정비트 & 1))) continue;
        if (자료위치.uhlobo_udidi != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!자료위치.기억영역크기) continue;
        if (자료위치.설정비트 & ~7u || !(자료위치.설정비트 & 4) || (자료위치.설정비트 & 3) == 3 || 자료위치.파일영역크기 > 자료위치.기억영역크기 ||
            (자료위치.파일영역크기 && !포함된범위(자료위치.Ukulinganisa_ixabiso, 자료위치.파일영역크기, Ubukhulu)) || 자료위치.idilesi < 사용자바탕 ||
            !포함된범위(자료위치.idilesi, 자료위치.기억영역크기, umsebenzisi_umfanekiso_phela) ||
            (!리눅스방식 && ((자료위치.idilesi & (ubungakanani_bekhasi - 1)) || (자료위치.Ukulinganisa_ixabiso & (ubungakanani_bekhasi - 1)) || 자료위치.맞춤 != ubungakanani_bekhasi)) ||
            (리눅스방식 && (((자료위치.idilesi ^ 자료위치.Ukulinganisa_ixabiso) & (ubungakanani_bekhasi - 1)) || !자료위치.맞춤 ||
                (자료위치.맞춤 & (자료위치.맞춤 - 1)) || 자료위치.맞춤 > 0x200000 || ((자료위치.idilesi ^ 자료위치.Ukulinganisa_ixabiso) & (자료위치.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (자료위치.idilesi - 사용자바탕) / ubungakanani_bekhasi;
        unsigned 항목수 = ((자료위치.idilesi & (ubungakanani_bekhasi - 1)) + 자료위치.기억영역크기 + ubungakanani_bekhasi - 1) / ubungakanani_bekhasi;
        for (unsigned ikhasi_ixabiso = 첫항목; ikhasi_ixabiso < 첫항목 + 항목수; ikhasi_ixabiso++) {
            if (사용량[ikhasi_ixabiso]) return 사용자실행파일오류;
            사용량[ikhasi_ixabiso] = 1;
        }
        if ((자료위치.설정비트 & 1) && 실행머리.ufako_nkcukacha_inqaku >= 자료위치.idilesi && 실행머리.ufako_nkcukacha_inqaku < 자료위치.idilesi + 자료위치.파일영역크기 && !(실행머리.ufako_nkcukacha_inqaku & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *iingcombolo, size_t Ubukhulu) { return 실행파일검사(iingcombolo, Ubukhulu, 0); }
static void ukuma_kwephepha(uintptr_t idilesi, uint64_t 설정비트, unsigned iimvume) {
    unsigned 색인 = (idilesi - 사용자바탕) / ubungakanani_bekhasi;
    ikhasi_uludwe[색인] = idilesi | 설정비트;
    iimvume_uludwe[색인] = iimvume;
}
static int 사용자범위(uintptr_t idilesi, size_t 항목수, int 쓰는중) {
    if (idilesi < 사용자바탕 || !포함된범위(idilesi, 항목수, umsebenzisi_phela)) return 0;
    if (!항목수) return 1;
    unsigned 첫항목 = (idilesi - 사용자바탕) / ubungakanani_bekhasi, 마지막 = (idilesi + 항목수 - 1 - 사용자바탕) / ubungakanani_bekhasi;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(iimvume_uludwe[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int kopa_indlela(uintptr_t idilesi, char *INDLELA) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!사용자범위(idilesi, 1, 0)) return -14;
        INDLELA[순번] = *(const char *)idilesi++;
        if (!INDLELA[순번]) return 0;
    }
    return -36;
}
static intptr_t 커널결과(intptr_t 결과) { return 결과 < 0 ? -오류번호 : 결과; }
static int 대응파일기술자(uint64_t ifayile_isibambi) { return ifayile_isibambi >= 3 && ifayile_isibambi < 19 ? ifayile_uludwe[ifayile_isibambi - 3] : -1; }
static int 통신끝점소유(uint64_t ifayile_isibambi) { return ifayile_isibambi >= 32 && ifayile_isibambi < 56 && 통신끝점들[ifayile_isibambi - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t ubude_ixabiso, struct pk_sockaddr_in *idilesi) {
    if (ubude_ixabiso != sizeof(*idilesi)) return -22;
    if (!사용자범위(가리킴값, ubude_ixabiso, 0)) return -14;
    memcpy(idilesi, (const void *)가리킴값, sizeof(*idilesi));
    return idilesi->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t ubude_isalathisi, pk_socklen_t *수용량) {
    if (!사용자범위(ubude_isalathisi, sizeof(*수용량), 1)) return -14;
    memcpy(수용량, (const void *)ubude_isalathisi, sizeof(*수용량));
    if (*수용량 > sizeof(struct pk_sockaddr_in)) *수용량 = sizeof(struct pk_sockaddr_in);
    if (*수용량 && !사용자범위(가리킴값, *수용량, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t ubude_isalathisi, pk_socklen_t 수용량, int idilesi, int 접속번호) {
    struct pk_sockaddr_in ixabiso; memset(&ixabiso, 0, sizeof(ixabiso));
    ixabiso.sin_family = AF_INET; ixabiso.sin_port = pk_htons(접속번호); ixabiso.sin_addr.s_addr = pk_htonl(idilesi);
    if (수용량) memcpy((void *)가리킴값, &ixabiso, 수용량);
    pk_socklen_t ubude_ixabiso = sizeof(ixabiso); memcpy((void *)ubude_isalathisi, &ubude_ixabiso, sizeof(ubude_ixabiso));
}
extern uintptr_t 보드통로(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(umsebenzisi_ifreyim *ifayile_ufako_nkcukacha) {
    uintptr_t 첫째값 = ifayile_ufako_nkcukacha->bhalisa_iingcombolo[0], 둘째값 = ifayile_ufako_nkcukacha->bhalisa_iingcombolo[1], ikhowudi_yekharakhtha = ifayile_ufako_nkcukacha->bhalisa_iingcombolo[2];
    char INDLELA[65];
    int ifayile_isibambi, 결과;
    switch (ifayile_ufako_nkcukacha->bhalisa_iingcombolo[8]) {
    case 0: return 1; // 자체 ABI 버전
    case 1: // write: isalathisi 전체를 검사한 Emva_ixabiso 출력/iFayili tshintsha_ixabiso
        if (ikhowudi_yekharakhtha > 65536) return -22;
        if (!사용자범위(둘째값, ikhowudi_yekharakhtha, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=iwotshi_ixabiso();
            for (size_t 순번 = 0; 순번 < ikhowudi_yekharakhtha; 순번++) 보드통로(첫째값, ((const unsigned char *)둘째값)[순번]);
            /* 큰 tty를 그린 ikheneli_ixabiso 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(esebenzisana_nomsebenzi){
                마감시각+=iwotshi_ixabiso()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(마감시각) : "memory");
            }
            return ikhowudi_yekharakhtha;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t 개수=ikhowudi_yekharakhtha>512?512:ikhowudi_yekharakhtha;for(size_t 순번=0;순번<개수;순번++)자바전문넣기(순번,((const unsigned char *)둘째값)[순번]);return 자바흐름쓰기(첫째값,개수);
        }
        ifayile_isibambi = 대응파일기술자(첫째값); if (ifayile_isibambi < 0) return -9;
        return 커널결과(pk_write(ifayile_isibambi, (const void *)둘째값, ikhowudi_yekharakhtha));
    case 2:
        if (ikhowudi_yekharakhtha > 65536) return -22;
        if (!사용자범위(둘째값, ikhowudi_yekharakhtha, 1)) return -14;
        if (첫째값 == 0) {
            size_t 개수 = 0;
            while (개수 < ikhowudi_yekharakhtha) {
                int ikharakhtha_ixabiso = (int32_t)보드글자읽기(); if (ikharakhtha_ixabiso == -2) return 개수; if (ikharakhtha_ixabiso < 0) break;
                ((unsigned char *)둘째값)[개수++] = ikharakhtha_ixabiso;
            }
            return 개수 ? (intptr_t)개수 : (ikhowudi_yekharakhtha ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            결과=자바흐름읽기(첫째값,ikhowudi_yekharakhtha>512?512:ikhowudi_yekharakhtha);if(결과>0)for(int 순번=0;순번<결과;순번++)((unsigned char *)둘째값)[순번]=자바전문얻기(순번);return 결과;
        }
        ifayile_isibambi = 대응파일기술자(첫째값); if (ifayile_isibambi < 0) return -9;
        return 커널결과(pk_read(ifayile_isibambi, (void *)둘째값, ikhowudi_yekharakhtha));
    case 3:
        결과 = kopa_indlela(첫째값, INDLELA); if (결과) return 결과;
        if (둘째값 > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (ifayile_uludwe[순번] < 0) {
            ifayile_isibambi = pk_open(INDLELA, (int)둘째값, 0600);
            if (ifayile_isibambi < 0) return -오류번호;
            ifayile_uludwe[순번] = ifayile_isibambi; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { 결과 = 통신끝점닫기(첫째값); if (!결과) 통신끝점들[첫째값 - 32] = 0; return 결과; }
        ifayile_isibambi = 대응파일기술자(첫째값); if (ifayile_isibambi < 0) return -9;
        결과 = pk_close(ifayile_isibambi); if (!결과) ifayile_uludwe[첫째값 - 3] = -1;
        return 커널결과(결과);
    case 5:
        ifayile_isibambi = 대응파일기술자(첫째값); if (ifayile_isibambi < 0) return -9;
        if (ikhowudi_yekharakhtha > 2) return -22;
        return 커널결과(pk_lseek(ifayile_isibambi, (int64_t)둘째값, ikhowudi_yekharakhtha));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 umsebenzisi RW/NX 힙, 새로 노출되는 페이지는 0으로 qalisa_umsebenzi
        if (!첫째값) return 동적기억끝;
        if (첫째값 < umsebenzisi_umfanekiso_phela || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + ubungakanani_bekhasi - 1) & ~(ubungakanani_bekhasi - 1);
        uintptr_t 새쪽들 = (첫째값 + ubungakanani_bekhasi - 1) & ~(ubungakanani_bekhasi - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t 자료위치 = 이전쪽들; 자료위치 < 새쪽들; 자료위치 += ubungakanani_bekhasi) ukuma_kwephepha(자료위치, ikheneli_ikhasi, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t 자료위치 = 이전쪽들; 자료위치 < 새쪽들; 자료위치 += ubungakanani_bekhasi) ukuma_kwephepha(자료위치, umsebenzisi_funda_bhala, 3);
        } else {
            for (uintptr_t 자료위치 = 새쪽들; 자료위치 < 이전쪽들; 자료위치 += ubungakanani_bekhasi) {
                ikhasi_uludwe[(자료위치 - 사용자바탕) / ubungakanani_bekhasi] = 0; iimvume_uludwe[(자료위치 - 사용자바탕) / ubungakanani_bekhasi] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        ifayile_isibambi = 대응파일기술자(첫째값); return ifayile_isibambi < 0 ? -9 : 커널결과(pk_size(ifayile_isibambi));
    case 10:
        ifayile_isibambi = 대응파일기술자(첫째값); return ifayile_isibambi < 0 ? -9 : 커널결과(pk_ftruncate(ifayile_isibambi, (int64_t)둘째값));
    case 11:
        결과 = kopa_indlela(첫째값, INDLELA); return 결과 ? 결과 : 커널결과(pk_unlink(INDLELA));
    case 12:
        ifayile_isibambi = 대응파일기술자(첫째값); return ifayile_isibambi < 0 ? -9 : 커널결과(pk_fsync(ifayile_isibambi));
    case 13: { // 그래픽 기초 API: umsebenzisi 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = ifayile_ufako_nkcukacha->bhalisa_iingcombolo[3], 높이값 = ifayile_ufako_nkcukacha->bhalisa_iingcombolo[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || 둘째값 > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - 둘째값) return -22;
        for (uintptr_t 세로좌표 = 둘째값; 세로좌표 < 둘째값 + 높이값; 세로좌표++) for (uintptr_t isilungelelanisi_x = 첫째값; isilungelelanisi_x < 첫째값 + 너비값; isilungelelanisi_x++) 보드화소(isilungelelanisi_x, 세로좌표, ikhowudi_yekharakhtha);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=개수; args(index,buffer,capacity)=UTF-8 ubude_ixabiso
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (ikhowudi_yekharakhtha <= 전달인수길이[첫째값]) return -36;
        if (!사용자범위(둘째값, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)둘째값, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;esebenzisana_nomsebenzi=1;return 보드터미널(13);}
        if(첫째값==2){esebenzisana_nomsebenzi=0;return 0;}
        if(첫째값==3)return 보드터미널(13);
        if(첫째값!=1||!esebenzisana_nomsebenzi)return -22;
        결과=(int32_t)보드글자읽기();
        if(결과==-4096)return 결과;
        시간제한시작();return 결과<0?-11:결과;
    case 17: { // 유한한 협력 대기: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t 끝시각 = iwotshi_ixabiso() + 진동수 * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (iwotshi_ixabiso() < 끝시각);
        시간제한시작(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 부모·빈 폴더를 검사한다.
        if (둘째값 > 2) return -22;
        결과 = kopa_indlela(첫째값, INDLELA); if (결과) return 결과;
        unsigned ubude_ixabiso = 0; while (INDLELA[ubude_ixabiso]) ubude_ixabiso++;
        결과 = 자바경로시작(ubude_ixabiso); if (결과 < 0) return 결과;
        for (unsigned 순번 = 0; 순번 < ubude_ixabiso; 순번++) 자바경로바이트(순번, (unsigned char)INDLELA[순번]);
        return 둘째값 == 0 ? 자바항목종류() : 둘째값 == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int ikharakhtha_ixabiso=(int32_t)보드글자읽기();if(ikharakhtha_ixabiso==-4096)return ikharakhtha_ixabiso;if(ikharakhtha_ixabiso>=0)화면누름(umnini_into,ikharakhtha_ixabiso);시간제한시작();}
        if(첫째값==3&&ikhowudi_yekharakhtha){if(!자바셸대화형())return -95;esebenzisana_nomsebenzi=1;보드터미널(300);}
        return 화면호출(umnini_into,첫째값,둘째값,ikhowudi_yekharakhtha,ifayile_ufako_nkcukacha->bhalisa_iingcombolo[3],ifayile_ufako_nkcukacha->bhalisa_iingcombolo[4],ifayile_ufako_nkcukacha->bhalisa_iingcombolo[5]);
    case 21:
        if(ikhowudi_yekharakhtha>127)return -22;if(!사용자범위(둘째값,ikhowudi_yekharakhtha*sizeof(uint32_t),0))return -14;
        return 화면글(umnini_into,첫째값,(const uint32_t *)둘째값,ikhowudi_yekharakhtha);
    case 22: // 화면 Ubukhulu umbuzo_ixabiso: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(둘째값==SOCK_STREAM&&(ikhowudi_yekharakhtha==0||ikhowudi_yekharakhtha==6))결과=자바흐름만들기();
        else if(둘째값==SOCK_DGRAM&&(ikhowudi_yekharakhtha==0||ikhowudi_yekharakhtha==IPPROTO_UDP))결과=자바전문만들기(첫째값,둘째값,ikhowudi_yekharakhtha);
        else return -93;
        if (결과 >= 32 && 결과 < 56) 통신끝점들[결과 - 32] = 1;
        return 결과;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in idilesi;
        결과 = 주소입력(둘째값, ikhowudi_yekharakhtha, &idilesi); if (결과) return 결과;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(idilesi.sin_addr.s_addr),pk_htons(idilesi.sin_port)):자바전문묶기(첫째값, pk_htonl(idilesi.sin_addr.s_addr), pk_htons(idilesi.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (ifayile_ufako_nkcukacha->bhalisa_iingcombolo[3]) return -95;
        if (ikhowudi_yekharakhtha > 512) return -90;
        if (ikhowudi_yekharakhtha && !사용자범위(둘째값, ikhowudi_yekharakhtha, 0)) return -14;
        struct pk_sockaddr_in idilesi;
        결과 = 주소입력(ifayile_ufako_nkcukacha->bhalisa_iingcombolo[4], ifayile_ufako_nkcukacha->bhalisa_iingcombolo[5], &idilesi); if (결과) return 결과;
        for (unsigned 순번 = 0; 순번 < ikhowudi_yekharakhtha; 순번++) 자바전문넣기(순번, ((const unsigned char *)둘째값)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(idilesi.sin_addr.s_addr), pk_htons(idilesi.sin_port), ikhowudi_yekharakhtha);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (ifayile_ufako_nkcukacha->bhalisa_iingcombolo[3]) return -95;
        if (ikhowudi_yekharakhtha > 512) return -90;
        if (ikhowudi_yekharakhtha && !사용자범위(둘째값, ikhowudi_yekharakhtha, 1)) return -14;
        pk_socklen_t 수용량 = 0;
        if (ifayile_ufako_nkcukacha->bhalisa_iingcombolo[4]) { 결과 = 주소출력검사(ifayile_ufako_nkcukacha->bhalisa_iingcombolo[4], ifayile_ufako_nkcukacha->bhalisa_iingcombolo[5], &수용량); if (결과) return 결과; }
        결과 = 자바전문받기(첫째값, ikhowudi_yekharakhtha); if (결과 < 0) return 결과;
        for (int 순번 = 0; 순번 < 결과; 순번++) ((unsigned char *)둘째값)[순번] = 자바전문얻기(순번);
        if (ifayile_ufako_nkcukacha->bhalisa_iingcombolo[4]) 주소출력(ifayile_ufako_nkcukacha->bhalisa_iingcombolo[4], ifayile_ufako_nkcukacha->bhalisa_iingcombolo[5], 수용량, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return 결과;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t 수용량;
        결과 = 주소출력검사(둘째값, ikhowudi_yekharakhtha, &수용량); if (결과) return 결과;
        주소출력(둘째값,ikhowudi_yekharakhtha,수용량,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in idilesi;
        결과=주소입력(둘째값,ikhowudi_yekharakhtha,&idilesi);if(결과)return 결과;
        return 자바흐름연결(첫째값,pk_htonl(idilesi.sin_addr.s_addr),pk_htons(idilesi.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,둘째값):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(둘째값||ikhowudi_yekharakhtha)return -95;결과=자바흐름연결받기(첫째값);if(결과>=40&&결과<56)통신끝점들[결과-32]=1;return 결과;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(umsebenzisi_ifreyim *ifayile_ufako_nkcukacha) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(ifayile_ufako_nkcukacha) : 자체체계호출(ifayile_ufako_nkcukacha);
}
static void 커널돌아가기(umsebenzisi_ifreyim *ifayile_ufako_nkcukacha, int 결과) {
    시간제한멈춤();
    ifayile_ufako_nkcukacha->bhalisa_iingcombolo[0] = (uint64_t)(int64_t)결과;
    ifayile_ufako_nkcukacha->명령위치 = (uintptr_t)사용자복귀;
    ifayile_ufako_nkcukacha->상태값 = 0x3c5; // EL1h, DAIF masked
}
int 사용자예외(umsebenzisi_ifreyim *ifayile_ufako_nkcukacha, unsigned 가로채기) {
    if (!edlamkileyo || (ifayile_ufako_nkcukacha->상태값 & 15) != 0) return 0;
    if (가로채기) {
        uint32_t 승인값 = umatshini_bhalisa(i_IRQ_i_CPU_isinxulumanisi + 0xc), isalathisi_ixabiso = 승인값 & 1023;
        if (isalathisi_ixabiso == 30) { 커널돌아가기(ifayile_ufako_nkcukacha, 사용자시간초과); umatshini_bhalisa(i_IRQ_i_CPU_isinxulumanisi + 0x10) = 승인값; return 1; }
        if (isalathisi_ixabiso < 1020) umatshini_bhalisa(i_IRQ_i_CPU_isinxulumanisi + 0x10) = 승인값;
        return 1;
    }
    uint64_t 예외상태; __asm__ volatile("mrs %0, esr_el1" : "=r"(예외상태));
    if (iwotshi_ixabiso() >= 마감시각) { 커널돌아가기(ifayile_ufako_nkcukacha, 사용자시간초과); return 1; }
    unsigned 예외분류 = 예외상태 >> 26;
    if (예외분류 == 0x15 && (예외상태 & 0xffff) == 0) {
        if (리눅스규약 ? ifayile_ufako_nkcukacha->bhalisa_iingcombolo[8] == 93 || ifayile_ufako_nkcukacha->bhalisa_iingcombolo[8] == 94 : ifayile_ufako_nkcukacha->bhalisa_iingcombolo[8] == 6) 커널돌아가기(ifayile_ufako_nkcukacha, (int)(ifayile_ufako_nkcukacha->bhalisa_iingcombolo[0] & 255));
        else {
            intptr_t 결과=체계호출(ifayile_ufako_nkcukacha);
            if(결과==-4096&&esebenzisana_nomsebenzi){
                저장값[umnini_into].실행틀=*ifayile_ufako_nkcukacha;저장값[umnini_into].실행틀.명령위치-=4;
                사용자실수보관(저장값[umnini_into].실수저장상태);커널돌아가기(ifayile_ufako_nkcukacha,사용자중단됨);
            }else ifayile_ufako_nkcukacha->bhalisa_iingcombolo[0]=(uint64_t)결과;
        }
    } else 커널돌아가기(ifayile_ufako_nkcukacha, 예외분류 == 0x24 ? umsebenzisi_iingcombolo_impazamo : 예외분류 == 0x20 ? 사용자실행오류 : umsebenzisi_ayisebenzi_umyalelo);
    return 1;
}

// 생성된 const ELF iqela_ixabiso: 실행은 반드시 inkqubo_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *iingcombolo; size_t Ubukhulu; unsigned 전달값; } inkqubo;
#include "programs.h"
static void *i_snapshot(unsigned 자리){return (void *)(0x04000000ul+자리*(umsebenzisi_phela-사용자바탕));}
static int Gqiba_inkqubo(int 결과){
    사용자누적시각[umnini_into]+=(uint32_t)보드밀리초()-사용자실행시각[umnini_into];
    시간제한멈춤();edlamkileyo=0;
    if(결과==사용자중단됨){
        저장된작업 *uluhlu_lweekharektha_iingcombolo=&저장값[umnini_into];uluhlu_lweekharektha_iingcombolo->멈춤상태=1;uluhlu_lweekharektha_iingcombolo->esebenzisana_nomsebenzi=esebenzisana_nomsebenzi;uluhlu_lweekharektha_iingcombolo->리눅스규약=리눅스규약;uluhlu_lweekharektha_iingcombolo->동적기억공간=동적기억끝;uluhlu_lweekharektha_iingcombolo->인수개수=전달인수개수;
        memcpy(uluhlu_lweekharektha_iingcombolo->iimvume_uludwe,iimvume_uludwe,sizeof(iimvume_uludwe));memcpy(uluhlu_lweekharektha_iingcombolo->ifayile_uludwe,ifayile_uludwe,sizeof(ifayile_uludwe));memcpy(uluhlu_lweekharektha_iingcombolo->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(uluhlu_lweekharektha_iingcombolo->isiniki_myalelo_ULUHLU,전달인수,sizeof(전달인수));memcpy(uluhlu_lweekharektha_iingcombolo->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<사용자쪽수;순번++)if(iimvume_uludwe[순번])memcpy((unsigned char *)i_snapshot(umnini_into)+순번*ubungakanani_bekhasi,(void *)(사용자바탕+순번*ubungakanani_bekhasi),ubungakanani_bekhasi);
    }else{
        저장값[umnini_into].멈춤상태=0;화면초기화(umnini_into);
        for(unsigned 순번=0;순번<16;순번++)if(ifayile_uludwe[순번]>=0)pk_close(ifayile_uludwe[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<사용자쪽수;순번++){ikhasi_uludwe[순번]=0;iimvume_uludwe[순번]=0;}변환표맞추기();return 결과;
}
uintptr_t 보드사용자제어(uintptr_t Intshukumo){
    unsigned 자리=Intshukumo&15;if(자리>=4||edlamkileyo)return (uint32_t)-22;
    저장된작업 *uluhlu_lweekharektha_iingcombolo=&저장값[자리];
    if(Intshukumo>=32){if(uluhlu_lweekharektha_iingcombolo->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(uluhlu_lweekharektha_iingcombolo->ifayile_uludwe[순번]>=0)pk_close(uluhlu_lweekharektha_iingcombolo->ifayile_uludwe[순번]);for(unsigned 순번=0;순번<24;순번++)if(uluhlu_lweekharektha_iingcombolo->통신끝점들[순번])통신끝점닫기(순번+32);}uluhlu_lweekharektha_iingcombolo->멈춤상태=0;화면초기화(자리);return 0;}
    if(Intshukumo>=16)return uluhlu_lweekharektha_iingcombolo->멈춤상태;
    if(!uluhlu_lweekharektha_iingcombolo->멈춤상태)return (uint32_t)-22;
    umnini_into=자리;esebenzisana_nomsebenzi=uluhlu_lweekharektha_iingcombolo->esebenzisana_nomsebenzi;리눅스규약=uluhlu_lweekharektha_iingcombolo->리눅스규약;동적기억끝=uluhlu_lweekharektha_iingcombolo->동적기억공간;전달인수개수=uluhlu_lweekharektha_iingcombolo->인수개수;
    memcpy(ifayile_uludwe,uluhlu_lweekharektha_iingcombolo->ifayile_uludwe,sizeof(ifayile_uludwe));memcpy(통신끝점들,uluhlu_lweekharektha_iingcombolo->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,uluhlu_lweekharektha_iingcombolo->isiniki_myalelo_ULUHLU,sizeof(전달인수));memcpy(전달인수길이,uluhlu_lweekharektha_iingcombolo->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<사용자쪽수;순번++)ikhasi_uludwe[순번]=(사용자바탕+순번*ubungakanani_bekhasi)|ikheneli_ikhasi;변환표맞추기();
    memset((void *)사용자바탕,0,umsebenzisi_phela-사용자바탕);
    for(unsigned 순번=0;순번<사용자쪽수;순번++)if(uluhlu_lweekharektha_iingcombolo->iimvume_uludwe[순번])memcpy((void *)(사용자바탕+순번*ubungakanani_bekhasi),(unsigned char *)i_snapshot(자리)+순번*ubungakanani_bekhasi,ubungakanani_bekhasi);
    memcpy(iimvume_uludwe,uluhlu_lweekharektha_iingcombolo->iimvume_uludwe,sizeof(iimvume_uludwe));
    for(unsigned 순번=0;순번<사용자쪽수;순번++){unsigned 자료위치=iimvume_uludwe[순번];ikhasi_uludwe[순번]=자료위치?(사용자바탕+순번*ubungakanani_bekhasi)|(자료위치==3?umsebenzisi_funda_bhala:자료위치==5?사용자읽고실행:umsebenzisi_efundwayo_kuphela):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");edlamkileyo=1;uluhlu_lweekharektha_iingcombolo->멈춤상태=0;시간제한시작();
    사용자실행시각[umnini_into]=보드밀리초();
    return (uint32_t)Gqiba_inkqubo(umsebenzisi_i_CV(&uluhlu_lweekharektha_iingcombolo->실행틀,uluhlu_lweekharektha_iingcombolo->실수저장상태));
}
static int i_run_inkqubo(const unsigned char *iingcombolo, size_t Ubukhulu, unsigned 전달값, int 리눅스방식, const char *Igama) {
    if (edlamkileyo) return -16;
    umnini_into=보드터미널(11);if(umnini_into<0||umnini_into>3||저장값[umnini_into].멈춤상태)return -16;esebenzisana_nomsebenzi=0;
    int 유효함 = 실행파일검사(iingcombolo, Ubukhulu, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned igama_indeksa=0;
    while (*Igama && igama_indeksa<31) umsebenzisi_umyalelo_igama[umnini_into][igama_indeksa++]=(unsigned char)*Igama++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (igama_indeksa) umsebenzisi_umyalelo_igama[umnini_into][igama_indeksa++]=' ';
        for (unsigned 자리=0; 자리<전달인수길이[0]; 자리++) umsebenzisi_umyalelo_igama[umnini_into][igama_indeksa++]=전달인수[0][자리];
    }
    umsebenzisi_umyalelo_igama[umnini_into][igama_indeksa]=0; inombolo_yomsebenzisi[umnini_into]=다음사용자번호++;
    if (다음사용자번호>0x7fffffffu) 다음사용자번호=10;
    사용자시작시각[umnini_into]=보드밀리초(); 사용자누적시각[umnini_into]=0;
    for (unsigned 순번 = 0; 순번 < 사용자쪽수; 순번++) ikhasi_uludwe[순번] = (사용자바탕 + 순번 * ubungakanani_bekhasi) | ikheneli_ikhasi;
    변환표맞추기();
    memset((void *)사용자바탕, 0, umsebenzisi_phela - 사용자바탕);
    memset(iimvume_uludwe, 0, sizeof(iimvume_uludwe));
    실행파일머리 실행머리; memcpy(&실행머리, iingcombolo, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.프로그램머리개수; 순번++) {
        실행파일구획 자료위치; memcpy(&자료위치, iingcombolo + 실행머리.inkqubo_Iheda_Ukulinganisa + 순번 * sizeof(자료위치), sizeof(자료위치));
        if (자료위치.uhlobo_udidi != 1 || !자료위치.기억영역크기) continue;
        if (자료위치.파일영역크기) memcpy((void *)(uintptr_t)자료위치.idilesi, iingcombolo + 자료위치.Ukulinganisa_ixabiso, 자료위치.파일영역크기);
        for (uintptr_t 현재위치 = 자료위치.idilesi & ~(ubungakanani_bekhasi - 1); 현재위치 < 자료위치.idilesi + 자료위치.기억영역크기; 현재위치 += ubungakanani_bekhasi) {
            iimvume_uludwe[(현재위치 - 사용자바탕) / ubungakanani_bekhasi] = (자료위치.설정비트 & 2) ? 3 : ((자료위치.설정비트 & 1) ? 5 : 1);
        }
    }
    for (uintptr_t 현재위치 = umsebenzisi_fumba_idilesi; 현재위치 < umsebenzisi_phela; 현재위치 += ubungakanani_bekhasi) iimvume_uludwe[(현재위치 - 사용자바탕) / ubungakanani_bekhasi] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.ufako_nkcukacha_inqaku) : umsebenzisi_phela;
    for (unsigned 순번 = 0; 순번 < 사용자쪽수; 순번++) {
        unsigned iimvume = iimvume_uludwe[순번];
        ikhasi_uludwe[순번] = iimvume ? (사용자바탕 + 순번 * ubungakanani_bekhasi) | (iimvume == 3 ? umsebenzisi_funda_bhala : iimvume == 5 ? 사용자읽고실행 : umsebenzisi_efundwayo_kuphela) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) ifayile_uludwe[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = umsebenzisi_umfanekiso_phela;
    edlamkileyo = 1; 시간제한시작();
    사용자실행시각[umnini_into]=보드밀리초();
    int 결과 = umsebenzisi_ngenisa(실행머리.ufako_nkcukacha_inqaku, 초기쌓임공간, 전달값);
    return Gqiba_inkqubo(결과);
}
uintptr_t 보드사용자실행(uintptr_t 색인) {
    if (색인 >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Igama=색인==10?"javac":색인==11?"java":색인==12?"python":색인==13?"vi":색인==14?"jar":색인==15?"cc":색인==16?"jaot":"ELF";
    return (uint32_t)i_run_inkqubo(실행항목들[색인].iingcombolo, 실행항목들[색인].Ubukhulu, 실행항목들[색인].전달값, 0, Igama);
}
static uintptr_t ukwenza_ifayile(int 리눅스방식) {
    static unsigned char umfanekiso[16384];
    if (edlamkileyo || !전달인수개수) return (uint32_t)-22;
    int ifayile_isibambi = pk_open((const char *)전달인수[0], efundwayo_kuphela_ixabiso, 0);
    if (ifayile_isibambi < 0) return (uint32_t)-오류번호;
    int Ubukhulu = pk_size(ifayile_isibambi);
    if (Ubukhulu < 0 || (unsigned)Ubukhulu > sizeof(umfanekiso)) { pk_close(ifayile_isibambi); return (uint32_t)-27; }
    int 받은수 = pk_read(ifayile_isibambi, umfanekiso, Ubukhulu); pk_close(ifayile_isibambi);
    if (받은수 != Ubukhulu) return (uint32_t)-5;
    return (uint32_t)i_run_inkqubo(umfanekiso, Ubukhulu, 0, 리눅스방식, "");
}
uintptr_t 보드사용자파일(void) { return ukwenza_ifayile(0); }
uintptr_t 보드사용자리눅스파일(void) { return ukwenza_ifayile(1); }
uintptr_t 보드사용자검사(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].iingcombolo, 잘못된실행항목들[순번].Ubukhulu) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
