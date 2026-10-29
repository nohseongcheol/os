// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 계산 {
    static int 합계(int 끝) {
        int پیمائش = 0;
        for (int اشاریہ = 1; اشاریہ <= 끝; اشاریہ++) پیمائش += اشاریہ;
        return پیمائش;
    }

    public static int چلائیں() {
        int[] 값들 = new int[3];
        값들[0] = 합계(10);
        값들[1] = -7 / 3;
        값들[2] = "한글".length();
        return 값들[0] == 55 && 값들[1] == -2 && 값들[2] == 2 ? 0 : 1;
    }
}
