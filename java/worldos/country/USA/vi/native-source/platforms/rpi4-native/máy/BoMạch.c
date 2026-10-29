#include "../cáchĐặtTên/cácTênLiênKếtMáy.h"
#include "thôngTinMànHình.h"
#include <stdint.h>
#include <stddef.h>
#include "NgườiDùng.h"
#include "../NgănXếpMạng/NgănXếpMạng.h"
typedef uintptr_t từMáy;
#define thanhGhiMáy(giáTrịĐầuTiên) (*(volatile uint32_t *)(uintptr_t)(giáTrịĐầuTiên))
#define thiếtBịNốiTiếp 0xfe201000u
#define vàoRaMụcĐíchTổngQuát 0xfe200000u
#define địaChỉHộpThư 0xfe00b880u
static inline void ràoChắnBộNhớ(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t sốLượngĐồngHồ(void) { uint64_t dữLiệuTạm; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(dữLiệuTạm)); return dữLiệuTạm; }
static uint64_t tầnSố;
static volatile uint32_t dữLiệuHộpThư[64] __attribute__((aligned(16)));
static unsigned sẵnSàngMànHình;
static uint32_t bKiBộNhớARM;

void *memset(void *vịTríDữLiệu, int mãKýTự, size_t sốLượngPhầnMục) { unsigned char *độLệchKếTiếp = vịTríDữLiệu; while (sốLượngPhầnMục--) *độLệchKếTiếp++ = mãKýTự; return vịTríDữLiệu; }
void *memcpy(void *dữLiệuĐích, const void *dữLiệuChuỗi, size_t sốLượngPhầnMục) { unsigned char *giáTrịĐầuTiên = dữLiệuĐích; const unsigned char *giáTrịThứHai = dữLiệuChuỗi; while (sốLượngPhầnMục--) *giáTrịĐầuTiên++ = *giáTrịThứHai++; return dữLiệuĐích; }

static int hộpThư(void) {
    uint32_t yêuCầu = (uint32_t)(uintptr_t)dữLiệuHộpThư | 8;
    uint64_t chạy = sốLượngĐồngHồ();
    ràoChắnBộNhớ();
    while (thanhGhiMáy(địaChỉHộpThư + 0x38) & 0x80000000u)
        if (sốLượngĐồngHồ() - chạy > tầnSố) return 0;
    thanhGhiMáy(địaChỉHộpThư + 0x20) = yêuCầu;
    for (;;) {
        if (!(thanhGhiMáy(địaChỉHộpThư + 0x18) & 0x40000000u)) {
            uint32_t lờiĐáp = thanhGhiMáy(địaChỉHộpThư);
            if (lờiĐáp == yêuCầu) { ràoChắnBộNhớ(); return dữLiệuHộpThư[1] == 0x80000000u; }
        }
        if (sốLượngĐồngHồ() - chạy > tầnSố) return 0;
    }
}

extern int32_t đầuRaVỏLệnhJava(int32_t, int32_t), đầuVàoVỏLệnhJava(void);
extern void byteThiếtBịCuối(unsigned);
extern int đangChờThiếtBịCuối(void);
extern void conTrỏThiếtBịCuối(unsigned,int,int),phímTắtThiếtBịCuối(unsigned);
extern void chếĐộĐầuVàoThiếtBịCuối(unsigned);
#include "../giáTrịTừXa/giáTrịTừXa.h"
static int cácLuồng;
static unsigned trướcĐóUART;
từMáy cácLuồngBoMạch(từMáy làĐãDùng) { cácLuồng=làĐãDùng!=0; return 0; }
từMáy kênhBoMạch(từMáy kênh, từMáy mãKýTự) {
    if(cácLuồng && đầuRaVỏLệnhJava((int32_t)kênh,(int32_t)(mãKýTự&255))) return 0;
    byteThiếtBịCuối(mãKýTự&255);
    đầuRaTừXa(mãKýTự&255);
    if ((mãKýTự&255)==10 && trướcĐóUART!=13) {
        while (thanhGhiMáy(thiếtBịNốiTiếp + 0x18) & 0x20) __asm__ volatile("yield");
        thanhGhiMáy(thiếtBịNốiTiếp)=13;
    }
    trướcĐóUART=mãKýTự&255;
    while (thanhGhiMáy(thiếtBịNốiTiếp + 0x18) & 0x20) __asm__ volatile("yield");
    thanhGhiMáy(thiếtBịNốiTiếp) = (uint32_t)mãKýTự & 255;
    return 0;
}
từMáy đặtKýTựBoMạch(từMáy mãKýTự) { return kênhBoMạch(1,mãKýTự); }
từMáy lấyKýTựThôBoMạch(void) {
    int kýTựTừXa=đầuVàoTừXa();if(kýTựTừXa>=0)return kýTựTừXa;
    if (thanhGhiMáy(thiếtBịNốiTiếp + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t giáTrị = thanhGhiMáy(thiếtBịNốiTiếp);
    if (giáTrị & 0xf00) { thanhGhiMáy(thiếtBịNốiTiếp + 4) = 0; return (uint32_t)-1; }
    return giáTrị & 255;
}
từMáy lấyKýTựBoMạch(void) {
    network_poll();
    static unsigned góiTinTrong,sứcChứaĐãDùng; static unsigned char dữLiệuGóiTin[6];
    if(đangChờThiếtBịCuối())return (uint32_t)-4096;
    if(cácLuồng){int32_t mãKýTự=đầuVàoVỏLệnhJava();if(mãKýTự!=-3)return (uint32_t)mãKýTự;}
    for(;;){
        int mãKýTự=(int32_t)lấyKýTựThôBoMạch();if(mãKýTự<0)return (uint32_t)mãKýTự;
        if(!góiTinTrong){if(mãKýTự!=30)return mãKýTự;góiTinTrong=1;sứcChứaĐãDùng=0;continue;}
        dữLiệuGóiTin[sứcChứaĐãDùng++]=mãKýTự;if(sứcChứaĐãDùng<6)continue;góiTinTrong=0;
        if(dữLiệuGóiTin[0]==1)conTrỏThiếtBịCuối(dữLiệuGóiTin[1],dữLiệuGóiTin[2]+dữLiệuGóiTin[3]*256,dữLiệuGóiTin[4]+dữLiệuGóiTin[5]*256);
        if(dữLiệuGóiTin[0]==2)phímTắtThiếtBịCuối(dữLiệuGóiTin[1]);
        if(dữLiệuGóiTin[0]==3)chếĐộĐầuVàoThiếtBịCuối(dữLiệuGóiTin[1]);
        if(đangChờThiếtBịCuối())return (uint32_t)-4096;
    }
}
từMáy miliGiâyGọnBoMạch(void) { return (uint32_t)(sốLượngĐồngHồ() / (tầnSố / 1000)); }
từMáy mứcNgoạiLệBoMạch(void) { uint64_t dữLiệuTạm; __asm__ volatile("mrs %0, CurrentEL" : "=r"(dữLiệuTạm)); return dữLiệuTạm >> 2; }
static void uARTĐặtChuỗi(const char *dữLiệuChuỗi) { while (*dữLiệuChuỗi) đặtKýTựBoMạch((unsigned char)*dữLiệuChuỗi++); }
static void uARTHệMườiSáu(từMáy sốLượngPhầnMục) { const char *cácChữSốThậpLụcPhân = "0123456789abcdef"; for (int dữLiệuChuỗi = 60; dữLiệuChuỗi >= 0; dữLiệuChuỗi -= 4) đặtKýTựBoMạch(cácChữSốThậpLụcPhân[(sốLượngPhầnMục >> dữLiệuChuỗi) & 15]); }
từMáy dừngBoMạch(từMáy giáTrịTrạngThái) {
    uARTĐặtChuỗi("\r\nHALTED "); uARTHệMườiSáu(giáTrịTrạngThái); uARTĐặtChuỗi("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void dừngKhẩnNhân(const char *giáTrịNguyênNhân) __attribute__((noreturn));
void dừngKhẩnNhân(const char *giáTrịNguyênNhân) { uARTĐặtChuỗi("\r\nPANIC: "); uARTĐặtChuỗi(giáTrịNguyênNhân); dừngBoMạch(1); __builtin_unreachable(); }
void ngoạiLệBoMạch(từMáy trạngTháiNgoạiLệ, từMáy vịTríLệnh, từMáy địaChỉKhôngHợpLệ) {
    uARTĐặtChuỗi("\r\nEXCEPTION ESR="); uARTHệMườiSáu(trạngTháiNgoạiLệ);
    uARTĐặtChuỗi(" PC="); uARTHệMườiSáu(vịTríLệnh); uARTĐặtChuỗi(" FAR="); uARTHệMườiSáu(địaChỉKhôngHợpLệ);
    dừngBoMạch(2);
}
int phầnCứngVậtLýBoMạch(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    dữLiệuHộpThư[0]=32;dữLiệuHộpThư[1]=0;dữLiệuHộpThư[2]=0x10004;dữLiệuHộpThư[3]=8;dữLiệuHộpThư[4]=0;
    dữLiệuHộpThư[5]=dữLiệuHộpThư[6]=dữLiệuHộpThư[7]=0;
    return hộpThư()&&dữLiệuHộpThư[4]==0x80000008u&&(dữLiệuHộpThư[5]||dữLiệuHộpThư[6]);
}
int địaChỉMáyBoMạch(unsigned char *địaChỉ) {
    dữLiệuHộpThư[0]=32;dữLiệuHộpThư[1]=0;dữLiệuHộpThư[2]=0x10003;dữLiệuHộpThư[3]=8;dữLiệuHộpThư[4]=0;
    dữLiệuHộpThư[5]=dữLiệuHộpThư[6]=dữLiệuHộpThư[7]=0;
    if(!hộpThư()||(dữLiệuHộpThư[4]&0x80000000u)==0||(dữLiệuHộpThư[4]&0xffff)!=6)return 0;
    const unsigned char *DữLiệu=(const unsigned char*)&dữLiệuHộpThư[5];unsigned giáTrịTổng=0;
    for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<6;chỉSốThứBậc++){địaChỉ[chỉSốThứBậc]=DữLiệu[chỉSốThứBậc];giáTrịTổng|=DữLiệu[chỉSốThứBậc];}return giáTrịTổng&&!(địaChỉ[0]&1);
}
void khởiTạoGọnBoMạch(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(tầnSố));
    thanhGhiMáy(thiếtBịNốiTiếp + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    thanhGhiMáy(vàoRaMụcĐíchTổngQuát + 4) = (thanhGhiMáy(vàoRaMụcĐíchTổngQuát + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    thanhGhiMáy(vàoRaMụcĐíchTổngQuát + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. giáTrịSựThấtBại 시 config.txt의 48MHz를 사용한다.
    dữLiệuHộpThư[0] = 36; dữLiệuHộpThư[1] = 0; dữLiệuHộpThư[2] = 0x38002; dữLiệuHộpThư[3] = 12;
    dữLiệuHộpThư[4] = 0; dữLiệuHộpThư[5] = 2; dữLiệuHộpThư[6] = 48000000; dữLiệuHộpThư[7] = 0; dữLiệuHộpThư[8] = 0;
    int ổnĐịnhĐồngHồ = hộpThư();
    uint32_t giáTrịTốcĐộ = ổnĐịnhĐồngHồ && dữLiệuHộpThư[6] >= 1843200 ? dữLiệuHộpThư[6] : 48000000;
    dữLiệuHộpThư[0]=32; dữLiệuHộpThư[1]=0; dữLiệuHộpThư[2]=0x10005; dữLiệuHộpThư[3]=8; dữLiệuHộpThư[4]=0;
    dữLiệuHộpThư[5]=dữLiệuHộpThư[6]=dữLiệuHộpThư[7]=0;
    if (hộpThư() && dữLiệuHộpThư[4]==0x80000008u) bKiBộNhớARM=dữLiệuHộpThư[6]/1024;
    uint32_t sốChia64 = (uint32_t)(((uint64_t)giáTrịTốcĐộ * 4 + 57600) / 115200);
    thanhGhiMáy(thiếtBịNốiTiếp + 0x44) = 0x7ff;
    thanhGhiMáy(thiếtBịNốiTiếp + 0x24) = sốChia64 / 64;
    thanhGhiMáy(thiếtBịNốiTiếp + 0x28) = sốChia64 % 64;
    thanhGhiMáy(thiếtBịNốiTiếp + 0x2c) = (3u << 5) | (1u << 4);
    thanhGhiMáy(thiếtBịNốiTiếp + 0x38) = 0;
    thanhGhiMáy(thiếtBịNốiTiếp + 0x30) = 0x301;
    ràoChắnBộNhớ();
    uARTĐặtChuỗi("JKOROS AARCH64 BARE METAL\r\n");
    khởiTạoGọnHệThốngNgườiDùng();
    network_init();
}
từMáy fTPBoMạch(từMáy hànhĐộng) { return (uint32_t)ftp_control((int)hànhĐộng); }
từMáy tìnhTrạngMạngBoMạch(từMáy giáTrịMục, từMáy sốHiệu) { return đọcTìnhTrạngMạng(giáTrịMục, sốHiệu); }
từMáy cácThiếtLậpMạngBoMạch(từMáy hànhĐộng, từMáy địaChỉ, từMáy giáTrịMặtNạ, từMáy giáTrịCổngNối) { return (uint32_t)đặtCấuHìnhMạng(hànhĐộng, địaChỉ, giáTrịMặtNạ, giáTrịCổngNối); }
từMáy phảnHồiGửiBoMạch(từMáy địaChỉ, từMáy giáTrịThứTự) { return (uint32_t)bắtChạyThửPhảnHồi(địaChỉ, giáTrịThứTự); }
từMáy phảnHồiĐọcBoMạch(từMáy giáTrịMục) { return (uint32_t)đọcThửPhảnHồi(giáTrịMục); }
từMáy tắtNguồnĐiệnBoMạch(void) {
    ftp_control(0);
    for (unsigned sốHiệu=0; sốHiệu<32; sốHiệu++) đóngMạng(sốHiệu);
    for (unsigned sốHiệu=0; sốHiệu<4; sốHiệu++) điềuKhiểnNgườiDùngBoMạch(32+sốHiệu);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    uARTĐặtChuỗi("\r\nPOWER OFF\r\n");
    while (thanhGhiMáy(thiếtBịNốiTiếp+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    thanhGhiMáy(0xfe100020ul)=0x5a000000u | (thanhGhiMáy(0xfe100020ul)&~0xfffu) | 0x555;
    thanhGhiMáy(0xfe100024ul)=0x5a000000u | 10;
    thanhGhiMáy(0xfe10001cul)=0x5a000000u | (thanhGhiMáy(0xfe10001cul)&~0x30u) | 0x20;
    ràoChắnBộNhớ();
    for (;;) __asm__ volatile("wfe");
}

từMáy bộĐệmKhungBoMạch(void) {
    if (sẵnSàngMànHình) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 phầnMụcHiệnTại 크기를 읽는다. */
    const uint32_t giáTrịTruyVấn[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t rộngĐãYêuCầu = 640, caoĐãYêuCầu = 480;
    for (size_t chỉSốThứBậc = 0; chỉSốThứBậc < sizeof(giáTrịTruyVấn)/4; chỉSốThứBậc++) dữLiệuHộpThư[chỉSốThứBậc] = giáTrịTruyVấn[chỉSốThứBậc];
    if (hộpThư() && dữLiệuHộpThư[4] == 0x80000008u &&
        dữLiệuHộpThư[5] >= 640 && dữLiệuHộpThư[5] <= 1920 &&
        dữLiệuHộpThư[6] >= 480 && dữLiệuHộpThư[6] <= 1080) {
        rộngĐãYêuCầu = dữLiệuHộpThư[5]; caoĐãYêuCầu = dữLiệuHộpThư[6];
    }
    const uint32_t yêuCầu[] = {
        35 * 4, 0,
        0x48003, 8, 0, rộngĐãYêuCầu, caoĐãYêuCầu,
        0x48004, 8, 0, rộngĐãYêuCầu, caoĐãYêuCầu,
        0x48005, 4, 0, 32,
        0x48006, 4, 0, 1,
        0x48009, 8, 0, 0, 0,
        0x40001, 8, 0, 4096, 0,
        0x40008, 4, 0, 0,
        0
    };
    for (size_t chỉSốThứBậc = 0; chỉSốThứBậc < sizeof(yêuCầu)/4; chỉSốThứBậc++) dữLiệuHộpThư[chỉSốThứBậc] = yêuCầu[chỉSốThứBậc];
    // giáTrịĐỉnh 메시지의 dữLiệuThựcTế 길이를 giáTrịDùng: 태그 thêmCuốiMục 시 độDài 불일치를 방지한다.
    dữLiệuHộpThư[0] = sizeof(yêuCầu);
    if (!hộpThư()) return 0;
    const unsigned cácPhảnHồi[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned độDàiPhảnHồi[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned chỉSốThứBậc = 0; chỉSốThứBậc < sizeof(cácPhảnHồi)/sizeof(cácPhảnHồi[0]); chỉSốThứBậc++)
        if (dữLiệuHộpThư[cácPhảnHồi[chỉSốThứBậc]] != (0x80000000u | độDàiPhảnHồi[chỉSốThứBậc])) return 0;
    uint32_t giáTrịNền = dữLiệuHộpThư[28] & 0x3fffffffu;
    uint32_t cỡ = dữLiệuHộpThư[29];
    uint32_t rộngĐãNhận = dữLiệuHộpThư[5], caoĐãNhận = dữLiệuHộpThư[6], giãnCáchDòngĐãNhận = dữLiệuHộpThư[33];
    if (dữLiệuHộpThư[15] != 32 || dữLiệuHộpThư[19] != 1 ||
        rộngĐãNhận < 640 || rộngĐãNhận > 1920 || caoĐãNhận < 480 || caoĐãNhận > 1080 ||
        dữLiệuHộpThư[10] < rộngĐãNhận || dữLiệuHộpThư[11] < caoĐãNhận || dữLiệuHộpThư[23] || dữLiệuHộpThư[24] ||
        !giáTrịNền || giáTrịNền < 0x1000000 || (giáTrịNền & 3) || giãnCáchDòngĐãNhận < rộngĐãNhận * 4 || (giãnCáchDòngĐãNhận & 3) ||
        (uint64_t)giãnCáchDòngĐãNhận * caoĐãNhận > cỡ || (uint64_t)giáTrịNền + cỡ > 0x40000000u)
        return 0;
    bảnVẽChuẩnBịBoMạch((volatile uint32_t *)(uintptr_t)giáTrịNền, rộngĐãNhận, caoĐãNhận, giãnCáchDòngĐãNhận);
    sẵnSàngMànHình = 1;
    return 1;
}

// 단일 코어의 협력식 giáTrịLuồngChạy. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t đãLưu[13]; } ngữCảnh;
static ngữCảnh cácNgữCảnh[3];
static unsigned char cácNgănXếp[2][65536] __attribute__((aligned(16)));
static int làĐangChạy[3] = {1, 0, 0};
static int tácVụHiệnTại;
extern void chuyểnNgữCảnh(ngữCảnh *, ngữCảnh *);
extern void tácVụJava(int32_t);
từMáy nhườngBoMạch(void) {
    network_poll();
    int phầnMụcTrướcĐó = tácVụHiệnTại, phầnMụcKếTiếp = (phầnMụcTrướcĐó + 1) % 3;
    while (phầnMụcKếTiếp != phầnMụcTrướcĐó && !làĐangChạy[phầnMụcKếTiếp]) phầnMụcKếTiếp = (phầnMụcKếTiếp + 1) % 3;
    if (phầnMụcKếTiếp != phầnMụcTrướcĐó) {
        for (unsigned chỉSốThứBậc = 0; chỉSốThứBậc < 2; chỉSốThứBậc++)
            if (làĐangChạy[chỉSốThứBậc + 1] && *(uint64_t *)cácNgănXếp[chỉSốThứBậc] != 0x6b6f726f7373746bull)
                dừngKhẩnNhân("task stack guard");
        tácVụHiệnTại = phầnMụcKếTiếp;
        chuyểnNgữCảnh(&cácNgữCảnh[phầnMụcTrướcĐó], &cácNgữCảnh[phầnMụcKếTiếp]);
    }
    return 0;
}
static void mồiKhởiĐộngTácVụ(void) {
    tácVụJava(tácVụHiệnTại);
    làĐangChạy[tácVụHiệnTại] = 0;
    nhườngBoMạch();
    dừngKhẩnNhân("finished task resumed");
}
từMáy tạoTácVụBoMạch(từMáy giáTrịĐịnhDanh) {
    if (giáTrịĐịnhDanh < 1 || giáTrịĐịnhDanh > 2 || làĐangChạy[giáTrịĐịnhDanh]) return (uint32_t)-1;
    memset(&cácNgữCảnh[giáTrịĐịnhDanh], 0, sizeof(ngữCảnh));
    *(uint64_t *)cácNgănXếp[giáTrịĐịnhDanh - 1] = 0x6b6f726f7373746bull;
    cácNgữCảnh[giáTrịĐịnhDanh].đãLưu[11] = (uintptr_t)mồiKhởiĐộngTácVụ;
    cácNgữCảnh[giáTrịĐịnhDanh].đãLưu[12] = (uintptr_t)(cácNgănXếp[giáTrịĐịnhDanh - 1] + sizeof(cácNgănXếp[0]));
    làĐangChạy[giáTrịĐịnhDanh] = 1;
    return 0;
}
từMáy trạngTháiTácVụBoMạch(từMáy giáTrịĐịnhDanh) { return giáTrịĐịnhDanh < 3 ? làĐangChạy[giáTrịĐịnhDanh] : (uint32_t)-1; }
extern từMáy traCứuBộNhớBiênDịchTrước(từMáy);
extern uint32_t đọcTrạngTháiNgườiDùng(unsigned, unsigned);
extern unsigned char ĐỉnhNgănXếp[];
từMáy hệThốngTruyVấnBoMạch(từMáy giáTrịMục, từMáy sốHiệu) {
    if (giáTrịMục==0) return bKiBộNhớARM;
    if (giáTrịMục==1) return ((uintptr_t)ĐỉnhNgănXếp-0x80000+1023)/1024;
    if (giáTrịMục==2 || giáTrịMục==3) return traCứuBộNhớBiênDịchTrước(giáTrịMục==3);
    if (giáTrịMục==4) return sẵnSàngMànHình ? (rộngMànHìnhBoMạch()*caoMànHìnhBoMạch()*4+1023)/1024 : 0;
    if (giáTrịMục==5) return 80*1024; /* thựcThiLệnh miềnĐịaChỉ 16 MiB + 네 세션 giữNguyênGiáTrị miềnĐịaChỉ. */
    if (giáTrịMục>=20) return đọcTrạngTháiNgườiDùng(giáTrịMục-20, sốHiệu);
    return 0;
}
int *pk_errno_location(void) { static int cácLỗi[3]; return &cácLỗi[tácVụHiệnTại]; }
