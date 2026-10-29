// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int Tafiyar_da() {
        int 첫째 = Mai_anfani_da_kwamfuta.buɗe_Hanyar_sadarwa(45000);
        if (첫째 < 0) { Mai_anfani_da_kwamfuta.Yi_Rubutu("NETWORK UNAVAILABLE\n"); return 3; }
        int[] Tarin_bayani = new int[8];
        boolean 통과 = Mai_anfani_da_kwamfuta.buɗe_Hanyar_sadarwa(45000) == -98
            && Mai_anfani_da_kwamfuta.자료받기(첫째, Tarin_bayani, 0) == -11
            && Mai_anfani_da_kwamfuta.자료받기(첫째, Tarin_bayani, 50) == -110
            && Mai_anfani_da_kwamfuta.자료받기(첫째, Tarin_bayani, 3000) == -22
            && Mai_anfani_da_kwamfuta.Aika_Tarin_bayani(첫째, 0x0a000202, 9, Tarin_bayani, 9) == -90
            && Mai_anfani_da_kwamfuta.자료받기(첫째, null, 0) == -14
            && Mai_anfani_da_kwamfuta.Rufe_Hanyar_sadarwa(첫째) == 0 && Mai_anfani_da_kwamfuta.Rufe_Hanyar_sadarwa(첫째) == -9;
        Mai_anfani_da_kwamfuta.Yi_Rubutu(통과 ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return 통과 ? 0 : 1;
    }
}
