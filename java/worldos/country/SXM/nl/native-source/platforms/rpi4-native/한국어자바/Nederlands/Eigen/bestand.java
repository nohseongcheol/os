// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.Eigen;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 gebruikersruimte 용어를 보존한다. actueel_item 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class bestand {
    private bestand() {}
    public static byte[] 바이트읽기(String Naam) throws I_O_uitzondering {
        try {
        FileInputStream Stream_WAARDE = new FileInputStream(Naam);
        try {
            byte[] 임시 = new byte[16384]; int nummer = 0, WAARDE;
            while ((WAARDE = Stream_WAARDE.read()) != -1) { if (nummer == 임시.length) throw new I_O_uitzondering("bestand Grootte 제한"); 임시[nummer++] = (byte)WAARDE; }
            byte[] resultaat = new byte[nummer]; System.arraycopy(임시, 0, resultaat, 0, nummer); return resultaat;
        } finally { Stream_WAARDE.close(); }
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public static void schrijven_byte_WAARDE(String Naam, byte[] Inhoud_WAARDE) throws I_O_uitzondering {
        try {
        FileOutputStream Stream_WAARDE = new FileOutputStream(Naam);
        try { for (int lus_INDEX = 0; lus_INDEX < Inhoud_WAARDE.length; lus_INDEX++) Stream_WAARDE.write(Inhoud_WAARDE[lus_INDEX] & 255); } finally { Stream_WAARDE.close(); }
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public static String Lezen(String Naam) throws I_O_uitzondering {
        try { return 문자.ontsleutelen_gegevens(바이트읽기(Naam));
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
    public static void Schrijven(String Naam, String Inhoud_WAARDE) throws I_O_uitzondering {
        try { schrijven_byte_WAARDE(Naam, 문자.coderen(Inhoud_WAARDE));
        } catch (java.io.IOException fout) { throw CONVERTEREN_uitzondering.I_O(fout); }
        catch (RuntimeException fout) { throw CONVERTEREN_uitzondering.Uitvoeren_opdracht(fout); }
    }
}
