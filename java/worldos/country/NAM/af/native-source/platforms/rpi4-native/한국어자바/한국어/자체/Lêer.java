// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 gebruiker 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Lêer {
    private Lêer() {}
    public static byte[] 바이트읽기(String Naam) throws I_O_uitsondering {
        try {
        FileInputStream Stream_VALUE = new FileInputStream(Naam);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, VALUE;
            while ((VALUE = Stream_VALUE.read()) != -1) { if (수 == 임시.length) throw new I_O_uitsondering("Lêer Grootte 제한"); 임시[수++] = (byte)VALUE; }
            byte[] maatreël = new byte[수]; System.arraycopy(임시, 0, maatreël, 0, 수); return maatreël;
        } finally { Stream_VALUE.close(); }
        } catch (java.io.IOException Fout) { throw CONVERT_uitsondering.I_O(Fout); }
        catch (RuntimeException Fout) { throw CONVERT_uitsondering.uitvoer_bevel(Fout); }
    }
    public static void skryf_greep_VALUE(String Naam, byte[] Inhoud_VALUE) throws I_O_uitsondering {
        try {
        FileOutputStream Stream_VALUE = new FileOutputStream(Naam);
        try { for (int lus_INDEX = 0; lus_INDEX < Inhoud_VALUE.length; lus_INDEX++) Stream_VALUE.write(Inhoud_VALUE[lus_INDEX] & 255); } finally { Stream_VALUE.close(); }
        } catch (java.io.IOException Fout) { throw CONVERT_uitsondering.I_O(Fout); }
        catch (RuntimeException Fout) { throw CONVERT_uitsondering.uitvoer_bevel(Fout); }
    }
    public static String Lees(String Naam) throws I_O_uitsondering {
        try { return 문자.dekripteer_data(바이트읽기(Naam));
        } catch (java.io.IOException Fout) { throw CONVERT_uitsondering.I_O(Fout); }
        catch (RuntimeException Fout) { throw CONVERT_uitsondering.uitvoer_bevel(Fout); }
    }
    public static void Skryf(String Naam, String Inhoud_VALUE) throws I_O_uitsondering {
        try { skryf_greep_VALUE(Naam, 문자.부호화(Inhoud_VALUE));
        } catch (java.io.IOException Fout) { throw CONVERT_uitsondering.I_O(Fout); }
        catch (RuntimeException Fout) { throw CONVERT_uitsondering.uitvoer_bevel(Fout); }
    }
}
