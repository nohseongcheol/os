// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.własny;

/** odbierać_WARTOŚĆ(受信)·port_WARTOŚĆ(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class odbierać_port {
    private final java.net.ServerSocket Standard_port;
    private odbierać_port(int numer_portu) throws We_Wy_wyjątek {
        try { Standard_port = new java.net.ServerSocket(numer_portu);
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public static odbierać_port Otwórz(int numer_portu) throws We_Wy_wyjątek {
        try { return new odbierać_port(numer_portu);
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public połączenie odbierać() throws We_Wy_wyjątek {
        try { return new połączenie(Standard_port.accept());
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public int numer_portu() { return Standard_port.getLocalPort(); }
    public void TIMEOUT(int 밀리초) throws We_Wy_wyjątek {
        try { Standard_port.setSoTimeout(밀리초);
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public boolean systemy_informacyjne_zamknięta() { return Standard_port.isClosed(); }
    public void Zamknięte() throws We_Wy_wyjątek {
        try { Standard_port.close();
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
}
