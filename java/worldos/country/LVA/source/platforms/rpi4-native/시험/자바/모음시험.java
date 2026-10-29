// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> ievade_Saraksts = new ArrayList<String>(); ievade_Saraksts.add("한글"); ievade_Saraksts.add("😀"); ievade_Saraksts.add("日本語");
        System.out.println(ievade_Saraksts.get(1)); System.out.println(ievade_Saraksts.set(1, "mainīt_VALUE")); System.out.println(ievade_Saraksts.remove(0));
        System.out.println(ievade_Saraksts.size()); System.out.println(ievade_Saraksts.get(0));
        Map<String, Integer> vārdnīca = new HashMap<String, Integer>();
        vārdnīca.put("하나", 1); vārdnīca.put("둘", 2); System.out.println(vārdnīca.put("하나", 3).intValue());
        System.out.println(vārdnīca.get("하나").intValue()); System.out.println(vārdnīca.containsKey("둘"));
        System.gc(); System.out.println(vārdnīca.remove("둘").intValue()); System.out.println(vārdnīca.size());
        ievade_Saraksts.clear(); vārdnīca.clear(); System.out.println(ievade_Saraksts.isEmpty()); System.out.println(vārdnīca.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Teksts")));
        String keep = "남는 Teksts"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
