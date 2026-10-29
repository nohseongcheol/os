// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int huutoraade() {
        int 첫째 = kuutoro.udditde_laylaytol(45000);
        if (첫째 < 0) { kuutoro.winndude("NETWORK UNAVAILABLE\n"); return 3; }
        int[] keɓe = new int[8];
        boolean 통과 = kuutoro.udditde_laylaytol(45000) == -98
            && kuutoro.자료받기(첫째, keɓe, 0) == -11
            && kuutoro.자료받기(첫째, keɓe, 50) == -110
            && kuutoro.자료받기(첫째, keɓe, 3000) == -22
            && kuutoro.neldude_keɓe(첫째, 0x0a000202, 9, keɓe, 9) == -90
            && kuutoro.자료받기(첫째, null, 0) == -14
            && kuutoro.uddude_laylaytol(첫째) == 0 && kuutoro.uddude_laylaytol(첫째) == -9;
        kuutoro.winndude(통과 ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return 통과 ? 0 : 1;
    }
}
