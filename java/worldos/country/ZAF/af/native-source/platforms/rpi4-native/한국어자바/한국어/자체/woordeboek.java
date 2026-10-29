// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** woordeboek(辭典): 찾는 Word_SMS(열쇠)에 값을 대응시킨다. */
public final class woordeboek {
    private final HashMap<String, String> inskrywing_VALUE = new HashMap<String, String>();
    public String 넣기(String 열쇠, String VALUE) { return inskrywing_VALUE.put(열쇠, VALUE); }
    public String FIND_inskrywing(String 열쇠) { return inskrywing_VALUE.get(열쇠); }
    public boolean 있는가(String 열쇠) { return inskrywing_VALUE.containsKey(열쇠); }
    public String vee_uit_inskrywing(String 열쇠) { return inskrywing_VALUE.remove(열쇠); }
    public int Grootte() { return inskrywing_VALUE.size(); }
    public void vee_uit_inhoud() { inskrywing_VALUE.clear(); }
}
