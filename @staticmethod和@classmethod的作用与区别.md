一般来说，要使用某个类的方法，需要先实例化一个对象再调用方法。

而使用@staticmethod或@classmethod，就可以不需要实例化，直接类名.方法名()来调用。这有利于组织代码，把某些应该属于某个类的函数给放到那个类里去，同时有利于命名空间的整洁。

既然@staticmethod和@classmethod都可以直接类名.方法名()来调用，那他们有什么区别呢？从它们的使用上来看：
- @staticmethod不需要表示自身对象的self和自身类的cls参数，就跟使用函数一样。
- @classmethod也不需要self参数，但第一个参数需要是表示自身类的cls参数。

如果在@staticmethod中要调用到这个类的一些属性方法，只能直接类名.属性名或类名.方法名。

而@classmethod因为持有cls参数，可以来调用类的属性，类的方法，实例化对象等，避免硬编码。
下面上代码：
```
class A(object):  
     bar = 1
  def foo(self):  
    print'foo'
    
  @staticmethod
  def static_foo():  
    print'static_foo'
    print A.bar
    
  @classmethod
  def class_foo(cls):  
    print'class_foo'
    printcls.bar  
    cls().foo()  
    
  A.static_foo()  
  A.class_foo() 
```
输出内容如下：
```
输出
static_foo
1
class_foo
1
foo
```

