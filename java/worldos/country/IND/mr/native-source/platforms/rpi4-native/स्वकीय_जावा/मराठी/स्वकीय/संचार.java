// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package मराठी.स्वकीय;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** IPv4 UDP संदेशांद्वारे संप्रेषण. बाहेरील टोकांसाठी संख्यात्मक पत्ते वापरले जातात. */
public final class संचार {
    private संचार() {}
    public static DatagramSocket उघडा(int पॉर्ट_मूल्य) throws इनपुट_आउटपुट_अपवाद {
        try { return new DatagramSocket(पॉर्ट_मूल्य);
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public static void पाठवा(DatagramSocket संचारटोक, int पॉर्ट_मूल्य, String सामुग्री_मूल्य) throws इनपुट_आउटपुट_अपवाद {
        try {
        पाठवा(संचारटोक, "127.0.0.1", पॉर्ट_मूल्य, सामुग्री_मूल्य);
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public static void पाठवा(DatagramSocket संचारटोक, String पत्ता, int पॉर्ट_मूल्य, String सामुग्री_मूल्य) throws इनपुट_आउटपुट_अपवाद {
        try {
        byte[] बाइट_मूल्य = वर्ण.संकेतन(सामुग्री_मूल्य);
        संचारटोक.send(new DatagramPacket(बाइट_मूल्य, बाइट_मूल्य.length, InetAddress.getByName(पत्ता), पॉर्ट_मूल्य));
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public static String स्वीकारा(DatagramSocket संचारटोक) throws इनपुट_आउटपुट_अपवाद {
        try {
        byte[] बाइट_मूल्य = new byte[512]; DatagramPacket स्वतंत्रसंदेश = new DatagramPacket(बाइट_मूल्य, बाइट_मूल्य.length); संचारटोक.receive(स्वतंत्रसंदेश);
        byte[] मोजमाप = new byte[स्वतंत्रसंदेश.getLength()]; System.arraycopy(बाइट_मूल्य, 0, मोजमाप, 0, मोजमाप.length); return वर्ण.डिक्रिप्ट_करा_डेटा(मोजमाप);
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public static void प्रतीक्षामर्यादा(DatagramSocket संचारटोक, int मिलिसेकंद) throws इनपुट_आउटपुट_अपवाद {
        try { संचारटोक.setSoTimeout(मिलिसेकंद);
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public static void बंद_करा(DatagramSocket संचारटोक) { संचारटोक.close(); }
}
