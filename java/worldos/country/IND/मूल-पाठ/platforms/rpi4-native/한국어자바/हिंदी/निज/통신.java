// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package हिंदी.निज;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP स्वतंत्रसंदेश. बाहरी_मान 주소는 अंक_मान 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket खोलें(int पोर्ट_मान) throws इनपुट_आउटपुट_अपवाद {
        try { return new DatagramSocket(पोर्ट_मान);
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public static void भेजें(DatagramSocket एंडपॉइंट, int पोर्ट_मान, String सामग्री_मान) throws इनपुट_आउटपुट_अपवाद {
        try {
        भेजें(एंडपॉइंट, "127.0.0.1", पोर्ट_मान, सामग्री_मान);
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public static void भेजें(DatagramSocket एंडपॉइंट, String पता, int पोर्ट_मान, String सामग्री_मान) throws इनपुट_आउटपुट_अपवाद {
        try {
        byte[] बाइट_मान = 문자.부호화(सामग्री_मान);
        एंडपॉइंट.send(new DatagramPacket(बाइट_मान, बाइट_मान.length, InetAddress.getByName(पता), पोर्ट_मान));
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public static String 받기(DatagramSocket एंडपॉइंट) throws इनपुट_आउटपुट_अपवाद {
        try {
        byte[] बाइट_मान = new byte[512]; DatagramPacket स्वतंत्रसंदेश = new DatagramPacket(बाइट_मान, बाइट_मान.length); एंडपॉइंट.receive(स्वतंत्रसंदेश);
        byte[] परिणाम = new byte[स्वतंत्रसंदेश.getLength()]; System.arraycopy(बाइट_मान, 0, परिणाम, 0, परिणाम.length); return 문자.डिक्रिप्ट_करें_डेटा(परिणाम);
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public static void 대기시간(DatagramSocket एंडपॉइंट, int 밀리초) throws इनपुट_आउटपुट_अपवाद {
        try { एंडपॉइंट.setSoTimeout(밀리초);
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public static void बंदकरें(DatagramSocket एंडपॉइंट) { एंडपॉइंट.close(); }
}
