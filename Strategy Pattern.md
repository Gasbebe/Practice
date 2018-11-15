Strategy pattern : 전략 패턴

인터페이스 : 선언과 구현 분리 통로

접근점을 통해 알고리즘을 교환가능하도록 하는 패턴

```c#
public class Stragy : MonoBehaviour
{

    public IStrategyPattern m_pattern = null;
	
	//delegate
    public void Attactk()
    {
        if (m_pattern == null)
        {
            Debug.Log("무기가 없습니다");
            return;
        }
        m_pattern.ExcuteFunc();
    }

    public void SetExcuteFunc(IStrategyPattern pattern){
        m_pattern = pattern;
    }


    private void Start()
    {
        Attactk();
        SetExcuteFunc(new ConcreteStrategyA());
        Attactk();
        SetExcuteFunc(new ConcreteStrategyB());
        Attactk();
    }
}


public interface IStrategyPattern
{
    void ExcuteFunc();
}

public class ConcreteStrategyA : IStrategyPattern
{
    public void ExcuteFunc()
    {
        Debug.Log("AA이다");
    }
}

public class ConcreteStrategyB : IStrategyPattern
{
    public void ExcuteFunc()
    {
        Debug.Log("BB이다");
    }
}


```

