// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> færsla_Listi = new ArrayList<String>(); færsla_Listi.add("한글"); færsla_Listi.add("😀"); færsla_Listi.add("日本語");
        System.out.println(færsla_Listi.get(1)); System.out.println(færsla_Listi.set(1, "breyta_VALUE_16f64fe4")); System.out.println(færsla_Listi.remove(0));
        System.out.println(færsla_Listi.size()); System.out.println(færsla_Listi.get(0));
        Map<String, Integer> orðabók = new HashMap<String, Integer>();
        orðabók.put("하나", 1); orðabók.put("둘", 2); System.out.println(orðabók.put("하나", 3).intValue());
        System.out.println(orðabók.get("하나").intValue()); System.out.println(orðabók.containsKey("둘"));
        System.gc(); System.out.println(orðabók.remove("둘").intValue()); System.out.println(orðabók.size());
        færsla_Listi.clear(); orðabók.clear(); System.out.println(færsla_Listi.isEmpty()); System.out.println(orðabók.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Texti")));
        String keep = "남는 Texti"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
