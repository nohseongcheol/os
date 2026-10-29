// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 ئىشلەتكۈچى 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class ھۆججەت {
    private ھۆججەت() {}
    public static byte[] 바이트읽기(String ئاتى) throws 입출력예외 {
        try {
        FileInputStream ئېقىم_قىممىتى = new FileInputStream(ئاتى);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, قىممىتى;
            while ((قىممىتى = ئېقىم_قىممىتى.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("ھۆججەت چوڭلۇقى 제한"); 임시[수++] = (byte)قىممىتى; }
            byte[] ئۆلچەم = new byte[수]; System.arraycopy(임시, 0, ئۆلچەم, 0, 수); return ئۆلچەم;
        } finally { ئېقىم_قىممىتى.close(); }
        } catch (java.io.IOException خاتالىق) { throw 예외변환.입출력(خاتالىق); }
        catch (RuntimeException خاتالىق) { throw 예외변환.ئىجرا_قىلىش_بۇيرۇق(خاتالىق); }
    }
    public static void يازماق_بايت_قىممىتى(String ئاتى, byte[] مەزمۇن_قىممىتى) throws 입출력예외 {
        try {
        FileOutputStream ئېقىم_قىممىتى = new FileOutputStream(ئاتى);
        try { for (int ئايلانما_ئىندېكس = 0; ئايلانما_ئىندېكس < مەزمۇن_قىممىتى.length; ئايلانما_ئىندېكس++) ئېقىم_قىممىتى.write(مەزمۇن_قىممىتى[ئايلانما_ئىندېكس] & 255); } finally { ئېقىم_قىممىتى.close(); }
        } catch (java.io.IOException خاتالىق) { throw 예외변환.입출력(خاتالىق); }
        catch (RuntimeException خاتالىق) { throw 예외변환.ئىجرا_قىلىش_بۇيرۇق(خاتالىق); }
    }
    public static String ئوقۇ(String ئاتى) throws 입출력예외 {
        try { return 문자.شىفىر_يېشىش_مەلۇمات(바이트읽기(ئاتى));
        } catch (java.io.IOException خاتالىق) { throw 예외변환.입출력(خاتالىق); }
        catch (RuntimeException خاتالىق) { throw 예외변환.ئىجرا_قىلىش_بۇيرۇق(خاتالىق); }
    }
    public static void ياز(String ئاتى, String مەزمۇن_قىممىتى) throws 입출력예외 {
        try { يازماق_بايت_قىممىتى(ئاتى, 문자.부호화(مەزمۇن_قىممىتى));
        } catch (java.io.IOException خاتالىق) { throw 예외변환.입출력(خاتالىق); }
        catch (RuntimeException خاتالىق) { throw 예외변환.ئىجرا_قىلىش_بۇيرۇق(خاتالىق); }
    }
}
