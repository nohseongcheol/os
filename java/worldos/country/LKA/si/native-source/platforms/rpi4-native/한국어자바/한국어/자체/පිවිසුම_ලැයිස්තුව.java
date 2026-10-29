// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** පිවිසුම_ලැයිස්තුව(目錄): 순서가 있는 항목의 모음. 이 판은 අනුලකුණු_වැල_අගය 목록을 제공한다. */
public final class පිවිසුම_ලැයිස්තුව {
    private final ArrayList<String> පිවිසුම_අගය = new ArrayList<String>();
    public void 더하기(String අගය) { පිවිසුම_අගය.add(අගය); }
    public String කියවීම(int අනුපිළිවෙළ_අගය) { return පිවිසුම_අගය.get(අනුපිළිවෙළ_අගය); }
    public String ප්_රතිස්ථාපනය_කරන්න_අගය(int අනුපිළිවෙළ_අගය, String අගය) { return පිවිසුම_අගය.set(අනුපිළිවෙළ_අගය, අගය); }
    public String 지우기(int අනුපිළිවෙළ_අගය) { return පිවිසුම_අගය.remove(අනුපිළිවෙළ_අගය); }
    public int ප්_රමාණය() { return පිවිසුම_අගය.size(); }
    public boolean 비었는가() { return පිවිසුම_අගය.isEmpty(); }
    public void හිස්_කරන්න_පටුන() { පිවිසුම_අගය.clear(); }
}
