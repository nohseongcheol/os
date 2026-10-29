// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** ворида_Рӯйхат(目錄): 순서가 있는 항목의 모음. 이 판은 сатр_қимат_6ca8363c 목록을 제공한다. */
public final class ворида_Рӯйхат {
    private final ArrayList<String> ворида_қимат = new ArrayList<String>();
    public void 더하기(String қимат) { ворида_қимат.add(қимат); }
    public String Хондан(int тартиб_қимат) { return ворида_қимат.get(тартиб_қимат); }
    public String ҷойгузин_кардан_қимат(int тартиб_қимат, String қимат) { return ворида_қимат.set(тартиб_қимат, қимат); }
    public String 지우기(int тартиб_қимат) { return ворида_қимат.remove(тартиб_қимат); }
    public int андоза_кардан() { return ворида_қимат.size(); }
    public boolean 비었는가() { return ворида_қимат.isEmpty(); }
    public void пок_кардан_Мундариҷа() { ворида_қимат.clear(); }
}
