// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 korisnik 용어를 보존한다. aktuelno_stavka 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Datoteka {
    private Datoteka() {}
    public static byte[] 바이트읽기(String ime) throws U_I_izuzetak {
        try {
        FileInputStream tok_VALUE = new FileInputStream(ime);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, VALUE;
            while ((VALUE = tok_VALUE.read()) != -1) { if (수 == 임시.length) throw new U_I_izuzetak("Datoteka promeniti_veličinu 제한"); 임시[수++] = (byte)VALUE; }
            byte[] KR = new byte[수]; System.arraycopy(임시, 0, KR, 0, 수); return KR;
        } finally { tok_VALUE.close(); }
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public static void 바이트쓰기(String ime, byte[] Sadržaj_VALUE) throws U_I_izuzetak {
        try {
        FileOutputStream tok_VALUE = new FileOutputStream(ime);
        try { for (int Loop_INDEX = 0; Loop_INDEX < Sadržaj_VALUE.length; Loop_INDEX++) tok_VALUE.write(Sadržaj_VALUE[Loop_INDEX] & 255); } finally { tok_VALUE.close(); }
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public static String 읽기(String ime) throws U_I_izuzetak {
        try { return 문자.dešifrovati_podaci(바이트읽기(ime));
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public static void 쓰기(String ime, String Sadržaj_VALUE) throws U_I_izuzetak {
        try { 바이트쓰기(ime, 문자.kodirati(Sadržaj_VALUE));
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
}
