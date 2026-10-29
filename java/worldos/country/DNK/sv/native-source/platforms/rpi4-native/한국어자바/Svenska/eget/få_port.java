// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svenska.eget;

/** få_värde(受信)·port_värde(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class få_port {
    private final java.net.ServerSocket Standard_port;
    private få_port(int portnummer) throws indata_utleverans_fel {
        try { Standard_port = new java.net.ServerSocket(portnummer);
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public static få_port Öppna(int portnummer) throws indata_utleverans_fel {
        try { return new få_port(portnummer);
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public kontakt få() throws indata_utleverans_fel {
        try { return new kontakt(Standard_port.accept());
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public int portnummer() { return Standard_port.getLocalPort(); }
    public void TIMEOUT(int 밀리초) throws indata_utleverans_fel {
        try { Standard_port.setSoTimeout(밀리초);
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public boolean informationsteknik_stängd() { return Standard_port.isClosed(); }
    public void Stäng() throws indata_utleverans_fel {
        try { Standard_port.close();
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
}
