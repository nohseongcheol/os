// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Dansk.eget;
import java.util.ArrayList;
/** post_Liste(目錄): 순서가 있는 항목의 모음. 이 판은 streng_VÆRDI 목록을 제공한다. */
public final class post_Liste {
    private final ArrayList<String> post_VÆRDI_962f286b = new ArrayList<String>();
    public void 더하기(String VÆRDI) { post_VÆRDI_962f286b.add(VÆRDI); }
    public String Læse(int ordre_VÆRDI) { return post_VÆRDI_962f286b.get(ordre_VÆRDI); }
    public String ERSTAT_VÆRDI(int ordre_VÆRDI, String VÆRDI) { return post_VÆRDI_962f286b.set(ordre_VÆRDI, VÆRDI); }
    public String slette_post(int ordre_VÆRDI) { return post_VÆRDI_962f286b.remove(ordre_VÆRDI); }
    public int Størrelse() { return post_VÆRDI_962f286b.size(); }
    public boolean 비었는가() { return post_VÆRDI_962f286b.isEmpty(); }
    public void rydde_Indhold() { post_VÆRDI_962f286b.clear(); }
}
