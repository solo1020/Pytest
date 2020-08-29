# Pytest 笔记

#### 常用命令：
pytest --collect-only 查看收集了哪些用例      
pytest --cache-clear    

#### Pytest 搜索用例规则
默认从当前目录搜索测试用例，即在哪个目录下允许pytest命令，就在哪个目录下搜索  

1. 收集test_开头或 _test结尾的的文件
2. 收集这些文件中test开头方法, 包括Test开头的测试类中的 test前缀方法，
和不在Test 类中的test前缀方法 
-----> 非Test开头的类中test前缀方法是否收集?
不收集
---

以上是指未带任何参数的情况，也可以指定参数：  
===

两种方式指定收集用例的参数：  

1. 命令行参数手动指定路径  
    - 手动指定忽略目录：即忽略该目录  
> --ignore 参数指定忽略目录或文件 可以指定多个  
pytest --ignore=tests/foobar/test_foobar_03.py --ignore=tests/hello/   
也支持 pytest --ignore-glob='*_01.py'  

```
tests/
|-- example
|   |-- test_example_01.py
|   |-- test_example_02.py
|   '-- test_example_03.py
|-- foobar
|   |-- test_foobar_01.py
|   |-- test_foobar_02.py
|   '-- test_foobar_03.py
'-- hello
    '-- world
        |-- test_world_01.py
        |-- test_world_02.py
        '-- test_world_03.py

=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-5.x.y, py-1.x.y, pluggy-0.x.y
rootdir: $REGENDOC_TMPDIR, inifile:
collected 5 items

tests/example/test_example_01.py .                                   [ 20%]
tests/example/test_example_02.py .                                   [ 40%]
tests/example/test_example_03.py .                                   [ 60%]
tests/foobar/test_foobar_01.py .                                     [ 80%]
tests/foobar/test_foobar_02.py .                                     [100%]

========================= 5 passed in 0.02 seconds ========================

``` 

2. 在 pytest.ini 文件中指定 [ 不支持中文 ]   
    - addopts 指定命令行执行参数 ==> 等价于 pytest --参数
    - testpaths 指定查找目录：即只在指定目录查找  
    - norecursedirs 指定忽略目录：递归查找时忽略的目录  
    
```
# content of pytest.ini
[pytest]
addopts = --maxfail=2 -rf  # exit after 2 failures, report fail info
testpaths = testing doc    # 在testing doc 两个目录搜索用例testcase
norecursedirs = tmp*       # 指定所有tmp前缀文件夹 为递归查找用例白名单目录
```

3. 在conftest.py配置文件中指定
    - 通过参数 collect_ignore 指定忽略文件(目录是否可以?)
    - 通过参数 collect_ignore_glob 模糊匹配指定忽略文件
```
# content of conftest.py
import sys

collect_ignore = ["setup.py"]
if sys.version_info[0] > 2:
    collect_ignore.append("pkg/module_py2.py")
    collect_ignore_glob = ["*_py2.py"]
```

4. 修改 pytest收集用例的文件规则：  
    - 修改测试类收集规则
    - 修改测试文件或模块名收集规则
    - 修改测试方法收集规则
```
[pytest]  
python_classes = *Suite     # 则只查找 Suite结尾的 Test 类  
python_files = test_*.py check_*.py example_*.py  # 指定的文件名或模块名形式 为pytest的收集规则
python_functions = *_test   # 指定测试方法testcase 收集规则  
```  
5. unittest.TestCase 的子类 无视以上规则, 因为unittest自身框架会收集这些case  

Pytest中用例执行
===
先搜索到的先执行  
问题：如何自定义顺序?  

Pytest测试结果
===
A dot (.) means that the test passed.  
An F means that the test has failed.  
An E means that the test raised an unexpected exception.  

Pytest 断言assert
===
1. 普通断言：

****************************************************

2. 预期异常断言
    - 断言异常的类型  
with pytest.raises(ZeroDivisionError) as excinfo:  
    ...预期在此处抛出指定异常  
assert excinfo.type == 指定异常 (ZeroDivisionError)  
    - 断言异常的内容
assert "division by zero" in str(excinfo.value)  
```
import pytest

def test_zero_division():
    with pytest.raises(ZeroDivisionError) as excinfo:
        1 / 0

    # 断言异常类型
    assert excinfo.type == ZeroDivisionError

    # 断言异常的内容
    assert "division by zero" in str(excinfo.value)

```
   - xfail 断言  
@pytest.mark.xfail(raises=IndexError)
```
@pytest.mark.xfail(raises=IndexError)
def test_f():
    f()
```

****************************************************
 
3. 断言预期warnning
    - 断言warnning内容  
```
import warnings  
import pytest  

def test_warning():  
    with pytest.warns(UserWarning):  
        warnings.warn("my warning", UserWarning) 

pytest.warns(expected_warning, func, *args, **kwargs)
pytest.warns(expected_warning, "func(*args, **kwargs)") 
```

****************************************************

4. 自定义失败断言信息
> 可以通过在conftest.py中重写pytest_assertrepr_compare来实现：    
自定义assert 断言的 左边 右边 的一个比较结果  
相当于 Java的重写 对象 compareTo() equals() 方法, 下面的例子中 将判断相等的依据重写为 对象的 val值的比较  

```
# content of conftest.py
from test_foocompare import Foo

def pytest_assertrepr_compare(op, left, right):
    if isinstance(left, Foo) and isinstance(right, Foo) and op == "==":
        return [
            "Comparing Foo instances:",
            "   vals: {} != {}".format(left.val, right.val),
        ]

# content of test_foocompare.py
class Foo:
    def __init__(self, val):
        self.val = val

    def __eq__(self, other):
        return self.val == other.val

def test_compare():
    f1 = Foo(1)
    f2 = Foo(2)
    assert f1 == f2
```

Pytest setup / teardown
===
支持经典Junit风格的 setup teardown 方法  
* module 级别
> 对整个module 内的testcase 执行一次setup teardown  
> pytest 3.0 参数module 可选  
> def setup_module(module)  
> def teardown_module(module)  

****************************************************

* class 级别------对类中的所有testcase 执行一次
> 使用 @classmethod 类方法修饰符  
> @classmethod  
  def setup_class(cls)  
> @classmethod  
  def teardown_class(cls)  

****************************************************

* method 级别-----每个testcase 或方法都会进行调用
   - Test 类中的 testcase/方法  
   > def setup_method(self, method)  
   > def teardown_method(self, method)  
   > pytest 3.0 method 可选  
   - 直接在module/ 文件中定义的 testcase/方法
   > def setup_function(function)  
   > def teardown_function(function)  
   > pytest 3.0 method 可选

Pytest Fixtures
====

1.用于多个testcase 共享测试数据输入：  
如何传递参数给fixture方法：  

```
class MyTester:
    def __init__(self, x):
        self.x = x

    def dothis(self):
        assert self.x

@pytest.fixture
def tester(tester_arg):
    """Create tester object"""
    return MyTester(tester_arg)

class TestIt:
    @pytest.mark.parametrize('tester_arg', [True, False])
    def test_tc1(self, tester):
       tester.dothis()
       assert 1
```
2.自动使用autouse  
```
from bs4 import BeautifulSoup
import pytest
import requests

class TestGoogle:
    @pytest.fixture(autouse=True)
    def _request_google_page(self, google):
        self._response = requests.get("https://www.google.com")
    
    def test_alive(self）：
        assert self._response.status_code == 200

    def test_html_title(self):
        soup = BeautifulSoup(self._response.content, "html.parser")
        assert soup.title.text.upper() == "GOOGLE"
```
@pytest.fixture(autouse=True) 方法会在当前Test类里面每个test方法执行时调用一次  
因此该方法返回的请求 response 每个test 方法是不一样的  
如果需要使用同一个response:  

设置fixtures函数的使用范围：  
fixture scopes (scope='class' scope='module' or scope='session')  

3.通过设置fixtures 函数的scope 来实现 setUp tearDown 功能  

4.  
```
import pytest

@pytest.fixture()
def resource():
    print("setup")
    yield "resource"
    print("teardown")

class TestResource(object):
    def test_that_depends_on_resource(self, resource):
        print("testing {}".format(resource))
```

Pytest Mark
====
标记testcase:  
如 @pytest.mark.database_access 标记数据库访问 testcase  
pytest -m database_access 即可只执行具有该标记的 testcase  
pytest -m "not database_access" 反选  

Pytest 配置文件：config/ini
===
1. pytest.ini
    - addopts 接收用户从命令行输入的参数
        > --rootdir 不能用在addopts 中 因为要根据rootdir去查找pytest.ini配置文件
        > addopts = --maxfail=2 -rf # exit after 2 failures, report fail info  

    - cache_dir 缓冲目录(默认在项目根目录)
    
    - testpaths= 设置搜索case的目录 路径分隔符为 / 即使在window平台 也使用/testcases/testCollectTestcase/invalidCases

    - -p no:cacheprovider  #在 pytest.ini中禁用cache缓存，该缓存一般用来重新执行上一次失败case

    - confcutdir 设置搜索conftest.py的目录

    - console_output_style 设置控制台输出风格
        > classic: 经典   
        > progress: pass
    - --trace-config 查看加载的插件

2. conftest.py
    - pytest_addoption 方法：
        > 接收命令行参数，一般是在内部通过执行 pytest.main(--testpaths=xxx )形式执行测试的时候传递的
    ```
    # content of conftest.py
    def pytest_addoption(parser):
        parser.addoption("--env",
                         action="store",
                         dest="environment",
                         default="test",
                         help="enviroment: test or prod")
    ```
    上述例子的作用是： 读取命令行参数 --env 存储到environment变量中，而在函数参数中添加request参数，并在函数内使用：
    request.config.getoption("enviroment") 这样就可以通过命令行来获取参数
    如果不想每次都在命令行输入 --env 可以将其放在pytest.ini中 但是 命令行的参数会覆盖pytest.ini   
    
退出测试：
===
pytest.exit("decide to stop the test run")

设置case 之间的关联：不仅限于 case的执行顺序，顺序可以使用mark.order=run 1,2,3 数字作顺序
===
```
@pytest.mark.dependency()
def test_long():
    pass

@pytest.mark.dependency(depends=['test_long])
def test_short():
    pass
```
#### test_short 这个case 只在 test_long 执行成功的时候才会执行
  
### 参数化
1. parametrize
    > indirect 参数标志 当前参数是传递给fixtures的参数
    > @pytest.mark.parametrize("myfixture",["1","2"],indirect=True) 
```
@pytest.fixture()
def myfixture(request):
    print("执行myfixture固件--%s" % request.param)
    return "你好"

class Test_pytest():
    @pytest.mark.parametrize("myfixture",["1","2"],indirect=True)
    def test_one(self,myfixture):
        print("test_one方法执行")
        print(myfixture)
        assert 1==1
```

2. fixture (夹具、固件)









其他
===
pytest --durations=3 查看耗时最慢的 3 个 testcase  
  
pytest --maxfail=2 指定最大失败数 即 失败两个case 后停止测试,可以用来冒烟测试?  
  

pytest.raise(TypeError) 预期抛出异常  
```
def test_raises_exception_on_non_string_arguments():
    with pytest.raises(TypeError):
        capital_case(9)
```
pytest.ini 配置文件：  
```
[pytest]
usefixtures = clean_db  # 列出应用到所有测试方法的 fixtures 函数
```
usefixtures 列出应用到所有测试方法的 fixtures 函数  
语义上与 @pytest.mark.usefixtures 的 marker 标记一样  

Logging:  
pytest.ini:  
[pytest]  
log_fomat = %(asctime)s %(levelname)s %(message)s  
log_data_format = %Y-%m-%d %H:%M:%S  
log_file = /path/log/file  
log_file_level  
log_file_format  
log_file_date_format  

request:  
* 通过命令行参数决定测试执行
如下： 根据命令行传递的 --cmdoopt= 选项的值来控制case的执行过程  

```
# content of test_sample.py
def test_answer(cmdopt):
    if cmdopt == "type1":
        print("first")
    elif cmdopt == "type2":
        print("second")
    assert 0

# content of conftest.py
import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--cmdopt", action="store", default="type1", help="my option: type1 or type2"
    )

@pytest.fixture
def cmdopt(request):
    return request.config.getoption("--cmdopt")
```






??? Testclass 中 test 方法自带 self 参数 如何调用其他方法





