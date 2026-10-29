// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** 목록(目錄): 순서가 있는 항목의 모음. 이 판은 مزى_ارزښت_6ca8363c 목록을 제공한다. */
public final class 목록 {
    private final ArrayList<String> ننوت_ارزښت = new ArrayList<String>();
    public void 더하기(String ارزښت) { ننوت_ارزښت.add(ارزښت); }
    public String لوستل(int اڼن_اوډون_ارزښت) { return ننوت_ارزښت.get(اڼن_اوډون_ارزښت); }
    public String 바꾸기(int اڼن_اوډون_ارزښت, String ارزښت) { return ننوت_ارزښت.set(اڼن_اوډون_ارزښت, ارزښت); }
    public String 지우기(int اڼن_اوډون_ارزښت) { return ننوت_ارزښت.remove(اڼن_اوډون_ارزښت); }
    public int کچ() { return ننوت_ارزښت.size(); }
    public boolean 비었는가() { return ننوت_ارزښت.isEmpty(); }
    public void پاک_منځپانګې() { ننوت_ارزښت.clear(); }
}
