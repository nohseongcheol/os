// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Dansk.eget;

/** Tilslut(連結)·Kanal_post(通路): 상대와 이어진 TCP byte_VÆRDI 흐름의 slutpunkt. */
public final class forbindelse {
    private final java.net.Socket Standard_bibliotek_bro;
    forbindelse(java.net.Socket Standard_bibliotek_bro) { this.Standard_bibliotek_bro = Standard_bibliotek_bro; }
    public static forbindelse Åbn(String mail, int portnummer) throws I_O_undtagelse {
        try {
            return new forbindelse(new java.net.Socket(mail, portnummer));
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public inputstream input_VÆRDI() throws I_O_undtagelse {
        try { return new inputstream(Standard_bibliotek_bro.getInputStream());
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public outputstream Udgang() throws I_O_undtagelse {
        try { return new outputstream(Standard_bibliotek_bro.getOutputStream());
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public void TIMEOUT(int 밀리초) throws I_O_undtagelse {
        try { Standard_bibliotek_bro.setSoTimeout(밀리초);
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public int portnummer() { return Standard_bibliotek_bro.getPort(); }
    public int lokal_portnummer() { return Standard_bibliotek_bro.getLocalPort(); }
    public boolean it_lukket() { return Standard_bibliotek_bro.isClosed(); }
    public boolean 연결됨() { return Standard_bibliotek_bro.isConnected(); }
    public void Luk() throws I_O_undtagelse {
        try { Standard_bibliotek_bro.close();
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
}
