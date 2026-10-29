// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.nativo;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** comunicação(通信): IPv4 UDP datagrama. externo_VALOR 주소는 dígito_VALOR 주소를 사용한다. */
public final class comunicação {
    private comunicação() {}
    public static DatagramSocket Abrir(int porta_VALOR) throws E_S_exceção {
        try { return new DatagramSocket(porta_VALOR);
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public static void enviar(DatagramSocket empresa, int porta_VALOR, String Conteúdo_VALOR) throws E_S_exceção {
        try {
        enviar(empresa, "127.0.0.1", porta_VALOR, Conteúdo_VALOR);
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public static void enviar(DatagramSocket empresa, String Endereço, int porta_VALOR, String Conteúdo_VALOR) throws E_S_exceção {
        try {
        byte[] byte_VALOR = 문자.codificar(Conteúdo_VALOR);
        empresa.send(new DatagramPacket(byte_VALOR, byte_VALOR.length, InetAddress.getByName(Endereço), porta_VALOR));
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public static String receber(DatagramSocket empresa) throws E_S_exceção {
        try {
        byte[] byte_VALOR = new byte[512]; DatagramPacket datagrama = new DatagramPacket(byte_VALOR, byte_VALOR.length); empresa.receive(datagrama);
        byte[] resultado = new byte[datagrama.getLength()]; System.arraycopy(byte_VALOR, 0, resultado, 0, resultado.length); return 문자.descriptografar_dados(resultado);
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public static void TEMPOLIMITE(DatagramSocket empresa, int 밀리초) throws E_S_exceção {
        try { empresa.setSoTimeout(밀리초);
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public static void Fechar(DatagramSocket empresa) { empresa.close(); }
}
