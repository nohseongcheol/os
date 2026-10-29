// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package አማርኛ.자체;
import java.util.HashMap;
/** መዝገበ_ቃላት(辭典): 찾는 ቃል_ጽሁፍ(열쇠)에 값을 대응시킨다. */
public final class መዝገበ_ቃላት {
    private final HashMap<String, String> ምዝግብ_እሴት = new HashMap<String, String>();
    public String 넣기(String 열쇠, String እሴት) { return ምዝግብ_እሴት.put(열쇠, እሴት); }
    public String አግኝ_ምዝግብ(String 열쇠) { return ምዝግብ_እሴት.get(열쇠); }
    public boolean 있는가(String 열쇠) { return ምዝግብ_እሴት.containsKey(열쇠); }
    public String አስወግድ_ምዝግብ_c8dbc399(String 열쇠) { return ምዝግብ_እሴት.remove(열쇠); }
    public int መጠን() { return ምዝግብ_እሴት.size(); }
    public void አጽዳ_ይዞታዎች() { ምዝግብ_እሴት.clear(); }
}
