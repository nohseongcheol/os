// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latviešu.savs;
import java.util.HashMap;
/** vārdnīca(辭典): 찾는 Word_SMS(열쇠)에 값을 대응시킨다. */
public final class vārdnīca {
    private final HashMap<String, String> ievade_VALUE = new HashMap<String, String>();
    public String 넣기(String 열쇠, String VALUE) { return ievade_VALUE.put(열쇠, VALUE); }
    public String FIND_ievade(String 열쇠) { return ievade_VALUE.get(열쇠); }
    public boolean 있는가(String 열쇠) { return ievade_VALUE.containsKey(열쇠); }
    public String dzēst_ievade(String 열쇠) { return ievade_VALUE.remove(열쇠); }
    public int Izmērs() { return ievade_VALUE.size(); }
    public void nodzēst_Satura_rādītājs() { ievade_VALUE.clear(); }
}
