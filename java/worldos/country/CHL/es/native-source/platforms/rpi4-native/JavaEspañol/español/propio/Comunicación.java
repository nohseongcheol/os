// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** Comunicación mediante datagramas IPv4 UDP. Los interlocutores externos usan direcciones numéricas. */
public final class Comunicación {
    private Comunicación() {}
    public static DatagramSocket abrir(int valorPuerto) throws ExcepciónSalidaEntrada {
        try { return new DatagramSocket(valorPuerto);
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public static void enviar(DatagramSocket extremo, int valorPuerto, String valorContenidoValor) throws ExcepciónSalidaEntrada {
        try {
        enviar(extremo, "127.0.0.1", valorPuerto, valorContenidoValor);
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public static void enviar(DatagramSocket extremo, String dirección, int valorPuerto, String valorContenidoValor) throws ExcepciónSalidaEntrada {
        try {
        byte[] valorByte = Caracteres.codificar(valorContenidoValor);
        extremo.send(new DatagramPacket(valorByte, valorByte.length, InetAddress.getByName(dirección), valorPuerto));
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public static String recibir(DatagramSocket extremo) throws ExcepciónSalidaEntrada {
        try {
        byte[] valorByte = new byte[512]; DatagramPacket datagrama = new DatagramPacket(valorByte, valorByte.length); extremo.receive(datagrama);
        byte[] resultado = new byte[datagrama.getLength()]; System.arraycopy(valorByte, 0, resultado, 0, resultado.length); return Caracteres.descifrarDatos(resultado);
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public static void tiempoEspera(DatagramSocket extremo, int milisegundos) throws ExcepciónSalidaEntrada {
        try { extremo.setSoTimeout(milisegundos);
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public static void cerrar(DatagramSocket extremo) { extremo.close(); }
}
