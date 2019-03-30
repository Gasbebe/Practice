# Tree

#### full binary tree 

모든 노드가 채워져있다.  높이가  n, 2^n- 1개의 노드를 가진다

#### complete binary tree

부모 : n , 왼쪽 자식 노드: 2n,  오른쪽 자식 노드 : 2n + 1 (일반 적인 이진트리에는 이 규칙이 적용 되지 않음 )

---

#### Linked Structure

left,data, p, right

계층적인 구조를 표현

1. 조직도
2. 디렉토리와 서브디렉토리 구조
3. 가계도

순회

1. 중순위(inorder)
2. 선순위(preorder)
3. 후순위(postorder)
4. 레벨오더(level-order)

## Huffman Code

이진트리 응용의 예

인코딩할때 주로사용하는 알고리즘



# Red-Black Tree

binart search tree 기본 형태를 유지 하면서 이 트리의 벨런스가 무너지지 않도록 유지시켜준다

삽입 삭제, 할때 극단적으로 벨런스가 무너지지 않도록 알고리즘을 적용한  Red-Black Tree

`이진탐색트리의 일종`,  `균형잡힌 트리 : 높이가 O(log2n)` 

각 노드는 하나의 키, 왼쪽자식, 오른쪽 자식, 그리고 부모노드 주소를 저장

자식노드가 존재하지 않을 경우 NIL노드라고 부르는 특수한 노드가 있다고 가정

따라서 모든 리프노드는 NIL노드

루트의 부모도 NIL노드라고 가정

노드들은 내부노드와 NIL노드로 분류 

#### 다음조건을 만족하는 Binary Tree

1. 각 노드는 `red`  or `black`
2. 루트노드는 `black`
3. 모든 리프노드는(즉, NIL노드)는 `black` 이고
4. `red` 노드의 자식노드들은 전부  `black` 이고 (즉 `red` 노드들은 연속되어 등장하지 않고)
5.  모든 노드에 대해서 그 노드로부터 자손인 리프노드에 이르는 모든 경로에는 동일한 개수의 `black` 노드가 존재한다.

BST(binary search tree)

```c#
// 이진검색트리 클래스
public class BST<T>
{
    private BinaryTreeNode<T> root = null;
    private Comparer<T> comparer = Comparer<T>.Default;

    public void Insert(T val)
    {
        BinaryTreeNode<T> node = root;
        if (node == null)
        {
            root = new BinaryTreeNode<T>(val);
            return;                
        }

        while(node != null)
        {
            int result = comparer.Compare(node.Data, val);
            if (result == 0)
            {
                return; 
            }
            else if (result > 0)
            {
                if (node.Left == null)
                {
                    node.Left = new BinaryTreeNode<T>(val);
                    return;                        
                }
                node = node.Left;
            }
            else
            {
                if (node.Right == null)
                {
                    node.Right = new BinaryTreeNode<T>(val);
                    return;                        
                }
                node = node.Right;
            }
        }
    }        

    public void PreOrderTraversal()
    {
        PreOrderRecursive(root);
    }
            
    private void PreOrderRecursive(BinaryTreeNode<T> node)
    {
        if (node == null) return;
        Console.WriteLine(node.Data);
        PreOrderRecursive(node.Left);
        PreOrderRecursive(node.Right);
    }
}

// 이진검색트리 테스트
internal class Program
{
    private static void Main(string[] args)
    {
        BST<int> bst = new BST<int>();
        bst.Insert(4);
        bst.Insert(2);
        bst.Insert(6);
        bst.Insert(1);
        bst.Insert(7);

        bst.PreOrderTraversal();
    }
}

```

그건 단순히 메모리의 총량이 많아서 생긴 문제가 아니라, 재귀 호출 스택과 지역 변수가 스택 영역을 사용하기 때문에 그런 것입니다. 스택 영역은 전체 메모리 한도와는 별개로 프로그래마다 배정이 되어 있는데, 이는 윈도우즈에서는 기본적으로 1MB, 리눅스에서는 8MB로 설정되어 있습니다. 하지만 이는 빌드 시에 설정을 따로 해줄 수 있고, BOJ에서는 제가 알기로는 64MB 정도까지 스택을 허용하기 때문에 문제가 되지 않습니다.

# algorithm

```c++
#include <iostream>
#include <algorithm>
#include <stack>

namespace std;
bool compare(int a, int b){
    return a > b;
}
class bts{
    public:
    	bts* leftNode;
    	bts* rightNode;
    private:
    	bts();
    	~bts();
    
}
int main(){
    int a[10] = {9,4,2,4,5,6,67,3,66,4};
    //오름차순
    sort(a, a + 10);
    //내림차순
    sort(a, a + 10, compare);
	return 0;    
}
```



```c++
class Student{
    public: 
    	string name;
    	int score;
    Student(string name, int score){
        this->name = name;
        this->score = score;
    }
    
    bool operator <(Student &student){
        return this->score < student.score;
    }
};

int main(void){
    Student student[] = {
      	Student("1", 90),
        Student("2", 44),
        Student("3", 77),
        Student("4", 88),
        Student("5", 33),
    };
    sort(student, student + 5);
}


```



```c++
#include<iostream>
#include<vector>
#include<algorithm>

using namespace std;

bool compare(pair<string, pair<int, int>> a,
             pair<string, pair<int, int>> b){
    if(a.second.first == b.second.first){
        return a.second.second > b.second.second;
    }else{
        return a.second.first > b.second.first;
    }
}

int main(void){
	vector<pair<int, string>> v;
    v.push_back(pair<int, string>(90, "1"));
    v.push_back(pair<int, string>(77, "1"));
    v.push_back(pair<int, string>(88, "1"));
    v.push_back(pair<int, string>(55, "1"));
    v.push_back(pair<int, string>(66, "1"));
    
    sort(v.begin(), v.end);
    for(int i = 0;  i< v.size(); i++){
        cout << v[i].second << ' '; 
    }
    
    vector <pair<string, pair<int, int> > > v2;
    v2.push_back(pair<string, pair<int, int > >("11", 99, 99));
    v2.push_back(pair<string, pair<int, int > >("11", 77, 55));
    v2.push_back(pair<string, pair<int, int > >("11", 99, 88));
    v2.push_back(pair<string, pair<int, int > >("11", 11, 922));
    v2.push_back(pair<string, pair<int, int > >("11", 33, 99));
}
```



# Counting Sort

범위조건이 있는 경우에 한해서 괴장히 빠른 정렬 크기를 기준으로 갯수만 세주면 되기 때문에

```c++
int main(void){
	int temp
	int count[5];
    return 0;
    
    for(int i = 0;  i < 5;  i++){
        count[i] = 0;
    }
    
    for(int i = 0; i < 30; i++){
        count[array[i] - 1]++;
    }
    for(int i= 0; i < 5; i++){
        if(count[i] != 0){
            for(int j = 0; j < count[i]; j++){
                printf("%d", i + 1);
            }
        }
    }
}
```



# Topology sort

##### 위상 정렬 `Topology sort`  여러 가지 조건이 결합된 그래프 상에서 경로를 찾기 위한 알고리즘으로 큐  `Queue`를 사용하는 위상 정렬

```c++
#include <iostream>
#include <queue>
#include <vector>
#define MAX 10

using namespace std;

int n, inDefree[MAX];
vector<int> a[MAX];

int main(void){
    int result[MAX];
    queue<int> q;
    for(int i=0 i <= n; i++){
        if(inDegree[i] == 0) q.push(i);
    }
    
    for(int i=0; i<= n; i++){
        if(q.empty()){
            return;
        }
        int x = q.front();
        q.pop();
        result[i] = x;
    }
    return 0;
}
```

