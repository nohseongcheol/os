// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** ការបញ្ចូល_បញ្ជី(目錄): 순서가 있는 항목의 모음. 이 판은 សំនុំអក្សរ_តំលៃ 목록을 제공한다. */
public final class ការបញ្ចូល_បញ្ជី {
    private final ArrayList<String> ការបញ្ចូល_តំលៃ = new ArrayList<String>();
    public void 더하기(String តំលៃ) { ការបញ្ចូល_តំលៃ.add(តំលៃ); }
    public String អាន(int លំដាប់_តំលៃ) { return ការបញ្ចូល_តំលៃ.get(លំដាប់_តំលៃ); }
    public String ជំនួស_តំលៃ(int លំដាប់_តំលៃ, String តំលៃ) { return ការបញ្ចូល_តំលៃ.set(លំដាប់_តំលៃ, តំលៃ); }
    public String លុប_ការបញ្ចូល(int លំដាប់_តំលៃ) { return ការបញ្ចូល_តំលៃ.remove(លំដាប់_តំលៃ); }
    public int ដាក់ទំហំ() { return ការបញ្ចូល_តំលៃ.size(); }
    public boolean បច្ចេកវិទ្យាព័ត៌មាន_ទទេរ_តំលៃ() { return ការបញ្ចូល_តំលៃ.isEmpty(); }
    public void លុប_មាតិការ() { ការបញ្ចូល_តំលៃ.clear(); }
}
