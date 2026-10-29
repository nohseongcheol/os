// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 корисник 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class фајл {
    private фајл() {}
    public static byte[] 바이트읽기(String назив) throws 입출력예외 {
        try {
        FileInputStream ток_вриједност = new FileInputStream(назив);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, вриједност;
            while ((вриједност = ток_вриједност.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("фајл подесити_величину 제한"); 임시[수++] = (byte)вриједност; }
            byte[] 결과 = new byte[수]; System.arraycopy(임시, 0, 결과, 0, 수); return 결과;
        } finally { ток_вриједност.close(); }
        } catch (java.io.IOException грешка) { throw 예외변환.У_И(грешка); }
        catch (RuntimeException грешка) { throw 예외변환.실행(грешка); }
    }
    public static void писати_бајт_вриједност(String назив, byte[] Садржај_вриједност) throws 입출력예외 {
        try {
        FileOutputStream ток_вриједност = new FileOutputStream(назив);
        try { for (int петља_индекс = 0; петља_индекс < Садржај_вриједност.length; петља_индекс++) ток_вриједност.write(Садржај_вриједност[петља_индекс] & 255); } finally { ток_вриједност.close(); }
        } catch (java.io.IOException грешка) { throw 예외변환.У_И(грешка); }
        catch (RuntimeException грешка) { throw 예외변환.실행(грешка); }
    }
    public static String 읽기(String назив) throws 입출력예외 {
        try { return 문자.дешифрирати_подаци(바이트읽기(назив));
        } catch (java.io.IOException грешка) { throw 예외변환.У_И(грешка); }
        catch (RuntimeException грешка) { throw 예외변환.실행(грешка); }
    }
    public static void писати(String назив, String Садржај_вриједност) throws 입출력예외 {
        try { писати_бајт_вриједност(назив, 문자.부호화(Садржај_вриједност));
        } catch (java.io.IOException грешка) { throw 예외변환.У_И(грешка); }
        catch (RuntimeException грешка) { throw 예외변환.실행(грешка); }
    }
}
