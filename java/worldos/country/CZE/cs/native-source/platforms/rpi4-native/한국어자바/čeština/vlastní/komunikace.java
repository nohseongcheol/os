// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package čeština.vlastní;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** komunikace(通信): IPv4 UDP datagram. externí_HODNOTA 주소는 číslice_HODNOTA 주소를 사용한다. */
public final class komunikace {
    private komunikace() {}
    public static DatagramSocket Otevřít(int port_HODNOTA) throws vstup_a_výstup_výjimka {
        try { return new DatagramSocket(port_HODNOTA);
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public static void poslat(DatagramSocket účastník, int port_HODNOTA, String Obsah_HODNOTA) throws vstup_a_výstup_výjimka {
        try {
        poslat(účastník, "127.0.0.1", port_HODNOTA, Obsah_HODNOTA);
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public static void poslat(DatagramSocket účastník, String Adresa, int port_HODNOTA, String Obsah_HODNOTA) throws vstup_a_výstup_výjimka {
        try {
        byte[] bajt_HODNOTA = 문자.kódovat(Obsah_HODNOTA);
        účastník.send(new DatagramPacket(bajt_HODNOTA, bajt_HODNOTA.length, InetAddress.getByName(Adresa), port_HODNOTA));
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public static String dostat(DatagramSocket účastník) throws vstup_a_výstup_výjimka {
        try {
        byte[] bajt_HODNOTA = new byte[512]; DatagramPacket datagram = new DatagramPacket(bajt_HODNOTA, bajt_HODNOTA.length); účastník.receive(datagram);
        byte[] VÝSLEDEK = new byte[datagram.getLength()]; System.arraycopy(bajt_HODNOTA, 0, VÝSLEDEK, 0, VÝSLEDEK.length); return 문자.dešifrovat_data(VÝSLEDEK);
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public static void TIMEOUT(DatagramSocket účastník, int 밀리초) throws vstup_a_výstup_výjimka {
        try { účastník.setSoTimeout(밀리초);
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public static void Zavřené(DatagramSocket účastník) { účastník.close(); }
}
