// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svenska.eget;

/** Anslut(連結)·Kanal_post(通路): 상대와 이어진 TCP byte_värde 흐름의 deltagare. */
public final class kontakt {
    private final java.net.Socket Standard_bibliotek_brygga;
    kontakt(java.net.Socket Standard_bibliotek_brygga) { this.Standard_bibliotek_brygga = Standard_bibliotek_brygga; }
    public static kontakt Öppna(String Adress, int portnummer) throws indata_utleverans_fel {
        try {
            return new kontakt(new java.net.Socket(Adress, portnummer));
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public indataström indata_värde() throws indata_utleverans_fel {
        try { return new indataström(Standard_bibliotek_brygga.getInputStream());
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public utdataström utmatningsposition() throws indata_utleverans_fel {
        try { return new utdataström(Standard_bibliotek_brygga.getOutputStream());
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public void TIMEOUT(int 밀리초) throws indata_utleverans_fel {
        try { Standard_bibliotek_brygga.setSoTimeout(밀리초);
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public int portnummer() { return Standard_bibliotek_brygga.getPort(); }
    public int lokal_portnummer() { return Standard_bibliotek_brygga.getLocalPort(); }
    public boolean informationsteknik_stängd() { return Standard_bibliotek_brygga.isClosed(); }
    public boolean 연결됨() { return Standard_bibliotek_brygga.isConnected(); }
    public void Stäng() throws indata_utleverans_fel {
        try { Standard_bibliotek_brygga.close();
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
}
