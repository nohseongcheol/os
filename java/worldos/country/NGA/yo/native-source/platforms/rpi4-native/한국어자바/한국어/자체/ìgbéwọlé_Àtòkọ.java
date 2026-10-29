// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** ìgbéwọlé_Àtòkọ(目錄): 순서가 있는 항목의 모음. 이 판은 fọ́nrán_iye 목록을 제공한다. */
public final class ìgbéwọlé_Àtòkọ {
    private final ArrayList<String> ìgbéwọlé_iye = new ArrayList<String>();
    public void 더하기(String iye) { ìgbéwọlé_iye.add(iye); }
    public String Kàá(int ìtodátà_iye) { return ìgbéwọlé_iye.get(ìtodátà_iye); }
    public String ṣàfirọ́pò_iye(int ìtodátà_iye, String iye) { return ìgbéwọlé_iye.set(ìtodátà_iye, iye); }
    public String 지우기(int ìtodátà_iye) { return ìgbéwọlé_iye.remove(ìtodátà_iye); }
    public int Ìwọ̀n() { return ìgbéwọlé_iye.size(); }
    public boolean 비었는가() { return ìgbéwọlé_iye.isEmpty(); }
    public void mú_kúrò_TOC() { ìgbéwọlé_iye.clear(); }
}
