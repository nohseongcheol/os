// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class perintä_testi {
    public static void main(String[] a) {
        List<String> merkintä_luettelo = new ArrayList<String>(); merkintä_luettelo.add("한글"); merkintä_luettelo.add("😀"); merkintä_luettelo.add("日本語");
        System.out.println(merkintä_luettelo.get(1)); System.out.println(merkintä_luettelo.set(1, "muuttaa_ARVO")); System.out.println(merkintä_luettelo.remove(0));
        System.out.println(merkintä_luettelo.size()); System.out.println(merkintä_luettelo.get(0));
        Map<String, Integer> sanakirja = new HashMap<String, Integer>();
        sanakirja.put("하나", 1); sanakirja.put("둘", 2); System.out.println(sanakirja.put("하나", 3).intValue());
        System.out.println(sanakirja.get("하나").intValue()); System.out.println(sanakirja.containsKey("둘"));
        System.gc(); System.out.println(sanakirja.remove("둘").intValue()); System.out.println(sanakirja.size());
        merkintä_luettelo.clear(); sanakirja.clear(); System.out.println(merkintä_luettelo.isEmpty()); System.out.println(sanakirja.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("teksti")));
        String keep = "남는 teksti"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
