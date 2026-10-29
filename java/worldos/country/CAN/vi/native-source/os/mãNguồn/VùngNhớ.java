// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Tra cứu thông tin khởi động và cấp phát, trả lại vùng tác vụ cố định 4 KiB; không phải bộ quản lý trang vật lý tổng quát. */
public final class VùngNhớ {
    static int[] giáTrịMụcĐoạn = new int[8192];
    static int[] giáTrịDùng = new int[8];

    static int phânTíchCúPhápSốNguyên(int địaChỉ) {
        return ThiếtBị.đọcBộNhớ(địaChỉ) | (ThiếtBị.đọcBộNhớ(địaChỉ + 1) << 8)
            | (ThiếtBị.đọcBộNhớ(địaChỉ + 2) << 16) | (ThiếtBị.đọcBộNhớ(địaChỉ + 3) << 24);
    }

    static int cỡBộNhớThượng() {
        int thôngTinHệThống = ThiếtBị.thôngTinKhởiĐộng();
        if (ThiếtBị.dấuMốcKhởiĐộng() != 0x2badb002 || thôngTinHệThống == 0 || (phânTíchCúPhápSốNguyên(thôngTinHệThống) & 1) == 0) return -1;
        return phânTíchCúPhápSốNguyên(thôngTinHệThống + 8);
    }

    static int cấpPhátLưuTrữ() {
        for (int sốHiệu = 0; sốHiệu < giáTrịDùng.length; sốHiệu++) {
            if (giáTrịDùng[sốHiệu] == 0) {
                giáTrịDùng[sốHiệu] = 1;
                for (int mụcÔ = 0; mụcÔ < 1024; mụcÔ++) giáTrịMụcĐoạn[sốHiệu * 1024 + mụcÔ] = 0;
                return sốHiệu;
            }
        }
        return -1;
    }

    static boolean kếtQuảTrảVề(int sốHiệu) {
        if (sốHiệu < 0 || sốHiệu >= giáTrịDùng.length || giáTrịDùng[sốHiệu] == 0) return false;
        giáTrịDùng[sốHiệu] = 0;
        return true;
    }

    static int sốLượngMụcĐãDùng() {
        int sốLượngPhầnMục = 0;
        for (int sốHiệu = 0; sốHiệu < giáTrịDùng.length; sốHiệu++) sốLượngPhầnMục += giáTrịDùng[sốHiệu];
        return sốLượngPhầnMục;
    }
}
