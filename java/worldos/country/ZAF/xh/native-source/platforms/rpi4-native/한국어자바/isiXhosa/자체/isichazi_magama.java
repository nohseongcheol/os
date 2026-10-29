// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package isiXhosa.자체;
import java.util.HashMap;
/** isichazi_magama(辭典): 찾는 Igama_I_SMS(열쇠)에 값을 대응시킨다. */
public final class isichazi_magama {
    private final HashMap<String, String> ufako_nkcukacha_ixabiso = new HashMap<String, String>();
    public String 넣기(String 열쇠, String ixabiso) { return ufako_nkcukacha_ixabiso.put(열쇠, ixabiso); }
    public String fumana_ufako_nkcukacha(String 열쇠) { return ufako_nkcukacha_ixabiso.get(열쇠); }
    public boolean 있는가(String 열쇠) { return ufako_nkcukacha_ixabiso.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return ufako_nkcukacha_ixabiso.remove(열쇠); }
    public int Ubukhulu() { return ufako_nkcukacha_ixabiso.size(); }
    public void susa_i_TOC() { ufako_nkcukacha_ixabiso.clear(); }
}
