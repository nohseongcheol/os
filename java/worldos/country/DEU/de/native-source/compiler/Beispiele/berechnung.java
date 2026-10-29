// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class berechnung {
    static int gesamtwertWert(int endung) {
        int ergebnis = 0;
        for (int Nummer = 1; Nummer <= endung; Nummer++) ergebnis += Nummer;
        return ergebnis;
    }

    public static int ausführenVorgang() {
        int[] werte = new int[3];
        werte[0] = gesamtwertWert(10);
        werte[1] = -7 / 3;
        werte[2] = "한글".length();
        return werte[0] == 55 && werte[1] == -2 && werte[2] == 2 ? 0 : 1;
    }
}
