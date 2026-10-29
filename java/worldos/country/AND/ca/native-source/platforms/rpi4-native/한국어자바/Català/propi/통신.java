// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Català.propi;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. extern_VALOR 주소는 dígit_VALOR 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Obre(int port_VALOR) throws E_S_excepció {
        try { return new DatagramSocket(port_VALOR);
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public static void enviar(DatagramSocket extrem, int port_VALOR, String contingut_VALOR) throws E_S_excepció {
        try {
        enviar(extrem, "127.0.0.1", port_VALOR, contingut_VALOR);
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public static void enviar(DatagramSocket extrem, String Adreça, int port_VALOR, String contingut_VALOR) throws E_S_excepció {
        try {
        byte[] byte_VALOR = 문자.부호화(contingut_VALOR);
        extrem.send(new DatagramPacket(byte_VALOR, byte_VALOR.length, InetAddress.getByName(Adreça), port_VALOR));
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public static String rebre(DatagramSocket extrem) throws E_S_excepció {
        try {
        byte[] byte_VALOR = new byte[512]; DatagramPacket 전문 = new DatagramPacket(byte_VALOR, byte_VALOR.length); extrem.receive(전문);
        byte[] RESULTAT = new byte[전문.getLength()]; System.arraycopy(byte_VALOR, 0, RESULTAT, 0, RESULTAT.length); return 문자.desencriptar_dades(RESULTAT);
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public static void TIMEOUT(DatagramSocket extrem, int 밀리초) throws E_S_excepció {
        try { extrem.setSoTimeout(밀리초);
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public static void Tanca(DatagramSocket extrem) { extrem.close(); }
}
