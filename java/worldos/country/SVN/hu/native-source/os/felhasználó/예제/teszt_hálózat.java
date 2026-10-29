// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class teszt_hálózat {
    public static int Futtatás() {
        int 첫째 = felhasználó.készít_hálózat(45000);
        if (첫째 < 0) { felhasználó.Írás("NETWORK UNAVAILABLE\n"); return 3; }
        int[] adat = new int[8];
        boolean továbbít_ÉRTÉK = felhasználó.készít_hálózat(45000) == -98
            && felhasználó.fogad_adat(첫째, adat, 0) == -11
            && felhasználó.fogad_adat(첫째, adat, 50) == -110
            && felhasználó.fogad_adat(첫째, adat, 3000) == -22
            && felhasználó.küld_adat(첫째, 0x0a000202, 9, adat, 9) == -90
            && felhasználó.fogad_adat(첫째, null, 0) == -14
            && felhasználó.bezár_hálózat(첫째) == 0 && felhasználó.bezár_hálózat(첫째) == -9;
        felhasználó.Írás(továbbít_ÉRTÉK ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return továbbít_ÉRTÉK ? 0 : 1;
    }
}
