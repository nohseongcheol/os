// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** प्रवेश_सुची(目錄): 순서가 있는 항목의 모음. 이 판은 स्ट्रिंग_मोल 목록을 제공한다. */
public final class प्रवेश_सुची {
    private final ArrayList<String> प्रवेश_मोल = new ArrayList<String>();
    public void 더하기(String मोल) { प्रवेश_मोल.add(मोल); }
    public String 읽기(int क्रम_मोल) { return प्रवेश_मोल.get(क्रम_मोल); }
    public String REPLACE_मोल(int क्रम_मोल, String मोल) { return प्रवेश_मोल.set(क्रम_मोल, मोल); }
    public String 지우기(int क्रम_मोल) { return प्रवेश_मोल.remove(क्रम_मोल); }
    public int आवाठ() { return प्रवेश_मोल.size(); }
    public boolean 비었는가() { return प्रवेश_मोल.isEmpty(); }
    public void पुसचें_TOC() { प्रवेश_मोल.clear(); }
}
