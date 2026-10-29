// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** faclair(辭典): 찾는 Word_SMS(열쇠)에 값을 대응시킨다. */
public final class faclair {
    private final HashMap<String, String> cur_a_steach_VALUE = new HashMap<String, String>();
    public String 넣기(String 열쇠, String VALUE) { return cur_a_steach_VALUE.put(열쇠, VALUE); }
    public String FIND_cur_a_steach(String 열쇠) { return cur_a_steach_VALUE.get(열쇠); }
    public boolean 있는가(String 열쇠) { return cur_a_steach_VALUE.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return cur_a_steach_VALUE.remove(열쇠); }
    public int atharraich_am_meud() { return cur_a_steach_VALUE.size(); }
    public void glan_susbaint() { cur_a_steach_VALUE.clear(); }
}
