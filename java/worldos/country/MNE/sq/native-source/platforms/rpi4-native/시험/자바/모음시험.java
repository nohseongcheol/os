// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> futje_Listë = new ArrayList<String>(); futje_Listë.add("한글"); futje_Listë.add("😀"); futje_Listë.add("日本語");
        System.out.println(futje_Listë.get(1)); System.out.println(futje_Listë.set(1, "ndryshoj_VALUE")); System.out.println(futje_Listë.remove(0));
        System.out.println(futje_Listë.size()); System.out.println(futje_Listë.get(0));
        Map<String, Integer> fjalor = new HashMap<String, Integer>();
        fjalor.put("하나", 1); fjalor.put("둘", 2); System.out.println(fjalor.put("하나", 3).intValue());
        System.out.println(fjalor.get("하나").intValue()); System.out.println(fjalor.containsKey("둘"));
        System.gc(); System.out.println(fjalor.remove("둘").intValue()); System.out.println(fjalor.size());
        futje_Listë.clear(); fjalor.clear(); System.out.println(futje_Listë.isEmpty()); System.out.println(fjalor.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Teksti")));
        String keep = "남는 Teksti"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
