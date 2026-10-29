// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> iontráil_Liosta = new ArrayList<String>(); iontráil_Liosta.add("한글"); iontráil_Liosta.add("😀"); iontráil_Liosta.add("日本語");
        System.out.println(iontráil_Liosta.get(1)); System.out.println(iontráil_Liosta.set(1, "athraigh_VALUE")); System.out.println(iontráil_Liosta.remove(0));
        System.out.println(iontráil_Liosta.size()); System.out.println(iontráil_Liosta.get(0));
        Map<String, Integer> foclóir = new HashMap<String, Integer>();
        foclóir.put("하나", 1); foclóir.put("둘", 2); System.out.println(foclóir.put("하나", 3).intValue());
        System.out.println(foclóir.get("하나").intValue()); System.out.println(foclóir.containsKey("둘"));
        System.gc(); System.out.println(foclóir.remove("둘").intValue()); System.out.println(foclóir.size());
        iontráil_Liosta.clear(); foclóir.clear(); System.out.println(iontráil_Liosta.isEmpty()); System.out.println(foclóir.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Téacs")));
        String keep = "남는 Téacs"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
