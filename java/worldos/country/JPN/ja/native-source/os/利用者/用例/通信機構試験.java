// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 通信機構試験 {
    public static int 起動処理() {
        int 先頭位置序数 = 利用者.通信網開放(45000);
        if (先頭位置序数 < 0) { 利用者.書込("NETWORK UNAVAILABLE\n"); return 3; }
        int[] データ = new int[8];
        boolean 通過値 = 利用者.通信網開放(45000) == -98
            && 利用者.データ受取(先頭位置序数, データ, 0) == -11
            && 利用者.データ受取(先頭位置序数, データ, 50) == -110
            && 利用者.データ受取(先頭位置序数, データ, 3000) == -22
            && 利用者.データ送信(先頭位置序数, 0x0a000202, 9, データ, 9) == -90
            && 利用者.データ受取(先頭位置序数, null, 0) == -14
            && 利用者.通信網閉鎖(先頭位置序数) == 0 && 利用者.通信網閉鎖(先頭位置序数) == -9;
        利用者.書込(通過値 ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return 通過値 ? 0 : 1;
    }
}
