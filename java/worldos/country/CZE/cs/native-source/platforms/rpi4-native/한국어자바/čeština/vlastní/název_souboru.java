// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package čeština.vlastní;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 uživatelský_prostor 용어를 보존한다. dobrá_zboží 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class název_souboru {
    private název_souboru() {}
    public static byte[] 바이트읽기(String Název) throws vstup_a_výstup_výjimka {
        try {
        FileInputStream tok_HODNOTA = new FileInputStream(Název);
        try {
            byte[] 임시 = new byte[16384]; int číslo = 0, HODNOTA;
            while ((HODNOTA = tok_HODNOTA.read()) != -1) { if (číslo == 임시.length) throw new vstup_a_výstup_výjimka("název_souboru Velikost 제한"); 임시[číslo++] = (byte)HODNOTA; }
            byte[] VÝSLEDEK = new byte[číslo]; System.arraycopy(임시, 0, VÝSLEDEK, 0, číslo); return VÝSLEDEK;
        } finally { tok_HODNOTA.close(); }
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public static void zápis_bajt_HODNOTA(String Název, byte[] Obsah_HODNOTA) throws vstup_a_výstup_výjimka {
        try {
        FileOutputStream tok_HODNOTA = new FileOutputStream(Název);
        try { for (int Loop_INDEX = 0; Loop_INDEX < Obsah_HODNOTA.length; Loop_INDEX++) tok_HODNOTA.write(Obsah_HODNOTA[Loop_INDEX] & 255); } finally { tok_HODNOTA.close(); }
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public static String Čtení(String Název) throws vstup_a_výstup_výjimka {
        try { return 문자.dešifrovat_data(바이트읽기(Název));
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
    public static void Zápis(String Název, String Obsah_HODNOTA) throws vstup_a_výstup_výjimka {
        try { zápis_bajt_HODNOTA(Název, 문자.kódovat(Obsah_HODNOTA));
        } catch (java.io.IOException chyba) { throw CONVERT_výjimka.vstup_a_výstup(chyba); }
        catch (RuntimeException chyba) { throw CONVERT_výjimka.Provést_příkaz(chyba); }
    }
}
