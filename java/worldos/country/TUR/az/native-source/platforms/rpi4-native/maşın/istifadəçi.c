#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 icra_etmək_əmr maşın lay_VALUE. FAYL verilənlər/정책은 기존 AOT Java 커널에 위임한다.
#include "istifadəçi.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../Şəbəkə_Yığın/Şəbəkə_Yığın.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define maşın_qeydiyyatdan_keçmək(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_distribyutor 0xff841000ul
#define IRQ_CPU_interfeys 0xff842000ul
#define səhifənin_ölçüsü 4096ul
#define 접근표시 (1ul << 10)
#define xeyr_icra_etmək_icazə (1ul << 53)
#define istifadəçi_xeyr_icra_etmək (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | 접근표시)
#define nüvə_səhifə (3ul | 보통기억 | xeyr_icra_etmək_icazə | istifadəçi_xeyr_icra_etmək)
#define istifadəçi_oxunan_yazılan (3ul | 보통기억 | (1ul << 6) | xeyr_icra_etmək_icazə | istifadəçi_xeyr_icra_etmək)
#define istifadəçi_yalnız_oxunan (3ul | 보통기억 | (3ul << 6) | xeyr_icra_etmək_icazə | istifadəçi_xeyr_icra_etmək)
#define 사용자읽고실행 (3ul | 보통기억 | (3ul << 6) | xeyr_icra_etmək_icazə)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t lövhə_piksel(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t lövhə_Terminal(uintptr_t);
extern int Terminal_gözləyir(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int istifadəçi_CV(istifadəçi_kadr *,void *);
extern void 사용자실수보관(void *);
extern int istifadəçi_daxil_etmək(uintptr_t daxiletmə_p, uintptr_t Yığın_Yaddaş, uintptr_t 전달값);
extern void istifadəçi_geri_qaytarmaq(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t kök_ünvan[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t səhifə_Siyahı[istifadəçi_səhifə_COUNT] __attribute__((aligned(4096)));
static uint8_t icazələr_Siyahı[istifadəçi_səhifə_COUNT];
static int Aktiv, fayl_Siyahı[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned fayl_tutacaq){return fayl_tutacaq<40?자바전문닫기(fayl_tutacaq):자바흐름닫기(fayl_tutacaq);}
static uint64_t FREQUENCY, 마감시각;
static uintptr_t 동적기억끝;
// nüvə_VALUE 셸이 준비한 UTF-8 인수. EL0에는 nümunə_VALUE 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,interaktiv,리눅스규약,fayl_Siyahı[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char arqument_ARRAY[8][256],icazələr_Siyahı[istifadəçi_səhifə_COUNT];
    uintptr_t 동적기억공간; istifadəçi_kadr 실행틀;
    unsigned char 실수저장상태[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int sahib_obyekt,interaktiv;
static uint32_t istifadəçi_nömrəsi[4], istifadəçi_Başla_TIME[4], 사용자누적시각[4], 사용자실행시각[4], Sonrakı_istifadəçi_nömrəsi=10;
static unsigned char istifadəçi_əmr_ad[4][288];
uint32_t 사용자상태읽기(unsigned daxiletmə_VALUE, unsigned INDEX) {
    unsigned yerinə_qoymaq_INDEX=INDEX&3;
    int vəziyyət_VALUE=(Aktiv && sahib_obyekt==(int)yerinə_qoymaq_INDEX) ? 1 : 저장값[yerinə_qoymaq_INDEX].멈춤상태 ? 2 : 0;
    if (daxiletmə_VALUE==0) return vəziyyət_VALUE;
    if (!vəziyyət_VALUE) return 0;
    if (daxiletmə_VALUE==1) return istifadəçi_nömrəsi[yerinə_qoymaq_INDEX];
    if (daxiletmə_VALUE==2) {
        unsigned char *쪽들=vəziyyət_VALUE==1?icazələr_Siyahı:저장값[yerinə_qoymaq_INDEX].icazələr_Siyahı;
        unsigned səhifə_COUNT=0; for (unsigned 순번=0; 순번<istifadəçi_səhifə_COUNT; 순번++) if(쪽들[순번]) səhifə_COUNT++;
        return səhifə_COUNT*4;
    }
    if (daxiletmə_VALUE==3) return (uint32_t)보드밀리초()-istifadəçi_Başla_TIME[yerinə_qoymaq_INDEX];
    if (daxiletmə_VALUE==4) return 사용자누적시각[yerinə_qoymaq_INDEX]+(vəziyyət_VALUE==1?(uint32_t)보드밀리초()-사용자실행시각[yerinə_qoymaq_INDEX]:0);
    if (daxiletmə_VALUE==5) return INDEX/4<sizeof(istifadəçi_əmr_ad[0])?istifadəçi_əmr_ad[yerinə_qoymaq_INDEX][INDEX/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t daxiletmə_COUNT) {
    if (Aktiv || daxiletmə_COUNT > 8) return (uint32_t)-22;
    전달인수개수 = daxiletmə_COUNT;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t LOOKUP_INDEX, uintptr_t 현재위치, uintptr_t bayt_verilənlər) {
    if (Aktiv || LOOKUP_INDEX >= 전달인수개수 || 현재위치 >= 255 || 현재위치 != 전달인수길이[LOOKUP_INDEX] || !bayt_verilənlər || bayt_verilənlər > 255)
        return (uint32_t)-22;
    전달인수[LOOKUP_INDEX][현재위치] = bayt_verilənlər;
    전달인수길이[LOOKUP_INDEX] = 현재위치 + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Saat_VALUE(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Dayandır_FASİLƏ(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    maşın_qeydiyyatdan_keçmək(IRQ_distribyutor + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void Başla_FASİLƏ(void) {
    uint64_t 간격 = FREQUENCY * 2, aktivləşdirmək = 1;
    마감시각 = Saat_VALUE() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(aktivləşdirmək) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned verilənlər_blokla = 0; verilənlər_blokla < 4; verilənlər_blokla++) {
        kök_ünvan[verilənlər_blokla] = (uintptr_t)가운데[verilənlər_blokla] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t ünvan = ((uintptr_t)verilənlər_blokla << 30) | ((uintptr_t)순번 << 21);
            가운데[verilənlər_blokla][순번] = ünvan | 1 | 접근표시 | istifadəçi_xeyr_icra_etmək;
            if (ünvan >= 0xfc000000ul) 가운데[verilənlər_blokla][순번] |= xeyr_icra_etmək_icazə; // Device-nGnRnE
            else 가운데[verilənlər_blokla][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned SECOND_VALUE = 0; SECOND_VALUE < istifadəçi_səhifə_COUNT / 512; SECOND_VALUE++)
        가운데[0][(istifadəçi_BASE >> 21) + SECOND_VALUE] = (uintptr_t)(səhifə_Siyahı + SECOND_VALUE * 512) | 3;
    for (unsigned 순번 = 0; 순번 < istifadəçi_səhifə_COUNT; 순번++) səhifə_Siyahı[순번] = (istifadəçi_BASE + 순번 * səhifənin_ölçüsü) | nüvə_səhifə;
    uint64_t Yaddaş_atribut_qeydiyyatdan_keçmək = 0x4400, ünvan_Tərcümə_nəzarət = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Yaddaş_atribut_qeydiyyatdan_keçmək), "r"(ünvan_Tərcümə_nəzarət), "r"((uintptr_t)kök_ünvan) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t 실수저장상태 = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(실수저장상태) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    Dayandır_FASİLƏ();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 daxiletmə_p_VALUE 때만 İcazə_ver_VALUE.
    maşın_qeydiyyatdan_keçmək(IRQ_distribyutor) = 0;
    maşın_qeydiyyatdan_keçmək(IRQ_distribyutor + 0x180) = 0xffffffff;
    maşın_qeydiyyatdan_keçmək(IRQ_distribyutor + 0x80) = 0xffffffff;
    maşın_qeydiyyatdan_keçmək(IRQ_distribyutor + 0x280) = 1u << 30;
    maşın_qeydiyyatdan_keçmək(IRQ_distribyutor + 0x41c) = 0x80808080;
    maşın_qeydiyyatdan_keçmək(IRQ_distribyutor + 0x100) = 1u << 30;
    maşın_qeydiyyatdan_keçmək(IRQ_CPU_interfeys + 4) = 0xff;
    maşın_qeydiyyatdan_keçmək(IRQ_CPU_interfeys + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 수 있다.
    int Təhlükəsizlik = (maşın_qeydiyyatdan_keçmək(IRQ_distribyutor + 4) & (1u << 10)) != 0;
    maşın_qeydiyyatdan_keçmək(IRQ_distribyutor) = Təhlükəsizlik ? 1 : 3;
    maşın_qeydiyyatdan_keçmək(IRQ_CPU_interfeys) = Təhlükəsizlik ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t TYPE_sahə, maşın_TYPE; uint32_t versiya_nömrəsi;
    uint64_t daxiletmə_p, proqram_Başlıq_OFFSET, bölmə_Başlıq_OFFSET; uint32_t konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti;
    uint16_t 실행머리크기, proqram_Başlıq_daxiletmə_ölçünü_dəyişmək, proqram_Başlıq_COUNT, bölmə_Başlıq_daxiletmə_ölçünü_dəyişmək, bölmə_Başlıq_COUNT, bölmə_ad_cədvəl_INDEX;
} 실행파일머리;
typedef struct { uint32_t TYPE_sahə, konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti; uint64_t OFFSET_VALUE, ünvan, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(istifadəçi_kadr) == 272, "exception assembly layout");
static int 포함된범위(uint64_t OFFSET_VALUE, uint64_t Böyüklük, uint64_t bitirmək_OFFSET) {
    return OFFSET_VALUE <= bitirmək_OFFSET && Böyüklük <= bitirmək_OFFSET - OFFSET_VALUE;
}
static int 부가정보검사(const unsigned char *verilənlər_yerinə_qoymaq, size_t Böyüklük) {
    size_t 현재위치 = 0;
    while (포함된범위(현재위치, 12, Böyüklük)) {
        uint32_t 낱말들[3]; memcpy(낱말들, verilənlər_yerinə_qoymaq + 현재위치, 12); 현재위치 += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(현재위치, 이름영역크기, Böyüklük) || !포함된범위(현재위치 + 이름영역크기, 설명크기, Böyüklük)) return 0;
        const unsigned char Ad[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Ad) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Ad); 순번++) if (verilənlər_yerinə_qoymaq[현재위치 + 순번] != Ad[순번]) 일치 = 0;
        uint32_t versiya_nömrəsi = 0;
        if (일치) memcpy(&versiya_nömrəsi, verilənlər_yerinə_qoymaq + 현재위치 + 이름영역크기, 4);
        if (일치 && versiya_nömrəsi == 1) return 1;
        현재위치 += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *verilənlər, size_t Böyüklük, int 리눅스방식) {
    if (Böyüklük < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, verilənlər, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.TYPE_sahə != 2 || 실행머리.maşın_TYPE != 183 || 실행머리.versiya_nömrəsi != 1 || 실행머리.konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.proqram_Başlıq_daxiletmə_ölçünü_dəyişmək != sizeof(실행파일구획) || !실행머리.proqram_Başlıq_COUNT || 실행머리.proqram_Başlıq_COUNT > 16 ||
        실행머리.proqram_Başlıq_OFFSET < sizeof(실행머리) || !포함된범위(실행머리.proqram_Başlıq_OFFSET, (uint64_t)실행머리.proqram_Başlıq_COUNT * sizeof(실행파일구획), Böyüklük)) return 사용자실행파일오류;
    uint8_t 사용량[(istifadəçi_IMAGE_bitirmək - istifadəçi_BASE) / səhifənin_ölçüsü] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.proqram_Başlıq_COUNT; 순번++) {
        실행파일구획 verilənlər_yerinə_qoymaq; memcpy(&verilənlər_yerinə_qoymaq, verilənlər + 실행머리.proqram_Başlıq_OFFSET + 순번 * sizeof(verilənlər_yerinə_qoymaq), sizeof(verilənlər_yerinə_qoymaq));
        if (verilənlər_yerinə_qoymaq.TYPE_sahə == 4) {
            if (!포함된범위(verilənlər_yerinə_qoymaq.OFFSET_VALUE, verilənlər_yerinə_qoymaq.파일영역크기, Böyüklük)) return 사용자실행파일오류;
            if (부가정보검사(verilənlər + verilənlər_yerinə_qoymaq.OFFSET_VALUE, verilənlər_yerinə_qoymaq.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (verilənlər_yerinə_qoymaq.TYPE_sahə == 0 || verilənlər_yerinə_qoymaq.TYPE_sahə == 6 || (verilənlər_yerinə_qoymaq.TYPE_sahə == 0x6474e551 && !(verilənlər_yerinə_qoymaq.konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti & 1))) continue;
        if (verilənlər_yerinə_qoymaq.TYPE_sahə != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!verilənlər_yerinə_qoymaq.기억영역크기) continue;
        if (verilənlər_yerinə_qoymaq.konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti & ~7u || !(verilənlər_yerinə_qoymaq.konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti & 4) || (verilənlər_yerinə_qoymaq.konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti & 3) == 3 || verilənlər_yerinə_qoymaq.파일영역크기 > verilənlər_yerinə_qoymaq.기억영역크기 ||
            (verilənlər_yerinə_qoymaq.파일영역크기 && !포함된범위(verilənlər_yerinə_qoymaq.OFFSET_VALUE, verilənlər_yerinə_qoymaq.파일영역크기, Böyüklük)) || verilənlər_yerinə_qoymaq.ünvan < istifadəçi_BASE ||
            !포함된범위(verilənlər_yerinə_qoymaq.ünvan, verilənlər_yerinə_qoymaq.기억영역크기, istifadəçi_IMAGE_bitirmək) ||
            (!리눅스방식 && ((verilənlər_yerinə_qoymaq.ünvan & (səhifənin_ölçüsü - 1)) || (verilənlər_yerinə_qoymaq.OFFSET_VALUE & (səhifənin_ölçüsü - 1)) || verilənlər_yerinə_qoymaq.맞춤 != səhifənin_ölçüsü)) ||
            (리눅스방식 && (((verilənlər_yerinə_qoymaq.ünvan ^ verilənlər_yerinə_qoymaq.OFFSET_VALUE) & (səhifənin_ölçüsü - 1)) || !verilənlər_yerinə_qoymaq.맞춤 ||
                (verilənlər_yerinə_qoymaq.맞춤 & (verilənlər_yerinə_qoymaq.맞춤 - 1)) || verilənlər_yerinə_qoymaq.맞춤 > 0x200000 || ((verilənlər_yerinə_qoymaq.ünvan ^ verilənlər_yerinə_qoymaq.OFFSET_VALUE) & (verilənlər_yerinə_qoymaq.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (verilənlər_yerinə_qoymaq.ünvan - istifadəçi_BASE) / səhifənin_ölçüsü;
        unsigned daxiletmə_COUNT = ((verilənlər_yerinə_qoymaq.ünvan & (səhifənin_ölçüsü - 1)) + verilənlər_yerinə_qoymaq.기억영역크기 + səhifənin_ölçüsü - 1) / səhifənin_ölçüsü;
        for (unsigned səhifə_VALUE = 첫항목; səhifə_VALUE < 첫항목 + daxiletmə_COUNT; səhifə_VALUE++) {
            if (사용량[səhifə_VALUE]) return 사용자실행파일오류;
            사용량[səhifə_VALUE] = 1;
        }
        if ((verilənlər_yerinə_qoymaq.konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti & 1) && 실행머리.daxiletmə_p >= verilənlər_yerinə_qoymaq.ünvan && 실행머리.daxiletmə_p < verilənlər_yerinə_qoymaq.ünvan + verilənlər_yerinə_qoymaq.파일영역크기 && !(실행머리.daxiletmə_p & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *verilənlər, size_t Böyüklük) { return 실행파일검사(verilənlər, Böyüklük, 0); }
static void səhifə_düzümü(uintptr_t ünvan, uint64_t konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti, unsigned icazələr) {
    unsigned LOOKUP_INDEX = (ünvan - istifadəçi_BASE) / səhifənin_ölçüsü;
    səhifə_Siyahı[LOOKUP_INDEX] = ünvan | konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti;
    icazələr_Siyahı[LOOKUP_INDEX] = icazələr;
}
static int 사용자범위(uintptr_t ünvan, size_t daxiletmə_COUNT, int 쓰는중) {
    if (ünvan < istifadəçi_BASE || !포함된범위(ünvan, daxiletmə_COUNT, istifadəçi_bitirmək)) return 0;
    if (!daxiletmə_COUNT) return 1;
    unsigned 첫항목 = (ünvan - istifadəçi_BASE) / səhifənin_ölçüsü, 마지막 = (ünvan + daxiletmə_COUNT - 1 - istifadəçi_BASE) / səhifənin_ölçüsü;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(icazələr_Siyahı[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int nümunə_yol(uintptr_t ünvan, char *Cığır) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!사용자범위(ünvan, 1, 0)) return -14;
        Cığır[순번] = *(const char *)ünvan++;
        if (!Cığır[순번]) return 0;
    }
    return -36;
}
static intptr_t nüvə_ölçü(intptr_t ölçü) { return ölçü < 0 ? -오류번호 : ölçü; }
static int 대응파일기술자(uint64_t fayl_tutacaq) { return fayl_tutacaq >= 3 && fayl_tutacaq < 19 ? fayl_Siyahı[fayl_tutacaq - 3] : -1; }
static int 통신끝점소유(uint64_t fayl_tutacaq) { return fayl_tutacaq >= 32 && fayl_tutacaq < 56 && 통신끝점들[fayl_tutacaq - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t uzunluq_VALUE, struct pk_sockaddr_in *ünvan) {
    if (uzunluq_VALUE != sizeof(*ünvan)) return -22;
    if (!사용자범위(가리킴값, uzunluq_VALUE, 0)) return -14;
    memcpy(ünvan, (const void *)가리킴값, sizeof(*ünvan));
    return ünvan->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t uzunluq_göstərici, pk_socklen_t *수용량) {
    if (!사용자범위(uzunluq_göstərici, sizeof(*수용량), 1)) return -14;
    memcpy(수용량, (const void *)uzunluq_göstərici, sizeof(*수용량));
    if (*수용량 > sizeof(struct pk_sockaddr_in)) *수용량 = sizeof(struct pk_sockaddr_in);
    if (*수용량 && !사용자범위(가리킴값, *수용량, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t uzunluq_göstərici, pk_socklen_t 수용량, int ünvan, int 접속번호) {
    struct pk_sockaddr_in VALUE; memset(&VALUE, 0, sizeof(VALUE));
    VALUE.sin_family = AF_INET; VALUE.sin_port = pk_htons(접속번호); VALUE.sin_addr.s_addr = pk_htonl(ünvan);
    if (수용량) memcpy((void *)가리킴값, &VALUE, 수용량);
    pk_socklen_t uzunluq_VALUE = sizeof(VALUE); memcpy((void *)uzunluq_göstərici, &uzunluq_VALUE, sizeof(uzunluq_VALUE));
}
extern uintptr_t lövhə_kanal(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(istifadəçi_kadr *fayl_daxiletmə) {
    uintptr_t 첫째값 = fayl_daxiletmə->qeydiyyatdan_keçmək_verilənlər[0], SECOND_VALUE = fayl_daxiletmə->qeydiyyatdan_keçmək_verilənlər[1], simvol_kodu = fayl_daxiletmə->qeydiyyatdan_keçmək_verilənlər[2];
    char Cığır[65];
    int fayl_tutacaq, ölçü;
    switch (fayl_daxiletmə->qeydiyyatdan_keçmək_verilənlər[8]) {
    case 0: return 1; // 자체 ABI 버전
    case 1: // write: göstərici 전체를 검사한 GERİ_VALUE 출력/FAYL dəyişdirmək_VALUE
        if (simvol_kodu > 65536) return -22;
        if (!사용자범위(SECOND_VALUE, simvol_kodu, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=Saat_VALUE();
            for (size_t 순번 = 0; 순번 < simvol_kodu; 순번++) lövhə_kanal(첫째값, ((const unsigned char *)SECOND_VALUE)[순번]);
            /* 큰 tty를 그린 nüvə_VALUE 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(interaktiv){
                마감시각+=Saat_VALUE()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(마감시각) : "memory");
            }
            return simvol_kodu;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t element_COUNT=simvol_kodu>512?512:simvol_kodu;for(size_t 순번=0;순번<element_COUNT;순번++)자바전문넣기(순번,((const unsigned char *)SECOND_VALUE)[순번]);return 자바흐름쓰기(첫째값,element_COUNT);
        }
        fayl_tutacaq = 대응파일기술자(첫째값); if (fayl_tutacaq < 0) return -9;
        return nüvə_ölçü(pk_write(fayl_tutacaq, (const void *)SECOND_VALUE, simvol_kodu));
    case 2:
        if (simvol_kodu > 65536) return -22;
        if (!사용자범위(SECOND_VALUE, simvol_kodu, 1)) return -14;
        if (첫째값 == 0) {
            size_t element_COUNT = 0;
            while (element_COUNT < simvol_kodu) {
                int simvol_VALUE_068c2631 = (int32_t)보드글자읽기(); if (simvol_VALUE_068c2631 == -2) return element_COUNT; if (simvol_VALUE_068c2631 < 0) break;
                ((unsigned char *)SECOND_VALUE)[element_COUNT++] = simvol_VALUE_068c2631;
            }
            return element_COUNT ? (intptr_t)element_COUNT : (simvol_kodu ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            ölçü=자바흐름읽기(첫째값,simvol_kodu>512?512:simvol_kodu);if(ölçü>0)for(int 순번=0;순번<ölçü;순번++)((unsigned char *)SECOND_VALUE)[순번]=자바전문얻기(순번);return ölçü;
        }
        fayl_tutacaq = 대응파일기술자(첫째값); if (fayl_tutacaq < 0) return -9;
        return nüvə_ölçü(pk_read(fayl_tutacaq, (void *)SECOND_VALUE, simvol_kodu));
    case 3:
        ölçü = nümunə_yol(첫째값, Cığır); if (ölçü) return ölçü;
        if (SECOND_VALUE > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (fayl_Siyahı[순번] < 0) {
            fayl_tutacaq = pk_open(Cığır, (int)SECOND_VALUE, 0600);
            if (fayl_tutacaq < 0) return -오류번호;
            fayl_Siyahı[순번] = fayl_tutacaq; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { ölçü = 통신끝점닫기(첫째값); if (!ölçü) 통신끝점들[첫째값 - 32] = 0; return ölçü; }
        fayl_tutacaq = 대응파일기술자(첫째값); if (fayl_tutacaq < 0) return -9;
        ölçü = pk_close(fayl_tutacaq); if (!ölçü) fayl_Siyahı[첫째값 - 3] = -1;
        return nüvə_ölçü(ölçü);
    case 5:
        fayl_tutacaq = 대응파일기술자(첫째값); if (fayl_tutacaq < 0) return -9;
        if (simvol_kodu > 2) return -22;
        return nüvə_ölçü(pk_lseek(fayl_tutacaq, (int64_t)SECOND_VALUE, simvol_kodu));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 istifadəçi RW/NX 힙, 새로 노출되는 페이지는 0으로 ilkin_qiymət_vermək
        if (!첫째값) return 동적기억끝;
        if (첫째값 < istifadəçi_IMAGE_bitirmək || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + səhifənin_ölçüsü - 1) & ~(səhifənin_ölçüsü - 1);
        uintptr_t 새쪽들 = (첫째값 + səhifənin_ölçüsü - 1) & ~(səhifənin_ölçüsü - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t verilənlər_yerinə_qoymaq = 이전쪽들; verilənlər_yerinə_qoymaq < 새쪽들; verilənlər_yerinə_qoymaq += səhifənin_ölçüsü) səhifə_düzümü(verilənlər_yerinə_qoymaq, nüvə_səhifə, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t verilənlər_yerinə_qoymaq = 이전쪽들; verilənlər_yerinə_qoymaq < 새쪽들; verilənlər_yerinə_qoymaq += səhifənin_ölçüsü) səhifə_düzümü(verilənlər_yerinə_qoymaq, istifadəçi_oxunan_yazılan, 3);
        } else {
            for (uintptr_t verilənlər_yerinə_qoymaq = 새쪽들; verilənlər_yerinə_qoymaq < 이전쪽들; verilənlər_yerinə_qoymaq += səhifənin_ölçüsü) {
                səhifə_Siyahı[(verilənlər_yerinə_qoymaq - istifadəçi_BASE) / səhifənin_ölçüsü] = 0; icazələr_Siyahı[(verilənlər_yerinə_qoymaq - istifadəçi_BASE) / səhifənin_ölçüsü] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        fayl_tutacaq = 대응파일기술자(첫째값); return fayl_tutacaq < 0 ? -9 : nüvə_ölçü(pk_size(fayl_tutacaq));
    case 10:
        fayl_tutacaq = 대응파일기술자(첫째값); return fayl_tutacaq < 0 ? -9 : nüvə_ölçü(pk_ftruncate(fayl_tutacaq, (int64_t)SECOND_VALUE));
    case 11:
        ölçü = nümunə_yol(첫째값, Cığır); return ölçü ? ölçü : nüvə_ölçü(pk_unlink(Cığır));
    case 12:
        fayl_tutacaq = 대응파일기술자(첫째값); return fayl_tutacaq < 0 ? -9 : nüvə_ölçü(pk_fsync(fayl_tutacaq));
    case 13: { // 그래픽 기초 API: istifadəçi 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = fayl_daxiletmə->qeydiyyatdan_keçmək_verilənlər[3], 높이값 = fayl_daxiletmə->qeydiyyatdan_keçmək_verilənlər[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SECOND_VALUE > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - SECOND_VALUE) return -22;
        for (uintptr_t Y_koordinat = SECOND_VALUE; Y_koordinat < SECOND_VALUE + 높이값; Y_koordinat++) for (uintptr_t x_koordinatı = 첫째값; x_koordinatı < 첫째값 + 너비값; x_koordinatı++) lövhə_piksel(x_koordinatı, Y_koordinat, simvol_kodu);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=element_COUNT; args(index,buffer,capacity)=UTF-8 uzunluq_VALUE
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (simvol_kodu <= 전달인수길이[첫째값]) return -36;
        if (!사용자범위(SECOND_VALUE, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SECOND_VALUE, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;interaktiv=1;return lövhə_Terminal(13);}
        if(첫째값==2){interaktiv=0;return 0;}
        if(첫째값==3)return lövhə_Terminal(13);
        if(첫째값!=1||!interaktiv)return -22;
        ölçü=(int32_t)보드글자읽기();
        if(ölçü==-4096)return ölçü;
        Başla_FASİLƏ();return ölçü<0?-11:ölçü;
    case 17: { // 유한한 협력 gözlə_VALUE: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t bitirmək_TIME = Saat_VALUE() + FREQUENCY * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Saat_VALUE() < bitirmək_TIME);
        Başla_FASİLƏ(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 부모·빈 폴더를 검사한다.
        if (SECOND_VALUE > 2) return -22;
        ölçü = nümunə_yol(첫째값, Cığır); if (ölçü) return ölçü;
        unsigned uzunluq_VALUE = 0; while (Cığır[uzunluq_VALUE]) uzunluq_VALUE++;
        ölçü = 자바경로시작(uzunluq_VALUE); if (ölçü < 0) return ölçü;
        for (unsigned 순번 = 0; 순번 < uzunluq_VALUE; 순번++) 자바경로바이트(순번, (unsigned char)Cığır[순번]);
        return SECOND_VALUE == 0 ? 자바항목종류() : SECOND_VALUE == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int simvol_VALUE_068c2631=(int32_t)보드글자읽기();if(simvol_VALUE_068c2631==-4096)return simvol_VALUE_068c2631;if(simvol_VALUE_068c2631>=0)화면누름(sahib_obyekt,simvol_VALUE_068c2631);Başla_FASİLƏ();}
        if(첫째값==3&&simvol_kodu){if(!자바셸대화형())return -95;interaktiv=1;lövhə_Terminal(300);}
        return 화면호출(sahib_obyekt,첫째값,SECOND_VALUE,simvol_kodu,fayl_daxiletmə->qeydiyyatdan_keçmək_verilənlər[3],fayl_daxiletmə->qeydiyyatdan_keçmək_verilənlər[4],fayl_daxiletmə->qeydiyyatdan_keçmək_verilənlər[5]);
    case 21:
        if(simvol_kodu>127)return -22;if(!사용자범위(SECOND_VALUE,simvol_kodu*sizeof(uint32_t),0))return -14;
        return 화면글(sahib_obyekt,첫째값,(const uint32_t *)SECOND_VALUE,simvol_kodu);
    case 22: // 화면 Böyüklük sorğu_VALUE: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SECOND_VALUE==SOCK_STREAM&&(simvol_kodu==0||simvol_kodu==6))ölçü=자바흐름만들기();
        else if(SECOND_VALUE==SOCK_DGRAM&&(simvol_kodu==0||simvol_kodu==IPPROTO_UDP))ölçü=자바전문만들기(첫째값,SECOND_VALUE,simvol_kodu);
        else return -93;
        if (ölçü >= 32 && ölçü < 56) 통신끝점들[ölçü - 32] = 1;
        return ölçü;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in ünvan;
        ölçü = 주소입력(SECOND_VALUE, simvol_kodu, &ünvan); if (ölçü) return ölçü;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(ünvan.sin_addr.s_addr),pk_htons(ünvan.sin_port)):자바전문묶기(첫째값, pk_htonl(ünvan.sin_addr.s_addr), pk_htons(ünvan.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (fayl_daxiletmə->qeydiyyatdan_keçmək_verilənlər[3]) return -95;
        if (simvol_kodu > 512) return -90;
        if (simvol_kodu && !사용자범위(SECOND_VALUE, simvol_kodu, 0)) return -14;
        struct pk_sockaddr_in ünvan;
        ölçü = 주소입력(fayl_daxiletmə->qeydiyyatdan_keçmək_verilənlər[4], fayl_daxiletmə->qeydiyyatdan_keçmək_verilənlər[5], &ünvan); if (ölçü) return ölçü;
        for (unsigned 순번 = 0; 순번 < simvol_kodu; 순번++) 자바전문넣기(순번, ((const unsigned char *)SECOND_VALUE)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(ünvan.sin_addr.s_addr), pk_htons(ünvan.sin_port), simvol_kodu);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (fayl_daxiletmə->qeydiyyatdan_keçmək_verilənlər[3]) return -95;
        if (simvol_kodu > 512) return -90;
        if (simvol_kodu && !사용자범위(SECOND_VALUE, simvol_kodu, 1)) return -14;
        pk_socklen_t 수용량 = 0;
        if (fayl_daxiletmə->qeydiyyatdan_keçmək_verilənlər[4]) { ölçü = 주소출력검사(fayl_daxiletmə->qeydiyyatdan_keçmək_verilənlər[4], fayl_daxiletmə->qeydiyyatdan_keçmək_verilənlər[5], &수용량); if (ölçü) return ölçü; }
        ölçü = 자바전문받기(첫째값, simvol_kodu); if (ölçü < 0) return ölçü;
        for (int 순번 = 0; 순번 < ölçü; 순번++) ((unsigned char *)SECOND_VALUE)[순번] = 자바전문얻기(순번);
        if (fayl_daxiletmə->qeydiyyatdan_keçmək_verilənlər[4]) 주소출력(fayl_daxiletmə->qeydiyyatdan_keçmək_verilənlər[4], fayl_daxiletmə->qeydiyyatdan_keçmək_verilənlər[5], 수용량, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return ölçü;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t 수용량;
        ölçü = 주소출력검사(SECOND_VALUE, simvol_kodu, &수용량); if (ölçü) return ölçü;
        주소출력(SECOND_VALUE,simvol_kodu,수용량,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in ünvan;
        ölçü=주소입력(SECOND_VALUE,simvol_kodu,&ünvan);if(ölçü)return ölçü;
        return 자바흐름연결(첫째값,pk_htonl(ünvan.sin_addr.s_addr),pk_htons(ünvan.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,SECOND_VALUE):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(SECOND_VALUE||simvol_kodu)return -95;ölçü=자바흐름연결받기(첫째값);if(ölçü>=40&&ölçü<56)통신끝점들[ölçü-32]=1;return ölçü;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(istifadəçi_kadr *fayl_daxiletmə) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(fayl_daxiletmə) : 자체체계호출(fayl_daxiletmə);
}
static void geri_qaytarmaq_nüvə(istifadəçi_kadr *fayl_daxiletmə, int ölçü) {
    Dayandır_FASİLƏ();
    fayl_daxiletmə->qeydiyyatdan_keçmək_verilənlər[0] = (uint64_t)(int64_t)ölçü;
    fayl_daxiletmə->əmr_yerinə_qoymaq = (uintptr_t)istifadəçi_geri_qaytarmaq;
    fayl_daxiletmə->vəziyyət_kod = 0x3c5; // EL1h, DAIF masked
}
int istifadəçi_istisna(istifadəçi_kadr *fayl_daxiletmə, unsigned INTERCEPT) {
    if (!Aktiv || (fayl_daxiletmə->vəziyyət_kod & 15) != 0) return 0;
    if (INTERCEPT) {
        uint32_t 승인값 = maşın_qeydiyyatdan_keçmək(IRQ_CPU_interfeys + 0xc), identifikator_VALUE = 승인값 & 1023;
        if (identifikator_VALUE == 30) { geri_qaytarmaq_nüvə(fayl_daxiletmə, istifadəçi_FASİLƏ); maşın_qeydiyyatdan_keçmək(IRQ_CPU_interfeys + 0x10) = 승인값; return 1; }
        if (identifikator_VALUE < 1020) maşın_qeydiyyatdan_keçmək(IRQ_CPU_interfeys + 0x10) = 승인값;
        return 1;
    }
    uint64_t istisna_vəziyyət; __asm__ volatile("mrs %0, esr_el1" : "=r"(istisna_vəziyyət));
    if (Saat_VALUE() >= 마감시각) { geri_qaytarmaq_nüvə(fayl_daxiletmə, istifadəçi_FASİLƏ); return 1; }
    unsigned istisna_sahə = istisna_vəziyyət >> 26;
    if (istisna_sahə == 0x15 && (istisna_vəziyyət & 0xffff) == 0) {
        if (리눅스규약 ? fayl_daxiletmə->qeydiyyatdan_keçmək_verilənlər[8] == 93 || fayl_daxiletmə->qeydiyyatdan_keçmək_verilənlər[8] == 94 : fayl_daxiletmə->qeydiyyatdan_keçmək_verilənlər[8] == 6) geri_qaytarmaq_nüvə(fayl_daxiletmə, (int)(fayl_daxiletmə->qeydiyyatdan_keçmək_verilənlər[0] & 255));
        else {
            intptr_t ölçü=체계호출(fayl_daxiletmə);
            if(ölçü==-4096&&interaktiv){
                저장값[sahib_obyekt].실행틀=*fayl_daxiletmə;저장값[sahib_obyekt].실행틀.əmr_yerinə_qoymaq-=4;
                사용자실수보관(저장값[sahib_obyekt].실수저장상태);geri_qaytarmaq_nüvə(fayl_daxiletmə,사용자중단됨);
            }else fayl_daxiletmə->qeydiyyatdan_keçmək_verilənlər[0]=(uint64_t)ölçü;
        }
    } else geri_qaytarmaq_nüvə(fayl_daxiletmə, istisna_sahə == 0x24 ? istifadəçi_verilənlər_səhv : istisna_sahə == 0x20 ? 사용자실행오류 : istifadəçi_yanlış_təlimat);
    return 1;
}

// 생성된 const ELF Qrup_VALUE: 실행은 반드시 proqram_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *verilənlər; size_t Böyüklük; unsigned 전달값; } proqram;
#include "programs.h"
static void *ani_görüntü(unsigned yerinə_qoymaq_INDEX){return (void *)(0x04000000ul+yerinə_qoymaq_INDEX*(istifadəçi_bitirmək-istifadəçi_BASE));}
static int Bitir_proqram(int ölçü){
    사용자누적시각[sahib_obyekt]+=(uint32_t)보드밀리초()-사용자실행시각[sahib_obyekt];
    Dayandır_FASİLƏ();Aktiv=0;
    if(ölçü==사용자중단됨){
        저장된작업 *sətir_verilənlər=&저장값[sahib_obyekt];sətir_verilənlər->멈춤상태=1;sətir_verilənlər->interaktiv=interaktiv;sətir_verilənlər->리눅스규약=리눅스규약;sətir_verilənlər->동적기억공간=동적기억끝;sətir_verilənlər->인수개수=전달인수개수;
        memcpy(sətir_verilənlər->icazələr_Siyahı,icazələr_Siyahı,sizeof(icazələr_Siyahı));memcpy(sətir_verilənlər->fayl_Siyahı,fayl_Siyahı,sizeof(fayl_Siyahı));memcpy(sətir_verilənlər->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(sətir_verilənlər->arqument_ARRAY,전달인수,sizeof(전달인수));memcpy(sətir_verilənlər->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<istifadəçi_səhifə_COUNT;순번++)if(icazələr_Siyahı[순번])memcpy((unsigned char *)ani_görüntü(sahib_obyekt)+순번*səhifənin_ölçüsü,(void *)(istifadəçi_BASE+순번*səhifənin_ölçüsü),səhifənin_ölçüsü);
    }else{
        저장값[sahib_obyekt].멈춤상태=0;화면초기화(sahib_obyekt);
        for(unsigned 순번=0;순번<16;순번++)if(fayl_Siyahı[순번]>=0)pk_close(fayl_Siyahı[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<istifadəçi_səhifə_COUNT;순번++){səhifə_Siyahı[순번]=0;icazələr_Siyahı[순번]=0;}변환표맞추기();return ölçü;
}
uintptr_t lövhə_istifadəçi_idarəetməsi(uintptr_t Gedişat){
    unsigned yerinə_qoymaq_INDEX=Gedişat&15;if(yerinə_qoymaq_INDEX>=4||Aktiv)return (uint32_t)-22;
    저장된작업 *sətir_verilənlər=&저장값[yerinə_qoymaq_INDEX];
    if(Gedişat>=32){if(sətir_verilənlər->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(sətir_verilənlər->fayl_Siyahı[순번]>=0)pk_close(sətir_verilənlər->fayl_Siyahı[순번]);for(unsigned 순번=0;순번<24;순번++)if(sətir_verilənlər->통신끝점들[순번])통신끝점닫기(순번+32);}sətir_verilənlər->멈춤상태=0;화면초기화(yerinə_qoymaq_INDEX);return 0;}
    if(Gedişat>=16)return sətir_verilənlər->멈춤상태;
    if(!sətir_verilənlər->멈춤상태)return (uint32_t)-22;
    sahib_obyekt=yerinə_qoymaq_INDEX;interaktiv=sətir_verilənlər->interaktiv;리눅스규약=sətir_verilənlər->리눅스규약;동적기억끝=sətir_verilənlər->동적기억공간;전달인수개수=sətir_verilənlər->인수개수;
    memcpy(fayl_Siyahı,sətir_verilənlər->fayl_Siyahı,sizeof(fayl_Siyahı));memcpy(통신끝점들,sətir_verilənlər->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,sətir_verilənlər->arqument_ARRAY,sizeof(전달인수));memcpy(전달인수길이,sətir_verilənlər->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<istifadəçi_səhifə_COUNT;순번++)səhifə_Siyahı[순번]=(istifadəçi_BASE+순번*səhifənin_ölçüsü)|nüvə_səhifə;변환표맞추기();
    memset((void *)istifadəçi_BASE,0,istifadəçi_bitirmək-istifadəçi_BASE);
    for(unsigned 순번=0;순번<istifadəçi_səhifə_COUNT;순번++)if(sətir_verilənlər->icazələr_Siyahı[순번])memcpy((void *)(istifadəçi_BASE+순번*səhifənin_ölçüsü),(unsigned char *)ani_görüntü(yerinə_qoymaq_INDEX)+순번*səhifənin_ölçüsü,səhifənin_ölçüsü);
    memcpy(icazələr_Siyahı,sətir_verilənlər->icazələr_Siyahı,sizeof(icazələr_Siyahı));
    for(unsigned 순번=0;순번<istifadəçi_səhifə_COUNT;순번++){unsigned verilənlər_yerinə_qoymaq=icazələr_Siyahı[순번];səhifə_Siyahı[순번]=verilənlər_yerinə_qoymaq?(istifadəçi_BASE+순번*səhifənin_ölçüsü)|(verilənlər_yerinə_qoymaq==3?istifadəçi_oxunan_yazılan:verilənlər_yerinə_qoymaq==5?사용자읽고실행:istifadəçi_yalnız_oxunan):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");Aktiv=1;sətir_verilənlər->멈춤상태=0;Başla_FASİLƏ();
    사용자실행시각[sahib_obyekt]=보드밀리초();
    return (uint32_t)Bitir_proqram(istifadəçi_CV(&sətir_verilənlər->실행틀,sətir_verilənlər->실수저장상태));
}
static int icra_proqram(const unsigned char *verilənlər, size_t Böyüklük, unsigned 전달값, int 리눅스방식, const char *Ad) {
    if (Aktiv) return -16;
    sahib_obyekt=lövhə_Terminal(11);if(sahib_obyekt<0||sahib_obyekt>3||저장값[sahib_obyekt].멈춤상태)return -16;interaktiv=0;
    int 유효함 = 실행파일검사(verilənlər, Böyüklük, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned ad_INDEX=0;
    while (*Ad && ad_INDEX<31) istifadəçi_əmr_ad[sahib_obyekt][ad_INDEX++]=(unsigned char)*Ad++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (ad_INDEX) istifadəçi_əmr_ad[sahib_obyekt][ad_INDEX++]=' ';
        for (unsigned yerinə_qoymaq_INDEX=0; yerinə_qoymaq_INDEX<전달인수길이[0]; yerinə_qoymaq_INDEX++) istifadəçi_əmr_ad[sahib_obyekt][ad_INDEX++]=전달인수[0][yerinə_qoymaq_INDEX];
    }
    istifadəçi_əmr_ad[sahib_obyekt][ad_INDEX]=0; istifadəçi_nömrəsi[sahib_obyekt]=Sonrakı_istifadəçi_nömrəsi++;
    if (Sonrakı_istifadəçi_nömrəsi>0x7fffffffu) Sonrakı_istifadəçi_nömrəsi=10;
    istifadəçi_Başla_TIME[sahib_obyekt]=보드밀리초(); 사용자누적시각[sahib_obyekt]=0;
    for (unsigned 순번 = 0; 순번 < istifadəçi_səhifə_COUNT; 순번++) səhifə_Siyahı[순번] = (istifadəçi_BASE + 순번 * səhifənin_ölçüsü) | nüvə_səhifə;
    변환표맞추기();
    memset((void *)istifadəçi_BASE, 0, istifadəçi_bitirmək - istifadəçi_BASE);
    memset(icazələr_Siyahı, 0, sizeof(icazələr_Siyahı));
    실행파일머리 실행머리; memcpy(&실행머리, verilənlər, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.proqram_Başlıq_COUNT; 순번++) {
        실행파일구획 verilənlər_yerinə_qoymaq; memcpy(&verilənlər_yerinə_qoymaq, verilənlər + 실행머리.proqram_Başlıq_OFFSET + 순번 * sizeof(verilənlər_yerinə_qoymaq), sizeof(verilənlər_yerinə_qoymaq));
        if (verilənlər_yerinə_qoymaq.TYPE_sahə != 1 || !verilənlər_yerinə_qoymaq.기억영역크기) continue;
        if (verilənlər_yerinə_qoymaq.파일영역크기) memcpy((void *)(uintptr_t)verilənlər_yerinə_qoymaq.ünvan, verilənlər + verilənlər_yerinə_qoymaq.OFFSET_VALUE, verilənlər_yerinə_qoymaq.파일영역크기);
        for (uintptr_t 현재위치 = verilənlər_yerinə_qoymaq.ünvan & ~(səhifənin_ölçüsü - 1); 현재위치 < verilənlər_yerinə_qoymaq.ünvan + verilənlər_yerinə_qoymaq.기억영역크기; 현재위치 += səhifənin_ölçüsü) {
            icazələr_Siyahı[(현재위치 - istifadəçi_BASE) / səhifənin_ölçüsü] = (verilənlər_yerinə_qoymaq.konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti & 2) ? 3 : ((verilənlər_yerinə_qoymaq.konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti & 1) ? 5 : 1);
        }
    }
    for (uintptr_t 현재위치 = istifadəçi_Yığın_ünvan; 현재위치 < istifadəçi_bitirmək; 현재위치 += səhifənin_ölçüsü) icazələr_Siyahı[(현재위치 - istifadəçi_BASE) / səhifənin_ölçüsü] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.daxiletmə_p) : istifadəçi_bitirmək;
    for (unsigned 순번 = 0; 순번 < istifadəçi_səhifə_COUNT; 순번++) {
        unsigned icazələr = icazələr_Siyahı[순번];
        səhifə_Siyahı[순번] = icazələr ? (istifadəçi_BASE + 순번 * səhifənin_ölçüsü) | (icazələr == 3 ? istifadəçi_oxunan_yazılan : icazələr == 5 ? 사용자읽고실행 : istifadəçi_yalnız_oxunan) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) fayl_Siyahı[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = istifadəçi_IMAGE_bitirmək;
    Aktiv = 1; Başla_FASİLƏ();
    사용자실행시각[sahib_obyekt]=보드밀리초();
    int ölçü = istifadəçi_daxil_etmək(실행머리.daxiletmə_p, 초기쌓임공간, 전달값);
    return Bitir_proqram(ölçü);
}
uintptr_t lövhə_istifadəçi_icra(uintptr_t LOOKUP_INDEX) {
    if (LOOKUP_INDEX >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Ad=LOOKUP_INDEX==10?"javac":LOOKUP_INDEX==11?"java":LOOKUP_INDEX==12?"python":LOOKUP_INDEX==13?"vi":LOOKUP_INDEX==14?"jar":LOOKUP_INDEX==15?"cc":LOOKUP_INDEX==16?"jaot":"ELF";
    return (uint32_t)icra_proqram(실행항목들[LOOKUP_INDEX].verilənlər, 실행항목들[LOOKUP_INDEX].Böyüklük, 실행항목들[LOOKUP_INDEX].전달값, 0, Ad);
}
static uintptr_t icra_etmək_fayl(int 리눅스방식) {
    static unsigned char IMAGE[16384];
    if (Aktiv || !전달인수개수) return (uint32_t)-22;
    int fayl_tutacaq = pk_open((const char *)전달인수[0], yalnız_oxunan_VALUE, 0);
    if (fayl_tutacaq < 0) return (uint32_t)-오류번호;
    int Böyüklük = pk_size(fayl_tutacaq);
    if (Böyüklük < 0 || (unsigned)Böyüklük > sizeof(IMAGE)) { pk_close(fayl_tutacaq); return (uint32_t)-27; }
    int RECEIVED_COUNT = pk_read(fayl_tutacaq, IMAGE, Böyüklük); pk_close(fayl_tutacaq);
    if (RECEIVED_COUNT != Böyüklük) return (uint32_t)-5;
    return (uint32_t)icra_proqram(IMAGE, Böyüklük, 0, 리눅스방식, "");
}
uintptr_t lövhə_istifadəçi_fayl(void) { return icra_etmək_fayl(0); }
uintptr_t 보드사용자리눅스파일(void) { return icra_etmək_fayl(1); }
uintptr_t lövhə_istifadəçi_təsdiqlə(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].verilənlər, 잘못된실행항목들[순번].Böyüklük) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
