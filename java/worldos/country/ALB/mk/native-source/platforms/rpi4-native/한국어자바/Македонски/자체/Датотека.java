// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Македонски.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 корисник 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Датотека {
    private Датотека() {}
    public static byte[] 바이트읽기(String Име) throws В_И_исклучок {
        try {
        FileInputStream Stream_VALUE = new FileInputStream(Име);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, VALUE;
            while ((VALUE = Stream_VALUE.read()) != -1) { if (수 == 임시.length) throw new В_И_исклучок("Датотека Големина 제한"); 임시[수++] = (byte)VALUE; }
            byte[] мерка = new byte[수]; System.arraycopy(임시, 0, мерка, 0, 수); return мерка;
        } finally { Stream_VALUE.close(); }
        } catch (java.io.IOException ГРЕШКА) { throw CONVERT_исклучок.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw CONVERT_исклучок.Изврши_наредба(ГРЕШКА); }
    }
    public static void запиши_бајт_VALUE(String Име, byte[] Содржина_VALUE) throws В_И_исклучок {
        try {
        FileOutputStream Stream_VALUE = new FileOutputStream(Име);
        try { for (int Loop_INDEX = 0; Loop_INDEX < Содржина_VALUE.length; Loop_INDEX++) Stream_VALUE.write(Содржина_VALUE[Loop_INDEX] & 255); } finally { Stream_VALUE.close(); }
        } catch (java.io.IOException ГРЕШКА) { throw CONVERT_исклучок.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw CONVERT_исклучок.Изврши_наредба(ГРЕШКА); }
    }
    public static String Читај(String Име) throws В_И_исклучок {
        try { return 문자.дешифрирај_податоци(바이트읽기(Име));
        } catch (java.io.IOException ГРЕШКА) { throw CONVERT_исклучок.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw CONVERT_исклучок.Изврши_наредба(ГРЕШКА); }
    }
    public static void Запиши(String Име, String Содржина_VALUE) throws В_И_исклучок {
        try { запиши_бајт_VALUE(Име, 문자.부호화(Содржина_VALUE));
        } catch (java.io.IOException ГРЕШКА) { throw CONVERT_исклучок.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw CONVERT_исклучок.Изврши_наредба(ГРЕШКА); }
    }
}
