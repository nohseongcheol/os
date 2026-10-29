// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;

/** Endpunkt zum Senden und Empfangen von UDP-Datagrammen mit erhaltenen Nachrichtengrenzen. */
public final class DatagrammKanal {
    private final java.net.DatagramSocket standardEndpunkt;
    private DatagrammKanal(int portNummer) throws EingabeAusgabeAusnahme {
        try { standardEndpunkt = Kommunikation.öffnen(portNummer);
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public static DatagrammKanal öffnen(int portNummer) throws EingabeAusgabeAusnahme {
        try { return new DatagrammKanal(portNummer);
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public void senden(String adresse, int portNummer, String Daten) throws EingabeAusgabeAusnahme {
        try { Kommunikation.senden(standardEndpunkt, adresse, portNummer, Daten);
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public String empfangen() throws EingabeAusgabeAusnahme {
        try { return Kommunikation.empfangen(standardEndpunkt);
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public void zeitüberschreitung(int millisekunden) throws EingabeAusgabeAusnahme {
        try { Kommunikation.zeitüberschreitung(standardEndpunkt, millisekunden);
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public int portNummer() { return standardEndpunkt.getLocalPort(); }
    public boolean istGeschlossen() { return standardEndpunkt.isClosed(); }
    public void schließen() { Kommunikation.schließen(standardEndpunkt); }
}
