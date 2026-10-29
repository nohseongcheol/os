// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Íslenska.eigin;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 notandi 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Skrá {
    private Skrá() {}
    public static byte[] 바이트읽기(String Heiti) throws I_Ú_undantekning {
        try {
        FileInputStream Stream_VALUE = new FileInputStream(Heiti);
        try {
            byte[] 임시 = new byte[16384]; int númer = 0, VALUE;
            while ((VALUE = Stream_VALUE.read()) != -1) { if (númer == 임시.length) throw new I_Ú_undantekning("Skrá Stærð 제한"); 임시[númer++] = (byte)VALUE; }
            byte[] NIÐURSTAÐA = new byte[númer]; System.arraycopy(임시, 0, NIÐURSTAÐA, 0, númer); return NIÐURSTAÐA;
        } finally { Stream_VALUE.close(); }
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public static void skrifa_bæti_VALUE(String Heiti, byte[] Efni_VALUE) throws I_Ú_undantekning {
        try {
        FileOutputStream Stream_VALUE = new FileOutputStream(Heiti);
        try { for (int Loop_INDEX = 0; Loop_INDEX < Efni_VALUE.length; Loop_INDEX++) Stream_VALUE.write(Efni_VALUE[Loop_INDEX] & 255); } finally { Stream_VALUE.close(); }
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public static String Lestur(String Heiti) throws I_Ú_undantekning {
        try { return 문자.dulráða_gögn(바이트읽기(Heiti));
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public static void Skrift(String Heiti, String Efni_VALUE) throws I_Ú_undantekning {
        try { skrifa_bæti_VALUE(Heiti, 문자.부호화(Efni_VALUE));
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
}
