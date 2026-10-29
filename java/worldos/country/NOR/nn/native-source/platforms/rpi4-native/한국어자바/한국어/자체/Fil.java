// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 brukar 용어를 보존한다. betalt_vare 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Fil {
    private Fil() {}
    public static byte[] 바이트읽기(String Namn) throws I_U_unntak {
        try {
        FileInputStream Stream_VALUE = new FileInputStream(Namn);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, VALUE;
            while ((VALUE = Stream_VALUE.read()) != -1) { if (수 == 임시.length) throw new I_U_unntak("Fil Storleik 제한"); 임시[수++] = (byte)VALUE; }
            byte[] forretningsmål = new byte[수]; System.arraycopy(임시, 0, forretningsmål, 0, 수); return forretningsmål;
        } finally { Stream_VALUE.close(); }
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public static void skrive_byte_VALUE(String Namn, byte[] Innhald_VALUE) throws I_U_unntak {
        try {
        FileOutputStream Stream_VALUE = new FileOutputStream(Namn);
        try { for (int Loop_INDEX = 0; Loop_INDEX < Innhald_VALUE.length; Loop_INDEX++) Stream_VALUE.write(Innhald_VALUE[Loop_INDEX] & 255); } finally { Stream_VALUE.close(); }
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public static String Les(String Namn) throws I_U_unntak {
        try { return 문자.dekryptere_data(바이트읽기(Namn));
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
    public static void Skriv(String Namn, String Innhald_VALUE) throws I_U_unntak {
        try { skrive_byte_VALUE(Namn, 문자.부호화(Innhald_VALUE));
        } catch (java.io.IOException FEIL) { throw CONVERT_unntak.I_U(FEIL); }
        catch (RuntimeException FEIL) { throw CONVERT_unntak.Utfør_kommando(FEIL); }
    }
}
