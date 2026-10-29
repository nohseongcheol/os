// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Català.propi;
import java.util.HashMap;
/** diccionari(辭典): 찾는 Word_SMS(열쇠)에 값을 대응시킨다. */
public final class diccionari {
    private final HashMap<String, String> introducció_VALOR = new HashMap<String, String>();
    public String 넣기(String 열쇠, String VALOR) { return introducció_VALOR.put(열쇠, VALOR); }
    public String BUSCA_introducció(String 열쇠) { return introducció_VALOR.get(열쇠); }
    public boolean 있는가(String 열쇠) { return introducció_VALOR.containsKey(열쇠); }
    public String esborrar_introducció(String 열쇠) { return introducció_VALOR.remove(열쇠); }
    public int Mida() { return introducció_VALOR.size(); }
    public void eliminar_Índex() { introducció_VALOR.clear(); }
}
