// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Méret/홀수 hossz_ÉRTÉK 데이터그램으로 tényleges_adat RTL8139 fogad_ÉRTÉK Loop_ÉRTÉK 순환을 시험한다. */
public final class hálózat_Loop {
    public static int Futtatás() {
        if (felhasználó.인수개수() != 1) { felhasználó.Írás("Usage: run stress PORT\n"); return 2; }
        String Szöveg = felhasználó.Argumentumok(0);
        int port_ÉRTÉK = 0;
        for (int INDEX = 0; INDEX < Szöveg.length(); INDEX++) {
            if (Szöveg.charAt(INDEX) < '0' || Szöveg.charAt(INDEX) > '9' || port_ÉRTÉK > 6553) return 2;
            port_ÉRTÉK = port_ÉRTÉK * 10 + Szöveg.charAt(INDEX) - '0';
        }
        if (port_ÉRTÉK < 1 || port_ÉRTÉK > 65535) return 2;
        int leíró_ÉRTÉK = felhasználó.készít_hálózat(0);
        if (leíró_ÉRTÉK < 0) return 3;
        int[] adat = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int hossz_ÉRTÉK = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < hossz_ÉRTÉK; INDEX++) adat[INDEX] = (INDEX + 회차) & 255;
            if (felhasználó.küld_adat(leíró_ÉRTÉK, 0x0a000202, port_ÉRTÉK, adat, hossz_ÉRTÉK) != hossz_ÉRTÉK) return 4;
            if (felhasználó.fogad_adat(leíró_ÉRTÉK, adat, 300) != hossz_ÉRTÉK) return 5;
            for (int INDEX = 0; INDEX < hossz_ÉRTÉK; INDEX++) if (adat[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        felhasználó.bezár_hálózat(leíró_ÉRTÉK);
        felhasználó.Írás("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
