// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;

/** Kanal zum geordneten Lesen eingehender Bytes. */
public final class EingabeDatenstrom {
    private final java.io.InputStream standardDatenstrom;
    EingabeDatenstrom(java.io.InputStream standardDatenstrom) { this.standardDatenstrom = standardDatenstrom; }
    public int lesen() throws EingabeAusgabeAusnahme {
        try { return standardDatenstrom.read();
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public int lesen(byte[] Daten) throws EingabeAusgabeAusnahme {
        try { return standardDatenstrom.read(Daten);
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public int lesen(byte[] Daten, int ausführenVorgang, int Länge) throws EingabeAusgabeAusnahme {
        try { return standardDatenstrom.read(Daten, ausführenVorgang, Länge);
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public void schließen() throws EingabeAusgabeAusnahme {
        try { standardDatenstrom.close();
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
}
