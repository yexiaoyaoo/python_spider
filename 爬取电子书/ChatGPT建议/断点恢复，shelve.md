要实现断点恢复的功能，你需要记录下你每次爬取的章节的url和页码，并保存在一个文件或者数据库中。然后，当你重新运行你的爬虫时，你需要先检查这个文件或数据库，看看上次爬取到哪里，然后从那里继续爬取。这样，你就可以实现断点恢复的功能了。

具体来说，你可以在你的代码中加入以下几个步骤：

1. 在你的代码开头，导入一个模块，比如`pickle`或者`shelve`，用来保存和读取你的爬取进度。
2. 在你的代码中定义一个变量，比如`progress`，用来存储你每次爬取的章节的url和页码。初始值可以设为一个空字典。
3. 在你开始爬取之前，先尝试打开一个文件，比如`progress.pkl`或者`progress.db`，用来读取上次保存的进度。如果文件存在且不为空，则将文件中的内容赋值给`progress`变量。如果文件不存在或为空，则跳过这一步。
4. 在你每次爬取一个章节时，将该章节的url和页码添加到`progress`变量中，并更新该变量。同时，在每次爬取完一个章节后，将`progress`变量保存到文件中，以备下次使用。
5. 在你完成所有爬取或者遇到异常中断时，关闭并删除文件。

shelve是一个Python模块，用于将对象存储在文件中。shelve模块实现了对任意可以被pickle模块处理的Python对象的持久化存储，使用类似于字典的API。当关系型数据库过于复杂时，shelve模块可以作为一个简单的持久化存储选项²⁴。

shelve模块中定义了一个shelf对象，它是一个类似于字典的对象，它被持久地存储在磁盘文件中。这个文件类似于UNIX系统上的dbm数据库。shelf对象中的键是字符串，值是Python对象²³。

shelve模块是Python标准库中的一个实用模块，所以不需要额外安装。你可以使用`import shelve`来导入这个模块。

shelve模块中有以下几个类和函数：

- 类`Shelf`：它是collections.abc.MutableMapping的一个子类，它将pickle化的值存储在字典对象中。这个类中有以下几个函数：
    - `get(key, default=None)`：返回shelf对象中与key对应的值，如果key不存在，则返回default。
    - `close()`：同步并关闭持久化字典对象。在一个关闭的shelf对象上进行操作会抛出ValueError异常。
    - `sync()`：如果shelf对象是以writeback参数为True打开的，则将缓存中的所有条目写回文件。同时，清空缓存并同步磁盘上的持久化字典，如果可行的话。这个函数会在shelf对象关闭时自动调用。
- 类`BsdDbShelf`：Shelf的一个子类，它暴露了一些在第三方bsddb模块（来自pybsddb）中可用的函数，但在其他数据库模块中不可用。这些函数包括`first()`，`next()`，`previous()`，`last()`和`set_location()`。传递给构造函数的字典对象必须支持这些函数。这个类中有以下几个函数：
    - `set_location(key)`：将游标移动到与key对应的位置，并返回(key, value)对。
    - `next()`：将游标移动到下一个位置，并返回(key, value)对。
    - `previous()`：将游标移动到上一个位置，并返回(key, value)对。
    - `first()`：将游标移动到第一个位置，并返回(key, value)对。
    - `last()`：将游标移动到最后一个位置，并返回(key, value)对。
- 类`DbfilenameShelf`：Shelf的一个子类，它接受一个文件名而不是一个类似于字典的对象。底层的文件会使用dbm.open()打开。默认情况下，文件会被创建并打开以供读写。这个类只包含一个构造函数。

要使用shelve模块，你可以参考以下几个步骤：

1. 使用`shelve.open(filename, flag='c', protocol=None, writeback=False)`函数来创建或打开一个持久化字典。filename参数指定了底层数据库文件的基本文件名。作为副作用，可能会给文件名添加一个扩展名，并且可能会创建多个文件。默认情况下，底层数据库文件会被打开以供读写。可选的flag参数有着与dbm.open()函数相同的含义。默认情况下，使用pickle.DEFAULT_PROTOCOL来序列化值。可以使用protocol参数来指定pickle协议的版本。由于Python语义的限制，shelf对象无法知道何时修改了一个可变的持久化字典条目。默认情况下，只有当对象被赋值给shelf时才会写入修改过的对象。如果可选的writeback参数被设置为True，所有访问过的条目也会被缓存在内存中，并在sync()和close()时写回；这可以使得更方便地修改持久化字典中的可变条目，但是，如果访问了很多条目，它可能会消耗大量的内存来存储缓存，而且它可能会使得close操作非常慢，因为所有访问过的条目都会被写回（没有办法确定哪些访问过的条目是可变的，也没有办法确定哪些实际上被修改了）。
2. 使用类似于字典的方法和操作来操作shelf对象。shelf对象支持大多数字典支持的方法和操作（除了复制、构造函数和运算符|和|=）。这可以使得从基于字典的脚本转换到需要持久化存储的脚本更加容易。另外，还有两个额外的方法：
    - `Shelf.sync()`：如果shelf对象是以writeback参数为True打开的，则将缓存中的所有条目写回文件。同时，清空缓存并同步磁盘上的持久化字典，如果可行的话。这个函数会在shelf对象关闭时自动调用。
    - `Shelf.close()`：同步并关闭持久化字典对象。在一个关闭的shelf对象上进行操作会抛出ValueError异常。
3. 不要依赖shelf对象被自动关闭；总是在不再需要它时显式地调用close()，或者使用shelve.open()作为一个上下文管理器：
```python
with shelve.open('spam') as db:
    db['eggs'] = 'eggs'
```

