// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;
import java.net.*;
public final class verbindungBeförderung {
    private verbindungBeförderung() {}
    public static Verbindung öffnen(String adresse, int portNummer) throws EingabeAusgabeAusnahme {
        try { return Verbindung.öffnen(adresse, portNummer);
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public static portEmpfangen empfängerÖffnen(int portNummer) throws EingabeAusgabeAusnahme {
        try { return portEmpfangen.öffnen(portNummer);
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public static Socket verbinden(String adresse, int portWert) throws EingabeAusgabeAusnahme {
        try { return new Socket(adresse, portWert);
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public static ServerSocket endpunktLauschen(int portWert) throws EingabeAusgabeAusnahme {
        try { return new ServerSocket(portWert);
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
    public static Socket empfangen(ServerSocket dienstanbieterWert) throws EingabeAusgabeAusnahme {
        try { return dienstanbieterWert.accept();
        } catch (java.io.IOException fehler) { throw ausnahmeUmwandeln.eingabeAusgabe(fehler); }
        catch (RuntimeException fehler) { throw ausnahmeUmwandeln.befehlAusführen(fehler); }
    }
}
