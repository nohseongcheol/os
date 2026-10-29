#include "../cáchĐặtTên/cácTênLiênKếtMáy.h"
#include "ABITệp.h"
// 표준 C++ thưViện 없는 freestanding C++11 ChươngTrình. 커널에 giáTrịTĩnh 링크한다.
extern "C" uintptr_t thửCácChươngTrìnhCộngCộng(void) {
    const char giáTrịNộiDung[] = "C++ → Java giáTrịNhân · 한글 😀";
    unsigned char đọcGiáTrị[sizeof(giáTrịNộiDung)] = {};
    int Tệp = mởTệp("KiểmThử.txt", GhiĐọc | ThiếuNếuTạo | CácNộiDungCắtNgắn, 0600);
    if (Tệp < 0) return 1;
    if (ghiDữLiệuTệp(Tệp, giáTrịNộiDung, sizeof(giáTrịNộiDung)) != sizeof(giáTrịNộiDung)) return 2;
    if (dịchVịTệp(Tệp, 0, PhầnĐầuTừ) != 0) return 3;
    if (đọcDữLiệuTệp(Tệp, đọcGiáTrị, sizeof(đọcGiáTrị)) != sizeof(đọcGiáTrị)) return 4;
    for (size_t chỉSốThứBậc = 0; chỉSốThứBậc < sizeof(giáTrịNộiDung); chỉSốThứBậc++) if (đọcGiáTrị[chỉSốThứBậc] != (unsigned char)giáTrịNộiDung[chỉSốThứBậc]) return 5;
    if (đọcDữLiệuTệp(Tệp, đọcGiáTrị, 1) != 0) return 6;
    if (lưuTrữTệpChốt(Tệp) != -1 || sốLỗi != 38) return 7;
    if (đóngTệp(Tệp) || đóngTệp(Tệp) != -1 || sốLỗi != 9) return 8;
    Tệp = mởTệp("KiểmThử.txt", đọcGiáTrịChỉ);
    if (Tệp < 0 || ghiDữLiệuTệp(Tệp, giáTrịNộiDung, 1) != -1 || sốLỗi != 9) return 9;
    if (đóngTệp(Tệp)) return 10;
    Tệp = mởTệp("KiểmThử.txt", GhiĐọc | thêmCuốiKếtThúcTại);
    if (Tệp < 0 || dịchVịTệp(Tệp, 0, PhầnĐầuTừ) != 0 || ghiDữLiệuTệp(Tệp, "!", 1) != 1 || cỡTệp(Tệp) != sizeof(giáTrịNộiDung) + 1) return 11;
    if (đặtGiáTrịĐộDàiTệp(Tệp, 2) || dịchVịTệp(Tệp, 4, PhầnĐầuTừ) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (ghiDữLiệuTệp(Tệp, "x", 1) != 1 || cỡTệp(Tệp) != 3 || đóngTệp(Tệp)) return 13;
    Tệp = mởTệp("구멍.bin", GhiĐọc | ThiếuNếuTạo | CácNộiDungCắtNgắn, 0600);
    if (Tệp < 0 || dịchVịTệp(Tệp, 3, PhầnĐầuTừ) != 3 || ghiDữLiệuTệp(Tệp, "z", 1) != 1) return 14;
    if (dịchVịTệp(Tệp, 0, PhầnĐầuTừ) != 0 || đọcDữLiệuTệp(Tệp, đọcGiáTrị, 4) != 4 || đọcGiáTrị[0] || đọcGiáTrị[1] || đọcGiáTrị[2] || đọcGiáTrị[3] != 'z') return 15;
    if (gỡTênMụcTệp("구멍.bin") || cỡTệp(Tệp) != 4 || đóngTệp(Tệp)) return 16;
    if (mởTệp("구멍.bin", đọcGiáTrịChỉ) != -1 || sốLỗi != 2) return 17;
    if (mởTệp("KiểmThử.txt", GhiĐọc | tạoTệpMới, 0600) != -1 || sốLỗi != 17) return 18;
    if (mởTệp("../giáTrịCấm", đọcGiáTrịChỉ) != -1) return 19;
    return 0;
}
