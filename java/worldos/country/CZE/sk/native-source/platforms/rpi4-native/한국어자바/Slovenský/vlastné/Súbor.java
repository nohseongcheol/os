// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenský.vlastné;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 používateľ 용어를 보존한다. v_termíne_splatnosti_položka 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Súbor {
    private Súbor() {}
    public static byte[] 바이트읽기(String Názov) throws vstup_a_výstup_výnimka {
        try {
        FileInputStream Stream_VALUE = new FileInputStream(Názov);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, VALUE;
            while ((VALUE = Stream_VALUE.read()) != -1) { if (수 == 임시.length) throw new vstup_a_výstup_výnimka("Súbor Veľkosť 제한"); 임시[수++] = (byte)VALUE; }
            byte[] KR = new byte[수]; System.arraycopy(임시, 0, KR, 0, 수); return KR;
        } finally { Stream_VALUE.close(); }
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public static void zapísať_Byte_VALUE(String Názov, byte[] obsah_VALUE) throws vstup_a_výstup_výnimka {
        try {
        FileOutputStream Stream_VALUE = new FileOutputStream(Názov);
        try { for (int Loop_INDEX = 0; Loop_INDEX < obsah_VALUE.length; Loop_INDEX++) Stream_VALUE.write(obsah_VALUE[Loop_INDEX] & 255); } finally { Stream_VALUE.close(); }
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public static String Čítanie(String Názov) throws vstup_a_výstup_výnimka {
        try { return 문자.dešifrovať_údaje(바이트읽기(Názov));
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
    public static void Zápis(String Názov, String obsah_VALUE) throws vstup_a_výstup_výnimka {
        try { zapísať_Byte_VALUE(Názov, 문자.kódovať(obsah_VALUE));
        } catch (java.io.IOException chyba) { throw CONVERT_výnimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výnimka.Vykonať_príkaz(chyba); }
    }
}
