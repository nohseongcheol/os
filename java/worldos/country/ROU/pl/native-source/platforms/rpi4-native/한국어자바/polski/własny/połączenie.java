// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.własny;

/** Połącz(連結)·Kanał_wpis(通路): 상대와 이어진 TCP bajt_WARTOŚĆ 흐름의 uczestnik. */
public final class połączenie {
    private final java.net.Socket Standard_biblioteka_mostek;
    połączenie(java.net.Socket Standard_biblioteka_mostek) { this.Standard_biblioteka_mostek = Standard_biblioteka_mostek; }
    public static połączenie Otwórz(String Adres, int numer_portu) throws We_Wy_wyjątek {
        try {
            return new połączenie(new java.net.Socket(Adres, numer_portu));
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public strumień_wejściowy wejście_WARTOŚĆ() throws We_Wy_wyjątek {
        try { return new strumień_wejściowy(Standard_biblioteka_mostek.getInputStream());
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public strumień_wyjściowy pozycja_wyjścia() throws We_Wy_wyjątek {
        try { return new strumień_wyjściowy(Standard_biblioteka_mostek.getOutputStream());
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public void TIMEOUT(int 밀리초) throws We_Wy_wyjątek {
        try { Standard_biblioteka_mostek.setSoTimeout(밀리초);
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public int numer_portu() { return Standard_biblioteka_mostek.getPort(); }
    public int lokalny_numer_portu() { return Standard_biblioteka_mostek.getLocalPort(); }
    public boolean systemy_informacyjne_zamknięta() { return Standard_biblioteka_mostek.isClosed(); }
    public boolean 연결됨() { return Standard_biblioteka_mostek.isConnected(); }
    public void Zamknięte() throws We_Wy_wyjątek {
        try { Standard_biblioteka_mostek.close();
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
}
