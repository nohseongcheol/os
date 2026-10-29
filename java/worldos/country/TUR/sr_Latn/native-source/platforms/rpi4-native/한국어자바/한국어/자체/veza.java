// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** veze(連結)·Kanal_stavka(通路): 상대와 이어진 TCP bajt_VALUE 흐름의 učesnik. */
public final class veza {
    private final java.net.Socket 표준연결;
    veza(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static veza otvoren(String adresa, int broj_porta) throws U_I_izuzetak {
        try {
            return new veza(new java.net.Socket(adresa, broj_porta));
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public 입력흐름 입력() throws U_I_izuzetak {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public 출력흐름 출력() throws U_I_izuzetak {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public void TIMEOUT(int 밀리초) throws U_I_izuzetak {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public int broj_porta() { return 표준연결.getPort(); }
    public int lokalni_broj_porta() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Zatvori() throws U_I_izuzetak {
        try { 표준연결.close();
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
}
