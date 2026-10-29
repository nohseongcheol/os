// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** слоўнік(辭典): 찾는 Гульні_са_словамі_Тэкст(열쇠)에 값을 대응시킨다. */
public final class слоўнік {
    private final HashMap<String, String> увядзенне_значэнне = new HashMap<String, String>();
    public String 넣기(String 열쇠, String значэнне) { return увядзенне_значэнне.put(열쇠, значэнне); }
    public String выявіць_увядзенне(String 열쇠) { return увядзенне_значэнне.get(열쇠); }
    public boolean 있는가(String 열쇠) { return увядзенне_значэнне.containsKey(열쇠); }
    public String ачысціць_увядзенне(String 열쇠) { return увядзенне_значэнне.remove(열쇠); }
    public int Памер() { return увядзенне_значэнне.size(); }
    public void ачысціць_Змест() { увядзенне_значэнне.clear(); }
}
