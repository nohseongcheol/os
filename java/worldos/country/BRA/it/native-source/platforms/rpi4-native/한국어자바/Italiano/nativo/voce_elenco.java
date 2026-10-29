// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italiano.nativo;
import java.util.ArrayList;
/** voce_elenco(目錄): 순서가 있는 항목의 모음. 이 판은 stringa_VALORE 목록을 제공한다. */
public final class voce_elenco {
    private final ArrayList<String> voce_VALORE = new ArrayList<String>();
    public void 더하기(String VALORE) { voce_VALORE.add(VALORE); }
    public String Lettura(int ordine_VALORE) { return voce_VALORE.get(ordine_VALORE); }
    public String RIMPIAZZA_VALORE(int ordine_VALORE, String VALORE) { return voce_VALORE.set(ordine_VALORE, VALORE); }
    public String cancellare_voce(int ordine_VALORE) { return voce_VALORE.remove(ordine_VALORE); }
    public int Dimensione() { return voce_VALORE.size(); }
    public boolean reparto_IT_vuota_VALORE() { return voce_VALORE.isEmpty(); }
    public void liquidare_Sommario() { voce_VALORE.clear(); }
}
