// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package አማርኛ.자체;
import java.util.ArrayList;
/** ምዝግብ_ዝርዝር(目錄): 순서가 있는 항목의 모음. 이 판은 ኅብረቁምፊ_እሴት 목록을 제공한다. */
public final class ምዝግብ_ዝርዝር {
    private final ArrayList<String> ምዝግብ_እሴት = new ArrayList<String>();
    public void 더하기(String እሴት) { ምዝግብ_እሴት.add(እሴት); }
    public String ማንበቢያ(int ቅደም_ተከተል_እሴት) { return ምዝግብ_እሴት.get(ቅደም_ተከተል_እሴት); }
    public String ተካ_እሴት(int ቅደም_ተከተል_እሴት, String እሴት) { return ምዝግብ_እሴት.set(ቅደም_ተከተል_እሴት, እሴት); }
    public String አስወግድ_ምዝግብ_c8dbc399(int ቅደም_ተከተል_እሴት) { return ምዝግብ_እሴት.remove(ቅደም_ተከተል_እሴት); }
    public int መጠን() { return ምዝግብ_እሴት.size(); }
    public boolean የመረጃ_ቴክኖሎጂ_ባዶ_እሴት() { return ምዝግብ_እሴት.isEmpty(); }
    public void አጽዳ_ይዞታዎች() { ምዝግብ_እሴት.clear(); }
}
