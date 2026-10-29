// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;

/** Convierte errores Java estándar en la frontera de la API en español, sin cambiar el significado de las cláusulas catch estándar. */
final class convertirExcepción {
    private convertirExcepción() {}
    public static ExcepciónSalidaEntrada salidaEntrada(java.io.IOException error) {
        if (error instanceof ExcepciónSalidaEntrada) return (ExcepciónSalidaEntrada)error;
        if (error instanceof java.net.SocketTimeoutException) return new ExcepciónTiempoEsperaEsperar("Se agotó el tiempo de espera de comunicación.");
        if (error instanceof java.net.UnknownHostException) return new ExcepciónBuscarDirección("No se puede resolver la dirección. Por ahora, use una dirección IPv4 numérica.");
        if (error instanceof java.io.FileNotFoundException) return new ExcepciónArchivoAusente("No se puede abrir el archivo.");
        if (error instanceof java.net.SocketException) return new ExcepciónComunicación("Falló la conexión: " + error.getMessage());
        return new ExcepciónSalidaEntrada("Falló la operación de entrada y salida: " + error.getMessage());
    }
    public static RuntimeException ejecutarComando(RuntimeException error) {
        if (error instanceof java.lang.NumberFormatException) return new FalloFormatoNúmero("Compruebe el formato y el intervalo del número.");
        if (error instanceof java.lang.IllegalArgumentException) return new ExcepciónArgumentoInválido("Compruebe el valor y el intervalo del argumento.");
        if (error instanceof java.lang.ArrayIndexOutOfBoundsException) return new ExcepciónLímitesArreglo("El índice está fuera de los límites del arreglo.");
        if (error instanceof java.lang.StringIndexOutOfBoundsException) return new ExcepciónLímitesCadena("El índice está fuera de los límites de la cadena.");
        if (error instanceof java.lang.IndexOutOfBoundsException) return new ExcepciónLímites("Se superó el intervalo permitido.");
        if (error instanceof java.lang.NullPointerException) return new ExcepciónReferenciaReferenciaNula("La referencia es nula.");
        return new ExcepciónEjecución(error.getMessage());
    }
}
