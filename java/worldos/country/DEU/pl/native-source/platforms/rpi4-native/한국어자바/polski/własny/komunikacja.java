// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.własny;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** komunikacja(通信): IPv4 UDP datagram. zewnętrzny_WARTOŚĆ 주소는 cyfra_WARTOŚĆ 주소를 사용한다. */
public final class komunikacja {
    private komunikacja() {}
    public static DatagramSocket Otwórz(int port_WARTOŚĆ) throws We_Wy_wyjątek {
        try { return new DatagramSocket(port_WARTOŚĆ);
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public static void wysłać(DatagramSocket uczestnik, int port_WARTOŚĆ, String treść_WARTOŚĆ_cb0f2404) throws We_Wy_wyjątek {
        try {
        wysłać(uczestnik, "127.0.0.1", port_WARTOŚĆ, treść_WARTOŚĆ_cb0f2404);
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public static void wysłać(DatagramSocket uczestnik, String Adres, int port_WARTOŚĆ, String treść_WARTOŚĆ_cb0f2404) throws We_Wy_wyjątek {
        try {
        byte[] bajt_WARTOŚĆ = 문자.kodować(treść_WARTOŚĆ_cb0f2404);
        uczestnik.send(new DatagramPacket(bajt_WARTOŚĆ, bajt_WARTOŚĆ.length, InetAddress.getByName(Adres), port_WARTOŚĆ));
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public static String odbierać(DatagramSocket uczestnik) throws We_Wy_wyjątek {
        try {
        byte[] bajt_WARTOŚĆ = new byte[512]; DatagramPacket datagram = new DatagramPacket(bajt_WARTOŚĆ, bajt_WARTOŚĆ.length); uczestnik.receive(datagram);
        byte[] WYNIK = new byte[datagram.getLength()]; System.arraycopy(bajt_WARTOŚĆ, 0, WYNIK, 0, WYNIK.length); return 문자.odszyfrować_dane(WYNIK);
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public static void TIMEOUT(DatagramSocket uczestnik, int 밀리초) throws We_Wy_wyjątek {
        try { uczestnik.setSoTimeout(밀리초);
        } catch (java.io.IOException błąd) { throw KONWERTUJ_wyjątek.We_Wy(błąd); }
        catch (RuntimeException błąd) { throw KONWERTUJ_wyjątek.Wykonaj_polecenie(błąd); }
    }
    public static void Zamknięte(DatagramSocket uczestnik) { uczestnik.close(); }
}
