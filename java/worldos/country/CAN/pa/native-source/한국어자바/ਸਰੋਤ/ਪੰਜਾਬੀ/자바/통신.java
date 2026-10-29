// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਪੰਜਾਬੀ.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP ਗਲਤੀ 상태도 호출자가 판단할 수 있도록 ਜਵਾਬ_ਦਿਓ 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI ਪਤਾ, Duration ਸਮਾਂ_ਸੀਮਾ)
            throws IOException, InterruptedException {
        HttpClient ਕੁਨੈਕਸ਼ਨ_ਕਰੋ = HttpClient.newBuilder().connectTimeout(ਸਮਾਂ_ਸੀਮਾ).build();
        return ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.send(HttpRequest.newBuilder(ਪਤਾ).timeout(ਸਮਾਂ_ਸੀਮਾ).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String ਪਤਾ, int 포트, int 제한밀리초) throws IOException {
        Socket ਕੁਨੈਕਸ਼ਨ_ਕਰੋ = new Socket();
        try {
            ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.connect(new InetSocketAddress(ਪਤਾ, 포트), 제한밀리초);
            ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.setSoTimeout(제한밀리초);
            return ਕੁਨੈਕਸ਼ਨ_ਕਰੋ;
        } catch (IOException ਗਲਤੀ) { ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.close(); throw ਗਲਤੀ; }
    }
}
