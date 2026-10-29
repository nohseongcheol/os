// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malti.자체;

/** 출력(出力)과 Stream_VALUE: 순서를 보존해 내보내는 바이트의 Kanal_entrata. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void kiteb(int VALUE) throws 입출력예외 {
        try { 표준흐름.write(VALUE);
        } catch (java.io.IOException żball) { throw 예외변환.I_O(żball); }
        catch (RuntimeException żball) { throw 예외변환.eżegwixxa_kmand(żball); }
    }
    public void kiteb(byte[] data) throws 입출력예외 {
        try { 표준흐름.write(data);
        } catch (java.io.IOException żball) { throw 예외변환.I_O(żball); }
        catch (RuntimeException żball) { throw 예외변환.eżegwixxa_kmand(żball); }
    }
    public void kiteb(byte[] data, int serje, int tul_VALUE) throws 입출력예외 {
        try { 표준흐름.write(data, serje, tul_VALUE);
        } catch (java.io.IOException żball) { throw 예외변환.I_O(żball); }
        catch (RuntimeException żball) { throw 예외변환.eżegwixxa_kmand(żball); }
    }
    public void 내보내기() throws 입출력예외 {
        try { 표준흐름.flush();
        } catch (java.io.IOException żball) { throw 예외변환.I_O(żball); }
        catch (RuntimeException żball) { throw 예외변환.eżegwixxa_kmand(żball); }
    }
    public void agħlaq() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException żball) { throw 예외변환.I_O(żball); }
        catch (RuntimeException żball) { throw 예외변환.eżegwixxa_kmand(żball); }
    }
}
