// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.własny;
import java.net.*;
public final class połączenie_transport {
    private połączenie_transport() {}
    public static połączenie Otwórz(String Adres, int numer_portu) throws We_Wy_wyjątek {
        try { return połączenie.Otwórz(Adres, numer_portu);
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public static odbierać_port 수신열기(int numer_portu) throws We_Wy_wyjątek {
        try { return odbierać_port.Otwórz(numer_portu);
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public static Socket Połącz(String Adres, int port_WARTOŚĆ) throws We_Wy_wyjątek {
        try { return new Socket(Adres, port_WARTOŚĆ);
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public static ServerSocket nasłuchiwać_uczestnik(int port_WARTOŚĆ) throws We_Wy_wyjątek {
        try { return new ServerSocket(port_WARTOŚĆ);
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public static Socket odbierać(ServerSocket serwer_WARTOŚĆ) throws We_Wy_wyjątek {
        try { return serwer_WARTOŚĆ.accept();
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
}
