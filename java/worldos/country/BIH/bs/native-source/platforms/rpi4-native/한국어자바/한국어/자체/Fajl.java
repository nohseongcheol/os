// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 korisnik 용어를 보존한다. trenutno_stavka 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Fajl {
    private Fajl() {}
    public static byte[] 바이트읽기(String Naziv) throws U_I_izuzetak {
        try {
        FileInputStream tok_VALUE = new FileInputStream(Naziv);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, VALUE;
            while ((VALUE = tok_VALUE.read()) != -1) { if (수 == 임시.length) throw new U_I_izuzetak("Fajl Veličina 제한"); 임시[수++] = (byte)VALUE; }
            byte[] mjera = new byte[수]; System.arraycopy(임시, 0, mjera, 0, 수); return mjera;
        } finally { tok_VALUE.close(); }
        } catch (java.io.IOException GRESKA) { throw CONVERT_izuzetak.U_I(GRESKA); }
        catch (RuntimeException GRESKA) { throw CONVERT_izuzetak.Izvrši_komanda(GRESKA); }
    }
    public static void pisati_bajt_VALUE(String Naziv, byte[] Sadržaj_VALUE) throws U_I_izuzetak {
        try {
        FileOutputStream tok_VALUE = new FileOutputStream(Naziv);
        try { for (int Loop_INDEX = 0; Loop_INDEX < Sadržaj_VALUE.length; Loop_INDEX++) tok_VALUE.write(Sadržaj_VALUE[Loop_INDEX] & 255); } finally { tok_VALUE.close(); }
        } catch (java.io.IOException GRESKA) { throw CONVERT_izuzetak.U_I(GRESKA); }
        catch (RuntimeException GRESKA) { throw CONVERT_izuzetak.Izvrši_komanda(GRESKA); }
    }
    public static String Čitaj(String Naziv) throws U_I_izuzetak {
        try { return 문자.dešifrirati_podaci(바이트읽기(Naziv));
        } catch (java.io.IOException GRESKA) { throw CONVERT_izuzetak.U_I(GRESKA); }
        catch (RuntimeException GRESKA) { throw CONVERT_izuzetak.Izvrši_komanda(GRESKA); }
    }
    public static void Piši(String Naziv, String Sadržaj_VALUE) throws U_I_izuzetak {
        try { pisati_bajt_VALUE(Naziv, 문자.부호화(Sadržaj_VALUE));
        } catch (java.io.IOException GRESKA) { throw CONVERT_izuzetak.U_I(GRESKA); }
        catch (RuntimeException GRESKA) { throw CONVERT_izuzetak.Izvrši_komanda(GRESKA); }
    }
}
