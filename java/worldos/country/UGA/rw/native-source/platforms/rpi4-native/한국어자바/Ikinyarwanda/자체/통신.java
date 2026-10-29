// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ikinyarwanda.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 umubare_agaciro 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Gufungura(int poti_agaciro) throws 입출력예외 {
        try { return new DatagramSocket(poti_agaciro);
        } catch (java.io.IOException IKOSA) { throw 예외변환.I_O(IKOSA); }
        catch (RuntimeException IKOSA) { throw 예외변환.gukora_ibwiriza(IKOSA); }
    }
    public static void kohereza(DatagramSocket 종단, int poti_agaciro, String Ibirimo_agaciro) throws 입출력예외 {
        try {
        kohereza(종단, "127.0.0.1", poti_agaciro, Ibirimo_agaciro);
        } catch (java.io.IOException IKOSA) { throw 예외변환.I_O(IKOSA); }
        catch (RuntimeException IKOSA) { throw 예외변환.gukora_ibwiriza(IKOSA); }
    }
    public static void kohereza(DatagramSocket 종단, String aderesi, int poti_agaciro, String Ibirimo_agaciro) throws 입출력예외 {
        try {
        byte[] bayiti_agaciro = 문자.부호화(Ibirimo_agaciro);
        종단.send(new DatagramPacket(bayiti_agaciro, bayiti_agaciro.length, InetAddress.getByName(aderesi), poti_agaciro));
        } catch (java.io.IOException IKOSA) { throw 예외변환.I_O(IKOSA); }
        catch (RuntimeException IKOSA) { throw 예외변환.gukora_ibwiriza(IKOSA); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] bayiti_agaciro = new byte[512]; DatagramPacket 전문 = new DatagramPacket(bayiti_agaciro, bayiti_agaciro.length); 종단.receive(전문);
        byte[] 결과 = new byte[전문.getLength()]; System.arraycopy(bayiti_agaciro, 0, 결과, 0, 결과.length); return 문자.gusobanura_amakurushingiro(결과);
        } catch (java.io.IOException IKOSA) { throw 예외변환.I_O(IKOSA); }
        catch (RuntimeException IKOSA) { throw 예외변환.gukora_ibwiriza(IKOSA); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException IKOSA) { throw 예외변환.I_O(IKOSA); }
        catch (RuntimeException IKOSA) { throw 예외변환.gukora_ibwiriza(IKOSA); }
    }
    public static void Gufunga(DatagramSocket 종단) { 종단.close(); }
}
