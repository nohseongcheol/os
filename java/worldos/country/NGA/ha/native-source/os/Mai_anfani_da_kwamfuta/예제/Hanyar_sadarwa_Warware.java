// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Girma/홀수 Tsawo_Daraja 데이터그램으로 Na_hakika_Tarin_bayani RTL8139 수신 Warware_Daraja 순환을 시험한다. */
public final class Hanyar_sadarwa_Warware {
    public static int Tafiyar_da() {
        if (Mai_anfani_da_kwamfuta.인수개수() != 1) { Mai_anfani_da_kwamfuta.Yi_Rubutu("Usage: run stress PORT\n"); return 2; }
        String SMS = Mai_anfani_da_kwamfuta.인수(0);
        int fot_Daraja = 0;
        for (int Indes = 0; Indes < SMS.length(); Indes++) {
            if (SMS.charAt(Indes) < '0' || SMS.charAt(Indes) > '9' || fot_Daraja > 6553) return 2;
            fot_Daraja = fot_Daraja * 10 + SMS.charAt(Indes) - '0';
        }
        if (fot_Daraja < 1 || fot_Daraja > 65535) return 2;
        int Mariki_Daraja = Mai_anfani_da_kwamfuta.buɗe_Hanyar_sadarwa(0);
        if (Mariki_Daraja < 0) return 3;
        int[] Tarin_bayani = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int Tsawo_Daraja = 1024 - (회차 & 1);
            for (int Indes = 0; Indes < Tsawo_Daraja; Indes++) Tarin_bayani[Indes] = (Indes + 회차) & 255;
            if (Mai_anfani_da_kwamfuta.Aika_Tarin_bayani(Mariki_Daraja, 0x0a000202, fot_Daraja, Tarin_bayani, Tsawo_Daraja) != Tsawo_Daraja) return 4;
            if (Mai_anfani_da_kwamfuta.자료받기(Mariki_Daraja, Tarin_bayani, 300) != Tsawo_Daraja) return 5;
            for (int Indes = 0; Indes < Tsawo_Daraja; Indes++) if (Tarin_bayani[Indes] != ((Indes + 회차) & 255)) return 6;
        }
        Mai_anfani_da_kwamfuta.Rufe_Hanyar_sadarwa(Mariki_Daraja);
        Mai_anfani_da_kwamfuta.Yi_Rubutu("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
