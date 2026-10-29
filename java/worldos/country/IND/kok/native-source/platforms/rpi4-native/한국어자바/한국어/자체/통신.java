// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 अंक_मोल 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket उगडचें(int पोर्ट_मोल) throws 입출력예외 {
        try { return new DatagramSocket(पोर्ट_मोल);
        } catch (java.io.IOException चूक) { throw 예외변환.I_O(चूक); }
        catch (RuntimeException चूक) { throw 예외변환.पाळो_दिवचो_आदेश(चूक); }
    }
    public static void धाडचें(DatagramSocket 종단, int पोर्ट_मोल, String अनुक्रमणिका_मोल) throws 입출력예외 {
        try {
        धाडचें(종단, "127.0.0.1", पोर्ट_मोल, अनुक्रमणिका_मोल);
        } catch (java.io.IOException चूक) { throw 예외변환.I_O(चूक); }
        catch (RuntimeException चूक) { throw 예외변환.पाळो_दिवचो_आदेश(चूक); }
    }
    public static void धाडचें(DatagramSocket 종단, String नामो, int पोर्ट_मोल, String अनुक्रमणिका_मोल) throws 입출력예외 {
        try {
        byte[] बायट_मोल = 문자.부호화(अनुक्रमणिका_मोल);
        종단.send(new DatagramPacket(बायट_मोल, बायट_मोल.length, InetAddress.getByName(नामो), पोर्ट_मोल));
        } catch (java.io.IOException चूक) { throw 예외변환.I_O(चूक); }
        catch (RuntimeException चूक) { throw 예외변환.पाळो_दिवचो_आदेश(चूक); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] बायट_मोल = new byte[512]; DatagramPacket 전문 = new DatagramPacket(बायट_मोल, बायट_मोल.length); 종단.receive(전문);
        byte[] मेजप = new byte[전문.getLength()]; System.arraycopy(बायट_मोल, 0, मेजप, 0, मेजप.length); return 문자.डिक्रिप्ट_डेटा(मेजप);
        } catch (java.io.IOException चूक) { throw 예외변환.I_O(चूक); }
        catch (RuntimeException चूक) { throw 예외변환.पाळो_दिवचो_आदेश(चूक); }
    }
    public static void कालबाह्य(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException चूक) { throw 예외변환.I_O(चूक); }
        catch (RuntimeException चूक) { throw 예외변환.पाळो_दिवचो_आदेश(चूक); }
    }
    public static void शेवट(DatagramSocket 종단) { 종단.close(); }
}
