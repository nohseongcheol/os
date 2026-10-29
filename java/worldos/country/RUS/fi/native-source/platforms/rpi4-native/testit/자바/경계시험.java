// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int virhe_ARVO() { throw new IllegalStateException("작업 중 poikkeus"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] pätemätön_KR = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("MATRIISI_ARVO MUUNNA_ARVO 검사"); }
        Object[] SMS_luettelo = new String[2];
        try { SMS_luettelo[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("MATRIISI_ARVO TYYPPI_ARVO 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, SMS_luettelo, 0, 2); } catch (ArrayStoreException e) { System.out.println("kopioida_ARVO TYYPPI_ARVO 검사"); }
        System.out.println((String)SMS_luettelo[0]);
        try { "teksti".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 leikata"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object lukita_ARVO = new Object(); try { synchronized (lukita_ARVO) { virhe_ARVO(); } } catch (IllegalStateException e) { System.out.println("lukita_ARVO poikkeus"); }
        synchronized (lukita_ARVO) { System.out.println("lukita_ARVO 회수"); }
        byte[] data = {0, (byte)128, (byte)255, 10};
        FileOutputStream tulostuspaikka = new FileOutputStream("tavu_ARVO.bin"); tulostuspaikka.write(data); tulostuspaikka.flush(); tulostuspaikka.close();
        FileInputStream syöte_ARVO = new FileInputStream("tavu_ARVO.bin"); byte[] lukea_KR = new byte[8];
        System.out.println(syöte_ARVO.read(lukea_KR, 2, 4)); System.out.println(lukea_KR[3] + ":" + lukea_KR[4]);
        System.out.println(syöte_ARVO.read(lukea_KR)); System.out.println(syöte_ARVO.read(lukea_KR, 0, 0)); syöte_ARVO.close();
        try { syöte_ARVO.read(); } catch (IOException e) { System.out.println("닫힌 tiedoston_nimi"); }
    }
}
