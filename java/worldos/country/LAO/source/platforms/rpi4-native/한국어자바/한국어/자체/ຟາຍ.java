// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 ຜູ້ໃຊ້ 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class ຟາຍ {
    private ຟາຍ() {}
    public static byte[] 바이트읽기(String ຊື່) throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try {
        FileInputStream ສະຕຣີມ_ຄ່າ = new FileInputStream(ຊື່);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, ຄ່າ;
            while ((ຄ່າ = ສະຕຣີມ_ຄ່າ.read()) != -1) { if (수 == 임시.length) throw new ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ("ຟາຍ ຂະ_ຫນາດ 제한"); 임시[수++] = (byte)ຄ່າ; }
            byte[] ມາດຕະການ = new byte[수]; System.arraycopy(임시, 0, ມາດຕະການ, 0, 수); return ມາດຕະການ;
        } finally { ສະຕຣີມ_ຄ່າ.close(); }
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public static void ຂຽນ_ໄບ_ຄ່າ(String ຊື່, byte[] ເນື້ອໃນ_ຄ່າ_cb0f2404) throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try {
        FileOutputStream ສະຕຣີມ_ຄ່າ = new FileOutputStream(ຊື່);
        try { for (int ຫ່ວງ_ດັດຊະນີ = 0; ຫ່ວງ_ດັດຊະນີ < ເນື້ອໃນ_ຄ່າ_cb0f2404.length; ຫ່ວງ_ດັດຊະນີ++) ສະຕຣີມ_ຄ່າ.write(ເນື້ອໃນ_ຄ່າ_cb0f2404[ຫ່ວງ_ດັດຊະນີ] & 255); } finally { ສະຕຣີມ_ຄ່າ.close(); }
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public static String 읽기(String ຊື່) throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { return 문자.ຖອດລະຫັດ_ຂໍ້ມູນ(바이트읽기(ຊື່));
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public static void ຂຽນ(String ຊື່, String ເນື້ອໃນ_ຄ່າ_cb0f2404) throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { ຂຽນ_ໄບ_ຄ່າ(ຊື່, 문자.부호화(ເນື້ອໃນ_ຄ່າ_cb0f2404));
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
}
