// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Velikost/홀수 délka_HODNOTA 데이터그램으로 skutečný_data RTL8139 dostat_HODNOTA Loop_HODNOTA 순환을 시험한다. */
public final class síť_Loop {
    public static int Spustit_2() {
        if (uživatelský_prostor.인수개수() != 1) { uživatelský_prostor.Zápis("Usage: run stress PORT\n"); return 2; }
        String text = uživatelský_prostor.argumenty(0);
        int port_HODNOTA = 0;
        for (int INDEX = 0; INDEX < text.length(); INDEX++) {
            if (text.charAt(INDEX) < '0' || text.charAt(INDEX) > '9' || port_HODNOTA > 6553) return 2;
            port_HODNOTA = port_HODNOTA * 10 + text.charAt(INDEX) - '0';
        }
        if (port_HODNOTA < 1 || port_HODNOTA > 65535) return 2;
        int úchyt_HODNOTA = uživatelský_prostor.otevřít_síť(0);
        if (úchyt_HODNOTA < 0) return 3;
        int[] data = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int délka_HODNOTA = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < délka_HODNOTA; INDEX++) data[INDEX] = (INDEX + 회차) & 255;
            if (uživatelský_prostor.poslat_data(úchyt_HODNOTA, 0x0a000202, port_HODNOTA, data, délka_HODNOTA) != délka_HODNOTA) return 4;
            if (uživatelský_prostor.dostat_data(úchyt_HODNOTA, data, 300) != délka_HODNOTA) return 5;
            for (int INDEX = 0; INDEX < délka_HODNOTA; INDEX++) if (data[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        uživatelský_prostor.Zavřít_síť(úchyt_HODNOTA);
        uživatelský_prostor.Zápis("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
