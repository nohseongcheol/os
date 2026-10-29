// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 測試聯網 {
    public static int 運行() {
        int 首位序數 = 使用者.打開網路(45000);
        if (首位序數 < 0) { 使用者.寫入("NETWORK UNAVAILABLE\n"); return 3; }
        int[] 資料 = new int[8];
        boolean 通過值 = 使用者.打開網路(45000) == -98
            && 使用者.接收資料(首位序數, 資料, 0) == -11
            && 使用者.接收資料(首位序數, 資料, 50) == -110
            && 使用者.接收資料(首位序數, 資料, 3000) == -22
            && 使用者.發送資料(首位序數, 0x0a000202, 9, 資料, 9) == -90
            && 使用者.接收資料(首位序數, null, 0) == -14
            && 使用者.關閉網路(首位序數) == 0 && 使用者.關閉網路(首位序數) == -9;
        使用者.寫入(通過值 ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return 通過值 ? 0 : 1;
    }
}
