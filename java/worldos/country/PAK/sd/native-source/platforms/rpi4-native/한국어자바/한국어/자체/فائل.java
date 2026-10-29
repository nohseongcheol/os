// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 صارف 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class فائل {
    private فائل() {}
    public static byte[] 바이트읽기(String نالو) throws 입출력예외 {
        try {
        FileInputStream اسٽريم_قدر = new FileInputStream(نالو);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, قدر;
            while ((قدر = اسٽريم_قدر.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("فائل سائيز 제한"); 임시[수++] = (byte)قدر; }
            byte[] 결과 = new byte[수]; System.arraycopy(임시, 0, 결과, 0, 수); return 결과;
        } finally { اسٽريم_قدر.close(); }
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.تعميل_ڪرڻ_حڪم(نقص); }
    }
    public static void لکو_بائٽ_قدر(String نالو, byte[] مواد_قدر) throws 입출력예외 {
        try {
        FileOutputStream اسٽريم_قدر = new FileOutputStream(نالو);
        try { for (int لوپ_ابتدائي = 0; لوپ_ابتدائي < مواد_قدر.length; لوپ_ابتدائي++) اسٽريم_قدر.write(مواد_قدر[لوپ_ابتدائي] & 255); } finally { اسٽريم_قدر.close(); }
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.تعميل_ڪرڻ_حڪم(نقص); }
    }
    public static String 읽기(String نالو) throws 입출력예외 {
        try { return 문자.طئي_ٿيل_ڪوائف(바이트읽기(نالو));
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.تعميل_ڪرڻ_حڪم(نقص); }
    }
    public static void لکو(String نالو, String مواد_قدر) throws 입출력예외 {
        try { لکو_بائٽ_قدر(نالو, 문자.부호화(مواد_قدر));
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.تعميل_ڪرڻ_حڪم(نقص); }
    }
}
