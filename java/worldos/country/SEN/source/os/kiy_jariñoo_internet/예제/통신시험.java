// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int daw() {
        int 첫째 = kiy_jariñoo_internet.sos_mbaal(45000);
        if (첫째 < 0) { kiy_jariñoo_internet.biir("NETWORK UNAVAILABLE\n"); return 3; }
        int[] mbir = new int[8];
        boolean jox_xëyma = kiy_jariñoo_internet.sos_mbaal(45000) == -98
            && kiy_jariñoo_internet.자료받기(첫째, mbir, 0) == -11
            && kiy_jariñoo_internet.자료받기(첫째, mbir, 50) == -110
            && kiy_jariñoo_internet.자료받기(첫째, mbir, 3000) == -22
            && kiy_jariñoo_internet.Yónnee_mbir(첫째, 0x0a000202, 9, mbir, 9) == -90
            && kiy_jariñoo_internet.자료받기(첫째, null, 0) == -14
            && kiy_jariñoo_internet.Tej_mbaal(첫째) == 0 && kiy_jariñoo_internet.Tej_mbaal(첫째) == -9;
        kiy_jariñoo_internet.biir(jox_xëyma ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return jox_xëyma ? 0 : 1;
    }
}
