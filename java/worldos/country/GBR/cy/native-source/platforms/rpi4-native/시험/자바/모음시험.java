// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> cofnod_Rhestr = new ArrayList<String>(); cofnod_Rhestr.add("한글"); cofnod_Rhestr.add("😀"); cofnod_Rhestr.add("日本語");
        System.out.println(cofnod_Rhestr.get(1)); System.out.println(cofnod_Rhestr.set(1, "newid_VALUE")); System.out.println(cofnod_Rhestr.remove(0));
        System.out.println(cofnod_Rhestr.size()); System.out.println(cofnod_Rhestr.get(0));
        Map<String, Integer> geiriadur = new HashMap<String, Integer>();
        geiriadur.put("하나", 1); geiriadur.put("둘", 2); System.out.println(geiriadur.put("하나", 3).intValue());
        System.out.println(geiriadur.get("하나").intValue()); System.out.println(geiriadur.containsKey("둘"));
        System.gc(); System.out.println(geiriadur.remove("둘").intValue()); System.out.println(geiriadur.size());
        cofnod_Rhestr.clear(); geiriadur.clear(); System.out.println(cofnod_Rhestr.isEmpty()); System.out.println(geiriadur.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Testun")));
        String keep = "남는 Testun"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
