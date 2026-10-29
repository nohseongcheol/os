// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> naatnugol_Doggol = new ArrayList<String>(); naatnugol_Doggol.add("한글"); naatnugol_Doggol.add("😀"); naatnugol_Doggol.add("日本語");
        System.out.println(naatnugol_Doggol.get(1)); System.out.println(naatnugol_Doggol.set(1, "waklude_njaru")); System.out.println(naatnugol_Doggol.remove(0));
        System.out.println(naatnugol_Doggol.size()); System.out.println(naatnugol_Doggol.get(0));
        Map<String, Integer> 사전 = new HashMap<String, Integer>();
        사전.put("하나", 1); 사전.put("둘", 2); System.out.println(사전.put("하나", 3).intValue());
        System.out.println(사전.get("하나").intValue()); System.out.println(사전.containsKey("둘"));
        System.gc(); System.out.println(사전.remove("둘").intValue()); System.out.println(사전.size());
        naatnugol_Doggol.clear(); 사전.clear(); System.out.println(naatnugol_Doggol.isEmpty()); System.out.println(사전.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("글")));
        String keep = "남는 binndi"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
