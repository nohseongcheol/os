// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italiano.nativo;
import java.util.HashMap;
/** dizionario(辭典): 찾는 Word_SMS(tasto_materiale)에 값을 대응시킨다. */
public final class dizionario {
    private final HashMap<String, String> voce_VALORE = new HashMap<String, String>();
    public String 넣기(String tasto_materiale, String VALORE) { return voce_VALORE.put(tasto_materiale, VALORE); }
    public String TROVA_voce(String tasto_materiale) { return voce_VALORE.get(tasto_materiale); }
    public boolean 있는가(String tasto_materiale) { return voce_VALORE.containsKey(tasto_materiale); }
    public String cancellare_voce(String tasto_materiale) { return voce_VALORE.remove(tasto_materiale); }
    public int Dimensione() { return voce_VALORE.size(); }
    public void liquidare_Sommario() { voce_VALORE.clear(); }
}
