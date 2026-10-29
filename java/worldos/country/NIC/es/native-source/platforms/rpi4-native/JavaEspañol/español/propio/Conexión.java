// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;

/** Extremo de un flujo de bytes TCP conectado con el interlocutor. */
public final class Conexión {
    private final java.net.Socket puenteBibliotecaEstándar;
    Conexión(java.net.Socket puenteBibliotecaEstándar) { this.puenteBibliotecaEstándar = puenteBibliotecaEstándar; }
    public static Conexión abrir(String dirección, int númeroPuerto) throws ExcepciónSalidaEntrada {
        try {
            return new Conexión(new java.net.Socket(dirección, númeroPuerto));
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public FlujoEntrada valorEntrada() throws ExcepciónSalidaEntrada {
        try { return new FlujoEntrada(puenteBibliotecaEstándar.getInputStream());
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public FlujoSalida Salida() throws ExcepciónSalidaEntrada {
        try { return new FlujoSalida(puenteBibliotecaEstándar.getOutputStream());
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public void tiempoEspera(int milisegundos) throws ExcepciónSalidaEntrada {
        try { puenteBibliotecaEstándar.setSoTimeout(milisegundos);
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public int númeroPuerto() { return puenteBibliotecaEstándar.getPort(); }
    public int númeroPuertoLocal() { return puenteBibliotecaEstándar.getLocalPort(); }
    public boolean esCerrado() { return puenteBibliotecaEstándar.isClosed(); }
    public boolean conectado() { return puenteBibliotecaEstándar.isConnected(); }
    public void cerrar() throws ExcepciónSalidaEntrada {
        try { puenteBibliotecaEstándar.close();
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
}
