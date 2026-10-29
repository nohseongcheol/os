// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** IPv4-UDP-Datagramme. Externe Gegenstellen verwenden numerische Adressen. */
public final class Kommunikation {
    private Kommunikation() {}
    public static DatagramSocket öffnen(int portWert) throws EingabeAusgabeAusnahme {
        try { return new DatagramSocket(portWert);
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public static void senden(DatagramSocket endpunkt, int portWert, String inhaltswertWert) throws EingabeAusgabeAusnahme {
        try {
        senden(endpunkt, "127.0.0.1", portWert, inhaltswertWert);
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public static void senden(DatagramSocket endpunkt, String adresse, int portWert, String inhaltswertWert) throws EingabeAusgabeAusnahme {
        try {
        byte[] byteWert = Zeichen.kodieren(inhaltswertWert);
        endpunkt.send(new DatagramPacket(byteWert, byteWert.length, InetAddress.getByName(adresse), portWert));
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public static String empfangen(DatagramSocket endpunkt) throws EingabeAusgabeAusnahme {
        try {
        byte[] byteWert = new byte[512]; DatagramPacket datagramm = new DatagramPacket(byteWert, byteWert.length); endpunkt.receive(datagramm);
        byte[] ergebnis = new byte[datagramm.getLength()]; System.arraycopy(byteWert, 0, ergebnis, 0, ergebnis.length); return Zeichen.datenEntschlüsseln(ergebnis);
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public static void zeitüberschreitung(DatagramSocket endpunkt, int millisekunden) throws EingabeAusgabeAusnahme {
        try { endpunkt.setSoTimeout(millisekunden);
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public static void schließen(DatagramSocket endpunkt) { endpunkt.close(); }
}
