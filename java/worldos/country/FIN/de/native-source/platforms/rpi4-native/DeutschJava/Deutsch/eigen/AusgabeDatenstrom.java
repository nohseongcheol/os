// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;

/** Kanal zum geordneten Schreiben ausgehender Bytes. */
public final class AusgabeDatenstrom {
    private final java.io.OutputStream standardDatenstrom;
    AusgabeDatenstrom(java.io.OutputStream standardDatenstrom) { this.standardDatenstrom = standardDatenstrom; }
    public void schreiben(int Wert) throws EingabeAusgabeAusnahme {
        try { standardDatenstrom.write(Wert);
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public void schreiben(byte[] Daten) throws EingabeAusgabeAusnahme {
        try { standardDatenstrom.write(Daten);
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public void schreiben(byte[] Daten, int ausführenVorgang, int Länge) throws EingabeAusgabeAusnahme {
        try { standardDatenstrom.write(Daten, ausführenVorgang, Länge);
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public void wertAusgeben() throws EingabeAusgabeAusnahme {
        try { standardDatenstrom.flush();
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public void schließen() throws EingabeAusgabeAusnahme {
        try { standardDatenstrom.close();
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
}
