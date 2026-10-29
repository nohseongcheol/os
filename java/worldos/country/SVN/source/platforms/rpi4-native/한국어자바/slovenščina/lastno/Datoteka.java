// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package slovenščina.lastno;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 uporabnik 용어를 보존한다. sprotno_element 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Datoteka {
    private Datoteka() {}
    public static byte[] 바이트읽기(String Ime) throws V_I_izjema {
        try {
        FileInputStream tok_VALUE = new FileInputStream(Ime);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, VALUE;
            while ((VALUE = tok_VALUE.read()) != -1) { if (수 == 임시.length) throw new V_I_izjema("Datoteka Velikost 제한"); 임시[수++] = (byte)VALUE; }
            byte[] REZULTAT = new byte[수]; System.arraycopy(임시, 0, REZULTAT, 0, 수); return REZULTAT;
        } finally { tok_VALUE.close(); }
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public static void pisati_bajt_VALUE(String Ime, byte[] vsebina_VALUE) throws V_I_izjema {
        try {
        FileOutputStream tok_VALUE = new FileOutputStream(Ime);
        try { for (int Loop_INDEX = 0; Loop_INDEX < vsebina_VALUE.length; Loop_INDEX++) tok_VALUE.write(vsebina_VALUE[Loop_INDEX] & 255); } finally { tok_VALUE.close(); }
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public static String Branje(String Ime) throws V_I_izjema {
        try { return 문자.dešifrirati_podatki(바이트읽기(Ime));
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public static void Pisanje(String Ime, String vsebina_VALUE) throws V_I_izjema {
        try { pisati_bajt_VALUE(Ime, 문자.kodirati(vsebina_VALUE));
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
}
