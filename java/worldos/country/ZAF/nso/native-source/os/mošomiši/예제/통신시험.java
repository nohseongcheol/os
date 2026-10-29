// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int Diriša() {
        int 첫째 = mošomiši.bula_Netweke(45000);
        if (첫째 < 0) { mošomiši.Ngwala("NETWORK UNAVAILABLE\n"); return 3; }
        int[] data = new int[8];
        boolean feta_boleng = mošomiši.bula_Netweke(45000) == -98
            && mošomiši.자료받기(첫째, data, 0) == -11
            && mošomiši.자료받기(첫째, data, 50) == -110
            && mošomiši.자료받기(첫째, data, 3000) == -22
            && mošomiši.Romela_data(첫째, 0x0a000202, 9, data, 9) == -90
            && mošomiši.자료받기(첫째, null, 0) == -14
            && mošomiši.tswalela_Netweke(첫째) == 0 && mošomiši.tswalela_Netweke(첫째) == -9;
        mošomiši.Ngwala(feta_boleng ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return feta_boleng ? 0 : 1;
    }
}
