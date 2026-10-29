// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** 사전(辭典): 찾는 말(열쇠)에 값을 대응시킨다. */
public final class 사전 {
    private final HashMap<String, String> ننوت_ارزښت = new HashMap<String, String>();
    public String 넣기(String 열쇠, String ارزښت) { return ننوت_ارزښت.put(열쇠, ارزښت); }
    public String 찾기(String 열쇠) { return ننوت_ارزښت.get(열쇠); }
    public boolean 있는가(String 열쇠) { return ننوت_ارزښت.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return ننوت_ارزښت.remove(열쇠); }
    public int کچ() { return ننوت_ارزښت.size(); }
    public void پاک_منځپانګې() { ننوت_ارزښت.clear(); }
}
