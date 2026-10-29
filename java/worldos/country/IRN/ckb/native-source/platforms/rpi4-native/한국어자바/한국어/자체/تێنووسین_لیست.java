// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** تێنووسین_لیست(目錄): 순서가 있는 항목의 모음. 이 판은 رست_نرخ 목록을 제공한다. */
public final class تێنووسین_لیست {
    private final ArrayList<String> تێنووسین_نرخ = new ArrayList<String>();
    public void 더하기(String نرخ) { تێنووسین_نرخ.add(نرخ); }
    public String 읽기(int ئۆردەر_نرخ) { return تێنووسین_نرخ.get(ئۆردەر_نرخ); }
    public String جێنشین_کردن_نرخ(int ئۆردەر_نرخ, String نرخ) { return تێنووسین_نرخ.set(ئۆردەر_نرخ, نرخ); }
    public String 지우기(int ئۆردەر_نرخ) { return تێنووسین_نرخ.remove(ئۆردەر_نرخ); }
    public int گۆڕینی_ئەندازە() { return تێنووسین_نرخ.size(); }
    public boolean 비었는가() { return تێنووسین_نرخ.isEmpty(); }
    public void سڕینەوە_TOC() { تێنووسین_نرخ.clear(); }
}
