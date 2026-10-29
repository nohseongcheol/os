// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 Benotzer 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Fichier {
    private Fichier() {}
    public static byte[] 바이트읽기(String Numm) throws 입출력예외 {
        try {
        FileInputStream Stream_VALUE = new FileInputStream(Numm);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, VALUE;
            while ((VALUE = Stream_VALUE.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("Fichier d_Gréisst_veränneren 제한"); 임시[수++] = (byte)VALUE; }
            byte[] Mooss = new byte[수]; System.arraycopy(임시, 0, Mooss, 0, 수); return Mooss;
        } finally { Stream_VALUE.close(); }
        } catch (java.io.IOException Feeler) { throw 예외변환.I_O(Feeler); }
        catch (RuntimeException Feeler) { throw 예외변환.ausféieren_Befeel(Feeler); }
    }
    public static void schreiwen_Byte_VALUE(String Numm, byte[] Inhalt_VALUE) throws 입출력예외 {
        try {
        FileOutputStream Stream_VALUE = new FileOutputStream(Numm);
        try { for (int Loop_INDEX = 0; Loop_INDEX < Inhalt_VALUE.length; Loop_INDEX++) Stream_VALUE.write(Inhalt_VALUE[Loop_INDEX] & 255); } finally { Stream_VALUE.close(); }
        } catch (java.io.IOException Feeler) { throw 예외변환.I_O(Feeler); }
        catch (RuntimeException Feeler) { throw 예외변환.ausféieren_Befeel(Feeler); }
    }
    public static String 읽기(String Numm) throws 입출력예외 {
        try { return 문자.decryptéieren_Daten(바이트읽기(Numm));
        } catch (java.io.IOException Feeler) { throw 예외변환.I_O(Feeler); }
        catch (RuntimeException Feeler) { throw 예외변환.ausféieren_Befeel(Feeler); }
    }
    public static void schreiwen(String Numm, String Inhalt_VALUE) throws 입출력예외 {
        try { schreiwen_Byte_VALUE(Numm, 문자.부호화(Inhalt_VALUE));
        } catch (java.io.IOException Feeler) { throw 예외변환.I_O(Feeler); }
        catch (RuntimeException Feeler) { throw 예외변환.ausféieren_Befeel(Feeler); }
    }
}
