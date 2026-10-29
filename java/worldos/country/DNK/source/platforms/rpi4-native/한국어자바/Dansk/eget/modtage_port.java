// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Dansk.eget;

/** modtage_VÆRDI(受信)·port_VÆRDI(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class modtage_port {
    private final java.net.ServerSocket Standard_port;
    private modtage_port(int portnummer) throws I_O_undtagelse {
        try { Standard_port = new java.net.ServerSocket(portnummer);
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public static modtage_port Åbn(int portnummer) throws I_O_undtagelse {
        try { return new modtage_port(portnummer);
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public forbindelse modtage() throws I_O_undtagelse {
        try { return new forbindelse(Standard_port.accept());
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public int portnummer() { return Standard_port.getLocalPort(); }
    public void TIMEOUT(int 밀리초) throws I_O_undtagelse {
        try { Standard_port.setSoTimeout(밀리초);
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public boolean it_lukket() { return Standard_port.isClosed(); }
    public void Luk() throws I_O_undtagelse {
        try { Standard_port.close();
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
}
