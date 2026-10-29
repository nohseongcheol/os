// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** речник(辭典): 찾는 Укрштенице_Текст(열쇠)에 값을 대응시킨다. */
public final class речник {
    private final HashMap<String, String> унос_вриједност = new HashMap<String, String>();
    public String 넣기(String 열쇠, String вриједност) { return унос_вриједност.put(열쇠, вриједност); }
    public String наћи_унос(String 열쇠) { return унос_вриједност.get(열쇠); }
    public boolean 있는가(String 열쇠) { return унос_вриједност.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return унос_вриједност.remove(열쇠); }
    public int Величина() { return унос_вриједност.size(); }
    public void обрисати_Садржај() { унос_вриједност.clear(); }
}
