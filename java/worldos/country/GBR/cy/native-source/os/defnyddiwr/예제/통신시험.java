// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int Gweithredu_2() {
        int 첫째 = defnyddiwr.agor_Rhwydwaith(45000);
        if (첫째 < 0) { defnyddiwr.Ysgrifennu("NETWORK UNAVAILABLE\n"); return 3; }
        int[] data = new int[8];
        boolean tocyn_VALUE = defnyddiwr.agor_Rhwydwaith(45000) == -98
            && defnyddiwr.자료받기(첫째, data, 0) == -11
            && defnyddiwr.자료받기(첫째, data, 50) == -110
            && defnyddiwr.자료받기(첫째, data, 3000) == -22
            && defnyddiwr.anfon_data(첫째, 0x0a000202, 9, data, 9) == -90
            && defnyddiwr.자료받기(첫째, null, 0) == -14
            && defnyddiwr.cau_Rhwydwaith(첫째) == 0 && defnyddiwr.cau_Rhwydwaith(첫째) == -9;
        defnyddiwr.Ysgrifennu(tocyn_VALUE ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return tocyn_VALUE ? 0 : 1;
    }
}
