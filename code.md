```c++
#include <iostream>

class Accumulator
{
 private:
    int counter_ = 0;
    
 public:
    int operator()(int i){return (counter_ += i);}
}

int main()
{
	Accumulator acc;
    std::cout << acc(10); << std::endl;
    std::cout << acc(20); << std::endl;
    
    return 0;
}
```

https://github.com/isocpp/CppCoreGuidelines