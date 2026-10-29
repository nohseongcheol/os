// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;
import java.util.HashMap;
/** Asocia claves de búsqueda con valores. */
public final class Diccionario {
    private final HashMap<String, String> valorEntradaElemento = new HashMap<String, String>();
    public String ponerValor(String materialTecla, String valor) { return valorEntradaElemento.put(materialTecla, valor); }
    public String encontrarEntradaElemento(String materialTecla) { return valorEntradaElemento.get(materialTecla); }
    public boolean efectúaExistencia(String materialTecla) { return valorEntradaElemento.containsKey(materialTecla); }
    public String borrarEntradaElemento(String materialTecla) { return valorEntradaElemento.remove(materialTecla); }
    public int tamaño() { return valorEntradaElemento.size(); }
    public void borrarContenidoContenido() { valorEntradaElemento.clear(); }
}
