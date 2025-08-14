# cython: subinterpreters_compatible = own_gil
# distutils: extra_compile_args="-DCYTHON_USE_MODULE_STATE=1"

# This benchmark is not designed to be run regularly. It's mainly
# a tool for investigating performance of the subinterpreters
# module state lookup.
#
# Note that it has an accompanying pxd file.
#
# run_many_benchmarks runs it on a range of different numbers of interpreters
# and is probably the most useful function to run. 

try:
    import cython
except:
    class cython:
        NULL = 0
        compiled=False

from time import monotonic

if not cython.compiled:
    def __Pyx_State_FindModule(arg):
        return 1

# interpreters_backport unfortunately has a different interface
from concurrent import interpreters

def _run_on_interpreter(n_loops: cython.int, can_proceed_queue, result_queue):
    can_proceed_queue.get()

    then = monotonic()
    try:
        for _ in range(n_loops):
            assert __Pyx_State_FindModule(cython.NULL) != cython.NULL
        now = monotonic()
    except:
        print("BAD!")
        result_queue.put(float('inf'))
        raise
    else:
        result_queue.put(now-then)
    finally:
        can_proceed_queue.put(None)


def run_benchmark(n_interpreters, n_simultaneous, n_loops, print_result=True):
    """
    Runs the benchmark for a fixed number of interpreters.
    n_simultaneous controls how many interpreters are allowed to run
    at once to investigate the effect of contention.
    1000000 is a good initial number for n_loops.
    """
    result_queue = interpreters.create_queue()
    can_proceed_queue = interpreters.create_queue()

    all_interpreters = [
        interpreters.create() for _ in range(n_interpreters-1)
    ]

    for i in all_interpreters:
        i.call_in_thread(_run_on_interpreter, n_loops, can_proceed_queue, result_queue)

    for _ in range(n_simultaneous):
        can_proceed_queue.put(None)

    # and on the main interpreter too
    _run_on_interpreter(n_loops, can_proceed_queue, result_queue)

    n_results = 0
    total_time = 0
    while n_results < n_interpreters:
        total_time += result_queue.get()
        n_results += 1

    if print_result:
        print(f"{n_interpreters=} {n_simultaneous=}: {total_time/n_results} s")
    return total_time/n_results

def run_many_benchmarks(n_interpreters_list, n_simultaneous, n_loops):
    """
    Run the benchmark on a list of different interpreter sizes.
    n_interpreters list can be None, in which case some default sizes are used.
    n_simultaneous and n_loops are passed to run_benchmark so have the same
    meaning as there.
    """
    from concurrent.futures import ProcessPoolExecutor
    if n_interpreters_list is None:
        # some default values
        n_interpreters_list = (
            list(range(1, 10)) +
            list(range(10, 50, 20)) +
            list(range(50, 200, 50)) +
            list(range(200, 500, 250)) +
            [500]
        )
    n_interpreters_list = [
        ni for ni in n_interpreters_list
        if ni >= n_simultaneous
    ]

    print("n_interrpeters\ttime (s)")
    for n_interpreters in n_interpreters_list:
        # Run a fresh process for each one to clear Cython static data
        executor = ProcessPoolExecutor()
        bm = executor.submit(
            run_benchmark,
            n_interpreters, n_simultaneous, n_loops,
            print_result=False
        ).result()
        print(f"{n_interpreters}\t{bm}")
