// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Dansk.eget;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 bruger 용어를 보존한다. aktuel_vare 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Fil {
    private Fil() {}
    public static byte[] 바이트읽기(String Navn) throws I_O_undtagelse {
        try {
        FileInputStream strøm_VÆRDI = new FileInputStream(Navn);
        try {
            byte[] 임시 = new byte[16384]; int tal = 0, VÆRDI;
            while ((VÆRDI = strøm_VÆRDI.read()) != -1) { if (tal == 임시.length) throw new I_O_undtagelse("Fil Størrelse 제한"); 임시[tal++] = (byte)VÆRDI; }
            byte[] KR = new byte[tal]; System.arraycopy(임시, 0, KR, 0, tal); return KR;
        } finally { strøm_VÆRDI.close(); }
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public static void skrive_byte_VÆRDI(String Navn, byte[] Indhold_VÆRDI) throws I_O_undtagelse {
        try {
        FileOutputStream strøm_VÆRDI = new FileOutputStream(Navn);
        try { for (int Loop_INDEKS = 0; Loop_INDEKS < Indhold_VÆRDI.length; Loop_INDEKS++) strøm_VÆRDI.write(Indhold_VÆRDI[Loop_INDEKS] & 255); } finally { strøm_VÆRDI.close(); }
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public static String Læse(String Navn) throws I_O_undtagelse {
        try { return 문자.dekryptere_data(바이트읽기(Navn));
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
    public static void Skrive(String Navn, String Indhold_VÆRDI) throws I_O_undtagelse {
        try { skrive_byte_VÆRDI(Navn, 문자.kode(Indhold_VÆRDI));
        } catch (java.io.IOException fejl) { throw KONVERTER_undtagelse.I_O(fejl); }
        catch (RuntimeException fejl) { throw KONVERTER_undtagelse.Udfør_kommando(fejl); }
    }
}
