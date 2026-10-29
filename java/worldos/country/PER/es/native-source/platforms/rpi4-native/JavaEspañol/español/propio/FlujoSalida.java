// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;

/** Canal para escribir bytes salientes en orden. */
public final class FlujoSalida {
    private final java.io.OutputStream flujoEstándar;
    FlujoSalida(java.io.OutputStream flujoEstándar) { this.flujoEstándar = flujoEstándar; }
    public void escribir(int valor) throws ExcepciónSalidaEntrada {
        try { flujoEstándar.write(valor);
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public void escribir(byte[] Datos) throws ExcepciónSalidaEntrada {
        try { flujoEstándar.write(Datos);
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public void escribir(byte[] Datos, int ponerEnMarcha, int longitud) throws ExcepciónSalidaEntrada {
        try { flujoEstándar.write(Datos, ponerEnMarcha, longitud);
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public void emitirValor() throws ExcepciónSalidaEntrada {
        try { flujoEstándar.flush();
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public void cerrar() throws ExcepciónSalidaEntrada {
        try { flujoEstándar.close();
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
}
