// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 عدد_قدر 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket بنڑاؤ(int دہانہ_قدر) throws 입출력예외 {
        try { return new DatagramSocket(دہانہ_قدر);
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.نفاذ_کرو_حکم(نقص); }
    }
    public static void بھیجو(DatagramSocket 종단, int دہانہ_قدر, String اجزاء_قدر) throws 입출력예외 {
        try {
        بھیجو(종단, "127.0.0.1", دہانہ_قدر, اجزاء_قدر);
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.نفاذ_کرو_حکم(نقص); }
    }
    public static void بھیجو(DatagramSocket 종단, String پتا, int دہانہ_قدر, String اجزاء_قدر) throws 입출력예외 {
        try {
        byte[] بائٹ_قدر = 문자.부호화(اجزاء_قدر);
        종단.send(new DatagramPacket(بائٹ_قدر, بائٹ_قدر.length, InetAddress.getByName(پتا), دہانہ_قدر));
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.نفاذ_کرو_حکم(نقص); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] بائٹ_قدر = new byte[512]; DatagramPacket 전문 = new DatagramPacket(بائٹ_قدر, بائٹ_قدر.length); 종단.receive(전문);
        byte[] 결과 = new byte[전문.getLength()]; System.arraycopy(بائٹ_قدر, 0, 결과, 0, 결과.length); return 문자.ضابطہ_کشائی_کرو_کوائف(결과);
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.نفاذ_کرو_حکم(نقص); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.نفاذ_کرو_حکم(نقص); }
    }
    public static void بند_کرو(DatagramSocket 종단) { 종단.close(); }
}
