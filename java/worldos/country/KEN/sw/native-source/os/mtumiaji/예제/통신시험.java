// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int endesha() {
        int 첫째 = mtumiaji.unda_Mtandao(45000);
        if (첫째 < 0) { mtumiaji.andika("NETWORK UNAVAILABLE\n"); return 3; }
        int[] data = new int[8];
        boolean pitisha_thamani = mtumiaji.unda_Mtandao(45000) == -98
            && mtumiaji.자료받기(첫째, data, 0) == -11
            && mtumiaji.자료받기(첫째, data, 50) == -110
            && mtumiaji.자료받기(첫째, data, 3000) == -22
            && mtumiaji.tuma_data(첫째, 0x0a000202, 9, data, 9) == -90
            && mtumiaji.자료받기(첫째, null, 0) == -14
            && mtumiaji.funga_Mtandao(첫째) == 0 && mtumiaji.funga_Mtandao(첫째) == -9;
        mtumiaji.andika(pitisha_thamani ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return pitisha_thamani ? 0 : 1;
    }
}
