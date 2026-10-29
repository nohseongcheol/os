// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int 시작() {
        int 첫째 = ka_yataayakalü.통신열기(45000);
        if (첫째 < 0) { ka_yataayakalü.ashajaa("NETWORK UNAVAILABLE\n"); return 3; }
        int[] atijaaya = new int[8];
        boolean 통과 = ka_yataayakalü.통신열기(45000) == -98
            && ka_yataayakalü.자료받기(첫째, atijaaya, 0) == -11
            && ka_yataayakalü.자료받기(첫째, atijaaya, 50) == -110
            && ka_yataayakalü.자료받기(첫째, atijaaya, 3000) == -22
            && ka_yataayakalü.ajütaa_atijaaya(첫째, 0x0a000202, 9, atijaaya, 9) == -90
            && ka_yataayakalü.자료받기(첫째, null, 0) == -14
            && ka_yataayakalü.asürülaa_kusu(첫째) == 0 && ka_yataayakalü.asürülaa_kusu(첫째) == -9;
        ka_yataayakalü.ashajaa(통과 ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return 통과 ? 0 : 1;
    }
}
