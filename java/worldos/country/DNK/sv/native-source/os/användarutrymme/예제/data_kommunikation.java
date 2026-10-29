// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class data_kommunikation {
    static int siffra_värde(String text) {
        if (text == null || text.length() == 0) return -1;
        int RESULTAT = 0;
        for (int INDEX = 0; INDEX < text.length(); INDEX++) {
            int värde = text.charAt(INDEX) - '0';
            if (värde < 0 || värde > 9 || RESULTAT > 6553) return -1;
            RESULTAT = RESULTAT * 10 + värde;
            if (RESULTAT > 65535) return -1;
        }
        return RESULTAT;
    }
    static int Adress(String text) {
        if (text == null) return 0;
        int värde = 0, RESULTAT = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= text.length(); INDEX++) {
            int 문자 = INDEX == text.length() ? '.' : text.charAt(INDEX);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                RESULTAT = (RESULTAT << 8) | värde; 부분++; värde = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                värde = värde * 10 + 문자 - '0';
                if (++자릿수 > 3 || värde > 255) return 0;
            }
        }
        return 부분 == 4 ? RESULTAT : 0;
    }
    public static int Kör() {
        if (användarutrymme.인수개수() != 3) { användarutrymme.Skriv("Usage: run udp IP PORT TEXT\n"); return 2; }
        int Adress = Adress(användarutrymme.argument(0)), port_värde = siffra_värde(användarutrymme.argument(1));
        String Innehåll_värde = användarutrymme.argument(2);
        if (Adress == 0 || port_värde < 1 || Innehåll_värde.length() > 1024) { användarutrymme.Skriv("Bad destination\n"); return 2; }
        int handtag_värde = användarutrymme.skapa_nätverk(0);
        if (handtag_värde < 0) { användarutrymme.Skriv("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] data = new int[1024];
        for (int INDEX = 0; INDEX < Innehåll_värde.length(); INDEX++) data[INDEX] = Innehåll_värde.charAt(INDEX);
        if (användarutrymme.skicka_data(handtag_värde, Adress, port_värde, data, Innehåll_värde.length()) < 0) {
            användarutrymme.Skriv("UDP SEND FAILED\n"); användarutrymme.Stäng_nätverk(handtag_värde); return 4;
        }
        användarutrymme.Skriv("UDP SENT\n");
        int BELOPP_längd = användarutrymme.få_data(handtag_värde, data, 1500);
        boolean 같음 = BELOPP_längd == Innehåll_värde.length() && användarutrymme.보낸주소(handtag_värde) == Adress && användarutrymme.보낸창구(handtag_värde) == port_värde;
        if (같음) for (int INDEX = 0; INDEX < BELOPP_längd; INDEX++) if (data[INDEX] != Innehåll_värde.charAt(INDEX)) 같음 = false;
        användarutrymme.Stäng_nätverk(handtag_värde);
        if (BELOPP_längd < 0) { användarutrymme.Skriv("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        användarutrymme.Skriv(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
