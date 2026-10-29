// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int serje() {
        int 첫째 = utent.fetaħ_netwerk(45000);
        if (첫째 < 0) { utent.kiteb("NETWORK UNAVAILABLE\n"); return 3; }
        int[] data = new int[8];
        boolean għadda_VALUE = utent.fetaħ_netwerk(45000) == -98
            && utent.자료받기(첫째, data, 0) == -11
            && utent.자료받기(첫째, data, 50) == -110
            && utent.자료받기(첫째, data, 3000) == -22
            && utent.bagħat_data(첫째, 0x0a000202, 9, data, 9) == -90
            && utent.자료받기(첫째, null, 0) == -14
            && utent.agħlaq_netwerk(첫째) == 0 && utent.agħlaq_netwerk(첫째) == -9;
        utent.kiteb(għadda_VALUE ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return għadda_VALUE ? 0 : 1;
    }
}
