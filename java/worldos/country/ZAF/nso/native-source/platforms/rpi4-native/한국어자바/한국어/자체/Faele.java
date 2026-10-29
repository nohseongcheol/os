// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 mošomiši 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Faele {
    private Faele() {}
    public static byte[] 바이트읽기(String Leina) throws 입출력예외 {
        try {
        FileInputStream Stream_boleng = new FileInputStream(Leina);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, boleng;
            while ((boleng = Stream_boleng.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("Faele Bogolo 제한"); 임시[수++] = (byte)boleng; }
            byte[] 결과 = new byte[수]; System.arraycopy(임시, 0, 결과, 0, 수); return 결과;
        } finally { Stream_boleng.close(); }
        } catch (java.io.IOException Phošo) { throw 예외변환.I_O(Phošo); }
        catch (RuntimeException Phošo) { throw 예외변환.phethagatša_taelo(Phošo); }
    }
    public static void ngwala_paete_boleng(String Leina, byte[] Diteng_boleng) throws 입출력예외 {
        try {
        FileOutputStream Stream_boleng = new FileOutputStream(Leina);
        try { for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < Diteng_boleng.length; ditaelopoeletšwa_lokela++) Stream_boleng.write(Diteng_boleng[ditaelopoeletšwa_lokela] & 255); } finally { Stream_boleng.close(); }
        } catch (java.io.IOException Phošo) { throw 예외변환.I_O(Phošo); }
        catch (RuntimeException Phošo) { throw 예외변환.phethagatša_taelo(Phošo); }
    }
    public static String Bala(String Leina) throws 입출력예외 {
        try { return 문자.boetša_sekeng_data(바이트읽기(Leina));
        } catch (java.io.IOException Phošo) { throw 예외변환.I_O(Phošo); }
        catch (RuntimeException Phošo) { throw 예외변환.phethagatša_taelo(Phošo); }
    }
    public static void Ngwala(String Leina, String Diteng_boleng) throws 입출력예외 {
        try { ngwala_paete_boleng(Leina, 문자.부호화(Diteng_boleng));
        } catch (java.io.IOException Phošo) { throw 예외변환.I_O(Phošo); }
        catch (RuntimeException Phošo) { throw 예외변환.phethagatša_taelo(Phošo); }
    }
}
