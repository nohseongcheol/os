// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Català.propi;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 usuari 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Fitxer {
    private Fitxer() {}
    public static byte[] tancar_byte_VALOR(String Nom) throws E_S_excepció {
        try {
        FileInputStream flux_VALOR = new FileInputStream(Nom);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, VALOR;
            while ((VALOR = flux_VALOR.read()) != -1) { if (수 == 임시.length) throw new E_S_excepció("Fitxer Mida 제한"); 임시[수++] = (byte)VALOR; }
            byte[] RESULTAT = new byte[수]; System.arraycopy(임시, 0, RESULTAT, 0, 수); return RESULTAT;
        } finally { flux_VALOR.close(); }
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public static void escriure_byte_VALOR(String Nom, byte[] contingut_VALOR) throws E_S_excepció {
        try {
        FileOutputStream flux_VALOR = new FileOutputStream(Nom);
        try { for (int Loop_INDEX = 0; Loop_INDEX < contingut_VALOR.length; Loop_INDEX++) flux_VALOR.write(contingut_VALOR[Loop_INDEX] & 255); } finally { flux_VALOR.close(); }
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public static String Lectura(String Nom) throws E_S_excepció {
        try { return 문자.desencriptar_dades(tancar_byte_VALOR(Nom));
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public static void Escriptura(String Nom, String contingut_VALOR) throws E_S_excepció {
        try { escriure_byte_VALOR(Nom, 문자.부호화(contingut_VALOR));
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
}
