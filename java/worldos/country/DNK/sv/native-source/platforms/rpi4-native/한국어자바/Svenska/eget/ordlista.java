// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svenska.eget;
import java.util.HashMap;
/** ordlista(辭典): 찾는 Ord_SMS(열쇠)에 값을 대응시킨다. */
public final class ordlista {
    private final HashMap<String, String> post_värde = new HashMap<String, String>();
    public String 넣기(String 열쇠, String värde) { return post_värde.put(열쇠, värde); }
    public String Sök_post(String 열쇠) { return post_värde.get(열쇠); }
    public boolean 있는가(String 열쇠) { return post_värde.containsKey(열쇠); }
    public String radera_post(String 열쇠) { return post_värde.remove(열쇠); }
    public int Storlek() { return post_värde.size(); }
    public void rensa_Innehåll() { post_värde.clear(); }
}
