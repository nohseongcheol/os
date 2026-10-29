// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.własny;

/** datagram(電文)·Kanał_wpis(通路): 경계를 가진 UDP 자료를 주고받는 uczestnik. */
public final class datagram_Kanał {
    private final java.net.DatagramSocket Standard_uczestnik;
    private datagram_Kanał(int numer_portu) throws We_Wy_wyjątek {
        try { Standard_uczestnik = komunikacja.Otwórz(numer_portu);
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public static datagram_Kanał Otwórz(int numer_portu) throws We_Wy_wyjątek {
        try { return new datagram_Kanał(numer_portu);
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public void wysłać(String Adres, int numer_portu, String dane) throws We_Wy_wyjątek {
        try { komunikacja.wysłać(Standard_uczestnik, Adres, numer_portu, dane);
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public String odbierać() throws We_Wy_wyjątek {
        try { return komunikacja.odbierać(Standard_uczestnik);
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public void TIMEOUT(int 밀리초) throws We_Wy_wyjątek {
        try { komunikacja.TIMEOUT(Standard_uczestnik, 밀리초);
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public int numer_portu() { return Standard_uczestnik.getLocalPort(); }
    public boolean systemy_informacyjne_zamknięta() { return Standard_uczestnik.isClosed(); }
    public void Zamknięte() { komunikacja.Zamknięte(Standard_uczestnik); }
}
