// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 колдонуучу 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Файл {
    private Файл() {}
    public static byte[] 바이트읽기(String Аты) throws 입출력예외 {
        try {
        FileInputStream агым_маани = new FileInputStream(Аты);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, маани;
            while ((маани = агым_маани.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("Файл Өлчөмү 제한"); 임시[수++] = (byte)маани; }
            byte[] 결과 = new byte[수]; System.arraycopy(임시, 0, 결과, 0, 수); return 결과;
        } finally { агым_маани.close(); }
        } catch (java.io.IOException Ката) { throw 예외변환.киргизүү_чыгаруу(Ката); }
        catch (RuntimeException Ката) { throw 예외변환.аткаруу_буйрук(Ката); }
    }
    public static void жазуу_байт_маани(String Аты, byte[] Мазмун_маани) throws 입출력예외 {
        try {
        FileOutputStream агым_маани = new FileOutputStream(Аты);
        try { for (int цикл_индекс = 0; цикл_индекс < Мазмун_маани.length; цикл_индекс++) агым_маани.write(Мазмун_маани[цикл_индекс] & 255); } finally { агым_маани.close(); }
        } catch (java.io.IOException Ката) { throw 예외변환.киргизүү_чыгаруу(Ката); }
        catch (RuntimeException Ката) { throw 예외변환.аткаруу_буйрук(Ката); }
    }
    public static String Окуу(String Аты) throws 입출력예외 {
        try { return 문자.чечмелөө_берилмелер(바이트읽기(Аты));
        } catch (java.io.IOException Ката) { throw 예외변환.киргизүү_чыгаруу(Ката); }
        catch (RuntimeException Ката) { throw 예외변환.аткаруу_буйрук(Ката); }
    }
    public static void Жазуу(String Аты, String Мазмун_маани) throws 입출력예외 {
        try { жазуу_байт_маани(Аты, 문자.부호화(Мазмун_маани));
        } catch (java.io.IOException Ката) { throw 예외변환.киргизүү_чыгаруу(Ката); }
        catch (RuntimeException Ката) { throw 예외변환.аткаруу_буйрук(Ката); }
    }
}
