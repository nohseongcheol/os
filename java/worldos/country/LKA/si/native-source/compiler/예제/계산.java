// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 계산 {
    static int 합계(int 끝) {
        int 결과 = 0;
        for (int සූචිය = 1; සූචිය <= 끝; සූචිය++) 결과 += සූචිය;
        return 결과;
    }

    public static int ක්_රියාත්මක_කරන්න_2() {
        int[] 값들 = new int[3];
        값들[0] = 합계(10);
        값들[1] = -7 / 3;
        값들[2] = "한글".length();
        return 값들[0] == 55 && 값들[1] == -2 && 값들[2] == 2 ? 0 : 1;
    }
}
