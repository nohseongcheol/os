// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Galego.자체;
import java.util.HashMap;
/** dicionario(辭典): 찾는 Word_SMS(열쇠)에 값을 대응시킨다. */
public final class dicionario {
    private final HashMap<String, String> introdución_VALOR = new HashMap<String, String>();
    public String 넣기(String 열쇠, String VALOR) { return introdución_VALOR.put(열쇠, VALOR); }
    public String Busca_introdución(String 열쇠) { return introdución_VALOR.get(열쇠); }
    public boolean 있는가(String 열쇠) { return introdución_VALOR.containsKey(열쇠); }
    public String borrar_introdución(String 열쇠) { return introdución_VALOR.remove(열쇠); }
    public int Tamaño() { return introdución_VALOR.size(); }
    public void desmarcar_Contido() { introdución_VALOR.clear(); }
}
