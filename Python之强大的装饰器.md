Python有大量强大又贴心的特性，如果要列个最受欢迎排行榜，那么装饰器绝对会在其中。

刚接触装饰器，会觉得代码不多却难以理解。其实装饰器的语法本身挺简单的，复杂是因为同时混杂了其它的概念。下面我们一起抛去无关概念，简单地理解下Python的装饰器。本文只会讲解函数装饰器而不牵涉到类装饰器。
<!-- more -->
### 装饰器的原理
通过一个例子直观的感受下`python`的装饰器。
```
def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print('hello world')
        return func(*args, **kw)
    return wrapper

@log
def now():
    print('2015-3-25')
```

`log`就是一个装饰器。被`log`装饰的`now`，执行`now()`方法时都会打印`hello world`。

### 理解装饰器的准备工作

接下来我们分成三部分来做准备工作。

#### 函数亦是对象
在`python`中`万物`皆是对象，当然这的`万物`自然也包括函数了。

我们定义个`print_str`函数。这时`print_str`也是个对象，它能做所有对象的操作。

```
def print_str():
    return 'hello world'
```
所有对象都有三种特性: id、类型、值。接下来就看看函数是否有这三种特性。
```
id(print_str)
139764090382048
type(print_str)
<type 'function'>
print_str
<function print_str at 0x7f1d5cf5a6e0>
```
所以函数也是对象，跟其他对象一样也可以被赋值给其它变量。同时可以当参数传递，也可以当返回值。

#### @是个语法糖

装饰器的@没有做什么特别的事，不用它也可以实现一样的功能，只不过需要更多的代码。
```
@log
def now():
    print('2015-3-25')
```
上面的代码等价于下面：
```
def now():
    print('2015-3-25')
now = log(now)
```
`log`是个函数，它要求入参是函数对象，返回值是函数对象。`@`的语法糖其实是省去了上面最后一行代码，使可读性更好。用了装饰器后，每次调用`now`，真正调用的是`log`返回的函数对象。

#### 嵌套函数和闭包

Python的函数可以嵌套定义。

```
def outer():
    print('Before def:', locals())
    def inner():
        pass
    print('After def:', locals())
    return inner
```

`inner`是在`outer`内定义的，所以算`outer`的局部变量。执行到`def inner`时函数对象才创建，因此每次调用`outer`都会创建一个新的`inner`。下面可以看出，每次返回的`inner`是不同的。
```
outer()
Before def: {}
After def: {'inner': <function outer.<locals>.inner at 0x7f0b18fa0048>}
<function outer.<locals>.inner at 0x7f0b18fa0048>

outer()
Before def: {}
After def: {'inner': <function outer.<locals>.inner at 0x7f0b18fa00d0>}
<function outer.<locals>.inner at 0x7f0b18fa00d0>
```
说到嵌套函数就不得不提闭包，在这里只说下闭包的两个特点：
1. `inner`能访问`outer`及其祖先函数的命名空间内的变量(局部变量，函数参数)。
2. 调用`outer`已经返回了，但是它的命名空间被返回的`inner`对象引用，所以还不会被回收。

### 用函数实现装饰器

装饰器要求入参是函数对象，返回值是函数对象，嵌套函数完全能胜任。

这里我们还是使用上边的例子：
```
def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print('hello world')
        return func(*args, **kw)
    return wrapper

@log
def now():
    print('2015-3-25')
    
now()
```

注意：因为返回的`wrapper`还在引用着，所以存在于`log`命名空间的`func`不会消失。`log`可以装饰多个函数，`wrapper`不会调用混淆，因为每次调用`log`，都会有创建新的命名空间和新的`wrapper`。

### 实现带参数的装饰器？

带参数的装饰器，有时会异常的好用。我们看个例子。
```
@log('DEBUG')
def now():
    print('2015-3-25')

now()
DEBUG: hello world
2015-3-25
```

怎么做到的呢？其实这跟装饰器语法没什么关系。去掉@语法糖会变得很容易理解。
```
@log('DEBUG')
def now():
    print('2015-3-25')
```
等价于
```
def now():
    print('2015-3-25')
unnamed_decorator = log('DEBUG')
now = unnamed_decorator(now)
```

上面代码中的`unnamed_decorator`才是真正的装饰器，`log`是个普通的函数，它的返回值是装饰器。

来看一下具体实现的代码:
```
def log(level):
    print('Create decorator')

    # 这部分跟通常的装饰器一样，只是wrapper通过闭包访问了变量level
    def decorator(func):
        print('Initialize')

        def wrapper(*args, **kw):
            print('%s: Hellow World' % level)
        return wrapper
    # log 返回装饰器
    return decorator
```
### functools.wraps

Python的装饰器倍感贴心的地方是对调用方透明。调用方完全不知道也不需要知道调用的函数被装饰了。这样我们就能在调用方的代码完全不改动的前提下，给函数patch功能，重要的事情讲三遍：patch，patch，patch。

为了对调用方透明，装饰器返回的对象要伪装成被装饰的函数。伪装得越像，对调用方来说差异越小。有时光伪装函数名和参数是不够的，因为`Python`的函数对象有一些元信息调用方可能读取了。为了连这些元信息也伪装上，`functools.wraps`出场了。它能用于把被调用函数的`__module__`，`__name__`，`__qualname__`，`__doc__`，`__annotations__`赋值给装饰器返回的函数对象。

使用`functools.wraps`的情况：
```
def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print('hello world')
        return func(*args, **kw)
    return wrapper
```
不使用`functools.wraps`的情况：
```
def log(func):
    def wrapper(*args, **kw):
        print('hello world')
        return func(*args, **kw)
    return wrapper
```
对比一下效果两种情况的效果：
```
@log
def now():
    print('2015-3-25')
```

不用functools.wraps的结果：
```
now.__name__

'wrapper' 
```
用functools.wraps的结果:
```
now.__name__

'now'
```
很明显，结果一目了然。实现装饰器时往往不知道调用方会怎么用，所以养成好习惯加上`functools.wraps`吧。

传送门：[简单地理解 Python 的装饰器](http://www.lightxue.com/understand-python-decorator-the-easy-way)
告侵删。