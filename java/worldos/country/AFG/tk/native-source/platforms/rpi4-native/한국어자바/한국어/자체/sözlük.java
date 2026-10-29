// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** sözlük(辭典): 찾는 Söz_SMS(열쇠)에 값을 대응시킨다. */
public final class sözlük {
    private final HashMap<String, String> girizmeklik_baha = new HashMap<String, String>();
    public String 넣기(String 열쇠, String baha) { return girizmeklik_baha.put(열쇠, baha); }
    public String tap_girizmeklik(String 열쇠) { return girizmeklik_baha.get(열쇠); }
    public boolean 있는가(String 열쇠) { return girizmeklik_baha.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return girizmeklik_baha.remove(열쇠); }
    public int Ululyk() { return girizmeklik_baha.size(); }
    public void arassala_TOC() { girizmeklik_baha.clear(); }
}
