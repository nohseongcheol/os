// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಕನ್ನಡ.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP ದೋಷ 상태도 호출자가 판단할 수 있도록 ಪ್ರತ್ಯುತ್ತರ 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI ಇಮೇಲ್, Duration ಸಮಯ_ಮಿತಿ)
            throws IOException, InterruptedException {
        HttpClient ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು = HttpClient.newBuilder().connectTimeout(ಸಮಯ_ಮಿತಿ).build();
        return ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.send(HttpRequest.newBuilder(ಇಮೇಲ್).timeout(ಸಮಯ_ಮಿತಿ).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String ಇಮೇಲ್, int 포트, int 제한밀리초) throws IOException {
        Socket ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು = new Socket();
        try {
            ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.connect(new InetSocketAddress(ಇಮೇಲ್, 포트), 제한밀리초);
            ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.setSoTimeout(제한밀리초);
            return ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು;
        } catch (IOException ದೋಷ) { ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.close(); throw ದೋಷ; }
    }
}
