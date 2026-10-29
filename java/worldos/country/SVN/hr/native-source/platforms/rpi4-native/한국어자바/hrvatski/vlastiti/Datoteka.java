// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package hrvatski.vlastiti;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 korisnik 용어를 보존한다. redovno_artikl 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Datoteka {
    private Datoteka() {}
    public static byte[] 바이트읽기(String Ime) throws U_I_iznimka {
        try {
        FileInputStream tok_VALUE = new FileInputStream(Ime);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, VALUE;
            while ((VALUE = tok_VALUE.read()) != -1) { if (수 == 임시.length) throw new U_I_iznimka("Datoteka Veličina 제한"); 임시[수++] = (byte)VALUE; }
            byte[] REZULTAT = new byte[수]; System.arraycopy(임시, 0, REZULTAT, 0, 수); return REZULTAT;
        } finally { tok_VALUE.close(); }
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public static void zapisivanje_bajt_VALUE(String Ime, byte[] Sadržaj_VALUE) throws U_I_iznimka {
        try {
        FileOutputStream tok_VALUE = new FileOutputStream(Ime);
        try { for (int Loop_INDEX = 0; Loop_INDEX < Sadržaj_VALUE.length; Loop_INDEX++) tok_VALUE.write(Sadržaj_VALUE[Loop_INDEX] & 255); } finally { tok_VALUE.close(); }
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public static String Čitaj(String Ime) throws U_I_iznimka {
        try { return 문자.dešifrirati_podaci(바이트읽기(Ime));
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
    public static void Zapisuj(String Ime, String Sadržaj_VALUE) throws U_I_iznimka {
        try { zapisivanje_bajt_VALUE(Ime, 문자.kodirati(Sadržaj_VALUE));
        } catch (java.io.IOException GREŠKA) { throw CONVERT_iznimka.U_I(GREŠKA); }
        catch (RuntimeException GREŠKA) { throw CONVERT_iznimka.Izvrši_naredba(GREŠKA); }
    }
}
