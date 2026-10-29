// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package فارسی.بومی;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 کاربر 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class پرونده {
    private پرونده() {}
    public static byte[] 바이트읽기(String نام) throws ورودی_خروجی_استثنا {
        try {
        FileInputStream جریان_مقدار = new FileInputStream(نام);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, مقدار;
            while ((مقدار = جریان_مقدار.read()) != -1) { if (수 == 임시.length) throw new ورودی_خروجی_استثنا("پرونده اندازه 제한"); 임시[수++] = (byte)مقدار; }
            byte[] سنجش = new byte[수]; System.arraycopy(임시, 0, سنجش, 0, 수); return سنجش;
        } finally { جریان_مقدار.close(); }
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public static void نوشتن_بایت_مقدار(String نام, byte[] محتوا_مقدار) throws ورودی_خروجی_استثنا {
        try {
        FileOutputStream جریان_مقدار = new FileOutputStream(نام);
        try { for (int حلقه_فهرست = 0; حلقه_فهرست < محتوا_مقدار.length; حلقه_فهرست++) جریان_مقدار.write(محتوا_مقدار[حلقه_فهرست] & 255); } finally { جریان_مقدار.close(); }
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public static String خواندن(String نام) throws ورودی_خروجی_استثنا {
        try { return 문자.رمزگشایی_داده_ها(바이트읽기(نام));
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public static void نوشتن(String نام, String محتوا_مقدار) throws ورودی_خروجی_استثنا {
        try { نوشتن_بایت_مقدار(نام, 문자.부호화(محتوا_مقدار));
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
}
