// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gaeilge.자체;
import java.util.HashMap;
/** foclóir(辭典): 찾는 Word_SMS(열쇠)에 값을 대응시킨다. */
public final class foclóir {
    private final HashMap<String, String> iontráil_VALUE = new HashMap<String, String>();
    public String 넣기(String 열쇠, String VALUE) { return iontráil_VALUE.put(열쇠, VALUE); }
    public String FIND_iontráil(String 열쇠) { return iontráil_VALUE.get(열쇠); }
    public boolean 있는가(String 열쇠) { return iontráil_VALUE.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return iontráil_VALUE.remove(열쇠); }
    public int Méid() { return iontráil_VALUE.size(); }
    public void glan_TOC() { iontráil_VALUE.clear(); }
}
