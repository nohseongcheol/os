// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package norsk.eget;
import java.net.*;
public final class kontakt_transport {
    private kontakt_transport() {}
    public static kontakt Åpne(String e_post, int portnummer) throws I_U_unntak {
        try { return kontakt.Åpne(e_post, portnummer);
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public static motta_port 수신열기(int portnummer) throws I_U_unntak {
        try { return motta_port.Åpne(portnummer);
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public static Socket Koble_til(String e_post, int port_VERDI) throws I_U_unntak {
        try { return new Socket(e_post, port_VERDI);
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public static ServerSocket 듣기(int port_VERDI) throws I_U_unntak {
        try { return new ServerSocket(port_VERDI);
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public static Socket motta(ServerSocket server_VERDI) throws I_U_unntak {
        try { return server_VERDI.accept();
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
}
