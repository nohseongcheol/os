// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Dansk.eget;
import java.net.*;
public final class forbindelse_transport {
    private forbindelse_transport() {}
    public static forbindelse Åbn(String mail, int portnummer) throws I_O_undtagelse {
        try { return forbindelse.Åbn(mail, portnummer);
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public static modtage_port 수신열기(int portnummer) throws I_O_undtagelse {
        try { return modtage_port.Åbn(portnummer);
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public static Socket Tilslut(String mail, int port_VÆRDI) throws I_O_undtagelse {
        try { return new Socket(mail, port_VÆRDI);
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public static ServerSocket lytte_slutpunkt(int port_VÆRDI) throws I_O_undtagelse {
        try { return new ServerSocket(port_VÆRDI);
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public static Socket modtage(ServerSocket server_VÆRDI) throws I_O_undtagelse {
        try { return server_VÆRDI.accept();
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
}
