// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> ìgbéwọlé_Àtòkọ = new ArrayList<String>(); ìgbéwọlé_Àtòkọ.add("한글"); ìgbéwọlé_Àtòkọ.add("😀"); ìgbéwọlé_Àtòkọ.add("日本語");
        System.out.println(ìgbéwọlé_Àtòkọ.get(1)); System.out.println(ìgbéwọlé_Àtòkọ.set(1, "ṣàyípadà_iye")); System.out.println(ìgbéwọlé_Àtòkọ.remove(0));
        System.out.println(ìgbéwọlé_Àtòkọ.size()); System.out.println(ìgbéwọlé_Àtòkọ.get(0));
        Map<String, Integer> àtumọ̀èdè = new HashMap<String, Integer>();
        àtumọ̀èdè.put("하나", 1); àtumọ̀èdè.put("둘", 2); System.out.println(àtumọ̀èdè.put("하나", 3).intValue());
        System.out.println(àtumọ̀èdè.get("하나").intValue()); System.out.println(àtumọ̀èdè.containsKey("둘"));
        System.gc(); System.out.println(àtumọ̀èdè.remove("둘").intValue()); System.out.println(àtumọ̀èdè.size());
        ìgbéwọlé_Àtòkọ.clear(); àtumọ̀èdè.clear(); System.out.println(ìgbéwọlé_Àtòkọ.isEmpty()); System.out.println(àtumọ̀èdè.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("글")));
        String keep = "남는 SMS"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
