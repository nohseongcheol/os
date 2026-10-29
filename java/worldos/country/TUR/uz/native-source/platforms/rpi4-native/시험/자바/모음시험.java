// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> kiritish_Ro_yxat = new ArrayList<String>(); kiritish_Ro_yxat.add("한글"); kiritish_Ro_yxat.add("😀"); kiritish_Ro_yxat.add("日本語");
        System.out.println(kiritish_Ro_yxat.get(1)); System.out.println(kiritish_Ro_yxat.set(1, "o_zgartirmoq_VALUE")); System.out.println(kiritish_Ro_yxat.remove(0));
        System.out.println(kiritish_Ro_yxat.size()); System.out.println(kiritish_Ro_yxat.get(0));
        Map<String, Integer> lug_at = new HashMap<String, Integer>();
        lug_at.put("하나", 1); lug_at.put("둘", 2); System.out.println(lug_at.put("하나", 3).intValue());
        System.out.println(lug_at.get("하나").intValue()); System.out.println(lug_at.containsKey("둘"));
        System.gc(); System.out.println(lug_at.remove("둘").intValue()); System.out.println(lug_at.size());
        kiritish_Ro_yxat.clear(); lug_at.clear(); System.out.println(kiritish_Ro_yxat.isEmpty()); System.out.println(lug_at.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Matn")));
        String keep = "남는 Matn"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
