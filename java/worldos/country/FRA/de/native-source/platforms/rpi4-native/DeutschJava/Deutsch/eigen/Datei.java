// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** Behält den vertrauten Dateibegriff bei. Der derzeitige Speicher besteht aus RAM-Dateien, die beim Neustart verloren gehen. */
public final class Datei {
    private Datei() {}
    public static byte[] byteWertLesen(String Name) throws EingabeAusgabeAusnahme {
        try {
        FileInputStream datenstromWert = new FileInputStream(Name);
        try {
            byte[] vorläufigWert = new byte[16384]; int Zahl = 0, Wert;
            while ((Wert = datenstromWert.read()) != -1) { if (Zahl == vorläufigWert.length) throw new EingabeAusgabeAusnahme("Größenbegrenzung der Datei"); vorläufigWert[Zahl++] = (byte)Wert; }
            byte[] ergebnis = new byte[Zahl]; System.arraycopy(vorläufigWert, 0, ergebnis, 0, Zahl); return ergebnis;
        } finally { datenstromWert.close(); }
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public static void byteWertSchreiben(String Name, byte[] inhaltswertWert) throws EingabeAusgabeAusnahme {
        try {
        FileOutputStream datenstromWert = new FileOutputStream(Name);
        try { for (int schleifeIndex = 0; schleifeIndex < inhaltswertWert.length; schleifeIndex++) datenstromWert.write(inhaltswertWert[schleifeIndex] & 255); } finally { datenstromWert.close(); }
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public static String lesen(String Name) throws EingabeAusgabeAusnahme {
        try { return Zeichen.datenEntschlüsseln(byteWertLesen(Name));
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public static void schreiben(String Name, String inhaltswertWert) throws EingabeAusgabeAusnahme {
        try { byteWertSchreiben(Name, Zeichen.kodieren(inhaltswertWert));
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
}
