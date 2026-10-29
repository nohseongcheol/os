// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** Gọi bộ xử lý giao thức Java thực trong JVM để kiểm tra nhanh giới hạn và đầu vào hỏng. */
public final class ThửGóiTin {
    static int sốLượngSựLặp = 0;
    static void xácMinh(boolean giáTrị) { if (!giáTrị) throw new AssertionError("case " + sốLượngSựLặp); sốLượngSựLặp++; }
    static int tổngKiểm(int[] giáTrị, int chạy, int độDài, int trạngTháiBanĐầu) {
        int giáTrịTổng = trạngTháiBanĐầu;
        for (int sốHiệu = 0; sốHiệu < độDài; sốHiệu++) giáTrịTổng += giáTrị[chạy + sốHiệu] << ((sốHiệu & 1) == 0 ? 8 : 0);
        giáTrịTổng = (giáTrịTổng & 65535) + (giáTrịTổng >>> 16);
        giáTrịTổng = (giáTrịTổng & 65535) + (giáTrịTổng >>> 16);
        return ~giáTrịTổng & 65535;
    }
    static void chuẩnBị(int độDài) {
        NgănXếpMạng.tiếnTrìnhSạch();
        xácMinh(NgănXếpMạng.mở(5000) == 3);
        int[] chỉSốKhung = NgănXếpMạng.khungĐầuVào;
        Arrays.fill(chỉSốKhung, 0);
        for (int sốHiệu = 0; sốHiệu < 6; sốHiệu++) chỉSốKhung[sốHiệu] = TrìnhĐiềuKhiểnMạng.địaChỉThiếtBị[sốHiệu];
        NgănXếpMạng.đặt16Bit(chỉSốKhung, 12, 0x0800);
        chỉSốKhung[14] = 0x45; chỉSốKhung[22] = 64; chỉSốKhung[23] = 17;
        NgănXếpMạng.đặt16Bit(chỉSốKhung, 16, 28 + độDài);
        NgănXếpMạng.đặt32Bit(chỉSốKhung, 26, 0x0a000202); NgănXếpMạng.đặt32Bit(chỉSốKhung, 30, NgănXếpMạng.địaChỉTựCó);
        NgănXếpMạng.đặt16Bit(chỉSốKhung, 34, 4321); NgănXếpMạng.đặt16Bit(chỉSốKhung, 36, 5000); NgănXếpMạng.đặt16Bit(chỉSốKhung, 38, độDài + 8);
        for (int sốHiệu = 0; sốHiệu < độDài; sốHiệu++) chỉSốKhung[42 + sốHiệu] = sốHiệu & 255;
        đặtGiáTrịTổngKiểm(độDài);
    }
    static void đặtGiáTrịTổngKiểm(int độDài) {
        int[] chỉSốKhung = NgănXếpMạng.khungĐầuVào;
        NgănXếpMạng.đặt16Bit(chỉSốKhung, 24, 0); NgănXếpMạng.đặt16Bit(chỉSốKhung, 40, 0);
        NgănXếpMạng.đặt16Bit(chỉSốKhung, 24, tổngKiểm(chỉSốKhung, 14, 20, 0));
        int trạngTháiBanĐầu = NgănXếpMạng.tổngKiểmĐầuMụcMôPhỏng(NgănXếpMạng.nguyên32(chỉSốKhung, 26), NgănXếpMạng.địaChỉTựCó, độDài + 8);
        int giáTrịTổng = tổngKiểm(chỉSốKhung, 34, độDài + 8, trạngTháiBanĐầu);
        NgănXếpMạng.đặt16Bit(chỉSốKhung, 40, giáTrịTổng == 0 ? 65535 : giáTrịTổng);
    }
    static void từChốiGiáTrị(int độDài) { NgănXếpMạng.khungTiếnTrình(độDài); xácMinh(NgănXếpMạng.độDàiĐãNhận[0] == -1); }
    public static void main(String[] cácĐốiSố) {
        for (int độDài : new int[]{0, 1, 2, 7, 1023, 1024}) {
            chuẩnBị(độDài); NgănXếpMạng.khungTiếnTrình(độDài + 42);
            xácMinh(NgănXếpMạng.độDàiĐãNhận[0] == độDài);
            xácMinh(NgănXếpMạng.địaChỉĐãNhận[0] == 0x0a000202 && NgănXếpMạng.sốCổngĐãNhận[0] == 4321);
            for (int sốHiệu = 0; sốHiệu < độDài; sốHiệu++) xácMinh(NgănXếpMạng.dữLiệuĐãNhận[sốHiệu] == (sốHiệu & 255));
        }
        for (int độDài = 0; độDài < 42; độDài++) { chuẩnBị(0); từChốiGiáTrị(độDài); }
        chuẩnBị(1025); từChốiGiáTrị(1067);
        chuẩnBị(2); NgănXếpMạng.khungĐầuVào[24] ^= 1; từChốiGiáTrị(44);
        chuẩnBị(2); NgănXếpMạng.khungĐầuVào[42] ^= 1; từChốiGiáTrị(44);
        chuẩnBị(2); NgănXếpMạng.đặt16Bit(NgănXếpMạng.khungĐầuVào, 38, 7); từChốiGiáTrị(44);
        chuẩnBị(2); NgănXếpMạng.đặt16Bit(NgănXếpMạng.khungĐầuVào, 38, 65535); từChốiGiáTrị(44);
        chuẩnBị(2); NgănXếpMạng.khungĐầuVào[14] = 0x4f; từChốiGiáTrị(44);
        chuẩnBị(2); NgănXếpMạng.khungĐầuVào[14] = 0x44; từChốiGiáTrị(44);
        chuẩnBị(2); NgănXếpMạng.khungĐầuVào[20] = 0x20; đặtGiáTrịTổngKiểm(2); từChốiGiáTrị(44);
        chuẩnBị(2); NgănXếpMạng.khungĐầuVào[21] = 1; đặtGiáTrịTổngKiểm(2); từChốiGiáTrị(44);
        chuẩnBị(2); NgănXếpMạng.khungĐầuVào[33] = 99; đặtGiáTrịTổngKiểm(2); từChốiGiáTrị(44);
        chuẩnBị(2); NgănXếpMạng.khungĐầuVào[0] ^= 1; từChốiGiáTrị(44);
        chuẩnBị(2); NgănXếpMạng.khungĐầuVào[23] = 6; đặtGiáTrịTổngKiểm(2); từChốiGiáTrị(44);
        chuẩnBị(2); NgănXếpMạng.đặt16Bit(NgănXếpMạng.khungĐầuVào, 40, 0); NgănXếpMạng.khungTiếnTrình(44); xácMinh(NgănXếpMạng.độDàiĐãNhận[0] == 2);
        int[] kếtQuả = new int[4];
        xácMinh(NgănXếpMạng.nhận(3, kếtQuả, 1, 0) == -90);
        xácMinh(NgănXếpMạng.nhận(3, kếtQuả, 4, 0) == -11);
        chuẩnBị(2); NgănXếpMạng.khungTiếnTrình(44); int loạiBỏGiáTrị = NgănXếpMạng.sốLượngĐãLoạiBỏ;
        NgănXếpMạng.khungTiếnTrình(44); xácMinh(NgănXếpMạng.sốLượngĐãLoạiBỏ == loạiBỏGiáTrị + 1);
        NgănXếpMạng.tiếnTrìnhSạch(); xácMinh(NgănXếpMạng.mở(5000) == 3);
        xácMinh(NgănXếpMạng.mở(5000) == -98); xácMinh(NgănXếpMạng.mở(0) == 4);
        xácMinh(NgănXếpMạng.mở(0) == 5); xácMinh(NgănXếpMạng.mở(0) == 6); xácMinh(NgănXếpMạng.mở(0) == -24);
        xácMinh(NgănXếpMạng.đóng(4) == 0); xácMinh(NgănXếpMạng.đóng(4) == -9);
        NgănXếpMạng.địaChỉĐãTìmThấy = NgănXếpMạng.giáTrịCổngNối;
        xácMinh(NgănXếpMạng.gửi(3, NgănXếpMạng.giáTrịCổngNối, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] cóĐãGửi = TrìnhĐiềuKhiểnMạng.giáTrịGầnĐây;
        xácMinh(tổngKiểm(cóĐãGửi, 14, 20, 0) == 0);
        xácMinh(tổngKiểm(cóĐãGửi, 34, 11, NgănXếpMạng.tổngKiểmĐầuMụcMôPhỏng(NgănXếpMạng.địaChỉTựCó, NgănXếpMạng.giáTrịCổngNối, 11)) == 0);
        xácMinh(cóĐãGửi[42] == 1 && cóĐãGửi[44] == 3);
        System.out.println("PACKET TEST PASS: " + sốLượngSựLặp + " assertions");
    }
}
