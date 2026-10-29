// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> tāurunga_Rārangi = new ArrayList<String>(); tāurunga_Rārangi.add("한글"); tāurunga_Rārangi.add("😀"); tāurunga_Rārangi.add("日本語");
        System.out.println(tāurunga_Rārangi.get(1)); System.out.println(tāurunga_Rārangi.set(1, "huri_uara")); System.out.println(tāurunga_Rārangi.remove(0));
        System.out.println(tāurunga_Rārangi.size()); System.out.println(tāurunga_Rārangi.get(0));
        Map<String, Integer> papakupu = new HashMap<String, Integer>();
        papakupu.put("하나", 1); papakupu.put("둘", 2); System.out.println(papakupu.put("하나", 3).intValue());
        System.out.println(papakupu.get("하나").intValue()); System.out.println(papakupu.containsKey("둘"));
        System.gc(); System.out.println(papakupu.remove("둘").intValue()); System.out.println(papakupu.size());
        tāurunga_Rārangi.clear(); papakupu.clear(); System.out.println(tāurunga_Rārangi.isEmpty()); System.out.println(papakupu.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Ngā_kupu")));
        String keep = "남는 Ngā_kupu"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
