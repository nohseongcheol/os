// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Quản lý cắt vùng vẽ, ghép các dải và nền dưới con trỏ. Mã bo mạch đảm nhiệm truy cập bộ nhớ màn hình thực. */
public final class BộGhépBộĐệmKhung {
    static int giáTrịRộng, giáTrịCao, làĐangGhép, giáTrịRanhGiớiTrái, ranhGiớiThượng, giáTrịRanhGiớiPhải, giáTrịRanhGiớiHạ;
    static int xConTrỏ, yConTrỏ, hìnhConTrỏ;
    static int thấpBộĐếm, caoTrênBộĐếm;
    static int[] cácĐiểmẢnhĐãGhép = new int[32 * 1920];
    static int[] nềnConTrỏ = new int[21 * 21];
    static int[] cácCậnĐãCắtXén = new int[4];
    public static void chuẩnBị(int khoảngTrảiRộng, int độDài) {
        giáTrịRộng = khoảngTrảiRộng; giáTrịCao = độDài; làĐangGhép = 0; hìnhConTrỏ = 0;
        thấpBộĐếm = 0; caoTrênBộĐếm = 0;
    }
    public static int lấyRộng() { return giáTrịRộng; }
    public static int lấyCao() { return giáTrịCao; }
    public static int lấyThấpBộĐếm() { return thấpBộĐếm; }
    public static int lấyCaoTrênBộĐếm() { return caoTrênBộĐếm; }
    public static int giáTrịCắtXén(int chỉSốThứBậc) { return cácCậnĐãCắtXén[chỉSốThứBậc]; }
    static int thêmĐộDàiDương(int bắtChạyGiáTrị, int độDài) {
        if (bắtChạyGiáTrị > 2147483647 - độDài) return 2147483647;
        return bắtChạyGiáTrị + độDài;
    }
    public static int cắtXén(int vịTríNgang, int vịTríDọc, int khoảngTrảiRộng, int độDài) {
        if (giáTrịRộng == 0 || khoảngTrảiRộng <= 0 || độDài <= 0) return 0;
        int phải = thêmĐộDàiDương(vịTríNgang, khoảngTrảiRộng), bênHạ = thêmĐộDàiDương(vịTríDọc, độDài);
        int bênTrái = làĐangGhép != 0 ? giáTrịRanhGiớiTrái : 0, bênThượng = làĐangGhép != 0 ? ranhGiớiThượng : 0;
        int vịTríNgangTốiĐa = làĐangGhép != 0 ? giáTrịRanhGiớiPhải : giáTrịRộng, vịTríDọcTốiĐa = làĐangGhép != 0 ? giáTrịRanhGiớiHạ : giáTrịCao;
        if (vịTríNgang < bênTrái) vịTríNgang = bênTrái;
        if (vịTríDọc < bênThượng) vịTríDọc = bênThượng;
        if (phải > vịTríNgangTốiĐa) phải = vịTríNgangTốiĐa;
        if (bênHạ > vịTríDọcTốiĐa) bênHạ = vịTríDọcTốiĐa;
        if (phải <= vịTríNgang || bênHạ <= vịTríDọc) return 0;
        cácCậnĐãCắtXén[0] = vịTríNgang; cácCậnĐãCắtXén[1] = vịTríDọc;
        cácCậnĐãCắtXén[2] = phải - vịTríNgang; cácCậnĐãCắtXén[3] = bênHạ - vịTríDọc;
        return 1;
    }
    public static int chạy(int vịTríNgang, int vịTríDọc, int khoảngTrảiRộng, int độDài) {
        if (làĐangGhép != 0 || độDài > 32 || cắtXén(vịTríNgang, vịTríDọc, khoảngTrảiRộng, độDài) == 0) return 0;
        giáTrịRanhGiớiTrái = cácCậnĐãCắtXén[0]; ranhGiớiThượng = cácCậnĐãCắtXén[1];
        giáTrịRanhGiớiPhải = giáTrịRanhGiớiTrái + cácCậnĐãCắtXén[2]; giáTrịRanhGiớiHạ = ranhGiớiThượng + cácCậnĐãCắtXén[3];
        làĐangGhép = 1; return 1;
    }
    static boolean bitConTrỏ(int vịTríNgang, int vịTríDọc, int giáTrịHình) {
        if (giáTrịHình == 1) return vịTríNgang >= 0 && vịTríNgang <= vịTríDọc / 2 && vịTríDọc < 16;
        if (giáTrịHình == 3) vịTríNgang = 20 - vịTríNgang;
        int giáTrịKhácBiệt = vịTríNgang - vịTríDọc; if (giáTrịKhácBiệt < 0) giáTrịKhácBiệt = -giáTrịKhácBiệt;
        return (giáTrịKhácBiệt <= 1 && vịTríNgang >= 3 && vịTríNgang <= 17) ||
            (vịTríNgang >= 2 && vịTríNgang <= 8 && vịTríDọc >= 2 && vịTríDọc <= 8 && (vịTríNgang <= 3 || vịTríDọc <= 3)) ||
            (vịTríNgang >= 12 && vịTríNgang <= 18 && vịTríDọc >= 12 && vịTríDọc <= 18 && (vịTríNgang >= 17 || vịTríDọc >= 17));
    }
    static int điểmẢnhConTrỏ(int vịTríNgang, int vịTríDọc) {
        if (bitConTrỏ(vịTríNgang, vịTríDọc, hìnhConTrỏ)) return 2;
        for (int dòng = -1; dòng <= 1; dòng++) for (int mụcÔ = -1; mụcÔ <= 1; mụcÔ++)
            if (bitConTrỏ(vịTríNgang + mụcÔ, vịTríDọc + dòng, hìnhConTrỏ)) return 1;
        return 0;
    }
    static void điểmẢnhHiểnThị(int vịTríNgang, int vịTríDọc, int giáTrịMàu) {
        int mụcÔ = vịTríNgang - xConTrỏ, dòng = vịTríDọc - yConTrỏ;
        if (hìnhConTrỏ != 0 && mụcÔ >= 0 && dòng >= 0 && mụcÔ < 21 && dòng < 21) {
            nềnConTrỏ[dòng * 21 + mụcÔ] = giáTrịMàu;
            int giáTrịĐiểm = điểmẢnhConTrỏ(mụcÔ, dòng); if (giáTrịĐiểm != 0) giáTrịMàu = giáTrịĐiểm == 2 ? 0xffffff : 0x101010;
        }
        if (BoMạch.đọcĐiểmẢnhHiểnThị(vịTríNgang, vịTríDọc) != giáTrịMàu) {
            BoMạch.ghiĐiểmẢnhHiểnThị(vịTríNgang, vịTríDọc, giáTrịMàu);
            thấpBộĐếm++; if (thấpBộĐếm == 0) caoTrênBộĐếm++;
        }
    }
    public static void hoànThành() {
        if (làĐangGhép == 0) return;
        for (int dòng = ranhGiớiThượng; dòng < giáTrịRanhGiớiHạ; dòng++) for (int mụcÔ = giáTrịRanhGiớiTrái; mụcÔ < giáTrịRanhGiớiPhải; mụcÔ++)
            điểmẢnhHiểnThị(mụcÔ, dòng, cácĐiểmẢnhĐãGhép[(dòng - ranhGiớiThượng) * 1920 + mụcÔ]);
        làĐangGhép = 0;
    }
    public static int điểmẢnh(int vịTríNgang, int vịTríDọc, int giáTrịMàu) {
        if (vịTríNgang < 0 || vịTríDọc < 0 || vịTríNgang >= giáTrịRộng || vịTríDọc >= giáTrịCao) return 0;
        if (làĐangGhép != 0) {
            if (vịTríNgang >= giáTrịRanhGiớiTrái && vịTríNgang < giáTrịRanhGiớiPhải && vịTríDọc >= ranhGiớiThượng && vịTríDọc < giáTrịRanhGiớiHạ)
                cácĐiểmẢnhĐãGhép[(vịTríDọc - ranhGiớiThượng) * 1920 + vịTríNgang] = giáTrịMàu;
        } else điểmẢnhHiểnThị(vịTríNgang, vịTríDọc, giáTrịMàu);
        return 0;
    }
    public static void lấpHìnhChữNhật(int vịTríNgang, int vịTríDọc, int khoảngTrảiRộng, int độDài, int giáTrịMàu) {
        if (cắtXén(vịTríNgang, vịTríDọc, khoảngTrảiRộng, độDài) == 0) return;
        vịTríNgang = cácCậnĐãCắtXén[0]; vịTríDọc = cácCậnĐãCắtXén[1]; khoảngTrảiRộng = cácCậnĐãCắtXén[2]; độDài = cácCậnĐãCắtXén[3];
        for (int dòng = vịTríDọc; dòng < vịTríDọc + độDài; dòng++) for (int mụcÔ = vịTríNgang; mụcÔ < vịTríNgang + khoảngTrảiRộng; mụcÔ++) {
            if (làĐangGhép != 0) cácĐiểmẢnhĐãGhép[(dòng - ranhGiớiThượng) * 1920 + mụcÔ] = giáTrịMàu;
            else điểmẢnhHiểnThị(mụcÔ, dòng, giáTrịMàu);
        }
    }
    public static void conTrỏ(int vịTríNgang, int vịTríDọc, int giáTrịHình) {
        if (giáTrịRộng == 0) return;
        int vịTríNgangMới = vịTríNgang - (giáTrịHình >= 2 ? 10 : 0), vịTríDọcMới = vịTríDọc - (giáTrịHình >= 2 ? 10 : 0);
        if (hìnhConTrỏ == giáTrịHình && xConTrỏ == vịTríNgangMới && yConTrỏ == vịTríDọcMới) return;
        if (hìnhConTrỏ != 0) for (int dòng = 0; dòng < 21; dòng++) for (int mụcÔ = 0; mụcÔ < 21; mụcÔ++) {
            int toánHạngĐầuTiên = xConTrỏ + mụcÔ, giáTrịBa = yConTrỏ + dòng;
            if (toánHạngĐầuTiên >= 0 && giáTrịBa >= 0 && toánHạngĐầuTiên < giáTrịRộng && giáTrịBa < giáTrịCao) BoMạch.ghiĐiểmẢnhHiểnThị(toánHạngĐầuTiên, giáTrịBa, nềnConTrỏ[dòng * 21 + mụcÔ]);
        }
        hìnhConTrỏ = giáTrịHình; xConTrỏ = vịTríNgangMới; yConTrỏ = vịTríDọcMới;
        if (giáTrịHình != 0) for (int dòng = 0; dòng < 21; dòng++) for (int mụcÔ = 0; mụcÔ < 21; mụcÔ++) {
            int toánHạngĐầuTiên = xConTrỏ + mụcÔ, giáTrịBa = yConTrỏ + dòng;
            if (toánHạngĐầuTiên >= 0 && giáTrịBa >= 0 && toánHạngĐầuTiên < giáTrịRộng && giáTrịBa < giáTrịCao) {
                nềnConTrỏ[dòng * 21 + mụcÔ] = BoMạch.đọcĐiểmẢnhHiểnThị(toánHạngĐầuTiên, giáTrịBa);
                int giáTrịĐiểm = điểmẢnhConTrỏ(mụcÔ, dòng); if (giáTrịĐiểm != 0) BoMạch.ghiĐiểmẢnhHiểnThị(toánHạngĐầuTiên, giáTrịBa, giáTrịĐiểm == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
