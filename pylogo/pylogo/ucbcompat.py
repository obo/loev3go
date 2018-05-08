from pylogo.common import *

class UCBArray(list):
    def __init__(v, origin=1):
        list.__init__(v)
        self.origin = origin
    def __getitem__(self, i):
        return list.__getitem__(self, i-self.origin)
    def __setitem__(self, i, value):
        list.__setitem__(self, i-self.origin, value)

def array(size, origin=1):
    """
    ARRAY size
    (ARRAY size origin)
    
    outputs an array of ``size`` members (must be a positive integer),
    each of which initially is an empty list.  Array members can be
    selected with ITEM and changed with SETITEM.  The first member of
    the array is member number 1 unless an ``origin`` input (must be
    an integer) is given, in which case the first member of the array
    has that number as its index.  (Typically 0 is used as the origin
    if anything.)
    """
    # UCB: Arrays are printed by PRINT and friends, and can be typed
    # in, inside curly braces; indicate an origin with {a b c}@0.
    return UCBArray([[]]*size)

def mdarray(sizelist, origin=1):
    """
    MDARRAY sizelist
    (MDARRAY sizelist origin)

    outputs a multi-dimensional array.  The first input must be a list
    of one or more positive integers.  The second input, if present,
    must be a single integer that applies to every dimension of the array.
    Ex: (MDARRAY [3 5] 0) outputs a two-dimensional array whose members
    range from [0 0] to [2 4].
    """
    if len(sizelist) == 1:
        return array(sizelist[0], origin=origin)
    else:
        result = []
        for i in range(sizelist[0]):
            result.append(array(sizelist[1:], origin=origin))
        return UCBArray(result, origin=origin)

def listtoarray(lst, origin=1):
    """
    LISTTOARRAY list
    (LISTTOARRAY list origin)

    outputs an array of the same size as the input list, whose members
    are the members of the input list.
    """
    return UCBArray(lst, origin=origin)

def arraytolist(array):
    """
    ARRAYTOLIST array

    outputs a list whose members are the members of the input array.
    The first member of the output is the first member of the array,
    regardless of the array's origin.
    """
    return list(array)

def mditem(indexlst, array):
    """
    MDITEM indexlist array

    outputs the member of the multidimensional ``array`` selected by
    the list of numbers ``indexlist``.
    """
    while indexlst:
        array = array[indexlst[0]]
        indexlst = indexlst[1:]
    return array

def quoted(v):
    """
    QUOTED thing

    outputs its input, if a list; outputs its input with a quotation
    mark prepended, if a word.
    """
    ## @@: I'm not sure this is really meaningful in the same way as
    ## it would be in UCBLogo
    if isinstance(v, str):
        return '"%s' % v
    else:
        return v

def mdsetitem(indexlst, array, value):
    """
    MDSETITEM indexlist array value

    command.  Replaces the member of ``array`` chosen by ``indexlist``
    with the new ``value``.
    """
    if len(indexlst) == 1:
        array[indexlst[0]] = value
    else:
        mdsetitem(indexlst[1:], array[indexlst[0]], value)


@logofunc(name='.setitem')
def dotsetitem(index, array, value):
    """
    .SETITEM index array value
    
    command.  Changes the ``index``th member of ``array`` to be
    ``value``, like SETITEM, but without checking for circularity.
    WARNING: Primitives whose names start with a period are DANGEROUS.
    Their use by non-experts is not recommended.  The use of .SETITEM
    can lead to circular arrays, which will get some Logo primitives
    into infinite loops; and the loss of memory if a circular
    structure is released.
    """
    ## @@: None of this applies to PyLogo, which doesn't do those
    ## checks anyway, and can handle circular structures (though those
    ## structures can cause infinite loops, but that's not an uncommon
    ## bug anyway)
    setitem(index, array, value)

@logofunc(aware=True)
def push(interp, stackname, thing):
    """
    PUSH stackname thing

    command.  Adds the ``thing`` to the stack that is the value of the
    variable whose name is ``stackname``.  This variable must have a
    list as its value; the initial value should be the empty list.
    New members are added at the front of the list.
    """
    var = interp.get_variable(stackname)
    var.append(thing)

@logofunc(aware=True)
def pop(interp, stackname):
    """
    POP stackname

    outputs the most recently PUSHed member of the stack that is the
    value of the variable whose name is ``stackname`` and removes that
    member from the stack.
    """
    var = interp.get_variable(stackname)
    return var.pop()

@logofunc(aware=True)
def queue(interp, queuename, thing):
    """
    QUEUE queuename thing

    command.  Adds the ``thing`` to the queue that is the value of the
    variable whose name is ``queuename``.  This variable must have a
    list as its value; the initial value should be the empty list.
    New members are added at the back of the list.
    """
    var = interp.get_variable(queuename)
    var.append(thing)

@logofunc(aware=True)
def dequeue(interp, queuename):
    """
    DEQUEUE queuename

    outputs the least recently QUEUEd member of the queue that is the
    value of the variable whose name is ``queuename`` and removes that
    member from the queue.
    """
    var = interp.get_variable(queuename)
    return var.pop(0)

@logofunc(aliases=['array?'])
def arrayp(v):
    """
    ARRAYP thing
    ARRAY? thing
    
    outputs TRUE if the input is an array, FALSE otherwise.
    """
    return isinstance(v, UCBArray)

@logofunc(aliases=['backslashed?'])
def backslashedp(c):
    """
    BACKSLASHEDP char
    BACKSLASHED? char
    """
    ## outputs TRUE if the input character was originally entered into
    ## Logo with a backslash (\) before it or within vertical bars (|)
    ## to prevent its usual special syntactic meaning, FALSE
    ## otherwise.  (Outputs TRUE only if the character is a
    ## backslashed space, tab, newline, or one of ()[]+-*/=<>\":;\\~?|
    ## )
    ## @@: doesn't make sense for us.
    return False
    
def rawascii(c):
    """
    RAWASCII char
    
    outputs the integer (between 0 and 255) that represents the input
    character in the ASCII code.
    """
    ## @@: Interprets control characters as representing themselves.
    ## To find out the ASCII code of an arbitrary keystroke, use
    ## RAWASCII RC.
    return ord(c)

_prefix = ''
def setprefix(s):
    """
    SETPREFIX string

    command.  Sets a prefix that will be used as the implicit beginning
    of filenames in OPENREAD, OPENWRITE, OPENAPPEND, OPENUPDATE, LOAD,
    and SAVE commands.  Logo will put the appropriate separator
    character (slash for Unix, backslash for DOS/Windows, colon for
    MacOS) between the prefix and the filename entered by the user.
    The input to SETPREFIX must be a word, unless it is the empty list,
    to indicate that there should be no prefix.
    """
    global _prefix
    if s:
        _prefix = s
    else:
        _prefix = ''

def prefix():
    """
    PREFIX

    outputs the current file prefix, or [] if there is no prefix.
    See SETPREFIX.
    """
    return _prefix or LogoList([])

_files = {}

def openread(filename):
    """
    OPENREAD filename

    command.  Opens the named file for reading.  The read position is
    initially at the beginning of the file.
    """
    _files[filename] = open(_prefix + filename)

def openwrite(filename):
    """
    OPENWRITE filename

    command.  Opens the named file for writing.  If the file already
    existed, the old version is deleted and a new, empty file created.
    """
    _files[filename] = open(_prefix + filename, 'w')

def openappend(filename):
    """
    OPENAPPEND filename

    command.  Opens the named file for writing.  If the file already
    exists, the write position is initially set to the end of the old
    file, so that newly written data will be appended to it.
    """
    _files[filename] = open(_prefix + filename, 'a')

def openupdate(filename):
    """
    OPENUPDATE filename

    command.  Opens the named file for reading and writing.  The read and
    write position is initially set to the end of the old file, if any.
    Note: each open file has only one position, for both reading and
    writing.  If a file opened for update is both READER and WRITER at
    the same time, then SETREADPOS will also affect WRITEPOS and vice
    versa.  Also, if you alternate reading and writing the same file,
    you must SETREADPOS between a write and a read, and SETWRITEPOS
    between a read and a write.
    """
    _files[filename] = open(_prefix + filename, 'a+')
    
def close(filename):
    """
    CLOSE filename
    
    command.  Closes the named file.
    """
    _files[filename].close()

def allopen():
    """
    ALLOPEN

    outputs a list whose members are the names of all files currently open.
    This list does not include the dribble file, if any.
    """
    return LogoList(_files.keys())

def closeall():
    """
    CLOSEALL

    command.  Closes all open files.  Abbreviates
    FOREACH ALLOPEN [CLOSE ?]
    """
    for key, value in _files.items():
        del _files[key]
        value.close()

@logofunc(aliases=['erf'])
def erasefile(filename):
    """
    ERASEFILE filename
    ERF filename
    
    command.  Erases (deletes, removes) the named file, which should not
    currently be open.
    """
    os.unlink(_prefix + filename)

_in_dribble = False

class Dribbler:

    def __init__(self, capture, fileobj):
        self.capture = capture
        self.file = fileobj
        for n in ['read', 'readline', 'readlines']:
            setattr(self, n, self.cap(n))
        for n in ['write']:
            setattr(self, n, self.copy(n))

    def cap(self, attr):
        def func(*args):
            v = getattr(self.capture, attr)(*args)
            self.file.write(v)
            return v
        return func

    def copy(self, attr):
        def func(*args):
            self.write.write(''.join(args))
            getattr(self.capture, attr)(*args)
        return func

    def close(self):
        self.capture.close()
        self.file.close()

    def nodribble(self):
        self.file.close()
        return self.capture

def dribble(filename):
    """
    DRIBBLE filename

    command.  Creates a new file whose name is the input, like OPENWRITE,
    and begins recording in that file everything that is read from the
    keyboard or written to the terminal.  That is, this writing is in
    addition to the writing to WRITER.  The intent is to create a
    transcript of a Logo session, including things like prompt
    characters and interactions.
    """
    out = open(filename, 'w')
    sys.stdout = Dribbler(sys.stdout, out)
    sys.stdin = Dribbler(sys.stdin)
    # @@... unfinished

_plists = {}

def _getplist(plistname):
    if not _plists.has_key(plistname.lower()):
        _plists[plistname.lower()] = {}
    return _plists[plistname.lower()]

def pprop(plistname, propname, value):
    """
    PPROP plistname propname value

    command.  Adds a property to the ``plistname`` property list with
    name ``propname`` and value ``value``.
    """
    _getplist(plistname)[propname.lower()] = value

def gprop(plistname, propname):
    """
    GPROP plistname propname

    outputs the value of the ``propname`` property in the
    ``plistname`` property list, or the empty list if there is no such
    property.
    """
    try:
        return _getplist(plistname)[propname.lower()]
    except KeyError:
        return LogoList([])

def remprop(plistname, propname):
    """
    REMPROP plistname propname

    command.  Removes the property named ``propname`` from the
    property list named ``plistname``.
    """
    try:
        del _getplist(plistname)[propname.lower()]
    except KeyError:
        pass

def plist(plistname):
    """
    PLIST plistname

    outputs a list whose odd-numbered members are the names, and
    whose even-numbered members are the values, of the properties
    in the property list named ``plistname``.  The output is a copy
    of the actual property list; changing properties later will not
    magically change a list output earlier by PLIST.
    """
    v = []
    for key, value in _getplist(plistname):
        v.extend([key, value])
    return LogoList(v)

@logofunc(aliases=['plist?'])
def plistp(plistname):
    """
    PLISTP name
    PLIST? name

    outputs TRUE if the input is the name of a *nonempty* property
    list.  (In principle every word is the name of a property list; if
    you haven't put any properties in it, PLIST of that name outputs
    an empty list, rather than giving an error message.)
    """
    if not _plists.has_key(plistname.lower()):
        return False
    return not not _getplist(plistname)

def erpls():
    """
    ERPLS

    command.  Erases all unburied property lists from the workspace.
    Abbreviates ERASE PLISTS.
    """
    global _plists
    _plists = {}
