"""
More-or-less like doctest, except with Logo
"""

import os
import doctest
import sys
import traceback
from cStringIO import StringIO
import reader
import interpreter
from pylogo import builtins
from pylogo import oobuiltins

def testfile(filename, globs=None, name=None,
             verbose=None, optionflags=0,
             report=True, master=None,
             interp=None,
             verbose_summary=False):
    if globs is None:
        globs = {}
    if interp is None:
        interp = interpreter.RootFrame()
        interp.import_module(builtins)
        interp.import_module(oobuiltins)
    interp.vars.update(globs)
    if name is None:
        name = os.path.basename(filename)
    runner = LogoRunner(interp, verbose=verbose,
                        optionflags=optionflags)
    s = open(filename).read()
    parser = doctest.DocTestParser()
    test = parser.get_doctest(s, globs, name,
                              filename, 0)
    runner.run(test)
    if report:
        runner.summarize(verbose or verbose_summary)
    if master is None:
        master = runner
    else:
        master.merge(runner)
    return runner.failures, runner.tries

class LogoRunner(doctest.DocTestRunner):

    def __init__(self, interpreter, *args, **kw):
        doctest.DocTestRunner.__init__(self, *args, **kw)
        self.interpreter = interpreter
    
    def _DocTestRunner__run(self, test, compileflags, out):
        failures, tries = self._run(test, compileflags, out)
        self._DocTestRunner__record_outcome(test, failures, tries)
        return failures, tries

    #/////////////////////////////////////////////////////////////////
    # DocTest Running
    #/////////////////////////////////////////////////////////////////

    def _DocTestRunner__run(self, test, compileflags, out):
        """
        Run the examples in `test`.  Write the outcome of each example
        with one of the `DocTestRunner.report_*` methods, using the
        writer function `out`.  `compileflags` is the set of compiler
        flags that should be used to execute examples.  Return a tuple
        `(f, t)`, where `t` is the number of examples tried, and `f`
        is the number of examples that failed.  The examples are run
        in the namespace `test.globs`.
        """
        # Keep track of the number of failures and tries.
        failures = tries = 0

        # Save the option flags (since option directives can be used
        # to modify them).
        original_optionflags = self.optionflags

        SUCCESS, FAILURE, BOOM = range(3) # `outcome` state

        check = self._checker.check_output

        # Process each example.
        for examplenum, example in enumerate(test.examples):

            # If REPORT_ONLY_FIRST_FAILURE is set, then supress
            # reporting after the first failure.
            quiet = (self.optionflags & doctest.REPORT_ONLY_FIRST_FAILURE and
                     failures > 0)

            # Merge in the example's options.
            self.optionflags = original_optionflags
            if example.options:
                for (optionflag, val) in example.options.items():
                    if val:
                        self.optionflags |= optionflag
                    else:
                        self.optionflags &= ~optionflag

            # Record that we started this example.
            tries += 1
            if not quiet:
                self.report_start(out, test, example)

            # Use a special filename for compile(), so we can retrieve
            # the source code during interactive debugging (see
            # __patched_linecache_getlines).
            filename = '<doctest %s[%d]>' % (test.name, examplenum)

            # Run the example in the given context (globs), and record
            # any exception that gets raised.  (But don't intercept
            # keyboard interrupts.)
            try:
                # Don't blink!  This is where the user's code gets run.
                self.run_example(example.source, filename, compileflags, test.globs)
                self.debugger.set_continue() # ==== Example Finished ====
                exception = None
            except KeyboardInterrupt:
                raise
            except:
                exception = sys.exc_info()
                self.debugger.set_continue() # ==== Example Finished ====

            got = self._fakeout.getvalue()  # the actual output
            self._fakeout.truncate(0)
            outcome = FAILURE   # guilty until proved innocent or insane

            # If the example executed without raising any exceptions,
            # verify its output.
            if exception is None:
                if check(example.want, got, self.optionflags):
                    outcome = SUCCESS

            # The example raised an exception:  check if it was expected.
            else:
                exc_info = sys.exc_info()
                exc_msg = traceback.format_exception_only(*exc_info[:2])[-1]
                if not quiet:
                    got += doctest._exception_traceback(exc_info)

                # If `example.exc_msg` is None, then we weren't expecting
                # an exception.
                if example.exc_msg is None:
                    outcome = BOOM

                # We expected an exception:  see whether it matches.
                elif check(example.exc_msg, exc_msg, self.optionflags):
                    outcome = SUCCESS

                # Another chance if they didn't care about the detail.
                elif self.optionflags & doctest.IGNORE_EXCEPTION_DETAIL:
                    m1 = re.match(r'[^:]*:', example.exc_msg)
                    m2 = re.match(r'[^:]*:', exc_msg)
                    if m1 and m2 and check(m1.group(0), m2.group(0),
                                           self.optionflags):
                        outcome = SUCCESS

            # Report the outcome.
            if outcome is SUCCESS:
                if not quiet:
                    self.report_success(out, test, example, got)
            elif outcome is FAILURE:
                if not quiet:
                    self.report_failure(out, test, example, got)
                failures += 1
            elif outcome is BOOM:
                if not quiet:
                    self.report_unexpected_exception(out, test, example,
                                                     exc_info)
                failures += 1
            else:
                assert False, ("unknown outcome", outcome)

        # Restore the option flags (in case they were modified)
        self.optionflags = original_optionflags

        # Record and return the number of failures and tries.
        self._DocTestRunner__record_outcome(test, failures, tries)
        return failures, tries

    prompts = {
        None: '',
        'to': '',
        '[': '',
        '(': '',
        'func': '',
        }

    def run_example(self, source, filename,
                    compileflags, globs):
        input = StringIO(source)
        input = reader.TrackingStream(input, name=filename)
        tokenizer = reader.FileTokenizer(
            input, prompt=self.prompts)
        interp = self.interpreter
        interp.push_tokenizer(tokenizer)
        try:
            v = interp.expr_top()
            if v is not None:
                print builtins.logo_repr(v)
        finally:
            interp.pop_tokenizer()

if __name__ == '__main__':
    filenames = sys.argv[1:]
    for filename in filenames:
        if filename.startswith('-'):
            continue
        print "testing", filename
        testfile(filename)
        
