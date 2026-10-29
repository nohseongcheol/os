// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> පිවිසුම_ලැයිස්තුව = new ArrayList<String>(); පිවිසුම_ලැයිස්තුව.add("한글"); පිවිසුම_ලැයිස්තුව.add("😀"); පිවිසුම_ලැයිස්තුව.add("日本語");
        System.out.println(පිවිසුම_ලැයිස්තුව.get(1)); System.out.println(පිවිසුම_ලැයිස්තුව.set(1, "වෙනස්_කරන්න_අගය")); System.out.println(පිවිසුම_ලැයිස්තුව.remove(0));
        System.out.println(පිවිසුම_ලැයිස්තුව.size()); System.out.println(පිවිසුම_ලැයිස්තුව.get(0));
        Map<String, Integer> ශබ්දකෝෂය = new HashMap<String, Integer>();
        ශබ්දකෝෂය.put("하나", 1); ශබ්දකෝෂය.put("둘", 2); System.out.println(ශබ්දකෝෂය.put("하나", 3).intValue());
        System.out.println(ශබ්දකෝෂය.get("하나").intValue()); System.out.println(ශබ්දකෝෂය.containsKey("둘"));
        System.gc(); System.out.println(ශබ්දකෝෂය.remove("둘").intValue()); System.out.println(ශබ්දකෝෂය.size());
        පිවිසුම_ලැයිස්තුව.clear(); ශබ්දකෝෂය.clear(); System.out.println(පිවිසුම_ලැයිස්තුව.isEmpty()); System.out.println(ශබ්දකෝෂය.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("පෙළ")));
        String keep = "남는 පෙළ"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
