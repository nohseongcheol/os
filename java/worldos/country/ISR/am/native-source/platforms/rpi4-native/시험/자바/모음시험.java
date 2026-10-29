// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> ምዝግብ_ዝርዝር = new ArrayList<String>(); ምዝግብ_ዝርዝር.add("한글"); ምዝግብ_ዝርዝር.add("😀"); ምዝግብ_ዝርዝር.add("日本語");
        System.out.println(ምዝግብ_ዝርዝር.get(1)); System.out.println(ምዝግብ_ዝርዝር.set(1, "ለውጥ_እሴት")); System.out.println(ምዝግብ_ዝርዝር.remove(0));
        System.out.println(ምዝግብ_ዝርዝር.size()); System.out.println(ምዝግብ_ዝርዝር.get(0));
        Map<String, Integer> መዝገበ_ቃላት = new HashMap<String, Integer>();
        መዝገበ_ቃላት.put("하나", 1); መዝገበ_ቃላት.put("둘", 2); System.out.println(መዝገበ_ቃላት.put("하나", 3).intValue());
        System.out.println(መዝገበ_ቃላት.get("하나").intValue()); System.out.println(መዝገበ_ቃላት.containsKey("둘"));
        System.gc(); System.out.println(መዝገበ_ቃላት.remove("둘").intValue()); System.out.println(መዝገበ_ቃላት.size());
        ምዝግብ_ዝርዝር.clear(); መዝገበ_ቃላት.clear(); System.out.println(ምዝግብ_ዝርዝር.isEmpty()); System.out.println(መዝገበ_ቃላት.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("ጽሁፍ")));
        String keep = "남는 ጽሁፍ"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
