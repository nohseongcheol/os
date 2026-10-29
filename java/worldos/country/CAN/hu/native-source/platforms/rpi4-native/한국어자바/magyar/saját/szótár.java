// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.saját;
import java.util.HashMap;
/** szótár(辭典): 찾는 szó_SMS(열쇠)에 값을 대응시킨다. */
public final class szótár {
    private final HashMap<String, String> bejegyzés_ÉRTÉK = new HashMap<String, String>();
    public String 넣기(String 열쇠, String ÉRTÉK) { return bejegyzés_ÉRTÉK.put(열쇠, ÉRTÉK); }
    public String keres_bejegyzés(String 열쇠) { return bejegyzés_ÉRTÉK.get(열쇠); }
    public boolean 있는가(String 열쇠) { return bejegyzés_ÉRTÉK.containsKey(열쇠); }
    public String töröl_bejegyzés(String 열쇠) { return bejegyzés_ÉRTÉK.remove(열쇠); }
    public int Méret() { return bejegyzés_ÉRTÉK.size(); }
    public void töröl_Tartalom() { bejegyzés_ÉRTÉK.clear(); }
}
