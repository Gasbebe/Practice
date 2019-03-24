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

