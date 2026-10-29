// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package norsk.eget;

/** Koble_til(連結)·Kanal_oppføring(通路): 상대와 이어진 TCP byte_VERDI 흐름의 deltaker. */
public final class kontakt {
    private final java.net.Socket Standard_bibliotek_bro;
    kontakt(java.net.Socket Standard_bibliotek_bro) { this.Standard_bibliotek_bro = Standard_bibliotek_bro; }
    public static kontakt Åpne(String e_post, int portnummer) throws I_U_unntak {
        try {
            return new kontakt(new java.net.Socket(e_post, portnummer));
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public inndataflyt inndata_VERDI() throws I_U_unntak {
        try { return new inndataflyt(Standard_bibliotek_bro.getInputStream());
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public utdataflyt Utgang() throws I_U_unntak {
        try { return new utdataflyt(Standard_bibliotek_bro.getOutputStream());
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public void TIMEOUT(int 밀리초) throws I_U_unntak {
        try { Standard_bibliotek_bro.setSoTimeout(밀리초);
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public int portnummer() { return Standard_bibliotek_bro.getPort(); }
    public int lokal_portnummer() { return Standard_bibliotek_bro.getLocalPort(); }
    public boolean informasjonssystemer_lukket() { return Standard_bibliotek_bro.isClosed(); }
    public boolean 연결됨() { return Standard_bibliotek_bro.isConnected(); }
    public void Lukk() throws I_U_unntak {
        try { Standard_bibliotek_bro.close();
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
}
