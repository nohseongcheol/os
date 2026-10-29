// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 계산 {
    static int summa_värde(int 끝) {
        int RESULTAT = 0;
        for (int INDEX = 1; INDEX <= 끝; INDEX++) RESULTAT += INDEX;
        return RESULTAT;
    }

    public static int Kör() {
        int[] 값들 = new int[3];
        값들[0] = summa_värde(10);
        값들[1] = -7 / 3;
        값들[2] = "한글".length();
        return 값들[0] == 55 && 값들[1] == -2 && 값들[2] == 2 ? 0 : 1;
    }
}
