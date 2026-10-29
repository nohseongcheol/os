// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** téereb_Tekki_baat(辭典): 찾는 Word_SMS(열쇠)에 값을 대응시킨다. */
public final class téereb_Tekki_baat {
    private final HashMap<String, String> dugal_xabaar_xëyma = new HashMap<String, String>();
    public String 넣기(String 열쇠, String xëyma) { return dugal_xabaar_xëyma.put(열쇠, xëyma); }
    public String seet_dugal_xabaar(String 열쇠) { return dugal_xabaar_xëyma.get(열쇠); }
    public boolean 있는가(String 열쇠) { return dugal_xabaar_xëyma.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return dugal_xabaar_xëyma.remove(열쇠); }
    public int tolluwaay() { return dugal_xabaar_xëyma.size(); }
    public void efaase_TOC() { dugal_xabaar_xëyma.clear(); }
}
