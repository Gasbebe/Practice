[TOC]



# 1. 닷넷 프레임워크

닷넷 프레임워크는 2002년 마소에서 발표한 응용프로그램 개발 환경으로서 프로세스 가상머신

닷넷 프레임워크를 기반으로 만들어진 응용 프로그램은 반드시 닷넷 프레임워크가 미리 설치된 환경에서만 실행이된다



# 2. CLR(Common Language Runtime)

닷넷 프레임워크를 설치하면 가상머신 역활을 하는 CLR 구성요소가 실행될 수 있는 환경이 윈도우 운영체제에 마련된다.

CLR은 프로세스가 실행되면 메모리에 함께 적재돼 실행된다.

내부적으로는 CLR 구성요소가 로드돼 실행돼고 그 CLR이 EXE/DLL에 함께 저장돼 있는 닷넷 코드를 실행한다.

C# 입장에서 C# 컴파일러는  소스코드를 기계어가 아닌 중간언어 IL(Intermediate Language)이라고 하는 중간 언어로 EXE/DLL 파일 내부에 생성한다 또한 프로그램이 시작하자마자 CLR을 로드하는 코드를 자동으로 EXE 파일 내부에 추가한다.



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



```c#
using System;

namespace Test
{
    class Program
    {
         static void Main(string[] args)
         {
			string read = Console.ReadLine();//함수명 그대로 한줄 읽기 \n 문자가 나올때까지의 문자를 읽는다.

         }
    }
}
```



#### scope

```c#
using System;

namespace Test
{
    class Program
    {
         static void Main(string[] args)
         {
		
		      //괄호를 스코프를 지정할수 있다 scope1
             {
                 int number = 0;
             }
             //scope2
             {
                 int number = 1;
             }
         }
    }
}
```



#### ref

```c#
using System;

namespace Test
{
    class Program
    {
         static void Main(string[] args)
         {
			double number = 5f;
            Square(ref number);
         }
    }
}
```



---

#### 너무 많이 함수 만들때 문제점

함수가 일단 있다는 건 누구든지 그 함수를 여러 곳에서 사용할 수 있다는 것

`버그나 기능 확장을 위해 그 함수를 변경`하려면 다른 사람들이 잘못된 가정을 하진 않았는지 확인해야 함

#### 베스트 프랙티스 : 함수는 언제 만들까?

- 현재 존재하는 혹은 향후에 발생 가능성이 높은 코드 중복을 피하고자 할 때
- 코드 중복은 좋지 않음 -> 다음 사람이 중복 코드에 있는 버그를 고칠때, 모든 코드를 수정할 것이라는 보장이 없기 때문

#### 베스트 프랙티스 : 함수 대신 중괄호

- 함수가 길어지면 동일한 이름의 지역 변수가 생기는 경우가 있음-> 중괄호를 사용하여 범위를 분리시키면 문제 해결 가능!(scope)

#### 베스트 프랙티스 : 함수 대신 #region와 #endregion

- C#전용
- 비주얼 스튜디오에서 코드를 접거나 펼 수 있게 해줌

#### 결론

함수는 코드 중복을 피하기 위해서 만드세요

만약 처음부터 함수를 만들기 어렵다면 함수 없이 코드를 모두 다 작성하고, 그 다음에 함수로 분리하세요.



#### 열거형(enum)

---

```c#
using System;

namespace Test
{
    class Program
    {
         static void Main(string[] args)
         {
			public enum EState
            {
                Idle = 1,
                Atk = 1 << 1,
                Die = 1 << 2
            }
             EState state = EState.Idle;
             
             //enum꼼수 - 배열 만들기
             enum EDirection
             {
                 North,
                 South,
                 East,
                 West,
                 Max,
             }
             //어느 함수
             string[] directions = new string[(int)EDirection.Max];
         }
    }
}
```

