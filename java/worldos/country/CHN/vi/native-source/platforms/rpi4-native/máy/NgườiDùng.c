#include "../cáchĐặtTên/cácTênLiênKếtMáy.h"
#include "thôngTinMànHình.h"
// EL0 thựcThiLệnh máy giáTrịTầng. Tệp DữLiệu/정책은 기존 AOT Java 커널에 위임한다.
#include "NgườiDùng.h"
#include "ABITệp.h"
#include "ABIMạng.h"
#include "../NgănXếpMạng/NgănXếpMạng.h"
extern int32_t từXaMạngJava(int32_t), địaChỉLuồngJava(int32_t);
#define thanhGhiMáy(giáTrịĐầuTiên) (*(volatile uint32_t *)(uintptr_t)(giáTrịĐầuTiên))
#define bộPhânPhốiNgắtXửLý 0xff841000ul
#define giaoDiệnCPUNgắtXửLý 0xff842000ul
#define cỡTrang 4096ul
#define dấuMốcTruyCập (1ul << 10)
#define quyềnThựcThiKhôngCó (1ul << 53)
#define thựcThiKhôngCóNgườiDùng (1ul << 54)
#define bộNhớBìnhThường ((1ul << 2) | (3ul << 8) | dấuMốcTruyCập)
#define trangNhân (3ul | bộNhớBìnhThường | quyềnThựcThiKhôngCó | thựcThiKhôngCóNgườiDùng)
#define ghiĐọcNgườiDùng (3ul | bộNhớBìnhThường | (1ul << 6) | quyềnThựcThiKhôngCó | thựcThiKhôngCóNgườiDùng)
#define chỉĐọcNgườiDùng (3ul | bộNhớBìnhThường | (3ul << 6) | quyềnThựcThiKhôngCó | thựcThiKhôngCóNgườiDùng)
#define thựcThiĐọcNgườiDùng (3ul | bộNhớBìnhThường | (3ul << 6) | quyềnThựcThiKhôngCó)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t đặtKýTựBoMạch(uintptr_t), lấyKýTựBoMạch(void), miliGiâyGọnBoMạch(void);
extern uintptr_t điểmẢnhBoMạch(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t bộĐệmKhungBoMạch(void);
extern uintptr_t thiếtBịCuốiBoMạch(uintptr_t);
extern int đangChờThiếtBịCuối(void);
extern int32_t tươngTácVỏLệnhJava(void);
extern int32_t bắtChạyĐườngDẫnJava(int32_t), byteĐườngDẫnJava(int32_t,int32_t);
extern int32_t thưMụcTạoJava(void), thưMụcGỡJava(void), loạiMụcJava(void);
extern int gọiThựcHiệnMànHình(int,unsigned,int,int,int,int,int),vănBảnMànHình(int,int,const uint32_t *,unsigned);
extern void khởiTạoMànHình(int),nhấnMànHình(int,unsigned);
extern int tiếpDiễnNgườiDùng(khungNgườiDùng *,void *);
extern void lưuDấuPhẩyĐộngGọnNgườiDùng(void *);
extern int vàoNgườiDùng(uintptr_t điểmMục, uintptr_t lưuTrữNgănXếp, uintptr_t giáTrịĐãChuyểnTiếp);
extern void trảVềNgườiDùng(void);
extern void dừngKhẩnNhân(const char *) __attribute__((noreturn));
static uint64_t địaChỉGốcCây[512] __attribute__((aligned(4096)));
static uint64_t giữa[4][512] __attribute__((aligned(4096)));
static uint64_t danhSáchTrang[sốLượngTrangNgườiDùng] __attribute__((aligned(4096)));
static uint8_t danhSáchCácQuyền[sốLượngTrangNgườiDùng];
static int hoạtĐộng, danhSáchTệp[16], aBILinux;
static unsigned cácĐiểmCuốiỔCắmMạng[24];
extern int32_t ổCắmMạngMạngJava(int32_t, int32_t, int32_t), ràngBuộcMạngJava(int32_t, int32_t, int32_t);
extern int32_t đặtMạngJava(int32_t, int32_t), lấyMạngJava(int32_t), gửiMạngJava(int32_t, int32_t, int32_t, int32_t);
extern int32_t nhậnGọnMạngJava(int32_t, int32_t), cổngMạngJava(int32_t), địaChỉMạngJava(int32_t), đốiTácMạngJava(int32_t), đóngMạngJava(int32_t);
extern int32_t tạoLuồngJava(void),ràngBuộcLuồngJava(int32_t,int32_t,int32_t),lắngNgheLuồngJava(int32_t,int32_t),kếtNốiLuồngJava(int32_t,int32_t,int32_t),chấpNhậnLuồngJava(int32_t),đọcLuồngJava(int32_t,int32_t),ghiLuồngJava(int32_t,int32_t),cổngLuồngJava(int32_t),đốiTácLuồngJava(int32_t),đóngLuồngJava(int32_t);
static int đóngĐiểmCuốiỔCắmMạng(unsigned thẻXửLýTệp){return thẻXửLýTệp<40?đóngMạngJava(thẻXửLýTệp):đóngLuồngJava(thẻXửLýTệp);}
static uint64_t tầnSố, thờiGianHạnChót;
static uintptr_t kếtThúcVùngNhớĐộng;
// giáTrịNhân 셸이 준비한 UTF-8 cácĐốiSố. EL0에는 saoChépGiáTrị 호출만 제공한다.
static unsigned sốLượngĐốiSốĐãChuyểnTiếp, độDàiĐốiSốĐãChuyểnTiếp[8];
static unsigned char đốiSốĐãChuyểnTiếp[8][256];
typedef struct {
    int trạngTháiĐãTạmDừng,tươngTác,aBILinux,danhSáchTệp[16]; unsigned cácĐiểmCuốiỔCắmMạng[24],sốLượngCácĐốiSố,độDàiĐốiSố[8];
    unsigned char mảngĐốiSố[8][256],danhSáchCácQuyền[sốLượngTrangNgườiDùng];
    uintptr_t lưuTrữVùngNhớĐộng; khungNgườiDùng khungViệcThựcThi;
    unsigned char trạngTháiĐiểmDấuPhẩyĐộng[528] __attribute__((aligned(16)));
} tiếnTrìnhĐãLưu;
static tiếnTrìnhĐãLưu đãLưu[4];
static int đốiTượngChủSởHữu,tươngTác;
static uint32_t sốNgườiDùng[4], thờiGianBắtChạyNgườiDùng[4], thờiGianTíchLũyNgườiDùng[4], thờiGianViệcThựcThiNgườiDùng[4], sốNgườiDùngKếTiếp=10;
static unsigned char tênLệnhNgườiDùng[4][288];
uint32_t đọcTrạngTháiNgườiDùng(unsigned giáTrịMục, unsigned sốHiệu) {
    unsigned chỉSốVịTrí=sốHiệu&3;
    int giáTrịTrạngThái=(hoạtĐộng && đốiTượngChủSởHữu==(int)chỉSốVịTrí) ? 1 : đãLưu[chỉSốVịTrí].trạngTháiĐãTạmDừng ? 2 : 0;
    if (giáTrịMục==0) return giáTrịTrạngThái;
    if (!giáTrịTrạngThái) return 0;
    if (giáTrịMục==1) return sốNgườiDùng[chỉSốVịTrí];
    if (giáTrịMục==2) {
        unsigned char *danhSáchCácTrang=giáTrịTrạngThái==1?danhSáchCácQuyền:đãLưu[chỉSốVịTrí].danhSáchCácQuyền;
        unsigned sốLượngTrang=0; for (unsigned chỉSốThứBậc=0; chỉSốThứBậc<sốLượngTrangNgườiDùng; chỉSốThứBậc++) if(danhSáchCácTrang[chỉSốThứBậc]) sốLượngTrang++;
        return sốLượngTrang*4;
    }
    if (giáTrịMục==3) return (uint32_t)miliGiâyGọnBoMạch()-thờiGianBắtChạyNgườiDùng[chỉSốVịTrí];
    if (giáTrịMục==4) return thờiGianTíchLũyNgườiDùng[chỉSốVịTrí]+(giáTrịTrạngThái==1?(uint32_t)miliGiâyGọnBoMạch()-thờiGianViệcThựcThiNgườiDùng[chỉSốVịTrí]:0);
    if (giáTrịMục==5) return sốHiệu/4<sizeof(tênLệnhNgườiDùng[0])?tênLệnhNgườiDùng[chỉSốVịTrí][sốHiệu/4]:0;
    return 0;
}
uintptr_t bắtĐầuDãyĐốiSốBoMạch(uintptr_t sốLượngMục) {
    if (hoạtĐộng || sốLượngMục > 8) return (uint32_t)-22;
    sốLượngĐốiSốĐãChuyểnTiếp = sốLượngMục;
    memset(độDàiĐốiSốĐãChuyểnTiếp, 0, sizeof(độDàiĐốiSốĐãChuyểnTiếp));
    memset(đốiSốĐãChuyểnTiếp, 0, sizeof(đốiSốĐãChuyểnTiếp));
    return 0;
}
uintptr_t byteDãyĐốiSốBoMạch(uintptr_t chỉSốTraCứu, uintptr_t vịTríHiệnTại, uintptr_t dữLiệuByte) {
    if (hoạtĐộng || chỉSốTraCứu >= sốLượngĐốiSốĐãChuyểnTiếp || vịTríHiệnTại >= 255 || vịTríHiệnTại != độDàiĐốiSốĐãChuyểnTiếp[chỉSốTraCứu] || !dữLiệuByte || dữLiệuByte > 255)
        return (uint32_t)-22;
    đốiSốĐãChuyểnTiếp[chỉSốTraCứu][vịTríHiệnTại] = dữLiệuByte;
    độDàiĐốiSốĐãChuyểnTiếp[chỉSốTraCứu] = vịTríHiệnTại + 1;
    return 0;
}
static void cácBảngTraĐồngBộ(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t giáTrịĐồngHồ(void) { uint64_t dữLiệuTạm; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(dữLiệuTạm)); return dữLiệuTạm; }
static void dừngHếtGiờ(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    thanhGhiMáy(bộPhânPhốiNgắtXửLý + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void bắtChạyHếtGiờ(void) {
    uint64_t giáTrịGiãnCách = tầnSố * 2, bật = 1;
    thờiGianHạnChót = giáTrịĐồngHồ() + giáTrịGiãnCách;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(giáTrịGiãnCách), "r"(bật) : "memory");
}
void khởiTạoGọnHệThốngNgườiDùng(void) {
    for (unsigned khốiDữLiệu = 0; khốiDữLiệu < 4; khốiDữLiệu++) {
        địaChỉGốcCây[khốiDữLiệu] = (uintptr_t)giữa[khốiDữLiệu] | 3;
        for (unsigned chỉSốThứBậc = 0; chỉSốThứBậc < 512; chỉSốThứBậc++) {
            uintptr_t địaChỉ = ((uintptr_t)khốiDữLiệu << 30) | ((uintptr_t)chỉSốThứBậc << 21);
            giữa[khốiDữLiệu][chỉSốThứBậc] = địaChỉ | 1 | dấuMốcTruyCập | thựcThiKhôngCóNgườiDùng;
            if (địaChỉ >= 0xfc000000ul) giữa[khốiDữLiệu][chỉSốThứBậc] |= quyềnThựcThiKhôngCó; // Device-nGnRnE
            else giữa[khốiDữLiệu][chỉSốThứBậc] |= bộNhớBìnhThường; // Normal, non-cacheable
        }
    }
    for (unsigned giáTrịThứHai = 0; giáTrịThứHai < sốLượngTrangNgườiDùng / 512; giáTrịThứHai++)
        giữa[0][(cơSởNgườiDùng >> 21) + giáTrịThứHai] = (uintptr_t)(danhSáchTrang + giáTrịThứHai * 512) | 3;
    for (unsigned chỉSốThứBậc = 0; chỉSốThứBậc < sốLượngTrangNgườiDùng; chỉSốThứBậc++) danhSáchTrang[chỉSốThứBậc] = (cơSởNgườiDùng + chỉSốThứBậc * cỡTrang) | trangNhân;
    uint64_t thanhGhiThuộcTínhBộNhớ = 0x4400, điềuKhiểnBảnDịchĐịaChỉ = 32 | (3ul << 12) | (1ul << 23), sCTLR;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(thanhGhiThuộcTínhBộNhớ), "r"(điềuKhiểnBảnDịchĐịaChỉ), "r"((uintptr_t)địaChỉGốcCây) : "memory");
    cácBảngTraĐồngBộ();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(sCTLR));
    sCTLR = (sCTLR & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(sCTLR) : "memory");
    uint64_t trạngTháiĐiểmDấuPhẩyĐộng = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(trạngTháiĐiểmDấuPhẩyĐộng) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(tầnSố));
    dừngHếtGiờ();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 giáTrịĐiểmMục 때만 choPhépGiáTrị.
    thanhGhiMáy(bộPhânPhốiNgắtXửLý) = 0;
    thanhGhiMáy(bộPhânPhốiNgắtXửLý + 0x180) = 0xffffffff;
    thanhGhiMáy(bộPhânPhốiNgắtXửLý + 0x80) = 0xffffffff;
    thanhGhiMáy(bộPhânPhốiNgắtXửLý + 0x280) = 1u << 30;
    thanhGhiMáy(bộPhânPhốiNgắtXửLý + 0x41c) = 0x80808080;
    thanhGhiMáy(bộPhânPhốiNgắtXửLý + 0x100) = 1u << 30;
    thanhGhiMáy(giaoDiệnCPUNgắtXửLý + 4) = 0xff;
    thanhGhiMáy(giaoDiệnCPUNgắtXửLý + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 làBìnhThường 확인할 trịSố 있다.
    int bảoMật = (thanhGhiMáy(bộPhânPhốiNgắtXửLý + 4) & (1u << 10)) != 0;
    thanhGhiMáy(bộPhânPhốiNgắtXửLý) = bảoMật ? 1 : 3;
    thanhGhiMáy(giaoDiệnCPUNgắtXửLý) = bảoMật ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char địnhDanhGọn[16]; uint16_t loạiMụcKiểu, kiểuMáy; uint32_t sốPhiênBản;
    uint64_t điểmMục, độLệchĐầuMụcChươngTrình, độLệchĐầuMụcMụcĐoạn; uint32_t cácBitCấuHình;
    uint16_t cỡĐầuMụcTệpThựcThi, cỡMụcĐầuMụcChươngTrình, sốLượngĐầuMụcChươngTrình, cỡMụcĐầuMụcMụcĐoạn, sốLượngĐầuMụcMụcĐoạn, chỉSốBảngTraTênMụcĐoạn;
} đầuMụcELF;
typedef struct { uint32_t loạiMụcKiểu, cácBitCấuHình; uint64_t giáTrịĐộLệch, địaChỉ, địaChỉVậtLý, cỡVùngTệp, cỡVùngBộNhớ, ranhGiớiCănChỉnh; } chươngTrìnhELF;
_Static_assert(sizeof(đầuMụcELF) == 64 && sizeof(chươngTrìnhELF) == 56, "ELF layout");
_Static_assert(sizeof(khungNgườiDùng) == 272, "exception assembly layout");
static int đượcChứa(uint64_t giáTrịĐộLệch, uint64_t cỡ, uint64_t độLệchKếtThúc) {
    return giáTrịĐộLệch <= độLệchKếtThúc && cỡ <= độLệchKếtThúc - giáTrịĐộLệch;
}
static int kiểmTraThôngTinPhụTrợ(const unsigned char *vịTríDữLiệu, size_t cỡ) {
    size_t vịTríHiệnTại = 0;
    while (đượcChứa(vịTríHiệnTại, 12, cỡ)) {
        uint32_t cácTừTừVựng[3]; memcpy(cácTừTừVựng, vịTríDữLiệu + vịTríHiệnTại, 12); vịTríHiệnTại += 12;
        uint64_t cỡVùngTên = ((uint64_t)cácTừTừVựng[0] + 3) & ~3ul;
        uint64_t cỡMôTả = ((uint64_t)cácTừTừVựng[1] + 3) & ~3ul;
        if (!đượcChứa(vịTríHiệnTại, cỡVùngTên, cỡ) || !đượcChứa(vịTríHiệnTại + cỡVùngTên, cỡMôTả, cỡ)) return 0;
        const unsigned char tên[] = {'J','K','O','R','O','S',0};
        int làBằng = cácTừTừVựng[0] == sizeof(tên) && cácTừTừVựng[1] == 4 && cácTừTừVựng[2] == 1;
        if (làBằng) for (unsigned chỉSốThứBậc = 0; chỉSốThứBậc < sizeof(tên); chỉSốThứBậc++) if (vịTríDữLiệu[vịTríHiệnTại + chỉSốThứBậc] != tên[chỉSốThứBậc]) làBằng = 0;
        uint32_t sốPhiênBản = 0;
        if (làBằng) memcpy(&sốPhiênBản, vịTríDữLiệu + vịTríHiệnTại + cỡVùngTên, 4);
        if (làBằng && sốPhiênBản == 1) return 1;
        vịTríHiệnTại += cỡVùngTên + cỡMôTả;
    }
    return 0;
}
static int thẩmĐịnhELF(const unsigned char *DữLiệu, size_t cỡ, int chếĐộLinux) {
    if (cỡ < sizeof(đầuMụcELF)) return lỗiTệpThựcThiNgườiDùng;
    đầuMụcELF đầuMụcTệpThựcThi; memcpy(&đầuMụcTệpThựcThi, DữLiệu, sizeof(đầuMụcTệpThựcThi));
    if (đầuMụcTệpThựcThi.địnhDanhGọn[0] != 127 || đầuMụcTệpThựcThi.địnhDanhGọn[1] != 'E' || đầuMụcTệpThựcThi.địnhDanhGọn[2] != 'L' || đầuMụcTệpThựcThi.địnhDanhGọn[3] != 'F' ||
        đầuMụcTệpThựcThi.địnhDanhGọn[4] != 2 || đầuMụcTệpThựcThi.địnhDanhGọn[5] != 1 || đầuMụcTệpThựcThi.địnhDanhGọn[6] != 1 || (đầuMụcTệpThựcThi.địnhDanhGọn[7] != 0 && (!chếĐộLinux || đầuMụcTệpThựcThi.địnhDanhGọn[7] != 3)) ||
        đầuMụcTệpThựcThi.loạiMụcKiểu != 2 || đầuMụcTệpThựcThi.kiểuMáy != 183 || đầuMụcTệpThựcThi.sốPhiênBản != 1 || đầuMụcTệpThựcThi.cácBitCấuHình || đầuMụcTệpThựcThi.cỡĐầuMụcTệpThựcThi != sizeof(đầuMụcTệpThựcThi) ||
        đầuMụcTệpThựcThi.cỡMụcĐầuMụcChươngTrình != sizeof(chươngTrìnhELF) || !đầuMụcTệpThựcThi.sốLượngĐầuMụcChươngTrình || đầuMụcTệpThựcThi.sốLượngĐầuMụcChươngTrình > 16 ||
        đầuMụcTệpThựcThi.độLệchĐầuMụcChươngTrình < sizeof(đầuMụcTệpThựcThi) || !đượcChứa(đầuMụcTệpThựcThi.độLệchĐầuMụcChươngTrình, (uint64_t)đầuMụcTệpThựcThi.sốLượngĐầuMụcChươngTrình * sizeof(chươngTrìnhELF), cỡ)) return lỗiTệpThựcThiNgườiDùng;
    uint8_t sứcChứaĐãDùng[(kếtThúcẢnhNgườiDùng - cơSởNgườiDùng) / cỡTrang] = {0};
    int điểmMụcHợpLệ = 0, ổnABI = 0, cácLầnNạp = 0;
    for (unsigned chỉSốThứBậc = 0; chỉSốThứBậc < đầuMụcTệpThựcThi.sốLượngĐầuMụcChươngTrình; chỉSốThứBậc++) {
        chươngTrìnhELF vịTríDữLiệu; memcpy(&vịTríDữLiệu, DữLiệu + đầuMụcTệpThựcThi.độLệchĐầuMụcChươngTrình + chỉSốThứBậc * sizeof(vịTríDữLiệu), sizeof(vịTríDữLiệu));
        if (vịTríDữLiệu.loạiMụcKiểu == 4) {
            if (!đượcChứa(vịTríDữLiệu.giáTrịĐộLệch, vịTríDữLiệu.cỡVùngTệp, cỡ)) return lỗiTệpThựcThiNgườiDùng;
            if (kiểmTraThôngTinPhụTrợ(DữLiệu + vịTríDữLiệu.giáTrịĐộLệch, vịTríDữLiệu.cỡVùngTệp)) ổnABI = 1;
            continue;
        }
        if (vịTríDữLiệu.loạiMụcKiểu == 0 || vịTríDữLiệu.loạiMụcKiểu == 6 || (vịTríDữLiệu.loạiMụcKiểu == 0x6474e551 && !(vịTríDữLiệu.cácBitCấuHình & 1))) continue;
        if (vịTríDữLiệu.loạiMụcKiểu != 1) return lỗiTệpThựcThiNgườiDùng; // PT_INTERP, DYNAMIC, TLS làKhôngHỗTrợ
        if (!vịTríDữLiệu.cỡVùngBộNhớ) continue;
        if (vịTríDữLiệu.cácBitCấuHình & ~7u || !(vịTríDữLiệu.cácBitCấuHình & 4) || (vịTríDữLiệu.cácBitCấuHình & 3) == 3 || vịTríDữLiệu.cỡVùngTệp > vịTríDữLiệu.cỡVùngBộNhớ ||
            (vịTríDữLiệu.cỡVùngTệp && !đượcChứa(vịTríDữLiệu.giáTrịĐộLệch, vịTríDữLiệu.cỡVùngTệp, cỡ)) || vịTríDữLiệu.địaChỉ < cơSởNgườiDùng ||
            !đượcChứa(vịTríDữLiệu.địaChỉ, vịTríDữLiệu.cỡVùngBộNhớ, kếtThúcẢnhNgườiDùng) ||
            (!chếĐộLinux && ((vịTríDữLiệu.địaChỉ & (cỡTrang - 1)) || (vịTríDữLiệu.giáTrịĐộLệch & (cỡTrang - 1)) || vịTríDữLiệu.ranhGiớiCănChỉnh != cỡTrang)) ||
            (chếĐộLinux && (((vịTríDữLiệu.địaChỉ ^ vịTríDữLiệu.giáTrịĐộLệch) & (cỡTrang - 1)) || !vịTríDữLiệu.ranhGiớiCănChỉnh ||
                (vịTríDữLiệu.ranhGiớiCănChỉnh & (vịTríDữLiệu.ranhGiớiCănChỉnh - 1)) || vịTríDữLiệu.ranhGiớiCănChỉnh > 0x200000 || ((vịTríDữLiệu.địaChỉ ^ vịTríDữLiệu.giáTrịĐộLệch) & (vịTríDữLiệu.ranhGiớiCănChỉnh - 1))))) return lỗiTệpThựcThiNgườiDùng;
        unsigned mụcĐầuTiên = (vịTríDữLiệu.địaChỉ - cơSởNgườiDùng) / cỡTrang;
        unsigned sốLượngMục = ((vịTríDữLiệu.địaChỉ & (cỡTrang - 1)) + vịTríDữLiệu.cỡVùngBộNhớ + cỡTrang - 1) / cỡTrang;
        for (unsigned giáTrịTrang = mụcĐầuTiên; giáTrịTrang < mụcĐầuTiên + sốLượngMục; giáTrịTrang++) {
            if (sứcChứaĐãDùng[giáTrịTrang]) return lỗiTệpThựcThiNgườiDùng;
            sứcChứaĐãDùng[giáTrịTrang] = 1;
        }
        if ((vịTríDữLiệu.cácBitCấuHình & 1) && đầuMụcTệpThựcThi.điểmMục >= vịTríDữLiệu.địaChỉ && đầuMụcTệpThựcThi.điểmMục < vịTríDữLiệu.địaChỉ + vịTríDữLiệu.cỡVùngTệp && !(đầuMụcTệpThựcThi.điểmMục & 3)) điểmMụcHợpLệ = 1;
        cácLầnNạp++;
    }
    return điểmMụcHợpLệ && (chếĐộLinux ? !ổnABI : ổnABI) && cácLầnNạp ? 0 : lỗiTệpThựcThiNgườiDùng;
}
int eLFThẩmĐịnhNgườiDùng(const unsigned char *DữLiệu, size_t cỡ) { return thẩmĐịnhELF(DữLiệu, cỡ, 0); }
static void bốTríTrang(uintptr_t địaChỉ, uint64_t cácBitCấuHình, unsigned cácQuyềnTruyCập) {
    unsigned chỉSốTraCứu = (địaChỉ - cơSởNgườiDùng) / cỡTrang;
    danhSáchTrang[chỉSốTraCứu] = địaChỉ | cácBitCấuHình;
    danhSáchCácQuyền[chỉSốTraCứu] = cácQuyềnTruyCập;
}
static int khoảngNgườiDùng(uintptr_t địaChỉ, size_t sốLượngMục, int đangGhi) {
    if (địaChỉ < cơSởNgườiDùng || !đượcChứa(địaChỉ, sốLượngMục, kếtThúcNgườiDùng)) return 0;
    if (!sốLượngMục) return 1;
    unsigned mụcĐầuTiên = (địaChỉ - cơSởNgườiDùng) / cỡTrang, phầnMụcCuối = (địaChỉ + sốLượngMục - 1 - cơSởNgườiDùng) / cỡTrang;
    for (unsigned chỉSốThứBậc = mụcĐầuTiên; chỉSốThứBậc <= phầnMụcCuối; chỉSốThứBậc++) if (!(danhSáchCácQuyền[chỉSốThứBậc] & (đangGhi ? 2 : 1))) return 0;
    return 1;
}
static int saoChépĐườngDẫn(uintptr_t địaChỉ, char *đườngDẫn) {
    for (unsigned chỉSốThứBậc = 0; chỉSốThứBậc < 65; chỉSốThứBậc++) {
        if (!khoảngNgườiDùng(địaChỉ, 1, 0)) return -14;
        đườngDẫn[chỉSốThứBậc] = *(const char *)địaChỉ++;
        if (!đườngDẫn[chỉSốThứBậc]) return 0;
    }
    return -36;
}
static intptr_t kếtQuảNhân(intptr_t kếtQuả) { return kếtQuả < 0 ? -sốLỗi : kếtQuả; }
static int mãTệpĐãÁnhXạ(uint64_t thẻXửLýTệp) { return thẻXửLýTệp >= 3 && thẻXửLýTệp < 19 ? danhSáchTệp[thẻXửLýTệp - 3] : -1; }
static int chủSởHữuĐiểmCuốiỔCắmMạng(uint64_t thẻXửLýTệp) { return thẻXửLýTệp >= 32 && thẻXửLýTệp < 56 && cácĐiểmCuốiỔCắmMạng[thẻXửLýTệp - 32]; }
static int đầuVàoĐịaChỉ(uintptr_t giáTrịViệcTrỏ, size_t độDài, struct pk_sockaddr_in *địaChỉ) {
    if (độDài != sizeof(*địaChỉ)) return -22;
    if (!khoảngNgườiDùng(giáTrịViệcTrỏ, độDài, 0)) return -14;
    memcpy(địaChỉ, (const void *)giáTrịViệcTrỏ, sizeof(*địaChỉ));
    return địaChỉ->sin_family == AF_INET ? 0 : -97;
}
static int kiểmTraĐầuRaĐịaChỉ(uintptr_t giáTrịViệcTrỏ, uintptr_t conTrỏĐộDài, pk_socklen_t *sứcChứaBộĐệm) {
    if (!khoảngNgườiDùng(conTrỏĐộDài, sizeof(*sứcChứaBộĐệm), 1)) return -14;
    memcpy(sứcChứaBộĐệm, (const void *)conTrỏĐộDài, sizeof(*sứcChứaBộĐệm));
    if (*sứcChứaBộĐệm > sizeof(struct pk_sockaddr_in)) *sứcChứaBộĐệm = sizeof(struct pk_sockaddr_in);
    if (*sứcChứaBộĐệm && !khoảngNgườiDùng(giáTrịViệcTrỏ, *sứcChứaBộĐệm, 1)) return -14;
    return 0;
}
static void đầuRaĐịaChỉ(uintptr_t giáTrịViệcTrỏ, uintptr_t conTrỏĐộDài, pk_socklen_t sứcChứaBộĐệm, int địaChỉ, int sốCổng) {
    struct pk_sockaddr_in giáTrị; memset(&giáTrị, 0, sizeof(giáTrị));
    giáTrị.sin_family = AF_INET; giáTrị.sin_port = pk_htons(sốCổng); giáTrị.sin_addr.s_addr = pk_htonl(địaChỉ);
    if (sứcChứaBộĐệm) memcpy((void *)giáTrịViệcTrỏ, &giáTrị, sứcChứaBộĐệm);
    pk_socklen_t độDài = sizeof(giáTrị); memcpy((void *)conTrỏĐộDài, &độDài, sizeof(độDài));
}
extern uintptr_t kênhBoMạch(uintptr_t, uintptr_t);
static intptr_t gọiHệThốngBảnĐịa(khungNgườiDùng *mụcTệp) {
    uintptr_t giáTrịĐầuTiên = mụcTệp->thanhGhiDữLiệu[0], giáTrịThứHai = mụcTệp->thanhGhiDữLiệu[1], mãKýTự = mụcTệp->thanhGhiDữLiệu[2];
    char đườngDẫn[65];
    int thẻXửLýTệp, kếtQuả;
    switch (mụcTệp->thanhGhiDữLiệu[8]) {
    case 0: return 1; // tựThân ABI 버전
    case 1: // write: conTrỏ 전체를 검사한 giáTrịLùi ĐầuRa/Tệp đổiGiáTrị
        if (mãKýTự > 65536) return -22;
        if (!khoảngNgườiDùng(giáTrịThứHai, mãKýTự, 0)) return -14;
        if (giáTrịĐầuTiên == 1 || giáTrịĐầuTiên == 2) {
            uint64_t bắtChạyĐầuRa=giáTrịĐồngHồ();
            for (size_t chỉSốThứBậc = 0; chỉSốThứBậc < mãKýTự; chỉSốThứBậc++) kênhBoMạch(giáTrịĐầuTiên, ((const unsigned char *)giáTrịThứHai)[chỉSốThứBậc]);
            /* 큰 tty를 그린 giáTrịNhân 시간만 돌려준다. EL0 phépTính 기한은 늘리지 않는다. */
            if(tươngTác){
                thờiGianHạnChót+=giáTrịĐồngHồ()-bắtChạyĐầuRa;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(thờiGianHạnChót) : "memory");
            }
            return mãKýTự;
        }
        if(giáTrịĐầuTiên>=40&&chủSởHữuĐiểmCuốiỔCắmMạng(giáTrịĐầuTiên)){
            size_t sốLượngPhầnMục=mãKýTự>512?512:mãKýTự;for(size_t chỉSốThứBậc=0;chỉSốThứBậc<sốLượngPhầnMục;chỉSốThứBậc++)đặtMạngJava(chỉSốThứBậc,((const unsigned char *)giáTrịThứHai)[chỉSốThứBậc]);return ghiLuồngJava(giáTrịĐầuTiên,sốLượngPhầnMục);
        }
        thẻXửLýTệp = mãTệpĐãÁnhXạ(giáTrịĐầuTiên); if (thẻXửLýTệp < 0) return -9;
        return kếtQuảNhân(pk_write(thẻXửLýTệp, (const void *)giáTrịThứHai, mãKýTự));
    case 2:
        if (mãKýTự > 65536) return -22;
        if (!khoảngNgườiDùng(giáTrịThứHai, mãKýTự, 1)) return -14;
        if (giáTrịĐầuTiên == 0) {
            size_t sốLượngPhầnMục = 0;
            while (sốLượngPhầnMục < mãKýTự) {
                int giáTrịKýTự = (int32_t)lấyKýTựBoMạch(); if (giáTrịKýTự == -2) return sốLượngPhầnMục; if (giáTrịKýTự < 0) break;
                ((unsigned char *)giáTrịThứHai)[sốLượngPhầnMục++] = giáTrịKýTự;
            }
            return sốLượngPhầnMục ? (intptr_t)sốLượngPhầnMục : (mãKýTự ? -11 : 0);
        }
        if(giáTrịĐầuTiên>=40&&chủSởHữuĐiểmCuốiỔCắmMạng(giáTrịĐầuTiên)){
            kếtQuả=đọcLuồngJava(giáTrịĐầuTiên,mãKýTự>512?512:mãKýTự);if(kếtQuả>0)for(int chỉSốThứBậc=0;chỉSốThứBậc<kếtQuả;chỉSốThứBậc++)((unsigned char *)giáTrịThứHai)[chỉSốThứBậc]=lấyMạngJava(chỉSốThứBậc);return kếtQuả;
        }
        thẻXửLýTệp = mãTệpĐãÁnhXạ(giáTrịĐầuTiên); if (thẻXửLýTệp < 0) return -9;
        return kếtQuảNhân(pk_read(thẻXửLýTệp, (void *)giáTrịThứHai, mãKýTự));
    case 3:
        kếtQuả = saoChépĐườngDẫn(giáTrịĐầuTiên, đườngDẫn); if (kếtQuả) return kếtQuả;
        if (giáTrịThứHai > 0x7ff) return -22;
        for (unsigned chỉSốThứBậc = 0; chỉSốThứBậc < 16; chỉSốThứBậc++) if (danhSáchTệp[chỉSốThứBậc] < 0) {
            thẻXửLýTệp = pk_open(đườngDẫn, (int)giáTrịThứHai, 0600);
            if (thẻXửLýTệp < 0) return -sốLỗi;
            danhSáchTệp[chỉSốThứBậc] = thẻXửLýTệp; return chỉSốThứBậc + 3;
        }
        return -24;
    case 4:
        if (chủSởHữuĐiểmCuốiỔCắmMạng(giáTrịĐầuTiên)) { kếtQuả = đóngĐiểmCuốiỔCắmMạng(giáTrịĐầuTiên); if (!kếtQuả) cácĐiểmCuốiỔCắmMạng[giáTrịĐầuTiên - 32] = 0; return kếtQuả; }
        thẻXửLýTệp = mãTệpĐãÁnhXạ(giáTrịĐầuTiên); if (thẻXửLýTệp < 0) return -9;
        kếtQuả = pk_close(thẻXửLýTệp); if (!kếtQuả) danhSáchTệp[giáTrịĐầuTiên - 3] = -1;
        return kếtQuảNhân(kếtQuả);
    case 5:
        thẻXửLýTệp = mãTệpĐãÁnhXạ(giáTrịĐầuTiên); if (thẻXửLýTệp < 0) return -9;
        if (mãKýTự > 2) return -22;
        return kếtQuảNhân(pk_lseek(thẻXửLýTệp, (int64_t)giáTrịThứHai, mãKýTự));
    case 7: return miliGiâyGọnBoMạch();
    case 8: { // brk: 별도 NgườiDùng RW/NX giáTrịVùngNhớĐộng, 새로 노출되는 페이지는 0으로 khởiTạo
        if (!giáTrịĐầuTiên) return kếtThúcVùngNhớĐộng;
        if (giáTrịĐầuTiên < kếtThúcẢnhNgườiDùng || giáTrịĐầuTiên > kếtThúcVùngNhớĐộngNgườiDùng) return -12;
        uintptr_t cácTrangCũ = (kếtThúcVùngNhớĐộng + cỡTrang - 1) & ~(cỡTrang - 1);
        uintptr_t cácTrangMới = (giáTrịĐầuTiên + cỡTrang - 1) & ~(cỡTrang - 1);
        if (cácTrangMới > cácTrangCũ) {
            for (uintptr_t vịTríDữLiệu = cácTrangCũ; vịTríDữLiệu < cácTrangMới; vịTríDữLiệu += cỡTrang) bốTríTrang(vịTríDữLiệu, trangNhân, 0);
            cácBảngTraĐồngBộ();
            memset((void *)cácTrangCũ, 0, cácTrangMới - cácTrangCũ);
            for (uintptr_t vịTríDữLiệu = cácTrangCũ; vịTríDữLiệu < cácTrangMới; vịTríDữLiệu += cỡTrang) bốTríTrang(vịTríDữLiệu, ghiĐọcNgườiDùng, 3);
        } else {
            for (uintptr_t vịTríDữLiệu = cácTrangMới; vịTríDữLiệu < cácTrangCũ; vịTríDữLiệu += cỡTrang) {
                danhSáchTrang[(vịTríDữLiệu - cơSởNgườiDùng) / cỡTrang] = 0; danhSáchCácQuyền[(vịTríDữLiệu - cơSởNgườiDùng) / cỡTrang] = 0;
            }
        }
        kếtThúcVùngNhớĐộng = giáTrịĐầuTiên; cácBảngTraĐồngBộ(); return giáTrịĐầuTiên;
    }
    case 9:
        thẻXửLýTệp = mãTệpĐãÁnhXạ(giáTrịĐầuTiên); return thẻXửLýTệp < 0 ? -9 : kếtQuảNhân(pk_size(thẻXửLýTệp));
    case 10:
        thẻXửLýTệp = mãTệpĐãÁnhXạ(giáTrịĐầuTiên); return thẻXửLýTệp < 0 ? -9 : kếtQuảNhân(pk_ftruncate(thẻXửLýTệp, (int64_t)giáTrịThứHai));
    case 11:
        kếtQuả = saoChépĐườngDẫn(giáTrịĐầuTiên, đườngDẫn); return kếtQuả ? kếtQuả : kếtQuảNhân(pk_unlink(đườngDẫn));
    case 12:
        thẻXửLýTệp = mãTệpĐãÁnhXạ(giáTrịĐầuTiên); return thẻXửLýTệp < 0 ? -9 : kếtQuảNhân(pk_fsync(thẻXửLýTệp));
    case 13: { // 그래픽 기초 API: NgườiDùng 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t giáTrịRộngĐãYêuCầu = mụcTệp->thanhGhiDữLiệu[3], giáTrịCaoĐãYêuCầu = mụcTệp->thanhGhiDữLiệu[4];
        if (!bộĐệmKhungBoMạch()) return -19;
        uintptr_t khoảngTrảiMànHình = rộngMànHìnhBoMạch(), độDàiMànHình = caoMànHìnhBoMạch();
        if (giáTrịĐầuTiên > khoảngTrảiMànHình || giáTrịThứHai > độDàiMànHình || giáTrịRộngĐãYêuCầu > khoảngTrảiMànHình - giáTrịĐầuTiên || giáTrịCaoĐãYêuCầu > độDàiMànHình - giáTrịThứHai) return -22;
        for (uintptr_t tọaĐộY = giáTrịThứHai; tọaĐộY < giáTrịThứHai + giáTrịCaoĐãYêuCầu; tọaĐộY++) for (uintptr_t tọaĐộX = giáTrịĐầuTiên; tọaĐộX < giáTrịĐầuTiên + giáTrịRộngĐãYêuCầu; tọaĐộX++) điểmẢnhBoMạch(tọaĐộX, tọaĐộY, mãKýTự);
        return 0;
    }
    case 14: return (int32_t)lấyKýTựBoMạch();
    case 15: // args(-1,0,0)=sốLượngPhầnMục; args(index,buffer,capacity)=UTF-8 độDài
        if (giáTrịĐầuTiên == UINTPTR_MAX) return sốLượngĐốiSốĐãChuyểnTiếp;
        if (giáTrịĐầuTiên >= sốLượngĐốiSốĐãChuyểnTiếp) return -22;
        if (mãKýTự <= độDàiĐốiSốĐãChuyểnTiếp[giáTrịĐầuTiên]) return -36;
        if (!khoảngNgườiDùng(giáTrịThứHai, độDàiĐốiSốĐãChuyểnTiếp[giáTrịĐầuTiên] + 1, 1)) return -14;
        memcpy((void *)giáTrịThứHai, đốiSốĐãChuyểnTiếp[giáTrịĐầuTiên], độDàiĐốiSốĐãChuyểnTiếp[giáTrịĐầuTiên] + 1);
        return độDàiĐốiSốĐãChuyểnTiếp[giáTrịĐầuTiên];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(giáTrịĐầuTiên==0){if(!tươngTácVỏLệnhJava())return -95;tươngTác=1;return thiếtBịCuốiBoMạch(13);}
        if(giáTrịĐầuTiên==2){tươngTác=0;return 0;}
        if(giáTrịĐầuTiên==3)return thiếtBịCuốiBoMạch(13);
        if(giáTrịĐầuTiên!=1||!tươngTác)return -22;
        kếtQuả=(int32_t)lấyKýTựBoMạch();
        if(kếtQuả==-4096)return kếtQuả;
        bắtChạyHếtGiờ();return kếtQuả<0?-11:kếtQuả;
    case 17: { // 유한한 협력 chờGiáTrị: TruyềnThông 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (giáTrịĐầuTiên > 100) return -22;
        uint64_t thờiGianKếtThúc = giáTrịĐồngHồ() + tầnSố * giáTrịĐầuTiên / 1000;
        do { xemXétMạng(); xemXétChuyểnGiaoTệp(); __asm__ volatile("yield"); } while (giáTrịĐồngHồ() < thờiGianKếtThúc);
        bắtChạyHếtGiờ(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 giáTrịCha·빈 폴더를 검사한다.
        if (giáTrịThứHai > 2) return -22;
        kếtQuả = saoChépĐườngDẫn(giáTrịĐầuTiên, đườngDẫn); if (kếtQuả) return kếtQuả;
        unsigned độDài = 0; while (đườngDẫn[độDài]) độDài++;
        kếtQuả = bắtChạyĐườngDẫnJava(độDài); if (kếtQuả < 0) return kếtQuả;
        for (unsigned chỉSốThứBậc = 0; chỉSốThứBậc < độDài; chỉSốThứBậc++) byteĐườngDẫnJava(chỉSốThứBậc, (unsigned char)đườngDẫn[chỉSốThứBậc]);
        return giáTrịThứHai == 0 ? loạiMụcJava() : giáTrịThứHai == 1 ? thưMụcTạoJava() : thưMụcGỡJava();
    }
    case 20:
        if(giáTrịĐầuTiên==5){int giáTrịKýTự=(int32_t)lấyKýTựBoMạch();if(giáTrịKýTự==-4096)return giáTrịKýTự;if(giáTrịKýTự>=0)nhấnMànHình(đốiTượngChủSởHữu,giáTrịKýTự);bắtChạyHếtGiờ();}
        if(giáTrịĐầuTiên==3&&mãKýTự){if(!tươngTácVỏLệnhJava())return -95;tươngTác=1;thiếtBịCuốiBoMạch(300);}
        return gọiThựcHiệnMànHình(đốiTượngChủSởHữu,giáTrịĐầuTiên,giáTrịThứHai,mãKýTự,mụcTệp->thanhGhiDữLiệu[3],mụcTệp->thanhGhiDữLiệu[4],mụcTệp->thanhGhiDữLiệu[5]);
    case 21:
        if(mãKýTự>127)return -22;if(!khoảngNgườiDùng(giáTrịThứHai,mãKýTự*sizeof(uint32_t),0))return -14;
        return vănBảnMànHình(đốiTượngChủSởHữu,giáTrịĐầuTiên,(const uint32_t *)giáTrịThứHai,mãKýTự);
    case 22: // MànHình cỡ giáTrịTruyVấn: 0=giáTrịRộng, 1=giáTrịCao. 사용자에게 주소를 노출하지 않는다.
        if (giáTrịĐầuTiên > 1) return -22;
        if (!bộĐệmKhungBoMạch()) return -19;
        return giáTrịĐầuTiên == 0 ? rộngMànHìnhBoMạch() : caoMànHìnhBoMạch();
    case 32:
        if (giáTrịĐầuTiên != AF_INET) return -97;
        if(giáTrịThứHai==SOCK_STREAM&&(mãKýTự==0||mãKýTự==6))kếtQuả=tạoLuồngJava();
        else if(giáTrịThứHai==SOCK_DGRAM&&(mãKýTự==0||mãKýTự==IPPROTO_UDP))kếtQuả=ổCắmMạngMạngJava(giáTrịĐầuTiên,giáTrịThứHai,mãKýTự);
        else return -93;
        if (kếtQuả >= 32 && kếtQuả < 56) cácĐiểmCuốiỔCắmMạng[kếtQuả - 32] = 1;
        return kếtQuả;
    case 33: {
        if (!chủSởHữuĐiểmCuốiỔCắmMạng(giáTrịĐầuTiên)) return -9;
        struct pk_sockaddr_in địaChỉ;
        kếtQuả = đầuVàoĐịaChỉ(giáTrịThứHai, mãKýTự, &địaChỉ); if (kếtQuả) return kếtQuả;
        return giáTrịĐầuTiên>=40?ràngBuộcLuồngJava(giáTrịĐầuTiên,pk_htonl(địaChỉ.sin_addr.s_addr),pk_htons(địaChỉ.sin_port)):ràngBuộcMạngJava(giáTrịĐầuTiên, pk_htonl(địaChỉ.sin_addr.s_addr), pk_htons(địaChỉ.sin_port));
    }
    case 34: {
        if (!chủSởHữuĐiểmCuốiỔCắmMạng(giáTrịĐầuTiên)) return -9;
        if(giáTrịĐầuTiên>=40)return -95;
        if (mụcTệp->thanhGhiDữLiệu[3]) return -95;
        if (mãKýTự > 512) return -90;
        if (mãKýTự && !khoảngNgườiDùng(giáTrịThứHai, mãKýTự, 0)) return -14;
        struct pk_sockaddr_in địaChỉ;
        kếtQuả = đầuVàoĐịaChỉ(mụcTệp->thanhGhiDữLiệu[4], mụcTệp->thanhGhiDữLiệu[5], &địaChỉ); if (kếtQuả) return kếtQuả;
        for (unsigned chỉSốThứBậc = 0; chỉSốThứBậc < mãKýTự; chỉSốThứBậc++) đặtMạngJava(chỉSốThứBậc, ((const unsigned char *)giáTrịThứHai)[chỉSốThứBậc]);
        return gửiMạngJava(giáTrịĐầuTiên, pk_htonl(địaChỉ.sin_addr.s_addr), pk_htons(địaChỉ.sin_port), mãKýTự);
    }
    case 35: {
        if (!chủSởHữuĐiểmCuốiỔCắmMạng(giáTrịĐầuTiên)) return -9;
        if(giáTrịĐầuTiên>=40)return -95;
        if (mụcTệp->thanhGhiDữLiệu[3]) return -95;
        if (mãKýTự > 512) return -90;
        if (mãKýTự && !khoảngNgườiDùng(giáTrịThứHai, mãKýTự, 1)) return -14;
        pk_socklen_t sứcChứaBộĐệm = 0;
        if (mụcTệp->thanhGhiDữLiệu[4]) { kếtQuả = kiểmTraĐầuRaĐịaChỉ(mụcTệp->thanhGhiDữLiệu[4], mụcTệp->thanhGhiDữLiệu[5], &sứcChứaBộĐệm); if (kếtQuả) return kếtQuả; }
        kếtQuả = nhậnGọnMạngJava(giáTrịĐầuTiên, mãKýTự); if (kếtQuả < 0) return kếtQuả;
        for (int chỉSốThứBậc = 0; chỉSốThứBậc < kếtQuả; chỉSốThứBậc++) ((unsigned char *)giáTrịThứHai)[chỉSốThứBậc] = lấyMạngJava(chỉSốThứBậc);
        if (mụcTệp->thanhGhiDữLiệu[4]) đầuRaĐịaChỉ(mụcTệp->thanhGhiDữLiệu[4], mụcTệp->thanhGhiDữLiệu[5], sứcChứaBộĐệm, từXaMạngJava(giáTrịĐầuTiên), đốiTácMạngJava(giáTrịĐầuTiên));
        return kếtQuả;
    }
    case 36: {
        if (!chủSởHữuĐiểmCuốiỔCắmMạng(giáTrịĐầuTiên)) return -9;
        pk_socklen_t sứcChứaBộĐệm;
        kếtQuả = kiểmTraĐầuRaĐịaChỉ(giáTrịThứHai, mãKýTự, &sứcChứaBộĐệm); if (kếtQuả) return kếtQuả;
        đầuRaĐịaChỉ(giáTrịThứHai,mãKýTự,sứcChứaBộĐệm,giáTrịĐầuTiên>=40?địaChỉLuồngJava(giáTrịĐầuTiên):địaChỉMạngJava(giáTrịĐầuTiên),giáTrịĐầuTiên>=40?cổngLuồngJava(giáTrịĐầuTiên):cổngMạngJava(giáTrịĐầuTiên)); return 0;
    }
    case 37: {
        if(giáTrịĐầuTiên<40||!chủSởHữuĐiểmCuốiỔCắmMạng(giáTrịĐầuTiên))return -9;struct pk_sockaddr_in địaChỉ;
        kếtQuả=đầuVàoĐịaChỉ(giáTrịThứHai,mãKýTự,&địaChỉ);if(kếtQuả)return kếtQuả;
        return kếtNốiLuồngJava(giáTrịĐầuTiên,pk_htonl(địaChỉ.sin_addr.s_addr),pk_htons(địaChỉ.sin_port));
    }
    case 38: return giáTrịĐầuTiên>=40&&chủSởHữuĐiểmCuốiỔCắmMạng(giáTrịĐầuTiên)?lắngNgheLuồngJava(giáTrịĐầuTiên,giáTrịThứHai):-9;
    case 39:
        if(giáTrịĐầuTiên<40||!chủSởHữuĐiểmCuốiỔCắmMạng(giáTrịĐầuTiên))return -9;
        if(giáTrịThứHai||mãKýTự)return -95;kếtQuả=chấpNhậnLuồngJava(giáTrịĐầuTiên);if(kếtQuả>=40&&kếtQuả<56)cácĐiểmCuốiỔCắmMạng[kếtQuả-32]=1;return kếtQuả;
    case 40: return giáTrịĐầuTiên>=40&&chủSởHữuĐiểmCuốiỔCắmMạng(giáTrịĐầuTiên)?đốiTácLuồngJava(giáTrịĐầuTiên):-9;
    default: return -38; // làKhôngHỗTrợ 기능을 성공으로 가장하지 않음
    }
}
#include "tươngThíchLinux.inc"
static intptr_t LờiGọiHệThống(khungNgườiDùng *mụcTệp) {
    network_poll();
    return aBILinux ? gọiHệThốngLinux(mụcTệp) : gọiHệThốngBảnĐịa(mụcTệp);
}
static void nhânTrảVề(khungNgườiDùng *mụcTệp, int kếtQuả) {
    dừngHếtGiờ();
    mụcTệp->thanhGhiDữLiệu[0] = (uint64_t)(int64_t)kếtQuả;
    mụcTệp->vịTríLệnh = (uintptr_t)trảVềNgườiDùng;
    mụcTệp->mãTrạngThái = 0x3c5; // EL1h, DAIF masked
}
int ngoạiLệNgườiDùng(khungNgườiDùng *mụcTệp, unsigned chặnBắt) {
    if (!hoạtĐộng || (mụcTệp->mãTrạngThái & 15) != 0) return 0;
    if (chặnBắt) {
        uint32_t giáTrịXácNhậnNhận = thanhGhiMáy(giaoDiệnCPUNgắtXửLý + 0xc), giáTrịĐịnhDanh = giáTrịXácNhậnNhận & 1023;
        if (giáTrịĐịnhDanh == 30) { nhânTrảVề(mụcTệp, hếtGiờNgườiDùng); thanhGhiMáy(giaoDiệnCPUNgắtXửLý + 0x10) = giáTrịXácNhậnNhận; return 1; }
        if (giáTrịĐịnhDanh < 1020) thanhGhiMáy(giaoDiệnCPUNgắtXửLý + 0x10) = giáTrịXácNhậnNhận;
        return 1;
    }
    uint64_t trạngTháiNgoạiLệ; __asm__ volatile("mrs %0, esr_el1" : "=r"(trạngTháiNgoạiLệ));
    if (giáTrịĐồngHồ() >= thờiGianHạnChót) { nhânTrảVề(mụcTệp, hếtGiờNgườiDùng); return 1; }
    unsigned loạiMụcNgoạiLệ = trạngTháiNgoạiLệ >> 26;
    if (loạiMụcNgoạiLệ == 0x15 && (trạngTháiNgoạiLệ & 0xffff) == 0) {
        if (aBILinux ? mụcTệp->thanhGhiDữLiệu[8] == 93 || mụcTệp->thanhGhiDữLiệu[8] == 94 : mụcTệp->thanhGhiDữLiệu[8] == 6) nhânTrảVề(mụcTệp, (int)(mụcTệp->thanhGhiDữLiệu[0] & 255));
        else {
            intptr_t kếtQuả=LờiGọiHệThống(mụcTệp);
            if(kếtQuả==-4096&&tươngTác){
                đãLưu[đốiTượngChủSởHữu].khungViệcThựcThi=*mụcTệp;đãLưu[đốiTượngChủSởHữu].khungViệcThựcThi.vịTríLệnh-=4;
                lưuDấuPhẩyĐộngGọnNgườiDùng(đãLưu[đốiTượngChủSởHữu].trạngTháiĐiểmDấuPhẩyĐộng);nhânTrảVề(mụcTệp,đãBịNgắtNgườiDùng);
            }else mụcTệp->thanhGhiDữLiệu[0]=(uint64_t)kếtQuả;
        }
    } else nhânTrảVề(mụcTệp, loạiMụcNgoạiLệ == 0x24 ? lỗiDữLiệuNgườiDùng : loạiMụcNgoạiLệ == 0x20 ? lỗiViệcThựcThiNgườiDùng : chỉLệnhKhôngHợpLệNgườiDùng);
    return 1;
}

// 생성된 const ELF giáTrịNhóm: 실행은 반드시 ChươngTrình 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *DữLiệu; size_t cỡ; unsigned giáTrịĐãChuyểnTiếp; } chươngTrình;
#include "programs.h"
static void *bảnChụp(unsigned chỉSốVịTrí){return (void *)(0x04000000ul+chỉSốVịTrí*(kếtThúcNgườiDùng-cơSởNgườiDùng));}
static int hoànThànhChươngTrình(int kếtQuả){
    thờiGianTíchLũyNgườiDùng[đốiTượngChủSởHữu]+=(uint32_t)miliGiâyGọnBoMạch()-thờiGianViệcThựcThiNgườiDùng[đốiTượngChủSởHữu];
    dừngHếtGiờ();hoạtĐộng=0;
    if(kếtQuả==đãBịNgắtNgườiDùng){
        tiếnTrìnhĐãLưu *dữLiệuChuỗi=&đãLưu[đốiTượngChủSởHữu];dữLiệuChuỗi->trạngTháiĐãTạmDừng=1;dữLiệuChuỗi->tươngTác=tươngTác;dữLiệuChuỗi->aBILinux=aBILinux;dữLiệuChuỗi->lưuTrữVùngNhớĐộng=kếtThúcVùngNhớĐộng;dữLiệuChuỗi->sốLượngCácĐốiSố=sốLượngĐốiSốĐãChuyểnTiếp;
        memcpy(dữLiệuChuỗi->danhSáchCácQuyền,danhSáchCácQuyền,sizeof(danhSáchCácQuyền));memcpy(dữLiệuChuỗi->danhSáchTệp,danhSáchTệp,sizeof(danhSáchTệp));memcpy(dữLiệuChuỗi->cácĐiểmCuốiỔCắmMạng,cácĐiểmCuốiỔCắmMạng,sizeof(cácĐiểmCuốiỔCắmMạng));
        memcpy(dữLiệuChuỗi->mảngĐốiSố,đốiSốĐãChuyểnTiếp,sizeof(đốiSốĐãChuyểnTiếp));memcpy(dữLiệuChuỗi->độDàiĐốiSố,độDàiĐốiSốĐãChuyểnTiếp,sizeof(độDàiĐốiSốĐãChuyểnTiếp));
        for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<sốLượngTrangNgườiDùng;chỉSốThứBậc++)if(danhSáchCácQuyền[chỉSốThứBậc])memcpy((unsigned char *)bảnChụp(đốiTượngChủSởHữu)+chỉSốThứBậc*cỡTrang,(void *)(cơSởNgườiDùng+chỉSốThứBậc*cỡTrang),cỡTrang);
    }else{
        đãLưu[đốiTượngChủSởHữu].trạngTháiĐãTạmDừng=0;khởiTạoMànHình(đốiTượngChủSởHữu);
        for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<16;chỉSốThứBậc++)if(danhSáchTệp[chỉSốThứBậc]>=0)pk_close(danhSáchTệp[chỉSốThứBậc]);
        for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<24;chỉSốThứBậc++)if(cácĐiểmCuốiỔCắmMạng[chỉSốThứBậc])đóngĐiểmCuốiỔCắmMạng(chỉSốThứBậc+32);
    }
    for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<sốLượngTrangNgườiDùng;chỉSốThứBậc++){danhSáchTrang[chỉSốThứBậc]=0;danhSáchCácQuyền[chỉSốThứBậc]=0;}cácBảngTraĐồngBộ();return kếtQuả;
}
uintptr_t điềuKhiểnNgườiDùngBoMạch(uintptr_t hànhĐộng){
    unsigned chỉSốVịTrí=hànhĐộng&15;if(chỉSốVịTrí>=4||hoạtĐộng)return (uint32_t)-22;
    tiếnTrìnhĐãLưu *dữLiệuChuỗi=&đãLưu[chỉSốVịTrí];
    if(hànhĐộng>=32){if(dữLiệuChuỗi->trạngTháiĐãTạmDừng){for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<16;chỉSốThứBậc++)if(dữLiệuChuỗi->danhSáchTệp[chỉSốThứBậc]>=0)pk_close(dữLiệuChuỗi->danhSáchTệp[chỉSốThứBậc]);for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<24;chỉSốThứBậc++)if(dữLiệuChuỗi->cácĐiểmCuốiỔCắmMạng[chỉSốThứBậc])đóngĐiểmCuốiỔCắmMạng(chỉSốThứBậc+32);}dữLiệuChuỗi->trạngTháiĐãTạmDừng=0;khởiTạoMànHình(chỉSốVịTrí);return 0;}
    if(hànhĐộng>=16)return dữLiệuChuỗi->trạngTháiĐãTạmDừng;
    if(!dữLiệuChuỗi->trạngTháiĐãTạmDừng)return (uint32_t)-22;
    đốiTượngChủSởHữu=chỉSốVịTrí;tươngTác=dữLiệuChuỗi->tươngTác;aBILinux=dữLiệuChuỗi->aBILinux;kếtThúcVùngNhớĐộng=dữLiệuChuỗi->lưuTrữVùngNhớĐộng;sốLượngĐốiSốĐãChuyểnTiếp=dữLiệuChuỗi->sốLượngCácĐốiSố;
    memcpy(danhSáchTệp,dữLiệuChuỗi->danhSáchTệp,sizeof(danhSáchTệp));memcpy(cácĐiểmCuốiỔCắmMạng,dữLiệuChuỗi->cácĐiểmCuốiỔCắmMạng,sizeof(cácĐiểmCuốiỔCắmMạng));memcpy(đốiSốĐãChuyểnTiếp,dữLiệuChuỗi->mảngĐốiSố,sizeof(đốiSốĐãChuyểnTiếp));memcpy(độDàiĐốiSốĐãChuyểnTiếp,dữLiệuChuỗi->độDàiĐốiSố,sizeof(độDàiĐốiSốĐãChuyểnTiếp));
    for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<sốLượngTrangNgườiDùng;chỉSốThứBậc++)danhSáchTrang[chỉSốThứBậc]=(cơSởNgườiDùng+chỉSốThứBậc*cỡTrang)|trangNhân;cácBảngTraĐồngBộ();
    memset((void *)cơSởNgườiDùng,0,kếtThúcNgườiDùng-cơSởNgườiDùng);
    for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<sốLượngTrangNgườiDùng;chỉSốThứBậc++)if(dữLiệuChuỗi->danhSáchCácQuyền[chỉSốThứBậc])memcpy((void *)(cơSởNgườiDùng+chỉSốThứBậc*cỡTrang),(unsigned char *)bảnChụp(chỉSốVịTrí)+chỉSốThứBậc*cỡTrang,cỡTrang);
    memcpy(danhSáchCácQuyền,dữLiệuChuỗi->danhSáchCácQuyền,sizeof(danhSáchCácQuyền));
    for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<sốLượngTrangNgườiDùng;chỉSốThứBậc++){unsigned vịTríDữLiệu=danhSáchCácQuyền[chỉSốThứBậc];danhSáchTrang[chỉSốThứBậc]=vịTríDữLiệu?(cơSởNgườiDùng+chỉSốThứBậc*cỡTrang)|(vịTríDữLiệu==3?ghiĐọcNgườiDùng:vịTríDữLiệu==5?thựcThiĐọcNgườiDùng:chỉĐọcNgườiDùng):0;}
    cácBảngTraĐồngBộ();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");hoạtĐộng=1;dữLiệuChuỗi->trạngTháiĐãTạmDừng=0;bắtChạyHếtGiờ();
    thờiGianViệcThựcThiNgườiDùng[đốiTượngChủSởHữu]=miliGiâyGọnBoMạch();
    return (uint32_t)hoànThànhChươngTrình(tiếpDiễnNgườiDùng(&dữLiệuChuỗi->khungViệcThựcThi,dữLiệuChuỗi->trạngTháiĐiểmDấuPhẩyĐộng));
}
static int chạyChươngTrình(const unsigned char *DữLiệu, size_t cỡ, unsigned giáTrịĐãChuyểnTiếp, int chếĐộLinux, const char *tên) {
    if (hoạtĐộng) return -16;
    đốiTượngChủSởHữu=thiếtBịCuốiBoMạch(11);if(đốiTượngChủSởHữu<0||đốiTượngChủSởHữu>3||đãLưu[đốiTượngChủSởHữu].trạngTháiĐãTạmDừng)return -16;tươngTác=0;
    int hợpLệ = thẩmĐịnhELF(DữLiệu, cỡ, chếĐộLinux); if (hợpLệ) return hợpLệ;
    aBILinux = chếĐộLinux;
    unsigned chỉSốTên=0;
    while (*tên && chỉSốTên<31) tênLệnhNgườiDùng[đốiTượngChủSởHữu][chỉSốTên++]=(unsigned char)*tên++;
    if (sốLượngĐốiSốĐãChuyểnTiếp && độDàiĐốiSốĐãChuyểnTiếp[0]) {
        if (chỉSốTên) tênLệnhNgườiDùng[đốiTượngChủSởHữu][chỉSốTên++]=' ';
        for (unsigned chỉSốVịTrí=0; chỉSốVịTrí<độDàiĐốiSốĐãChuyểnTiếp[0]; chỉSốVịTrí++) tênLệnhNgườiDùng[đốiTượngChủSởHữu][chỉSốTên++]=đốiSốĐãChuyểnTiếp[0][chỉSốVịTrí];
    }
    tênLệnhNgườiDùng[đốiTượngChủSởHữu][chỉSốTên]=0; sốNgườiDùng[đốiTượngChủSởHữu]=sốNgườiDùngKếTiếp++;
    if (sốNgườiDùngKếTiếp>0x7fffffffu) sốNgườiDùngKếTiếp=10;
    thờiGianBắtChạyNgườiDùng[đốiTượngChủSởHữu]=miliGiâyGọnBoMạch(); thờiGianTíchLũyNgườiDùng[đốiTượngChủSởHữu]=0;
    for (unsigned chỉSốThứBậc = 0; chỉSốThứBậc < sốLượngTrangNgườiDùng; chỉSốThứBậc++) danhSáchTrang[chỉSốThứBậc] = (cơSởNgườiDùng + chỉSốThứBậc * cỡTrang) | trangNhân;
    cácBảngTraĐồngBộ();
    memset((void *)cơSởNgườiDùng, 0, kếtThúcNgườiDùng - cơSởNgườiDùng);
    memset(danhSáchCácQuyền, 0, sizeof(danhSáchCácQuyền));
    đầuMụcELF đầuMụcTệpThựcThi; memcpy(&đầuMụcTệpThựcThi, DữLiệu, sizeof(đầuMụcTệpThựcThi));
    for (unsigned chỉSốThứBậc = 0; chỉSốThứBậc < đầuMụcTệpThựcThi.sốLượngĐầuMụcChươngTrình; chỉSốThứBậc++) {
        chươngTrìnhELF vịTríDữLiệu; memcpy(&vịTríDữLiệu, DữLiệu + đầuMụcTệpThựcThi.độLệchĐầuMụcChươngTrình + chỉSốThứBậc * sizeof(vịTríDữLiệu), sizeof(vịTríDữLiệu));
        if (vịTríDữLiệu.loạiMụcKiểu != 1 || !vịTríDữLiệu.cỡVùngBộNhớ) continue;
        if (vịTríDữLiệu.cỡVùngTệp) memcpy((void *)(uintptr_t)vịTríDữLiệu.địaChỉ, DữLiệu + vịTríDữLiệu.giáTrịĐộLệch, vịTríDữLiệu.cỡVùngTệp);
        for (uintptr_t vịTríHiệnTại = vịTríDữLiệu.địaChỉ & ~(cỡTrang - 1); vịTríHiệnTại < vịTríDữLiệu.địaChỉ + vịTríDữLiệu.cỡVùngBộNhớ; vịTríHiệnTại += cỡTrang) {
            danhSáchCácQuyền[(vịTríHiệnTại - cơSởNgườiDùng) / cỡTrang] = (vịTríDữLiệu.cácBitCấuHình & 2) ? 3 : ((vịTríDữLiệu.cácBitCấuHình & 1) ? 5 : 1);
        }
    }
    for (uintptr_t vịTríHiệnTại = địaChỉNgănXếpNgườiDùng; vịTríHiệnTại < kếtThúcNgườiDùng; vịTríHiệnTại += cỡTrang) danhSáchCácQuyền[(vịTríHiệnTại - cơSởNgườiDùng) / cỡTrang] = 3;
    uintptr_t ngănXếpBanĐầu = chếĐộLinux ? ngănXếpBắtChạyLinux(đầuMụcTệpThựcThi.điểmMục) : kếtThúcNgườiDùng;
    for (unsigned chỉSốThứBậc = 0; chỉSốThứBậc < sốLượngTrangNgườiDùng; chỉSốThứBậc++) {
        unsigned cácQuyềnTruyCập = danhSáchCácQuyền[chỉSốThứBậc];
        danhSáchTrang[chỉSốThứBậc] = cácQuyềnTruyCập ? (cơSởNgườiDùng + chỉSốThứBậc * cỡTrang) | (cácQuyềnTruyCập == 3 ? ghiĐọcNgườiDùng : cácQuyềnTruyCập == 5 ? thựcThiĐọcNgườiDùng : chỉĐọcNgườiDùng) : 0;
    }
    cácBảngTraĐồngBộ();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned chỉSốThứBậc = 0; chỉSốThứBậc < 16; chỉSốThứBậc++) danhSáchTệp[chỉSốThứBậc] = -1;
    memset(cácĐiểmCuốiỔCắmMạng, 0, sizeof(cácĐiểmCuốiỔCắmMạng));
    kếtThúcVùngNhớĐộng = kếtThúcẢnhNgườiDùng;
    hoạtĐộng = 1; bắtChạyHếtGiờ();
    thờiGianViệcThựcThiNgườiDùng[đốiTượngChủSởHữu]=miliGiâyGọnBoMạch();
    int kếtQuả = vàoNgườiDùng(đầuMụcTệpThựcThi.điểmMục, ngănXếpBanĐầu, giáTrịĐãChuyểnTiếp);
    return hoànThànhChươngTrình(kếtQuả);
}
uintptr_t chạyNgườiDùngBoMạch(uintptr_t chỉSốTraCứu) {
    if (chỉSốTraCứu >= sizeof(cácMụcTệpThựcThi) / sizeof(cácMụcTệpThựcThi[0])) return (uint32_t)-22;
    const char *tên=chỉSốTraCứu==10?"javac":chỉSốTraCứu==11?"java":chỉSốTraCứu==12?"python":chỉSốTraCứu==13?"vi":chỉSốTraCứu==14?"jar":chỉSốTraCứu==15?"cc":chỉSốTraCứu==16?"jaot":"ELF";
    return (uint32_t)chạyChươngTrình(cácMụcTệpThựcThi[chỉSốTraCứu].DữLiệu, cácMụcTệpThựcThi[chỉSốTraCứu].cỡ, cácMụcTệpThựcThi[chỉSốTraCứu].giáTrịĐãChuyểnTiếp, 0, tên);
}
static uintptr_t thựcThiTệp(int chếĐộLinux) {
    static unsigned char ảnh[16384];
    if (hoạtĐộng || !sốLượngĐốiSốĐãChuyểnTiếp) return (uint32_t)-22;
    int thẻXửLýTệp = pk_open((const char *)đốiSốĐãChuyểnTiếp[0], đọcGiáTrịChỉ, 0);
    if (thẻXửLýTệp < 0) return (uint32_t)-sốLỗi;
    int cỡ = pk_size(thẻXửLýTệp);
    if (cỡ < 0 || (unsigned)cỡ > sizeof(ảnh)) { pk_close(thẻXửLýTệp); return (uint32_t)-27; }
    int sốLượngĐãNhận = pk_read(thẻXửLýTệp, ảnh, cỡ); pk_close(thẻXửLýTệp);
    if (sốLượngĐãNhận != cỡ) return (uint32_t)-5;
    return (uint32_t)chạyChươngTrình(ảnh, cỡ, 0, chếĐộLinux, "");
}
uintptr_t tệpNgườiDùngBoMạch(void) { return thựcThiTệp(0); }
uintptr_t tệpLinuxNgườiDùngBoMạch(void) { return thựcThiTệp(1); }
uintptr_t thẩmĐịnhNgườiDùngBoMạch(void) {
    for (unsigned chỉSốThứBậc = 0; chỉSốThứBậc < sizeof(cácTệpThựcThiKhôngHợpLệ) / sizeof(cácTệpThựcThiKhôngHợpLệ[0]); chỉSốThứBậc++)
        if (eLFThẩmĐịnhNgườiDùng(cácTệpThựcThiKhôngHợpLệ[chỉSốThứBậc].DữLiệu, cácTệpThựcThiKhôngHợpLệ[chỉSốThứBậc].cỡ) != lỗiTệpThựcThiNgườiDùng) return chỉSốThứBậc + 1;
    return 0;
}
