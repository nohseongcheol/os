// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package हिंदी.निज;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 उपयोगकर्ता 용어를 보존한다. अद्यतित_आइटम 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class संचिका {
    private संचिका() {}
    public static byte[] पढें_बाइट_मान(String नाम) throws इनपुट_आउटपुट_अपवाद {
        try {
        FileInputStream स्ट्रीम_मान = new FileInputStream(नाम);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, मान;
            while ((मान = स्ट्रीम_मान.read()) != -1) { if (수 == 임시.length) throw new इनपुट_आउटपुट_अपवाद("संचिका आकार 제한"); 임시[수++] = (byte)मान; }
            byte[] परिणाम = new byte[수]; System.arraycopy(임시, 0, परिणाम, 0, 수); return परिणाम;
        } finally { स्ट्रीम_मान.close(); }
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public static void लिखना_बाइट_मान(String नाम, byte[] सामग्री_मान) throws इनपुट_आउटपुट_अपवाद {
        try {
        FileOutputStream स्ट्रीम_मान = new FileOutputStream(नाम);
        try { for (int लूप_इंडेक्स = 0; लूप_इंडेक्स < सामग्री_मान.length; लूप_इंडेक्स++) स्ट्रीम_मान.write(सामग्री_मान[लूप_इंडेक्स] & 255); } finally { स्ट्रीम_मान.close(); }
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public static String पढ़ें(String नाम) throws इनपुट_आउटपुट_अपवाद {
        try { return 문자.डिक्रिप्ट_करें_डेटा(पढें_बाइट_मान(नाम));
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public static void लिखें(String नाम, String सामग्री_मान) throws इनपुट_आउटपुट_अपवाद {
        try { लिखना_बाइट_मान(नाम, 문자.부호화(सामग्री_मान));
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
}
