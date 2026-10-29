// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static kontakt Opna(String ADDRESS, int portnummer) throws I_U_unntak {
        try { return kontakt.Opna(ADDRESS, portnummer);
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public static 수신창구 수신열기(int portnummer) throws I_U_unntak {
        try { return 수신창구.Opna(portnummer);
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public static Socket Kopla_til(String ADDRESS, int port_VALUE) throws I_U_unntak {
        try { return new Socket(ADDRESS, port_VALUE);
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public static ServerSocket lytte_endepunkt(int port_VALUE) throws I_U_unntak {
        try { return new ServerSocket(port_VALUE);
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public static Socket 받기(ServerSocket tenar_VALUE) throws I_U_unntak {
        try { return tenar_VALUE.accept();
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
}
