// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import español.propio.*;

public class pruebaExcepcionesCoreano {
    static void tiempoEsperaPredeterminado() throws java.io.IOException {
        throw new java.net.SocketTimeoutException("원래 excepción");
    }
    public static void main(String[] argumentos) throws ExcepciónSalidaEntrada {
        try { throw new ExcepciónTiempoEsperaEsperar("esperarEstadoValor terminación"); }
        catch (ExcepciónTiempoEsperaEsperar error) { Salida.escribirLínea(error.descripción()); }
        try { throw new ExcepciónBuscarDirección("dirección valorFallo"); }
        catch (ExcepciónSalidaEntrada error) { Salida.escribirLínea(error.descripción()); }
        try { throw new ExcepciónArchivoAusente("Archivo valorFallo"); }
        catch (java.io.IOException error) { Salida.escribirLínea("표준 상위 excepción 호환"); }
        try { tiempoEsperaPredeterminado(); }
        catch (ExcepciónTiempoEsperaEsperar incorrectamenteCapturadoEra) { Salida.escribirLínea("잘못된 nombreAlternativo"); }
        catch (java.io.IOException errorOriginal) { Salida.escribirLínea("español 예외의 독립된 categoríaTipo"); }
        try { Archivo.leer("없는한글파일"); }
        catch (ExcepciónArchivoAusente error) { Salida.escribirLínea("Archivo error español convertirValor"); }
        try { Caracteres.analizarEnteroValor("숫자가아님"); }
        catch (FalloFormatoNúmero error) { Salida.escribirLínea("valorDígito error español convertirValor"); }
        try { Comprobaciones.exigir(false, "Comprobaciones valorFallo"); }
        catch (ExcepciónArgumentoInválido error) { Salida.escribirLínea(error.descripción()); }
        try { throw new ExcepciónLímitesArreglo("recortar valorFallo"); }
        catch (ExcepciónLímites error) { Salida.escribirLínea(error.descripción()); }
        try { throw new ExcepciónReferenciaReferenciaNula("빈 referencia"); }
        catch (java.lang.RuntimeException error) { Salida.escribirLínea("ejecutarComando excepción 호환"); }
        try { throw new excepción("직접 정의한 descripción"); }
        catch (excepción error) { Salida.escribirLínea(error.descripción()); }
        try { throw new ExcepciónEstadoValorHiloEjecución("ExcepciónEstadoValorHiloEjecución"); }
        catch (ExcepciónEstadoValorHiloEjecución error) { Salida.escribirLínea(error.descripción()); }
        try { throw new ExcepciónTiempoEsperaEsperar("ExcepciónTiempoEsperaEsperar"); }
        catch (ExcepciónTiempoEsperaEsperar error) { Salida.escribirLínea(error.descripción()); }
        try { throw new ExcepciónInterrumpidoEsperar("ExcepciónInterrumpidoEsperar"); }
        catch (ExcepciónInterrumpidoEsperar error) { Salida.escribirLínea(error.descripción()); }
        try { throw new ExcepciónLímitesCadena("ExcepciónLímitesCadena"); }
        catch (ExcepciónLímitesCadena error) { Salida.escribirLínea(error.descripción()); }
        try { throw new ExcepciónLímitesArreglo("ExcepciónLímitesArreglo"); }
        catch (ExcepciónLímitesArreglo error) { Salida.escribirLínea(error.descripción()); }
        try { throw new FalloAlmacenarArreglo("FalloAlmacenarArreglo"); }
        catch (FalloAlmacenarArreglo error) { Salida.escribirLínea(error.descripción()); }
        try { throw new ExcepciónLímites("ExcepciónLímites"); }
        catch (ExcepciónLímites error) { Salida.escribirLínea(error.descripción()); }
        try { throw new ExcepciónReferenciaReferenciaNula("ExcepciónReferenciaReferenciaNula"); }
        catch (ExcepciónReferenciaReferenciaNula error) { Salida.escribirLínea(error.descripción()); }
        try { throw new FalloAritmética("FalloAritmética"); }
        catch (FalloAritmética error) { Salida.escribirLínea(error.descripción()); }
        try { throw new ExcepciónEstadoValor("ExcepciónEstadoValor"); }
        catch (ExcepciónEstadoValor error) { Salida.escribirLínea(error.descripción()); }
        try { throw new FalloFormatoNúmero("FalloFormatoNúmero"); }
        catch (FalloFormatoNúmero error) { Salida.escribirLínea(error.descripción()); }
        try { throw new ExcepciónEjecución("ExcepciónEjecución"); }
        catch (ExcepciónEjecución error) { Salida.escribirLínea(error.descripción()); }
        try { throw new excepción("excepción"); }
        catch (excepción error) { Salida.escribirLínea(error.descripción()); }
        try { throw new FalloTamañoArregloNegativo("FalloTamañoArregloNegativo"); }
        catch (FalloTamañoArregloNegativo error) { Salida.escribirLínea(error.descripción()); }
        try { throw new ExcepciónSalidaEntrada("ExcepciónSalidaEntrada"); }
        catch (ExcepciónSalidaEntrada error) { Salida.escribirLínea(error.descripción()); }
        try { throw new ExcepciónArgumentoInválido("ExcepciónArgumentoInválido"); }
        catch (ExcepciónArgumentoInválido error) { Salida.escribirLínea(error.descripción()); }
        try { throw new ExcepciónBuscarDirección("ExcepciónBuscarDirección"); }
        catch (ExcepciónBuscarDirección error) { Salida.escribirLínea(error.descripción()); }
        try { throw new ExcepciónComunicación("ExcepciónComunicación"); }
        catch (ExcepciónComunicación error) { Salida.escribirLínea(error.descripción()); }
        try { throw new ExcepciónArchivoAusente("ExcepciónArchivoAusente"); }
        catch (ExcepciónArchivoAusente error) { Salida.escribirLínea(error.descripción()); }
        try { throw new ExcepciónConversiónTipoTipo("ExcepciónConversiónTipoTipo"); }
        catch (ExcepciónConversiónTipoTipo error) { Salida.escribirLínea(error.descripción()); }
        Salida.escribirLínea("español excepción entradaElementoValorProceso esTerminado");
    }
}
