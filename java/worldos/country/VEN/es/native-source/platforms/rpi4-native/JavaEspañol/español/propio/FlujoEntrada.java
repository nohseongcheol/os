// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;

/** Canal para leer bytes entrantes en orden. */
public final class FlujoEntrada {
    private final java.io.InputStream flujoEstándar;
    FlujoEntrada(java.io.InputStream flujoEstándar) { this.flujoEstándar = flujoEstándar; }
    public int leer() throws ExcepciónSalidaEntrada {
        try { return flujoEstándar.read();
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public int leer(byte[] Datos) throws ExcepciónSalidaEntrada {
        try { return flujoEstándar.read(Datos);
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public int leer(byte[] Datos, int ponerEnMarcha, int longitud) throws ExcepciónSalidaEntrada {
        try { return flujoEstándar.read(Datos, ponerEnMarcha, longitud);
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public void cerrar() throws ExcepciónSalidaEntrada {
        try { flujoEstándar.close();
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
}
