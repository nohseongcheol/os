// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** ingizo_Orodha(目錄): 순서가 있는 항목의 모음. 이 판은 tungo_thamani 목록을 제공한다. */
public final class ingizo_Orodha {
    private final ArrayList<String> ingizo_thamani = new ArrayList<String>();
    public void 더하기(String thamani) { ingizo_thamani.add(thamani); }
    public String 읽기(int mpangilio_thamani) { return ingizo_thamani.get(mpangilio_thamani); }
    public String badilisha_thamani(int mpangilio_thamani, String thamani) { return ingizo_thamani.set(mpangilio_thamani, thamani); }
    public String futa_ingizo(int mpangilio_thamani) { return ingizo_thamani.remove(mpangilio_thamani); }
    public int panga_ukubwa() { return ingizo_thamani.size(); }
    public boolean teknolojia_ya_maelezo_tupu_thamani() { return ingizo_thamani.isEmpty(); }
    public void ondoa_YAL() { ingizo_thamani.clear(); }
}
