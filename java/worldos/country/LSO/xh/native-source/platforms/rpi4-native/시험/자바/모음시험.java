// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> ufako_nkcukacha_uludwe = new ArrayList<String>(); ufako_nkcukacha_uludwe.add("한글"); ufako_nkcukacha_uludwe.add("😀"); ufako_nkcukacha_uludwe.add("日本語");
        System.out.println(ufako_nkcukacha_uludwe.get(1)); System.out.println(ufako_nkcukacha_uludwe.set(1, "tshintsha_ixabiso")); System.out.println(ufako_nkcukacha_uludwe.remove(0));
        System.out.println(ufako_nkcukacha_uludwe.size()); System.out.println(ufako_nkcukacha_uludwe.get(0));
        Map<String, Integer> isichazi_magama = new HashMap<String, Integer>();
        isichazi_magama.put("하나", 1); isichazi_magama.put("둘", 2); System.out.println(isichazi_magama.put("하나", 3).intValue());
        System.out.println(isichazi_magama.get("하나").intValue()); System.out.println(isichazi_magama.containsKey("둘"));
        System.gc(); System.out.println(isichazi_magama.remove("둘").intValue()); System.out.println(isichazi_magama.size());
        ufako_nkcukacha_uludwe.clear(); isichazi_magama.clear(); System.out.println(ufako_nkcukacha_uludwe.isEmpty()); System.out.println(isichazi_magama.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Umbhalo")));
        String keep = "남는 Umbhalo"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
