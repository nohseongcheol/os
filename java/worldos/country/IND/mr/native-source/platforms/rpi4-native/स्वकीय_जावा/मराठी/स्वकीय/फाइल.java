// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package मराठी.स्वकीय;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** वापरकर्त्याला परिचित संचिका संकल्पना राखते. सध्याच्या RAM संचिका पुनःप्रारंभानंतर नष्ट होतात. */
public final class फाइल {
    private फाइल() {}
    public static byte[] बाइट_मूल्य_वाचा(String नाव) throws इनपुट_आउटपुट_अपवाद {
        try {
        FileInputStream प्रवाह_मूल्य = new FileInputStream(नाव);
        try {
            byte[] तात्पुरते_मूल्य = new byte[16384]; int संख्या = 0, मूल्य;
            while ((मूल्य = प्रवाह_मूल्य.read()) != -1) { if (संख्या == तात्पुरते_मूल्य.length) throw new इनपुट_आउटपुट_अपवाद("संचिकेच्या आकाराची मर्यादा"); तात्पुरते_मूल्य[संख्या++] = (byte)मूल्य; }
            byte[] मोजमाप = new byte[संख्या]; System.arraycopy(तात्पुरते_मूल्य, 0, मोजमाप, 0, संख्या); return मोजमाप;
        } finally { प्रवाह_मूल्य.close(); }
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public static void बाइट_मूल्य_लिहा(String नाव, byte[] सामुग्री_मूल्य) throws इनपुट_आउटपुट_अपवाद {
        try {
        FileOutputStream प्रवाह_मूल्य = new FileOutputStream(नाव);
        try { for (int लूप_अनुक्रमणिका = 0; लूप_अनुक्रमणिका < सामुग्री_मूल्य.length; लूप_अनुक्रमणिका++) प्रवाह_मूल्य.write(सामुग्री_मूल्य[लूप_अनुक्रमणिका] & 255); } finally { प्रवाह_मूल्य.close(); }
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public static String वाचन(String नाव) throws इनपुट_आउटपुट_अपवाद {
        try { return वर्ण.डिक्रिप्ट_करा_डेटा(बाइट_मूल्य_वाचा(नाव));
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public static void लेखन(String नाव, String सामुग्री_मूल्य) throws इनपुट_आउटपुट_अपवाद {
        try { बाइट_मूल्य_लिहा(नाव, वर्ण.संकेतन(सामुग्री_मूल्य));
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
}
