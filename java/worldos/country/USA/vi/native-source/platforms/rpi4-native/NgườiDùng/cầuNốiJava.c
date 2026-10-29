#include "../cáchĐặtTên/cácTênLiênKếtMáy.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Tệp/ĐầuRa/인수는 xâyDựngTấtCả EL0 SVC를 거친다.
#include "gọiThựcHiện.h"
#include "java-resources.h"
#include "GóiGộp.h"
typedef uintptr_t từMáy;
static int giáTrịLoạiMục;
static int hoạtĐộngJAR, dịchJAR;
static từMáy đốiSốĐãChuyểnTiếp[8][257];
static unsigned thayMãĐangChờ;
extern int32_t mụcJava(void);
static intptr_t gọiThựcHiện(unsigned sốLượngPhầnMục, từMáy giáTrịĐầuTiên, từMáy giáTrịThứHai, từMáy mãKýTự) {
    return gọiThựcHiệnNgườiDùng(sốLượngPhầnMục, giáTrịĐầuTiên, giáTrịThứHai, mãKýTự, 0, 0, 0);
}
static void cácGiáTrịByte(const char *vịTríDữLiệu, size_t sốLượngPhầnMục) { gọiThựcHiện(1, 1, (từMáy)vịTríDữLiệu, sốLượngPhầnMục); }
static void kýTự(unsigned mãKýTự) {
    unsigned char DữLiệu[4]; unsigned sốLượngPhầnMục = 0;
    if (mãKýTự < 128) DữLiệu[sốLượngPhầnMục++] = mãKýTự;
    else if (mãKýTự < 2048) { DữLiệu[sốLượngPhầnMục++] = 0xc0 | (mãKýTự >> 6); DữLiệu[sốLượngPhầnMục++] = 0x80 | (mãKýTự & 63); }
    else if (mãKýTự < 65536) { DữLiệu[sốLượngPhầnMục++] = 0xe0 | (mãKýTự >> 12); DữLiệu[sốLượngPhầnMục++] = 0x80 | ((mãKýTự >> 6) & 63); DữLiệu[sốLượngPhầnMục++] = 0x80 | (mãKýTự & 63); }
    else { DữLiệu[sốLượngPhầnMục++] = 0xf0 | (mãKýTự >> 18); DữLiệu[sốLượngPhầnMục++] = 0x80 | ((mãKýTự >> 12) & 63); DữLiệu[sốLượngPhầnMục++] = 0x80 | ((mãKýTự >> 6) & 63); DữLiệu[sốLượngPhầnMục++] = 0x80 | (mãKýTự & 63); }
    cácGiáTrịByte((const char *)DữLiệu, sốLượngPhầnMục);
}
từMáy kýTựCôngCụ(từMáy giáTrị) {
    unsigned mãKýTự = giáTrị;
    if (thayMãĐangChờ) {
        unsigned phầnCaoTrên = thayMãĐangChờ; thayMãĐangChờ = 0;
        if (mãKýTự >= 0xdc00 && mãKýTự <= 0xdfff) { kýTự(0x10000 + ((phầnCaoTrên - 0xd800) << 10) + mãKýTự - 0xdc00); return 1; }
        kýTự(0xfffd);
    }
    if (mãKýTự >= 0xd800 && mãKýTự <= 0xdbff) thayMãĐangChờ = mãKýTự;
    else kýTự(mãKýTự > 0x10ffff || (mãKýTự >= 0xdc00 && mãKýTự <= 0xdfff) ? 0xfffd : mãKýTự);
    return 1;
}
từMáy inCôngCụ(từMáy giáTrị) {
    const từMáy *dữLiệuChuỗi = (const từMáy *)giáTrị;
    for (từMáy chỉSốThứBậc = 0; chỉSốThứBậc < dữLiệuChuỗi[0]; chỉSốThứBậc++) kýTựCôngCụ(dữLiệuChuỗi[chỉSốThứBậc + 1]);
    return dữLiệuChuỗi[0];
}
static int đườngDẫn(từMáy thamChiếuĐốiTượng, char dữLiệuKếtQuả[512]) {
    const từMáy *giáTrịĐầuTiên = (const từMáy *)thamChiếuĐốiTượng;
    unsigned sứcChứaĐãDùng = 0;
    for (từMáy chỉSốThứBậc = 1; chỉSốThứBậc <= giáTrịĐầuTiên[0] && giáTrịĐầuTiên[chỉSốThứBậc]; chỉSốThứBậc++) {
        unsigned mãKýTự = giáTrịĐầuTiên[chỉSốThứBậc];
        // UTF-16 -> UTF-8. 기존 도구의 char[] chếĐộPhươngThức 경로와 호환한다.
        if (mãKýTự >= 0xd800 && mãKýTự <= 0xdbff && chỉSốThứBậc < giáTrịĐầuTiên[0] && giáTrịĐầuTiên[chỉSốThứBậc + 1] >= 0xdc00 && giáTrịĐầuTiên[chỉSốThứBậc + 1] <= 0xdfff)
            { unsigned giáTrịThấp = giáTrịĐầuTiên[++chỉSốThứBậc]; mãKýTự = 0x10000 + ((mãKýTự - 0xd800) << 10) + giáTrịThấp - 0xdc00; }
        else if (mãKýTự >= 0xd800 && mãKýTự <= 0xdfff) return -22;
        unsigned sốLượngPhầnMục = mãKýTự < 128 ? 1 : mãKýTự < 2048 ? 2 : mãKýTự < 65536 ? 3 : 4;
        if (sứcChứaĐãDùng + sốLượngPhầnMục > 511) return -36;
        if (sốLượngPhầnMục == 1) dữLiệuKếtQuả[sứcChứaĐãDùng++] = mãKýTự;
        else {
            dữLiệuKếtQuả[sứcChứaĐãDùng++] = (sốLượngPhầnMục == 2 ? 0xc0 : sốLượngPhầnMục == 3 ? 0xe0 : 0xf0) | (mãKýTự >> (6 * (sốLượngPhầnMục - 1)));
            for (unsigned thứBậcPhíaTrong = sốLượngPhầnMục - 1; thứBậcPhíaTrong; thứBậcPhíaTrong--) dữLiệuKếtQuả[sứcChứaĐãDùng++] = 0x80 | ((mãKýTự >> (6 * (thứBậcPhíaTrong - 1))) & 63);
        }
    }
    dữLiệuKếtQuả[sứcChứaĐãDùng] = 0; return sứcChứaĐãDùng ? 0 : -22;
}
từMáy mởCôngCụ(từMáy tên, từMáy cácBitCấuHình) {
    char vịTríDữLiệu[512]; int lỗi = đườngDẫn(tên, vịTríDữLiệu);
    return (uint32_t)(lỗi ? lỗi : gọiThựcHiện(3, (từMáy)vịTríDữLiệu, cácBitCấuHình, 0));
}
từMáy đóngCôngCụ(từMáy thẻXửLýTệp) { return (uint32_t)gọiThựcHiện(4, thẻXửLýTệp, 0, 0); }
từMáy byteĐọcCôngCụ(từMáy thẻXửLýTệp) {
    unsigned char giáTrịThứHai; intptr_t sốLượngPhầnMục = gọiThựcHiện(2, thẻXửLýTệp, (từMáy)&giáTrịThứHai, 1);
    return (uint32_t)(sốLượngPhầnMục == 1 ? giáTrịThứHai : sốLượngPhầnMục == 0 ? 256 : sốLượngPhầnMục);
}
từMáy byteGhiCôngCụ(từMáy thẻXửLýTệp, từMáy giáTrị) {
    unsigned char giáTrịThứHai = giáTrị; return (uint32_t)gọiThựcHiện(1, thẻXửLýTệp, (từMáy)&giáTrịThứHai, 1);
}
từMáy đọcCôngCụ(từMáy tên, từMáy địaChỉDữLiệuĐích) {
    if (hoạtĐộngJAR) {
        char vịTríDữLiệu[512]; int lỗi = đườngDẫn(tên, vịTríDữLiệu); if (lỗi) return (uint32_t)lỗi;
        unsigned sốLượngPhầnMục = 0; while (vịTríDữLiệu[sốLượngPhầnMục]) sốLượngPhầnMục++;
        if (sốLượngPhầnMục >= 6) for (unsigned chỉSốThứBậc = 0; chỉSốThứBậc < sốLượngPhầnMục - 6; chỉSốThứBậc++) if (vịTríDữLiệu[chỉSốThứBậc] == '.') vịTríDữLiệu[chỉSốThứBậc] = '/';
        unsigned char cácGiáTrịByte[16384]; từMáy *vịTríGiáTrịĐích = (từMáy *)địaChỉDữLiệuĐích;
        int sốLượngĐãNhận = đọcJAR(vịTríDữLiệu, cácGiáTrịByte, vịTríGiáTrịĐích[0] < sizeof(cácGiáTrịByte) ? vịTríGiáTrịĐích[0] : sizeof(cácGiáTrịByte));
        if (sốLượngĐãNhận >= 0) { for (int chỉSốThứBậc = 0; chỉSốThứBậc < sốLượngĐãNhận; chỉSốThứBậc++) vịTríGiáTrịĐích[chỉSốThứBậc + 1] = cácGiáTrịByte[chỉSốThứBậc]; return sốLượngĐãNhận; }
        if (sốLượngĐãNhận != -2) return (uint32_t)sốLượngĐãNhận;
    }
    int thẻXửLýTệp = hoạtĐộngJAR ? -2 : (int32_t)mởCôngCụ(tên, 0);
    if (thẻXửLýTệp < 0) {
        char vịTríDữLiệu[512]; int lỗi = đườngDẫn(tên, vịTríDữLiệu); if (lỗi) return (uint32_t)lỗi;
        for (unsigned chỉSốThứBậc = 0; chỉSốThứBậc < sizeof(danhSáchLớpJava) / sizeof(danhSáchLớpJava[0]); chỉSốThứBậc++) {
            const char *độLệchKếTiếp = danhSáchLớpJava[chỉSốThứBậc].tên; unsigned thứBậcPhíaTrong = 0;
            while (vịTríDữLiệu[thứBậcPhíaTrong] && vịTríDữLiệu[thứBậcPhíaTrong] == độLệchKếTiếp[thứBậcPhíaTrong]) thứBậcPhíaTrong++;
            if (vịTríDữLiệu[thứBậcPhíaTrong] || độLệchKếTiếp[thứBậcPhíaTrong]) continue;
            từMáy *vịTríGiáTrịĐích = (từMáy *)địaChỉDữLiệuĐích;
            if (vịTríGiáTrịĐích[0] < danhSáchLớpJava[chỉSốThứBậc].cỡ) return (uint32_t)-27;
            for (thứBậcPhíaTrong = 0; thứBậcPhíaTrong < danhSáchLớpJava[chỉSốThứBậc].cỡ; thứBậcPhíaTrong++) vịTríGiáTrịĐích[thứBậcPhíaTrong + 1] = danhSáchLớpJava[chỉSốThứBậc].DữLiệu[thứBậcPhíaTrong];
            return danhSáchLớpJava[chỉSốThứBậc].cỡ;
        }
        return (uint32_t)thẻXửLýTệp;
    }
    từMáy *giáTrịĐầuTiên = (từMáy *)địaChỉDữLiệuĐích;
    intptr_t cỡ = gọiThựcHiện(9, thẻXửLýTệp, 0, 0), lượngĐãHoànTất = 0;
    if (cỡ < 0 || (từMáy)cỡ > giáTrịĐầuTiên[0]) { đóngCôngCụ(thẻXửLýTệp); return (uint32_t)(cỡ < 0 ? cỡ : -27); }
    unsigned char khốiDữLiệu[256];
    while (lượngĐãHoànTất < cỡ) {
        intptr_t sốLượngPhầnMục = gọiThựcHiện(2, thẻXửLýTệp, (từMáy)khốiDữLiệu, cỡ - lượngĐãHoànTất < 256 ? cỡ - lượngĐãHoànTất : 256);
        if (sốLượngPhầnMục <= 0) { đóngCôngCụ(thẻXửLýTệp); return (uint32_t)(sốLượngPhầnMục ? sốLượngPhầnMục : -5); }
        for (intptr_t chỉSốThứBậc = 0; chỉSốThứBậc < sốLượngPhầnMục; chỉSốThứBậc++) giáTrịĐầuTiên[1 + lượngĐãHoànTất + chỉSốThứBậc] = khốiDữLiệu[chỉSốThứBậc];
        lượngĐãHoànTất += sốLượngPhầnMục;
    }
    đóngCôngCụ(thẻXửLýTệp); return lượngĐãHoànTất;
}
từMáy ghiCôngCụ(từMáy tên, từMáy dữLiệuNguyênBản, từMáy sốLượngMục) {
    const từMáy *giáTrịĐầuTiên = (const từMáy *)dữLiệuNguyênBản;
    if (sốLượngMục > giáTrịĐầuTiên[0] || sốLượngMục > 16384) return (uint32_t)-27;
    int thẻXửLýTệp = (int32_t)mởCôngCụ(tên, 577); if (thẻXửLýTệp < 0) return (uint32_t)thẻXửLýTệp;
    unsigned char khốiDữLiệu[256]; từMáy lượngĐãHoànTất = 0;
    while (lượngĐãHoànTất < sốLượngMục) {
        từMáy sốLượngPhầnMục = sốLượngMục - lượngĐãHoànTất < 256 ? sốLượngMục - lượngĐãHoànTất : 256;
        for (từMáy chỉSốThứBậc = 0; chỉSốThứBậc < sốLượngPhầnMục; chỉSốThứBậc++) khốiDữLiệu[chỉSốThứBậc] = giáTrịĐầuTiên[1 + lượngĐãHoànTất + chỉSốThứBậc];
        intptr_t kếtQuả = gọiThựcHiện(1, thẻXửLýTệp, (từMáy)khốiDữLiệu, sốLượngPhầnMục);
        if (kếtQuả <= 0) { đóngCôngCụ(thẻXửLýTệp); return (uint32_t)(kếtQuả ? kếtQuả : -5); }
        lượngĐãHoànTất += kếtQuả;
    }
    đóngCôngCụ(thẻXửLýTệp); return sốLượngMục;
}
từMáy sốĐốiSốCôngCụ(void) { return gọiThựcHiện(15, UINTPTR_MAX, 0, 0) - (hoạtĐộngJAR ? dịchJAR : 0); }
từMáy đốiSốCôngCụ(từMáy chỉSốTraCứu) {
    static const từMáy giáTrịRỗng[1] = {0};
    if (chỉSốTraCứu >= 8) return (từMáy)giáTrịRỗng;
    unsigned char đầuVào[256]; intptr_t sốLượngPhầnMục;
    if (hoạtĐộngJAR && chỉSốTraCứu == 0) { const char *vịTríDữLiệu = chínhJAR(); sốLượngPhầnMục = 0; while (vịTríDữLiệu[sốLượngPhầnMục] && sốLượngPhầnMục < 255) { đầuVào[sốLượngPhầnMục] = vịTríDữLiệu[sốLượngPhầnMục]; sốLượngPhầnMục++; } }
    else sốLượngPhầnMục = gọiThựcHiện(15, chỉSốTraCứu + (hoạtĐộngJAR ? dịchJAR : 0), (từMáy)đầuVào, sizeof(đầuVào));
    if (sốLượngPhầnMục < 0) return (từMáy)giáTrịRỗng;
    từMáy *dữLiệuKếtQuả = đốiSốĐãChuyểnTiếp[chỉSốTraCứu]; unsigned sốLượngMục = 0;
    for (intptr_t chỉSốThứBậc = 0; chỉSốThứBậc < sốLượngPhầnMục;) {
        unsigned mãKýTự = đầuVào[chỉSốThứBậc++], cóThêmNữa = mãKýTự < 128 ? 0 : mãKýTự >= 0xc2 && mãKýTự < 0xe0 ? 1 : mãKýTự < 0xf0 && mãKýTự >= 0xe0 ? 2 : mãKýTự >= 0xf0 && mãKýTự <= 0xf4 ? 3 : 4;
        if (cóThêmNữa == 4 || chỉSốThứBậc + cóThêmNữa > sốLượngPhầnMục) { dữLiệuKếtQuả[++sốLượngMục] = 0xfffd; continue; }
        unsigned dữLiệuTốiThiểu = cóThêmNữa == 1 ? 128 : cóThêmNữa == 2 ? 2048 : cóThêmNữa == 3 ? 65536 : 0;
        if (cóThêmNữa) mãKýTự &= (1u << (6 - cóThêmNữa)) - 1;
        unsigned thứBậcPhíaTrong = 0;
        while (thứBậcPhíaTrong < cóThêmNữa && (đầuVào[chỉSốThứBậc] & 0xc0) == 0x80) { mãKýTự = (mãKýTự << 6) | (đầuVào[chỉSốThứBậc++] & 63); thứBậcPhíaTrong++; }
        if (thứBậcPhíaTrong != cóThêmNữa || mãKýTự < dữLiệuTốiThiểu || mãKýTự > 0x10ffff || (mãKýTự >= 0xd800 && mãKýTự <= 0xdfff)) mãKýTự = 0xfffd;
        if (mãKýTự >= 65536) { mãKýTự -= 65536; dữLiệuKếtQuả[++sốLượngMục] = 0xd800 | (mãKýTự >> 10); dữLiệuKếtQuả[++sốLượngMục] = 0xdc00 | (mãKýTự & 1023); }
        else dữLiệuKếtQuả[++sốLượngMục] = mãKýTự;
    }
    dữLiệuKếtQuả[0] = sốLượngMục; return (từMáy)dữLiệuKếtQuả;
}
từMáy loạiCôngCụ(void) { return giáTrịLoạiMục; }
void dừngKhẩnNhân(const char *vănBảnThôngBáo) {
    const char *vịTríDữLiệu = vănBảnThôngBáo; while (*vịTríDữLiệu) vịTríDữLiệu++;
    cácGiáTrịByte("Java tool runtime error: ", 25); cácGiáTrịByte(vănBảnThôngBáo, vịTríDữLiệu - vănBảnThôngBáo); kýTự(10);
    gọiThựcHiện(6, 1, 0, 0); for (;;) {}
}
int bắtChạyChươngTrìnhNgườiDùng(int chếĐộPhươngThức) {
    giáTrịLoạiMục = chếĐộPhươngThức;
    unsigned char mụcĐầuTiên[256]; intptr_t sốLượngPhầnMục = gọiThựcHiện(15, 0, (từMáy)mụcĐầuTiên, sizeof(mụcĐầuTiên));
    if (chếĐộPhươngThức == 2 || (chếĐộPhươngThức == 1 && sốLượngPhầnMục == 4 && mụcĐầuTiên[0] == '-' && mụcĐầuTiên[1] == 'j' && mụcĐầuTiên[2] == 'a' && mụcĐầuTiên[3] == 'r')) {
        dịchJAR = chếĐộPhươngThức == 2 ? 0 : 1;
        char tênMụcTệp[256]; intptr_t dữLiệuĐộDài = gọiThựcHiện(15, dịchJAR, (từMáy)tênMụcTệp, sizeof(tênMụcTệp));
        if (dữLiệuĐộDài <= 0 || mởJAR(tênMụcTệp) < 0) {
            static const char lỗi[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            cácGiáTrịByte(lỗi, sizeof(lỗi) - 1); return 1;
        }
        hoạtĐộngJAR = 1;
    }
    int kếtQuả = mụcJava();
    if (thayMãĐangChờ) kýTự(0xfffd);
    return kếtQuả;
}

// UDP는 tựThân 커널의 SVC를 통과하며 phầnMụcHiệnTại 127.0.0.1만 제공한다.
struct địaChỉJava { uint16_t họ, sốCổng; uint32_t địaChỉ; unsigned char giáTrịKhôngSố[8]; };
static struct địaChỉJava địaChỉUDP(unsigned sốCổng) {
    struct địaChỉJava giáTrịĐầuTiên = {2, (uint16_t)((sốCổng << 8) | (sốCổng >> 8)), 0x0100007f, {0}}; return giáTrịĐầuTiên;
}
từMáy mởUDPCôngCụ(từMáy sốCổng) {
    intptr_t thẻXửLýTệp = gọiThựcHiện(32, 2, 2, 17); if (thẻXửLýTệp < 0) return (uint32_t)thẻXửLýTệp;
    struct địaChỉJava giáTrịĐầuTiên = địaChỉUDP(sốCổng);
    giáTrịĐầuTiên.địaChỉ = 0;
    intptr_t giáTrịTrạngThái = gọiThựcHiện(33, thẻXửLýTệp, (từMáy)&giáTrịĐầuTiên, sizeof(giáTrịĐầuTiên));
    if (giáTrịTrạngThái < 0) { đóngCôngCụ(thẻXửLýTệp); return (uint32_t)giáTrịTrạngThái; }
    return thẻXửLýTệp;
}
từMáy gửiUDPCôngCụ(từMáy thẻXửLýTệp, từMáy sốCổng, từMáy giáTrịMảng, từMáy độDài) {
    const từMáy *địaChỉNguyênBản = (const từMáy *)giáTrịMảng; unsigned char DữLiệu[512];
    if (độDài > 512 || độDài > địaChỉNguyênBản[0]) return (uint32_t)-90;
    for (từMáy chỉSốThứBậc = 0; chỉSốThứBậc < độDài; chỉSốThứBậc++) DữLiệu[chỉSốThứBậc] = địaChỉNguyênBản[chỉSốThứBậc + 1];
    struct địaChỉJava giáTrịĐầuTiên = địaChỉUDP(sốCổng);
    return (uint32_t)gọiThựcHiệnNgườiDùng(34, thẻXửLýTệp, (từMáy)DữLiệu, độDài, 0, (từMáy)&giáTrịĐầuTiên, sizeof(giáTrịĐầuTiên));
}
static uint32_t thứTựByteĐảo(uint32_t sốLượngPhầnMục) { return (sốLượngPhầnMục>>24)|((sốLượngPhầnMục>>8)&0xff00)|((sốLượngPhầnMục<<8)&0xff0000)|(sốLượngPhầnMục<<24); }
từMáy địaChỉGửiUDPCôngCụ(từMáy thẻXửLýTệp, từMáy địaChỉ, từMáy sốCổng, từMáy giáTrịMảng, từMáy độDài) {
    const từMáy *địaChỉNguyênBản = (const từMáy *)giáTrịMảng; unsigned char DữLiệu[512];
    if (độDài > 512 || độDài > địaChỉNguyênBản[0]) return (uint32_t)-90;
    for (từMáy chỉSốThứBậc = 0; chỉSốThứBậc < độDài; chỉSốThứBậc++) DữLiệu[chỉSốThứBậc] = địaChỉNguyênBản[chỉSốThứBậc + 1];
    struct địaChỉJava giáTrịĐầuTiên = địaChỉUDP(sốCổng); giáTrịĐầuTiên.địaChỉ = thứTựByteĐảo(địaChỉ);
    return (uint32_t)gọiThựcHiệnNgườiDùng(34, thẻXửLýTệp, (từMáy)DữLiệu, độDài, 0, (từMáy)&giáTrịĐầuTiên, sizeof(giáTrịĐầuTiên));
}
từMáy kếtNốiCôngCụ(từMáy thẻXửLýTệp, từMáy địaChỉ, từMáy sốCổng) {
    struct địaChỉJava giáTrịĐầuTiên = địaChỉUDP(sốCổng); giáTrịĐầuTiên.địaChỉ = thứTựByteĐảo(địaChỉ);
    uint32_t chạy = gọiThựcHiện(7, 0, 0, 0);
    for (;;) {
        intptr_t kếtQuả = gọiThựcHiện(37, thẻXửLýTệp, (từMáy)&giáTrịĐầuTiên, sizeof(giáTrịĐầuTiên));
        if (kếtQuả != -115) return (uint32_t)kếtQuả;
        if ((uint32_t)(gọiThựcHiện(7, 0, 0, 0) - chạy) >= 1000) return (uint32_t)-110;
    }
}
từMáy nhậnGọnUDPCôngCụ(từMáy thẻXửLýTệp, từMáy giáTrịMảng, từMáy sứcChứaBộĐệm) {
    từMáy *địaChỉĐích = (từMáy *)giáTrịMảng; unsigned char DữLiệu[512];
    if (sứcChứaBộĐệm > 512 || địaChỉĐích[0] < 514) return (uint32_t)-90;
    struct địaChỉJava giáTrịĐầuTiên; unsigned dữLiệuĐộDài = sizeof(giáTrịĐầuTiên);
    intptr_t sốLượngPhầnMục = gọiThựcHiệnNgườiDùng(35, thẻXửLýTệp, (từMáy)DữLiệu, sứcChứaBộĐệm, 0, (từMáy)&giáTrịĐầuTiên, (từMáy)&dữLiệuĐộDài);
    if (sốLượngPhầnMục >= 0) { for (intptr_t chỉSốThứBậc = 0; chỉSốThứBậc < sốLượngPhầnMục; chỉSốThứBậc++) địaChỉĐích[chỉSốThứBậc + 1] = DữLiệu[chỉSốThứBậc]; địaChỉĐích[513] = (giáTrịĐầuTiên.sốCổng << 8 | giáTrịĐầuTiên.sốCổng >> 8) & 65535; địaChỉĐích[514] = thứTựByteĐảo(giáTrịĐầuTiên.địaChỉ); }
    return (uint32_t)sốLượngPhầnMục;
}
từMáy cổngUDPCôngCụ(từMáy thẻXửLýTệp) {
    struct địaChỉJava giáTrịĐầuTiên; unsigned dữLiệuĐộDài = sizeof(giáTrịĐầuTiên);
    intptr_t giáTrịĐãTrảVề = gọiThựcHiện(36, thẻXửLýTệp, (từMáy)&giáTrịĐầuTiên, (từMáy)&dữLiệuĐộDài);
    return (uint32_t)(giáTrịĐãTrảVề < 0 ? giáTrịĐãTrảVề : (giáTrịĐầuTiên.sốCổng << 8 | giáTrịĐầuTiên.sốCổng >> 8) & 65535);
}
từMáy miliGiâyGọnCôngCụ(void) { return (uint32_t)gọiThựcHiện(7, 0, 0, 0); }
từMáy rộngMànHìnhCôngCụ(void) { return (uint32_t)đọcRộngMànHình(); }
từMáy caoMànHìnhCôngCụ(void) { return (uint32_t)đọcCaoMànHình(); }
từMáy chờĐồHọaCôngCụ(void) { return (uint32_t)chờPhímMànHìnhCho(); }
từMáy hìnhChữNhậtCôngCụ(từMáy tọaĐộX, từMáy tọaĐộY, từMáy giáTrịRộngĐãYêuCầu, từMáy giáTrịCaoĐãYêuCầu, từMáy màuĐiểmẢnh) {
    return (uint32_t)gọiThựcHiệnNgườiDùng(13, tọaĐộX, tọaĐộY, màuĐiểmẢnh, giáTrịRộngĐãYêuCầu, giáTrịCaoĐãYêuCầu, 0);
}

từMáy luồngCôngCụ(từMáy hànhĐộng,từMáy thẻXửLýTệp,từMáy giáTrị){
    if(hànhĐộng==0)return (uint32_t)gọiThựcHiện(32,2,1,6);
    struct địaChỉJava giáTrịĐầuTiên=địaChỉUDP(giáTrị);
    if(hànhĐộng==1){giáTrịĐầuTiên.địaChỉ=0;intptr_t giáTrịĐãTrảVề=gọiThựcHiện(33,thẻXửLýTệp,(từMáy)&giáTrịĐầuTiên,sizeof(giáTrịĐầuTiên));return (uint32_t)(giáTrịĐãTrảVề<0?giáTrịĐãTrảVề:gọiThựcHiện(38,thẻXửLýTệp,4,0));}
    if(hànhĐộng==2)return (uint32_t)gọiThựcHiện(37,thẻXửLýTệp,(từMáy)&giáTrịĐầuTiên,sizeof(giáTrịĐầuTiên));
    if(hànhĐộng==3)return (uint32_t)gọiThựcHiện(39,thẻXửLýTệp,0,0);
    if(hànhĐộng==4)return cổngUDPCôngCụ(thẻXửLýTệp);
    if(hànhĐộng==5)return (uint32_t)gọiThựcHiện(40,thẻXửLýTệp,0,0);
    return (uint32_t)-22;
}
từMáy giaoDiệnĐồHọaCôngCụ(từMáy hànhĐộng,từMáy giáTrịĐịnhDanh,từMáy giáTrịĐầuTiên,từMáy giáTrịThứHai,từMáy mãKýTự,từMáy dữLiệuĐích){return (uint32_t)gọiThựcHiệnNgườiDùng(20,hànhĐộng,giáTrịĐịnhDanh,giáTrịĐầuTiên,giáTrịThứHai,mãKýTự,dữLiệuĐích);}
từMáy vănBảnGiaoDiệnĐồHọaCôngCụ(từMáy giáTrịĐịnhDanh,từMáy giáTrịMảng,từMáy sốLượngPhầnMục){
    const từMáy *địaChỉNguyênBản=(const từMáy *)giáTrịMảng;uint32_t DữLiệu[127];unsigned sốLượngMục=0;
    if(sốLượngPhầnMục>địaChỉNguyênBản[0])return (uint32_t)-22;
    for(từMáy chỉSốThứBậc=0;chỉSốThứBậc<sốLượngPhầnMục;chỉSốThứBậc++){unsigned mãHóaKýTự=địaChỉNguyênBản[chỉSốThứBậc+1];if(mãHóaKýTự>=0xd800&&mãHóaKýTự<=0xdbff&&chỉSốThứBậc+1<sốLượngPhầnMục){unsigned giáTrịThấp=địaChỉNguyênBản[++chỉSốThứBậc+1];if(giáTrịThấp<0xdc00||giáTrịThấp>0xdfff)return (uint32_t)-22;mãHóaKýTự=0x10000+((mãHóaKýTự-0xd800)<<10)+giáTrịThấp-0xdc00;}if(sốLượngMục==127)return (uint32_t)-22;DữLiệu[sốLượngMục++]=mãHóaKýTự;}
    return (uint32_t)gọiThựcHiệnNgườiDùng(21,giáTrịĐịnhDanh,(từMáy)DữLiệu,sốLượngMục,0,0,0);
}
