// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Galego.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 usuario 용어를 보존한다. ao_corrente_elemento 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Ficheiro {
    private Ficheiro() {}
    public static byte[] 바이트읽기(String Nome) throws E_S_excepción {
        try {
        FileInputStream fluxo_VALOR = new FileInputStream(Nome);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, VALOR;
            while ((VALOR = fluxo_VALOR.read()) != -1) { if (수 == 임시.length) throw new E_S_excepción("Ficheiro Tamaño 제한"); 임시[수++] = (byte)VALOR; }
            byte[] RESULTANTE = new byte[수]; System.arraycopy(임시, 0, RESULTANTE, 0, 수); return RESULTANTE;
        } finally { fluxo_VALOR.close(); }
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public static void escribir_byte_VALOR(String Nome, byte[] Contido_VALOR) throws E_S_excepción {
        try {
        FileOutputStream fluxo_VALOR = new FileOutputStream(Nome);
        try { for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Contido_VALOR.length; Loop_ÍNDICE++) fluxo_VALOR.write(Contido_VALOR[Loop_ÍNDICE] & 255); } finally { fluxo_VALOR.close(); }
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public static String Lectura(String Nome) throws E_S_excepción {
        try { return 문자.descifrar_datos(바이트읽기(Nome));
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public static void Escritura(String Nome, String Contido_VALOR) throws E_S_excepción {
        try { escribir_byte_VALOR(Nome, 문자.부호화(Contido_VALOR));
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
}
