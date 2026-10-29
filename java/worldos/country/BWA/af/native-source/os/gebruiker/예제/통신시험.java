// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int Loop() {
        int 첫째 = gebruiker.skep_Netwerk(45000);
        if (첫째 < 0) { gebruiker.Skryf("NETWORK UNAVAILABLE\n"); return 3; }
        int[] data = new int[8];
        boolean aanstuur_VALUE = gebruiker.skep_Netwerk(45000) == -98
            && gebruiker.자료받기(첫째, data, 0) == -11
            && gebruiker.자료받기(첫째, data, 50) == -110
            && gebruiker.자료받기(첫째, data, 3000) == -22
            && gebruiker.e_pos_data(첫째, 0x0a000202, 9, data, 9) == -90
            && gebruiker.자료받기(첫째, null, 0) == -14
            && gebruiker.sluit_Netwerk(첫째) == 0 && gebruiker.sluit_Netwerk(첫째) == -9;
        gebruiker.Skryf(aanstuur_VALUE ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return aanstuur_VALUE ? 0 : 1;
    }
}
