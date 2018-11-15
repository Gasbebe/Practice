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





Adapter Pattern

사전의미 기계 기구등을 다목적으로 사용하기 위한 부가 기구

adapter pattern은 관계가 없는 인터페이스들이 같이 일할 수 있도록 도와주는 디자인 패턴이다. 이 두 인터페이스를 이어주는 인터페이스를 adapter라 부른다. 아래 예제를 보면서 이해해보도록하자.   

```c#
public class Volt {
    private int volts;

    public Volt(int v) {
        this.volts = v;
    }

    public int getVolts() {
        return this.volts;
    }

    public void setVolts(int volts) {
        this.volts = volts;
    }
}


public class Socket {
    public Volt getVolt() {
        return new Volt(120);
    }
}

public interface SocketAdapter {
    public Volt get120Volt();
    public Volt get12Volt();
    public Volt get3Volt();
}



public class SocketObjectAdapterImpl : SocketAdapter {

    private Socket sock = new Socket();

    public Volt get120Volt() {
        return sock.getVolt();
    }

    public Volt get12Volt() {
        Volt v = sock.getVolt();
        return convertVolt(v, 10);
    }

    public Volt get3Volt() {
        Volt v = sock.getVolt();
        return convertVolt(v, 40);
    }

    private Volt convertVolt(Volt v, int i) {
        return new Volt(v.getVolts()/i);
    }

}
```

