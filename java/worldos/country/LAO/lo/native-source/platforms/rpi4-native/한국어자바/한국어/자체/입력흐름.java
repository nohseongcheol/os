// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 ສະຕຣີມ_ຄ່າ: 순서대로 들어오는 바이트를 읽는 ຊ່ອງທາງ_ເຂົ້າໃນ. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int 읽기() throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { return 표준흐름.read();
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public int 읽기(byte[] ຂໍ້ມູນ) throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { return 표준흐름.read(ຂໍ້ມູນ);
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public int 읽기(byte[] ຂໍ້ມູນ, int ແລ່ນ, int ຄວາມຍາວ_ຄ່າ) throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { return 표준흐름.read(ຂໍ້ມູນ, ແລ່ນ, ຄວາມຍາວ_ຄ່າ);
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public void ປິດ() throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { 표준흐름.close();
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
}
