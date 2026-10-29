// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class Farbe {
    public static void main(String[] argumente) throws Exception {
        int summeWert = 0;
        int Zahl = 1;
        while (Zahl <= 10) {
            summeWert = summeWert + Zahl;
            Zahl = Zahl + 1;
        }
        Deutsch.eigen.Ausgabe.nummerSchreiben(summeWert);
        Deutsch.eigen.Datei.schreiben("aot.txt", "한글 AOT Datei 😀");
        Deutsch.eigen.Ausgabe.zeileSchreiben(Deutsch.eigen.Datei.lesen("aot.txt"));
    }
}
