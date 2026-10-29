// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;
import java.util.ArrayList;
/** Colección ordenada de elementos. Esta edición ofrece listas de cadenas. */
public final class listaEntradaElemento {
    private final ArrayList<String> valorEntradaElemento = new ArrayList<String>();
    public void añadirValores(String valor) { valorEntradaElemento.add(valor); }
    public String leer(int valorOrden) { return valorEntradaElemento.get(valorOrden); }
    public String reemplazarValor(int valorOrden, String valor) { return valorEntradaElemento.set(valorOrden, valor); }
    public String borrarEntradaElemento(int valorOrden) { return valorEntradaElemento.remove(valorOrden); }
    public int tamaño() { return valorEntradaElemento.size(); }
    public boolean esValorVacíoEstado() { return valorEntradaElemento.isEmpty(); }
    public void borrarContenidoContenido() { valorEntradaElemento.clear(); }
}
