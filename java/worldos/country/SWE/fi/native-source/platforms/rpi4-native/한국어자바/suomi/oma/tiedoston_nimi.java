// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package suomi.oma;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 käyttäjätila 용어를 보존한다. nykyinen_kohde 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class tiedoston_nimi {
    private tiedoston_nimi() {}
    public static byte[] lukea_tavu_ARVO(String Nimi) throws I_O_poikkeus {
        try {
        FileInputStream virta_ARVO = new FileInputStream(Nimi);
        try {
            byte[] 임시 = new byte[16384]; int numero = 0, ARVO;
            while ((ARVO = virta_ARVO.read()) != -1) { if (numero == 임시.length) throw new I_O_poikkeus("tiedoston_nimi Koko 제한"); 임시[numero++] = (byte)ARVO; }
            byte[] TULOS = new byte[numero]; System.arraycopy(임시, 0, TULOS, 0, numero); return TULOS;
        } finally { virta_ARVO.close(); }
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public static void kirjoitus_tavu_ARVO(String Nimi, byte[] Sisältö_ARVO) throws I_O_poikkeus {
        try {
        FileOutputStream virta_ARVO = new FileOutputStream(Nimi);
        try { for (int Loop_INDEKSI = 0; Loop_INDEKSI < Sisältö_ARVO.length; Loop_INDEKSI++) virta_ARVO.write(Sisältö_ARVO[Loop_INDEKSI] & 255); } finally { virta_ARVO.close(); }
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public static String Luku(String Nimi) throws I_O_poikkeus {
        try { return 문자.pura_salaus_data(lukea_tavu_ARVO(Nimi));
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
    public static void Kirjoitus(String Nimi, String Sisältö_ARVO) throws I_O_poikkeus {
        try { kirjoitus_tavu_ARVO(Nimi, 문자.koodata(Sisältö_ARVO));
        } catch (java.io.IOException VIRHE) { throw MUUNNA_poikkeus.I_O(VIRHE); }
        catch (RuntimeException VIRHE) { throw MUUNNA_poikkeus.Suorita_komento(VIRHE); }
    }
}
