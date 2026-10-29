// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाली.निज;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 प्रयोगकर्ता 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class फाइल {
    private फाइल() {}
    public static byte[] 바이트읽기(String नाम) throws 입출력예외 {
        try {
        FileInputStream प्रवाह_मान = new FileInputStream(नाम);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, मान;
            while ((मान = प्रवाह_मान.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("फाइल आकार 제한"); 임시[수++] = (byte)मान; }
            byte[] मापन = new byte[수]; System.arraycopy(임시, 0, मापन, 0, 수); return मापन;
        } finally { प्रवाह_मान.close(); }
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
    public static void लेख्नुहोस्_बाइट_मान(String नाम, byte[] सामग्री_मान) throws 입출력예외 {
        try {
        FileOutputStream प्रवाह_मान = new FileOutputStream(नाम);
        try { for (int लुप_अनुक्रमणिका = 0; लुप_अनुक्रमणिका < सामग्री_मान.length; लुप_अनुक्रमणिका++) प्रवाह_मान.write(सामग्री_मान[लुप_अनुक्रमणिका] & 255); } finally { प्रवाह_मान.close(); }
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
    public static String पढनुहोस्(String नाम) throws 입출력예외 {
        try { return 문자.गुप्तलेखन_उल्टाउनुहोस्_लगत(바이트읽기(नाम));
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
    public static void लेख्नुहोस्(String नाम, String सामग्री_मान) throws 입출력예외 {
        try { लेख्नुहोस्_बाइट_मान(नाम, 문자.부호화(सामग्री_मान));
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
}
