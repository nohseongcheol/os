// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.savas;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 naudotojas 용어를 보존한다. dabartinis_prekė 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Failas {
    private Failas() {}
    public static byte[] 바이트읽기(String Pavadinimas_2) throws Į_I_išimtis {
        try {
        FileInputStream Stream_VALUE = new FileInputStream(Pavadinimas_2);
        try {
            byte[] 임시 = new byte[16384]; int numeris = 0, VALUE;
            while ((VALUE = Stream_VALUE.read()) != -1) { if (numeris == 임시.length) throw new Į_I_išimtis("Failas Dydis 제한"); 임시[numeris++] = (byte)VALUE; }
            byte[] REZULTATAS = new byte[numeris]; System.arraycopy(임시, 0, REZULTATAS, 0, numeris); return REZULTATAS;
        } finally { Stream_VALUE.close(); }
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public static void rašymas_baitas_VALUE(String Pavadinimas_2, byte[] Turinys_VALUE) throws Į_I_išimtis {
        try {
        FileOutputStream Stream_VALUE = new FileOutputStream(Pavadinimas_2);
        try { for (int Loop_INDEX = 0; Loop_INDEX < Turinys_VALUE.length; Loop_INDEX++) Stream_VALUE.write(Turinys_VALUE[Loop_INDEX] & 255); } finally { Stream_VALUE.close(); }
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public static String Skaitymas(String Pavadinimas_2) throws Į_I_išimtis {
        try { return 문자.iššifruoti_duomenys(바이트읽기(Pavadinimas_2));
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
    public static void Rašymas(String Pavadinimas_2, String Turinys_VALUE) throws Į_I_išimtis {
        try { rašymas_baitas_VALUE(Pavadinimas_2, 문자.koduoti(Turinys_VALUE));
        } catch (java.io.IOException KLAIDA) { throw CONVERT_išimtis.Į_I(KLAIDA); }
        catch (RuntimeException KLAIDA) { throw CONVERT_išimtis.Vykdyti_komanda(KLAIDA); }
    }
}
