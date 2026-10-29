// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> dugal_xabaar_lim = new ArrayList<String>(); dugal_xabaar_lim.add("한글"); dugal_xabaar_lim.add("😀"); dugal_xabaar_lim.add("日本語");
        System.out.println(dugal_xabaar_lim.get(1)); System.out.println(dugal_xabaar_lim.set(1, "soppi_xëyma_16f64fe4")); System.out.println(dugal_xabaar_lim.remove(0));
        System.out.println(dugal_xabaar_lim.size()); System.out.println(dugal_xabaar_lim.get(0));
        Map<String, Integer> téereb_Tekki_baat = new HashMap<String, Integer>();
        téereb_Tekki_baat.put("하나", 1); téereb_Tekki_baat.put("둘", 2); System.out.println(téereb_Tekki_baat.put("하나", 3).intValue());
        System.out.println(téereb_Tekki_baat.get("하나").intValue()); System.out.println(téereb_Tekki_baat.containsKey("둘"));
        System.gc(); System.out.println(téereb_Tekki_baat.remove("둘").intValue()); System.out.println(téereb_Tekki_baat.size());
        dugal_xabaar_lim.clear(); téereb_Tekki_baat.clear(); System.out.println(dugal_xabaar_lim.isEmpty()); System.out.println(téereb_Tekki_baat.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Tekst")));
        String keep = "남는 Tekst"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
