// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti.oma;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 kasutaja 용어를 보존한다. tähtaja_piires_kaup 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Fail {
    private Fail() {}
    public static byte[] 바이트읽기(String Nimi_2) throws I_O_erand {
        try {
        FileInputStream voog_VALUE = new FileInputStream(Nimi_2);
        try {
            byte[] 임시 = new byte[16384]; int number = 0, VALUE;
            while ((VALUE = voog_VALUE.read()) != -1) { if (number == 임시.length) throw new I_O_erand("Fail Suurus 제한"); 임시[number++] = (byte)VALUE; }
            byte[] TULEMUS = new byte[number]; System.arraycopy(임시, 0, TULEMUS, 0, number); return TULEMUS;
        } finally { voog_VALUE.close(); }
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public static void kirjutamine_bait_VALUE(String Nimi_2, byte[] Sisu_VALUE) throws I_O_erand {
        try {
        FileOutputStream voog_VALUE = new FileOutputStream(Nimi_2);
        try { for (int Loop_INDEX = 0; Loop_INDEX < Sisu_VALUE.length; Loop_INDEX++) voog_VALUE.write(Sisu_VALUE[Loop_INDEX] & 255); } finally { voog_VALUE.close(); }
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public static String Lugemine(String Nimi_2) throws I_O_erand {
        try { return 문자.dekrüptima_andmed(바이트읽기(Nimi_2));
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public static void Kirjutamine(String Nimi_2, String Sisu_VALUE) throws I_O_erand {
        try { kirjutamine_bait_VALUE(Nimi_2, 문자.kodeerima(Sisu_VALUE));
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
}
