// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svenska.eget;

/** datagram(電文)·Kanal_post(通路): 경계를 가진 UDP 자료를 주고받는 deltagare. */
public final class datagram_Kanal {
    private final java.net.DatagramSocket Standard_deltagare;
    private datagram_Kanal(int portnummer) throws indata_utleverans_fel {
        try { Standard_deltagare = kommunikation.Öppna(portnummer);
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public static datagram_Kanal Öppna(int portnummer) throws indata_utleverans_fel {
        try { return new datagram_Kanal(portnummer);
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public void skicka(String Adress, int portnummer, String data) throws indata_utleverans_fel {
        try { kommunikation.skicka(Standard_deltagare, Adress, portnummer, data);
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public String få() throws indata_utleverans_fel {
        try { return kommunikation.få(Standard_deltagare);
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public void TIMEOUT(int 밀리초) throws indata_utleverans_fel {
        try { kommunikation.TIMEOUT(Standard_deltagare, 밀리초);
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public int portnummer() { return Standard_deltagare.getLocalPort(); }
    public boolean informationsteknik_stängd() { return Standard_deltagare.isClosed(); }
    public void Stäng() { kommunikation.Stäng(Standard_deltagare); }
}
