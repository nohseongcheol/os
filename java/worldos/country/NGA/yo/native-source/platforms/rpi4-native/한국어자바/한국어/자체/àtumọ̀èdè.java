// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** àtumọ̀èdè(辭典): 찾는 Ọ̀rọ̀_SMS(열쇠)에 값을 대응시킨다. */
public final class àtumọ̀èdè {
    private final HashMap<String, String> ìgbéwọlé_iye = new HashMap<String, String>();
    public String 넣기(String 열쇠, String iye) { return ìgbéwọlé_iye.put(열쇠, iye); }
    public String wá_ìgbéwọlé(String 열쇠) { return ìgbéwọlé_iye.get(열쇠); }
    public boolean 있는가(String 열쇠) { return ìgbéwọlé_iye.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return ìgbéwọlé_iye.remove(열쇠); }
    public int Ìwọ̀n() { return ìgbéwọlé_iye.size(); }
    public void mú_kúrò_TOC() { ìgbéwọlé_iye.clear(); }
}
