// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 istifadəçi 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class FAYL {
    private FAYL() {}
    public static byte[] 바이트읽기(String Ad) throws giriş_çıxış_istisna {
        try {
        FileInputStream axın_VALUE = new FileInputStream(Ad);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, VALUE;
            while ((VALUE = axın_VALUE.read()) != -1) { if (수 == 임시.length) throw new giriş_çıxış_istisna("FAYL Böyüklük 제한"); 임시[수++] = (byte)VALUE; }
            byte[] ölçü = new byte[수]; System.arraycopy(임시, 0, ölçü, 0, 수); return ölçü;
        } finally { axın_VALUE.close(); }
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
    public static void yazmaq_bayt_VALUE(String Ad, byte[] Məzmun_VALUE) throws giriş_çıxış_istisna {
        try {
        FileOutputStream axın_VALUE = new FileOutputStream(Ad);
        try { for (int Loop_INDEX = 0; Loop_INDEX < Məzmun_VALUE.length; Loop_INDEX++) axın_VALUE.write(Məzmun_VALUE[Loop_INDEX] & 255); } finally { axın_VALUE.close(); }
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
    public static String Oxuma(String Ad) throws giriş_çıxış_istisna {
        try { return 문자.şifr_açmaq_verilənlər(바이트읽기(Ad));
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
    public static void Yazma(String Ad, String Məzmun_VALUE) throws giriş_çıxış_istisna {
        try { yazmaq_bayt_VALUE(Ad, 문자.부호화(Məzmun_VALUE));
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
}
