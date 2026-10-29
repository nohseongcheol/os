// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** kamusi(辭典): 찾는 Neno_SMS(열쇠)에 값을 대응시킨다. */
public final class kamusi {
    private final HashMap<String, String> ingizo_thamani = new HashMap<String, String>();
    public String 넣기(String 열쇠, String thamani) { return ingizo_thamani.put(열쇠, thamani); }
    public String gundua_ingizo(String 열쇠) { return ingizo_thamani.get(열쇠); }
    public boolean 있는가(String 열쇠) { return ingizo_thamani.containsKey(열쇠); }
    public String futa_ingizo(String 열쇠) { return ingizo_thamani.remove(열쇠); }
    public int panga_ukubwa() { return ingizo_thamani.size(); }
    public void ondoa_YAL() { ingizo_thamani.clear(); }
}
