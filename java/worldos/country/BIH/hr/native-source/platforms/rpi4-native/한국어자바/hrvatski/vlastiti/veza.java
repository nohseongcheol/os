// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package hrvatski.vlastiti;

/** Spoji_se(連結)·kanal_unos(通路): 상대와 이어진 TCP bajt_VALUE 흐름의 sudionik. */
public final class veza {
    private final java.net.Socket 표준연결;
    veza(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static veza Otvori(String adresa, int broj_priključka) throws U_I_iznimka {
        try {
            return new veza(new java.net.Socket(adresa, broj_priključka));
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public ulazni_tok 입력() throws U_I_iznimka {
        try { return new ulazni_tok(표준연결.getInputStream());
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public izlazni_tok Izlaz() throws U_I_iznimka {
        try { return new izlazni_tok(표준연결.getOutputStream());
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public void TIMEOUT(int 밀리초) throws U_I_iznimka {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public int broj_priključka() { return 표준연결.getPort(); }
    public int lokalno_broj_priključka() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Zatvori() throws U_I_iznimka {
        try { 표준연결.close();
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
}
