// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class thửKếtNốiMạng {
    public static int chạy() {
        int thứBậcĐầuTiên = NgườiDùng.mởMạng(45000);
        if (thứBậcĐầuTiên < 0) { NgườiDùng.ghi("NETWORK UNAVAILABLE\n"); return 3; }
        int[] DữLiệu = new int[8];
        boolean giáTrịQua = NgườiDùng.mởMạng(45000) == -98
            && NgườiDùng.nhậnDữLiệu(thứBậcĐầuTiên, DữLiệu, 0) == -11
            && NgườiDùng.nhậnDữLiệu(thứBậcĐầuTiên, DữLiệu, 50) == -110
            && NgườiDùng.nhậnDữLiệu(thứBậcĐầuTiên, DữLiệu, 3000) == -22
            && NgườiDùng.gửiDữLiệu(thứBậcĐầuTiên, 0x0a000202, 9, DữLiệu, 9) == -90
            && NgườiDùng.nhậnDữLiệu(thứBậcĐầuTiên, null, 0) == -14
            && NgườiDùng.đóngMạng(thứBậcĐầuTiên) == 0 && NgườiDùng.đóngMạng(thứBậcĐầuTiên) == -9;
        NgườiDùng.ghi(giáTrịQua ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return giáTrịQua ? 0 : 1;
    }
}
