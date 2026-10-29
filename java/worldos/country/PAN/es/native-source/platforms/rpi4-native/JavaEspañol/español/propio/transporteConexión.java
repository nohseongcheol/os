// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;
import java.net.*;
public final class transporteConexión {
    private transporteConexión() {}
    public static Conexión abrir(String dirección, int númeroPuerto) throws ExcepciónSalidaEntrada {
        try { return Conexión.abrir(dirección, númeroPuerto);
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public static recibirPuerto abrirReceptor(int númeroPuerto) throws ExcepciónSalidaEntrada {
        try { return recibirPuerto.abrir(númeroPuerto);
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public static Socket conectar(String dirección, int valorPuerto) throws ExcepciónSalidaEntrada {
        try { return new Socket(dirección, valorPuerto);
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public static ServerSocket escucharExtremo(int valorPuerto) throws ExcepciónSalidaEntrada {
        try { return new ServerSocket(valorPuerto);
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public static Socket recibir(ServerSocket valorServidor) throws ExcepciónSalidaEntrada {
        try { return valorServidor.accept();
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
}
