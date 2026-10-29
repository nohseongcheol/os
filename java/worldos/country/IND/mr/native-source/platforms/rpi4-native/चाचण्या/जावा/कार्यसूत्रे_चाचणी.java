// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class काउंटर_मूल्य {
    int संख्या;
    synchronized void जोडा_मूल्ये() { int पुढील_मूल्य = संख्या; Thread.yield(); संख्या = पुढील_मूल्य + 1; }
}
class कार्य_क्रिया implements Runnable {
    काउंटर_मूल्य काउंटर_संदर्भ; कार्य_क्रिया(काउंटर_मूल्य काउंटर_संदर्भ) { this.काउंटर_संदर्भ = काउंटर_संदर्भ; }
    public void run() { for (int i = 0; i < 20; i++) काउंटर_संदर्भ.जोडा_मूल्ये(); }
}
class कार्यसूत्र_मूल्य_5b72a632 extends Thread { public void run() { synchronized (कार्यसूत्रे_चाचणी.कुलूप_मूल्य) { कार्यसूत्रे_चाचणी.आहे_पूर्ण = 1; } } }
public class कार्यसूत्रे_चाचणी {
    static Object कुलूप_मूल्य = new Object(); static int आहे_पूर्ण;
    public static void main(String[] a) throws Exception {
        काउंटर_मूल्य काउंटर_संदर्भ = new काउंटर_मूल्य(); Thread एक_मूल्य = new Thread(new कार्य_क्रिया(काउंटर_संदर्भ)); Thread दोन_मूल्य = new Thread(new कार्य_क्रिया(काउंटर_संदर्भ));
        एक_मूल्य.start(); दोन_मूल्य.start(); एक_मूल्य.join(); दोन_मूल्य.join(); System.out.println(काउंटर_संदर्भ.संख्या); System.out.println(एक_मूल्य.isAlive());
        कार्यसूत्र_मूल्य_5b72a632 तिसरे_आयटम = new कार्यसूत्र_मूल्य_5b72a632(); तिसरे_आयटम.start(); तिसरे_आयटम.join(); System.out.println(आहे_पूर्ण);
        try { एक_मूल्य.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 अस्वीकृत_करा_मूल्य"); }
        System.out.println("कार्यसूत्र_मूल्य_5b72a632 आहे_पूर्ण");
    }
}
