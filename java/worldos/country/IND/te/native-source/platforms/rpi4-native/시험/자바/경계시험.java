// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int వైఫల్యం_మూల్యం() { throw new IllegalStateException("작업 중 మినహాయింపు"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] చెల్లని_ప్రమాణం = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("శ్రేణి_మూల్యం 변환 검사"); }
        Object[] పాఠం_జాబితా = new String[2];
        try { పాఠం_జాబితా[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("శ్రేణి_మూల్యం టైప్_చేయండి_మూల్యం 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, పాఠం_జాబితా, 0, 2); } catch (ArrayStoreException e) { System.out.println("కాపీ_మూల్యం టైప్_చేయండి_మూల్యం 검사"); }
        System.out.println((String)పాఠం_జాబితా[0]);
        try { "పాఠ్యము".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 క్లిప్"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object 잠금 = new Object(); try { synchronized (잠금) { వైఫల్యం_మూల్యం(); } } catch (IllegalStateException e) { System.out.println("잠금 మినహాయింపు"); }
        synchronized (잠금) { System.out.println("잠금 회수"); }
        byte[] డేటా = {0, (byte)128, (byte)255, 10};
        FileOutputStream అవుట్పుట్ = new FileOutputStream("బైట్_మూల్యం.bin"); అవుట్పుట్.write(డేటా); అవుట్పుట్.flush(); అవుట్పుట్.close();
        FileInputStream 입력 = new FileInputStream("బైట్_మూల్యం.bin"); byte[] 읽음 = new byte[8];
        System.out.println(입력.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(입력.read(읽음)); System.out.println(입력.read(읽음, 0, 0)); 입력.close();
        try { 입력.read(); } catch (IOException e) { System.out.println("닫힌 దస్త్రం"); }
    }
}
