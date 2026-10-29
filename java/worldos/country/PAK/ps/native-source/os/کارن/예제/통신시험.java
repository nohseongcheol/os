// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int ځغلول() {
        int 첫째 = کارن.통신열기(45000);
        if (첫째 < 0) { کارن.لوستل_2("NETWORK UNAVAILABLE\n"); return 3; }
        int[] اومتوک = new int[8];
        boolean 통과 = کارن.통신열기(45000) == -98
            && کارن.자료받기(첫째, اومتوک, 0) == -11
            && کارن.자료받기(첫째, اومتوک, 50) == -110
            && کارن.자료받기(첫째, اومتوک, 3000) == -22
            && کارن.استول_اومتوک(첫째, 0x0a000202, 9, اومتوک, 9) == -90
            && کارن.자료받기(첫째, null, 0) == -14
            && کارن.بندول_جال(첫째) == 0 && کارن.بندول_جال(첫째) == -9;
        کارن.لوستل_2(통과 ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return 통과 ? 0 : 1;
    }
}
