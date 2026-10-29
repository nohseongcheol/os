// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** fjalor(辭典): 찾는 Word_SMS(열쇠)에 값을 대응시킨다. */
public final class fjalor {
    private final HashMap<String, String> futje_VALUE = new HashMap<String, String>();
    public String 넣기(String 열쇠, String VALUE) { return futje_VALUE.put(열쇠, VALUE); }
    public String FIND_futje(String 열쇠) { return futje_VALUE.get(열쇠); }
    public boolean 있는가(String 열쇠) { return futje_VALUE.containsKey(열쇠); }
    public String spastroj_futje(String 열쇠) { return futje_VALUE.remove(열쇠); }
    public int Madhësi() { return futje_VALUE.size(); }
    public void pastroj_TOC() { futje_VALUE.clear(); }
}
