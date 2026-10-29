#include "ABITệp.h"
#include "gọiThựcHiện.h"
static int giáTrịBộKhởiTạo;
static volatile int hạtGiốngBộKhởiTạo = 72;
static volatile double hạtGiốngĐiểmDấuPhẩyĐộng = 1.25;
static int sốLượngViệcHủy;
struct thửViệcKhởiTạo { thửViệcKhởiTạo() { giáTrịBộKhởiTạo = hạtGiốngBộKhởiTạo + 1; } } khởiTạoCácThànhPhầnTĩnh;
class tệpTựĐộngHóa {
    int sốHiệu;
public:
    explicit tệpTựĐộngHóa(const char *tên) : sốHiệu(mởTệp(tên, GhiĐọc | ThiếuNếuTạo | CácNộiDungCắtNgắn, 0600)) {}
    ~tệpTựĐộngHóa() { if (sốHiệu >= 0) đóngTệp(sốHiệu); sốLượngViệcHủy++; }
    int mụcBộMôTả() const { return sốHiệu; }
};
extern "C" int bắtChạyChươngTrìnhNgườiDùng(int) {
    if (giáTrịBộKhởiTạo != 73 || gọiThựcHiệnNgườiDùng(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double giáTrịĐiểmDấuPhẩyĐộng = hạtGiốngĐiểmDấuPhẩyĐộng * 2.0 + 0.5;
    if (gọiThựcHiệnNgườiDùng(0, 0, 0, 0, 0, 0, 0) != 1 || giáTrịĐiểmDấuPhẩyĐộng != 3.0) return 16;
    static const char giáTrịNộiDung[] = "EL0 C++ → posix-kor → Java Tệp · 안녕하세요 😀\n";
    char đọcGiáTrị[sizeof(giáTrịNộiDung)] = {};
    {
        tệpTựĐộngHóa Tệp("NgườiDùng.txt");
        int sốHiệu = Tệp.mụcBộMôTả();
        if (sốHiệu < 0 || ghiDữLiệuTệp(sốHiệu, giáTrịNộiDung, sizeof(giáTrịNộiDung)) != sizeof(giáTrịNộiDung)) return 2;
        if (dịchVịTệp(sốHiệu, 0, PhầnĐầuTừ) || đọcDữLiệuTệp(sốHiệu, đọcGiáTrị, sizeof(đọcGiáTrị)) != sizeof(đọcGiáTrị)) return 3;
        for (unsigned chỉSốThứBậc = 0; chỉSốThứBậc < sizeof(giáTrịNộiDung); chỉSốThứBậc++) if (đọcGiáTrị[chỉSốThứBậc] != giáTrịNộiDung[chỉSốThứBậc]) return 4;
    }
    if (sốLượngViệcHủy != 1) return 5;
    if (ghiDữLiệuTệp(1, giáTrịNộiDung, sizeof(giáTrịNộiDung) - 1) != sizeof(giáTrịNộiDung) - 1) return 6;
    uintptr_t mụcĐáy = kếtThúcBộNhớNgườiDùng(0);
    if (mụcĐáy != 0x02c00000 || kếtThúcBộNhớNgườiDùng(mụcĐáy + 8192) != (intptr_t)(mụcĐáy + 8192)) return 7;
    volatile unsigned char *BộNhớ = (volatile unsigned char *)mụcĐáy;
    if (BộNhớ[0] || BộNhớ[8191]) return 8;
    BộNhớ[8191] = 137;
    if (kếtThúcBộNhớNgườiDùng(mụcĐáy) != (intptr_t)mụcĐáy || kếtThúcBộNhớNgườiDùng(mụcĐáy + 8192) != (intptr_t)(mụcĐáy + 8192) || BộNhớ[8191]) return 9;
    // 잘못된 NgườiDùng conTrỏ/번호는 오류이며 커널을 중단하지 않는다.
    if (ghiDữLiệuTệp(1, (const void *)0x80000, 8) != -1 || sốLỗi != 14) return 10;
    if (đọcDữLiệuTệp(0, (void *)giáTrịNộiDung, 1) != -1 || sốLỗi != 14) return 11;
    if (gọiThựcHiệnNgườiDùng(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t khoảngTrảiMànHình = đọcRộngMànHình(), độDàiMànHình = đọcCaoMànHình();
    if (khoảngTrảiMànHình <= 0 || độDàiMànHình <= 0 || gọiThựcHiệnNgườiDùng(13, khoảngTrảiMànHình-1, độDàiMànHình-1, 0, 2, 2, 0) != -22) return 13;
    if (hìnhChữNhậtMànHình(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 chươngTrìnhRa 시 열린 서술자가 자동 정리되어야 한다.
    if (mởTệp("NgườiDùng.txt", đọcGiáTrịChỉ) < 0) return 15;
    return 0;
}
