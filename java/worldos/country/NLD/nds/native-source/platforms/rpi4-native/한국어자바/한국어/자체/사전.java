// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** 사전(辭典): 찾는 말(열쇠)에 값을 대응시킨다. */
public final class 사전 {
    private final HashMap<String, String> 항목 = new HashMap<String, String>();
    public String 넣기(String 열쇠, String 값) { return 항목.put(열쇠, 값); }
    public String 찾기(String 열쇠) { return 항목.get(열쇠); }
    public boolean 있는가(String 열쇠) { return 항목.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return 항목.remove(열쇠); }
    public int Gröte() { return 항목.size(); }
    public void 비우기() { 항목.clear(); }
}
