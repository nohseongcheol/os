// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** oppføring_Liste(目錄): 순서가 있는 항목의 모음. 이 판은 streng_VALUE 목록을 제공한다. */
public final class oppføring_Liste {
    private final ArrayList<String> oppføring_VALUE = new ArrayList<String>();
    public void 더하기(String VALUE) { oppføring_VALUE.add(VALUE); }
    public String Les(int rekkjefølgje_VALUE) { return oppføring_VALUE.get(rekkjefølgje_VALUE); }
    public String REPLACE_VALUE(int rekkjefølgje_VALUE, String VALUE) { return oppføring_VALUE.set(rekkjefølgje_VALUE, VALUE); }
    public String 지우기(int rekkjefølgje_VALUE) { return oppføring_VALUE.remove(rekkjefølgje_VALUE); }
    public int Storleik() { return oppføring_VALUE.size(); }
    public boolean informasjonsteknologi_tom_VALUE() { return oppføring_VALUE.isEmpty(); }
    public void fjerne_Innhald() { oppføring_VALUE.clear(); }
}
