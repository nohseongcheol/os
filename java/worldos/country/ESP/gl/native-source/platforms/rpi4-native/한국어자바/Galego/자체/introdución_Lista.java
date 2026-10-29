// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Galego.자체;
import java.util.ArrayList;
/** introdución_Lista(目錄): 순서가 있는 항목의 모음. 이 판은 cadea_VALOR 목록을 제공한다. */
public final class introdución_Lista {
    private final ArrayList<String> introdución_VALOR = new ArrayList<String>();
    public void 더하기(String VALOR) { introdución_VALOR.add(VALOR); }
    public String Lectura(int orde_VALOR) { return introdución_VALOR.get(orde_VALOR); }
    public String SUBSTITUÍR_VALOR(int orde_VALOR, String VALOR) { return introdución_VALOR.set(orde_VALOR, VALOR); }
    public String borrar_introdución(int orde_VALOR) { return introdución_VALOR.remove(orde_VALOR); }
    public int Tamaño() { return introdución_VALOR.size(); }
    public boolean Tecnoloxía_da_información_TI_baleiro_VALOR() { return introdución_VALOR.isEmpty(); }
    public void desmarcar_Contido() { introdución_VALOR.clear(); }
}
