// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int Bido() {
        int 첫째 = òjìàrụ.mepee_Netwọọkụ(45000);
        if (첫째 < 0) { òjìàrụ.Chekwaa_ozi("NETWORK UNAVAILABLE\n"); return 3; }
        int[] datà = new int[8];
        boolean 통과 = òjìàrụ.mepee_Netwọọkụ(45000) == -98
            && òjìàrụ.자료받기(첫째, datà, 0) == -11
            && òjìàrụ.자료받기(첫째, datà, 50) == -110
            && òjìàrụ.자료받기(첫째, datà, 3000) == -22
            && òjìàrụ.zìga_datà(첫째, 0x0a000202, 9, datà, 9) == -90
            && òjìàrụ.자료받기(첫째, null, 0) == -14
            && òjìàrụ.mmechi_Netwọọkụ(첫째) == 0 && òjìàrụ.mmechi_Netwọọkụ(첫째) == -9;
        òjìàrụ.Chekwaa_ozi(통과 ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return 통과 ? 0 : 1;
    }
}
