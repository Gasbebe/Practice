bst(binary search tree)

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

