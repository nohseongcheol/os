// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 출력(出力)과 ສະຕຣີມ_ຄ່າ: 순서를 보존해 내보내는 바이트의 ຊ່ອງທາງ_ເຂົ້າໃນ. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void ຂຽນ(int ຄ່າ) throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { 표준흐름.write(ຄ່າ);
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public void ຂຽນ(byte[] ຂໍ້ມູນ) throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { 표준흐름.write(ຂໍ້ມູນ);
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public void ຂຽນ(byte[] ຂໍ້ມູນ, int ແລ່ນ, int ຄວາມຍາວ_ຄ່າ) throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { 표준흐름.write(ຂໍ້ມູນ, ແລ່ນ, ຄວາມຍາວ_ຄ່າ);
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public void 내보내기() throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { 표준흐름.flush();
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public void ປິດ() throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { 표준흐름.close();
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
}
