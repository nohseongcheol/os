// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 計算結果 {
    static int 總計值(int 結尾) {
        int 結果 = 0;
        for (int 編號 = 1; 編號 <= 結尾; 編號++) 結果 += 編號;
        return 結果;
    }

    public static int 運行() {
        int[] 值列 = new int[3];
        值列[0] = 總計值(10);
        值列[1] = -7 / 3;
        值列[2] = "한글".length();
        return 值列[0] == 55 && 值列[1] == -2 && 值列[2] == 2 ? 0 : 1;
    }
}
