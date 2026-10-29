// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package hrvatski.vlastiti;
import java.util.HashMap;
/** rječnik(辭典): 찾는 Word_SMS(열쇠)에 값을 대응시킨다. */
public final class rječnik {
    private final HashMap<String, String> unos_VALUE = new HashMap<String, String>();
    public String 넣기(String 열쇠, String VALUE) { return unos_VALUE.put(열쇠, VALUE); }
    public String FIND_unos(String 열쇠) { return unos_VALUE.get(열쇠); }
    public boolean 있는가(String 열쇠) { return unos_VALUE.containsKey(열쇠); }
    public String izbrisati_unos(String 열쇠) { return unos_VALUE.remove(열쇠); }
    public int Veličina() { return unos_VALUE.size(); }
    public void očistiti_Sadržaj() { unos_VALUE.clear(); }
}
