// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;

/** Extremo para enviar y recibir datagramas UDP conservando los límites de los mensajes. */
public final class CanalDatagrama {
    private final java.net.DatagramSocket extremoEstándar;
    private CanalDatagrama(int númeroPuerto) throws ExcepciónSalidaEntrada {
        try { extremoEstándar = Comunicación.abrir(númeroPuerto);
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public static CanalDatagrama abrir(int númeroPuerto) throws ExcepciónSalidaEntrada {
        try { return new CanalDatagrama(númeroPuerto);
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public void enviar(String dirección, int númeroPuerto, String Datos) throws ExcepciónSalidaEntrada {
        try { Comunicación.enviar(extremoEstándar, dirección, númeroPuerto, Datos);
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public String recibir() throws ExcepciónSalidaEntrada {
        try { return Comunicación.recibir(extremoEstándar);
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public void tiempoEspera(int milisegundos) throws ExcepciónSalidaEntrada {
        try { Comunicación.tiempoEspera(extremoEstándar, milisegundos);
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public int númeroPuerto() { return extremoEstándar.getLocalPort(); }
    public boolean esCerrado() { return extremoEstándar.isClosed(); }
    public void cerrar() { Comunicación.cerrar(extremoEstándar); }
}
