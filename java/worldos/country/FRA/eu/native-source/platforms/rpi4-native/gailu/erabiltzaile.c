#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 exekutatu_komando gailu maila_balio. Fitxategia datuak/정책은 기존 AOT Java 커널에 위임한다.
#include "erabiltzaile.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../sare_pila/sare_pila.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define gailu_izena_eman(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_banatzailea 0xff841000ul
#define IRQ_PUZ_interfaze 0xff842000ul
#define orrialdearen_tamaina 4096ul
#define 접근표시 (1ul << 10)
#define ez_exekutatu_baimen (1ul << 53)
#define erabiltzaile_ez_exekutatu (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | 접근표시)
#define nukleo_orri (3ul | 보통기억 | ez_exekutatu_baimen | erabiltzaile_ez_exekutatu)
#define erabiltzaile_irakurri_idatzi (3ul | 보통기억 | (1ul << 6) | ez_exekutatu_baimen | erabiltzaile_ez_exekutatu)
#define erabiltzaile_irakurtzeko_soilik (3ul | 보통기억 | (3ul << 6) | ez_exekutatu_baimen | erabiltzaile_ez_exekutatu)
#define 사용자읽고실행 (3ul | 보통기억 | (3ul << 6) | ez_exekutatu_baimen)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t arbel_pixel(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t arbel_Terminal(uintptr_t);
extern int Terminal_zain(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int erabiltzaile_CV(erabiltzaile_marko *,void *);
extern void 사용자실수보관(void *);
extern int erabiltzaile_sartu(uintptr_t sarrera_p, uintptr_t pila_biltegi, uintptr_t 전달값);
extern void erabiltzaile_itzuli(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t erro_helbide[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t orri_Zerrenda[erabiltzaile_orri_ZENBATU] __attribute__((aligned(4096)));
static uint8_t Baimenak_Zerrenda[erabiltzaile_orri_ZENBATU];
static int aktibo, fitxategi_Zerrenda[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned fitxategi_helduleku){return fitxategi_helduleku<40?자바전문닫기(fitxategi_helduleku):자바흐름닫기(fitxategi_helduleku);}
static uint64_t MAIZTASUNA, 마감시각;
static uintptr_t 동적기억끝;
// nukleo_balio 셸이 준비한 UTF-8 Argumentuak. EL0에는 kopiatu_balio 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,interaktibo,리눅스규약,fitxategi_Zerrenda[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char arg_matrize[8][256],Baimenak_Zerrenda[erabiltzaile_orri_ZENBATU];
    uintptr_t 동적기억공간; erabiltzaile_marko 실행틀;
    unsigned char mugikor_p_Egoera[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int jabe_objektu,interaktibo;
static uint32_t erabiltzaile_zenbaki[4], erabiltzaile_HASI_ordua[4], 사용자누적시각[4], 사용자실행시각[4], Hurrengoa_erabiltzaile_zenbaki=10;
static unsigned char erabiltzaile_komando_izen[4][288];
uint32_t 사용자상태읽기(unsigned sarrera_balio, unsigned INDIZE) {
    unsigned kargu_INDIZE=INDIZE&3;
    int Egoera_balio=(aktibo && jabe_objektu==(int)kargu_INDIZE) ? 1 : 저장값[kargu_INDIZE].멈춤상태 ? 2 : 0;
    if (sarrera_balio==0) return Egoera_balio;
    if (!Egoera_balio) return 0;
    if (sarrera_balio==1) return erabiltzaile_zenbaki[kargu_INDIZE];
    if (sarrera_balio==2) {
        unsigned char *쪽들=Egoera_balio==1?Baimenak_Zerrenda:저장값[kargu_INDIZE].Baimenak_Zerrenda;
        unsigned orri_ZENBATU=0; for (unsigned 순번=0; 순번<erabiltzaile_orri_ZENBATU; 순번++) if(쪽들[순번]) orri_ZENBATU++;
        return orri_ZENBATU*4;
    }
    if (sarrera_balio==3) return (uint32_t)보드밀리초()-erabiltzaile_HASI_ordua[kargu_INDIZE];
    if (sarrera_balio==4) return 사용자누적시각[kargu_INDIZE]+(Egoera_balio==1?(uint32_t)보드밀리초()-사용자실행시각[kargu_INDIZE]:0);
    if (sarrera_balio==5) return INDIZE/4<sizeof(erabiltzaile_komando_izen[0])?erabiltzaile_komando_izen[kargu_INDIZE][INDIZE/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t sarrera_ZENBATU) {
    if (aktibo || sarrera_ZENBATU > 8) return (uint32_t)-22;
    전달인수개수 = sarrera_ZENBATU;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t BEGIRATU_INDIZE, uintptr_t 현재위치, uintptr_t byte_datuak) {
    if (aktibo || BEGIRATU_INDIZE >= 전달인수개수 || 현재위치 >= 255 || 현재위치 != 전달인수길이[BEGIRATU_INDIZE] || !byte_datuak || byte_datuak > 255)
        return (uint32_t)-22;
    전달인수[BEGIRATU_INDIZE][현재위치] = byte_datuak;
    전달인수길이[BEGIRATU_INDIZE] = 현재위치 + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t erloju_balio(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Stop_DENBORA_MUGA(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    gailu_izena_eman(IRQ_banatzailea + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void HASI_DENBORA_MUGA(void) {
    uint64_t 간격 = MAIZTASUNA * 2, gaitu = 1;
    마감시각 = erloju_balio() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(gaitu) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned datuak_blokeatu = 0; datuak_blokeatu < 4; datuak_blokeatu++) {
        erro_helbide[datuak_blokeatu] = (uintptr_t)가운데[datuak_blokeatu] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t helbide = ((uintptr_t)datuak_blokeatu << 30) | ((uintptr_t)순번 << 21);
            가운데[datuak_blokeatu][순번] = helbide | 1 | 접근표시 | erabiltzaile_ez_exekutatu;
            if (helbide >= 0xfc000000ul) 가운데[datuak_blokeatu][순번] |= ez_exekutatu_baimen; // Device-nGnRnE
            else 가운데[datuak_blokeatu][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned SEGUNDOA_balio = 0; SEGUNDOA_balio < erabiltzaile_orri_ZENBATU / 512; SEGUNDOA_balio++)
        가운데[0][(erabiltzaile_BASE >> 21) + SEGUNDOA_balio] = (uintptr_t)(orri_Zerrenda + SEGUNDOA_balio * 512) | 3;
    for (unsigned 순번 = 0; 순번 < erabiltzaile_orri_ZENBATU; 순번++) orri_Zerrenda[순번] = (erabiltzaile_BASE + 순번 * orrialdearen_tamaina) | nukleo_orri;
    uint64_t Memoria_atributu_izena_eman = 0x4400, helbide_Itzulpena_kontrol = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Memoria_atributu_izena_eman), "r"(helbide_Itzulpena_kontrol), "r"((uintptr_t)erro_helbide) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t mugikor_p_Egoera = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(mugikor_p_Egoera) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(MAIZTASUNA));
    Stop_DENBORA_MUGA();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 sarrera_p_balio 때만 Onartu_balio.
    gailu_izena_eman(IRQ_banatzailea) = 0;
    gailu_izena_eman(IRQ_banatzailea + 0x180) = 0xffffffff;
    gailu_izena_eman(IRQ_banatzailea + 0x80) = 0xffffffff;
    gailu_izena_eman(IRQ_banatzailea + 0x280) = 1u << 30;
    gailu_izena_eman(IRQ_banatzailea + 0x41c) = 0x80808080;
    gailu_izena_eman(IRQ_banatzailea + 0x100) = 1u << 30;
    gailu_izena_eman(IRQ_PUZ_interfaze + 4) = 0xff;
    gailu_izena_eman(IRQ_PUZ_interfaze + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 수 있다.
    int segurtasun = (gailu_izena_eman(IRQ_banatzailea + 4) & (1u << 10)) != 0;
    gailu_izena_eman(IRQ_banatzailea) = segurtasun ? 1 : 3;
    gailu_izena_eman(IRQ_PUZ_interfaze) = segurtasun ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t MOTA_Kategoria, gailu_MOTA; uint32_t 판번호;
    uint64_t sarrera_p, aplik_goiburu_Geruzak, atalaren_goiburu_Geruzak; uint32_t konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna;
    uint16_t 실행머리크기, 프로그램머리항목크기, aplik_goiburu_ZENBATU, 구역머리항목크기, atalaren_goiburu_ZENBATU, sekzio_izen_taula_INDIZE;
} 실행파일머리;
typedef struct { uint32_t MOTA_Kategoria, konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna; uint64_t Geruzak_balio, helbide, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(erabiltzaile_marko) == 272, "exception assembly layout");
static int 포함된범위(uint64_t Geruzak_balio, uint64_t Tamaina, uint64_t amaitu_Geruzak) {
    return Geruzak_balio <= amaitu_Geruzak && Tamaina <= amaitu_Geruzak - Geruzak_balio;
}
static int 부가정보검사(const unsigned char *datuak_kargu, size_t Tamaina) {
    size_t 현재위치 = 0;
    while (포함된범위(현재위치, 12, Tamaina)) {
        uint32_t 낱말들[3]; memcpy(낱말들, datuak_kargu + 현재위치, 12); 현재위치 += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(현재위치, 이름영역크기, Tamaina) || !포함된범위(현재위치 + 이름영역크기, 설명크기, Tamaina)) return 0;
        const unsigned char Izena[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Izena) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Izena); 순번++) if (datuak_kargu[현재위치 + 순번] != Izena[순번]) 일치 = 0;
        uint32_t 판번호 = 0;
        if (일치) memcpy(&판번호, datuak_kargu + 현재위치 + 이름영역크기, 4);
        if (일치 && 판번호 == 1) return 1;
        현재위치 += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *datuak, size_t Tamaina, int 리눅스방식) {
    if (Tamaina < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, datuak, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.MOTA_Kategoria != 2 || 실행머리.gailu_MOTA != 183 || 실행머리.판번호 != 1 || 실행머리.konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.프로그램머리항목크기 != sizeof(실행파일구획) || !실행머리.aplik_goiburu_ZENBATU || 실행머리.aplik_goiburu_ZENBATU > 16 ||
        실행머리.aplik_goiburu_Geruzak < sizeof(실행머리) || !포함된범위(실행머리.aplik_goiburu_Geruzak, (uint64_t)실행머리.aplik_goiburu_ZENBATU * sizeof(실행파일구획), Tamaina)) return 사용자실행파일오류;
    uint8_t 사용량[(erabiltzaile_irudi_amaitu - erabiltzaile_BASE) / orrialdearen_tamaina] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.aplik_goiburu_ZENBATU; 순번++) {
        실행파일구획 datuak_kargu; memcpy(&datuak_kargu, datuak + 실행머리.aplik_goiburu_Geruzak + 순번 * sizeof(datuak_kargu), sizeof(datuak_kargu));
        if (datuak_kargu.MOTA_Kategoria == 4) {
            if (!포함된범위(datuak_kargu.Geruzak_balio, datuak_kargu.파일영역크기, Tamaina)) return 사용자실행파일오류;
            if (부가정보검사(datuak + datuak_kargu.Geruzak_balio, datuak_kargu.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (datuak_kargu.MOTA_Kategoria == 0 || datuak_kargu.MOTA_Kategoria == 6 || (datuak_kargu.MOTA_Kategoria == 0x6474e551 && !(datuak_kargu.konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna & 1))) continue;
        if (datuak_kargu.MOTA_Kategoria != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!datuak_kargu.기억영역크기) continue;
        if (datuak_kargu.konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna & ~7u || !(datuak_kargu.konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna & 4) || (datuak_kargu.konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna & 3) == 3 || datuak_kargu.파일영역크기 > datuak_kargu.기억영역크기 ||
            (datuak_kargu.파일영역크기 && !포함된범위(datuak_kargu.Geruzak_balio, datuak_kargu.파일영역크기, Tamaina)) || datuak_kargu.helbide < erabiltzaile_BASE ||
            !포함된범위(datuak_kargu.helbide, datuak_kargu.기억영역크기, erabiltzaile_irudi_amaitu) ||
            (!리눅스방식 && ((datuak_kargu.helbide & (orrialdearen_tamaina - 1)) || (datuak_kargu.Geruzak_balio & (orrialdearen_tamaina - 1)) || datuak_kargu.맞춤 != orrialdearen_tamaina)) ||
            (리눅스방식 && (((datuak_kargu.helbide ^ datuak_kargu.Geruzak_balio) & (orrialdearen_tamaina - 1)) || !datuak_kargu.맞춤 ||
                (datuak_kargu.맞춤 & (datuak_kargu.맞춤 - 1)) || datuak_kargu.맞춤 > 0x200000 || ((datuak_kargu.helbide ^ datuak_kargu.Geruzak_balio) & (datuak_kargu.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (datuak_kargu.helbide - erabiltzaile_BASE) / orrialdearen_tamaina;
        unsigned sarrera_ZENBATU = ((datuak_kargu.helbide & (orrialdearen_tamaina - 1)) + datuak_kargu.기억영역크기 + orrialdearen_tamaina - 1) / orrialdearen_tamaina;
        for (unsigned orri_balio = 첫항목; orri_balio < 첫항목 + sarrera_ZENBATU; orri_balio++) {
            if (사용량[orri_balio]) return 사용자실행파일오류;
            사용량[orri_balio] = 1;
        }
        if ((datuak_kargu.konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna & 1) && 실행머리.sarrera_p >= datuak_kargu.helbide && 실행머리.sarrera_p < datuak_kargu.helbide + datuak_kargu.파일영역크기 && !(실행머리.sarrera_p & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *datuak, size_t Tamaina) { return 실행파일검사(datuak, Tamaina, 0); }
static void orriaren_diseinu(uintptr_t helbide, uint64_t konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna, unsigned baimenak) {
    unsigned BEGIRATU_INDIZE = (helbide - erabiltzaile_BASE) / orrialdearen_tamaina;
    orri_Zerrenda[BEGIRATU_INDIZE] = helbide | konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna;
    Baimenak_Zerrenda[BEGIRATU_INDIZE] = baimenak;
}
static int erabiltzaile_barruti(uintptr_t helbide, size_t sarrera_ZENBATU, int 쓰는중) {
    if (helbide < erabiltzaile_BASE || !포함된범위(helbide, sarrera_ZENBATU, erabiltzaile_amaitu)) return 0;
    if (!sarrera_ZENBATU) return 1;
    unsigned 첫항목 = (helbide - erabiltzaile_BASE) / orrialdearen_tamaina, 마지막 = (helbide + sarrera_ZENBATU - 1 - erabiltzaile_BASE) / orrialdearen_tamaina;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(Baimenak_Zerrenda[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int kopiatu_bide_izen(uintptr_t helbide, char *Bide_izena) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!erabiltzaile_barruti(helbide, 1, 0)) return -14;
        Bide_izena[순번] = *(const char *)helbide++;
        if (!Bide_izena[순번]) return 0;
    }
    return -36;
}
static intptr_t nukleo_neurria(intptr_t EMAITZA) { return EMAITZA < 0 ? -errorearen_zenbaki : EMAITZA; }
static int 대응파일기술자(uint64_t fitxategi_helduleku) { return fitxategi_helduleku >= 3 && fitxategi_helduleku < 19 ? fitxategi_Zerrenda[fitxategi_helduleku - 3] : -1; }
static int 통신끝점소유(uint64_t fitxategi_helduleku) { return fitxategi_helduleku >= 32 && fitxategi_helduleku < 56 && 통신끝점들[fitxategi_helduleku - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t luzera_balio, struct pk_sockaddr_in *helbide) {
    if (luzera_balio != sizeof(*helbide)) return -22;
    if (!erabiltzaile_barruti(가리킴값, luzera_balio, 0)) return -14;
    memcpy(helbide, (const void *)가리킴값, sizeof(*helbide));
    return helbide->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t luzera_erakusle, pk_socklen_t *buffer_ahalmen) {
    if (!erabiltzaile_barruti(luzera_erakusle, sizeof(*buffer_ahalmen), 1)) return -14;
    memcpy(buffer_ahalmen, (const void *)luzera_erakusle, sizeof(*buffer_ahalmen));
    if (*buffer_ahalmen > sizeof(struct pk_sockaddr_in)) *buffer_ahalmen = sizeof(struct pk_sockaddr_in);
    if (*buffer_ahalmen && !erabiltzaile_barruti(가리킴값, *buffer_ahalmen, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t luzera_erakusle, pk_socklen_t buffer_ahalmen, int helbide, int ataka_zenbaki) {
    struct pk_sockaddr_in balio; memset(&balio, 0, sizeof(balio));
    balio.sin_family = AF_INET; balio.sin_port = pk_htons(ataka_zenbaki); balio.sin_addr.s_addr = pk_htonl(helbide);
    if (buffer_ahalmen) memcpy((void *)가리킴값, &balio, buffer_ahalmen);
    pk_socklen_t luzera_balio = sizeof(balio); memcpy((void *)luzera_erakusle, &luzera_balio, sizeof(luzera_balio));
}
extern uintptr_t arbel_kanal(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(erabiltzaile_marko *fitxategi_sarrera) {
    uintptr_t 첫째값 = fitxategi_sarrera->izena_eman_datuak[0], SEGUNDOA_balio = fitxategi_sarrera->izena_eman_datuak[1], karaktere_kode = fitxategi_sarrera->izena_eman_datuak[2];
    char Bide_izena[65];
    int fitxategi_helduleku, EMAITZA;
    switch (fitxategi_sarrera->izena_eman_datuak[8]) {
    case 0: return 1; // 자체 ABI 버전
    case 1: // write: erakusle 전체를 검사한 ATZERA_balio Irteera/Fitxategia aldatu_balio
        if (karaktere_kode > 65536) return -22;
        if (!erabiltzaile_barruti(SEGUNDOA_balio, karaktere_kode, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=erloju_balio();
            for (size_t 순번 = 0; 순번 < karaktere_kode; 순번++) arbel_kanal(첫째값, ((const unsigned char *)SEGUNDOA_balio)[순번]);
            /* 큰 tty를 그린 nukleo_balio 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(interaktibo){
                마감시각+=erloju_balio()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(마감시각) : "memory");
            }
            return karaktere_kode;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t elementu_ZENBATU=karaktere_kode>512?512:karaktere_kode;for(size_t 순번=0;순번<elementu_ZENBATU;순번++)자바전문넣기(순번,((const unsigned char *)SEGUNDOA_balio)[순번]);return 자바흐름쓰기(첫째값,elementu_ZENBATU);
        }
        fitxategi_helduleku = 대응파일기술자(첫째값); if (fitxategi_helduleku < 0) return -9;
        return nukleo_neurria(pk_write(fitxategi_helduleku, (const void *)SEGUNDOA_balio, karaktere_kode));
    case 2:
        if (karaktere_kode > 65536) return -22;
        if (!erabiltzaile_barruti(SEGUNDOA_balio, karaktere_kode, 1)) return -14;
        if (첫째값 == 0) {
            size_t elementu_ZENBATU = 0;
            while (elementu_ZENBATU < karaktere_kode) {
                int karaktere_balio = (int32_t)보드글자읽기(); if (karaktere_balio == -2) return elementu_ZENBATU; if (karaktere_balio < 0) break;
                ((unsigned char *)SEGUNDOA_balio)[elementu_ZENBATU++] = karaktere_balio;
            }
            return elementu_ZENBATU ? (intptr_t)elementu_ZENBATU : (karaktere_kode ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            EMAITZA=자바흐름읽기(첫째값,karaktere_kode>512?512:karaktere_kode);if(EMAITZA>0)for(int 순번=0;순번<EMAITZA;순번++)((unsigned char *)SEGUNDOA_balio)[순번]=자바전문얻기(순번);return EMAITZA;
        }
        fitxategi_helduleku = 대응파일기술자(첫째값); if (fitxategi_helduleku < 0) return -9;
        return nukleo_neurria(pk_read(fitxategi_helduleku, (void *)SEGUNDOA_balio, karaktere_kode));
    case 3:
        EMAITZA = kopiatu_bide_izen(첫째값, Bide_izena); if (EMAITZA) return EMAITZA;
        if (SEGUNDOA_balio > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (fitxategi_Zerrenda[순번] < 0) {
            fitxategi_helduleku = pk_open(Bide_izena, (int)SEGUNDOA_balio, 0600);
            if (fitxategi_helduleku < 0) return -errorearen_zenbaki;
            fitxategi_Zerrenda[순번] = fitxategi_helduleku; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { EMAITZA = 통신끝점닫기(첫째값); if (!EMAITZA) 통신끝점들[첫째값 - 32] = 0; return EMAITZA; }
        fitxategi_helduleku = 대응파일기술자(첫째값); if (fitxategi_helduleku < 0) return -9;
        EMAITZA = pk_close(fitxategi_helduleku); if (!EMAITZA) fitxategi_Zerrenda[첫째값 - 3] = -1;
        return nukleo_neurria(EMAITZA);
    case 5:
        fitxategi_helduleku = 대응파일기술자(첫째값); if (fitxategi_helduleku < 0) return -9;
        if (karaktere_kode > 2) return -22;
        return nukleo_neurria(pk_lseek(fitxategi_helduleku, (int64_t)SEGUNDOA_balio, karaktere_kode));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 erabiltzaile RW/NX 힙, 새로 노출되는 페이지는 0으로 hasieratu
        if (!첫째값) return 동적기억끝;
        if (첫째값 < erabiltzaile_irudi_amaitu || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + orrialdearen_tamaina - 1) & ~(orrialdearen_tamaina - 1);
        uintptr_t 새쪽들 = (첫째값 + orrialdearen_tamaina - 1) & ~(orrialdearen_tamaina - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t datuak_kargu = 이전쪽들; datuak_kargu < 새쪽들; datuak_kargu += orrialdearen_tamaina) orriaren_diseinu(datuak_kargu, nukleo_orri, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t datuak_kargu = 이전쪽들; datuak_kargu < 새쪽들; datuak_kargu += orrialdearen_tamaina) orriaren_diseinu(datuak_kargu, erabiltzaile_irakurri_idatzi, 3);
        } else {
            for (uintptr_t datuak_kargu = 새쪽들; datuak_kargu < 이전쪽들; datuak_kargu += orrialdearen_tamaina) {
                orri_Zerrenda[(datuak_kargu - erabiltzaile_BASE) / orrialdearen_tamaina] = 0; Baimenak_Zerrenda[(datuak_kargu - erabiltzaile_BASE) / orrialdearen_tamaina] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        fitxategi_helduleku = 대응파일기술자(첫째값); return fitxategi_helduleku < 0 ? -9 : nukleo_neurria(pk_size(fitxategi_helduleku));
    case 10:
        fitxategi_helduleku = 대응파일기술자(첫째값); return fitxategi_helduleku < 0 ? -9 : nukleo_neurria(pk_ftruncate(fitxategi_helduleku, (int64_t)SEGUNDOA_balio));
    case 11:
        EMAITZA = kopiatu_bide_izen(첫째값, Bide_izena); return EMAITZA ? EMAITZA : nukleo_neurria(pk_unlink(Bide_izena));
    case 12:
        fitxategi_helduleku = 대응파일기술자(첫째값); return fitxategi_helduleku < 0 ? -9 : nukleo_neurria(pk_fsync(fitxategi_helduleku));
    case 13: { // 그래픽 기초 API: erabiltzaile 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = fitxategi_sarrera->izena_eman_datuak[3], 높이값 = fitxategi_sarrera->izena_eman_datuak[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SEGUNDOA_balio > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - SEGUNDOA_balio) return -22;
        for (uintptr_t Y_koordenatu = SEGUNDOA_balio; Y_koordenatu < SEGUNDOA_balio + 높이값; Y_koordenatu++) for (uintptr_t X_koordenatu = 첫째값; X_koordenatu < 첫째값 + 너비값; X_koordenatu++) arbel_pixel(X_koordenatu, Y_koordenatu, karaktere_kode);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=elementu_ZENBATU; args(index,buffer,capacity)=UTF-8 luzera_balio
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (karaktere_kode <= 전달인수길이[첫째값]) return -36;
        if (!erabiltzaile_barruti(SEGUNDOA_balio, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SEGUNDOA_balio, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;interaktibo=1;return arbel_Terminal(13);}
        if(첫째값==2){interaktibo=0;return 0;}
        if(첫째값==3)return arbel_Terminal(13);
        if(첫째값!=1||!interaktibo)return -22;
        EMAITZA=(int32_t)보드글자읽기();
        if(EMAITZA==-4096)return EMAITZA;
        HASI_DENBORA_MUGA();return EMAITZA<0?-11:EMAITZA;
    case 17: { // 유한한 협력 itxaron_balio: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t amaitu_ordua = erloju_balio() + MAIZTASUNA * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (erloju_balio() < amaitu_ordua);
        HASI_DENBORA_MUGA(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 부모·빈 폴더를 검사한다.
        if (SEGUNDOA_balio > 2) return -22;
        EMAITZA = kopiatu_bide_izen(첫째값, Bide_izena); if (EMAITZA) return EMAITZA;
        unsigned luzera_balio = 0; while (Bide_izena[luzera_balio]) luzera_balio++;
        EMAITZA = 자바경로시작(luzera_balio); if (EMAITZA < 0) return EMAITZA;
        for (unsigned 순번 = 0; 순번 < luzera_balio; 순번++) 자바경로바이트(순번, (unsigned char)Bide_izena[순번]);
        return SEGUNDOA_balio == 0 ? 자바항목종류() : SEGUNDOA_balio == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int karaktere_balio=(int32_t)보드글자읽기();if(karaktere_balio==-4096)return karaktere_balio;if(karaktere_balio>=0)화면누름(jabe_objektu,karaktere_balio);HASI_DENBORA_MUGA();}
        if(첫째값==3&&karaktere_kode){if(!자바셸대화형())return -95;interaktibo=1;arbel_Terminal(300);}
        return 화면호출(jabe_objektu,첫째값,SEGUNDOA_balio,karaktere_kode,fitxategi_sarrera->izena_eman_datuak[3],fitxategi_sarrera->izena_eman_datuak[4],fitxategi_sarrera->izena_eman_datuak[5]);
    case 21:
        if(karaktere_kode>127)return -22;if(!erabiltzaile_barruti(SEGUNDOA_balio,karaktere_kode*sizeof(uint32_t),0))return -14;
        return 화면글(jabe_objektu,첫째값,(const uint32_t *)SEGUNDOA_balio,karaktere_kode);
    case 22: // 화면 Tamaina kontsulta_balio: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SEGUNDOA_balio==SOCK_STREAM&&(karaktere_kode==0||karaktere_kode==6))EMAITZA=자바흐름만들기();
        else if(SEGUNDOA_balio==SOCK_DGRAM&&(karaktere_kode==0||karaktere_kode==IPPROTO_UDP))EMAITZA=자바전문만들기(첫째값,SEGUNDOA_balio,karaktere_kode);
        else return -93;
        if (EMAITZA >= 32 && EMAITZA < 56) 통신끝점들[EMAITZA - 32] = 1;
        return EMAITZA;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in helbide;
        EMAITZA = 주소입력(SEGUNDOA_balio, karaktere_kode, &helbide); if (EMAITZA) return EMAITZA;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(helbide.sin_addr.s_addr),pk_htons(helbide.sin_port)):자바전문묶기(첫째값, pk_htonl(helbide.sin_addr.s_addr), pk_htons(helbide.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (fitxategi_sarrera->izena_eman_datuak[3]) return -95;
        if (karaktere_kode > 512) return -90;
        if (karaktere_kode && !erabiltzaile_barruti(SEGUNDOA_balio, karaktere_kode, 0)) return -14;
        struct pk_sockaddr_in helbide;
        EMAITZA = 주소입력(fitxategi_sarrera->izena_eman_datuak[4], fitxategi_sarrera->izena_eman_datuak[5], &helbide); if (EMAITZA) return EMAITZA;
        for (unsigned 순번 = 0; 순번 < karaktere_kode; 순번++) 자바전문넣기(순번, ((const unsigned char *)SEGUNDOA_balio)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(helbide.sin_addr.s_addr), pk_htons(helbide.sin_port), karaktere_kode);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (fitxategi_sarrera->izena_eman_datuak[3]) return -95;
        if (karaktere_kode > 512) return -90;
        if (karaktere_kode && !erabiltzaile_barruti(SEGUNDOA_balio, karaktere_kode, 1)) return -14;
        pk_socklen_t buffer_ahalmen = 0;
        if (fitxategi_sarrera->izena_eman_datuak[4]) { EMAITZA = 주소출력검사(fitxategi_sarrera->izena_eman_datuak[4], fitxategi_sarrera->izena_eman_datuak[5], &buffer_ahalmen); if (EMAITZA) return EMAITZA; }
        EMAITZA = 자바전문받기(첫째값, karaktere_kode); if (EMAITZA < 0) return EMAITZA;
        for (int 순번 = 0; 순번 < EMAITZA; 순번++) ((unsigned char *)SEGUNDOA_balio)[순번] = 자바전문얻기(순번);
        if (fitxategi_sarrera->izena_eman_datuak[4]) 주소출력(fitxategi_sarrera->izena_eman_datuak[4], fitxategi_sarrera->izena_eman_datuak[5], buffer_ahalmen, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return EMAITZA;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t buffer_ahalmen;
        EMAITZA = 주소출력검사(SEGUNDOA_balio, karaktere_kode, &buffer_ahalmen); if (EMAITZA) return EMAITZA;
        주소출력(SEGUNDOA_balio,karaktere_kode,buffer_ahalmen,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in helbide;
        EMAITZA=주소입력(SEGUNDOA_balio,karaktere_kode,&helbide);if(EMAITZA)return EMAITZA;
        return 자바흐름연결(첫째값,pk_htonl(helbide.sin_addr.s_addr),pk_htons(helbide.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,SEGUNDOA_balio):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(SEGUNDOA_balio||karaktere_kode)return -95;EMAITZA=자바흐름연결받기(첫째값);if(EMAITZA>=40&&EMAITZA<56)통신끝점들[EMAITZA-32]=1;return EMAITZA;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(erabiltzaile_marko *fitxategi_sarrera) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(fitxategi_sarrera) : 자체체계호출(fitxategi_sarrera);
}
static void itzuli_nukleo(erabiltzaile_marko *fitxategi_sarrera, int EMAITZA) {
    Stop_DENBORA_MUGA();
    fitxategi_sarrera->izena_eman_datuak[0] = (uint64_t)(int64_t)EMAITZA;
    fitxategi_sarrera->komando_kargu = (uintptr_t)erabiltzaile_itzuli;
    fitxategi_sarrera->Egoera_KODE = 0x3c5; // EL1h, DAIF masked
}
int erabiltzaile_salbuespen(erabiltzaile_marko *fitxategi_sarrera, unsigned EBAKIDURA) {
    if (!aktibo || (fitxategi_sarrera->Egoera_KODE & 15) != 0) return 0;
    if (EBAKIDURA) {
        uint32_t 승인값 = gailu_izena_eman(IRQ_PUZ_interfaze + 0xc), identifikatzaile_balio = 승인값 & 1023;
        if (identifikatzaile_balio == 30) { itzuli_nukleo(fitxategi_sarrera, erabiltzaile_DENBORA_MUGA); gailu_izena_eman(IRQ_PUZ_interfaze + 0x10) = 승인값; return 1; }
        if (identifikatzaile_balio < 1020) gailu_izena_eman(IRQ_PUZ_interfaze + 0x10) = 승인값;
        return 1;
    }
    uint64_t salbuespen_Egoera; __asm__ volatile("mrs %0, esr_el1" : "=r"(salbuespen_Egoera));
    if (erloju_balio() >= 마감시각) { itzuli_nukleo(fitxategi_sarrera, erabiltzaile_DENBORA_MUGA); return 1; }
    unsigned salbuespen_Kategoria = salbuespen_Egoera >> 26;
    if (salbuespen_Kategoria == 0x15 && (salbuespen_Egoera & 0xffff) == 0) {
        if (리눅스규약 ? fitxategi_sarrera->izena_eman_datuak[8] == 93 || fitxategi_sarrera->izena_eman_datuak[8] == 94 : fitxategi_sarrera->izena_eman_datuak[8] == 6) itzuli_nukleo(fitxategi_sarrera, (int)(fitxategi_sarrera->izena_eman_datuak[0] & 255));
        else {
            intptr_t EMAITZA=체계호출(fitxategi_sarrera);
            if(EMAITZA==-4096&&interaktibo){
                저장값[jabe_objektu].실행틀=*fitxategi_sarrera;저장값[jabe_objektu].실행틀.komando_kargu-=4;
                사용자실수보관(저장값[jabe_objektu].mugikor_p_Egoera);itzuli_nukleo(fitxategi_sarrera,사용자중단됨);
            }else fitxategi_sarrera->izena_eman_datuak[0]=(uint64_t)EMAITZA;
        }
    } else itzuli_nukleo(fitxategi_sarrera, salbuespen_Kategoria == 0x24 ? erabiltzaile_datuak_errore : salbuespen_Kategoria == 0x20 ? 사용자실행오류 : erabiltzaile_baliogabe_instrukzio);
    return 1;
}

// 생성된 const ELF talde_balio: 실행은 반드시 aplik_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *datuak; size_t Tamaina; unsigned 전달값; } aplik;
#include "programs.h"
static void *argazki(unsigned kargu_INDIZE){return (void *)(0x04000000ul+kargu_INDIZE*(erabiltzaile_amaitu-erabiltzaile_BASE));}
static int Amaitu_aplik(int EMAITZA){
    사용자누적시각[jabe_objektu]+=(uint32_t)보드밀리초()-사용자실행시각[jabe_objektu];
    Stop_DENBORA_MUGA();aktibo=0;
    if(EMAITZA==사용자중단됨){
        저장된작업 *kate_datuak=&저장값[jabe_objektu];kate_datuak->멈춤상태=1;kate_datuak->interaktibo=interaktibo;kate_datuak->리눅스규약=리눅스규약;kate_datuak->동적기억공간=동적기억끝;kate_datuak->인수개수=전달인수개수;
        memcpy(kate_datuak->Baimenak_Zerrenda,Baimenak_Zerrenda,sizeof(Baimenak_Zerrenda));memcpy(kate_datuak->fitxategi_Zerrenda,fitxategi_Zerrenda,sizeof(fitxategi_Zerrenda));memcpy(kate_datuak->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(kate_datuak->arg_matrize,전달인수,sizeof(전달인수));memcpy(kate_datuak->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<erabiltzaile_orri_ZENBATU;순번++)if(Baimenak_Zerrenda[순번])memcpy((unsigned char *)argazki(jabe_objektu)+순번*orrialdearen_tamaina,(void *)(erabiltzaile_BASE+순번*orrialdearen_tamaina),orrialdearen_tamaina);
    }else{
        저장값[jabe_objektu].멈춤상태=0;화면초기화(jabe_objektu);
        for(unsigned 순번=0;순번<16;순번++)if(fitxategi_Zerrenda[순번]>=0)pk_close(fitxategi_Zerrenda[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<erabiltzaile_orri_ZENBATU;순번++){orri_Zerrenda[순번]=0;Baimenak_Zerrenda[순번]=0;}변환표맞추기();return EMAITZA;
}
uintptr_t arbel_erabiltzaile_kontrola(uintptr_t Ekintza){
    unsigned kargu_INDIZE=Ekintza&15;if(kargu_INDIZE>=4||aktibo)return (uint32_t)-22;
    저장된작업 *kate_datuak=&저장값[kargu_INDIZE];
    if(Ekintza>=32){if(kate_datuak->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(kate_datuak->fitxategi_Zerrenda[순번]>=0)pk_close(kate_datuak->fitxategi_Zerrenda[순번]);for(unsigned 순번=0;순번<24;순번++)if(kate_datuak->통신끝점들[순번])통신끝점닫기(순번+32);}kate_datuak->멈춤상태=0;화면초기화(kargu_INDIZE);return 0;}
    if(Ekintza>=16)return kate_datuak->멈춤상태;
    if(!kate_datuak->멈춤상태)return (uint32_t)-22;
    jabe_objektu=kargu_INDIZE;interaktibo=kate_datuak->interaktibo;리눅스규약=kate_datuak->리눅스규약;동적기억끝=kate_datuak->동적기억공간;전달인수개수=kate_datuak->인수개수;
    memcpy(fitxategi_Zerrenda,kate_datuak->fitxategi_Zerrenda,sizeof(fitxategi_Zerrenda));memcpy(통신끝점들,kate_datuak->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,kate_datuak->arg_matrize,sizeof(전달인수));memcpy(전달인수길이,kate_datuak->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<erabiltzaile_orri_ZENBATU;순번++)orri_Zerrenda[순번]=(erabiltzaile_BASE+순번*orrialdearen_tamaina)|nukleo_orri;변환표맞추기();
    memset((void *)erabiltzaile_BASE,0,erabiltzaile_amaitu-erabiltzaile_BASE);
    for(unsigned 순번=0;순번<erabiltzaile_orri_ZENBATU;순번++)if(kate_datuak->Baimenak_Zerrenda[순번])memcpy((void *)(erabiltzaile_BASE+순번*orrialdearen_tamaina),(unsigned char *)argazki(kargu_INDIZE)+순번*orrialdearen_tamaina,orrialdearen_tamaina);
    memcpy(Baimenak_Zerrenda,kate_datuak->Baimenak_Zerrenda,sizeof(Baimenak_Zerrenda));
    for(unsigned 순번=0;순번<erabiltzaile_orri_ZENBATU;순번++){unsigned datuak_kargu=Baimenak_Zerrenda[순번];orri_Zerrenda[순번]=datuak_kargu?(erabiltzaile_BASE+순번*orrialdearen_tamaina)|(datuak_kargu==3?erabiltzaile_irakurri_idatzi:datuak_kargu==5?사용자읽고실행:erabiltzaile_irakurtzeko_soilik):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");aktibo=1;kate_datuak->멈춤상태=0;HASI_DENBORA_MUGA();
    사용자실행시각[jabe_objektu]=보드밀리초();
    return (uint32_t)Amaitu_aplik(erabiltzaile_CV(&kate_datuak->실행틀,kate_datuak->mugikor_p_Egoera));
}
static int exekutatu_aplik(const unsigned char *datuak, size_t Tamaina, unsigned 전달값, int 리눅스방식, const char *Izena) {
    if (aktibo) return -16;
    jabe_objektu=arbel_Terminal(11);if(jabe_objektu<0||jabe_objektu>3||저장값[jabe_objektu].멈춤상태)return -16;interaktibo=0;
    int 유효함 = 실행파일검사(datuak, Tamaina, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned izen_INDIZE=0;
    while (*Izena && izen_INDIZE<31) erabiltzaile_komando_izen[jabe_objektu][izen_INDIZE++]=(unsigned char)*Izena++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (izen_INDIZE) erabiltzaile_komando_izen[jabe_objektu][izen_INDIZE++]=' ';
        for (unsigned kargu_INDIZE=0; kargu_INDIZE<전달인수길이[0]; kargu_INDIZE++) erabiltzaile_komando_izen[jabe_objektu][izen_INDIZE++]=전달인수[0][kargu_INDIZE];
    }
    erabiltzaile_komando_izen[jabe_objektu][izen_INDIZE]=0; erabiltzaile_zenbaki[jabe_objektu]=Hurrengoa_erabiltzaile_zenbaki++;
    if (Hurrengoa_erabiltzaile_zenbaki>0x7fffffffu) Hurrengoa_erabiltzaile_zenbaki=10;
    erabiltzaile_HASI_ordua[jabe_objektu]=보드밀리초(); 사용자누적시각[jabe_objektu]=0;
    for (unsigned 순번 = 0; 순번 < erabiltzaile_orri_ZENBATU; 순번++) orri_Zerrenda[순번] = (erabiltzaile_BASE + 순번 * orrialdearen_tamaina) | nukleo_orri;
    변환표맞추기();
    memset((void *)erabiltzaile_BASE, 0, erabiltzaile_amaitu - erabiltzaile_BASE);
    memset(Baimenak_Zerrenda, 0, sizeof(Baimenak_Zerrenda));
    실행파일머리 실행머리; memcpy(&실행머리, datuak, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.aplik_goiburu_ZENBATU; 순번++) {
        실행파일구획 datuak_kargu; memcpy(&datuak_kargu, datuak + 실행머리.aplik_goiburu_Geruzak + 순번 * sizeof(datuak_kargu), sizeof(datuak_kargu));
        if (datuak_kargu.MOTA_Kategoria != 1 || !datuak_kargu.기억영역크기) continue;
        if (datuak_kargu.파일영역크기) memcpy((void *)(uintptr_t)datuak_kargu.helbide, datuak + datuak_kargu.Geruzak_balio, datuak_kargu.파일영역크기);
        for (uintptr_t 현재위치 = datuak_kargu.helbide & ~(orrialdearen_tamaina - 1); 현재위치 < datuak_kargu.helbide + datuak_kargu.기억영역크기; 현재위치 += orrialdearen_tamaina) {
            Baimenak_Zerrenda[(현재위치 - erabiltzaile_BASE) / orrialdearen_tamaina] = (datuak_kargu.konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna & 2) ? 3 : ((datuak_kargu.konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna & 1) ? 5 : 1);
        }
    }
    for (uintptr_t 현재위치 = erabiltzaile_pila_helbide; 현재위치 < erabiltzaile_amaitu; 현재위치 += orrialdearen_tamaina) Baimenak_Zerrenda[(현재위치 - erabiltzaile_BASE) / orrialdearen_tamaina] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.sarrera_p) : erabiltzaile_amaitu;
    for (unsigned 순번 = 0; 순번 < erabiltzaile_orri_ZENBATU; 순번++) {
        unsigned baimenak = Baimenak_Zerrenda[순번];
        orri_Zerrenda[순번] = baimenak ? (erabiltzaile_BASE + 순번 * orrialdearen_tamaina) | (baimenak == 3 ? erabiltzaile_irakurri_idatzi : baimenak == 5 ? 사용자읽고실행 : erabiltzaile_irakurtzeko_soilik) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) fitxategi_Zerrenda[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = erabiltzaile_irudi_amaitu;
    aktibo = 1; HASI_DENBORA_MUGA();
    사용자실행시각[jabe_objektu]=보드밀리초();
    int EMAITZA = erabiltzaile_sartu(실행머리.sarrera_p, 초기쌓임공간, 전달값);
    return Amaitu_aplik(EMAITZA);
}
uintptr_t arbel_erabiltzaile_exekutatu(uintptr_t BEGIRATU_INDIZE) {
    if (BEGIRATU_INDIZE >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Izena=BEGIRATU_INDIZE==10?"javac":BEGIRATU_INDIZE==11?"java":BEGIRATU_INDIZE==12?"python":BEGIRATU_INDIZE==13?"vi":BEGIRATU_INDIZE==14?"jar":BEGIRATU_INDIZE==15?"cc":BEGIRATU_INDIZE==16?"jaot":"ELF";
    return (uint32_t)exekutatu_aplik(실행항목들[BEGIRATU_INDIZE].datuak, 실행항목들[BEGIRATU_INDIZE].Tamaina, 실행항목들[BEGIRATU_INDIZE].전달값, 0, Izena);
}
static uintptr_t exekutatu_fitxategi(int 리눅스방식) {
    static unsigned char irudi[16384];
    if (aktibo || !전달인수개수) return (uint32_t)-22;
    int fitxategi_helduleku = pk_open((const char *)전달인수[0], irakurtzeko_soilik_balio, 0);
    if (fitxategi_helduleku < 0) return (uint32_t)-errorearen_zenbaki;
    int Tamaina = pk_size(fitxategi_helduleku);
    if (Tamaina < 0 || (unsigned)Tamaina > sizeof(irudi)) { pk_close(fitxategi_helduleku); return (uint32_t)-27; }
    int RECEIVED_ZENBATU = pk_read(fitxategi_helduleku, irudi, Tamaina); pk_close(fitxategi_helduleku);
    if (RECEIVED_ZENBATU != Tamaina) return (uint32_t)-5;
    return (uint32_t)exekutatu_aplik(irudi, Tamaina, 0, 리눅스방식, "");
}
uintptr_t arbel_erabiltzaile_fitxategi(void) { return exekutatu_fitxategi(0); }
uintptr_t 보드사용자리눅스파일(void) { return exekutatu_fitxategi(1); }
uintptr_t arbel_erabiltzaile_baliozkotu(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].datuak, 잘못된실행항목들[순번].Tamaina) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
