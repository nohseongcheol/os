// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svenska.eget;
import java.util.ArrayList;
/** post_ange(目錄): 순서가 있는 항목의 모음. 이 판은 sträng_värde 목록을 제공한다. */
public final class post_ange {
    private final ArrayList<String> post_värde = new ArrayList<String>();
    public void 더하기(String värde) { post_värde.add(värde); }
    public String Läs(int order_värde) { return post_värde.get(order_värde); }
    public String ERSÄTT_värde(int order_värde, String värde) { return post_värde.set(order_värde, värde); }
    public String radera_post(int order_värde) { return post_värde.remove(order_värde); }
    public int Storlek() { return post_värde.size(); }
    public boolean 비었는가() { return post_värde.isEmpty(); }
    public void rensa_Innehåll() { post_värde.clear(); }
}
