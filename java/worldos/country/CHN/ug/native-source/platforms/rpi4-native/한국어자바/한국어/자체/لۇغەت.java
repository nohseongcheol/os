// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** لۇغەت(辭典): 찾는 سۆز_تېكست(열쇠)에 값을 대응시킨다. */
public final class لۇغەت {
    private final HashMap<String, String> كىرگۈزۈش_قىممىتى = new HashMap<String, String>();
    public String 넣기(String 열쇠, String قىممىتى) { return كىرگۈزۈش_قىممىتى.put(열쇠, قىممىتى); }
    public String ئىزدەش_كىرگۈزۈش(String 열쇠) { return كىرگۈزۈش_قىممىتى.get(열쇠); }
    public boolean 있는가(String 열쇠) { return كىرگۈزۈش_قىممىتى.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return كىرگۈزۈش_قىممىتى.remove(열쇠); }
    public int چوڭلۇقى() { return كىرگۈزۈش_قىممىتى.size(); }
    public void تازىلىماق_مۇندەرىجە() { كىرگۈزۈش_قىممىتى.clear(); }
}
