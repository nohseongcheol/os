// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Canada.JCanOS.ngắtXửLý;

import java.util.Arrays;

/** Đăng ký và phân phối bộ xử lý IDT ở phía được Java quản lý. */
public final class BộQuảnLýNgắtXửLý {
    private final BộXửLýNgắtXửLý[] danhSáchBộXửLý = new BộXửLýNgắtXửLý[256];
    private boolean hoạtĐộng;

    public void thanhGhiMục(int sốHiệu, BộXửLýNgắtXửLý BộXửLý) {
        xácMinhSố(sốHiệu);
        danhSáchBộXửLý[sốHiệu] = BộXửLý;
    }

    public void giảiPhóngLưuTrữ(int sốHiệu) {
        xácMinhSố(sốHiệu);
        danhSáchBộXửLý[sốHiệu] = null;
    }

    public int phânPhốiGiáTrị(int sốHiệu, int địaChỉNgănXếpĐãLưu) {
        xácMinhSố(sốHiệu);
        if (!hoạtĐộng) {
            return địaChỉNgănXếpĐãLưu;
        }
        BộXửLýNgắtXửLý BộXửLý = danhSáchBộXửLý[sốHiệu];
        return BộXửLý == null ? địaChỉNgănXếpĐãLưu : BộXửLý.mụcGiáTrịTiếnTrình(địaChỉNgănXếpĐãLưu);
    }

    public void bật() {
        hoạtĐộng = true;
    }

    public void ngừngKíchHoạt() {
        hoạtĐộng = false;
    }

    public boolean làHoạtĐộng() {
        return hoạtĐộng;
    }

    public void giảiPhóngTấtCả() {
        Arrays.fill(danhSáchBộXửLý, null);
    }

    private void xácMinhSố(int sốHiệu) {
        if (sốHiệu < 0 || sốHiệu >= danhSáchBộXửLý.length) {
            throw new IllegalArgumentException("ngắtXửLý 번호가 올바르지 않습니다.");
        }
    }
}

