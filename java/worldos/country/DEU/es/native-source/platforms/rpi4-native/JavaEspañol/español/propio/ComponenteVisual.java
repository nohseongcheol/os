// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;
/** Métodos auxiliares para crear componentes de pantalla de la API en español. */
public final class ComponenteVisual {
    private ComponenteVisual() {}
    public static void invocarPosterior(TareaTareaEjecutable AcciónTarea) { ColaEvento.invocarPosterior(AcciónTarea); }
    public static etiqueta valorEtiquetaMarcador(String texto, int posiciónHorizontal, int posiciónVertical, int extensiónRangoAnchura, int valorAltura) {
        return new etiqueta(texto, posiciónHorizontal, posiciónVertical, extensiónRangoAnchura, valorAltura);
    }
    public static botón botón(String texto, int posiciónHorizontal, int posiciónVertical, int extensiónRangoAnchura, int valorAltura, ReceptorAcción valorReceptor) {
        return new botón(texto, posiciónHorizontal, posiciónVertical, extensiónRangoAnchura, valorAltura, valorReceptor);
    }
    public static CampoTexto CampoTexto(String texto, int posiciónHorizontal, int posiciónVertical, int extensiónRangoAnchura, int valorAltura) {
        return new CampoTexto(texto, posiciónHorizontal, posiciónVertical, extensiónRangoAnchura, valorAltura);
    }
}
