// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> inskrywing_Lys = new ArrayList<String>(); inskrywing_Lys.add("한글"); inskrywing_Lys.add("😀"); inskrywing_Lys.add("日本語");
        System.out.println(inskrywing_Lys.get(1)); System.out.println(inskrywing_Lys.set(1, "verander_VALUE")); System.out.println(inskrywing_Lys.remove(0));
        System.out.println(inskrywing_Lys.size()); System.out.println(inskrywing_Lys.get(0));
        Map<String, Integer> woordeboek = new HashMap<String, Integer>();
        woordeboek.put("하나", 1); woordeboek.put("둘", 2); System.out.println(woordeboek.put("하나", 3).intValue());
        System.out.println(woordeboek.get("하나").intValue()); System.out.println(woordeboek.containsKey("둘"));
        System.gc(); System.out.println(woordeboek.remove("둘").intValue()); System.out.println(woordeboek.size());
        inskrywing_Lys.clear(); woordeboek.clear(); System.out.println(inskrywing_Lys.isEmpty()); System.out.println(woordeboek.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Teks")));
        String keep = "남는 Teks"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
