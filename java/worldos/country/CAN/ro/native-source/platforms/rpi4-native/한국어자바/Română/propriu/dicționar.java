// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Română.propriu;
import java.util.HashMap;
/** dicționar(辭典): 찾는 Word_SMS(열쇠)에 값을 대응시킨다. */
public final class dicționar {
    private final HashMap<String, String> intrare_VALUE = new HashMap<String, String>();
    public String 넣기(String 열쇠, String VALUE) { return intrare_VALUE.put(열쇠, VALUE); }
    public String FIND_intrare(String 열쇠) { return intrare_VALUE.get(열쇠); }
    public boolean 있는가(String 열쇠) { return intrare_VALUE.containsKey(열쇠); }
    public String șterge_intrare(String 열쇠) { return intrare_VALUE.remove(열쇠); }
    public int Mărime() { return intrare_VALUE.size(); }
    public void goli_TOC() { intrare_VALUE.clear(); }
}
