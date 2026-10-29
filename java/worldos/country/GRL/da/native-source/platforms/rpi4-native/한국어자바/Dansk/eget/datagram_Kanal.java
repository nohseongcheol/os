// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Dansk.eget;

/** datagram(電文)·Kanal_post(通路): 경계를 가진 UDP 자료를 주고받는 slutpunkt. */
public final class datagram_Kanal {
    private final java.net.DatagramSocket Standard_slutpunkt;
    private datagram_Kanal(int portnummer) throws I_O_undtagelse {
        try { Standard_slutpunkt = 통신.Åbn(portnummer);
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public static datagram_Kanal Åbn(int portnummer) throws I_O_undtagelse {
        try { return new datagram_Kanal(portnummer);
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public void maile(String mail, int portnummer, String data) throws I_O_undtagelse {
        try { 통신.maile(Standard_slutpunkt, mail, portnummer, data);
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public String modtage() throws I_O_undtagelse {
        try { return 통신.modtage(Standard_slutpunkt);
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public void TIMEOUT(int 밀리초) throws I_O_undtagelse {
        try { 통신.TIMEOUT(Standard_slutpunkt, 밀리초);
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public int portnummer() { return Standard_slutpunkt.getLocalPort(); }
    public boolean it_lukket() { return Standard_slutpunkt.isClosed(); }
    public void Luk() { 통신.Luk(Standard_slutpunkt); }
}
