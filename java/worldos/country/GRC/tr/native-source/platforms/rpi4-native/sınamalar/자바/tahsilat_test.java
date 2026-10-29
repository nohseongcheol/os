// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class tahsilat_test {
    public static void main(String[] a) {
        List<String> girdi_Liste = new ArrayList<String>(); girdi_Liste.add("한글"); girdi_Liste.add("😀"); girdi_Liste.add("日本語");
        System.out.println(girdi_Liste.get(1)); System.out.println(girdi_Liste.set(1, "değiştirmek_değer")); System.out.println(girdi_Liste.remove(0));
        System.out.println(girdi_Liste.size()); System.out.println(girdi_Liste.get(0));
        Map<String, Integer> sözlük = new HashMap<String, Integer>();
        sözlük.put("하나", 1); sözlük.put("둘", 2); System.out.println(sözlük.put("하나", 3).intValue());
        System.out.println(sözlük.get("하나").intValue()); System.out.println(sözlük.containsKey("둘"));
        System.gc(); System.out.println(sözlük.remove("둘").intValue()); System.out.println(sözlük.size());
        girdi_Liste.clear(); sözlük.clear(); System.out.println(girdi_Liste.isEmpty()); System.out.println(sözlük.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("metin")));
        String keep = "남는 metin"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
