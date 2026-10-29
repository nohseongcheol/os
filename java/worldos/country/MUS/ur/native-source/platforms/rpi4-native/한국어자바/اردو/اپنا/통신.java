// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package اردو.اپنا;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 عدد_قدر 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket کھولیں(int پورٹ_قدر) throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { return new DatagramSocket(پورٹ_قدر);
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public static void بھیجیں(DatagramSocket 종단, int پورٹ_قدر, String مشمول_قدر) throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try {
        بھیجیں(종단, "127.0.0.1", پورٹ_قدر, مشمول_قدر);
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public static void بھیجیں(DatagramSocket 종단, String پتہ, int پورٹ_قدر, String مشمول_قدر) throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try {
        byte[] بائٹ_قدر = 문자.부호화(مشمول_قدر);
        종단.send(new DatagramPacket(بائٹ_قدر, بائٹ_قدر.length, InetAddress.getByName(پتہ), پورٹ_قدر));
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public static String 받기(DatagramSocket 종단) throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try {
        byte[] بائٹ_قدر = new byte[512]; DatagramPacket 전문 = new DatagramPacket(بائٹ_قدر, بائٹ_قدر.length); 종단.receive(전문);
        byte[] پیمائش = new byte[전문.getLength()]; System.arraycopy(بائٹ_قدر, 0, پیمائش, 0, پیمائش.length); return 문자.خفیہ_کشائی_کریں_کوائف(پیمائش);
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public static void ٹائم_آؤٹ(DatagramSocket 종단, int 밀리초) throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public static void بند_کریں(DatagramSocket 종단) { 종단.close(); }
}
