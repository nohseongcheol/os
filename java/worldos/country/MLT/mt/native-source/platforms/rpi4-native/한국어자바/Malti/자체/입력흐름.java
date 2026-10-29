// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malti.자체;

/** 입력(入力)과 Stream_VALUE: 순서대로 들어오는 바이트를 읽는 Kanal_entrata. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int 읽기() throws 입출력예외 {
        try { return 표준흐름.read();
        } catch (java.io.IOException żball) { throw 예외변환.I_O(żball); }
        catch (RuntimeException żball) { throw 예외변환.eżegwixxa_kmand(żball); }
    }
    public int 읽기(byte[] data) throws 입출력예외 {
        try { return 표준흐름.read(data);
        } catch (java.io.IOException żball) { throw 예외변환.I_O(żball); }
        catch (RuntimeException żball) { throw 예외변환.eżegwixxa_kmand(żball); }
    }
    public int 읽기(byte[] data, int serje, int tul_VALUE) throws 입출력예외 {
        try { return 표준흐름.read(data, serje, tul_VALUE);
        } catch (java.io.IOException żball) { throw 예외변환.I_O(żball); }
        catch (RuntimeException żball) { throw 예외변환.eżegwixxa_kmand(żball); }
    }
    public void agħlaq() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException żball) { throw 예외변환.I_O(żball); }
        catch (RuntimeException żball) { throw 예외변환.eżegwixxa_kmand(żball); }
    }
}
