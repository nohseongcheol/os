// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> પ્રવેશ_સૂચી = new ArrayList<String>(); પ્રવેશ_સૂચી.add("한글"); પ્રવેશ_સૂચી.add("😀"); પ્રવેશ_સૂચી.add("日本語");
        System.out.println(પ્રવેશ_સૂચી.get(1)); System.out.println(પ્રવેશ_સૂચી.set(1, "પરિવર્તન_કરો_મૂલ્ય")); System.out.println(પ્રવેશ_સૂચી.remove(0));
        System.out.println(પ્રવેશ_સૂચી.size()); System.out.println(પ્રવેશ_સૂચી.get(0));
        Map<String, Integer> શબ્દકોશ = new HashMap<String, Integer>();
        શબ્દકોશ.put("하나", 1); શબ્દકોશ.put("둘", 2); System.out.println(શબ્દકોશ.put("하나", 3).intValue());
        System.out.println(શબ્દકોશ.get("하나").intValue()); System.out.println(શબ્દકોશ.containsKey("둘"));
        System.gc(); System.out.println(શબ્દકોશ.remove("둘").intValue()); System.out.println(શબ્દકોશ.size());
        પ્રવેશ_સૂચી.clear(); શબ્દકોશ.clear(); System.out.println(પ્રવેશ_સૂચી.isEmpty()); System.out.println(શબ્દકોશ.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("લખાણ")));
        String keep = "남는 લખાણ"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
