# practice
그냥 잡다한것, 모르는 것, 정리할 것
---

# 일지

- 버그는 없어진게 아니라 숨겨진 경우도 있다 (무조건 고쳤다고 생각하지 말기)
- 필터 : 골라서 가져온다는 의미가 크다
- draft는 문서에서 초안이라는 의미를 가진다
- https://wiki.kldp.org/HOWTO/html/Adv-Bash-Scr-HOWTO/ Bash Script 
- definition라는 단어가 나오면 다 구현이 되어있는 상태를 말한다
- 선언과 정의를 구분(c/c++)
- c++에서 초기화를 하는데 `long i = 13123123123`,   `long i2 = {12312321}`  첫번째는 플랫폼 아키택쳐에 따란 비트가 버려질수 있다. 두번째는 비트가 버려질때 오류를 발생시킨다. 안전하게 하려면 중괄호 초기화를 써야한다
- web RTC
- tracing 서로 주고 받는다라는 의미로도 쓰인다
- https://storyprogramming.com/category/unity/
- 마둠파 https://blog.naver.com/mnpshino
- https://blog.naver.com/plasticbag0
- App, Process, Thread
- buffer
- RestAPI
- 인터럽트
- 문자 데이터를 다룰때 용도에 따라 화이트스페이스, \n \r  다 제거하기
- TCU : Transmission Cotrol Unit
- RTE : Runtime Environment
- std::bind 파라미터의 받는 순서를 변경 할수도 있다
- void*, function pointer? = generic pointer
- 동적 라이브러리, 정적 라이브러리(모듈) -fPIC?
- 상속은 is a 관계에서 많이 쓰인다
- 이미지, 빌드
- https://ko.wikipedia.org/wiki/%EB%A3%A8%ED%94%84%EB%B0%B1 네트워크 lo
- 이스케이프 문자 /0x0b /0x5b
- cpp에서 형변환 할때 (const void)* const (void*) 괄호나 위치 때문에 문제가 생길수 있다 조심하자 
- vector.data로 포인트를 받아 포인터형식으로 데이터를 추가하여도 vector크기는 증가한게 아니라 resize로 다시 잡아주거나 push.back을 해줘야한다
- https://d2.naver.com/helloworld/267396
- https://jacking75.github.io/
- LLP64
- https://m.blog.naver.com/PostView.nhn?blogId=tipsware&logNo=221065382244&proxyReferer=https%3A%2F%2Fwww.google.com%2F
- https://riptutorial.com/csharp/example/304/chaining-methods
- so파일에 적히는 함수명은 c, cpp다르게 적힌다 cpp는 override가 있기 때문이다
- 네임맹글링 = 네임 
- https://m.blog.naver.com/PostView.nhn?blogId=tipsware&logNo=221065382244&proxyReferer=https%3A%2F%2Fwww.google.com%2F
- c는 컴파일할떄 헤더파일을 포함 안해도 선언한 함수이름의 정의를 알아서 찾아 링크 해준다
- 디버그가 힘든 환경이 존재 할떄는 로그를 잘찍어야한다
- 오류, 원인을 찾기 위해 분석을 해라
- 세마포어 멀티프로그래밍 환경에서 공유 자원에 대한 접근을 제한하는 방법으로 사용된다
- 형변환 신경쓸것 몇 바이트인지 잘 생각 
- 핸들이란 리소스의 주소를 정수로 저장한것
- 푸쉬서버
- 메소드 뎁스를 설정하여 뎁스따라 함수 부르는 갯수를 설정 할 수 있다. depth++ depth--
- 압축을 이용하여 속도를 증가 
- https://en.wikipedia.org/wiki/ANSI_escape_code
- 데이터타입을 비트나 바이트단위로 자주 생각하자 int64도 캐스트만 잘하면 모든 데이터를 담을 수 있다
- internal이라는 키워드에 변수로 이름을 정할때 플랫폼경우에는 이 키워드가 붙어있는 변수를 몰라두 되고 건드리지 말라는 뜻으로 많이 쓰인다
- https://halisavakis.com/my-take-on-shaders-spherical-mask-dissolve/_
- mbcs
- noexcept(false) : 쓰는 함수의 define봐서 throw가 있을때, 적절하게 예외처리를 할 수 없을때
- noexcept : throw가 없을때 try catch에서 처리 , 적절하게 예외처리를 할 수 있을때
- std::move(m)를 사용했는데 그 다음줄에서 m을 사용하여 앱이 이상동작함, 신경쓸것
- https://en.m.wikipedia.org/wiki/Projectile_motion
- 데이터를 쓰고 있을때 그 데이터를 읽는것은 상관이 없다(lock, unlock 안해두 됨)
- 이벤트 콜백함수에 여러개에 함수가 등록 되어있을때 e.handle = true로 해주면 이 이벤트 콜백 함수는 처리되었다는 뜻이고 등록되어 있는 나머지 함수들은 호출하지 않는다(wpf)
- https://social.technet.microsoft.com/wiki/contents/articles/12347.wpf-howto-add-a-debugoutput-console-to-your-application.aspx cosole hook(wpf)
- 편법 보다는 원칙대로 기능을 구현해라, 나중에 꼬일수도 있다
- oop soild원칙중 단일책임 원칙 계속 생각하면서 구현하기
- https://www.youtube.com/embed/32OaU7DXTE0?autoplay=1&modestbranding=1&rel=0&mute=0

