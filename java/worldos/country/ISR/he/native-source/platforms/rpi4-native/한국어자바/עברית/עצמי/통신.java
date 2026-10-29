// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package עברית.עצמי;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP יחידת_נתונים. חיצוני_ערך 주소는 ספרה_ערך 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket פתח(int הסב_ערך) throws קלט_פלט_חריגה {
        try { return new DatagramSocket(הסב_ערך);
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public static void שלח(DatagramSocket משתתף, int הסב_ערך, String תוכן_ערך) throws קלט_פלט_חריגה {
        try {
        שלח(משתתף, "127.0.0.1", הסב_ערך, תוכן_ערך);
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public static void שלח(DatagramSocket משתתף, String למען, int הסב_ערך, String תוכן_ערך) throws קלט_פלט_חריגה {
        try {
        byte[] בית_ערך = 문자.לקדד(תוכן_ערך);
        משתתף.send(new DatagramPacket(בית_ערך, בית_ערך.length, InetAddress.getByName(למען), הסב_ערך));
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public static String לקבל(DatagramSocket משתתף) throws קלט_פלט_חריגה {
        try {
        byte[] בית_ערך = new byte[512]; DatagramPacket יחידת_נתונים = new DatagramPacket(בית_ערך, בית_ערך.length); משתתף.receive(יחידת_נתונים);
        byte[] תוצאה = new byte[יחידת_נתונים.getLength()]; System.arraycopy(בית_ערך, 0, תוצאה, 0, תוצאה.length); return 문자.פענח_נתונים(תוצאה);
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public static void פסק_זמן(DatagramSocket משתתף, int 밀리초) throws קלט_פלט_חריגה {
        try { משתתף.setSoTimeout(밀리초);
        } catch (java.io.IOException שגיאה) { throw המר_חריגה.קלט_פלט(שגיאה); }
        catch (RuntimeException שגיאה) { throw המר_חריגה.לבצע_פקודה(שגיאה); }
    }
    public static void סגירה(DatagramSocket משתתף) { משתתף.close(); }
}
