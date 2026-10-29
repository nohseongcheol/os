// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 అంకె_మూల్యం 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket తెరువు(int పోర్టు_మూల్యం) throws మూ_ఫ_మినహాయింపు {
        try { return new DatagramSocket(పోర్టు_మూల్యం);
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public static void పంపు(DatagramSocket 종단, int పోర్టు_మూల్యం, String విషయం_మూల్యం) throws మూ_ఫ_మినహాయింపు {
        try {
        పంపు(종단, "127.0.0.1", పోర్టు_మూల్యం, విషయం_మూల్యం);
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public static void పంపు(DatagramSocket 종단, String ఇమెయిల్, int పోర్టు_మూల్యం, String విషయం_మూల్యం) throws మూ_ఫ_మినహాయింపు {
        try {
        byte[] బైట్_మూల్యం = 문자.부호화(విషయం_మూల్యం);
        종단.send(new DatagramPacket(బైట్_మూల్యం, బైట్_మూల్యం.length, InetAddress.getByName(ఇమెయిల్), పోర్టు_మూల్యం));
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public static String 받기(DatagramSocket 종단) throws మూ_ఫ_మినహాయింపు {
        try {
        byte[] బైట్_మూల్యం = new byte[512]; DatagramPacket 전문 = new DatagramPacket(బైట్_మూల్యం, బైట్_మూల్యం.length); 종단.receive(전문);
        byte[] ప్రమాణం = new byte[전문.getLength()]; System.arraycopy(బైట్_మూల్యం, 0, ప్రమాణం, 0, ప్రమాణం.length); return 문자.వ్యక్తపరుచు_డేటా(ప్రమాణం);
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws మూ_ఫ_మినహాయింపు {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public static void మూసివేయి(DatagramSocket 종단) { 종단.close(); }
}
