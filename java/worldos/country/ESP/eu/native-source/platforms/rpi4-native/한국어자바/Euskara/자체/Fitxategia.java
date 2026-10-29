// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Euskara.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 erabiltzaile 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Fitxategia {
    private Fitxategia() {}
    public static byte[] 바이트읽기(String Izena) throws S_I_salbuespen {
        try {
        FileInputStream Stream_balio = new FileInputStream(Izena);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, balio;
            while ((balio = Stream_balio.read()) != -1) { if (수 == 임시.length) throw new S_I_salbuespen("Fitxategia Tamaina 제한"); 임시[수++] = (byte)balio; }
            byte[] EMAITZA = new byte[수]; System.arraycopy(임시, 0, EMAITZA, 0, 수); return EMAITZA;
        } finally { Stream_balio.close(); }
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public static void idatzi_byte_balio(String Izena, byte[] eduki_balio) throws S_I_salbuespen {
        try {
        FileOutputStream Stream_balio = new FileOutputStream(Izena);
        try { for (int Loop_INDIZE = 0; Loop_INDIZE < eduki_balio.length; Loop_INDIZE++) Stream_balio.write(eduki_balio[Loop_INDIZE] & 255); } finally { Stream_balio.close(); }
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public static String Irakurri(String Izena) throws S_I_salbuespen {
        try { return 문자.desenkriptatu_datuak(바이트읽기(Izena));
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public static void Idatzi(String Izena, String eduki_balio) throws S_I_salbuespen {
        try { idatzi_byte_balio(Izena, 문자.부호화(eduki_balio));
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
}
