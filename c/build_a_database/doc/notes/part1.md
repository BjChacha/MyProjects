## Sqlite

一次询问（query）一般经历一系列流程，来取出或修改数据。前端包括：

- tokenizer
- parser
- code generator

前端的输入是一次SQL询问，输出是sqlite虚拟机可操作的二进制代码。

后端包括：

- virtual machine
- B-tree
- pager
- os interaface

**虚拟机**接收前端输出的二进制码，执行其中表示的操作，操作一个或多个表或者索引。操作的对象以B树的数据格式储存。VM实质上是一个大型switch-case代码。

每个**B树**包含很多节点，每个节点表示一页。B树可以从硬盘中取出一页数据，或者将数据通过pager保存到硬盘中。

**Pager**接收指令来读写数据。它主要负责对读写操作给予在文件中合适的偏移。它也在内存中为近期访问的页维护一个缓存区，并决定哪些页需要被写回到硬盘中。

**os interface**负责区分sqlite编译在哪些操作系统。这里不考虑多平台支持。

## 写一个简单的REPL