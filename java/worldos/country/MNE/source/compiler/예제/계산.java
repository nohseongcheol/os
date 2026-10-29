// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 계산 {
    static int ukupan_VALUE(int 끝) {
        int KR = 0;
        for (int INDEX = 1; INDEX <= 끝; INDEX++) KR += INDEX;
        return KR;
    }

    public static int koristiti() {
        int[] 값들 = new int[3];
        값들[0] = ukupan_VALUE(10);
        값들[1] = -7 / 3;
        값들[2] = "한글".length();
        return 값들[0] == 55 && 값들[1] == -2 && 값들[2] == 2 ? 0 : 1;
    }
}
