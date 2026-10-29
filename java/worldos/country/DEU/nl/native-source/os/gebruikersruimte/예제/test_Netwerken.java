// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class test_Netwerken {
    public static int starten() {
        int 첫째 = gebruikersruimte.open_net(45000);
        if (첫째 < 0) { gebruikersruimte.Schrijven("NETWORK UNAVAILABLE\n"); return 3; }
        int[] gegevens = new int[8];
        boolean doorgeven_WAARDE = gebruikersruimte.open_net(45000) == -98
            && gebruikersruimte.ontvangen_gegevens(첫째, gegevens, 0) == -11
            && gebruikersruimte.ontvangen_gegevens(첫째, gegevens, 50) == -110
            && gebruikersruimte.ontvangen_gegevens(첫째, gegevens, 3000) == -22
            && gebruikersruimte.e_mailen_gegevens(첫째, 0x0a000202, 9, gegevens, 9) == -90
            && gebruikersruimte.ontvangen_gegevens(첫째, null, 0) == -14
            && gebruikersruimte.Sluiten_net(첫째) == 0 && gebruikersruimte.Sluiten_net(첫째) == -9;
        gebruikersruimte.Schrijven(doorgeven_WAARDE ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return doorgeven_WAARDE ? 0 : 1;
    }
}
