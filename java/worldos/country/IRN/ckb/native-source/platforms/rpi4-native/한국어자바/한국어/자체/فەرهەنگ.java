// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** فەرهەنگ(辭典): 찾는 وشە_دەق(열쇠)에 값을 대응시킨다. */
public final class فەرهەنگ {
    private final HashMap<String, String> تێنووسین_نرخ = new HashMap<String, String>();
    public String 넣기(String 열쇠, String نرخ) { return تێنووسین_نرخ.put(열쇠, نرخ); }
    public String دۆزینەوە_تێنووسین(String 열쇠) { return تێنووسین_نرخ.get(열쇠); }
    public boolean 있는가(String 열쇠) { return تێنووسین_نرخ.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return تێنووسین_نرخ.remove(열쇠); }
    public int گۆڕینی_ئەندازە() { return تێنووسین_نرخ.size(); }
    public void سڕینەوە_TOC() { تێنووسین_نرخ.clear(); }
}
