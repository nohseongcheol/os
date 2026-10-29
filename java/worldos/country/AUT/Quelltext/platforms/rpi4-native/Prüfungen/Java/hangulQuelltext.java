// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class hangulQuelltext {
    public static void main(String[] argumente) throws Deutsch.eigen.EingabeAusgabeAusnahme {
        Deutsch.eigen.Ausgabe.zeileSchreiben("eigen 컴파일러와 Deutsch bibliothek");
        int zeichenAnzahl = Deutsch.eigen.Zeichen.kodePunktAnzahl("한글😀");
        Deutsch.eigen.Ausgabe.nummerSchreiben(zeichenAnzahl);
        Deutsch.eigen.Datei.schreiben("한글자료.txt", "eigen betriebskernWert 안에서 저장한 한글😀");
        Deutsch.eigen.Ausgabe.zeileSchreiben(Deutsch.eigen.Datei.lesen("한글자료.txt"));
    }
}
