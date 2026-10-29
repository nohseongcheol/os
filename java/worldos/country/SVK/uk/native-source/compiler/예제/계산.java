// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 계산 {
    static int усього_значення(int 끝) {
        int результат = 0;
        for (int індекс = 1; індекс <= 끝; індекс++) результат += індекс;
        return результат;
    }

    public static int запустити() {
        int[] 값들 = new int[3];
        값들[0] = усього_значення(10);
        값들[1] = -7 / 3;
        값들[2] = "한글".length();
        return 값들[0] == 55 && 값들[1] == -2 && 값들[2] == 2 ? 0 : 1;
    }
}
