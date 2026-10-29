// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package norsk.eget;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 bruker 용어를 보존한다. betalt_vare 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Fil {
    private Fil() {}
    public static byte[] 바이트읽기(String Navn) throws I_U_unntak {
        try {
        FileInputStream strøm_VERDI = new FileInputStream(Navn);
        try {
            byte[] 임시 = new byte[16384]; int nummer = 0, VERDI;
            while ((VERDI = strøm_VERDI.read()) != -1) { if (nummer == 임시.length) throw new I_U_unntak("Fil Størrelse 제한"); 임시[nummer++] = (byte)VERDI; }
            byte[] KR = new byte[nummer]; System.arraycopy(임시, 0, KR, 0, nummer); return KR;
        } finally { strøm_VERDI.close(); }
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public static void skrive_byte_VERDI(String Navn, byte[] Innhold_VERDI) throws I_U_unntak {
        try {
        FileOutputStream strøm_VERDI = new FileOutputStream(Navn);
        try { for (int Loop_INDEKS = 0; Loop_INDEKS < Innhold_VERDI.length; Loop_INDEKS++) strøm_VERDI.write(Innhold_VERDI[Loop_INDEKS] & 255); } finally { strøm_VERDI.close(); }
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public static String Les(String Navn) throws I_U_unntak {
        try { return 문자.dekryptere_data(바이트읽기(Navn));
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
    public static void Skriv(String Navn, String Innhold_VERDI) throws I_U_unntak {
        try { skrive_byte_VERDI(Navn, 문자.부호화(Innhold_VERDI));
        } catch (java.io.IOException feil) { throw KONVERTER_unntak.I_U(feil); }
        catch (RuntimeException feil) { throw KONVERTER_unntak.Utfør_kommando(feil); }
    }
}
