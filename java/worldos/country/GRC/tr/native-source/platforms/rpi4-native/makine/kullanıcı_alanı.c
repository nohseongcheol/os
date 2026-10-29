#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 yürütmek_komut makine katman_değer_e65604ef. dosya veri/정책은 기존 AOT Java 커널에 위임한다.
#include "kullanıcı_alanı.h"
#include "Dosya_ABI.h"
#include "ağ_ABI.h"
#include "../ağ_Yığın/ağ_Yığın.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define makine_yazmaç(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_dağıtımcı 0xff841000ul
#define IRQ_CPU_arabirim 0xff842000ul
#define sayfa_boyutu 4096ul
#define erişim_işaret (1ul << 10)
#define hayır_yürütmek_izin (1ul << 53)
#define kullanıcı_hayır_yürütmek (1ul << 54)
#define normal_Bellek ((1ul << 2) | (3ul << 8) | erişim_işaret)
#define çekirdek_sayfa (3ul | normal_Bellek | hayır_yürütmek_izin | kullanıcı_hayır_yürütmek)
#define kullanıcı_R_W (3ul | normal_Bellek | (1ul << 6) | hayır_yürütmek_izin | kullanıcı_hayır_yürütmek)
#define kullanıcı_salt_okunur (3ul | normal_Bellek | (3ul << 6) | hayır_yürütmek_izin | kullanıcı_hayır_yürütmek)
#define 사용자읽고실행 (3ul | normal_Bellek | (3ul << 6) | hayır_yürütmek_izin)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t Pano_piksel(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t Pano_Terminal(uintptr_t);
extern int Terminal_Beklemede(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int kullanıcı_özgeçmiş(kullanıcı_kare *,void *);
extern void 사용자실수보관(void *);
extern int kullanıcı_girmek(uintptr_t giriş_noktası, uintptr_t yığın_belleği, uintptr_t 전달값);
extern void kullanıcı_İade(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t kök_ADRES[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t sayfa_Liste[kullanıcı_sayfa_BAĞ_DEĞ_SAY] __attribute__((aligned(4096)));
static uint8_t izinler_Liste[kullanıcı_sayfa_BAĞ_DEĞ_SAY];
static int Aktif, dosya_listesi[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int Kapat_yuva_uç_nokta(unsigned dosya_tanıtıcısı){return dosya_tanıtıcısı<40?자바전문닫기(dosya_tanıtıcısı):자바흐름닫기(dosya_tanıtıcısı);}
static uint64_t SIKLIK, son_tarih_saat;
static uintptr_t yığın_Bitiş;
// çekirdek_değer 셸이 준비한 UTF-8 bağımsız_değişkenler. EL0에는 örnek_değer 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int duraklatılmış_Durum,devralmak,리눅스규약,dosya_listesi[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char bağımsız_değişken_DİZİ[8][256],izinler_Liste[kullanıcı_sayfa_BAĞ_DEĞ_SAY];
    uintptr_t dinamik_bellek; kullanıcı_kare yürütme_kare;
    unsigned char kayan_nokta_Durum[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int sahip_nesne,devralmak;
static uint32_t kullanıcı_numarası[4], kullanıcı_Start_saat[4], 사용자누적시각[4], kullanıcı_yürütme_saat[4], Sonraki_kullanıcı_numarası=10;
static unsigned char kullanıcı_komut_ad[4][288];
uint32_t 사용자상태읽기(unsigned girdi_değer, unsigned Dizin) {
    unsigned konum_dizini=Dizin&3;
    int Durum_değer=(Aktif && sahip_nesne==(int)konum_dizini) ? 1 : 저장값[konum_dizini].duraklatılmış_Durum ? 2 : 0;
    if (girdi_değer==0) return Durum_değer;
    if (!Durum_değer) return 0;
    if (girdi_değer==1) return kullanıcı_numarası[konum_dizini];
    if (girdi_değer==2) {
        unsigned char *쪽들=Durum_değer==1?izinler_Liste:저장값[konum_dizini].izinler_Liste;
        unsigned sayfa_BAĞ_DEĞ_SAY=0; for (unsigned 순번=0; 순번<kullanıcı_sayfa_BAĞ_DEĞ_SAY; 순번++) if(쪽들[순번]) sayfa_BAĞ_DEĞ_SAY++;
        return sayfa_BAĞ_DEĞ_SAY*4;
    }
    if (girdi_değer==3) return (uint32_t)보드밀리초()-kullanıcı_Start_saat[konum_dizini];
    if (girdi_değer==4) return 사용자누적시각[konum_dizini]+(Durum_değer==1?(uint32_t)보드밀리초()-kullanıcı_yürütme_saat[konum_dizini]:0);
    if (girdi_değer==5) return Dizin/4<sizeof(kullanıcı_komut_ad[0])?kullanıcı_komut_ad[konum_dizini][Dizin/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t girdi_BAĞ_DEĞ_SAY) {
    if (Aktif || girdi_BAĞ_DEĞ_SAY > 8) return (uint32_t)-22;
    전달인수개수 = girdi_BAĞ_DEĞ_SAY;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t ARA_Dizin, uintptr_t geçerli_konum, uintptr_t bayt_veri) {
    if (Aktif || ARA_Dizin >= 전달인수개수 || geçerli_konum >= 255 || geçerli_konum != 전달인수길이[ARA_Dizin] || !bayt_veri || bayt_veri > 255)
        return (uint32_t)-22;
    전달인수[ARA_Dizin][geçerli_konum] = bayt_veri;
    전달인수길이[ARA_Dizin] = geçerli_konum + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Saat_değer(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Dur_ZAMANAŞIMI(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    makine_yazmaç(IRQ_dağıtımcı + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void Start_ZAMANAŞIMI(void) {
    uint64_t 간격 = SIKLIK * 2, açmak = 1;
    son_tarih_saat = Saat_değer() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(açmak) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned veri_bloğu = 0; veri_bloğu < 4; veri_bloğu++) {
        kök_ADRES[veri_bloğu] = (uintptr_t)가운데[veri_bloğu] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t ADRES = ((uintptr_t)veri_bloğu << 30) | ((uintptr_t)순번 << 21);
            가운데[veri_bloğu][순번] = ADRES | 1 | erişim_işaret | kullanıcı_hayır_yürütmek;
            if (ADRES >= 0xfc000000ul) 가운데[veri_bloğu][순번] |= hayır_yürütmek_izin; // Device-nGnRnE
            else 가운데[veri_bloğu][순번] |= normal_Bellek; // Normal, non-cacheable
        }
    }
    for (unsigned SANİYE_değer = 0; SANİYE_değer < kullanıcı_sayfa_BAĞ_DEĞ_SAY / 512; SANİYE_değer++)
        가운데[0][(kullanıcı_TABAN >> 21) + SANİYE_değer] = (uintptr_t)(sayfa_Liste + SANİYE_değer * 512) | 3;
    for (unsigned 순번 = 0; 순번 < kullanıcı_sayfa_BAĞ_DEĞ_SAY; 순번++) sayfa_Liste[순번] = (kullanıcı_TABAN + 순번 * sayfa_boyutu) | çekirdek_sayfa;
    uint64_t Bellek_öznitelik_yazmaç = 0x4400, ADRES_Çeviri_denetim = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Bellek_öznitelik_yazmaç), "r"(ADRES_Çeviri_denetim), "r"((uintptr_t)kök_ADRES) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t kayan_nokta_Durum = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(kayan_nokta_Durum) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(SIKLIK));
    Dur_ZAMANAŞIMI();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 giriş_noktası_değer 때만 İzin_Ver_değer.
    makine_yazmaç(IRQ_dağıtımcı) = 0;
    makine_yazmaç(IRQ_dağıtımcı + 0x180) = 0xffffffff;
    makine_yazmaç(IRQ_dağıtımcı + 0x80) = 0xffffffff;
    makine_yazmaç(IRQ_dağıtımcı + 0x280) = 1u << 30;
    makine_yazmaç(IRQ_dağıtımcı + 0x41c) = 0x80808080;
    makine_yazmaç(IRQ_dağıtımcı + 0x100) = 1u << 30;
    makine_yazmaç(IRQ_CPU_arabirim + 4) = 0xff;
    makine_yazmaç(IRQ_CPU_arabirim + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 bilgi_teknolojisi_normal 확인할 수 있다.
    int Güvenlik = (makine_yazmaç(IRQ_dağıtımcı + 4) & (1u << 10)) != 0;
    makine_yazmaç(IRQ_dağıtımcı) = Güvenlik ? 1 : 3;
    makine_yazmaç(IRQ_CPU_arabirim) = Güvenlik ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t TÜR_alan, makine_TÜR; uint32_t sürüm_numarası;
    uint64_t giriş_noktası, program_Başlık_Ofset, bölüm_üst_bilgisi_Ofset; uint32_t Yapılandırma_BITS;
    uint16_t yürütülebilir_Başlık_boyutlandırmak, program_Başlık_girdi_boyutlandırmak, program_Başlık_BAĞ_DEĞ_SAY, bölüm_üst_bilgisi_girdi_boyutlandırmak, bölüm_üst_bilgisi_BAĞ_DEĞ_SAY, bölüm_ad_tablo_Dizin;
} 실행파일머리;
typedef struct { uint32_t TÜR_alan, Yapılandırma_BITS; uint64_t Ofset_değer, ADRES, 물리주소, 파일영역크기, 기억영역크기, hizalamak_sınır; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(kullanıcı_kare) == 272, "exception assembly layout");
static int 포함된범위(uint64_t Ofset_değer, uint64_t Boyut, uint64_t Bitiş_Ofset) {
    return Ofset_değer <= Bitiş_Ofset && Boyut <= Bitiş_Ofset - Ofset_değer;
}
static int 부가정보검사(const unsigned char *veri_konum, size_t Boyut) {
    size_t geçerli_konum = 0;
    while (포함된범위(geçerli_konum, 12, Boyut)) {
        uint32_t 낱말들[3]; memcpy(낱말들, veri_konum + geçerli_konum, 12); geçerli_konum += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(geçerli_konum, 이름영역크기, Boyut) || !포함된범위(geçerli_konum + 이름영역크기, 설명크기, Boyut)) return 0;
        const unsigned char İsim[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(İsim) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(İsim); 순번++) if (veri_konum[geçerli_konum + 순번] != İsim[순번]) 일치 = 0;
        uint32_t sürüm_numarası = 0;
        if (일치) memcpy(&sürüm_numarası, veri_konum + geçerli_konum + 이름영역크기, 4);
        if (일치 && sürüm_numarası == 1) return 1;
        geçerli_konum += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *veri, size_t Boyut, int 리눅스방식) {
    if (Boyut < sizeof(실행파일머리)) return kullanıcı_yürütülebilir_hata;
    실행파일머리 yürütülebilir_Başlık; memcpy(&yürütülebilir_Başlık, veri, sizeof(yürütülebilir_Başlık));
    if (yürütülebilir_Başlık.형식식별[0] != 127 || yürütülebilir_Başlık.형식식별[1] != 'E' || yürütülebilir_Başlık.형식식별[2] != 'L' || yürütülebilir_Başlık.형식식별[3] != 'F' ||
        yürütülebilir_Başlık.형식식별[4] != 2 || yürütülebilir_Başlık.형식식별[5] != 1 || yürütülebilir_Başlık.형식식별[6] != 1 || (yürütülebilir_Başlık.형식식별[7] != 0 && (!리눅스방식 || yürütülebilir_Başlık.형식식별[7] != 3)) ||
        yürütülebilir_Başlık.TÜR_alan != 2 || yürütülebilir_Başlık.makine_TÜR != 183 || yürütülebilir_Başlık.sürüm_numarası != 1 || yürütülebilir_Başlık.Yapılandırma_BITS || yürütülebilir_Başlık.yürütülebilir_Başlık_boyutlandırmak != sizeof(yürütülebilir_Başlık) ||
        yürütülebilir_Başlık.program_Başlık_girdi_boyutlandırmak != sizeof(실행파일구획) || !yürütülebilir_Başlık.program_Başlık_BAĞ_DEĞ_SAY || yürütülebilir_Başlık.program_Başlık_BAĞ_DEĞ_SAY > 16 ||
        yürütülebilir_Başlık.program_Başlık_Ofset < sizeof(yürütülebilir_Başlık) || !포함된범위(yürütülebilir_Başlık.program_Başlık_Ofset, (uint64_t)yürütülebilir_Başlık.program_Başlık_BAĞ_DEĞ_SAY * sizeof(실행파일구획), Boyut)) return kullanıcı_yürütülebilir_hata;
    uint8_t 사용량[(kullanıcı_RESİM_Bitiş - kullanıcı_TABAN) / sayfa_boyutu] = {0};
    int geçerli_giriş_noktası = 0, ABI_Tamam = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < yürütülebilir_Başlık.program_Başlık_BAĞ_DEĞ_SAY; 순번++) {
        실행파일구획 veri_konum; memcpy(&veri_konum, veri + yürütülebilir_Başlık.program_Başlık_Ofset + 순번 * sizeof(veri_konum), sizeof(veri_konum));
        if (veri_konum.TÜR_alan == 4) {
            if (!포함된범위(veri_konum.Ofset_değer, veri_konum.파일영역크기, Boyut)) return kullanıcı_yürütülebilir_hata;
            if (부가정보검사(veri + veri_konum.Ofset_değer, veri_konum.파일영역크기)) ABI_Tamam = 1;
            continue;
        }
        if (veri_konum.TÜR_alan == 0 || veri_konum.TÜR_alan == 6 || (veri_konum.TÜR_alan == 0x6474e551 && !(veri_konum.Yapılandırma_BITS & 1))) continue;
        if (veri_konum.TÜR_alan != 1) return kullanıcı_yürütülebilir_hata; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!veri_konum.기억영역크기) continue;
        if (veri_konum.Yapılandırma_BITS & ~7u || !(veri_konum.Yapılandırma_BITS & 4) || (veri_konum.Yapılandırma_BITS & 3) == 3 || veri_konum.파일영역크기 > veri_konum.기억영역크기 ||
            (veri_konum.파일영역크기 && !포함된범위(veri_konum.Ofset_değer, veri_konum.파일영역크기, Boyut)) || veri_konum.ADRES < kullanıcı_TABAN ||
            !포함된범위(veri_konum.ADRES, veri_konum.기억영역크기, kullanıcı_RESİM_Bitiş) ||
            (!리눅스방식 && ((veri_konum.ADRES & (sayfa_boyutu - 1)) || (veri_konum.Ofset_değer & (sayfa_boyutu - 1)) || veri_konum.hizalamak_sınır != sayfa_boyutu)) ||
            (리눅스방식 && (((veri_konum.ADRES ^ veri_konum.Ofset_değer) & (sayfa_boyutu - 1)) || !veri_konum.hizalamak_sınır ||
                (veri_konum.hizalamak_sınır & (veri_konum.hizalamak_sınır - 1)) || veri_konum.hizalamak_sınır > 0x200000 || ((veri_konum.ADRES ^ veri_konum.Ofset_değer) & (veri_konum.hizalamak_sınır - 1))))) return kullanıcı_yürütülebilir_hata;
        unsigned 첫항목 = (veri_konum.ADRES - kullanıcı_TABAN) / sayfa_boyutu;
        unsigned girdi_BAĞ_DEĞ_SAY = ((veri_konum.ADRES & (sayfa_boyutu - 1)) + veri_konum.기억영역크기 + sayfa_boyutu - 1) / sayfa_boyutu;
        for (unsigned sayfa_değer = 첫항목; sayfa_değer < 첫항목 + girdi_BAĞ_DEĞ_SAY; sayfa_değer++) {
            if (사용량[sayfa_değer]) return kullanıcı_yürütülebilir_hata;
            사용량[sayfa_değer] = 1;
        }
        if ((veri_konum.Yapılandırma_BITS & 1) && yürütülebilir_Başlık.giriş_noktası >= veri_konum.ADRES && yürütülebilir_Başlık.giriş_noktası < veri_konum.ADRES + veri_konum.파일영역크기 && !(yürütülebilir_Başlık.giriş_noktası & 3)) geçerli_giriş_noktası = 1;
        적재구획++;
    }
    return geçerli_giriş_noktası && (리눅스방식 ? !ABI_Tamam : ABI_Tamam) && 적재구획 ? 0 : kullanıcı_yürütülebilir_hata;
}
int 사용자실행파일검사(const unsigned char *veri, size_t Boyut) { return 실행파일검사(veri, Boyut, 0); }
static void sayfa_düzeni(uintptr_t ADRES, uint64_t Yapılandırma_BITS, unsigned izinler) {
    unsigned ARA_Dizin = (ADRES - kullanıcı_TABAN) / sayfa_boyutu;
    sayfa_Liste[ARA_Dizin] = ADRES | Yapılandırma_BITS;
    izinler_Liste[ARA_Dizin] = izinler;
}
static int kullanıcı_aralık(uintptr_t ADRES, size_t girdi_BAĞ_DEĞ_SAY, int 쓰는중) {
    if (ADRES < kullanıcı_TABAN || !포함된범위(ADRES, girdi_BAĞ_DEĞ_SAY, kullanıcı_Bitiş)) return 0;
    if (!girdi_BAĞ_DEĞ_SAY) return 1;
    unsigned 첫항목 = (ADRES - kullanıcı_TABAN) / sayfa_boyutu, 마지막 = (ADRES + girdi_BAĞ_DEĞ_SAY - 1 - kullanıcı_TABAN) / sayfa_boyutu;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(izinler_Liste[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int örnek_yol(uintptr_t ADRES, char *yol) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!kullanıcı_aralık(ADRES, 1, 0)) return -14;
        yol[순번] = *(const char *)ADRES++;
        if (!yol[순번]) return 0;
    }
    return -36;
}
static intptr_t çekirdek_KR(intptr_t sonuç) { return sonuç < 0 ? -hata_numarası : sonuç; }
static int 대응파일기술자(uint64_t dosya_tanıtıcısı) { return dosya_tanıtıcısı >= 3 && dosya_tanıtıcısı < 19 ? dosya_listesi[dosya_tanıtıcısı - 3] : -1; }
static int yuva_uç_nokta_sahip(uint64_t dosya_tanıtıcısı) { return dosya_tanıtıcısı >= 32 && dosya_tanıtıcısı < 56 && 통신끝점들[dosya_tanıtıcısı - 32]; }
static int ADRES_artış(uintptr_t 가리킴값, size_t süre_değer, struct pk_sockaddr_in *ADRES) {
    if (süre_değer != sizeof(*ADRES)) return -22;
    if (!kullanıcı_aralık(가리킴값, süre_değer, 0)) return -14;
    memcpy(ADRES, (const void *)가리킴값, sizeof(*ADRES));
    return ADRES->sin_family == AF_INET ? 0 : -97;
}
static int ADRES_çıktı_çek(uintptr_t 가리킴값, uintptr_t süre_işaretçi, pk_socklen_t *tampon_kapasite) {
    if (!kullanıcı_aralık(süre_işaretçi, sizeof(*tampon_kapasite), 1)) return -14;
    memcpy(tampon_kapasite, (const void *)süre_işaretçi, sizeof(*tampon_kapasite));
    if (*tampon_kapasite > sizeof(struct pk_sockaddr_in)) *tampon_kapasite = sizeof(struct pk_sockaddr_in);
    if (*tampon_kapasite && !kullanıcı_aralık(가리킴값, *tampon_kapasite, 1)) return -14;
    return 0;
}
static void ADRES_çıktı(uintptr_t 가리킴값, uintptr_t süre_işaretçi, pk_socklen_t tampon_kapasite, int ADRES, int bağlantı_noktası_numarası) {
    struct pk_sockaddr_in değer; memset(&değer, 0, sizeof(değer));
    değer.sin_family = AF_INET; değer.sin_port = pk_htons(bağlantı_noktası_numarası); değer.sin_addr.s_addr = pk_htonl(ADRES);
    if (tampon_kapasite) memcpy((void *)가리킴값, &değer, tampon_kapasite);
    pk_socklen_t süre_değer = sizeof(değer); memcpy((void *)süre_işaretçi, &süre_değer, sizeof(süre_değer));
}
extern uintptr_t Pano_Kanal(uintptr_t, uintptr_t);
static intptr_t yerel_Sistem_Ara(kullanıcı_kare *Dosya_girdi) {
    uintptr_t 첫째값 = Dosya_girdi->yazmaç_veri[0], SANİYE_değer = Dosya_girdi->yazmaç_veri[1], kod_noktası = Dosya_girdi->yazmaç_veri[2];
    char yol[65];
    int dosya_tanıtıcısı, sonuç;
    switch (Dosya_girdi->yazmaç_veri[8]) {
    case 0: return 1; // Öz ABI 버전
    case 1: // write: işaretçi 전체를 검사한 BACK_değer metinÇıktısı/dosya değiştirmek_değer
        if (kod_noktası > 65536) return -22;
        if (!kullanıcı_aralık(SANİYE_değer, kod_noktası, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t Start_çıktı=Saat_değer();
            for (size_t 순번 = 0; 순번 < kod_noktası; 순번++) Pano_Kanal(첫째값, ((const unsigned char *)SANİYE_değer)[순번]);
            /* 큰 tty를 그린 çekirdek_değer 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(devralmak){
                son_tarih_saat+=Saat_değer()-Start_çıktı;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(son_tarih_saat) : "memory");
            }
            return kod_noktası;
        }
        if(첫째값>=40&&yuva_uç_nokta_sahip(첫째값)){
            size_t öğe_BAĞ_DEĞ_SAY=kod_noktası>512?512:kod_noktası;for(size_t 순번=0;순번<öğe_BAĞ_DEĞ_SAY;순번++)자바전문넣기(순번,((const unsigned char *)SANİYE_değer)[순번]);return 자바흐름쓰기(첫째값,öğe_BAĞ_DEĞ_SAY);
        }
        dosya_tanıtıcısı = 대응파일기술자(첫째값); if (dosya_tanıtıcısı < 0) return -9;
        return çekirdek_KR(pk_write(dosya_tanıtıcısı, (const void *)SANİYE_değer, kod_noktası));
    case 2:
        if (kod_noktası > 65536) return -22;
        if (!kullanıcı_aralık(SANİYE_değer, kod_noktası, 1)) return -14;
        if (첫째값 == 0) {
            size_t öğe_BAĞ_DEĞ_SAY = 0;
            while (öğe_BAĞ_DEĞ_SAY < kod_noktası) {
                int karakter_değer = (int32_t)보드글자읽기(); if (karakter_değer == -2) return öğe_BAĞ_DEĞ_SAY; if (karakter_değer < 0) break;
                ((unsigned char *)SANİYE_değer)[öğe_BAĞ_DEĞ_SAY++] = karakter_değer;
            }
            return öğe_BAĞ_DEĞ_SAY ? (intptr_t)öğe_BAĞ_DEĞ_SAY : (kod_noktası ? -11 : 0);
        }
        if(첫째값>=40&&yuva_uç_nokta_sahip(첫째값)){
            sonuç=자바흐름읽기(첫째값,kod_noktası>512?512:kod_noktası);if(sonuç>0)for(int 순번=0;순번<sonuç;순번++)((unsigned char *)SANİYE_değer)[순번]=자바전문얻기(순번);return sonuç;
        }
        dosya_tanıtıcısı = 대응파일기술자(첫째값); if (dosya_tanıtıcısı < 0) return -9;
        return çekirdek_KR(pk_read(dosya_tanıtıcısı, (void *)SANİYE_değer, kod_noktası));
    case 3:
        sonuç = örnek_yol(첫째값, yol); if (sonuç) return sonuç;
        if (SANİYE_değer > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (dosya_listesi[순번] < 0) {
            dosya_tanıtıcısı = pk_open(yol, (int)SANİYE_değer, 0600);
            if (dosya_tanıtıcısı < 0) return -hata_numarası;
            dosya_listesi[순번] = dosya_tanıtıcısı; return 순번 + 3;
        }
        return -24;
    case 4:
        if (yuva_uç_nokta_sahip(첫째값)) { sonuç = Kapat_yuva_uç_nokta(첫째값); if (!sonuç) 통신끝점들[첫째값 - 32] = 0; return sonuç; }
        dosya_tanıtıcısı = 대응파일기술자(첫째값); if (dosya_tanıtıcısı < 0) return -9;
        sonuç = pk_close(dosya_tanıtıcısı); if (!sonuç) dosya_listesi[첫째값 - 3] = -1;
        return çekirdek_KR(sonuç);
    case 5:
        dosya_tanıtıcısı = 대응파일기술자(첫째값); if (dosya_tanıtıcısı < 0) return -9;
        if (kod_noktası > 2) return -22;
        return çekirdek_KR(pk_lseek(dosya_tanıtıcısı, (int64_t)SANİYE_değer, kod_noktası));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 kullanıcı_alanı RW/NX yığın_değer, 새로 노출되는 페이지는 0으로 başlat
        if (!첫째값) return yığın_Bitiş;
        if (첫째값 < kullanıcı_RESİM_Bitiş || 첫째값 > kullanıcı_yığın_Bitiş) return -12;
        uintptr_t 이전쪽들 = (yığın_Bitiş + sayfa_boyutu - 1) & ~(sayfa_boyutu - 1);
        uintptr_t 새쪽들 = (첫째값 + sayfa_boyutu - 1) & ~(sayfa_boyutu - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t veri_konum = 이전쪽들; veri_konum < 새쪽들; veri_konum += sayfa_boyutu) sayfa_düzeni(veri_konum, çekirdek_sayfa, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t veri_konum = 이전쪽들; veri_konum < 새쪽들; veri_konum += sayfa_boyutu) sayfa_düzeni(veri_konum, kullanıcı_R_W, 3);
        } else {
            for (uintptr_t veri_konum = 새쪽들; veri_konum < 이전쪽들; veri_konum += sayfa_boyutu) {
                sayfa_Liste[(veri_konum - kullanıcı_TABAN) / sayfa_boyutu] = 0; izinler_Liste[(veri_konum - kullanıcı_TABAN) / sayfa_boyutu] = 0;
            }
        }
        yığın_Bitiş = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        dosya_tanıtıcısı = 대응파일기술자(첫째값); return dosya_tanıtıcısı < 0 ? -9 : çekirdek_KR(pk_size(dosya_tanıtıcısı));
    case 10:
        dosya_tanıtıcısı = 대응파일기술자(첫째값); return dosya_tanıtıcısı < 0 ? -9 : çekirdek_KR(pk_ftruncate(dosya_tanıtıcısı, (int64_t)SANİYE_değer));
    case 11:
        sonuç = örnek_yol(첫째값, yol); return sonuç ? sonuç : çekirdek_KR(pk_unlink(yol));
    case 12:
        dosya_tanıtıcısı = 대응파일기술자(첫째값); return dosya_tanıtıcısı < 0 ? -9 : çekirdek_KR(pk_fsync(dosya_tanıtıcısı));
    case 13: { // 그래픽 기초 API: kullanıcı_alanı 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = Dosya_girdi->yazmaç_veri[3], 높이값 = Dosya_girdi->yazmaç_veri[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SANİYE_değer > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - SANİYE_değer) return -22;
        for (uintptr_t Y_koordinat = SANİYE_değer; Y_koordinat < SANİYE_değer + 높이값; Y_koordinat++) for (uintptr_t x_koordinatı = 첫째값; x_koordinatı < 첫째값 + 너비값; x_koordinatı++) Pano_piksel(x_koordinatı, Y_koordinat, kod_noktası);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=öğe_BAĞ_DEĞ_SAY; args(index,buffer,capacity)=UTF-8 süre_değer
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (kod_noktası <= 전달인수길이[첫째값]) return -36;
        if (!kullanıcı_aralık(SANİYE_değer, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SANİYE_değer, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;devralmak=1;return Pano_Terminal(13);}
        if(첫째값==2){devralmak=0;return 0;}
        if(첫째값==3)return Pano_Terminal(13);
        if(첫째값!=1||!devralmak)return -22;
        sonuç=(int32_t)보드글자읽기();
        if(sonuç==-4096)return sonuç;
        Start_ZAMANAŞIMI();return sonuç<0?-11:sonuç;
    case 17: { // 유한한 협력 bekle_değer: iletişim 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t Bitiş_saat = Saat_değer() + SIKLIK * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Saat_değer() < Bitiş_saat);
        Start_ZAMANAŞIMI(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 ana_değer·빈 폴더를 검사한다.
        if (SANİYE_değer > 2) return -22;
        sonuç = örnek_yol(첫째값, yol); if (sonuç) return sonuç;
        unsigned süre_değer = 0; while (yol[süre_değer]) süre_değer++;
        sonuç = 자바경로시작(süre_değer); if (sonuç < 0) return sonuç;
        for (unsigned 순번 = 0; 순번 < süre_değer; 순번++) 자바경로바이트(순번, (unsigned char)yol[순번]);
        return SANİYE_değer == 0 ? 자바항목종류() : SANİYE_değer == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int karakter_değer=(int32_t)보드글자읽기();if(karakter_değer==-4096)return karakter_değer;if(karakter_değer>=0)화면누름(sahip_nesne,karakter_değer);Start_ZAMANAŞIMI();}
        if(첫째값==3&&kod_noktası){if(!자바셸대화형())return -95;devralmak=1;Pano_Terminal(300);}
        return 화면호출(sahip_nesne,첫째값,SANİYE_değer,kod_noktası,Dosya_girdi->yazmaç_veri[3],Dosya_girdi->yazmaç_veri[4],Dosya_girdi->yazmaç_veri[5]);
    case 21:
        if(kod_noktası>127)return -22;if(!kullanıcı_aralık(SANİYE_değer,kod_noktası*sizeof(uint32_t),0))return -14;
        return 화면글(sahip_nesne,첫째값,(const uint32_t *)SANİYE_değer,kod_noktası);
    case 22: // 화면 Boyut sorgu_değer: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SANİYE_değer==SOCK_STREAM&&(kod_noktası==0||kod_noktası==6))sonuç=자바흐름만들기();
        else if(SANİYE_değer==SOCK_DGRAM&&(kod_noktası==0||kod_noktası==IPPROTO_UDP))sonuç=자바전문만들기(첫째값,SANİYE_değer,kod_noktası);
        else return -93;
        if (sonuç >= 32 && sonuç < 56) 통신끝점들[sonuç - 32] = 1;
        return sonuç;
    case 33: {
        if (!yuva_uç_nokta_sahip(첫째값)) return -9;
        struct pk_sockaddr_in ADRES;
        sonuç = ADRES_artış(SANİYE_değer, kod_noktası, &ADRES); if (sonuç) return sonuç;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(ADRES.sin_addr.s_addr),pk_htons(ADRES.sin_port)):자바전문묶기(첫째값, pk_htonl(ADRES.sin_addr.s_addr), pk_htons(ADRES.sin_port));
    }
    case 34: {
        if (!yuva_uç_nokta_sahip(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Dosya_girdi->yazmaç_veri[3]) return -95;
        if (kod_noktası > 512) return -90;
        if (kod_noktası && !kullanıcı_aralık(SANİYE_değer, kod_noktası, 0)) return -14;
        struct pk_sockaddr_in ADRES;
        sonuç = ADRES_artış(Dosya_girdi->yazmaç_veri[4], Dosya_girdi->yazmaç_veri[5], &ADRES); if (sonuç) return sonuç;
        for (unsigned 순번 = 0; 순번 < kod_noktası; 순번++) 자바전문넣기(순번, ((const unsigned char *)SANİYE_değer)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(ADRES.sin_addr.s_addr), pk_htons(ADRES.sin_port), kod_noktası);
    }
    case 35: {
        if (!yuva_uç_nokta_sahip(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Dosya_girdi->yazmaç_veri[3]) return -95;
        if (kod_noktası > 512) return -90;
        if (kod_noktası && !kullanıcı_aralık(SANİYE_değer, kod_noktası, 1)) return -14;
        pk_socklen_t tampon_kapasite = 0;
        if (Dosya_girdi->yazmaç_veri[4]) { sonuç = ADRES_çıktı_çek(Dosya_girdi->yazmaç_veri[4], Dosya_girdi->yazmaç_veri[5], &tampon_kapasite); if (sonuç) return sonuç; }
        sonuç = 자바전문받기(첫째값, kod_noktası); if (sonuç < 0) return sonuç;
        for (int 순번 = 0; 순번 < sonuç; 순번++) ((unsigned char *)SANİYE_değer)[순번] = 자바전문얻기(순번);
        if (Dosya_girdi->yazmaç_veri[4]) ADRES_çıktı(Dosya_girdi->yazmaç_veri[4], Dosya_girdi->yazmaç_veri[5], tampon_kapasite, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return sonuç;
    }
    case 36: {
        if (!yuva_uç_nokta_sahip(첫째값)) return -9;
        pk_socklen_t tampon_kapasite;
        sonuç = ADRES_çıktı_çek(SANİYE_değer, kod_noktası, &tampon_kapasite); if (sonuç) return sonuç;
        ADRES_çıktı(SANİYE_değer,kod_noktası,tampon_kapasite,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!yuva_uç_nokta_sahip(첫째값))return -9;struct pk_sockaddr_in ADRES;
        sonuç=ADRES_artış(SANİYE_değer,kod_noktası,&ADRES);if(sonuç)return sonuç;
        return 자바흐름연결(첫째값,pk_htonl(ADRES.sin_addr.s_addr),pk_htons(ADRES.sin_port));
    }
    case 38: return 첫째값>=40&&yuva_uç_nokta_sahip(첫째값)?자바흐름듣기(첫째값,SANİYE_değer):-9;
    case 39:
        if(첫째값<40||!yuva_uç_nokta_sahip(첫째값))return -9;
        if(SANİYE_değer||kod_noktası)return -95;sonuç=자바흐름연결받기(첫째값);if(sonuç>=40&&sonuç<56)통신끝점들[sonuç-32]=1;return sonuç;
    case 40: return 첫째값>=40&&yuva_uç_nokta_sahip(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t sistem_çağrısı(kullanıcı_kare *Dosya_girdi) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(Dosya_girdi) : yerel_Sistem_Ara(Dosya_girdi);
}
static void İade_çekirdek(kullanıcı_kare *Dosya_girdi, int sonuç) {
    Dur_ZAMANAŞIMI();
    Dosya_girdi->yazmaç_veri[0] = (uint64_t)(int64_t)sonuç;
    Dosya_girdi->komut_konum = (uintptr_t)kullanıcı_İade;
    Dosya_girdi->Durum_KOD = 0x3c5; // EL1h, DAIF masked
}
int kullanıcı_özel_durumu(kullanıcı_kare *Dosya_girdi, unsigned kesen) {
    if (!Aktif || (Dosya_girdi->Durum_KOD & 15) != 0) return 0;
    if (kesen) {
        uint32_t kabul_etme_değer = makine_yazmaç(IRQ_CPU_arabirim + 0xc), tanımlayıcı_değer = kabul_etme_değer & 1023;
        if (tanımlayıcı_değer == 30) { İade_çekirdek(Dosya_girdi, kullanıcı_ZAMANAŞIMI); makine_yazmaç(IRQ_CPU_arabirim + 0x10) = kabul_etme_değer; return 1; }
        if (tanımlayıcı_değer < 1020) makine_yazmaç(IRQ_CPU_arabirim + 0x10) = kabul_etme_değer;
        return 1;
    }
    uint64_t özel_durum_Durum; __asm__ volatile("mrs %0, esr_el1" : "=r"(özel_durum_Durum));
    if (Saat_değer() >= son_tarih_saat) { İade_çekirdek(Dosya_girdi, kullanıcı_ZAMANAŞIMI); return 1; }
    unsigned özel_durum_alan = özel_durum_Durum >> 26;
    if (özel_durum_alan == 0x15 && (özel_durum_Durum & 0xffff) == 0) {
        if (리눅스규약 ? Dosya_girdi->yazmaç_veri[8] == 93 || Dosya_girdi->yazmaç_veri[8] == 94 : Dosya_girdi->yazmaç_veri[8] == 6) İade_çekirdek(Dosya_girdi, (int)(Dosya_girdi->yazmaç_veri[0] & 255));
        else {
            intptr_t sonuç=sistem_çağrısı(Dosya_girdi);
            if(sonuç==-4096&&devralmak){
                저장값[sahip_nesne].yürütme_kare=*Dosya_girdi;저장값[sahip_nesne].yürütme_kare.komut_konum-=4;
                사용자실수보관(저장값[sahip_nesne].kayan_nokta_Durum);İade_çekirdek(Dosya_girdi,사용자중단됨);
            }else Dosya_girdi->yazmaç_veri[0]=(uint64_t)sonuç;
        }
    } else İade_çekirdek(Dosya_girdi, özel_durum_alan == 0x24 ? kullanıcı_veri_hata : özel_durum_alan == 0x20 ? kullanıcı_yürütme_hata : 사용자잘못된명령);
    return 1;
}

// 생성된 const ELF Grup_değer: 실행은 반드시 program_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *veri; size_t Boyut; unsigned 전달값; } program;
#include "programs.h"
static void *gölge_kopya(unsigned konum_dizini){return (void *)(0x04000000ul+konum_dizini*(kullanıcı_Bitiş-kullanıcı_TABAN));}
static int Son_program(int sonuç){
    사용자누적시각[sahip_nesne]+=(uint32_t)보드밀리초()-kullanıcı_yürütme_saat[sahip_nesne];
    Dur_ZAMANAŞIMI();Aktif=0;
    if(sonuç==사용자중단됨){
        저장된작업 *dize_veri=&저장값[sahip_nesne];dize_veri->duraklatılmış_Durum=1;dize_veri->devralmak=devralmak;dize_veri->리눅스규약=리눅스규약;dize_veri->dinamik_bellek=yığın_Bitiş;dize_veri->인수개수=전달인수개수;
        memcpy(dize_veri->izinler_Liste,izinler_Liste,sizeof(izinler_Liste));memcpy(dize_veri->dosya_listesi,dosya_listesi,sizeof(dosya_listesi));memcpy(dize_veri->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(dize_veri->bağımsız_değişken_DİZİ,전달인수,sizeof(전달인수));memcpy(dize_veri->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<kullanıcı_sayfa_BAĞ_DEĞ_SAY;순번++)if(izinler_Liste[순번])memcpy((unsigned char *)gölge_kopya(sahip_nesne)+순번*sayfa_boyutu,(void *)(kullanıcı_TABAN+순번*sayfa_boyutu),sayfa_boyutu);
    }else{
        저장값[sahip_nesne].duraklatılmış_Durum=0;화면초기화(sahip_nesne);
        for(unsigned 순번=0;순번<16;순번++)if(dosya_listesi[순번]>=0)pk_close(dosya_listesi[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])Kapat_yuva_uç_nokta(순번+32);
    }
    for(unsigned 순번=0;순번<kullanıcı_sayfa_BAĞ_DEĞ_SAY;순번++){sayfa_Liste[순번]=0;izinler_Liste[순번]=0;}변환표맞추기();return sonuç;
}
uintptr_t Pano_kullanıcı_kontrolü(uintptr_t Eylem){
    unsigned konum_dizini=Eylem&15;if(konum_dizini>=4||Aktif)return (uint32_t)-22;
    저장된작업 *dize_veri=&저장값[konum_dizini];
    if(Eylem>=32){if(dize_veri->duraklatılmış_Durum){for(unsigned 순번=0;순번<16;순번++)if(dize_veri->dosya_listesi[순번]>=0)pk_close(dize_veri->dosya_listesi[순번]);for(unsigned 순번=0;순번<24;순번++)if(dize_veri->통신끝점들[순번])Kapat_yuva_uç_nokta(순번+32);}dize_veri->duraklatılmış_Durum=0;화면초기화(konum_dizini);return 0;}
    if(Eylem>=16)return dize_veri->duraklatılmış_Durum;
    if(!dize_veri->duraklatılmış_Durum)return (uint32_t)-22;
    sahip_nesne=konum_dizini;devralmak=dize_veri->devralmak;리눅스규약=dize_veri->리눅스규약;yığın_Bitiş=dize_veri->dinamik_bellek;전달인수개수=dize_veri->인수개수;
    memcpy(dosya_listesi,dize_veri->dosya_listesi,sizeof(dosya_listesi));memcpy(통신끝점들,dize_veri->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,dize_veri->bağımsız_değişken_DİZİ,sizeof(전달인수));memcpy(전달인수길이,dize_veri->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<kullanıcı_sayfa_BAĞ_DEĞ_SAY;순번++)sayfa_Liste[순번]=(kullanıcı_TABAN+순번*sayfa_boyutu)|çekirdek_sayfa;변환표맞추기();
    memset((void *)kullanıcı_TABAN,0,kullanıcı_Bitiş-kullanıcı_TABAN);
    for(unsigned 순번=0;순번<kullanıcı_sayfa_BAĞ_DEĞ_SAY;순번++)if(dize_veri->izinler_Liste[순번])memcpy((void *)(kullanıcı_TABAN+순번*sayfa_boyutu),(unsigned char *)gölge_kopya(konum_dizini)+순번*sayfa_boyutu,sayfa_boyutu);
    memcpy(izinler_Liste,dize_veri->izinler_Liste,sizeof(izinler_Liste));
    for(unsigned 순번=0;순번<kullanıcı_sayfa_BAĞ_DEĞ_SAY;순번++){unsigned veri_konum=izinler_Liste[순번];sayfa_Liste[순번]=veri_konum?(kullanıcı_TABAN+순번*sayfa_boyutu)|(veri_konum==3?kullanıcı_R_W:veri_konum==5?사용자읽고실행:kullanıcı_salt_okunur):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");Aktif=1;dize_veri->duraklatılmış_Durum=0;Start_ZAMANAŞIMI();
    kullanıcı_yürütme_saat[sahip_nesne]=보드밀리초();
    return (uint32_t)Son_program(kullanıcı_özgeçmiş(&dize_veri->yürütme_kare,dize_veri->kayan_nokta_Durum));
}
static int çalıştırma_program(const unsigned char *veri, size_t Boyut, unsigned 전달값, int 리눅스방식, const char *İsim) {
    if (Aktif) return -16;
    sahip_nesne=Pano_Terminal(11);if(sahip_nesne<0||sahip_nesne>3||저장값[sahip_nesne].duraklatılmış_Durum)return -16;devralmak=0;
    int geçerli = 실행파일검사(veri, Boyut, 리눅스방식); if (geçerli) return geçerli;
    리눅스규약 = 리눅스방식;
    unsigned ad_Dizin=0;
    while (*İsim && ad_Dizin<31) kullanıcı_komut_ad[sahip_nesne][ad_Dizin++]=(unsigned char)*İsim++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (ad_Dizin) kullanıcı_komut_ad[sahip_nesne][ad_Dizin++]=' ';
        for (unsigned konum_dizini=0; konum_dizini<전달인수길이[0]; konum_dizini++) kullanıcı_komut_ad[sahip_nesne][ad_Dizin++]=전달인수[0][konum_dizini];
    }
    kullanıcı_komut_ad[sahip_nesne][ad_Dizin]=0; kullanıcı_numarası[sahip_nesne]=Sonraki_kullanıcı_numarası++;
    if (Sonraki_kullanıcı_numarası>0x7fffffffu) Sonraki_kullanıcı_numarası=10;
    kullanıcı_Start_saat[sahip_nesne]=보드밀리초(); 사용자누적시각[sahip_nesne]=0;
    for (unsigned 순번 = 0; 순번 < kullanıcı_sayfa_BAĞ_DEĞ_SAY; 순번++) sayfa_Liste[순번] = (kullanıcı_TABAN + 순번 * sayfa_boyutu) | çekirdek_sayfa;
    변환표맞추기();
    memset((void *)kullanıcı_TABAN, 0, kullanıcı_Bitiş - kullanıcı_TABAN);
    memset(izinler_Liste, 0, sizeof(izinler_Liste));
    실행파일머리 yürütülebilir_Başlık; memcpy(&yürütülebilir_Başlık, veri, sizeof(yürütülebilir_Başlık));
    for (unsigned 순번 = 0; 순번 < yürütülebilir_Başlık.program_Başlık_BAĞ_DEĞ_SAY; 순번++) {
        실행파일구획 veri_konum; memcpy(&veri_konum, veri + yürütülebilir_Başlık.program_Başlık_Ofset + 순번 * sizeof(veri_konum), sizeof(veri_konum));
        if (veri_konum.TÜR_alan != 1 || !veri_konum.기억영역크기) continue;
        if (veri_konum.파일영역크기) memcpy((void *)(uintptr_t)veri_konum.ADRES, veri + veri_konum.Ofset_değer, veri_konum.파일영역크기);
        for (uintptr_t geçerli_konum = veri_konum.ADRES & ~(sayfa_boyutu - 1); geçerli_konum < veri_konum.ADRES + veri_konum.기억영역크기; geçerli_konum += sayfa_boyutu) {
            izinler_Liste[(geçerli_konum - kullanıcı_TABAN) / sayfa_boyutu] = (veri_konum.Yapılandırma_BITS & 2) ? 3 : ((veri_konum.Yapılandırma_BITS & 1) ? 5 : 1);
        }
    }
    for (uintptr_t geçerli_konum = kullanıcı_Yığın_ADRES; geçerli_konum < kullanıcı_Bitiş; geçerli_konum += sayfa_boyutu) izinler_Liste[(geçerli_konum - kullanıcı_TABAN) / sayfa_boyutu] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(yürütülebilir_Başlık.giriş_noktası) : kullanıcı_Bitiş;
    for (unsigned 순번 = 0; 순번 < kullanıcı_sayfa_BAĞ_DEĞ_SAY; 순번++) {
        unsigned izinler = izinler_Liste[순번];
        sayfa_Liste[순번] = izinler ? (kullanıcı_TABAN + 순번 * sayfa_boyutu) | (izinler == 3 ? kullanıcı_R_W : izinler == 5 ? 사용자읽고실행 : kullanıcı_salt_okunur) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) dosya_listesi[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    yığın_Bitiş = kullanıcı_RESİM_Bitiş;
    Aktif = 1; Start_ZAMANAŞIMI();
    kullanıcı_yürütme_saat[sahip_nesne]=보드밀리초();
    int sonuç = kullanıcı_girmek(yürütülebilir_Başlık.giriş_noktası, 초기쌓임공간, 전달값);
    return Son_program(sonuç);
}
uintptr_t Pano_kullanıcı_çalıştırma(uintptr_t ARA_Dizin) {
    if (ARA_Dizin >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *İsim=ARA_Dizin==10?"javac":ARA_Dizin==11?"java":ARA_Dizin==12?"python":ARA_Dizin==13?"vi":ARA_Dizin==14?"jar":ARA_Dizin==15?"cc":ARA_Dizin==16?"jaot":"ELF";
    return (uint32_t)çalıştırma_program(실행항목들[ARA_Dizin].veri, 실행항목들[ARA_Dizin].Boyut, 실행항목들[ARA_Dizin].전달값, 0, İsim);
}
static uintptr_t yürütmek_Dosya(int 리눅스방식) {
    static unsigned char RESİM[16384];
    if (Aktif || !전달인수개수) return (uint32_t)-22;
    int dosya_tanıtıcısı = pk_open((const char *)전달인수[0], salt_okunur_değer, 0);
    if (dosya_tanıtıcısı < 0) return (uint32_t)-hata_numarası;
    int Boyut = pk_size(dosya_tanıtıcısı);
    if (Boyut < 0 || (unsigned)Boyut > sizeof(RESİM)) { pk_close(dosya_tanıtıcısı); return (uint32_t)-27; }
    int GETİRİ_BAĞ_DEĞ_SAY = pk_read(dosya_tanıtıcısı, RESİM, Boyut); pk_close(dosya_tanıtıcısı);
    if (GETİRİ_BAĞ_DEĞ_SAY != Boyut) return (uint32_t)-5;
    return (uint32_t)çalıştırma_program(RESİM, Boyut, 0, 리눅스방식, "");
}
uintptr_t Pano_kullanıcı_Dosya(void) { return yürütmek_Dosya(0); }
uintptr_t 보드사용자리눅스파일(void) { return yürütmek_Dosya(1); }
uintptr_t Pano_kullanıcı_doğrulamak(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].veri, 잘못된실행항목들[순번].Boyut) != kullanıcı_yürütülebilir_hata) return 순번 + 1;
    return 0;
}
