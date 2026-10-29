// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 계산 {
    static int סך_הכל_ערך(int 끝) {
        int תוצאה = 0;
        for (int מדד = 1; מדד <= 끝; מדד++) תוצאה += מדד;
        return תוצאה;
    }

    public static int הפעלה() {
        int[] 값들 = new int[3];
        값들[0] = סך_הכל_ערך(10);
        값들[1] = -7 / 3;
        값들[2] = "한글".length();
        return 값들[0] == 55 && 값들[1] == -2 && 값들[2] == 2 ? 0 : 1;
    }
}
