// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 صارف 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class فائل {
    private فائل() {}
    public static byte[] 바이트읽기(String ناں) throws 입출력예외 {
        try {
        FileInputStream سٹریم_قدر = new FileInputStream(ناں);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, قدر;
            while ((قدر = سٹریم_قدر.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("فائل سائز 제한"); 임시[수++] = (byte)قدر; }
            byte[] 결과 = new byte[수]; System.arraycopy(임시, 0, 결과, 0, 수); return 결과;
        } finally { سٹریم_قدر.close(); }
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.نفاذ_کرو_حکم(نقص); }
    }
    public static void لکھو_بائٹ_قدر(String ناں, byte[] اجزاء_قدر) throws 입출력예외 {
        try {
        FileOutputStream سٹریم_قدر = new FileOutputStream(ناں);
        try { for (int لوپ_اشاریہ = 0; لوپ_اشاریہ < اجزاء_قدر.length; لوپ_اشاریہ++) سٹریم_قدر.write(اجزاء_قدر[لوپ_اشاریہ] & 255); } finally { سٹریم_قدر.close(); }
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.نفاذ_کرو_حکم(نقص); }
    }
    public static String 읽기(String ناں) throws 입출력예외 {
        try { return 문자.ضابطہ_کشائی_کرو_کوائف(바이트읽기(ناں));
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.نفاذ_کرو_حکم(نقص); }
    }
    public static void لکھو(String ناں, String اجزاء_قدر) throws 입출력예외 {
        try { لکھو_بائٹ_قدر(ناں, 문자.부호화(اجزاء_قدر));
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.نفاذ_کرو_حکم(نقص); }
    }
}
