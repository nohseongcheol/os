// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package മലേഷ്യ.JMysOS.സംഭരണം_മൊബൈൽ;

import java.util.Arrays;

/** ATA 28비트 ആജ്ഞ 계층과 같은 512바이트 논리 വിഭാഗം_മൂല്യം 장치다. */
public final class 고급기술결합장치 {
    public static final int വിഭാഗം_വലുപ്പം_ക്രമീകരിക്കുക = 512;
    private final byte[] ഡാറ്റാ;
    private final boolean വായന_മാത്രം_മൂല്യം;

    public 고급기술결합장치(int 구역수, boolean വായന_മാത്രം_മൂല്യം) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("വിഭാഗം_മൂല്യം 수가 올바르지 않습니다.");
        }
        ഡാറ്റാ = new byte[Math.multiplyExact(구역수, വിഭാഗം_വലുപ്പം_ക്രമീകരിക്കുക)];
        this.വായന_മാത്രം_മൂല്യം = വായന_മാത്രം_മൂല്യം;
    }

    public int 구역수() {
        return ഡാറ്റാ.length / വിഭാഗം_വലുപ്പം_ക്രമീകരിക്കുക;
    }

    public void വായന(int വിഭാഗം_സൂചിക, byte[] 받을곳) {
        범위확인(വിഭാഗം_സൂചിക, 받을곳);
        System.arraycopy(ഡാറ്റാ, വിഭാഗം_സൂചിക * വിഭാഗം_വലുപ്പം_ക്രമീകരിക്കുക, 받을곳, 0, വിഭാഗം_വലുപ്പം_ക്രമീകരിക്കുക);
    }

    public void എഴുത്തു്(int വിഭാഗം_സൂചിക, byte[] 쓸자료) {
        if (വായന_മാത്രം_മൂല്യം) {
            throw new IllegalStateException("വായന 전용 장치입니다.");
        }
        범위확인(വിഭാഗം_സൂചിക, 쓸자료);
        System.arraycopy(쓸자료, 0, ഡാറ്റാ, വിഭാഗം_സൂചിക * വിഭാഗം_വലുപ്പം_ക്രമീകരിക്കുക, വിഭാഗം_വലുപ്പം_ക്രമീകരിക്കുക);
    }

    public void മായ്ക്കുക_എന്_ട്രി() {
        if (വായന_മാത്രം_മൂല്യം) {
            throw new IllegalStateException("വായന 전용 장치입니다.");
        }
        Arrays.fill(ഡാറ്റാ, (byte) 0);
    }

    private void 범위확인(int വിഭാഗം_സൂചിക, byte[] 임시공간) {
        if (വിഭാഗം_സൂചിക < 0 || വിഭാഗം_സൂചിക >= 구역수() || 임시공간.length < വിഭാഗം_വലുപ്പം_ക്രമീകരിക്കുക) {
            throw new IllegalArgumentException("ATA വിഭാഗം_മൂല്യം 범위가 올바르지 않습니다.");
        }
    }
}

