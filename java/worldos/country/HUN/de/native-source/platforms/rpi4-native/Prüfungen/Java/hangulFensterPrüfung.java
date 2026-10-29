// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Deutsch.eigen.fenster;
import Deutsch.eigen.Bedienelement;
import Deutsch.eigen.*;

public class hangulFensterPrüfung implements AusführbarAufgabe, AktionEmpfänger {
    fenster Bildschirm;
    beschriftung Anleitung;
    TextFeld Eingabewert;
    public void aufgabeAusführen() {
        Prüfpunkte.erfordern(EreignisWarteschlange.istEreignisVerteilend(), "Deutsch Bildschirm Aufgabe 큐");
        Bildschirm = new fenster("Deutsch bibliothek fenster", 400, 280);
        Anleitung = Bedienelement.kennzeichenWert("한글로 Java 코딩", 20, 20, 340, 30);
        Eingabewert = Bedienelement.TextFeld("Name", 20, 65, 340, 30);
        Bildschirm.elementHinzufügen(Anleitung);
        Bildschirm.elementHinzufügen(Eingabewert);
        Bildschirm.elementHinzufügen(Bedienelement.schaltfläche("grüßen", 20, 110, 180, 32, this));
        Bildschirm.fensterAnzeigen();
        Ausgabe.zeileSchreiben("KOREAN SWING READY");
    }
    public void aktionEmpfangen(AktionMitteilung ereignis) {
        Prüfpunkte.erfordern(EreignisWarteschlange.istEreignisVerteilend(), "Deutsch aktion 되부름");
        Prüfpunkte.erfordern(ereignis.Nummer() == 1001 && ereignis.ereignisQuelltext() instanceof schaltfläche, "Deutsch ereignis 객체와 ursprungWert");
        Prüfpunkte.erfordern(!((Object)ereignis.ereignisQuelltext() instanceof javax.swing.JButton), "표준 단추와 독립된 formatWert");
        Prüfpunkte.erfordern(!((Object)ereignis instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 formatWert");
        Anleitung.textSchreiben("안녕하세요 " + Eingabewert.textLesen());
        Ausgabe.zeileSchreiben("KOREAN SWING CLICK " + Eingabewert.textLesen());
    }
    public static void main(String[] argumente) {
        EreignisWarteschlange.späterAufrufen(new hangulFensterPrüfung());
    }
}
