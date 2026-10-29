// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 rəqəm_VALUE 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Aç(int port_VALUE) throws giriş_çıxış_istisna {
        try { return new DatagramSocket(port_VALUE);
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
    public static void göndərmək(DatagramSocket 종단, int port_VALUE, String Məzmun_VALUE) throws giriş_çıxış_istisna {
        try {
        göndərmək(종단, "127.0.0.1", port_VALUE, Məzmun_VALUE);
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
    public static void göndərmək(DatagramSocket 종단, String ünvan, int port_VALUE, String Məzmun_VALUE) throws giriş_çıxış_istisna {
        try {
        byte[] bayt_VALUE = 문자.부호화(Məzmun_VALUE);
        종단.send(new DatagramPacket(bayt_VALUE, bayt_VALUE.length, InetAddress.getByName(ünvan), port_VALUE));
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
    public static String 받기(DatagramSocket 종단) throws giriş_çıxış_istisna {
        try {
        byte[] bayt_VALUE = new byte[512]; DatagramPacket 전문 = new DatagramPacket(bayt_VALUE, bayt_VALUE.length); 종단.receive(전문);
        byte[] ölçü = new byte[전문.getLength()]; System.arraycopy(bayt_VALUE, 0, ölçü, 0, ölçü.length); return 문자.şifr_açmaq_verilənlər(ölçü);
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
    public static void FASİLƏ(DatagramSocket 종단, int 밀리초) throws giriş_çıxış_istisna {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
    public static void Bağla(DatagramSocket 종단) { 종단.close(); }
}
