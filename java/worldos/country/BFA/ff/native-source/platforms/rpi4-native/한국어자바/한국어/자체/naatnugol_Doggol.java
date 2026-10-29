// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** naatnugol_Doggol(目錄): 순서가 있는 항목의 모음. 이 판은 ɓoggol_njaru 목록을 제공한다. */
public final class naatnugol_Doggol {
    private final ArrayList<String> naatnugol_njaru = new ArrayList<String>();
    public void 더하기(String njaru) { naatnugol_njaru.add(njaru); }
    public String 읽기(int deggondiral_njaru) { return naatnugol_njaru.get(deggondiral_njaru); }
    public String lomtinde_njaru(int deggondiral_njaru, String njaru) { return naatnugol_njaru.set(deggondiral_njaru, njaru); }
    public String 지우기(int deggondiral_njaru) { return naatnugol_njaru.remove(deggondiral_njaru); }
    public int waylude_etannde() { return naatnugol_njaru.size(); }
    public boolean 비었는가() { return naatnugol_njaru.isEmpty(); }
    public void festude_Haatumeere_loowdi() { naatnugol_njaru.clear(); }
}
