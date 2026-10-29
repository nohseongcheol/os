// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 境界一覧試験 {
    static int 失敗値() { throw new IllegalStateException("作業 중 例外"); }
    public static void main(String[] a) throws Exception {
        Object 平文配列 = new Object[2]; System.out.println(平文配列 instanceof String[]);
        try { String[] 無効結果 = (String[])平文配列; } catch (ClassCastException e) { System.out.println("配列値 値変換 検査項目"); }
        Object[] 本文一覧 = new String[2];
        try { 本文一覧[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("配列値 型値 検査項目"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, 本文一覧, 0, 2); } catch (ArrayStoreException e) { System.out.println("値複写 型値 検査項目"); }
        System.out.println((String)本文一覧[0]);
        try { "文".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("文字 切抜き"); }
        Integer 一値 = Integer.valueOf(127), 二値 = Integer.valueOf(127); System.out.println(一値 == 二値);
        Object 錠値 = new Object(); try { synchronized (錠値) { 失敗値(); } } catch (IllegalStateException e) { System.out.println("錠値 例外"); }
        synchronized (錠値) { System.out.println("錠値 회수"); }
        byte[] データ = {0, (byte)128, (byte)255, 10};
        FileOutputStream 出力 = new FileOutputStream("バイト値.bin"); 出力.write(データ); 出力.flush(); 出力.close();
        FileInputStream 入力値 = new FileInputStream("バイト値.bin"); byte[] 結果読取 = new byte[8];
        System.out.println(入力値.read(結果読取, 2, 4)); System.out.println(結果読取[3] + ":" + 結果読取[4]);
        System.out.println(入力値.read(結果読取)); System.out.println(入力値.read(結果読取, 0, 0)); 入力値.close();
        try { 入力値.read(); } catch (IOException e) { System.out.println("닫힌 ファイル"); }
    }
}
