// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package தமிழ்.자체;
import java.util.HashMap;
/** அகராதி(辭典): 찾는 சொல்_உரை(열쇠)에 값을 대응시킨다. */
public final class அகராதி {
    private final HashMap<String, String> உள்ளீடு_மதிப்பு = new HashMap<String, String>();
    public String 넣기(String 열쇠, String மதிப்பு) { return உள்ளீடு_மதிப்பு.put(열쇠, மதிப்பு); }
    public String கண்டறி_உள்ளீடு(String 열쇠) { return உள்ளீடு_மதிப்பு.get(열쇠); }
    public boolean 있는가(String 열쇠) { return உள்ளீடு_மதிப்பு.containsKey(열쇠); }
    public String அழி_உள்ளீடு(String 열쇠) { return உள்ளீடு_மதிப்பு.remove(열쇠); }
    public int அளவு() { return உள்ளீடு_மதிப்பு.size(); }
    public void அழி_உள்ளடக்கங்கள்() { உள்ளீடு_மதிப்பு.clear(); }
}
