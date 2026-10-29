// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package اردو.اپنا;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 صارف 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class فائل_کا_نام {
    private فائل_کا_نام() {}
    public static byte[] 바이트읽기(String نام) throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try {
        FileInputStream بہاؤ_قدر = new FileInputStream(نام);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, قدر;
            while ((قدر = بہاؤ_قدر.read()) != -1) { if (수 == 임시.length) throw new ان_پٹ_آؤٹ_پٹ_استثنا("فائل_کا_نام حجم 제한"); 임시[수++] = (byte)قدر; }
            byte[] پیمائش = new byte[수]; System.arraycopy(임시, 0, پیمائش, 0, 수); return پیمائش;
        } finally { بہاؤ_قدر.close(); }
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public static void لکھیں_بائٹ_قدر(String نام, byte[] مشمول_قدر) throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try {
        FileOutputStream بہاؤ_قدر = new FileOutputStream(نام);
        try { for (int لوپ_اشاریہ = 0; لوپ_اشاریہ < مشمول_قدر.length; لوپ_اشاریہ++) بہاؤ_قدر.write(مشمول_قدر[لوپ_اشاریہ] & 255); } finally { بہاؤ_قدر.close(); }
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public static String پڑھیں(String نام) throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { return 문자.خفیہ_کشائی_کریں_کوائف(바이트읽기(نام));
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public static void لکھیں(String نام, String مشمول_قدر) throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { لکھیں_بائٹ_قدر(نام, 문자.부호화(مشمول_قدر));
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
}
