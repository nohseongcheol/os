// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 بەکارهێنەر 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class فایل {
    private فایل() {}
    public static byte[] 바이트읽기(String ناو) throws 입출력예외 {
        try {
        FileInputStream Stream_نرخ = new FileInputStream(ناو);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, نرخ;
            while ((نرخ = Stream_نرخ.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("فایل گۆڕینی_ئەندازە 제한"); 임시[수++] = (byte)نرخ; }
            byte[] 결과 = new byte[수]; System.arraycopy(임시, 0, 결과, 0, 수); return 결과;
        } finally { Stream_نرخ.close(); }
        } catch (java.io.IOException هەڵە) { throw 예외변환.I_O(هەڵە); }
        catch (RuntimeException هەڵە) { throw 예외변환.جێبەجێکردن_فەرمان(هەڵە); }
    }
    public static void ڕایت_کردن_بایت_نرخ(String ناو, byte[] ناوەرۆک_نرخ) throws 입출력예외 {
        try {
        FileOutputStream Stream_نرخ = new FileOutputStream(ناو);
        try { for (int گێژەن_پێرست = 0; گێژەن_پێرست < ناوەرۆک_نرخ.length; گێژەن_پێرست++) Stream_نرخ.write(ناوەرۆک_نرخ[گێژەن_پێرست] & 255); } finally { Stream_نرخ.close(); }
        } catch (java.io.IOException هەڵە) { throw 예외변환.I_O(هەڵە); }
        catch (RuntimeException هەڵە) { throw 예외변환.جێبەجێکردن_فەرمان(هەڵە); }
    }
    public static String 읽기(String ناو) throws 입출력예외 {
        try { return 문자.بێڕەمز_کردن_دەیتا(바이트읽기(ناو));
        } catch (java.io.IOException هەڵە) { throw 예외변환.I_O(هەڵە); }
        catch (RuntimeException هەڵە) { throw 예외변환.جێبەجێکردن_فەرمان(هەڵە); }
    }
    public static void ڕایت_کردن(String ناو, String ناوەرۆک_نرخ) throws 입출력예외 {
        try { ڕایت_کردن_بایت_نرخ(ناو, 문자.부호화(ناوەرۆک_نرخ));
        } catch (java.io.IOException هەڵە) { throw 예외변환.I_O(هەڵە); }
        catch (RuntimeException هەڵە) { throw 예외변환.جێبەجێکردن_فەرمان(هەڵە); }
    }
}
