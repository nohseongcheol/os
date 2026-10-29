// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाली.निज;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 अङ्क_मान 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket खोल्नुहोस्(int पोर्ट_मान) throws 입출력예외 {
        try { return new DatagramSocket(पोर्ट_मान);
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
    public static void पठाउनुहोस्(DatagramSocket 종단, int पोर्ट_मान, String सामग्री_मान) throws 입출력예외 {
        try {
        पठाउनुहोस्(종단, "127.0.0.1", पोर्ट_मान, सामग्री_मान);
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
    public static void पठाउनुहोस्(DatagramSocket 종단, String ठेगाना, int पोर्ट_मान, String सामग्री_मान) throws 입출력예외 {
        try {
        byte[] बाइट_मान = 문자.부호화(सामग्री_मान);
        종단.send(new DatagramPacket(बाइट_मान, बाइट_मान.length, InetAddress.getByName(ठेगाना), पोर्ट_मान));
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] बाइट_मान = new byte[512]; DatagramPacket 전문 = new DatagramPacket(बाइट_मान, बाइट_मान.length); 종단.receive(전문);
        byte[] मापन = new byte[전문.getLength()]; System.arraycopy(बाइट_मान, 0, मापन, 0, मापन.length); return 문자.गुप्तलेखन_उल्टाउनुहोस्_लगत(मापन);
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
    public static void समय_सकियो(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
    public static void बन्दगर्नुहोस्(DatagramSocket 종단) { 종단.close(); }
}
