// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** girizmeklik_Sanaw(目錄): 순서가 있는 항목의 모음. 이 판은 setir_baha_6ca8363c 목록을 제공한다. */
public final class girizmeklik_Sanaw {
    private final ArrayList<String> girizmeklik_baha = new ArrayList<String>();
    public void 더하기(String baha) { girizmeklik_baha.add(baha); }
    public String Oka(int tertip_baha) { return girizmeklik_baha.get(tertip_baha); }
    public String çalşyr_baha(int tertip_baha, String baha) { return girizmeklik_baha.set(tertip_baha, baha); }
    public String 지우기(int tertip_baha) { return girizmeklik_baha.remove(tertip_baha); }
    public int Ululyk() { return girizmeklik_baha.size(); }
    public boolean 비었는가() { return girizmeklik_baha.isEmpty(); }
    public void arassala_TOC() { girizmeklik_baha.clear(); }
}
