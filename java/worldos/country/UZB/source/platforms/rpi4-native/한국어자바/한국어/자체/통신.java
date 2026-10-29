// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 raqam_VALUE 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Ochish(int port_VALUE) throws I_O_istisno {
        try { return new DatagramSocket(port_VALUE);
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public static void yuborish(DatagramSocket 종단, int port_VALUE, String tarkib_VALUE) throws I_O_istisno {
        try {
        yuborish(종단, "127.0.0.1", port_VALUE, tarkib_VALUE);
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public static void yuborish(DatagramSocket 종단, String manzil, int port_VALUE, String tarkib_VALUE) throws I_O_istisno {
        try {
        byte[] bayt_VALUE = 문자.부호화(tarkib_VALUE);
        종단.send(new DatagramPacket(bayt_VALUE, bayt_VALUE.length, InetAddress.getByName(manzil), port_VALUE));
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public static String 받기(DatagramSocket 종단) throws I_O_istisno {
        try {
        byte[] bayt_VALUE = new byte[512]; DatagramPacket 전문 = new DatagramPacket(bayt_VALUE, bayt_VALUE.length); 종단.receive(전문);
        byte[] o_lchov = new byte[전문.getLength()]; System.arraycopy(bayt_VALUE, 0, o_lchov, 0, o_lchov.length); return 문자.shifrsizlantirish_ma_lumotlar(o_lchov);
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public static void TANAFFUS(DatagramSocket 종단, int 밀리초) throws I_O_istisno {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public static void Yopish(DatagramSocket 종단) { 종단.close(); }
}
