// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.nativo;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 espaço_do_utilizador 용어를 보존한다. em_dia_item 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class ficheiro {
    private ficheiro() {}
    public static byte[] leitura_byte_VALOR(String Nome) throws E_S_exceção {
        try {
        FileInputStream fluxo_VALOR = new FileInputStream(Nome);
        try {
            byte[] 임시 = new byte[16384]; int número = 0, VALOR;
            while ((VALOR = fluxo_VALOR.read()) != -1) { if (número == 임시.length) throw new E_S_exceção("ficheiro Tamanho 제한"); 임시[número++] = (byte)VALOR; }
            byte[] resultado = new byte[número]; System.arraycopy(임시, 0, resultado, 0, número); return resultado;
        } finally { fluxo_VALOR.close(); }
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public static void gravar_byte_VALOR(String Nome, byte[] Conteúdo_VALOR) throws E_S_exceção {
        try {
        FileOutputStream fluxo_VALOR = new FileOutputStream(Nome);
        try { for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Conteúdo_VALOR.length; Loop_ÍNDICE++) fluxo_VALOR.write(Conteúdo_VALOR[Loop_ÍNDICE] & 255); } finally { fluxo_VALOR.close(); }
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public static String Leitura(String Nome) throws E_S_exceção {
        try { return 문자.descriptografar_dados(leitura_byte_VALOR(Nome));
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public static void Escrita(String Nome, String Conteúdo_VALOR) throws E_S_exceção {
        try { gravar_byte_VALOR(Nome, 문자.codificar(Conteúdo_VALOR));
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
}
