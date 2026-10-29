// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ଭାରତ.JIndOS.체계호출;

public final class 체계정보 {
    private final String ସିଷ୍ଟମ_ନାମ;
    private final String ସଂଯୋଗ_ବିନ୍ଦୁ_ନାମ;
    private final String 배포판;
    private final String ସଂସ୍କରଣ_ମୂଲ୍ୟ;
    private final String ମେସିନ୍;

    public 체계정보(String ସିଷ୍ଟମ_ନାମ, String ସଂଯୋଗ_ବିନ୍ଦୁ_ନାମ, String 배포판, String ସଂସ୍କରଣ_ମୂଲ୍ୟ, String ମେସିନ୍) {
        this.ସିଷ୍ଟମ_ନାମ = ସିଷ୍ଟମ_ନାମ;
        this.ସଂଯୋଗ_ବିନ୍ଦୁ_ନାମ = ସଂଯୋଗ_ବିନ୍ଦୁ_ନାମ;
        this.배포판 = 배포판;
        this.ସଂସ୍କରଣ_ମୂଲ୍ୟ = ସଂସ୍କରଣ_ମୂଲ୍ୟ;
        this.ମେସିନ୍ = ମେସିନ୍;
    }

    public String ସିଷ୍ଟମ_ନାମ() { return ସିଷ୍ଟମ_ନାମ; }
    public String ସଂଯୋଗ_ବିନ୍ଦୁ_ନାମ() { return ସଂଯୋଗ_ବିନ୍ଦୁ_ନାମ; }
    public String 배포판() { return 배포판; }
    public String ସଂସ୍କରଣ_ମୂଲ୍ୟ() { return ସଂସ୍କରଣ_ମୂଲ୍ୟ; }
    public String ମେସିନ୍() { return ମେସିନ୍; }
}
