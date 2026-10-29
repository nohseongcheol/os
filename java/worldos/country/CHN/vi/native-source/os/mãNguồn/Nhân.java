// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Điểm vào Java được gọi sau khi khởi động thực; không phụ thuộc JVM hay hệ điều hành máy chủ. */
public final class Nhân {
    static int giáTrịTổngCộng(int phầnKết) {
        int giáTrịTổng = 0;
        for (int sốHiệu = 1; sốHiệu <= phầnKết; sốHiệu++) giáTrịTổng += sốHiệu;
        return giáTrịTổng;
    }

    static boolean KiểmThử() {
        int[] cácGiáTrị = new int[4];
        cácGiáTrị[2] = giáTrịTổngCộng(10);
        int giáTrịÂm = -7;
        int giáTrịTốiThiểu = 0x80000000;
        int kếtQuảPhépChia = -1;
        int sốHiệu = VùngNhớ.cấpPhátLưuTrữ();
        boolean giáTrịQua = cácGiáTrị[0] == 0 && cácGiáTrị[2] == 55 && cácGiáTrị.length == 4
            && giáTrịÂm / 3 == -2 && giáTrịÂm % 3 == -1 && giáTrịTốiThiểu / kếtQuảPhépChia == giáTrịTốiThiểu
            && giáTrịTốiThiểu % kếtQuảPhépChia == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && sốHiệu >= 0 && VùngNhớ.kếtQuảTrảVề(sốHiệu) && !VùngNhớ.kếtQuảTrảVề(sốHiệu);
        ĐầuCuốiVănBản.ghi(giáTrịQua ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return giáTrịQua;
    }

    public static void chạy() {
        ĐầuCuốiVănBản.chuẩnBị();
        ĐầuCuốiVănBản.ghi("JKOROS NATIVE JAVA\n");
        ĐầuCuốiVănBản.ghi("Java 기계어 giáTrịNhân chạy\n");
        if (ThiếtBị.dấuMốcKhởiĐộng() != 0x2badb002) {
            ĐầuCuốiVănBản.ghi("BAD MULTIBOOT MAGIC\n");
            ThiếtBị.việcThựcThiDừngHẳn();
        }
        if (!KiểmThử()) ThiếtBị.việcThựcThiDừngHẳn();
        if (VùngNhớ.cỡBộNhớThượng() < 15360) {
            ĐầuCuốiVănBản.ghi("At least 16 MiB RAM required\n");
            ThiếtBị.việcThựcThiDừngHẳn();
        }
        ThiếtBị.chuẩnBịChươngTrìnhNgườiDùng();
        ĐầuCuốiVănBản.ghi("USER ELF: ring 3 / paging / int 0x80\n");
        TrìnhĐiềuKhiểnMạng.chuẩnBị();
        NgănXếpMạng.tiếnTrìnhSạch();
        HệTệpBộNhớ.chuẩnBị();
        LưuGiữTệp.chuẩnBị();
        TrìnhThôngDịchLệnh.chạy();
    }
}
