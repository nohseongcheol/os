// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Română.propriu;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 utilizator 용어를 보존한다. curent_element 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Fișier {
    private Fișier() {}
    public static byte[] 바이트읽기(String Nume) throws I_O_excepție {
        try {
        FileInputStream flux_VALUE = new FileInputStream(Nume);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, VALUE;
            while ((VALUE = flux_VALUE.read()) != -1) { if (수 == 임시.length) throw new I_O_excepție("Fișier Mărime 제한"); 임시[수++] = (byte)VALUE; }
            byte[] KR = new byte[수]; System.arraycopy(임시, 0, KR, 0, 수); return KR;
        } finally { flux_VALUE.close(); }
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public static void scriere_byte_VALUE(String Nume, byte[] Conținut_VALUE) throws I_O_excepție {
        try {
        FileOutputStream flux_VALUE = new FileOutputStream(Nume);
        try { for (int Loop_INDEX = 0; Loop_INDEX < Conținut_VALUE.length; Loop_INDEX++) flux_VALUE.write(Conținut_VALUE[Loop_INDEX] & 255); } finally { flux_VALUE.close(); }
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public static String Citire(String Nume) throws I_O_excepție {
        try { return 문자.decripta_date(바이트읽기(Nume));
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
    public static void Scriere(String Nume, String Conținut_VALUE) throws I_O_excepție {
        try { scriere_byte_VALUE(Nume, 문자.codifica(Conținut_VALUE));
        } catch (java.io.IOException eroare) { throw CONVERT_excepție.I_O(eroare); }
        catch (RuntimeException eroare) { throw CONVERT_excepție.executa_comandă(eroare); }
    }
}
