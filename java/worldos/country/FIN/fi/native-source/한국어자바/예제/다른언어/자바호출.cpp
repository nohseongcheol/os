// JNI의 Luokka_ARVO·menetelmä_ARVO 이름은 문자열로 전달하므로 suomi API도 호출할 numero 있다.
#include <jni.h>
#include <iostream>
#include <string>
#include <thread>
#include <vector>

static int call_java(const char *jar) {
    std::string classpath = std::string("-Djava.class.path=") + jar;
    JavaVMOption option{};
    option.optionString = &classpath[0];
    JavaVMInitArgs args{};
    args.version = JNI_VERSION_1_8;
    args.nOptions = 1;
    args.options = &option;
    JavaVM *vm = nullptr;
    JNIEnv *env = nullptr;
    jint created = JNI_CreateJavaVM(&vm, reinterpret_cast<void **>(&env), &args);
    if (created != JNI_OK) {
        std::cerr << "JVM Suorita_2 virhe_ARVO: " << created << '\n';
        return 1;
    }
    int result = 1;
    do {
        jclass type = env->FindClass("suomi/자바/문자");
        if (!type || env->ExceptionCheck()) break;
        jmethodID method = env->GetStaticMethodID(type, "koodipiste_LASKE", "(Ljava/lang/String;)I");
        if (!method || env->ExceptionCheck()) break;
        // JNI NewStringUTF는 modified UTF-8을 받는다. 이모지를 포함하는
        // 일반 문자열은 여기처럼 UTF-16 단위로 NewString에 전달한다.
        std::u16string text = u"한글 😀";
        std::vector<jchar> units(text.begin(), text.end());
        jstring input = env->NewString(units.data(), static_cast<jsize>(units.size()));
        if (!input || env->ExceptionCheck()) break;
        jint count = env->CallStaticIntMethod(type, method, input);
        if (env->ExceptionCheck()) break;
        std::cout << "C++ → suomi.자바.문자.koodipiste_LASKE: " << count << '\n';
        result = (count == 4) ? 0 : 1;
    } while (false);
    if (env->ExceptionCheck()) {
        env->ExceptionDescribe();
        env->ExceptionClear();
    }
    if (vm->DestroyJavaVM() != JNI_OK) result = 1;
    return result;
}

int main(int argc, char **argv) {
    if (argc != 2) {
        std::cerr << "사용법: 자바호출 /절대경로/한국어자바.jar\n";
        return 2;
    }
    int result = 1;
    std::thread worker([&] { result = call_java(argv[1]); });
    worker.join();
    return result;
}
