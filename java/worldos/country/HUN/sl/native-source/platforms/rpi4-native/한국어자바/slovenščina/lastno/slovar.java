// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package slovenščina.lastno;
import java.util.HashMap;
/** slovar(辭典): 찾는 Word_SMS(열쇠)에 값을 대응시킨다. */
public final class slovar {
    private final HashMap<String, String> vnos_VALUE = new HashMap<String, String>();
    public String 넣기(String 열쇠, String VALUE) { return vnos_VALUE.put(열쇠, VALUE); }
    public String FIND_vnos(String 열쇠) { return vnos_VALUE.get(열쇠); }
    public boolean 있는가(String 열쇠) { return vnos_VALUE.containsKey(열쇠); }
    public String izbrisati_vnos(String 열쇠) { return vnos_VALUE.remove(열쇠); }
    public int Velikost() { return vnos_VALUE.size(); }
    public void počistiti_Vsebina() { vnos_VALUE.clear(); }
}
