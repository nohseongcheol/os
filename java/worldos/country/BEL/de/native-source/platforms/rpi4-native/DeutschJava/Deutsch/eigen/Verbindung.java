// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;

/** Endpunkt eines mit der Gegenstelle verbundenen TCP-Bytestroms. */
public final class Verbindung {
    private final java.net.Socket standardBibliothekBrücke;
    Verbindung(java.net.Socket standardBibliothekBrücke) { this.standardBibliothekBrücke = standardBibliothekBrücke; }
    public static Verbindung öffnen(String adresse, int portNummer) throws EingabeAusgabeAusnahme {
        try {
            return new Verbindung(new java.net.Socket(adresse, portNummer));
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public EingabeDatenstrom Eingabewert() throws EingabeAusgabeAusnahme {
        try { return new EingabeDatenstrom(standardBibliothekBrücke.getInputStream());
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public AusgabeDatenstrom Ausgabe() throws EingabeAusgabeAusnahme {
        try { return new AusgabeDatenstrom(standardBibliothekBrücke.getOutputStream());
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public void zeitüberschreitung(int millisekunden) throws EingabeAusgabeAusnahme {
        try { standardBibliothekBrücke.setSoTimeout(millisekunden);
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public int portNummer() { return standardBibliothekBrücke.getPort(); }
    public int lokalPortNummer() { return standardBibliothekBrücke.getLocalPort(); }
    public boolean istGeschlossen() { return standardBibliothekBrücke.isClosed(); }
    public boolean verbunden() { return standardBibliothekBrücke.isConnected(); }
    public void schließen() throws EingabeAusgabeAusnahme {
        try { standardBibliothekBrücke.close();
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
}
