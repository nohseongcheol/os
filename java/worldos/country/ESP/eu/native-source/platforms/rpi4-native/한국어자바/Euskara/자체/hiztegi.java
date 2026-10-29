// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Euskara.자체;
import java.util.HashMap;
/** hiztegi(辭典): 찾는 Word_SMS(열쇠)에 값을 대응시킨다. */
public final class hiztegi {
    private final HashMap<String, String> sarrera_balio = new HashMap<String, String>();
    public String 넣기(String 열쇠, String balio) { return sarrera_balio.put(열쇠, balio); }
    public String Bilatu_sarrera(String 열쇠) { return sarrera_balio.get(열쇠); }
    public boolean 있는가(String 열쇠) { return sarrera_balio.containsKey(열쇠); }
    public String ezabatu_sarrera(String 열쇠) { return sarrera_balio.remove(열쇠); }
    public int Tamaina() { return sarrera_balio.size(); }
    public void garbitu_Edukia() { sarrera_balio.clear(); }
}
