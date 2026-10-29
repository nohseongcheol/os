// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class Dateibeispiel {
    public static void ausführenVorgang() throws Deutsch.eigen.EingabeAusgabeAusnahme {
        Deutsch.eigen.Datei.schreiben("java.txt", "JAVA Datei: de 😀\n");
        Deutsch.eigen.Ausgabe.schreiben(Deutsch.eigen.Datei.lesen("java.txt"));
    }
}
