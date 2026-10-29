// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Deutsch.eigen.fenster;
import Deutsch.eigen.beschriftung;
import Deutsch.eigen.TextFeld;
import Deutsch.eigen.schaltfläche;
import Deutsch.eigen.EreignisWarteschlange;
import Deutsch.eigen.Ausgabe;
import Deutsch.eigen.AusführbarAufgabe;
import Deutsch.eigen.AktionEmpfänger;
import Deutsch.eigen.AktionMitteilung;

/** Swing-Fenster auf dem eigenständigen Kernel: deutsche Texteingabe, Schaltflächenaktion und Aktualisierung der Beschriftung. */
public class Fensterbeispiel implements AusführbarAufgabe, AktionEmpfänger {
    private fenster grußFenster;
    private TextFeld nameFeld;
    private beschriftung gruß;
    private int grußAnzahl;

    public void fensterÖffnen() {
        grußFenster = new fenster("de Swing", 460, 300);
        grußFenster.elementHinzufügen(new beschriftung("Guten Tag", 20, 20, 420, 28));
        nameFeld = new TextFeld("de", 20, 64, 420, 30);
        gruß = new beschriftung("Guten Tag", 20, 152, 420, 28);
        grußFenster.elementHinzufügen(nameFeld);
        grußFenster.elementHinzufügen(new schaltfläche("grüßen", 20, 108, 180, 32, this));
        grußFenster.elementHinzufügen(gruß);
        grußFenster.elementHinzufügen(new beschriftung("F9 / Shift+Space | X", 20, 204, 420, 28));
        grußFenster.fensterAnzeigen();
        Ausgabe.zeileSchreiben("GUI Beispiele vorbereiten: Fensterbeispiel");
    }

    public void grüßen() {
        grußAnzahl++;
        gruß.textSchreiben("Guten Tag, " + nameFeld.textLesen() + "님! (" + grußAnzahl + ")");
        Ausgabe.zeileSchreiben("GUI Gruß: " + gruß.textLesen());
    }

    public void aufgabeAusführen() { fensterÖffnen(); }
    public void aktionEmpfangen(AktionMitteilung mitteilung) {
        Ausgabe.zeileSchreiben("aktion mitteilung: " + mitteilung.befehlText());
        grüßen();
    }
    public static void ausführenVorgang() {
        EreignisWarteschlange.späterAufrufen(new Fensterbeispiel());
    }
}
