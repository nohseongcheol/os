// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;

/** Nimmt eingehende TCP-Verbindungen an. */
public final class portEmpfangen {
    private final java.net.ServerSocket standardPort;
    private portEmpfangen(int portNummer) throws EingabeAusgabeAusnahme {
        try { standardPort = new java.net.ServerSocket(portNummer);
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public static portEmpfangen öffnen(int portNummer) throws EingabeAusgabeAusnahme {
        try { return new portEmpfangen(portNummer);
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public Verbindung empfangen() throws EingabeAusgabeAusnahme {
        try { return new Verbindung(standardPort.accept());
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public int portNummer() { return standardPort.getLocalPort(); }
    public void zeitüberschreitung(int millisekunden) throws EingabeAusgabeAusnahme {
        try { standardPort.setSoTimeout(millisekunden);
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public boolean istGeschlossen() { return standardPort.isClosed(); }
    public void schließen() throws EingabeAusgabeAusnahme {
        try { standardPort.close();
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
}
