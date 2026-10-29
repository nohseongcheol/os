// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Galego.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. externo_VALOR 주소는 díxito_VALOR 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Abrir(int porto_VALOR) throws E_S_excepción {
        try { return new DatagramSocket(porto_VALOR);
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public static void enviar(DatagramSocket extremo, int porto_VALOR, String Contido_VALOR) throws E_S_excepción {
        try {
        enviar(extremo, "127.0.0.1", porto_VALOR, Contido_VALOR);
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public static void enviar(DatagramSocket extremo, String ENDEREZO, int porto_VALOR, String Contido_VALOR) throws E_S_excepción {
        try {
        byte[] byte_VALOR = 문자.부호화(Contido_VALOR);
        extremo.send(new DatagramPacket(byte_VALOR, byte_VALOR.length, InetAddress.getByName(ENDEREZO), porto_VALOR));
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public static String 받기(DatagramSocket extremo) throws E_S_excepción {
        try {
        byte[] byte_VALOR = new byte[512]; DatagramPacket 전문 = new DatagramPacket(byte_VALOR, byte_VALOR.length); extremo.receive(전문);
        byte[] RESULTANTE = new byte[전문.getLength()]; System.arraycopy(byte_VALOR, 0, RESULTANTE, 0, RESULTANTE.length); return 문자.descifrar_datos(RESULTANTE);
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public static void TIMEOUT(DatagramSocket extremo, int 밀리초) throws E_S_excepción {
        try { extremo.setSoTimeout(밀리초);
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public static void Pechar(DatagramSocket extremo) { extremo.close(); }
}
