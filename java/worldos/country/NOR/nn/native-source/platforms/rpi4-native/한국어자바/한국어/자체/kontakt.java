// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** Kopla_til(連結)·kanal_oppføring(通路): 상대와 이어진 TCP byte_VALUE 흐름의 endepunkt. */
public final class kontakt {
    private final java.net.Socket 표준연결;
    kontakt(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static kontakt Opna(String ADDRESS, int portnummer) throws I_U_unntak {
        try {
            return new kontakt(new java.net.Socket(ADDRESS, portnummer));
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public 입력흐름 입력() throws I_U_unntak {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public 출력흐름 Utdata() throws I_U_unntak {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public void TIMEOUT(int 밀리초) throws I_U_unntak {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public int portnummer() { return 표준연결.getPort(); }
    public int lokal_portnummer() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Lukk() throws I_U_unntak {
        try { 표준연결.close();
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
}
