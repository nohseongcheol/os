// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int run() {
        int 첫째 = gumagamit.buksan_Network(45000);
        if (첫째 < 0) { gumagamit.sumulat("NETWORK UNAVAILABLE\n"); return 3; }
        int[] data = new int[8];
        boolean ipasa_VALUE = gumagamit.buksan_Network(45000) == -98
            && gumagamit.자료받기(첫째, data, 0) == -11
            && gumagamit.자료받기(첫째, data, 50) == -110
            && gumagamit.자료받기(첫째, data, 3000) == -22
            && gumagamit.i_email_data(첫째, 0x0a000202, 9, data, 9) == -90
            && gumagamit.자료받기(첫째, null, 0) == -14
            && gumagamit.isara_Network(첫째) == 0 && gumagamit.isara_Network(첫째) == -9;
        gumagamit.sumulat(ipasa_VALUE ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return ipasa_VALUE ? 0 : 1;
    }
}
