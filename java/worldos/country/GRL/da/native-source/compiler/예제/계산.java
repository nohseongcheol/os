// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 계산 {
    static int i_alt_VÆRDI(int 끝) {
        int KR = 0;
        for (int INDEKS = 1; INDEKS <= 끝; INDEKS++) KR += INDEKS;
        return KR;
    }

    public static int Kør_2() {
        int[] 값들 = new int[3];
        값들[0] = i_alt_VÆRDI(10);
        값들[1] = -7 / 3;
        값들[2] = "한글".length();
        return 값들[0] == 55 && 값들[1] == -2 && 값들[2] == 2 ? 0 : 1;
    }
}
