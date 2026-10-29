// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package norsk.eget;

/** datagram(電文)·Kanal_oppføring(通路): 경계를 가진 UDP 자료를 주고받는 deltaker. */
public final class datagram_Kanal {
    private final java.net.DatagramSocket Standard_deltaker;
    private datagram_Kanal(int portnummer) throws I_U_unntak {
        try { Standard_deltaker = 통신.Åpne(portnummer);
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public static datagram_Kanal Åpne(int portnummer) throws I_U_unntak {
        try { return new datagram_Kanal(portnummer);
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public void sende(String e_post, int portnummer, String data) throws I_U_unntak {
        try { 통신.sende(Standard_deltaker, e_post, portnummer, data);
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public String motta() throws I_U_unntak {
        try { return 통신.motta(Standard_deltaker);
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public void TIMEOUT(int 밀리초) throws I_U_unntak {
        try { 통신.TIMEOUT(Standard_deltaker, 밀리초);
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public int portnummer() { return Standard_deltaker.getLocalPort(); }
    public boolean informasjonssystemer_lukket() { return Standard_deltaker.isClosed(); }
    public void Lukk() { 통신.Lukk(Standard_deltaker); }
}
