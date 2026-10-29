// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Dansk.eget;
import java.util.HashMap;
/** ordbog(辭典): 찾는 Ord_sms(열쇠)에 값을 대응시킨다. */
public final class ordbog {
    private final HashMap<String, String> post_VÆRDI_962f286b = new HashMap<String, String>();
    public String 넣기(String 열쇠, String VÆRDI) { return post_VÆRDI_962f286b.put(열쇠, VÆRDI); }
    public String Søg_post(String 열쇠) { return post_VÆRDI_962f286b.get(열쇠); }
    public boolean 있는가(String 열쇠) { return post_VÆRDI_962f286b.containsKey(열쇠); }
    public String slette_post(String 열쇠) { return post_VÆRDI_962f286b.remove(열쇠); }
    public int Størrelse() { return post_VÆRDI_962f286b.size(); }
    public void rydde_Indhold() { post_VÆRDI_962f286b.clear(); }
}
