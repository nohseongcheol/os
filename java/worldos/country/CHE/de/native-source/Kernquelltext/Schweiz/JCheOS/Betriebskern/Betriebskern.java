// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Schweiz.JCheOS.Betriebskern;

import Schweiz.JCheOS.Speicherraum.SpeicherVerwalter;
import Schweiz.JCheOS.Speicherraum.SeiteVerwalter;
import Schweiz.JCheOS.Eingabewert.EingabeVerwalter;
import Schweiz.JCheOS.Aufgabe.prozessWert;
import Schweiz.JCheOS.Aufgabe.Ablaufplaner;
import Schweiz.JCheOS.Systemaufruf.Systemaufruf;
import Schweiz.JCheOS.DateiSystem.dateiDeskriptorTabelle;
import Schweiz.JCheOS.DateiSystem.DateiSystem;

/** Setzt den Java-verwalteten Kernel zusammen und startet ihn. */
public final class Betriebskern {
    private final hardwareWert Gerät;
    private final SpeicherVerwalter Speicherraum = new SpeicherVerwalter(32 * 1024 * 1024);
    private final SeiteVerwalter seiteVerwaltung = new SeiteVerwalter();
    private final DateiSystem DateiSystem = new DateiSystem();
    private final Ablaufplaner Ablaufplaner = new Ablaufplaner(seiteVerwaltung);
    private final EingabeVerwalter EingabeVerwaltung = new EingabeVerwalter(256);
    private final prozessWert ersterProzess;
    private final Systemaufruf Systemaufruf;

    public Betriebskern(hardwareWert Gerät) {
        this.Gerät = Gerät;
        ersterProzess = Ablaufplaner.ersterProzess(new dateiDeskriptorTabelle(DateiSystem));
        Systemaufruf = new Systemaufruf(DateiSystem, seiteVerwaltung, Ablaufplaner, Gerät, EingabeVerwaltung);
    }

    public void ausführenVorgang() {
        Gerät.seriellAusgabe("=== JCheOS 관리 betriebskernWert ===\n");
    }

    public void schrittAusführen() {
        Gerät.anhaltenCPU();
    }

    public SpeicherVerwalter Speicherraum() {
        return Speicherraum;
    }

    public SeiteVerwalter seiteVerwaltung() {
        return seiteVerwaltung;
    }

    public DateiSystem DateiSystem() {
        return DateiSystem;
    }

    public Ablaufplaner Ablaufplaner() {
        return Ablaufplaner;
    }

    public EingabeVerwalter EingabeVerwaltung() {
        return EingabeVerwaltung;
    }

    public prozessWert ersterProzess() {
        return ersterProzess;
    }

    public Systemaufruf Systemaufruf() {
        return Systemaufruf;
    }
}
