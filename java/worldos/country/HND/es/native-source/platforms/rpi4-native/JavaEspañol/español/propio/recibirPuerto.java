// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;

/** Acepta conexiones TCP entrantes. */
public final class recibirPuerto {
    private final java.net.ServerSocket puertoEstándar;
    private recibirPuerto(int númeroPuerto) throws ExcepciónSalidaEntrada {
        try { puertoEstándar = new java.net.ServerSocket(númeroPuerto);
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public static recibirPuerto abrir(int númeroPuerto) throws ExcepciónSalidaEntrada {
        try { return new recibirPuerto(númeroPuerto);
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public Conexión recibir() throws ExcepciónSalidaEntrada {
        try { return new Conexión(puertoEstándar.accept());
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public int númeroPuerto() { return puertoEstándar.getLocalPort(); }
    public void tiempoEspera(int milisegundos) throws ExcepciónSalidaEntrada {
        try { puertoEstándar.setSoTimeout(milisegundos);
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public boolean esCerrado() { return puertoEstándar.isClosed(); }
    public void cerrar() throws ExcepciónSalidaEntrada {
        try { puertoEstándar.close();
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
}
