// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 계산 {
    static int итог_ЗНАЧЕН(int 끝) {
        int результат = 0;
        for (int ИНДЕКС = 1; ИНДЕКС <= 끝; ИНДЕКС++) результат += ИНДЕКС;
        return результат;
    }

    public static int запустить() {
        int[] 값들 = new int[3];
        값들[0] = итог_ЗНАЧЕН(10);
        값들[1] = -7 / 3;
        값들[2] = "한글".length();
        return 값들[0] == 55 && 값들[1] == -2 && 값들[2] == 2 ? 0 : 1;
    }
}
