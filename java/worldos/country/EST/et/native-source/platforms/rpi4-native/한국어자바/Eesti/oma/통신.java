// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti.oma;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP datagramm. väline_VALUE 주소는 number_VALUE 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Ava(int port_VALUE) throws I_O_erand {
        try { return new DatagramSocket(port_VALUE);
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public static void saatma(DatagramSocket osaleja, int port_VALUE, String Sisu_VALUE) throws I_O_erand {
        try {
        saatma(osaleja, "127.0.0.1", port_VALUE, Sisu_VALUE);
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public static void saatma(DatagramSocket osaleja, String ADDRESS, int port_VALUE, String Sisu_VALUE) throws I_O_erand {
        try {
        byte[] bait_VALUE = 문자.kodeerima(Sisu_VALUE);
        osaleja.send(new DatagramPacket(bait_VALUE, bait_VALUE.length, InetAddress.getByName(ADDRESS), port_VALUE));
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public static String saama(DatagramSocket osaleja) throws I_O_erand {
        try {
        byte[] bait_VALUE = new byte[512]; DatagramPacket datagramm = new DatagramPacket(bait_VALUE, bait_VALUE.length); osaleja.receive(datagramm);
        byte[] TULEMUS = new byte[datagramm.getLength()]; System.arraycopy(bait_VALUE, 0, TULEMUS, 0, TULEMUS.length); return 문자.dekrüptima_andmed(TULEMUS);
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public static void TIMEOUT(DatagramSocket osaleja, int 밀리초) throws I_O_erand {
        try { osaleja.setSoTimeout(밀리초);
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public static void Suletud(DatagramSocket osaleja) { osaleja.close(); }
}
