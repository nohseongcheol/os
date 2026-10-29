// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italien.JItaOS.unterbrechen;

import java.util.Arrays;

/** Registriert und verteilt die Java-verwalteten IDT-Behandler. */
public final class UnterbrechenVerwalter {
    private final UnterbrechenBehandler[] behandlerListe = new UnterbrechenBehandler[256];
    private boolean aktiv;

    public void eintragRegister(int Nummer, UnterbrechenBehandler Behandler) {
        nummerÜberprüfen(Nummer);
        behandlerListe[Nummer] = Behandler;
    }

    public void speichergerätFreigeben(int Nummer) {
        nummerÜberprüfen(Nummer);
        behandlerListe[Nummer] = null;
    }

    public int wertVerteilen(int Nummer, int gespeichertStapelAdresse) {
        nummerÜberprüfen(Nummer);
        if (!aktiv) {
            return gespeichertStapelAdresse;
        }
        UnterbrechenBehandler Behandler = behandlerListe[Nummer];
        return Behandler == null ? gespeichertStapelAdresse : Behandler.prozessWertEintrag(gespeichertStapelAdresse);
    }

    public void aktivieren() {
        aktiv = true;
    }

    public void deaktivieren() {
        aktiv = false;
    }

    public boolean istAktiv() {
        return aktiv;
    }

    public void alleFreigeben() {
        Arrays.fill(behandlerListe, null);
    }

    private void nummerÜberprüfen(int Nummer) {
        if (Nummer < 0 || Nummer >= behandlerListe.length) {
            throw new IllegalArgumentException("unterbrechen 번호가 올바르지 않습니다.");
        }
    }
}

