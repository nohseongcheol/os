// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** ශබ්දකෝෂය(辭典): 찾는 말(열쇠)에 값을 대응시킨다. */
public final class ශබ්දකෝෂය {
    private final HashMap<String, String> පිවිසුම_අගය = new HashMap<String, String>();
    public String 넣기(String 열쇠, String අගය) { return පිවිසුම_අගය.put(열쇠, අගය); }
    public String සොයන්න_පිවිසුම(String 열쇠) { return පිවිසුම_අගය.get(열쇠); }
    public boolean 있는가(String 열쇠) { return පිවිසුම_අගය.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return පිවිසුම_අගය.remove(열쇠); }
    public int ප්_රමාණය() { return පිවිසුම_අගය.size(); }
    public void හිස්_කරන්න_පටුන() { පිවිසුම_අගය.clear(); }
}
