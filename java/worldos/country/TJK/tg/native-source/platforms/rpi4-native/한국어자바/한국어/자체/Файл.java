// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 корбар 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Файл {
    private Файл() {}
    public static byte[] 바이트읽기(String Ном) throws 입출력예외 {
        try {
        FileInputStream ҷараён_қимат = new FileInputStream(Ном);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, қимат;
            while ((қимат = ҷараён_қимат.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("Файл андоза_кардан 제한"); 임시[수++] = (byte)қимат; }
            byte[] 결과 = new byte[수]; System.arraycopy(임시, 0, 결과, 0, 수); return 결과;
        } finally { ҷараён_қимат.close(); }
        } catch (java.io.IOException Хато) { throw 예외변환.вуруд_хуруҷ(Хато); }
        catch (RuntimeException Хато) { throw 예외변환.иҷро_кардан_фармон(Хато); }
    }
    public static void навиштан_байт_қимат(String Ном, byte[] Мӯҳтаво_қимат) throws 입출력예외 {
        try {
        FileOutputStream ҷараён_қимат = new FileOutputStream(Ном);
        try { for (int ҳалқа_индекс = 0; ҳалқа_индекс < Мӯҳтаво_қимат.length; ҳалқа_индекс++) ҷараён_қимат.write(Мӯҳтаво_қимат[ҳалқа_индекс] & 255); } finally { ҷараён_қимат.close(); }
        } catch (java.io.IOException Хато) { throw 예외변환.вуруд_хуруҷ(Хато); }
        catch (RuntimeException Хато) { throw 예외변환.иҷро_кардан_фармон(Хато); }
    }
    public static String Хондан(String Ном) throws 입출력예외 {
        try { return 문자.рамзкушоӣ_кардан_иттилоот(바이트읽기(Ном));
        } catch (java.io.IOException Хато) { throw 예외변환.вуруд_хуруҷ(Хато); }
        catch (RuntimeException Хато) { throw 예외변환.иҷро_кардан_фармон(Хато); }
    }
    public static void Навиштан(String Ном, String Мӯҳтаво_қимат) throws 입출력예외 {
        try { навиштан_байт_қимат(Ном, 문자.부호화(Мӯҳтаво_қимат));
        } catch (java.io.IOException Хато) { throw 예외변환.вуруд_хуруҷ(Хато); }
        catch (RuntimeException Хато) { throw 예외변환.иҷро_кардан_фармон(Хато); }
    }
}
