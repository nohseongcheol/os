// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svenska.eget;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 användarutrymme 용어를 보존한다. aktuellt_objekt 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class filnamn {
    private filnamn() {}
    public static byte[] läsa_byte_värde(String Namn) throws indata_utleverans_fel {
        try {
        FileInputStream flöde_värde = new FileInputStream(Namn);
        try {
            byte[] 임시 = new byte[16384]; int nummer = 0, värde;
            while ((värde = flöde_värde.read()) != -1) { if (nummer == 임시.length) throw new indata_utleverans_fel("filnamn Storlek 제한"); 임시[nummer++] = (byte)värde; }
            byte[] RESULTAT = new byte[nummer]; System.arraycopy(임시, 0, RESULTAT, 0, nummer); return RESULTAT;
        } finally { flöde_värde.close(); }
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public static void skriva_byte_värde(String Namn, byte[] Innehåll_värde) throws indata_utleverans_fel {
        try {
        FileOutputStream flöde_värde = new FileOutputStream(Namn);
        try { for (int Loop_INDEX = 0; Loop_INDEX < Innehåll_värde.length; Loop_INDEX++) flöde_värde.write(Innehåll_värde[Loop_INDEX] & 255); } finally { flöde_värde.close(); }
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public static String Läs(String Namn) throws indata_utleverans_fel {
        try { return 문자.avkryptera_data(läsa_byte_värde(Namn));
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
    public static void Skriv(String Namn, String Innehåll_värde) throws indata_utleverans_fel {
        try { skriva_byte_värde(Namn, 문자.koda(Innehåll_värde));
        } catch (java.io.IOException fel) { throw KONVERTERA_fel.indata_utleverans(fel); }
        catch (RuntimeException fel) { throw KONVERTERA_fel.köra_kommando(fel); }
    }
}
