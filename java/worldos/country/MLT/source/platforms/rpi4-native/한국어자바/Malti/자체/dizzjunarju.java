// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malti.자체;
import java.util.HashMap;
/** dizzjunarju(辭典): 찾는 Word_SMS(열쇠)에 값을 대응시킨다. */
public final class dizzjunarju {
    private final HashMap<String, String> entrata_VALUE = new HashMap<String, String>();
    public String 넣기(String 열쇠, String VALUE) { return entrata_VALUE.put(열쇠, VALUE); }
    public String sab_entrata(String 열쇠) { return entrata_VALUE.get(열쇠); }
    public boolean 있는가(String 열쇠) { return entrata_VALUE.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return entrata_VALUE.remove(열쇠); }
    public int daqqas() { return entrata_VALUE.size(); }
    public void neħħa_TOC() { entrata_VALUE.clear(); }
}
