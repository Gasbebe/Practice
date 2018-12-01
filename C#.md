[TOC]



# 1. 닷넷 프레임워크

닷넷 프레임워크는 2002년 마소에서 발표한 응용프로그램 개발 환경으로서 프로세스 가상머신

닷넷 프레임워크를 기반으로 만들어진 응용 프로그램은 반드시 닷넷 프레임워크가 미리 설치된 환경에서만 실행이된다



# 2. CLR(Common Language Runtime)

닷넷 프레임워크를 설치하면 가상머신 역활을 하는 CLR 구성요소가 실행될 수 있는 환경이 윈도우 운영체제에 마련된다.

CLR은 프로세스가 실행되면 메모리에 함께 적재돼 실행된다.

내부적으로는 CLR 구성요소가 로드돼 실행돼고 그 CLR이 EXE/DLL에 함께 저장돼 있는 닷넷 코드를 실행한다.

C# 입장에서 C# 컴파일러는  소스코드를 기계어가 아닌 중간언어 IL(Intermediate Language)이라고 하는 중간 언어로 EXE/DLL 파일 내부에 생성한다 또한 프로그램이 시작하자마자 CLR을 로드하는 코드를 자동으로 EXE 파일 내부에 추가한다.



==============================================================================

차근차근 정리할것

==============================================================================

# System.Array

소스코드에 정의되는 배열은 모두 System.Array 타입을 조상으로 둔다.

| 멤버     | 타입              | 설명                                      |
| -------- | ----------------- | ----------------------------------------- |
| Rank     | 인스턴스 프로퍼티 | 배열의 인스턴스의 차원수(dimenstion) 반환 |
| Length   | 인스턴스 프로퍼티 | 배열의 인스턴스의 요소수(element) 반환    |
| Sort     | 정적 메서드       | 배열 요소를 값의 순서대로 정렬한다        |
| GetValue | 인스턴스 메서드   | 지정된 인덱스의 배열의 요소 값을 반환한다 |
| Copy     | 정적 메서드       | 배열의 내용을 다른 배열에 복사한다        |



```c#
class Program
{
    static void Main(string[] args)
    {
    	bool[,] bArray = new bool[,]{{true, false},{true, false}};
        int[] iArray = new int[] {5,4,3,2,1};
        
        Array.Sort(iArray); //Sort 정적 메서드
        
        int[] copyArray = new int[iArray.Length];
        Array.Copy(iArray, copyArray, iArray.Length); //Copy 정적 메서드
        
        Console.WriteLine("배열의 차워 수 : " + bArray.Rank);
        Console.WriteLine("배열의 요소 수 : " + bArray.Length);
    }
}
```











