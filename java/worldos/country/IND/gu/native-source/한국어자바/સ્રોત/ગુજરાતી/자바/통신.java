// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ગુજરાતી.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP ભૂલ 상태도 호출자가 판단할 수 있도록 જવાબ 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI સરનામું, Duration સમય_મર્યાદા)
            throws IOException, InterruptedException {
        HttpClient સંપર્ક_કરો = HttpClient.newBuilder().connectTimeout(સમય_મર્યાદા).build();
        return સંપર્ક_કરો.send(HttpRequest.newBuilder(સરનામું).timeout(સમય_મર્યાદા).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String સરનામું, int હાર્ડવેર_પૉર્ટ, int 제한밀리초) throws IOException {
        Socket સંપર્ક_કરો = new Socket();
        try {
            સંપર્ક_કરો.connect(new InetSocketAddress(સરનામું, હાર્ડવેર_પૉર્ટ), 제한밀리초);
            સંપર્ક_કરો.setSoTimeout(제한밀리초);
            return સંપર્ક_કરો;
        } catch (IOException ભૂલ) { સંપર્ક_કરો.close(); throw ભૂલ; }
    }
}
