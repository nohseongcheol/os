// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** увядзенне_Спіс(目錄): 순서가 있는 항목의 모음. 이 판은 радок_значэнне 목록을 제공한다. */
public final class увядзенне_Спіс {
    private final ArrayList<String> увядзенне_значэнне = new ArrayList<String>();
    public void 더하기(String значэнне) { увядзенне_значэнне.add(значэнне); }
    public String Чытанне(int парадак_значэнне) { return увядзенне_значэнне.get(парадак_значэнне); }
    public String замяніць_значэнне(int парадак_значэнне, String значэнне) { return увядзенне_значэнне.set(парадак_значэнне, значэнне); }
    public String ачысціць_увядзенне(int парадак_значэнне) { return увядзенне_значэнне.remove(парадак_значэнне); }
    public int Памер() { return увядзенне_значэнне.size(); }
    public boolean аддзел_інфармацыйных_тэхналогій_нулявая_значэнне() { return увядзенне_значэнне.isEmpty(); }
    public void ачысціць_Змест() { увядзенне_значэнне.clear(); }
}
