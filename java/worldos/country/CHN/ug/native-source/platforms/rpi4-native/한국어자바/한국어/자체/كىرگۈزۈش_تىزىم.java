// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** كىرگۈزۈش_تىزىم(目錄): 순서가 있는 항목의 모음. 이 판은 ھەرپ_تىزمىسى_قىممىتى 목록을 제공한다. */
public final class كىرگۈزۈش_تىزىم {
    private final ArrayList<String> كىرگۈزۈش_قىممىتى = new ArrayList<String>();
    public void 더하기(String قىممىتى) { كىرگۈزۈش_قىممىتى.add(قىممىتى); }
    public String ئوقۇ(int تەرتىپ_قىممىتى) { return كىرگۈزۈش_قىممىتى.get(تەرتىپ_قىممىتى); }
    public String ئالماشتۇرماق_قىممىتى(int تەرتىپ_قىممىتى, String قىممىتى) { return كىرگۈزۈش_قىممىتى.set(تەرتىپ_قىممىتى, قىممىتى); }
    public String 지우기(int تەرتىپ_قىممىتى) { return كىرگۈزۈش_قىممىتى.remove(تەرتىپ_قىممىتى); }
    public int چوڭلۇقى() { return كىرگۈزۈش_قىممىتى.size(); }
    public boolean 비었는가() { return كىرگۈزۈش_قىممىتى.isEmpty(); }
    public void تازىلىماق_مۇندەرىجە() { كىرگۈزۈش_قىممىتى.clear(); }
}
