// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Татарча.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 кулланучы 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Birem {
    private Birem() {}
    public static byte[] 바이트읽기(String исем) throws 입출력예외 {
        try {
        FileInputStream агым_VALUE = new FileInputStream(исем);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, VALUE;
            while ((VALUE = агым_VALUE.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("Birem үлчәмен_үзгәртү 제한"); 임시[수++] = (byte)VALUE; }
            byte[] үлчәм = new byte[수]; System.arraycopy(임시, 0, үлчәм, 0, 수); return үлчәм;
        } finally { агым_VALUE.close(); }
        } catch (java.io.IOException Хата) { throw 예외변환.К_Ч(Хата); }
        catch (RuntimeException Хата) { throw 예외변환.үтәргә_команда(Хата); }
    }
    public static void язу_байт_VALUE(String исем, byte[] Эчтәлек_VALUE) throws 입출력예외 {
        try {
        FileOutputStream агым_VALUE = new FileOutputStream(исем);
        try { for (int Loop_INDEX = 0; Loop_INDEX < Эчтәлек_VALUE.length; Loop_INDEX++) агым_VALUE.write(Эчтәлек_VALUE[Loop_INDEX] & 255); } finally { агым_VALUE.close(); }
        } catch (java.io.IOException Хата) { throw 예외변환.К_Ч(Хата); }
        catch (RuntimeException Хата) { throw 예외변환.үтәргә_команда(Хата); }
    }
    public static String 읽기(String исем) throws 입출력예외 {
        try { return 문자.шифрны_ачу_мәгълүмат(바이트읽기(исем));
        } catch (java.io.IOException Хата) { throw 예외변환.К_Ч(Хата); }
        catch (RuntimeException Хата) { throw 예외변환.үтәргә_команда(Хата); }
    }
    public static void язу(String исем, String Эчтәлек_VALUE) throws 입출력예외 {
        try { язу_байт_VALUE(исем, 문자.부호화(Эчтәлек_VALUE));
        } catch (java.io.IOException Хата) { throw 예외변환.К_Ч(Хата); }
        catch (RuntimeException Хата) { throw 예외변환.үтәргә_команда(Хата); }
    }
}
