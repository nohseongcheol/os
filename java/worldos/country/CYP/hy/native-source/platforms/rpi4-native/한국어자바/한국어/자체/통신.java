// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 թվանշան_արժեք 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Բաց(int միացք_արժեք) throws 입출력예외 {
        try { return new DatagramSocket(միացք_արժեք);
        } catch (java.io.IOException Սխալ) { throw 예외변환.ներածում_արտածում(Սխալ); }
        catch (RuntimeException Սխալ) { throw 예외변환.կատարել_հրաման(Սխալ); }
    }
    public static void ուղարկել(DatagramSocket 종단, int միացք_արժեք, String Բովանդակություն_արժեք) throws 입출력예외 {
        try {
        ուղարկել(종단, "127.0.0.1", միացք_արժեք, Բովանդակություն_արժեք);
        } catch (java.io.IOException Սխալ) { throw 예외변환.ներածում_արտածում(Սխալ); }
        catch (RuntimeException Սխալ) { throw 예외변환.կատարել_հրաման(Սխալ); }
    }
    public static void ուղարկել(DatagramSocket 종단, String հասցե, int միացք_արժեք, String Բովանդակություն_արժեք) throws 입출력예외 {
        try {
        byte[] բայթ_արժեք = 문자.부호화(Բովանդակություն_արժեք);
        종단.send(new DatagramPacket(բայթ_արժեք, բայթ_արժեք.length, InetAddress.getByName(հասցե), միացք_արժեք));
        } catch (java.io.IOException Սխալ) { throw 예외변환.ներածում_արտածում(Սխալ); }
        catch (RuntimeException Սխալ) { throw 예외변환.կատարել_հրաման(Սխալ); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] բայթ_արժեք = new byte[512]; DatagramPacket 전문 = new DatagramPacket(բայթ_արժեք, բայթ_արժեք.length); 종단.receive(전문);
        byte[] չափ = new byte[전문.getLength()]; System.arraycopy(բայթ_արժեք, 0, չափ, 0, չափ.length); return 문자.վերծանել_տվյալ(չափ);
        } catch (java.io.IOException Սխալ) { throw 예외변환.ներածում_արտածում(Սխալ); }
        catch (RuntimeException Սխալ) { throw 예외변환.կատարել_հրաման(Սխալ); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException Սխալ) { throw 예외변환.ներածում_արտածում(Սխալ); }
        catch (RuntimeException Սխալ) { throw 예외변환.կատարել_հրաման(Սխալ); }
    }
    public static void Փակ(DatagramSocket 종단) { 종단.close(); }
}
