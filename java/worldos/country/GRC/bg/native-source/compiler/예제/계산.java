// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 계산 {
    static int общо_стойност(int 끝) {
        int РЕЗУЛТАТ = 0;
        for (int индекс = 1; индекс <= 끝; индекс++) РЕЗУЛТАТ += индекс;
        return РЕЗУЛТАТ;
    }

    public static int Стартиране() {
        int[] 값들 = new int[3];
        값들[0] = общо_стойност(10);
        값들[1] = -7 / 3;
        값들[2] = "한글".length();
        return 값들[0] == 55 && 값들[1] == -2 && 값들[2] == 2 ? 0 : 1;
    }
}
