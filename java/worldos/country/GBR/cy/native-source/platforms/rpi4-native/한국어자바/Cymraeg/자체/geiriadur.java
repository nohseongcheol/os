// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cymraeg.자체;
import java.util.HashMap;
/** geiriadur(辭典): 찾는 Word_SMS(열쇠)에 값을 대응시킨다. */
public final class geiriadur {
    private final HashMap<String, String> cofnod_VALUE = new HashMap<String, String>();
    public String 넣기(String 열쇠, String VALUE) { return cofnod_VALUE.put(열쇠, VALUE); }
    public String FIND_cofnod(String 열쇠) { return cofnod_VALUE.get(열쇠); }
    public boolean 있는가(String 열쇠) { return cofnod_VALUE.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return cofnod_VALUE.remove(열쇠); }
    public int Maint() { return cofnod_VALUE.size(); }
    public void clirio_Cynnwys() { cofnod_VALUE.clear(); }
}
