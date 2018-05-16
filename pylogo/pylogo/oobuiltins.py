import types
#from cStringIO import StringIO
from io import StringIO    # for handling unicode strings
from pylogo.builtins import _join, logo_soft_repr
import pylogo.interpreter
from pylogo.common import *

class Writer(object):
    def __init__(self, output):
        self._output = output

    @logofunc(aliases=['print'], arity=-1)
    def pr(self, *args):
        trans = []
        for arg in args:
            if isinstance(arg, list):
                trans.append(_join(map(logo_soft_repr, arg)))
            else:
                trans.append(logo_soft_repr(arg))
        self._output.write(' '.join(trans))
        self._output.write('\n')

    @logofunc(name='type', arity=-1)
    def logo_type(self, *args):
        trans = []
        for arg in args:
            if isinstance(arg, list):
                trans.append(_join(map(logo_soft_repr, arg)))
            else:
                trans.append(logo_soft_repr(arg))
        self._output.write(' '.join(trans))

    def show(self, *args):
        self._output.write(' '.join(map(repr(args))))
        self._output.write('\n')

    def writer(self):
        return self

    def setwritepos(self, charpos):
        """
        SETWRITEPOS charpos
        
	command.  Sets the file pointer of the write stream file so
	that the next PRINT, etc., will begin writing at the
	``charpos`` character in the file, counting from 0.  (That is,
	SETWRITEPOS 0 will start writing from the beginning of the
	file.)  Meaningless if the write stream is the terminal.
        """
        self.output.seek(charpos)

    def writepos(self):
        """
        WRITEPOS
        
	outputs the file position of the current write stream file.
        """
        return self.output.tell()

    
class Reader(object):

    def __init__(self, input):
        self.input = input

    def reader(self):
        return self

    def setreadpos(self, charpos):
        """
        SETREADPOS charpos
        
	command.  Sets the file pointer of the read stream file so
	that the next READLIST, etc., will begin reading at the
	``charpos`` character in the file, counting from 0.  (That is,
	SETREADPOS 0 will start reading from the beginning of the
	file.)  Meaningless if the read stream is the terminal.
        """
        self.input.seek(charpos)
        
    def readpos(self):
        """
        READPOS
        
	outputs the file position of the current read stream file.
        """
        return self.input.tell()

    @logofunc(aliases=["eof?"])
    def eofp(self):
        """
        EOFP
        EOF?

	predicate, outputs TRUE if there are no more characters to be
	read in the read stream file, FALSE otherwise.
        """
        fn = self.input.name
        size = os.stat(fn).st_size
        return self.input.tell() >= size

class CaptureWriter(Writer):

    logo_class = True

    def __init__(self):
        super(CaptureWriter, self).__init__(StringIO())

    def writervalue(self):
        return self._output.getvalue()

@logofunc(aware=True, name='create')
def logo_create(interp, superclass, name, block):
    frame = interp.new()
    methods = {}
    def set_function(name, func):
        methods[name] = func
    def get_function(name):
        if name in methods:
            return methods[name]
        else:
            return frame.__class__.get_function(frame, name)
    frame.set_function = set_function
    frame.get_function = get_function
    frame.eval(block)
    frame.vars.update(methods)
    if hasattr(superclass, '__logo_create__'):
        new = superclass.__logo_create__(name, frame.vars)
    elif not isinstance(superclass, (types.ClassType, type)):
        new = superclass.__class__()
        new.__dict__.update(superclass.__dict__)
        for a_name, a_value in frame.vars.items():
            if isinstance(a_value, interpreter.UserFunction):
                a_value = interpreter.BoundUserFunction(a_value, new)
            setattr(new, a_name, a_value)
    else:
        new = type(superclass)(name, (superclass,), frame.vars)
        new.logo_class = True
    interp.set_variable(name, new)
    interp.set_function(name, new)
    return new

@logofunc(aware=True)
def actor(interp, the_actor):
    """
    ACTOR object

    Adds the actor to the top of the actor list, so that commands will
    be passed to the actor first.
    """
    interp.push_actor(the_actor)

@logofunc(aware=True)
def actors(interp):
    """
    ACTORS

    outputs all the actors; the first object in the list is the
    topmost actor that gets first chance at commands.
    """
    return interp.actors

@logofunc(aware=True, arity=1)
def removeactor(interp, the_actor=None):
    """
    REMOVEACTOR object

    Remove the actor from the actor list.  If the actor does not
    appear on the list, it will be an error.  If the actor is None or
    [] then the most recent actor added with ACTOR will be removed.
    """
    if the_actor is None or the_actor == []:
        interp.pop_actor()
    else:
        interp.pop_actor(the_actor)
    
def oobuiltins_main(interp):
    interp.set_variable('object', object)



############################################################
## File access from UCBLogo
############################################################

_filename_prefix = None

@logofunc()
def setprefix(prefix):
    """
    SETPREFIX string

    command.  Sets a prefix that will be used as the implicit
    beginning of filenames in OPENREAD, OPENWRITE, OPENAPPEND,
    OPENUPDATE, LOAD, and SAVE commands.  Logo will put the
    appropriate separator character (slash for Unix, backslash for
    DOS/Windows, colon for MacOS) between the prefix and the filename
    entered by the user.  The input to SETPREFIX must be a word,
    unless it is the empty list, to indicate that there should be no
    prefix.

    @@ Note: LOAD and SAVE don't use this
    """
    global _filename_prefix
    # @@: Should this be interpreter-local?
    if not prefix:
        _filename_prefix = None
    else:
        _filename_prefix = prefix

@logofunc()
def prefix():
    """
    PREFIX

    outputs the current file prefix, or None if there is no prefix.
    See SETPREFIX.

    @@ Note: None instead of [] like in ucblogo
    """
    return _filename_prefix

@logofunc(hide=True)
def _filename(filename):
    if _filename_prefix is not None:
        filename = os.path.join(_filename_prefix, filename)
    return filename

@logofunc()
def openread(filename):
    """
    OPENREAD filename
    
    command.  Opens the named file for reading.  The read position is
    initially at the beginning of the file.

    Use ``ACTOR OPENREAD filename`` to take all input from the given
    file.
    """
    f = open(_filename(filename))
    return Reader(f)

@logofunc()
def openwrite(filename):
    """
    OPENWRITE filename
    
    command.  Opens the named file for writing.  If the file already
    existed, the old version is deleted and a new, empty file created.

    Use ``ACTOR OPENWRITE filename`` to put all output to the given
    file.
    """
    f = open(_filename(filename), 'w')
    return Writer(f)

@logofunc()
def openappend(filename):
    """
    OPENAPPEND filename

    command.  Opens the named file for writing.  If the file already
    exists, the write position is initially set to the end of the old
    file, so that newly written data will be appended to it.

    Use ``ACTOR OPENAPPEND filename`` to put all output to the given
    file.
    """
    f = open(_filename(filename), 'a')
    return Writer(f)

# @@: not done: OPENUPDATE

@logofunc(aware=True)
def close(interp, filename):
    """
    CLOSE filename
    
    command.  Closes the named file, or file object.
    """
    if isinstance(filename, basestring):
        filename = _filename(filename)
        for actor in interp.actors:
            if isinstance(actor, Reader):
                f = actor.input
                if getattr(f, 'name', None) == filename:
                    break
            elif isinstance(actor, Writer):
                f = actor.output
                if getattr(f, 'name', None) == filename:
                    break
        else:
            raise ValueError(
                "No file with the name %r found in the actor list"
                % filename)
    else:
        f = filename
    if isinstance(f, Reader):
        f.input.close()
    else:
        f.output.close()
    if f in interp.actors:
        interp.actors.remove(f)

@logofunc(aware=True)
def allopen(interp):
    """
    ALLOPEN

    outputs a list whose members are the file objects currently open.
    This list does not include the dribble file, if any.
    """
    result = []
    for actor in actors:
        if isinstance(actor, (Reader, Writer)):
            result.append(actor)
    return result

@logofunc(aware=True)
def closeall(interp):
    """
    CLOSEALL

    command.  Closes all open files.  Abbreviates
    FOREACH ALLOPEN [CLOSE ?]
    """
    for f in allopen(interp):
        close(interp, f)

@logofunc(aliases=['erf'])
def erasefile(filename):
    """
    ERASEFILE filename
    ERF filename

    command.  Erases (deletes, removes) the named file, which should not
    currently be open.
    """
    os.unlink(_filename(filename))

# @@: Not implemented: DRIBBLE NODRIBBLE
# @@: Not applicable: SETREAD, SETWRITE
# @@: Not the same: READER, WRITER

@logofunc(aliases=["file?"])
def filep(filename):
    """
    FILEP filename
    FILE? filename

    predicate, outputs TRUE if a file of the specified name exists
    and can be read, FALSE otherwise.
    """
    return os.path.exists(_filename(filename))
