#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 phethagatša_taelo motšhene llaga_boleng. Faele data/정책은 기존 AOT Java 커널에 위임한다.
#include "mošomiši.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../Netweke_kgoboko/Netweke_kgoboko.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define motšhene_ngwadiša(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_moabi 0xff841000ul
#define IRQ_CPU_lefelokgokagano 0xff842000ul
#define bogolo_bja_letlakala 4096ul
#define 접근표시 (1ul << 10)
#define 권한실행금지 (1ul << 53)
#define 사용자실행금지 (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | 접근표시)
#define khenele_letlakala (3ul | 보통기억 | 권한실행금지 | 사용자실행금지)
#define mošomiši_bala_ngwala (3ul | 보통기억 | (1ul << 6) | 권한실행금지 | 사용자실행금지)
#define mošomiši_balwago_fela (3ul | 보통기억 | (3ul << 6) | 권한실행금지 | 사용자실행금지)
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
extern int mošomiši_CV(mošomiši_freime *,void *);
extern void 사용자실수보관(void *);
extern int mošomiši_tsenya(uintptr_t go_tsenya_tshedimošo_ntlha, uintptr_t kgoboko_Bobolokelo, uintptr_t 전달값);
extern void 사용자복귀(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t 뿌리주소[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t letlakala_Lenaneo[사용자쪽수] __attribute__((aligned(4096)));
static uint8_t ditumelelo_Lenaneo[사용자쪽수];
static int ekthibi, faele_Lenaneo[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned faele_tshwaro){return faele_tshwaro<40?자바전문닫기(faele_tshwaro):자바흐름닫기(faele_tshwaro);}
static uint64_t 진동수, 마감시각;
static uintptr_t 동적기억끝;
// khenele_boleng 셸이 준비한 UTF-8 인수. EL0에는 kopiša_boleng 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,ya_kgokagano,리눅스규약,faele_Lenaneo[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char akumente_arei[8][256],ditumelelo_Lenaneo[사용자쪽수];
    uintptr_t 동적기억공간; mošomiši_freime 실행틀;
    unsigned char 실수저장상태[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int mong_selo,ya_kgokagano;
static uint32_t nomoro_ya_mošomiši[4], 사용자시작시각[4], 사용자누적시각[4], 사용자실행시각[4], 다음사용자번호=10;
static unsigned char mošomiši_taelo_leina[4][288];
uint32_t 사용자상태읽기(unsigned go_tsenya_tshedimošo_boleng, unsigned lokela) {
    unsigned 자리=lokela&3;
    int boemo_boleng=(ekthibi && mong_selo==(int)자리) ? 1 : 저장값[자리].멈춤상태 ? 2 : 0;
    if (go_tsenya_tshedimošo_boleng==0) return boemo_boleng;
    if (!boemo_boleng) return 0;
    if (go_tsenya_tshedimošo_boleng==1) return nomoro_ya_mošomiši[자리];
    if (go_tsenya_tshedimošo_boleng==2) {
        unsigned char *쪽들=boemo_boleng==1?ditumelelo_Lenaneo:저장값[자리].ditumelelo_Lenaneo;
        unsigned 쪽수=0; for (unsigned 순번=0; 순번<사용자쪽수; 순번++) if(쪽들[순번]) 쪽수++;
        return 쪽수*4;
    }
    if (go_tsenya_tshedimošo_boleng==3) return (uint32_t)보드밀리초()-사용자시작시각[자리];
    if (go_tsenya_tshedimošo_boleng==4) return 사용자누적시각[자리]+(boemo_boleng==1?(uint32_t)보드밀리초()-사용자실행시각[자리]:0);
    if (go_tsenya_tshedimošo_boleng==5) return lokela/4<sizeof(mošomiši_taelo_leina[0])?mošomiši_taelo_leina[자리][lokela/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t 항목수) {
    if (ekthibi || 항목수 > 8) return (uint32_t)-22;
    전달인수개수 = 항목수;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t 색인, uintptr_t 현재위치, uintptr_t paete_data) {
    if (ekthibi || 색인 >= 전달인수개수 || 현재위치 >= 255 || 현재위치 != 전달인수길이[색인] || !paete_data || paete_data > 255)
        return (uint32_t)-22;
    전달인수[색인][현재위치] = paete_data;
    전달인수길이[색인] = 현재위치 + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t sešupanako_boleng(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void 시간제한멈춤(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    motšhene_ngwadiša(IRQ_moabi + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void 시간제한시작(void) {
    uint64_t 간격 = 진동수 * 2, bula = 1;
    마감시각 = sešupanako_boleng() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(bula) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned data_thibela = 0; data_thibela < 4; data_thibela++) {
        뿌리주소[data_thibela] = (uintptr_t)가운데[data_thibela] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t atrese = ((uintptr_t)data_thibela << 30) | ((uintptr_t)순번 << 21);
            가운데[data_thibela][순번] = atrese | 1 | 접근표시 | 사용자실행금지;
            if (atrese >= 0xfc000000ul) 가운데[data_thibela][순번] |= 권한실행금지; // Device-nGnRnE
            else 가운데[data_thibela][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned 둘째값 = 0; 둘째값 < 사용자쪽수 / 512; 둘째값++)
        가운데[0][(사용자바탕 >> 21) + 둘째값] = (uintptr_t)(letlakala_Lenaneo + 둘째값 * 512) | 3;
    for (unsigned 순번 = 0; 순번 < 사용자쪽수; 순번++) letlakala_Lenaneo[순번] = (사용자바탕 + 순번 * bogolo_bja_letlakala) | khenele_letlakala;
    uint64_t memori_tlhaodi_ya_faele_ngwadiša = 0x4400, atrese_Phetolelo_taolo = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(memori_tlhaodi_ya_faele_ngwadiša), "r"(atrese_Phetolelo_taolo), "r"((uintptr_t)뿌리주소) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t 실수저장상태 = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(실수저장상태) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(진동수));
    시간제한멈춤();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 go_tsenya_tshedimošo_ntlha_boleng 때만 Dumelela_boleng.
    motšhene_ngwadiša(IRQ_moabi) = 0;
    motšhene_ngwadiša(IRQ_moabi + 0x180) = 0xffffffff;
    motšhene_ngwadiša(IRQ_moabi + 0x80) = 0xffffffff;
    motšhene_ngwadiša(IRQ_moabi + 0x280) = 1u << 30;
    motšhene_ngwadiša(IRQ_moabi + 0x41c) = 0x80808080;
    motšhene_ngwadiša(IRQ_moabi + 0x100) = 1u << 30;
    motšhene_ngwadiša(IRQ_CPU_lefelokgokagano + 4) = 0xff;
    motšhene_ngwadiša(IRQ_CPU_lefelokgokagano + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 수 있다.
    int Tšhireletšo = (motšhene_ngwadiša(IRQ_moabi + 4) & (1u << 10)) != 0;
    motšhene_ngwadiša(IRQ_moabi) = Tšhireletšo ? 1 : 3;
    motšhene_ngwadiša(IRQ_CPU_lefelokgokagano) = Tšhireletšo ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t thaepa_legoro, motšhene_thaepa; uint32_t 판번호;
    uint64_t go_tsenya_tshedimošo_ntlha, tirišo_Hlogo_E_Šetšego, karolo_Hlogo_E_Šetšego; uint32_t 설정비트;
    uint16_t 실행머리크기, tirišo_Hlogo_go_tsenya_tshedimošo_bogolo, 프로그램머리개수, karolo_Hlogo_go_tsenya_tshedimošo_bogolo, 구역머리개수, karolo_leina_tafola_lokela;
} 실행파일머리;
typedef struct { uint32_t thaepa_legoro, 설정비트; uint64_t E_Šetšego_boleng, atrese, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(mošomiši_freime) == 272, "exception assembly layout");
static int 포함된범위(uint64_t E_Šetšego_boleng, uint64_t Bogolo, uint64_t fetša_E_Šetšego) {
    return E_Šetšego_boleng <= fetša_E_Šetšego && Bogolo <= fetša_E_Šetšego - E_Šetšego_boleng;
}
static int 부가정보검사(const unsigned char *자료위치, size_t Bogolo) {
    size_t 현재위치 = 0;
    while (포함된범위(현재위치, 12, Bogolo)) {
        uint32_t 낱말들[3]; memcpy(낱말들, 자료위치 + 현재위치, 12); 현재위치 += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(현재위치, 이름영역크기, Bogolo) || !포함된범위(현재위치 + 이름영역크기, 설명크기, Bogolo)) return 0;
        const unsigned char Leina[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Leina) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Leina); 순번++) if (자료위치[현재위치 + 순번] != Leina[순번]) 일치 = 0;
        uint32_t 판번호 = 0;
        if (일치) memcpy(&판번호, 자료위치 + 현재위치 + 이름영역크기, 4);
        if (일치 && 판번호 == 1) return 1;
        현재위치 += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *data, size_t Bogolo, int 리눅스방식) {
    if (Bogolo < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, data, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.thaepa_legoro != 2 || 실행머리.motšhene_thaepa != 183 || 실행머리.판번호 != 1 || 실행머리.설정비트 || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.tirišo_Hlogo_go_tsenya_tshedimošo_bogolo != sizeof(실행파일구획) || !실행머리.프로그램머리개수 || 실행머리.프로그램머리개수 > 16 ||
        실행머리.tirišo_Hlogo_E_Šetšego < sizeof(실행머리) || !포함된범위(실행머리.tirišo_Hlogo_E_Šetšego, (uint64_t)실행머리.프로그램머리개수 * sizeof(실행파일구획), Bogolo)) return 사용자실행파일오류;
    uint8_t 사용량[(mošomiši_seswantšho_fetša - 사용자바탕) / bogolo_bja_letlakala] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.프로그램머리개수; 순번++) {
        실행파일구획 자료위치; memcpy(&자료위치, data + 실행머리.tirišo_Hlogo_E_Šetšego + 순번 * sizeof(자료위치), sizeof(자료위치));
        if (자료위치.thaepa_legoro == 4) {
            if (!포함된범위(자료위치.E_Šetšego_boleng, 자료위치.파일영역크기, Bogolo)) return 사용자실행파일오류;
            if (부가정보검사(data + 자료위치.E_Šetšego_boleng, 자료위치.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (자료위치.thaepa_legoro == 0 || 자료위치.thaepa_legoro == 6 || (자료위치.thaepa_legoro == 0x6474e551 && !(자료위치.설정비트 & 1))) continue;
        if (자료위치.thaepa_legoro != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!자료위치.기억영역크기) continue;
        if (자료위치.설정비트 & ~7u || !(자료위치.설정비트 & 4) || (자료위치.설정비트 & 3) == 3 || 자료위치.파일영역크기 > 자료위치.기억영역크기 ||
            (자료위치.파일영역크기 && !포함된범위(자료위치.E_Šetšego_boleng, 자료위치.파일영역크기, Bogolo)) || 자료위치.atrese < 사용자바탕 ||
            !포함된범위(자료위치.atrese, 자료위치.기억영역크기, mošomiši_seswantšho_fetša) ||
            (!리눅스방식 && ((자료위치.atrese & (bogolo_bja_letlakala - 1)) || (자료위치.E_Šetšego_boleng & (bogolo_bja_letlakala - 1)) || 자료위치.맞춤 != bogolo_bja_letlakala)) ||
            (리눅스방식 && (((자료위치.atrese ^ 자료위치.E_Šetšego_boleng) & (bogolo_bja_letlakala - 1)) || !자료위치.맞춤 ||
                (자료위치.맞춤 & (자료위치.맞춤 - 1)) || 자료위치.맞춤 > 0x200000 || ((자료위치.atrese ^ 자료위치.E_Šetšego_boleng) & (자료위치.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (자료위치.atrese - 사용자바탕) / bogolo_bja_letlakala;
        unsigned 항목수 = ((자료위치.atrese & (bogolo_bja_letlakala - 1)) + 자료위치.기억영역크기 + bogolo_bja_letlakala - 1) / bogolo_bja_letlakala;
        for (unsigned letlakala_boleng = 첫항목; letlakala_boleng < 첫항목 + 항목수; letlakala_boleng++) {
            if (사용량[letlakala_boleng]) return 사용자실행파일오류;
            사용량[letlakala_boleng] = 1;
        }
        if ((자료위치.설정비트 & 1) && 실행머리.go_tsenya_tshedimošo_ntlha >= 자료위치.atrese && 실행머리.go_tsenya_tshedimošo_ntlha < 자료위치.atrese + 자료위치.파일영역크기 && !(실행머리.go_tsenya_tshedimošo_ntlha & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *data, size_t Bogolo) { return 실행파일검사(data, Bogolo, 0); }
static void ponagalo_ya_letlakala(uintptr_t atrese, uint64_t 설정비트, unsigned ditumelelo) {
    unsigned 색인 = (atrese - 사용자바탕) / bogolo_bja_letlakala;
    letlakala_Lenaneo[색인] = atrese | 설정비트;
    ditumelelo_Lenaneo[색인] = ditumelelo;
}
static int 사용자범위(uintptr_t atrese, size_t 항목수, int 쓰는중) {
    if (atrese < 사용자바탕 || !포함된범위(atrese, 항목수, mošomiši_fetša)) return 0;
    if (!항목수) return 1;
    unsigned 첫항목 = (atrese - 사용자바탕) / bogolo_bja_letlakala, 마지막 = (atrese + 항목수 - 1 - 사용자바탕) / bogolo_bja_letlakala;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(ditumelelo_Lenaneo[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int kopiša_tsela(uintptr_t atrese, char *Tsejana) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!사용자범위(atrese, 1, 0)) return -14;
        Tsejana[순번] = *(const char *)atrese++;
        if (!Tsejana[순번]) return 0;
    }
    return -36;
}
static intptr_t 커널결과(intptr_t 결과) { return 결과 < 0 ? -오류번호 : 결과; }
static int 대응파일기술자(uint64_t faele_tshwaro) { return faele_tshwaro >= 3 && faele_tshwaro < 19 ? faele_Lenaneo[faele_tshwaro - 3] : -1; }
static int 통신끝점소유(uint64_t faele_tshwaro) { return faele_tshwaro >= 32 && faele_tshwaro < 56 && 통신끝점들[faele_tshwaro - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t botelele_boleng, struct pk_sockaddr_in *atrese) {
    if (botelele_boleng != sizeof(*atrese)) return -22;
    if (!사용자범위(가리킴값, botelele_boleng, 0)) return -14;
    memcpy(atrese, (const void *)가리킴값, sizeof(*atrese));
    return atrese->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t botelele_sešupi, pk_socklen_t *수용량) {
    if (!사용자범위(botelele_sešupi, sizeof(*수용량), 1)) return -14;
    memcpy(수용량, (const void *)botelele_sešupi, sizeof(*수용량));
    if (*수용량 > sizeof(struct pk_sockaddr_in)) *수용량 = sizeof(struct pk_sockaddr_in);
    if (*수용량 && !사용자범위(가리킴값, *수용량, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t botelele_sešupi, pk_socklen_t 수용량, int atrese, int 접속번호) {
    struct pk_sockaddr_in boleng; memset(&boleng, 0, sizeof(boleng));
    boleng.sin_family = AF_INET; boleng.sin_port = pk_htons(접속번호); boleng.sin_addr.s_addr = pk_htonl(atrese);
    if (수용량) memcpy((void *)가리킴값, &boleng, 수용량);
    pk_socklen_t botelele_boleng = sizeof(boleng); memcpy((void *)botelele_sešupi, &botelele_boleng, sizeof(botelele_boleng));
}
extern uintptr_t 보드통로(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(mošomiši_freime *faele_go_tsenya_tshedimošo) {
    uintptr_t 첫째값 = faele_go_tsenya_tshedimošo->ngwadiša_data[0], 둘째값 = faele_go_tsenya_tshedimošo->ngwadiša_data[1], khouto_ya_tlhaka = faele_go_tsenya_tshedimošo->ngwadiša_data[2];
    char Tsejana[65];
    int faele_tshwaro, 결과;
    switch (faele_go_tsenya_tshedimošo->ngwadiša_data[8]) {
    case 0: return 1; // 자체 ABI 버전
    case 1: // write: sešupi 전체를 검사한 Morago_boleng 출력/Faele fetoša_boleng
        if (khouto_ya_tlhaka > 65536) return -22;
        if (!사용자범위(둘째값, khouto_ya_tlhaka, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=sešupanako_boleng();
            for (size_t 순번 = 0; 순번 < khouto_ya_tlhaka; 순번++) 보드통로(첫째값, ((const unsigned char *)둘째값)[순번]);
            /* 큰 tty를 그린 khenele_boleng 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(ya_kgokagano){
                마감시각+=sešupanako_boleng()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(마감시각) : "memory");
            }
            return khouto_ya_tlhaka;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t 개수=khouto_ya_tlhaka>512?512:khouto_ya_tlhaka;for(size_t 순번=0;순번<개수;순번++)자바전문넣기(순번,((const unsigned char *)둘째값)[순번]);return 자바흐름쓰기(첫째값,개수);
        }
        faele_tshwaro = 대응파일기술자(첫째값); if (faele_tshwaro < 0) return -9;
        return 커널결과(pk_write(faele_tshwaro, (const void *)둘째값, khouto_ya_tlhaka));
    case 2:
        if (khouto_ya_tlhaka > 65536) return -22;
        if (!사용자범위(둘째값, khouto_ya_tlhaka, 1)) return -14;
        if (첫째값 == 0) {
            size_t 개수 = 0;
            while (개수 < khouto_ya_tlhaka) {
                int tlhaka_boleng = (int32_t)보드글자읽기(); if (tlhaka_boleng == -2) return 개수; if (tlhaka_boleng < 0) break;
                ((unsigned char *)둘째값)[개수++] = tlhaka_boleng;
            }
            return 개수 ? (intptr_t)개수 : (khouto_ya_tlhaka ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            결과=자바흐름읽기(첫째값,khouto_ya_tlhaka>512?512:khouto_ya_tlhaka);if(결과>0)for(int 순번=0;순번<결과;순번++)((unsigned char *)둘째값)[순번]=자바전문얻기(순번);return 결과;
        }
        faele_tshwaro = 대응파일기술자(첫째값); if (faele_tshwaro < 0) return -9;
        return 커널결과(pk_read(faele_tshwaro, (void *)둘째값, khouto_ya_tlhaka));
    case 3:
        결과 = kopiša_tsela(첫째값, Tsejana); if (결과) return 결과;
        if (둘째값 > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (faele_Lenaneo[순번] < 0) {
            faele_tshwaro = pk_open(Tsejana, (int)둘째값, 0600);
            if (faele_tshwaro < 0) return -오류번호;
            faele_Lenaneo[순번] = faele_tshwaro; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { 결과 = 통신끝점닫기(첫째값); if (!결과) 통신끝점들[첫째값 - 32] = 0; return 결과; }
        faele_tshwaro = 대응파일기술자(첫째값); if (faele_tshwaro < 0) return -9;
        결과 = pk_close(faele_tshwaro); if (!결과) faele_Lenaneo[첫째값 - 3] = -1;
        return 커널결과(결과);
    case 5:
        faele_tshwaro = 대응파일기술자(첫째값); if (faele_tshwaro < 0) return -9;
        if (khouto_ya_tlhaka > 2) return -22;
        return 커널결과(pk_lseek(faele_tshwaro, (int64_t)둘째값, khouto_ya_tlhaka));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 mošomiši RW/NX 힙, 새로 노출되는 페이지는 0으로 thomiša
        if (!첫째값) return 동적기억끝;
        if (첫째값 < mošomiši_seswantšho_fetša || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + bogolo_bja_letlakala - 1) & ~(bogolo_bja_letlakala - 1);
        uintptr_t 새쪽들 = (첫째값 + bogolo_bja_letlakala - 1) & ~(bogolo_bja_letlakala - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t 자료위치 = 이전쪽들; 자료위치 < 새쪽들; 자료위치 += bogolo_bja_letlakala) ponagalo_ya_letlakala(자료위치, khenele_letlakala, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t 자료위치 = 이전쪽들; 자료위치 < 새쪽들; 자료위치 += bogolo_bja_letlakala) ponagalo_ya_letlakala(자료위치, mošomiši_bala_ngwala, 3);
        } else {
            for (uintptr_t 자료위치 = 새쪽들; 자료위치 < 이전쪽들; 자료위치 += bogolo_bja_letlakala) {
                letlakala_Lenaneo[(자료위치 - 사용자바탕) / bogolo_bja_letlakala] = 0; ditumelelo_Lenaneo[(자료위치 - 사용자바탕) / bogolo_bja_letlakala] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        faele_tshwaro = 대응파일기술자(첫째값); return faele_tshwaro < 0 ? -9 : 커널결과(pk_size(faele_tshwaro));
    case 10:
        faele_tshwaro = 대응파일기술자(첫째값); return faele_tshwaro < 0 ? -9 : 커널결과(pk_ftruncate(faele_tshwaro, (int64_t)둘째값));
    case 11:
        결과 = kopiša_tsela(첫째값, Tsejana); return 결과 ? 결과 : 커널결과(pk_unlink(Tsejana));
    case 12:
        faele_tshwaro = 대응파일기술자(첫째값); return faele_tshwaro < 0 ? -9 : 커널결과(pk_fsync(faele_tshwaro));
    case 13: { // 그래픽 기초 API: mošomiši 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = faele_go_tsenya_tshedimošo->ngwadiša_data[3], 높이값 = faele_go_tsenya_tshedimošo->ngwadiša_data[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || 둘째값 > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - 둘째값) return -22;
        for (uintptr_t 세로좌표 = 둘째값; 세로좌표 < 둘째값 + 높이값; 세로좌표++) for (uintptr_t kamano_ya_x = 첫째값; kamano_ya_x < 첫째값 + 너비값; kamano_ya_x++) 보드화소(kamano_ya_x, 세로좌표, khouto_ya_tlhaka);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=개수; args(index,buffer,capacity)=UTF-8 botelele_boleng
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (khouto_ya_tlhaka <= 전달인수길이[첫째값]) return -36;
        if (!사용자범위(둘째값, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)둘째값, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;ya_kgokagano=1;return 보드터미널(13);}
        if(첫째값==2){ya_kgokagano=0;return 0;}
        if(첫째값==3)return 보드터미널(13);
        if(첫째값!=1||!ya_kgokagano)return -22;
        결과=(int32_t)보드글자읽기();
        if(결과==-4096)return 결과;
        시간제한시작();return 결과<0?-11:결과;
    case 17: { // 유한한 협력 대기: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t 끝시각 = sešupanako_boleng() + 진동수 * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (sešupanako_boleng() < 끝시각);
        시간제한시작(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 부모·빈 폴더를 검사한다.
        if (둘째값 > 2) return -22;
        결과 = kopiša_tsela(첫째값, Tsejana); if (결과) return 결과;
        unsigned botelele_boleng = 0; while (Tsejana[botelele_boleng]) botelele_boleng++;
        결과 = 자바경로시작(botelele_boleng); if (결과 < 0) return 결과;
        for (unsigned 순번 = 0; 순번 < botelele_boleng; 순번++) 자바경로바이트(순번, (unsigned char)Tsejana[순번]);
        return 둘째값 == 0 ? 자바항목종류() : 둘째값 == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int tlhaka_boleng=(int32_t)보드글자읽기();if(tlhaka_boleng==-4096)return tlhaka_boleng;if(tlhaka_boleng>=0)화면누름(mong_selo,tlhaka_boleng);시간제한시작();}
        if(첫째값==3&&khouto_ya_tlhaka){if(!자바셸대화형())return -95;ya_kgokagano=1;보드터미널(300);}
        return 화면호출(mong_selo,첫째값,둘째값,khouto_ya_tlhaka,faele_go_tsenya_tshedimošo->ngwadiša_data[3],faele_go_tsenya_tshedimošo->ngwadiša_data[4],faele_go_tsenya_tshedimošo->ngwadiša_data[5]);
    case 21:
        if(khouto_ya_tlhaka>127)return -22;if(!사용자범위(둘째값,khouto_ya_tlhaka*sizeof(uint32_t),0))return -14;
        return 화면글(mong_selo,첫째값,(const uint32_t *)둘째값,khouto_ya_tlhaka);
    case 22: // 화면 Bogolo kwiri_boleng: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(둘째값==SOCK_STREAM&&(khouto_ya_tlhaka==0||khouto_ya_tlhaka==6))결과=자바흐름만들기();
        else if(둘째값==SOCK_DGRAM&&(khouto_ya_tlhaka==0||khouto_ya_tlhaka==IPPROTO_UDP))결과=자바전문만들기(첫째값,둘째값,khouto_ya_tlhaka);
        else return -93;
        if (결과 >= 32 && 결과 < 56) 통신끝점들[결과 - 32] = 1;
        return 결과;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in atrese;
        결과 = 주소입력(둘째값, khouto_ya_tlhaka, &atrese); if (결과) return 결과;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(atrese.sin_addr.s_addr),pk_htons(atrese.sin_port)):자바전문묶기(첫째값, pk_htonl(atrese.sin_addr.s_addr), pk_htons(atrese.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (faele_go_tsenya_tshedimošo->ngwadiša_data[3]) return -95;
        if (khouto_ya_tlhaka > 512) return -90;
        if (khouto_ya_tlhaka && !사용자범위(둘째값, khouto_ya_tlhaka, 0)) return -14;
        struct pk_sockaddr_in atrese;
        결과 = 주소입력(faele_go_tsenya_tshedimošo->ngwadiša_data[4], faele_go_tsenya_tshedimošo->ngwadiša_data[5], &atrese); if (결과) return 결과;
        for (unsigned 순번 = 0; 순번 < khouto_ya_tlhaka; 순번++) 자바전문넣기(순번, ((const unsigned char *)둘째값)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(atrese.sin_addr.s_addr), pk_htons(atrese.sin_port), khouto_ya_tlhaka);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (faele_go_tsenya_tshedimošo->ngwadiša_data[3]) return -95;
        if (khouto_ya_tlhaka > 512) return -90;
        if (khouto_ya_tlhaka && !사용자범위(둘째값, khouto_ya_tlhaka, 1)) return -14;
        pk_socklen_t 수용량 = 0;
        if (faele_go_tsenya_tshedimošo->ngwadiša_data[4]) { 결과 = 주소출력검사(faele_go_tsenya_tshedimošo->ngwadiša_data[4], faele_go_tsenya_tshedimošo->ngwadiša_data[5], &수용량); if (결과) return 결과; }
        결과 = 자바전문받기(첫째값, khouto_ya_tlhaka); if (결과 < 0) return 결과;
        for (int 순번 = 0; 순번 < 결과; 순번++) ((unsigned char *)둘째값)[순번] = 자바전문얻기(순번);
        if (faele_go_tsenya_tshedimošo->ngwadiša_data[4]) 주소출력(faele_go_tsenya_tshedimošo->ngwadiša_data[4], faele_go_tsenya_tshedimošo->ngwadiša_data[5], 수용량, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return 결과;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t 수용량;
        결과 = 주소출력검사(둘째값, khouto_ya_tlhaka, &수용량); if (결과) return 결과;
        주소출력(둘째값,khouto_ya_tlhaka,수용량,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in atrese;
        결과=주소입력(둘째값,khouto_ya_tlhaka,&atrese);if(결과)return 결과;
        return 자바흐름연결(첫째값,pk_htonl(atrese.sin_addr.s_addr),pk_htons(atrese.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,둘째값):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(둘째값||khouto_ya_tlhaka)return -95;결과=자바흐름연결받기(첫째값);if(결과>=40&&결과<56)통신끝점들[결과-32]=1;return 결과;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(mošomiši_freime *faele_go_tsenya_tshedimošo) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(faele_go_tsenya_tshedimošo) : 자체체계호출(faele_go_tsenya_tshedimošo);
}
static void 커널돌아가기(mošomiši_freime *faele_go_tsenya_tshedimošo, int 결과) {
    시간제한멈춤();
    faele_go_tsenya_tshedimošo->ngwadiša_data[0] = (uint64_t)(int64_t)결과;
    faele_go_tsenya_tshedimošo->명령위치 = (uintptr_t)사용자복귀;
    faele_go_tsenya_tshedimošo->상태값 = 0x3c5; // EL1h, DAIF masked
}
int 사용자예외(mošomiši_freime *faele_go_tsenya_tshedimošo, unsigned 가로채기) {
    if (!ekthibi || (faele_go_tsenya_tshedimošo->상태값 & 15) != 0) return 0;
    if (가로채기) {
        uint32_t 승인값 = motšhene_ngwadiša(IRQ_CPU_lefelokgokagano + 0xc), sešupi_boleng = 승인값 & 1023;
        if (sešupi_boleng == 30) { 커널돌아가기(faele_go_tsenya_tshedimošo, 사용자시간초과); motšhene_ngwadiša(IRQ_CPU_lefelokgokagano + 0x10) = 승인값; return 1; }
        if (sešupi_boleng < 1020) motšhene_ngwadiša(IRQ_CPU_lefelokgokagano + 0x10) = 승인값;
        return 1;
    }
    uint64_t 예외상태; __asm__ volatile("mrs %0, esr_el1" : "=r"(예외상태));
    if (sešupanako_boleng() >= 마감시각) { 커널돌아가기(faele_go_tsenya_tshedimošo, 사용자시간초과); return 1; }
    unsigned 예외분류 = 예외상태 >> 26;
    if (예외분류 == 0x15 && (예외상태 & 0xffff) == 0) {
        if (리눅스규약 ? faele_go_tsenya_tshedimošo->ngwadiša_data[8] == 93 || faele_go_tsenya_tshedimošo->ngwadiša_data[8] == 94 : faele_go_tsenya_tshedimošo->ngwadiša_data[8] == 6) 커널돌아가기(faele_go_tsenya_tshedimošo, (int)(faele_go_tsenya_tshedimošo->ngwadiša_data[0] & 255));
        else {
            intptr_t 결과=체계호출(faele_go_tsenya_tshedimošo);
            if(결과==-4096&&ya_kgokagano){
                저장값[mong_selo].실행틀=*faele_go_tsenya_tshedimošo;저장값[mong_selo].실행틀.명령위치-=4;
                사용자실수보관(저장값[mong_selo].실수저장상태);커널돌아가기(faele_go_tsenya_tshedimošo,사용자중단됨);
            }else faele_go_tsenya_tshedimošo->ngwadiša_data[0]=(uint64_t)결과;
        }
    } else 커널돌아가기(faele_go_tsenya_tshedimošo, 예외분류 == 0x24 ? mošomiši_data_phošo : 예외분류 == 0x20 ? 사용자실행오류 : mošomiši_ye_e_phošagetšego_taelo);
    return 1;
}

// 생성된 const ELF sehlopha_boleng: 실행은 반드시 tirišo_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *data; size_t Bogolo; unsigned 전달값; } tirišo;
#include "programs.h"
static void *go_tšea_senepe(unsigned 자리){return (void *)(0x04000000ul+자리*(mošomiši_fetša-사용자바탕));}
static int Fetša_tirišo(int 결과){
    사용자누적시각[mong_selo]+=(uint32_t)보드밀리초()-사용자실행시각[mong_selo];
    시간제한멈춤();ekthibi=0;
    if(결과==사용자중단됨){
        저장된작업 *molokoloko_data=&저장값[mong_selo];molokoloko_data->멈춤상태=1;molokoloko_data->ya_kgokagano=ya_kgokagano;molokoloko_data->리눅스규약=리눅스규약;molokoloko_data->동적기억공간=동적기억끝;molokoloko_data->인수개수=전달인수개수;
        memcpy(molokoloko_data->ditumelelo_Lenaneo,ditumelelo_Lenaneo,sizeof(ditumelelo_Lenaneo));memcpy(molokoloko_data->faele_Lenaneo,faele_Lenaneo,sizeof(faele_Lenaneo));memcpy(molokoloko_data->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(molokoloko_data->akumente_arei,전달인수,sizeof(전달인수));memcpy(molokoloko_data->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<사용자쪽수;순번++)if(ditumelelo_Lenaneo[순번])memcpy((unsigned char *)go_tšea_senepe(mong_selo)+순번*bogolo_bja_letlakala,(void *)(사용자바탕+순번*bogolo_bja_letlakala),bogolo_bja_letlakala);
    }else{
        저장값[mong_selo].멈춤상태=0;화면초기화(mong_selo);
        for(unsigned 순번=0;순번<16;순번++)if(faele_Lenaneo[순번]>=0)pk_close(faele_Lenaneo[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<사용자쪽수;순번++){letlakala_Lenaneo[순번]=0;ditumelelo_Lenaneo[순번]=0;}변환표맞추기();return 결과;
}
uintptr_t 보드사용자제어(uintptr_t Mogato){
    unsigned 자리=Mogato&15;if(자리>=4||ekthibi)return (uint32_t)-22;
    저장된작업 *molokoloko_data=&저장값[자리];
    if(Mogato>=32){if(molokoloko_data->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(molokoloko_data->faele_Lenaneo[순번]>=0)pk_close(molokoloko_data->faele_Lenaneo[순번]);for(unsigned 순번=0;순번<24;순번++)if(molokoloko_data->통신끝점들[순번])통신끝점닫기(순번+32);}molokoloko_data->멈춤상태=0;화면초기화(자리);return 0;}
    if(Mogato>=16)return molokoloko_data->멈춤상태;
    if(!molokoloko_data->멈춤상태)return (uint32_t)-22;
    mong_selo=자리;ya_kgokagano=molokoloko_data->ya_kgokagano;리눅스규약=molokoloko_data->리눅스규약;동적기억끝=molokoloko_data->동적기억공간;전달인수개수=molokoloko_data->인수개수;
    memcpy(faele_Lenaneo,molokoloko_data->faele_Lenaneo,sizeof(faele_Lenaneo));memcpy(통신끝점들,molokoloko_data->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,molokoloko_data->akumente_arei,sizeof(전달인수));memcpy(전달인수길이,molokoloko_data->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<사용자쪽수;순번++)letlakala_Lenaneo[순번]=(사용자바탕+순번*bogolo_bja_letlakala)|khenele_letlakala;변환표맞추기();
    memset((void *)사용자바탕,0,mošomiši_fetša-사용자바탕);
    for(unsigned 순번=0;순번<사용자쪽수;순번++)if(molokoloko_data->ditumelelo_Lenaneo[순번])memcpy((void *)(사용자바탕+순번*bogolo_bja_letlakala),(unsigned char *)go_tšea_senepe(자리)+순번*bogolo_bja_letlakala,bogolo_bja_letlakala);
    memcpy(ditumelelo_Lenaneo,molokoloko_data->ditumelelo_Lenaneo,sizeof(ditumelelo_Lenaneo));
    for(unsigned 순번=0;순번<사용자쪽수;순번++){unsigned 자료위치=ditumelelo_Lenaneo[순번];letlakala_Lenaneo[순번]=자료위치?(사용자바탕+순번*bogolo_bja_letlakala)|(자료위치==3?mošomiši_bala_ngwala:자료위치==5?사용자읽고실행:mošomiši_balwago_fela):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");ekthibi=1;molokoloko_data->멈춤상태=0;시간제한시작();
    사용자실행시각[mong_selo]=보드밀리초();
    return (uint32_t)Fetša_tirišo(mošomiši_CV(&molokoloko_data->실행틀,molokoloko_data->실수저장상태));
}
static int sepetša_tirišo(const unsigned char *data, size_t Bogolo, unsigned 전달값, int 리눅스방식, const char *Leina) {
    if (ekthibi) return -16;
    mong_selo=보드터미널(11);if(mong_selo<0||mong_selo>3||저장값[mong_selo].멈춤상태)return -16;ya_kgokagano=0;
    int 유효함 = 실행파일검사(data, Bogolo, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned leina_lokela=0;
    while (*Leina && leina_lokela<31) mošomiši_taelo_leina[mong_selo][leina_lokela++]=(unsigned char)*Leina++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (leina_lokela) mošomiši_taelo_leina[mong_selo][leina_lokela++]=' ';
        for (unsigned 자리=0; 자리<전달인수길이[0]; 자리++) mošomiši_taelo_leina[mong_selo][leina_lokela++]=전달인수[0][자리];
    }
    mošomiši_taelo_leina[mong_selo][leina_lokela]=0; nomoro_ya_mošomiši[mong_selo]=다음사용자번호++;
    if (다음사용자번호>0x7fffffffu) 다음사용자번호=10;
    사용자시작시각[mong_selo]=보드밀리초(); 사용자누적시각[mong_selo]=0;
    for (unsigned 순번 = 0; 순번 < 사용자쪽수; 순번++) letlakala_Lenaneo[순번] = (사용자바탕 + 순번 * bogolo_bja_letlakala) | khenele_letlakala;
    변환표맞추기();
    memset((void *)사용자바탕, 0, mošomiši_fetša - 사용자바탕);
    memset(ditumelelo_Lenaneo, 0, sizeof(ditumelelo_Lenaneo));
    실행파일머리 실행머리; memcpy(&실행머리, data, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.프로그램머리개수; 순번++) {
        실행파일구획 자료위치; memcpy(&자료위치, data + 실행머리.tirišo_Hlogo_E_Šetšego + 순번 * sizeof(자료위치), sizeof(자료위치));
        if (자료위치.thaepa_legoro != 1 || !자료위치.기억영역크기) continue;
        if (자료위치.파일영역크기) memcpy((void *)(uintptr_t)자료위치.atrese, data + 자료위치.E_Šetšego_boleng, 자료위치.파일영역크기);
        for (uintptr_t 현재위치 = 자료위치.atrese & ~(bogolo_bja_letlakala - 1); 현재위치 < 자료위치.atrese + 자료위치.기억영역크기; 현재위치 += bogolo_bja_letlakala) {
            ditumelelo_Lenaneo[(현재위치 - 사용자바탕) / bogolo_bja_letlakala] = (자료위치.설정비트 & 2) ? 3 : ((자료위치.설정비트 & 1) ? 5 : 1);
        }
    }
    for (uintptr_t 현재위치 = mošomiši_kgoboko_atrese; 현재위치 < mošomiši_fetša; 현재위치 += bogolo_bja_letlakala) ditumelelo_Lenaneo[(현재위치 - 사용자바탕) / bogolo_bja_letlakala] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.go_tsenya_tshedimošo_ntlha) : mošomiši_fetša;
    for (unsigned 순번 = 0; 순번 < 사용자쪽수; 순번++) {
        unsigned ditumelelo = ditumelelo_Lenaneo[순번];
        letlakala_Lenaneo[순번] = ditumelelo ? (사용자바탕 + 순번 * bogolo_bja_letlakala) | (ditumelelo == 3 ? mošomiši_bala_ngwala : ditumelelo == 5 ? 사용자읽고실행 : mošomiši_balwago_fela) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) faele_Lenaneo[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = mošomiši_seswantšho_fetša;
    ekthibi = 1; 시간제한시작();
    사용자실행시각[mong_selo]=보드밀리초();
    int 결과 = mošomiši_tsenya(실행머리.go_tsenya_tshedimošo_ntlha, 초기쌓임공간, 전달값);
    return Fetša_tirišo(결과);
}
uintptr_t 보드사용자실행(uintptr_t 색인) {
    if (색인 >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Leina=색인==10?"javac":색인==11?"java":색인==12?"python":색인==13?"vi":색인==14?"jar":색인==15?"cc":색인==16?"jaot":"ELF";
    return (uint32_t)sepetša_tirišo(실행항목들[색인].data, 실행항목들[색인].Bogolo, 실행항목들[색인].전달값, 0, Leina);
}
static uintptr_t phethagatša_faele(int 리눅스방식) {
    static unsigned char seswantšho[16384];
    if (ekthibi || !전달인수개수) return (uint32_t)-22;
    int faele_tshwaro = pk_open((const char *)전달인수[0], balwago_fela_boleng, 0);
    if (faele_tshwaro < 0) return (uint32_t)-오류번호;
    int Bogolo = pk_size(faele_tshwaro);
    if (Bogolo < 0 || (unsigned)Bogolo > sizeof(seswantšho)) { pk_close(faele_tshwaro); return (uint32_t)-27; }
    int 받은수 = pk_read(faele_tshwaro, seswantšho, Bogolo); pk_close(faele_tshwaro);
    if (받은수 != Bogolo) return (uint32_t)-5;
    return (uint32_t)sepetša_tirišo(seswantšho, Bogolo, 0, 리눅스방식, "");
}
uintptr_t 보드사용자파일(void) { return phethagatša_faele(0); }
uintptr_t 보드사용자리눅스파일(void) { return phethagatša_faele(1); }
uintptr_t 보드사용자검사(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].data, 잘못된실행항목들[순번].Bogolo) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
