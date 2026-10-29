// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class အစုစမ်းသပ် {
    public static void main(String[] a) {
        List<String> အချက်စာရင်း = new ArrayList<String>(); အချက်စာရင်း.add("한글"); အချက်စာရင်း.add("😀"); အချက်စာရင်း.add("日本語");
        System.out.println(အချက်စာရင်း.get(1)); System.out.println(အချက်စာရင်း.set(1, "တန်ဖိုးပြောင်း")); System.out.println(အချက်စာရင်း.remove(0));
        System.out.println(အချက်စာရင်း.size()); System.out.println(အချက်စာရင်း.get(0));
        Map<String, Integer> အဘိဓာန် = new HashMap<String, Integer>();
        အဘိဓာန်.put("တစ်တန်ဖိုး", 1); အဘိဓာန်.put("둘", 2); System.out.println(အဘိဓာန်.put("တစ်တန်ဖိုး", 3).intValue());
        System.out.println(အဘိဓာန်.get("တစ်တန်ဖိုး").intValue()); System.out.println(အဘိဓာန်.containsKey("둘"));
        System.gc(); System.out.println(အဘိဓာန်.remove("둘").intValue()); System.out.println(အဘိဓာန်.size());
        အချက်စာရင်း.clear(); အဘိဓာန်.clear(); System.out.println(အချက်စာရင်း.isEmpty()); System.out.println(အဘိဓာန်.isEmpty());
        System.out.println("한글😀အက္ခရာ".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("글")));
        String keep = "남는 စာသား"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
