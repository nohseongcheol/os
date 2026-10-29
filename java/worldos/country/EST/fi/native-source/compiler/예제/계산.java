// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 계산 {
    static int summa_ARVO(int 끝) {
        int TULOS = 0;
        for (int INDEKSI = 1; INDEKSI <= 끝; INDEKSI++) TULOS += INDEKSI;
        return TULOS;
    }

    public static int Suorita_2() {
        int[] 값들 = new int[3];
        값들[0] = summa_ARVO(10);
        값들[1] = -7 / 3;
        값들[2] = "한글".length();
        return 값들[0] == 55 && 값들[1] == -2 && 값들[2] == 2 ? 0 : 1;
    }
}
