// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** Conserva el concepto familiar de archivo. El almacenamiento actual consiste en archivos RAM que desaparecen al reiniciar. */
public final class Archivo {
    private Archivo() {}
    public static byte[] leerValorByte(String nombre) throws ExcepciónSalidaEntrada {
        try {
        FileInputStream valorFlujo = new FileInputStream(nombre);
        try {
            byte[] valorTemporal = new byte[16384]; int númeroValor = 0, valor;
            while ((valor = valorFlujo.read()) != -1) { if (númeroValor == valorTemporal.length) throw new ExcepciónSalidaEntrada("Límite del tamaño del archivo"); valorTemporal[númeroValor++] = (byte)valor; }
            byte[] resultado = new byte[númeroValor]; System.arraycopy(valorTemporal, 0, resultado, 0, númeroValor); return resultado;
        } finally { valorFlujo.close(); }
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public static void escribirValorByte(String nombre, byte[] valorContenidoValor) throws ExcepciónSalidaEntrada {
        try {
        FileOutputStream valorFlujo = new FileOutputStream(nombre);
        try { for (int índiceBucle = 0; índiceBucle < valorContenidoValor.length; índiceBucle++) valorFlujo.write(valorContenidoValor[índiceBucle] & 255); } finally { valorFlujo.close(); }
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public static String leer(String nombre) throws ExcepciónSalidaEntrada {
        try { return Caracteres.descifrarDatos(leerValorByte(nombre));
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
    public static void escribir(String nombre, String valorContenidoValor) throws ExcepciónSalidaEntrada {
        try { escribirValorByte(nombre, Caracteres.codificar(valorContenidoValor));
        } catch (java.io.IOException error) { throw convertirExcepción.salidaEntrada(error); }
        catch (RuntimeException error) { throw convertirExcepción.ejecutarComando(error); }
    }
}
