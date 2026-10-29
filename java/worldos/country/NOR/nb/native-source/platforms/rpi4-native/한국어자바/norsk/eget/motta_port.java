// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package norsk.eget;

/** motta_VERDI(受信)·port_VERDI(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class motta_port {
    private final java.net.ServerSocket Standard_port;
    private motta_port(int portnummer) throws I_U_unntak {
        try { Standard_port = new java.net.ServerSocket(portnummer);
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public static motta_port Åpne(int portnummer) throws I_U_unntak {
        try { return new motta_port(portnummer);
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public kontakt motta() throws I_U_unntak {
        try { return new kontakt(Standard_port.accept());
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public int portnummer() { return Standard_port.getLocalPort(); }
    public void TIMEOUT(int 밀리초) throws I_U_unntak {
        try { Standard_port.setSoTimeout(밀리초);
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public boolean informasjonssystemer_lukket() { return Standard_port.isClosed(); }
    public void Lukk() throws I_U_unntak {
        try { Standard_port.close();
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
}
