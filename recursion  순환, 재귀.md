recursion : 순환, 재귀 알고리즘 연습

자기 자신을 호출하는 함수

```c++
void func(){
    func();
}
```

 쵀대공약수

```c++
static void double gcd(int m, int n){
    if(m<n){
        int temp =m; m =n;  n = temp;
    }
    
    if(m%n == 0){
        return n;
    }
    else{
        return gcd(n, m%n);
    }
}


static int gcd(int p, int q){
    if(q==0)
        return p;
    else
        return gcd(q, p%q);
}
```



문자열 뒤집어서 프린트

```c++
static void printreverse(string arg){
    if(arg.length == 0)
        return;
    else
        printreverse(str.substring(1));
    	cout << art.at(0);
}
```



2진수 변환하여 출력

```c++
void printBinary(int n){
    if(n < 2)      //if(n < 0)
        cout << n;    
    else{
        printBinary(n/2);
        cout << n%2;
    }
}
```



배열의 합 구하기

```c++
public static int sum(int n, int [] data){
    if(n <= 0)
        return 0;
    else
        return sum(n-1, data) + data[n-1];
}
```



모든 순환함수는 반복문(iteration)으로 변경 가능

그 역도 성립함 즉 모든 반복문은 recursion으로 표현 가능

순환함수는 복잡한 알고리즘을 단순하고 알기쉽게 표현하는 것을 가능하게 함

하지만 함수 호출에 따른 오버해드가 있음 (매개변수 전달, 액티베이션 프레임 생성 등)





Designing Recursion 순환 알고리즘의 설계

1. 적어도 하나의 base case  즉 순환되지 않고 종료되는  case가 있어야한다
2. 모든 case는 결국 base case로 수렴해야 함



암시적(implicit), 명시적(explicit)

순차탐색

```c++
int search(int [] data, int n, int target){
    for(int i = 0; i<n; i++)
        if(data[i] == target)
            return i;
    return -1;
}

```







# Sort

selection sort, merge sort, quick sort

분할정복법

분할 : 해결하고자 하는 문제를 작은 크기의 동일한 문제들로 분할

정복 : 각각의 작은 문제를 순환적으로 해결

합병 : 작은 문제의 해를 합하여 원래 문제에 대한 해를 구함

```c++
char word [] = {A,L,G,O,R,I,T,H,M,S};

```

T(n) = 0  if n = 1

​       T([n/2]) + T([n/2]) + n 

벤다이어 그램으로 논리 만들기

https://www.alanzucconi.com/

http://halisavakis.com/category/blog-posts/

