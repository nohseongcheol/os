// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 계산 {
    static int totaal_WAARDE(int 끝) {
        int resultaat = 0;
        for (int INDEX = 1; INDEX <= 끝; INDEX++) resultaat += INDEX;
        return resultaat;
    }

    public static int starten() {
        int[] 값들 = new int[3];
        값들[0] = totaal_WAARDE(10);
        값들[1] = -7 / 3;
        값들[2] = "한글".length();
        return 값들[0] == 55 && 값들[1] == -2 && 값들[2] == 2 ? 0 : 1;
    }
}
