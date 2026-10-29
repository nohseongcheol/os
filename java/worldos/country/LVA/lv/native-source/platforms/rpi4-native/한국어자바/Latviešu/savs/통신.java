// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latviešu.savs;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP datogramma. ārējs_VALUE 주소는 cipars_VALUE 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Atvērt(int ports_VALUE) throws ievadizvade_izņēmums {
        try { return new DatagramSocket(ports_VALUE);
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public static void sūtīt(DatagramSocket dalībnieks, int ports_VALUE, String Saturs_VALUE) throws ievadizvade_izņēmums {
        try {
        sūtīt(dalībnieks, "127.0.0.1", ports_VALUE, Saturs_VALUE);
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public static void sūtīt(DatagramSocket dalībnieks, String adrese, int ports_VALUE, String Saturs_VALUE) throws ievadizvade_izņēmums {
        try {
        byte[] byte_VALUE = 문자.kodēt(Saturs_VALUE);
        dalībnieks.send(new DatagramPacket(byte_VALUE, byte_VALUE.length, InetAddress.getByName(adrese), ports_VALUE));
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public static String saņemt(DatagramSocket dalībnieks) throws ievadizvade_izņēmums {
        try {
        byte[] byte_VALUE = new byte[512]; DatagramPacket datogramma = new DatagramPacket(byte_VALUE, byte_VALUE.length); dalībnieks.receive(datogramma);
        byte[] mērs = new byte[datogramma.getLength()]; System.arraycopy(byte_VALUE, 0, mērs, 0, mērs.length); return 문자.atšifrēt_dati(mērs);
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public static void NOILGUMS(DatagramSocket dalībnieks, int 밀리초) throws ievadizvade_izņēmums {
        try { dalībnieks.setSoTimeout(밀리초);
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public static void Aizvērt(DatagramSocket dalībnieks) { dalībnieks.close(); }
}
