// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Storlek/홀수 längd_värde 데이터그램으로 verklig_data RTL8139 få_värde Loop_värde 순환을 시험한다. */
public final class nätverk_Loop {
    public static int Kör() {
        if (användarutrymme.인수개수() != 1) { användarutrymme.Skriv("Usage: run stress PORT\n"); return 2; }
        String text = användarutrymme.argument(0);
        int port_värde = 0;
        for (int INDEX = 0; INDEX < text.length(); INDEX++) {
            if (text.charAt(INDEX) < '0' || text.charAt(INDEX) > '9' || port_värde > 6553) return 2;
            port_värde = port_värde * 10 + text.charAt(INDEX) - '0';
        }
        if (port_värde < 1 || port_värde > 65535) return 2;
        int handtag_värde = användarutrymme.skapa_nätverk(0);
        if (handtag_värde < 0) return 3;
        int[] data = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int längd_värde = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < längd_värde; INDEX++) data[INDEX] = (INDEX + 회차) & 255;
            if (användarutrymme.skicka_data(handtag_värde, 0x0a000202, port_värde, data, längd_värde) != längd_värde) return 4;
            if (användarutrymme.få_data(handtag_värde, data, 300) != längd_värde) return 5;
            for (int INDEX = 0; INDEX < längd_värde; INDEX++) if (data[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        användarutrymme.Stäng_nätverk(handtag_värde);
        användarutrymme.Skriv("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
