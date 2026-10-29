// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** kiritish_Ro_yxat(目錄): 순서가 있는 항목의 모음. 이 판은 satr_VALUE 목록을 제공한다. */
public final class kiritish_Ro_yxat {
    private final ArrayList<String> kiritish_VALUE = new ArrayList<String>();
    public void 더하기(String VALUE) { kiritish_VALUE.add(VALUE); }
    public String Oʻqish(int tartib_VALUE) { return kiritish_VALUE.get(tartib_VALUE); }
    public String REPLACE_VALUE(int tartib_VALUE, String VALUE) { return kiritish_VALUE.set(tartib_VALUE, VALUE); }
    public String tozalash_kiritish(int tartib_VALUE) { return kiritish_VALUE.remove(tartib_VALUE); }
    public int Hajmi() { return kiritish_VALUE.size(); }
    public boolean 비었는가() { return kiritish_VALUE.isEmpty(); }
    public void tozalamoq_TOC() { kiritish_VALUE.clear(); }
}
