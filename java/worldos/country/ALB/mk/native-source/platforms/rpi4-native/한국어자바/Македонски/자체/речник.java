// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Македонски.자체;
import java.util.HashMap;
/** речник(辭典): 찾는 Word_СМС(열쇠)에 값을 대응시킨다. */
public final class речник {
    private final HashMap<String, String> внес_VALUE = new HashMap<String, String>();
    public String 넣기(String 열쇠, String VALUE) { return внес_VALUE.put(열쇠, VALUE); }
    public String FIND_внес(String 열쇠) { return внес_VALUE.get(열쇠); }
    public boolean 있는가(String 열쇠) { return внес_VALUE.containsKey(열쇠); }
    public String избриши_внес(String 열쇠) { return внес_VALUE.remove(열쇠); }
    public int Големина() { return внес_VALUE.size(); }
    public void исчисти_Содржина() { внес_VALUE.clear(); }
}
