// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Монгол.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 хэрэглэгч 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Файл {
    private Файл() {}
    public static byte[] 바이트읽기(String Нэр) throws 입출력예외 {
        try {
        FileInputStream урсгал_утга = new FileInputStream(Нэр);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, утга;
            while ((утга = урсгал_утга.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("Файл Хэмжээ 제한"); 임시[수++] = (byte)утга; }
            byte[] 결과 = new byte[수]; System.arraycopy(임시, 0, 결과, 0, 수); return 결과;
        } finally { урсгал_утга.close(); }
        } catch (java.io.IOException Алдаа) { throw 예외변환.оролт_гаралт(Алдаа); }
        catch (RuntimeException Алдаа) { throw 예외변환.Гүйцэтгэх_команд(Алдаа); }
    }
    public static void бичих_байт_утга(String Нэр, byte[] Агуулга_утга) throws 입출력예외 {
        try {
        FileOutputStream урсгал_утга = new FileOutputStream(Нэр);
        try { for (int давтах_индекс = 0; давтах_индекс < Агуулга_утга.length; давтах_индекс++) урсгал_утга.write(Агуулга_утга[давтах_индекс] & 255); } finally { урсгал_утга.close(); }
        } catch (java.io.IOException Алдаа) { throw 예외변환.оролт_гаралт(Алдаа); }
        catch (RuntimeException Алдаа) { throw 예외변환.Гүйцэтгэх_команд(Алдаа); }
    }
    public static String Унших(String Нэр) throws 입출력예외 {
        try { return 문자.шифрийг_задлах_өгөгдөл(바이트읽기(Нэр));
        } catch (java.io.IOException Алдаа) { throw 예외변환.оролт_гаралт(Алдаа); }
        catch (RuntimeException Алдаа) { throw 예외변환.Гүйцэтгэх_команд(Алдаа); }
    }
    public static void Бичих(String Нэр, String Агуулга_утга) throws 입출력예외 {
        try { бичих_байт_утга(Нэр, 문자.부호화(Агуулга_утга));
        } catch (java.io.IOException Алдаа) { throw 예외변환.оролт_гаралт(Алдаа); }
        catch (RuntimeException Алдаа) { throw 예외변환.Гүйцэтгэх_команд(Алдаа); }
    }
}
