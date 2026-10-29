// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class data_komunikace {
    static int číslice_HODNOTA(String text) {
        if (text == null || text.length() == 0) return -1;
        int VÝSLEDEK = 0;
        for (int INDEX = 0; INDEX < text.length(); INDEX++) {
            int HODNOTA = text.charAt(INDEX) - '0';
            if (HODNOTA < 0 || HODNOTA > 9 || VÝSLEDEK > 6553) return -1;
            VÝSLEDEK = VÝSLEDEK * 10 + HODNOTA;
            if (VÝSLEDEK > 65535) return -1;
        }
        return VÝSLEDEK;
    }
    static int Adresa(String text) {
        if (text == null) return 0;
        int HODNOTA = 0, VÝSLEDEK = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= text.length(); INDEX++) {
            int 문자 = INDEX == text.length() ? '.' : text.charAt(INDEX);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                VÝSLEDEK = (VÝSLEDEK << 8) | HODNOTA; 부분++; HODNOTA = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                HODNOTA = HODNOTA * 10 + 문자 - '0';
                if (++자릿수 > 3 || HODNOTA > 255) return 0;
            }
        }
        return 부분 == 4 ? VÝSLEDEK : 0;
    }
    public static int Spustit_2() {
        if (uživatelský_prostor.인수개수() != 3) { uživatelský_prostor.Zápis("Usage: run udp IP PORT TEXT\n"); return 2; }
        int Adresa = Adresa(uživatelský_prostor.argumenty(0)), port_HODNOTA = číslice_HODNOTA(uživatelský_prostor.argumenty(1));
        String Obsah_HODNOTA = uživatelský_prostor.argumenty(2);
        if (Adresa == 0 || port_HODNOTA < 1 || Obsah_HODNOTA.length() > 1024) { uživatelský_prostor.Zápis("Bad destination\n"); return 2; }
        int úchyt_HODNOTA = uživatelský_prostor.otevřít_síť(0);
        if (úchyt_HODNOTA < 0) { uživatelský_prostor.Zápis("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] data = new int[1024];
        for (int INDEX = 0; INDEX < Obsah_HODNOTA.length(); INDEX++) data[INDEX] = Obsah_HODNOTA.charAt(INDEX);
        if (uživatelský_prostor.poslat_data(úchyt_HODNOTA, Adresa, port_HODNOTA, data, Obsah_HODNOTA.length()) < 0) {
            uživatelský_prostor.Zápis("UDP SEND FAILED\n"); uživatelský_prostor.Zavřít_síť(úchyt_HODNOTA); return 4;
        }
        uživatelský_prostor.Zápis("UDP SENT\n");
        int RECEIVED_délka = uživatelský_prostor.dostat_data(úchyt_HODNOTA, data, 1500);
        boolean 같음 = RECEIVED_délka == Obsah_HODNOTA.length() && uživatelský_prostor.보낸주소(úchyt_HODNOTA) == Adresa && uživatelský_prostor.보낸창구(úchyt_HODNOTA) == port_HODNOTA;
        if (같음) for (int INDEX = 0; INDEX < RECEIVED_délka; INDEX++) if (data[INDEX] != Obsah_HODNOTA.charAt(INDEX)) 같음 = false;
        uživatelský_prostor.Zavřít_síť(úchyt_HODNOTA);
        if (RECEIVED_délka < 0) { uživatelský_prostor.Zápis("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        uživatelský_prostor.Zápis(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
