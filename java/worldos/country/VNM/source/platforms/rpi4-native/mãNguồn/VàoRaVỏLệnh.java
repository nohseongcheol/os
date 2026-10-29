// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Các ống thực thi tuần tự từng khối 16 KiB. Không mô phỏng tiến trình hay đường ống đồng thời. */
public final class VàoRaVỏLệnh {
    static int[] dữLiệuĐầuVào = new int[16384], dữLiệuĐầuRa = new int[16384];
    static int độDàiĐầuVào, vịTríĐầuVào, độDàiĐầuRa, tệpĐầuVào = -1, tệpĐầuRa = -1;
    static boolean đầuVàoỐngDẫn, đầuRaỐngDẫn;
    static int giáTrịSựThấtBại;
    static boolean choPhépTươngTác = true;
    public static int làTươngTác() { return choPhépTươngTác && tệpĐầuVào < 3 && tệpĐầuRa < 3 && !đầuVàoỐngDẫn && !đầuRaỐngDẫn ? 1 : 0; }
    public static int ĐầuRa(int giáTrịKênh, int giáTrị) {
        if (giáTrịKênh != 1) return 0;
        if (tệpĐầuRa >= 3) { int giáTrịĐãXửLý = CácTệpBộNhớ.ghi(tệpĐầuRa, giáTrị); if (giáTrịĐãXửLý < 0) giáTrịSựThấtBại = giáTrịĐãXửLý; return 1; }
        if (!đầuRaỐngDẫn) return 0;
        if (độDàiĐầuRa == dữLiệuĐầuRa.length) giáTrịSựThấtBại = -28;
        else dữLiệuĐầuRa[độDàiĐầuRa++] = giáTrị;
        return 1;
    }
    public static int giáTrịVào() {
        if (tệpĐầuVào >= 3) { int giáTrịĐãXửLý = CácTệpBộNhớ.đọc(tệpĐầuVào); return giáTrịĐãXửLý == 256 ? -2 : giáTrịĐãXửLý; }
        if (đầuVàoỐngDẫn) return vịTríĐầuVào < độDàiĐầuVào ? dữLiệuĐầuVào[vịTríĐầuVào++] : -2;
        return -3; // Chuyển tới UART.
    }
    static void chạy(boolean ốngDẫnDẫnĐầu, boolean ốngDẫnỞCuối) {
        đầuVàoỐngDẫn = ốngDẫnDẫnĐầu; đầuRaỐngDẫn = ốngDẫnỞCuối;
        vịTríĐầuVào = 0; độDàiĐầuRa = 0; tệpĐầuVào = -1; tệpĐầuRa = -1; giáTrịSựThấtBại = 0;
    }
    static void phầnKết() {
        BoMạch.vàoRaChuyển(0);
        if (tệpĐầuVào >= 3) CácTệpBộNhớ.đóng(tệpĐầuVào);
        if (tệpĐầuRa >= 3) CácTệpBộNhớ.đóng(tệpĐầuRa);
        if (đầuRaỐngDẫn) { độDàiĐầuVào = độDàiĐầuRa; for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < độDàiĐầuRa; chỉSốVòngLặp++) dữLiệuĐầuVào[chỉSốVòngLặp] = dữLiệuĐầuRa[chỉSốVòngLặp]; }
        tệpĐầuVào = -1; tệpĐầuRa = -1; đầuVàoỐngDẫn = false; đầuRaỐngDẫn = false;
    }
}
