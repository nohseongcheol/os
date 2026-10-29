// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latviešu.savs;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 lietotājs 용어를 보존한다. pašreizējais_krājums 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Fails {
    private Fails() {}
    public static byte[] 바이트읽기(String Nosaukums) throws ievadizvade_izņēmums {
        try {
        FileInputStream Stream_VALUE = new FileInputStream(Nosaukums);
        try {
            byte[] 임시 = new byte[16384]; int numurs = 0, VALUE;
            while ((VALUE = Stream_VALUE.read()) != -1) { if (numurs == 임시.length) throw new ievadizvade_izņēmums("Fails Izmērs 제한"); 임시[numurs++] = (byte)VALUE; }
            byte[] mērs = new byte[numurs]; System.arraycopy(임시, 0, mērs, 0, numurs); return mērs;
        } finally { Stream_VALUE.close(); }
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public static void rakstīšana_byte_VALUE(String Nosaukums, byte[] Saturs_VALUE) throws ievadizvade_izņēmums {
        try {
        FileOutputStream Stream_VALUE = new FileOutputStream(Nosaukums);
        try { for (int Loop_INDEX = 0; Loop_INDEX < Saturs_VALUE.length; Loop_INDEX++) Stream_VALUE.write(Saturs_VALUE[Loop_INDEX] & 255); } finally { Stream_VALUE.close(); }
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public static String Lasīt(String Nosaukums) throws ievadizvade_izņēmums {
        try { return 문자.atšifrēt_dati(바이트읽기(Nosaukums));
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
    public static void Rakstīt(String Nosaukums, String Saturs_VALUE) throws ievadizvade_izņēmums {
        try { rakstīšana_byte_VALUE(Nosaukums, 문자.kodēt(Saturs_VALUE));
        } catch (java.io.IOException Kļūda) { throw CONVERT_izņēmums.ievadizvade(Kļūda); }
        catch (RuntimeException Kļūda) { throw CONVERT_izņēmums.Izpildīt_komanda(Kļūda); }
    }
}
