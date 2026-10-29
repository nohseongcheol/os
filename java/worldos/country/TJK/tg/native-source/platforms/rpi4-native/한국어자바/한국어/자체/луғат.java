// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** луғат(辭典): 찾는 Калимабозӣ_Матн(열쇠)에 값을 대응시킨다. */
public final class луғат {
    private final HashMap<String, String> ворида_қимат = new HashMap<String, String>();
    public String 넣기(String 열쇠, String қимат) { return ворида_қимат.put(열쇠, қимат); }
    public String ёфтан_ворида(String 열쇠) { return ворида_қимат.get(열쇠); }
    public boolean 있는가(String 열쇠) { return ворида_қимат.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return ворида_қимат.remove(열쇠); }
    public int андоза_кардан() { return ворида_қимат.size(); }
    public void пок_кардан_Мундариҷа() { ворида_қимат.clear(); }
}
