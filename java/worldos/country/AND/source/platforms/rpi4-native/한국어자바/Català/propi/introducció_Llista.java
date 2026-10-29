// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Català.propi;
import java.util.ArrayList;
/** introducció_Llista(目錄): 순서가 있는 항목의 모음. 이 판은 cadena_VALOR 목록을 제공한다. */
public final class introducció_Llista {
    private final ArrayList<String> introducció_VALOR = new ArrayList<String>();
    public void 더하기(String VALOR) { introducció_VALOR.add(VALOR); }
    public String Lectura(int comanda_VALOR) { return introducció_VALOR.get(comanda_VALOR); }
    public String REEMPLAÇA_VALOR(int comanda_VALOR, String VALOR) { return introducció_VALOR.set(comanda_VALOR, VALOR); }
    public String esborrar_introducció(int comanda_VALOR) { return introducció_VALOR.remove(comanda_VALOR); }
    public int Mida() { return introducció_VALOR.size(); }
    public boolean 비었는가() { return introducció_VALOR.isEmpty(); }
    public void eliminar_Índex() { introducció_VALOR.clear(); }
}
