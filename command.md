```c#
public class MyCommand
{
    virtual void excute();
}

public class ConcreteCommand : MyCommand
{
	override void excute(){
		Console.WriteLine("Command A");
	}
}

public class Receiver
{
	ConcereteCommand commandA = new ConcreteCommand();    
    public void action(ConcreteCommand command)
    {
        command.excute();
    }
}
```



Builder Pattern : 인스턴스 생성과정을 단순화

```c#
public class BluePrint
{
    virtual public void Test();
    virtual public void SetCPU();
    virtual public void SetRam();
    virtual public void SetStorage()
}

public class ComputerBluePrint : BluePrint
{
	//init
    void ComputerBluePrint()
    {
    	Test();
    	SetCpu();
    	SetRam();
    	SetStorage();
    }
	override public void Test(){}
	override public void SetCpu(){}
	override public void SetRam(){}
	override public void SetStorage(){}
}

public class MyMain{
	public void main(string[] args)
	{
		new ComputerBluePrint computeBluePrint = new ComputeBluePrint();
	}
}
```



Composite Pattern

```c#
public class Component
{
	public Component [] component;    
    public void operation(){}
    public void add(Component component){}
    public void remove(Component component){}
    public void getChild(int number){}
}

public class MusicComponent : Component
{
	
}

public class PhysicsComponent : Component
{

}
```



Facade Pattern  : 단순한 접근하기 위한 패턴

```c#
namespace MyPattern
{
	class Facade
	{
   	 	private MySystem mySystem1;
        private MySystem mySystem2;
        private MySystem mySystem3;
        
        public Facade()
        {
        	mySystem1 = new MySystem();    
            mySystem2 = new MySystem();
            mySystem3 = new MySystem();
        }
        
        public void process()
        {
            mySystem1.Process;
            mySystem2.Process;
            mySystem3.Process;
        }
	}
}

class MySystme
{
    public void Process(){}
}

class MyMain
{
    pblic void main(string [] args)
    {
        Facade facade = new Facade();
        facade.Process();
    }
}
```

