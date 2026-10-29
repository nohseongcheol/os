// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.saját;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 felhasználó 용어를 보존한다. aktuális_cikk 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Fájl {
    private Fájl() {}
    public static byte[] 바이트읽기(String Név) throws I_O_kivétel {
        try {
        FileInputStream Stream_ÉRTÉK = new FileInputStream(Név);
        try {
            byte[] 임시 = new byte[16384]; int szám = 0, ÉRTÉK;
            while ((ÉRTÉK = Stream_ÉRTÉK.read()) != -1) { if (szám == 임시.length) throw new I_O_kivétel("Fájl Méret 제한"); 임시[szám++] = (byte)ÉRTÉK; }
            byte[] KR = new byte[szám]; System.arraycopy(임시, 0, KR, 0, szám); return KR;
        } finally { Stream_ÉRTÉK.close(); }
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public static void ír_bájt_ÉRTÉK(String Név, byte[] Tartalom_ÉRTÉK) throws I_O_kivétel {
        try {
        FileOutputStream Stream_ÉRTÉK = new FileOutputStream(Név);
        try { for (int Loop_INDEX = 0; Loop_INDEX < Tartalom_ÉRTÉK.length; Loop_INDEX++) Stream_ÉRTÉK.write(Tartalom_ÉRTÉK[Loop_INDEX] & 255); } finally { Stream_ÉRTÉK.close(); }
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public static String Olvasás(String Név) throws I_O_kivétel {
        try { return 문자.visszafejt_adat(바이트읽기(Név));
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
    public static void Írás(String Név, String Tartalom_ÉRTÉK) throws I_O_kivétel {
        try { ír_bájt_ÉRTÉK(Név, 문자.kódolás(Tartalom_ÉRTÉK));
        } catch (java.io.IOException HIBA) { throw konvertál_kivétel.I_O(HIBA); }
        catch (RuntimeException HIBA) { throw konvertál_kivétel.végrehajt_parancs(HIBA); }
    }
}
