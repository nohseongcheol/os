// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package தமிழ்.자체;
import java.util.ArrayList;
/** உள்ளீடு_பட்டியல்(目錄): 순서가 있는 항목의 모음. 이 판은 சரம்_மதிப்பு 목록을 제공한다. */
public final class உள்ளீடு_பட்டியல் {
    private final ArrayList<String> உள்ளீடு_மதிப்பு = new ArrayList<String>();
    public void 더하기(String மதிப்பு) { உள்ளீடு_மதிப்பு.add(மதிப்பு); }
    public String படி(int வரிசை_மதிப்பு) { return உள்ளீடு_மதிப்பு.get(வரிசை_மதிப்பு); }
    public String மாற்று_மதிப்பு(int வரிசை_மதிப்பு, String மதிப்பு) { return உள்ளீடு_மதிப்பு.set(வரிசை_மதிப்பு, மதிப்பு); }
    public String அழி_உள்ளீடு(int வரிசை_மதிப்பு) { return உள்ளீடு_மதிப்பு.remove(வரிசை_மதிப்பு); }
    public int அளவு() { return உள்ளீடு_மதிப்பு.size(); }
    public boolean தகவல்_தொழில்நுட்பம்_வெறுமை_மதிப்பு() { return உள்ளீடு_மதிப்பு.isEmpty(); }
    public void அழி_உள்ளடக்கங்கள்() { உள்ளீடு_மதிப்பு.clear(); }
}
