Command Pattern : 명령을 객체화

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

migration..



```c#
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

public class LogManager
{
    private string mPath;
    
    public  LogManger(string path)
    {
        mPath = path;
        _SetLogPath();
    }
    
    public LogManger() : this(System.IO.Path.Combine(Application.Root, "Log");)
    {}
    
    private void _SetLogPath()
    {
    	if(!System.IO.Directory.Exists(mPath))
            System.IO.Directory.CreateDirectory(mPath));
        string logFile = DataTime.Now.ToString("yyyyMMdd") + ".txt";
        mPath = Path.Combine(mPath, logFile);           
    }
    
    public void Write(string data)
    {
        try{
        	using(StreamWriter writer = new StreamWriter(mPath, true))
        	{
            	writer.Write(data);
        	}
        }
        catch(Exception e){
            
        }
    }
    
    public void WriteLine(string data)
    {
        using(StreamWriter writer = new StreamWriter(mPath, true))
        {
            writer.WriteLine(DataTime.Now.ToString("yyyyMMdd HH:mm:ss\t")+ data);
        }
    }
}
                            
class void Main
{
	static void Main(string [] args)
    {
        LogManager log = new LogManger();
        log.WirteLine("Begin Processing...");
        
        for(int i = 0;  i < 10; i++)
        {
            log.WriteLine("Processing " + i);
            System.Threading.Sleep(500);
            log.WriteLine("Dond " + i );
        }
        
        log.WriteLine("End Processing");
    }
}
                             
```

